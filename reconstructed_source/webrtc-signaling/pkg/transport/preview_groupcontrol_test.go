package transport_test

import (
	"encoding/binary"
	"encoding/json"
	"strings"
	"testing"
	"time"

	"github.com/gorilla/websocket"

	"cloudphone-signaling/pkg/transport"
)

// TestStartPreviewAndRefcountLifecycle verifies GATE-WS-01, GATE-WS-05, and GATE-WS-06 contracts:
// - Client 1 start_preview triggers agent start_preview
// - Client 2 start_preview reuses stream (no duplicate agent relay)
// - Client 1 stop_preview does not stop agent stream while Client 2 is still subscribed
// - Client 2 disconnect automatically triggers stop_preview on agent
func TestStartPreviewAndRefcountLifecycle(t *testing.T) {
	server, _, _, _, _, adminToken, _ := setupTransportTestEnv(t)

	// 1. Connect and register agent for dev-1
	agentURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/register_agent"
	agentWS, _, err := websocket.DefaultDialer.Dial(agentURL, nil)
	if err != nil {
		t.Fatalf("dial agent error: %v", err)
	}
	defer agentWS.Close()

	if err := agentWS.WriteJSON(map[string]interface{}{
		"type":      "agent_register",
		"device_id": "dev-1",
		"is_webrtc": true,
	}); err != nil {
		t.Fatalf("agent_register write error: %v", err)
	}

	var ack transport.AgentRegisterOkMessage
	if err := agentWS.ReadJSON(&ack); err != nil || ack.MessageType != "agent_register_ok" {
		t.Fatalf("expected agent_register_ok, got err=%v ack=%+v", err, ack)
	}

	agentMsgs := make(chan []byte, 20)
	go func() {
		for {
			_, msg, err := agentWS.ReadMessage()
			if err != nil {
				return
			}
			agentMsgs <- msg
		}
	}()

	readAgentMsg := func(timeout time.Duration) ([]byte, bool) {
		select {
		case msg := <-agentMsgs:
			return msg, true
		case <-time.After(timeout):
			return nil, false
		}
	}

	// 2. Client 1 connects
	cli1URL := "ws" + strings.TrimPrefix(server.URL, "http") + "/connect_client?token=" + adminToken
	cli1WS, _, err := websocket.DefaultDialer.Dial(cli1URL, nil)
	if err != nil {
		t.Fatalf("dial client 1 error: %v", err)
	}
	defer cli1WS.Close()

	// Client 1 sends start_preview
	startMsg1 := transport.StartPreviewMessage{
		MessageType: "start_preview",
		DeviceID:    "dev-1",
		FPS:         30,
		Bitrate:     4000000,
	}
	if err := cli1WS.WriteJSON(startMsg1); err != nil {
		t.Fatalf("client 1 write start_preview error: %v", err)
	}

	// Agent should receive start_preview
	rawMsg, ok := readAgentMsg(2 * time.Second)
	if !ok {
		t.Fatalf("timed out waiting for agent to receive start_preview")
	}
	var agentMsg1 transport.StartPreviewMessage
	if err := json.Unmarshal(rawMsg, &agentMsg1); err != nil {
		t.Fatalf("unmarshal agent start_preview error: %v", err)
	}
	if agentMsg1.DeviceID != "dev-1" || agentMsg1.FPS != 30 {
		t.Errorf("unexpected agent start_preview msg: %+v", agentMsg1)
	}

	// 3. Client 2 connects and requests start_preview on same device
	cli2WS, _, err := websocket.DefaultDialer.Dial(cli1URL, nil)
	if err != nil {
		t.Fatalf("dial client 2 error: %v", err)
	}
	defer cli2WS.Close()

	if err := cli2WS.WriteJSON(startMsg1); err != nil {
		t.Fatalf("client 2 write start_preview error: %v", err)
	}

	// Agent should NOT receive another start_preview (wasFirst == false)
	if raw, ok := readAgentMsg(150 * time.Millisecond); ok {
		t.Errorf("expected no duplicate start_preview on agent, but got: %s", string(raw))
	}

	// 4. Client 1 stops preview
	stopMsg := transport.StopPreviewMessage{
		MessageType: "stop_preview",
		DeviceID:    "dev-1",
	}
	if err := cli1WS.WriteJSON(stopMsg); err != nil {
		t.Fatalf("client 1 write stop_preview error: %v", err)
	}

	// Agent should NOT receive stop_preview because Client 2 is still subscribed
	if raw, ok := readAgentMsg(150 * time.Millisecond); ok {
		t.Errorf("expected no stop_preview on agent while client 2 subscribed, but got: %s", string(raw))
	}

	// 5. Client 2 disconnects -> should trigger automatic stop_preview to agent!
	_ = cli2WS.Close()

	rawStop, ok := readAgentMsg(2 * time.Second)
	if !ok {
		t.Fatalf("expected agent to receive stop_preview after all subscribers left, timed out")
	}
	var agentStopMsg transport.StopPreviewMessage
	if err := json.Unmarshal(rawStop, &agentStopMsg); err != nil {
		t.Fatalf("unmarshal stop_preview error: %v", err)
	}
	if agentStopMsg.DeviceID != "dev-1" {
		t.Errorf("expected stop_preview for dev-1, got %+v", agentStopMsg)
	}
}

// TestBinaryPreviewRelayAndDeviceValidation verifies GATE-WS-03, GATE-WS-04, and boundDeviceID validation:
// - Agent binary PREV frame relayed to subscribed client
// - Spoofed frame with mismatched device_id dropped
func TestBinaryPreviewRelayAndDeviceValidation(t *testing.T) {
	server, _, _, _, _, adminToken, _ := setupTransportTestEnv(t)

	agentURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/register_agent"
	agentWS, _, err := websocket.DefaultDialer.Dial(agentURL, nil)
	if err != nil {
		t.Fatalf("dial agent error: %v", err)
	}
	defer agentWS.Close()

	_ = agentWS.WriteJSON(map[string]interface{}{
		"type":      "agent_register",
		"device_id": "dev-1",
	})
	var ack transport.AgentRegisterOkMessage
	_ = agentWS.ReadJSON(&ack)

	// Client connects and subscribes
	cliURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/connect_client?token=" + adminToken
	cliWS, _, err := websocket.DefaultDialer.Dial(cliURL, nil)
	if err != nil {
		t.Fatalf("dial client error: %v", err)
	}
	defer cliWS.Close()

	_ = cliWS.WriteJSON(transport.StartPreviewMessage{
		MessageType: "start_preview",
		DeviceID:    "dev-1",
	})
	// Drain start_preview on agent
	var dummy transport.StartPreviewMessage
	_ = agentWS.ReadJSON(&dummy)

	// Helper to build PREV frame
	makePrevFrame := func(devID string, payload []byte) []byte {
		buf := make([]byte, 49+len(payload))
		copy(buf[0:4], []byte("PREV"))
		copy(buf[4:36], []byte(devID))
		buf[36] = 1 // keyframe
		binary.BigEndian.PutUint64(buf[37:45], 123456)
		binary.BigEndian.PutUint32(buf[45:49], uint32(len(payload)))
		copy(buf[49:], payload)
		return buf
	}

	// 1. Agent sends valid frame for dev-1
	nalu := []byte{0x00, 0x00, 0x00, 0x01, 0x67, 0x42, 0x00, 0x1f}
	validFrame := makePrevFrame("dev-1", nalu)
	if err := agentWS.WriteMessage(websocket.BinaryMessage, validFrame); err != nil {
		t.Fatalf("write binary frame error: %v", err)
	}

	_ = cliWS.SetReadDeadline(time.Now().Add(2 * time.Second))
	msgType, data, err := cliWS.ReadMessage()
	if err != nil {
		t.Fatalf("client read binary frame error: %v", err)
	}
	if msgType != websocket.BinaryMessage {
		t.Errorf("expected BinaryMessage, got %d", msgType)
	}
	if string(data[0:4]) != "PREV" || len(data) != len(validFrame) {
		t.Errorf("frame content mismatch, got %v", data)
	}

	// 2. Agent tries to send spoofed frame with dev-spoof
	spoofedFrame := makePrevFrame("dev-spoof", nalu)
	if err := agentWS.WriteMessage(websocket.BinaryMessage, spoofedFrame); err != nil {
		t.Fatalf("write spoofed frame error: %v", err)
	}

	// Client should NOT receive spoofed frame
	_ = cliWS.SetReadDeadline(time.Now().Add(200 * time.Millisecond))
	_, _, err = cliWS.ReadMessage()
	if err == nil {
		t.Errorf("expected spoofed frame to be dropped, but client received it")
	}
}

// TestGroupControlRelay verifies client dispatching group_control_event to agent
func TestGroupControlRelay(t *testing.T) {
	server, _, _, _, _, adminToken, _ := setupTransportTestEnv(t)

	agentURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/register_agent"
	agentWS, _, err := websocket.DefaultDialer.Dial(agentURL, nil)
	if err != nil {
		t.Fatalf("dial agent error: %v", err)
	}
	defer agentWS.Close()

	_ = agentWS.WriteJSON(map[string]interface{}{
		"type":      "agent_register",
		"device_id": "dev-1",
	})
	var ack transport.AgentRegisterOkMessage
	_ = agentWS.ReadJSON(&ack)

	cliURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/connect_client?token=" + adminToken
	cliWS, _, err := websocket.DefaultDialer.Dial(cliURL, nil)
	if err != nil {
		t.Fatalf("dial client error: %v", err)
	}
	defer cliWS.Close()

	// Client sends group_control_event
	gcEnv := transport.GroupControlEnvelope{
		MessageType:     "group_control_event",
		TargetDeviceIDs: []string{"dev-1"},
		Event: map[string]interface{}{
			"type":   "touch",
			"action": 0,
			"x":      500,
			"y":      800,
		},
	}
	if err := cliWS.WriteJSON(gcEnv); err != nil {
		t.Fatalf("write group_control_event error: %v", err)
	}

	_ = agentWS.SetReadDeadline(time.Now().Add(2 * time.Second))
	var received map[string]interface{}
	if err := agentWS.ReadJSON(&received); err != nil {
		t.Fatalf("agent read group_control_event error: %v", err)
	}
	if received["message_type"] != "group_control_event" {
		t.Errorf("expected message_type group_control_event, got %+v", received)
	}
	ev, ok := received["event"].(map[string]interface{})
	if !ok || ev["type"] != "touch" {
		t.Errorf("unexpected event payload: %+v", ev)
	}
}
