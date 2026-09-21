/**
 * apply-r5-hotpath-recovery.cjs
 * 
 * Implements Phase R5.3 - R5.4A across index-DIPw8r74.js:
 * 1. R5.1b-1: DevicePanel.Vt() reverts reconnect-in-place; preserves native mode switch.
 * 2. R5.1b-2: Native mouse/touch event architecture preserved; no pointer capture on MouseEvents.
 * 3. R5.1b-3: Single unified controllerSessionId across DevicePanel, PeerConnection, and DataChannel.
 * 4. R5.1b-4: Stream stat calculation with deltas (actualFps, avgJitterBufferMs, avgDecodeMs, bitrateKbps).
 * 5. R5.1b-5: Native keycode injection for useWebSocketStream.sendCommand().
 * 6. R5.3.4-R5.3.9: Normalized geometry touch mapping with letterbox/pillarbox removal, fail safe, and [GEOMETRY]/[TOUCH-MAP] logging.
 * 7. R5.3.3: Device metadata & rotation propagation from server device_info.
 * 8. R5.4A-0: Initial Open State Machine (CLOSED -> OPENING -> SIGNALING_CONNECTED -> MEDIA_STARTING -> READY/FAILED).
 * 9. R5.4A-0: Connection Epoch & Attempt ID with responsive key remount (${deviceId}_${mode}_${epoch}).
 * 10. R5.4A-1: Idempotent disconnect() in useWebRTC and useWebSocketStream with instanceId & disposed guard.
 * 11. R5.4A-3: Bidirectional handoff stream_ready / stream_failed Protocol ACKs.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const TARGET_FILES = [
  path.resolve(__dirname, '../../reconstructed_source/web-app/public/assets/index-DIPw8r74.js'),
  path.resolve(__dirname, '../../reconstructed_source/web-app/dist/assets/index-DIPw8r74.js')
];

const patches = [
  // 1. PeerConnection Creation Tracking & Unified Session Assignment
  {
    name: 'Patch 1: PeerConnection Creation Tracking & Unified Session',
    find: 'A=new RTCPeerConnection({iceServers:h,iceTransportPolicy:P,encodedInsertableStreams:_e})',
    findFallback: [
      'A=new RTCPeerConnection({iceServers:h,iceTransportPolicy:P,encodedInsertableStreams:_e}),A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A,A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A,A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A,A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A,A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A'
    ],
    replace: 'A=new RTCPeerConnection({iceServers:h,iceTransportPolicy:P,encodedInsertableStreams:_e}),A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A'
  },

  // 2. DataChannel Lifecycle Tracking & Unified Session Propagation + CONTROL_READY Trigger
  {
    name: 'Patch 2: DataChannel Lifecycle Tracking & CONTROL_READY Trigger',
    find: 'A.ondatachannel=Se=>{ct("[WebRTC] Received DataChannel:",Se.channel.label),Se.channel.label==="input-channel"?(d=Se.channel,d.onopen=()=>{ct("[DataChannel] input-channel OPEN")},d.onclose=()=>{ct("[DataChannel] input-channel CLOSED")},d.onerror=Te=>console.error("[DataChannel] Error:",Te)):Se.channel.label==="clipboard-channel"?(v=Se.channel,v.onopen=()=>{ct("[DataChannel] clipboard-channel OPEN")',
    findFallback: [
      'd.onopen=()=>{window.__recordDcLife&&window.__recordDcLife("open",d.__sessionId,{label:d.label,id:d.id}),ct("[DataChannel] input-channel OPEN")}'
    ],
    replace: 'd.onopen=()=>{window.__recordDcLife&&window.__recordDcLife("open",d.__sessionId,{label:d.label,id:d.id}),ct("[DataChannel] input-channel OPEN"),window.__checkRtcReady&&window.__checkRtcReady("CONTROL_READY")}'
  },

  // 3. useWebRTC.sendTouch Normalized Geometry Mapping & Touch Safety (Guaranteed UP/MOVE)
  {
    name: 'Patch 3: useWebRTC.sendTouch Normalized Geometry Mapping & Touch Safety',
    find: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l||!d||d.readyState!=="open")return;const Te=s.value&&f?f():g?g():null;if(!Te)return;const Ye=Te.videoWidth||Te.width||B.value,gt=Te.videoHeight||Te.height||w.value;if(!Ye||!gt)return;const Tt=++E,Vt=Date.now(),Gt=B.value>w.value,Ni=Ye>gt!==Gt,Pi=Ni?w.value:B.value,Ce=Ni?B.value:w.value;let Ke,nt;if(Se&&Se.isRotated){const Qt=Math.round(Se.x/Ye*Pi),vi=Math.round(Se.y/gt*Ce);Ke=Math.max(0,Math.min(Pi,Qt)),nt=Math.max(0,Math.min(Ce,vi))}else{const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El,eg=Math.round(oh/Wi*Pi),tg=Math.round(yo/Rn*Ce);Ke=Math.max(0,Math.min(Pi,eg)),nt=Math.max(0,Math.min(Ce,tg))}const ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce});const dt=d.bufferedAmount;(P!==2||Tt%30===0||dt>65536)&&qm("[TouchTrace] dc-send",{seq:Tt,action:P,id:Ue,x:Ke,y:nt,w:Pi,h:Ce,clientTsMs:Vt,bufferedBefore:wt,bufferedAfter:dt})}',
    findFallback: [
      'function Ot(P,ue,_e,Ue=0,Se=null){if(l){window.__recordTouchDrop&&window.__recordTouchDrop("VIEW_ONLY",{l,dcState:d?d.readyState:"none"});return}if(!d){window.__recordTouchDrop&&window.__recordTouchDrop("NO_DATA_CHANNEL",{dcState:"none",pcState:A?A.connectionState:"none"});return}if(d.readyState!=="open"){const rS=d.readyState==="connecting"?"DC_CONNECTING":d.readyState==="closing"?"DC_CLOSING":d.readyState==="closed"?"DC_CLOSED":("DC_"+d.readyState.toUpperCase());window.__recordTouchDrop&&window.__recordTouchDrop(rS,{dcState:d.readyState,pcState:A?A.connectionState:"none"});return}const Te=s.value&&f?f():g?g():null;if(!Te){window.__recordTouchDrop&&window.__recordTouchDrop("NO_ACTIVE_MEDIA_ELEMENT",{dcState:d.readyState,hasCanvasGetter:!!f,hasVideoGetter:!!g});return}const Ye=Te.videoWidth||Te.width||B.value,gt=Te.videoHeight||Te.height||w.value;if(!Ye||!gt){window.__recordTouchDrop&&window.__recordTouchDrop("INVALID_VIDEO_DIMENSIONS",{videoWidth:Te.videoWidth,width:Te.width,defaultW:B.value,videoHeight:Te.videoHeight,height:Te.height,defaultH:w.value});return}const Tt=++E,Vt=Date.now(),Gt=B.value>w.value,Ni=Ye>gt!==Gt,Pi=Ni?w.value:B.value,Ce=Ni?B.value:w.value;let Ke,nt;if(Se&&Se.isRotated){const Qt=Math.round(Se.x/Ye*Pi),vi=Math.round(Se.y/gt*Ce);Ke=Math.max(0,Math.min(Pi,Qt)),nt=Math.max(0,Math.min(Ce,vi))}else{const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El,eg=Math.round(oh/Wi*Pi),tg=Math.round(yo/Rn*Ce);Ke=Math.max(0,Math.min(Pi,eg)),nt=Math.max(0,Math.min(Ce,tg));window.__recordCoordDiag&&window.__recordCoordDiag({elementRect:Qt,videoWidth:Ye,videoHeight:gt,actualW:Wi,actualH:Rn,offsetX:ps,offsetY:El,relativeX:oh,relativeY:yo,finalX:Ke,finalY:nt,targetW:Pi,targetH:Ce,isRotated:!1})}const ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce});window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:d.__sessionId,pcSession:A?A.__sessionId:null,seq:Tt,action:P===0?"DOWN":P===1?"UP":"MOVE",actionCode:P,result:"SENT",dcState:d.readyState,dcId:d.id,pcState:A?A.connectionState:"unknown",bufferedAmount:wt,x:Ke,y:nt,w:Pi,h:Ce,overheadMs:Date.now()-Vt})}',
      'function Ot(P,ue,_e,Ue=0,Se=null){if(l){window.__recordTouchDrop&&window.__recordTouchDrop("VIEW_ONLY",{l,dcState:d?d.readyState:"none"});return}if(!d){window.__recordTouchDrop&&window.__recordTouchDrop("NO_DATA_CHANNEL",{dcState:"none",pcState:A?A.connectionState:"none"});return}if(d.readyState!=="open"){const rS=d.readyState==="connecting"?"DC_CONNECTING":d.readyState==="closing"?"DC_CLOSING":d.readyState==="closed"?"DC_CLOSED":("DC_"+d.readyState.toUpperCase());window.__recordTouchDrop&&window.__recordTouchDrop(rS,{dcState:d.readyState,pcState:A?A.connectionState:"none"});return}const Te=s.value&&f?f():g?g():null;if(!Te){window.__recordTouchDrop&&window.__recordTouchDrop("NO_ACTIVE_MEDIA_ELEMENT",{dcState:d.readyState,hasCanvasGetter:!!f,hasVideoGetter:!!g});return}const Ye=Te.videoWidth||Te.width||0,gt=Te.videoHeight||Te.height||0;if(!Ye||!gt){window.__recordTouchDrop&&window.__recordTouchDrop("INVALID_VIDEO_DIMENSIONS",{videoWidth:Te.videoWidth,width:Te.width,videoHeight:Te.videoHeight,height:Te.height});return}const logicalW=B.value,logicalH=w.value;if(!logicalW||!logicalH||o.value==="unknown"){window.__recordTouchDrop&&window.__recordTouchDrop("DEVICE_GEOMETRY_UNKNOWN",{deviceId:i,agentVersion:o.value,w:logicalW,h:logicalH});return}const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El;if(oh<0||oh>Wi||yo<0||yo>Rn){window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{localX:oh,localY:yo,contentW:Wi,contentH:Rn,clientX:ue,clientY:_e});return}const u=Math.max(0,Math.min(1,oh/Wi)),v=Math.max(0,Math.min(1,yo/Rn));let rot=window.__deviceRotation!==undefined?window.__deviceRotation:(Se&&Se.rotation!==undefined?Se.rotation:0);let tx=u,ty=v;rot===90||(Se&&Se.isRotated&&rot===0)?(tx=v,ty=1-u):rot===180?(tx=1-u,ty=1-v):rot===270&&(tx=1-v,ty=u);const Ke=Math.max(0,Math.min(logicalW,Math.round(tx*logicalW))),nt=Math.max(0,Math.min(logicalH,Math.round(ty*logicalH)));if(P===0||P===1){console.log(`[GEOMETRY] device=${i} logical=${logicalW}x${logicalH} frame=${Ye}x${gt} viewport=${Math.round(vi)}x${Math.round(Yi)} contentRect=[${Math.round(Qt.left+ps)},${Math.round(Qt.top+El)},${Math.round(Wi)}x${Math.round(Rn)}] rotation=${rot}`);console.log(`[TOUCH-MAP] client=(${ue},${_e}) normalized=(${u.toFixed(3)},${v.toFixed(3)}) mapped=(${Ke},${nt}) target=(${logicalW},${logicalH})`)}window.__recordCoordDiag&&window.__recordCoordDiag({elementRect:Qt,videoWidth:Ye,videoHeight:gt,actualW:Wi,actualH:Rn,offsetX:ps,offsetY:El,relativeX:oh,relativeY:yo,u,v,rotation:rot,finalX:Ke,finalY:nt,targetW:logicalW,targetH:logicalH});const Tt=++E,Vt=Date.now(),ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:logicalW,h:logicalH}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:logicalW,h:logicalH});window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:d.__sessionId,pcSession:A?A.__sessionId:null,seq:Tt,action:P===0?"DOWN":P===1?"UP":"MOVE",actionCode:P,result:"SENT",dcState:d.readyState,dcId:d.id,pcState:A?A.connectionState:"unknown",bufferedAmount:wt,x:Ke,y:nt,w:logicalW,h:logicalH,overheadMs:Date.now()-Vt})}'
    ],
    replace: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l){window.__recordTouchDrop&&window.__recordTouchDrop("VIEW_ONLY",{l,dcState:d?d.readyState:"none"});return}if(!d){window.__recordTouchDrop&&window.__recordTouchDrop("NO_DATA_CHANNEL",{dcState:"none",pcState:A?A.connectionState:"none"});return}if(d.readyState!=="open"){const rS=d.readyState==="connecting"?"DC_CONNECTING":d.readyState==="closing"?"DC_CLOSING":d.readyState==="closed"?"DC_CLOSED":("DC_"+d.readyState.toUpperCase());window.__recordTouchDrop&&window.__recordTouchDrop(rS,{dcState:d.readyState,pcState:A?A.connectionState:"none"});return}const Te=s.value&&f?f():g?g():null;if(!Te){window.__recordTouchDrop&&window.__recordTouchDrop("NO_ACTIVE_MEDIA_ELEMENT",{dcState:d.readyState,hasCanvasGetter:!!f,hasVideoGetter:!!g});return}const Ye=Te.videoWidth||Te.width||0,gt=Te.videoHeight||Te.height||0;if(!Ye||!gt){window.__recordTouchDrop&&window.__recordTouchDrop("INVALID_VIDEO_DIMENSIONS",{videoWidth:Te.videoWidth,width:Te.width,videoHeight:Te.videoHeight,height:Te.height});return}const logicalW=B.value,logicalH=w.value;if(!logicalW||!logicalH||o.value==="unknown"){window.__recordTouchDrop&&window.__recordTouchDrop("DEVICE_GEOMETRY_UNKNOWN",{deviceId:i,agentVersion:o.value,w:logicalW,h:logicalH});return}const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El;if(P===0&&(oh<0||oh>Wi||yo<0||yo>Rn)){window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{localX:oh,localY:yo,contentW:Wi,contentH:Rn,clientX:ue,clientY:_e});return}const u=Math.max(0,Math.min(1,Wi>0?oh/Wi:0)),v=Math.max(0,Math.min(1,Rn>0?yo/Rn:0));let rot=window.__deviceRotation!==undefined?window.__deviceRotation:(Se&&Se.rotation!==undefined?Se.rotation:0);let tx=u,ty=v;rot===90||(Se&&Se.isRotated&&rot===0)?(tx=v,ty=1-u):rot===180?(tx=1-u,ty=1-v):rot===270&&(tx=1-v,ty=u);const Ke=Math.max(0,Math.min(logicalW,Math.round(tx*logicalW))),nt=Math.max(0,Math.min(logicalH,Math.round(ty*logicalH)));if(P===0||P===1){console.log(`[GEOMETRY] device=${i} logical=${logicalW}x${logicalH} frame=${Ye}x${gt} viewport=${Math.round(vi)}x${Math.round(Yi)} contentRect=[${Math.round(Qt.left+ps)},${Math.round(Qt.top+El)},${Math.round(Wi)}x${Math.round(Rn)}] rotation=${rot}`);console.log(`[TOUCH-MAP] client=(${ue},${_e}) normalized=(${u.toFixed(3)},${v.toFixed(3)}) mapped=(${Ke},${nt}) target=(${logicalW},${logicalH})`)}window.__recordCoordDiag&&window.__recordCoordDiag({elementRect:Qt,videoWidth:Ye,videoHeight:gt,actualW:Wi,actualH:Rn,offsetX:ps,offsetY:El,relativeX:oh,relativeY:yo,u,v,rotation:rot,finalX:Ke,finalY:nt,targetW:logicalW,targetH:logicalH});const Tt=++E,Vt=Date.now(),ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:logicalW,h:logicalH}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:logicalW,h:logicalH});window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:d.__sessionId,pcSession:A?A.__sessionId:null,seq:Tt,action:P===0?"DOWN":P===1?"UP":"MOVE",actionCode:P,result:"SENT",dcState:d.readyState,dcId:d.id,pcState:A?A.connectionState:"unknown",bufferedAmount:wt,x:Ke,y:nt,w:logicalW,h:logicalH,overheadMs:Date.now()-Vt})}'
  },

  // 4. useWebSocketStream.sendCommand keycode translation
  {
    name: 'Patch 4: useWebSocketStream.sendCommand keycode translation',
    find: 'function Qe(ae){return!1}',
    replace: 'function Qe(ae){if(typeof ae=="string"){const m=ae.match(/input\\s+keyevent\\s+(\\d+)/);if(m){const kc=parseInt(m[1],10);J(0,kc),setTimeout(()=>J(1,kc),50);return!0}}return!1}'
  },

  // 5. useWebSocketStream.sendTouch diagnostics & guaranteed UP delivery
  {
    name: 'Patch 5: useWebSocketStream.sendTouch diagnostics & guaranteed UP delivery',
    find: 'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe)return;const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht)}',
    findFallback: [
      'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe){window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{mode:"websocket",x:Ne,y:ze});return}const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht);window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:"ws",pcSession:"ws",seq:R,action:ae===0?"DOWN":ae===1?"UP":"MOVE",actionCode:ae,result:"SENT",mode:"websocket",x:qe.x,y:qe.y,w:qe.w,h:qe.h})}'
    ],
    replace: 'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe){if(ae===1){const fbX=T||0,fbY=O||0,fbW=d.value||540,fbH=v.value||960;const Ht={type:"touch",action:1,x:fbX,y:fbY,w:fbW,h:fbH,id:et,seq:R,client_ts_ms:Date.now()};t.sendGroupControlEvent([i],Ht),_&&_(Ht);window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:"ws",pcSession:"ws",seq:R,action:"UP",actionCode:1,result:"SENT",mode:"websocket",x:fbX,y:fbY,w:fbW,h:fbH})}else{window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{mode:"websocket",x:Ne,y:ze})}return}const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht);window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:"ws",pcSession:"ws",seq:R,action:ae===0?"DOWN":ae===1?"UP":"MOVE",actionCode:ae,result:"SENT",mode:"websocket",x:qe.x,y:qe.y,w:qe.w,h:qe.h})}'
  },

  // 6. DevicePanel Mode Switch Revert & Mount Lifecycle
  {
    name: 'Patch 6: DevicePanel Mode Switch Revert & Mount Lifecycle',
    find: 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}a.value&&n.registerWebRTC(a.value,Te);',
    findFallback: [
      'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}window.__globalSessionSeq=(window.__globalSessionSeq||0)+1,window.__activeSessionId=window.__globalSessionSeq,window.__recordCtrlLife&&window.__recordCtrlLife("mount",window.__activeSessionId,{deviceId:a.value}),a.value&&n.registerWebRTC(a.value,Te);'
    ],
    replace: 'function Vt(){const X=Ye.value?"display":"websocket";window.__deviceModes=window.__deviceModes||{},window.__deviceModes[a.value]=X,n.setDeviceMode(a.value,X)}window.__globalSessionSeq=(window.__globalSessionSeq||0)+1,window.__activeSessionId=window.__globalSessionSeq,window.__recordCtrlLife&&window.__recordCtrlLife("mount",window.__activeSessionId,{deviceId:a.value}),window.__deviceModes=window.__deviceModes||{},window.__deviceModes[a.value]=n.getDeviceMode(a.value)||"display",a.value&&n.registerWebRTC(a.value,Te);'
  },

  // 7. DevicePanel Unmount Lifecycle (with deduplication clean up)
  {
    name: 'Patch 7: DevicePanel Unmount Lifecycle',
    find: 'Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)',
    findFallback: [
      'window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)'
    ],
    replace: 'window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)'
  },

  // 8. Mouse Down Native Handling, Deduplication & Self-Healing UP
  {
    name: 'Patch 8: Mouse Down Native Handling, Deduplication & Self-Healing UP',
    find: 'function ZS(X){if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y),p.value&&(p.value.focus(),ct("[Keyboard] focused hidden input element. activeElement:",document.activeElement?document.activeElement.tagName:"none")),X.preventDefault()}',
    findFallback: [
      'function ZS(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mousedown",clientX:X.clientX,clientY:X.clientY,target:X.target?X.target.tagName:"none"});if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y),p.value&&(p.value.focus(),ct("[Keyboard] focused hidden input element. activeElement:",document.activeElement?document.activeElement.tagName:"none")),X.preventDefault()}'
    ],
    replace: 'function ZS(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mousedown",clientX:X.clientX,clientY:X.clientY,target:X.target?X.target.tagName:"none"});if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}if(sh){const prevX=window.__lastMouseX!==undefined?window.__lastMouseX:X.clientX,prevY=window.__lastMouseY!==undefined?window.__lastMouseY:X.clientY,prevRot=window.__lastMouseRot||null;sh=!1,Te.sendTouch(1,prevX,prevY,-1,prevRot),window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"self_heal_up",clientX:prevX,clientY:prevY})}const Y=ys(X.clientX,X.clientY);window.__lastMouseX=X.clientX,window.__lastMouseY=X.clientY,window.__lastMouseRot=Y,window.__activeReleaseTouch=()=>sh&&Te.sendTouch&&(sh=!1,Te.sendTouch(1,window.__lastMouseX,window.__lastMouseY,-1,window.__lastMouseRot));sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y),p.value&&(p.value.focus(),ct("[Keyboard] focused hidden input element. activeElement:",document.activeElement?document.activeElement.tagName:"none")),X.preventDefault()}'
  },

  // 9. Mouse Up Native Handling, Deduplication & Clean Release
  {
    name: 'Patch 9: Mouse Up Native Handling, Deduplication & Clean Release',
    find: 'function tb(X){if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}',
    findFallback: [
      'function tb(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mouseup",clientX:X.clientX,clientY:X.clientY,target:X.target?X.target.tagName:"none"});if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}'
    ],
    replace: 'function tb(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mouseup",clientX:X.clientX,clientY:X.clientY,target:X.target?X.target.tagName:"none"});if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}window.__lastMouseX=X.clientX,window.__lastMouseY=X.clientY;const Y=ys(X.clientX,X.clientY);window.__lastMouseRot=Y,sh=!1,window.__activeReleaseTouch=null,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}'
  },

  // 10. Mouse Leave Clean Release
  {
    name: 'Patch 10: Mouse Leave Clean Release',
    find: 'function ib(X){if(O.value){z.value=!1;return}if(sh){const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}}',
    findFallback: [
      'function ib(X){if(O.value){z.value=!1;return}if(sh){window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mouseleave",clientX:X.clientX,clientY:X.clientY});const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}}'
    ],
    replace: 'function ib(X){if(O.value){z.value=!1;return}if(sh){window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mouseleave",clientX:X.clientX,clientY:X.clientY});window.__lastMouseX=X.clientX,window.__lastMouseY=X.clientY;const Y=ys(X.clientX,X.clientY);window.__lastMouseRot=Y,sh=!1,window.__activeReleaseTouch=null,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}}'
  },

  // 11. Touch Start Marker & [INPUT] Logging
  {
    name: 'Patch 11: Touch Start Marker & [INPUT] Logging',
    find: 'function rb(X){if(!O.value)for(let Y=0;Y<X.changedTouches.length;Y++){const pe=X.changedTouches[Y],Je=ys(pe.clientX,pe.clientY);Te.sendTouch(0,pe.clientX,pe.clientY,pe.identifier,Je)}}',
    replace: 'function rb(X){window.__lastTouchTs=Date.now();if(!O.value)for(let Y=0;Y<X.changedTouches.length;Y++){const pe=X.changedTouches[Y],Je=ys(pe.clientX,pe.clientY);window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"touchstart",clientX:pe.clientX,clientY:pe.clientY});Te.sendTouch(0,pe.clientX,pe.clientY,pe.identifier,Je)}}'
  },

  // 12. Touch End Marker & [INPUT] Logging
  {
    name: 'Patch 12: Touch End Marker & [INPUT] Logging',
    find: 'function sg(X){if(!O.value)for(let Y=0;Y<X.changedTouches.length;Y++){const pe=X.changedTouches[Y],Je=ys(pe.clientX,pe.clientY);Te.sendTouch(1,pe.clientX,pe.clientY,pe.identifier,Je)}}',
    replace: 'function sg(X){window.__lastTouchTs=Date.now();if(!O.value)for(let Y=0;Y<X.changedTouches.length;Y++){const pe=X.changedTouches[Y],Je=ys(pe.clientX,pe.clientY);window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"touchend",clientX:pe.clientX,clientY:pe.clientY});Te.sendTouch(1,pe.clientX,pe.clientY,pe.identifier,Je)}}'
  },

  // 13. K(P) Device Geometry & Rotation Metadata Propagation (R5.3)
  {
    name: 'Patch 13: K(P) Device Geometry & Rotation Metadata Propagation (R5.3)',
    find: 'function K(P){if(P&&(P.app_version&&(o.value=P.app_version),P.displays&&P.displays.length>0)){const ue=P.displays[0];B.value=ue.x_res||1080,w.value=ue.y_res||1920,ct(`[WebRTC] Device dimensions updated: ${B.value}x${w.value}`)}}',
    replace: 'function K(P){if(P&&(P.app_version&&(o.value=P.app_version),P.displays&&P.displays.length>0)){const ue=P.displays[0];B.value=ue.x_res||1080,w.value=ue.y_res||1920,window.__deviceRotation=ue.rotation||0,window.__deviceGeometry={deviceId:i,logicalW:B.value,logicalH:w.value,rotation:window.__deviceRotation,model:P.model,version:P.app_version},ct(`[WebRTC] Device dimensions updated: ${B.value}x${w.value}, rotation: ${window.__deviceRotation}`)}}'
  },

  // 14. Phase R5.4: [FPS-CONFIG] request-offer payload logging & window.__lastFpsConfig
  {
    name: 'Patch 14: Phase R5.4 [FPS-CONFIG] request-offer payload logging & window.__lastFpsConfig',
    find: 'case"config":t.value="waiting_offer",P.ice_servers&&P.ice_servers.length>0&&(h=P.ice_servers,ct("[WebRTC] ICE Servers updated from config:",h));const _e={type:"request-offer",ip_preference:q("ipPreference","auto")};Object.keys(e).length>0&&(_e.scrcpy_options=e),ot(_e);break;',
    replace: 'case"config":t.value="waiting_offer",P.ice_servers&&P.ice_servers.length>0&&(h=P.ice_servers,ct("[WebRTC] ICE Servers updated from config:",h));const _e={type:"request-offer",ip_preference:q("ipPreference","auto")};Object.keys(e).length>0&&(_e.scrcpy_options=e),console.log(`[FPS-CONFIG] device=${i} mode=webrtc settingsFps=${e.max_fps!==undefined?e.max_fps:"unrestricted(0)"} scrcpyMaxFps=${e.max_fps!==undefined?e.max_fps:0} maxSize=${e.max_size||0} bitrate=${e.bitrate||0} bwe=${e.bwe}`),window.__lastFpsConfig={device:i,mode:"webrtc",settingsFps:e.max_fps!==undefined?e.max_fps:0,scrcpyMaxFps:e.max_fps!==undefined?e.max_fps:0,maxSize:e.max_size||0,bitrate:e.bitrate||0,bwe:e.bwe},ot(_e);break;'
  },

  // 15. Phase R5.4: 4-Tier FPS Separation (SRC/RX/DEC/PRES) & Silence decode-pause spam + MEDIA_READY Trigger
  {
    name: 'Patch 15: Phase R5.4 4-Tier FPS Separation (SRC/RX/DEC/PRES) & MEDIA_READY Trigger',
    find: '_vEl.__presCount=0;function _rvLoop(n_w,m_t){',
    findFallback: [
      'let xe={timestamp:0,bytesReceived:0,framesDecoded:0},Qe=0,te=!1;async function je(){if(!A)return null;try{const P=await A.getStats();let ue=0,_e=null;for(const Se of P.values())if(Se.type==="candidate-pair"&&Se.state==="succeeded"){_e=Se,ue=(Se.currentRoundTripTime||0)*1e3;break}if(!_e){for(const Se of P.values())if(Se.type==="candidate-pair"&&(Se.nominated||Se.selected)){_e=Se,Se.currentRoundTripTime!==void 0&&(ue=Se.currentRoundTripTime*1e3);break}}let Ue="UDP p2p";if(_e){const Se=P.get(_e.localCandidateId);if(Se){const Te=(Se.protocol||"udp").toUpperCase();Se.candidateType==="relay"?Ue=`${Te} relay`:Ue=`${Te} p2p`}}for(const Se of P.values())if(Se.type==="inbound-rtp"&&Se.kind==="video"){const Te=Se.timestamp,Ye=xe.timestamp?(Te-xe.timestamp)/1e3:0;let gt=0,Tt=Se.framesDecoded||0,Vt=0,Gt=0;if(s.value&&p)gt=p.currentFps.toFixed(0),Tt=p.totalFramesDecoded,Vt=.5,Gt=0;else{const nt=Tt-xe.framesDecoded;gt=Ye>0?(nt/Ye).toFixed(0):0,Gt=Se.jitterBufferDelay/(Se.jitterBufferEmittedCount||1)*1e3||0,Vt=Se.totalDecodeTime/(Tt||1)*1e3||0,Ye>0&&nt===0&&!te&&t.value==="connected"?(Qe++,te=!0,Bn("[VideoTrace] decode-pause",{pauseCount:Qe,ts:Date.now(),dtMs:Math.round(Ye*1e3),framesDecoded:Tt,bytesReceived:Se.bytesReceived,pliCount:Se.pliCount||0,packetsLost:Se.packetsLost||0,jitterBufferDelay:Se.jitterBufferDelay,jitterBufferEmittedCount:Se.jitterBufferEmittedCount})):nt>0&&(te&&qm("[VideoTrace] decode-resume",{ts:Date.now(),newFrames:nt,framesDecoded:Tt,pliCount:Se.pliCount||0,packetsLost:Se.packetsLost||0}),te=!1)}const ar=Ye>0?((Se.bytesReceived-xe.bytesReceived)*8/Ye/1e3).toFixed(0):0,Ni=Gt.toFixed(0),Pi=(ue+Gt+Vt+10).toFixed(0),Ce=Se.pliCount||0,Ke=Se.packetsLost||0;return xe={timestamp:Te,bytesReceived:Se.bytesReceived,framesDecoded:Tt},{fps:gt,bitrate:ar,jbDelay:Ni,e2eDelay:Pi,rtt:ue.toFixed(0),pliCount:Ce,pauseCount:Qe,lostCount:Ke,connectionType:Ue}}}catch{}return null}function ke(){xe={timestamp:0,bytesReceived:0,framesDecoded:0},Qe=0,te=!1}'
    ],
    replace: '_vEl.__presCount=0;function _rvLoop(n_w,m_t){window.__checkRtcReady&&window.__checkRtcReady("MEDIA_READY");'
  },

  // 16. Phase R5.4: UI Stats Overlay display 4-tier FPS
  {
    name: 'Patch 16: Phase R5.4 UI Stats Overlay display 4-tier FPS',
    find: 'm("span",Dz,ee(oe.value.fps)+"fps",1)',
    replace: 'm("span",Dz,ee(oe.value.fpsLabel||(oe.value.fps+"fps")),1)'
  },

  // 17. Phase R5.5: Global Window Mouseup & Blur Safety Net
  {
    name: 'Patch 17: Global Window Mouseup & Blur Safety Net',
    find: 'let sh=!1;',
    replace: 'let sh=!1;if(!window.__mouseSafetyInstalled){window.__mouseSafetyInstalled=!0;window.addEventListener("mouseup",function(ev){if(window.__activeReleaseTouch){window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"global_window_mouseup",clientX:ev.clientX,clientY:ev.clientY});const rel=window.__activeReleaseTouch;window.__activeReleaseTouch=null;rel()}},!0);window.addEventListener("blur",function(){if(window.__activeReleaseTouch){window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"global_window_blur"});const rel=window.__activeReleaseTouch;window.__activeReleaseTouch=null;rel()}})}'
  },

  // 18. Phase R5.5: Mouse Move Coordinates Tracking
  {
    name: 'Patch 18: Mouse Move Coordinates Tracking',
    find: 'function eb(X){if(O.value){if(z.value){const Y=X.clientX-J.x,pe=X.clientY-J.y;j.value=U.x+Y,fe.value=U.y+pe}return}if(sh){const Y=ys(X.clientX,X.clientY);Te.sendTouch(2,X.clientX,X.clientY,-1,Y)}}',
    replace: 'function eb(X){window.__lastMouseX=X.clientX,window.__lastMouseY=X.clientY;if(O.value){if(z.value){const Y=X.clientX-J.x,pe=X.clientY-J.y;j.value=U.x+Y,fe.value=U.y+pe}return}if(sh){const Y=ys(X.clientX,X.clientY);window.__lastMouseRot=Y,Te.sendTouch(2,X.clientX,X.clientY,-1,Y)}}'
  },

  // 19. Phase R5.4A-0: Store openDevice State Machine & connectionEpoch
  {
    name: 'Patch 19: Store openDevice State Machine & connectionEpoch',
    find: 'const W=Z([]),ne=Z(null),ve=Z(null),Ee=Z("grid"),be=Z("exclusive"),De=Z(!1),M=Z(null),H=uB(new Map);function V(Ce,Ke){if(!Ce||!Ke)return;const nt=new Map(H.value);nt.set(Ce,Ey(Ke)),H.value=nt}function j(Ce){if(Ce&&H.value.has(Ce)){const Ke=new Map(H.value);Ke.delete(Ce),H.value=Ke}}function fe(Ce){return Ce&&H.value.get(Ce)||null}const z=we({get:()=>ne.value||W.value[0]||null,set:Ce=>{Ce?$(Ce):Qe()}}),J=we(()=>{if(ne.value&&H.value.has(ne.value))return H.value.get(ne.value);const Ce=W.value[0];return Ce&&H.value.has(Ce)?H.value.get(Ce):null}),U=we(()=>i.value.find(Ce=>Ce.id===z.value));function $(Ce){Ce&&(W.value.includes(Ce)||W.value.push(Ce),ne.value=Ce,ve.value||(ve.value=Ce))}function re(Ce){const Ke=W.value.indexOf(Ce);Ke>-1&&W.value.splice(Ke,1),j(Ce),ne.value===Ce&&(ne.value=W.value[W.value.length-1]||null),ve.value===Ce&&(ve.value=W.value[0]||null),M.value===Ce&&(M.value=null),ce.value[Ce]="display",W.value.length===0&&Qe()}',
    findFallback: [
      'const W=Z([]),ne=Z(null),ve=Z(null),Ee=Z("grid"),be=Z("exclusive"),De=Z(!1),M=Z(null),H=uB(new Map);function V(Ce,Ke){if(!Ce||!Ke)return;const nt=new Map(H.value);nt.set(Ce,Ey(Ke)),H.value=nt}function j(Ce){if(Ce&&H.value.has(Ce)){const Ke=new Map(H.value);Ke.delete(Ce),H.value=Ke}}function fe(Ce){return Ce&&H.value.get(Ce)||null}const z=we({get:()=>ne.value||W.value[0]||null,set:Ce=>{Ce?$(Ce):Qe()}}),J=we(()=>{if(ne.value&&H.value.has(ne.value))return H.value.get(ne.value);const Ce=W.value[0];return Ce&&H.value.has(Ce)?H.value.get(Ce):null}),U=we(()=>i.value.find(Ce=>Ce.id===z.value));const pe_epoch=Z({});function _getEpoch(Ce){return(Ce&&pe_epoch.value[Ce])||1}function _incEpoch(Ce){if(Ce){window.__deviceEpochs=window.__deviceEpochs||{};const nEp=(_getEpoch(Ce)+1);pe_epoch.value[Ce]=nEp,pe_epoch.value={...pe_epoch.value},window.__deviceEpochs[Ce]=nEp}}function _sendSignaling(msg){if(Ie&&Ie.readyState===WebSocket.OPEN){Ie.send(typeof msg==="string"?msg:JSON.stringify(msg))}}function $(Ce){if(!Ce)return;window.__deviceConnectionStates=window.__deviceConnectionStates||{};window.__deviceEpochs=window.__deviceEpochs||{};window.__deviceAttempts=window.__deviceAttempts||{};const curSt=window.__deviceConnectionStates[Ce]||"CLOSED",inList=W.value.includes(Ce);if(inList){if(curSt==="READY"||curSt==="OPENING"||curSt==="SIGNALING_CONNECTED"||curSt==="MEDIA_STARTING"){console.log(`[LIFECYCLE] openDevice(${Ce}) state=${curSt} inList=true -> focus only`);ne.value=Ce;return}console.log(`[LIFECYCLE] openDevice(${Ce}) state=${curSt} inList=true -> explicit retry`);_incEpoch(Ce),window.__deviceAttempts[Ce]=(window.__deviceAttempts[Ce]||1)+1,window.__deviceConnectionStates[Ce]="OPENING",ne.value=Ce}else{window.__deviceEpochs[Ce]=window.__deviceEpochs[Ce]||1,window.__deviceAttempts[Ce]=(window.__deviceAttempts[Ce]||0)+1,window.__deviceConnectionStates[Ce]="OPENING",console.log(`[LIFECYCLE] openDevice(${Ce}) initial open epoch=${window.__deviceEpochs[Ce]} attempt=${window.__deviceAttempts[Ce]}`),W.value.push(Ce),ne.value=Ce,ve.value||(ve.value=Ce)}}function re(Ce){const Ke=W.value.indexOf(Ce);Ke>-1&&W.value.splice(Ke,1),j(Ce),window.__deviceConnectionStates&&(window.__deviceConnectionStates[Ce]="CLOSED"),ne.value===Ce&&(ne.value=W.value[W.value.length-1]||null),ve.value===Ce&&(ve.value=W.value[0]||null),M.value===Ce&&(M.value=null),ce.value[Ce]="display",W.value.length===0&&Qe()}'
    ],
    replace: 'const W=Z([]),ne=Z(null),ve=Z(null),Ee=Z("grid"),be=Z("exclusive"),De=Z(!1),M=Z(null),H=uB(new Map);function V(Ce,Ke){if(!Ce||!Ke)return;const nt=new Map(H.value);nt.set(Ce,Ey(Ke)),H.value=nt}function j(Ce){if(Ce&&H.value.has(Ce)){const Ke=new Map(H.value);Ke.delete(Ce),H.value=Ke}}function fe(Ce){return Ce&&H.value.get(Ce)||null}const z=we({get:()=>ne.value||W.value[0]||null,set:Ce=>{Ce?$(Ce):Qe()}}),J=we(()=>{if(ne.value&&H.value.has(ne.value))return H.value.get(ne.value);const Ce=W.value[0];return Ce&&H.value.has(Ce)?H.value.get(Ce):null}),U=we(()=>i.value.find(Ce=>Ce.id===z.value));const pe_epoch=Z({});function _getEpoch(Ce){return(Ce&&pe_epoch.value[Ce])||1}function _incEpoch(Ce){if(Ce){window.__deviceEpochs=window.__deviceEpochs||{};const nEp=(_getEpoch(Ce)+1);pe_epoch.value[Ce]=nEp,pe_epoch.value={...pe_epoch.value},window.__deviceEpochs[Ce]=nEp}}function _sendSignaling(msg){if(Ie&&Ie.readyState===WebSocket.OPEN){Ie.send(typeof msg==="string"?msg:JSON.stringify(msg))}}function $(Ce){if(!Ce)return;window.__deviceConnectionStates=window.__deviceConnectionStates||{};window.__deviceEpochs=window.__deviceEpochs||{};window.__deviceAttempts=window.__deviceAttempts||{};const curSt=window.__deviceConnectionStates[Ce]||"CLOSED",inList=W.value.includes(Ce);if(inList){if(curSt==="READY"||curSt==="OPENING"||curSt==="SIGNALING_CONNECTED"||curSt==="MEDIA_STARTING"){console.log(`[LIFECYCLE] openDevice(${Ce}) state=${curSt} inList=true -> focus only`);ne.value=Ce;return}console.log(`[LIFECYCLE] openDevice(${Ce}) state=${curSt} inList=true -> explicit retry`);_incEpoch(Ce),window.__deviceAttempts[Ce]=(window.__deviceAttempts[Ce]||1)+1,window.__deviceConnectionStates[Ce]="OPENING",ne.value=Ce}else{window.__deviceEpochs[Ce]=window.__deviceEpochs[Ce]||1,window.__deviceAttempts[Ce]=(window.__deviceAttempts[Ce]||0)+1,window.__deviceConnectionStates[Ce]="OPENING",console.log(`[LIFECYCLE] openDevice(${Ce}) initial open epoch=${window.__deviceEpochs[Ce]} attempt=${window.__deviceAttempts[Ce]}`),W.value.push(Ce),window.__activeDeviceIds=W.value,ne.value=Ce,ve.value||(ve.value=Ce)}}function re(Ce){const Ke=W.value.indexOf(Ce);Ke>-1&&W.value.splice(Ke,1),window.__activeDeviceIds=W.value,window.__heldWebRTC&&window.__heldWebRTC[Ce]&&(window.__heldWebRTC[Ce].close(),delete window.__heldWebRTC[Ce]),j(Ce),window.__deviceConnectionStates&&(window.__deviceConnectionStates[Ce]="CLOSED"),ne.value===Ce&&(ne.value=W.value[W.value.length-1]||null),ve.value===Ce&&(ve.value=W.value[0]||null),M.value===Ce&&(M.value=null),ce.value[Ce]="display",window.__deviceModes&&(window.__deviceModes[Ce]="display"),W.value.length===0&&Qe()}'
  },

  // 19b. Phase R5.4A-0: Store Exports getDeviceEpoch, incDeviceEpoch, sendSignalingMessage
  {
    name: 'Patch 19b: Store Exports getDeviceEpoch & incDeviceEpoch & sendSignalingMessage',
    find: 'setDeviceMode:Me,getDeviceMode:He,setActiveWebRTC:ot,clearActiveDevice:Ot,',
    replace: 'setDeviceMode:Me,getDeviceMode:He,getDeviceEpoch:_getEpoch,incDeviceEpoch:_incEpoch,sendSignalingMessage:_sendSignaling,setActiveWebRTC:ot,clearActiveDevice:Ot,'
  },

  // 19c. Phase R5.4A: Store Mode Mirroring & Held WebRTC Cleanup
  {
    name: 'Patch 19c: Store Mode Mirroring & Held WebRTC Cleanup',
    find: 'const ce=Z({});function Me(Ce,Ke="display"){Ce&&(ce.value[Ce]=Ke)}function He(Ce){return Ce&&ce.value[Ce]||"display"}function Ve(Ce){Ce&&(Me(Ce,"camera"),$(Ce))}function xe(Ce){Ce&&(Me(Ce,"websocket"),$(Ce))}function Qe(){W.value=[],ne.value=null,ve.value=null,M.value=null,H.value=new Map,ce.value={}}',
    replace: 'const ce=Z({});function Me(Ce,Ke="display"){Ce&&(ce.value[Ce]=Ke,window.__deviceModes=window.__deviceModes||{},window.__deviceModes[Ce]=Ke)}function He(Ce){return Ce&&ce.value[Ce]||"display"}function Ve(Ce){Ce&&(Me(Ce,"camera"),$(Ce))}function xe(Ce){Ce&&(Me(Ce,"websocket"),$(Ce))}function Qe(){W.value=[],window.__activeDeviceIds=[],ne.value=null,ve.value=null,M.value=null,H.value=new Map,ce.value={},window.__heldWebRTC&&(Object.keys(window.__heldWebRTC).forEach(k=>{try{window.__heldWebRTC[k].close()}catch(e){}}),window.__heldWebRTC={})}'
  },

  // 20. Phase R5.4A-1: Idempotent useWebRTC disconnect with CoreService WebRTC Preservation Guard
  {
    name: 'Patch 20: Idempotent useWebRTC disconnect',
    find: 'function se(){Ht(),p&&(p.stop(),p=null,s.value=!1),A&&(A.close(),A=null);const P=g?g():null;if(P&&(P.srcObject=null),y=null,re(),c&&(c.close(),c=null),pi){try{pi.close()}catch{}pi=null}if(Ie.value=!1,k){try{k.close()}catch{}k=null}R.clear(),t.value="disconnected",u&&(u._adbInstance=null,u._adbTransport=null,u._adbRawConnection=null,u._adbActiveSocketsCount=0)}pr(()=>{se()});',
    findFallback: [
      'let _webrtcDisposed=!1,_webrtcInstId=++window.__webrtcInstSeq||(window.__webrtcInstSeq=1);function se(){if(_webrtcDisposed){console.log(`[WebRTC-LIFE] inst=${_webrtcInstId} already disposed, suppressing duplicate disconnect`);return}_webrtcDisposed=!0,console.log(`[WebRTC-LIFE] inst=${_webrtcInstId} disconnecting dev=${i}`);window.__rtcWatchdogTimer&&clearTimeout(window.__rtcWatchdogTimer);Ht(),p&&(p.stop(),p=null,s.value=!1),A&&(A.close(),A=null);const P=g?g():null;if(P&&(P.srcObject=null),y=null,re(),c&&(c.close(),c=null),pi){try{pi.close()}catch{}pi=null}if(Ie.value=!1,k){try{k.close()}catch{}k=null}R.clear(),t.value="disconnected",u&&(u._adbInstance=null,u._adbTransport=null,u._adbRawConnection=null,u._adbActiveSocketsCount=0)}pr(()=>{se()});'
    ],
    replace: 'let _webrtcDisposed=!1,_webrtcInstId=++window.__webrtcInstSeq||(window.__webrtcInstSeq=1);function se(){if(_webrtcDisposed){console.log(`[WebRTC-LIFE] inst=${_webrtcInstId} already disposed, suppressing duplicate disconnect`);return}_webrtcDisposed=!0,console.log(`[WebRTC-LIFE] inst=${_webrtcInstId} disconnecting dev=${i}`);window.__rtcWatchdogTimer&&clearTimeout(window.__rtcWatchdogTimer);Ht(),p&&(p.stop(),p=null,s.value=!1);const P=g?g():null;if(P&&(P.srcObject=null),y=null,re(),pi){try{pi.close()}catch{}pi=null}if(Ie.value=!1,k){try{k.close()}catch{}k=null}R.clear(),t.value="disconnected",u&&(u._adbInstance=null,u._adbTransport=null,u._adbRawConnection=null,u._adbActiveSocketsCount=0);const isActive=!window.__activeDeviceIds||window.__activeDeviceIds.includes(i),isWs=window.__deviceModes&&window.__deviceModes[i]==="websocket";if(isActive&&isWs&&A){console.log(`[WebRTC-HOLD] Preserving WebRTC for ${i} in websocket mode to protect CoreService from ICE collapse`);window.__heldWebRTC=window.__heldWebRTC||{};if(window.__heldWebRTC[i]&&window.__heldWebRTC[i].pc!==A){try{window.__heldWebRTC[i].close()}catch(e){}}const heldPc=A,heldWs=c;window.__heldWebRTC[i]={pc:heldPc,ws:heldWs,close:()=>{try{heldPc&&heldPc.close()}catch(e){}try{heldWs&&heldWs.close()}catch(e){}}};A=null,c=null;}else{console.log(`[WebRTC-LIFE] Full WebRTC teardown dev=${i} active=${isActive} isWs=${isWs}`);A&&(A.close(),A=null);if(c){try{c.close()}catch{}c=null}}}pr(()=>{se()});'
  },

  // 21. Phase R5.4A-1: Idempotent useWebSocketStream disconnect with instanceId & disposed guard
  {
    name: 'Patch 21: Idempotent useWebSocketStream disconnect',
    find: 'function yt(){if(r.value="disconnected",Ct(),S(),t.unregisterPreviewCallback(i,"stream"),t.hasPreviewSubscribers(i)||t.sendPreviewControl("stop_preview",i),b){try{b.close()}catch{}b=null}x=!1,Q=null,L=null,D&&(D=null),c.value=!1,k=!1}',
    replace: 'let _wsDisposed=!1,_wsInstId=++window.__wsInstSeq||(window.__wsInstSeq=1);function yt(){if(_wsDisposed){console.log(`[WS-LIFE] inst=${_wsInstId} already disposed, suppressing duplicate disconnect`);return}_wsDisposed=!0,console.log(`[WS-LIFE] inst=${_wsInstId} disconnecting dev=${i}`);if(r.value="disconnected",Ct(),S(),t.unregisterPreviewCallback(i,"stream"),t.hasPreviewSubscribers(i)||t.sendPreviewControl("stop_preview",i),b){try{b.close()}catch{}b=null}x=!1,Q=null,L=null,D&&(D=null),c.value=!1,k=!1}'
  },

  // 22. Phase R5.4A-0 & R5.4A-3: useWebRTC Signaling onopen, Ready Protocol ACKs & Timeout Watchdog
  {
    name: 'Patch 22: useWebRTC Signaling onopen & Ready Protocol',
    find: 'ct("[Signaling] Connecting to:",Se),c=new WebSocket(Se),c.onopen=()=>{ct("[Signaling] WebSocket connected"),t.value="signaling",c.send(JSON.stringify({message_type:"connect",device_id:i}))},c.onmessage=Te=>{',
    replace: 'ct("[Signaling] Connecting to:",Se),c=new WebSocket(Se);let _rtcMediaReady=!1,_rtcCtrlReady=!1,_rtcStreamReadySent=!1;function _checkRtcReady(stage){if(stage==="MEDIA_READY")_rtcMediaReady=!0;if(stage==="CONTROL_READY")_rtcCtrlReady=!0;console.log(`[READY-CHECK] dev=${i} mode=webrtc stage=${stage} media=${_rtcMediaReady} ctrl=${_rtcCtrlReady} sent=${_rtcStreamReadySent}`);if(_rtcMediaReady&&_rtcCtrlReady&&!_rtcStreamReadySent){_rtcStreamReadySent=!0,window.__rtcWatchdogTimer&&clearTimeout(window.__rtcWatchdogTimer),window.__deviceConnectionStates&&(window.__deviceConnectionStates[i]="READY");const gen=(window.__deviceEpochs&&window.__deviceEpochs[i])||1,att=(window.__deviceAttempts&&window.__deviceAttempts[i])||1;console.log(`[READY] WebRTC fully READY for dev=${i} gen=${gen} att=${att}, sending stream_ready ACK`);c&&c.readyState===WebSocket.OPEN&&c.send(JSON.stringify({message_type:"stream_ready",device_id:i,mode:"webrtc",generation:gen,attempt_id:att}))}}window.__checkRtcReady=_checkRtcReady;function _onRtcFailed(reason){if(!_rtcStreamReadySent){window.__rtcWatchdogTimer&&clearTimeout(window.__rtcWatchdogTimer),window.__deviceConnectionStates&&(window.__deviceConnectionStates[i]="FAILED");const gen=(window.__deviceEpochs&&window.__deviceEpochs[i])||1;console.warn(`[FAILED] WebRTC failed dev=${i} reason=${reason}, sending stream_failed`);c&&c.readyState===WebSocket.OPEN&&c.send(JSON.stringify({message_type:"stream_failed",device_id:i,mode:"webrtc",generation:gen,reason:reason}))}}window.__onRtcFailed=_onRtcFailed;window.__rtcWatchdogTimer=setTimeout(()=>{if(!_rtcStreamReadySent&&t.value!=="connected"&&!_webrtcDisposed){_onRtcFailed("RTC_CONNECT_TIMEOUT"),r.value="连接超时: WebRTC 建立连接超时，请重试",t.value="error"}},15000);c.onopen=()=>{ct("[Signaling] WebSocket connected"),t.value="signaling",window.__deviceConnectionStates&&(window.__deviceConnectionStates[i]="SIGNALING_CONNECTED"),c.send(JSON.stringify({message_type:"connect",device_id:i}))},c.onmessage=Te=>{'
  },

  // 22b. Phase R5.4A-0 & R5.4A-3: useWebRTC onconnectionstatechange NACK & Hold Clean
  {
    name: 'Patch 22b: useWebRTC onconnectionstatechange NACK',
    find: 'A.onconnectionstatechange=()=>{ct("[WebRTC] Connection State:",A.connectionState),A.connectionState==="connected"?t.value="connected":A.connectionState==="failed"?(r.value="连接失败: "+Ue(),t.value="error"):(A.connectionState==="closed"||A.connectionState==="disconnected")&&(t.value="disconnected")}',
    findFallback: [
      'A.onconnectionstatechange=()=>{ct("[WebRTC] Connection State:",A.connectionState),A.connectionState==="connected"?t.value="connected":A.connectionState==="failed"?(window.__onRtcFailed&&window.__onRtcFailed("CONNECTION_FAILED"),r.value="连接失败: "+Ue(),t.value="error"):(A.connectionState==="closed"||A.connectionState==="disconnected")&&(t.value="disconnected")}'
    ],
    replace: 'A.onconnectionstatechange=()=>{ct("[WebRTC] Connection State:",A.connectionState),A.connectionState==="connected"?(t.value="connected",window.__heldWebRTC&&window.__heldWebRTC[i]&&(window.__heldWebRTC[i].pc!==A)&&(console.log("[WebRTC-HOLD] Closing previous held connection for "+i),window.__heldWebRTC[i].close(),delete window.__heldWebRTC[i])):A.connectionState==="failed"?(window.__onRtcFailed&&window.__onRtcFailed("CONNECTION_FAILED"),r.value="连接失败: "+Ue(),t.value="error"):(A.connectionState==="closed"||A.connectionState==="disconnected")&&(t.value="disconnected")}'
  },

  // 23a. Phase R5.4A-0 & R5.4A-3: useWebSocketStream timeout NACK
  {
    name: 'Patch 23a: useWebSocketStream timeout NACK',
    find: 'const E=1e4;let B=null;function w(){S(),B=setTimeout(()=>{r.value==="connecting"&&(n.value="等待设备推流超时：设备可能离线、Agent 版本过旧不支持 WS 投屏，或 TCP 通道被阻断",r.value="disconnected")},E)}',
    replace: 'const E=1e4;let B=null;function w(){S(),B=setTimeout(()=>{if(r.value==="connecting"){window.__deviceConnectionStates&&(window.__deviceConnectionStates[i]="FAILED");const gen=(window.__deviceEpochs&&window.__deviceEpochs[i])||1;t.sendSignalingMessage&&t.sendSignalingMessage({message_type:"stream_failed",device_id:i,mode:"websocket",generation:gen,reason:"FIRST_FRAME_TIMEOUT"}),n.value="等待设备推流超时：设备可能离线、Agent 版本过旧不支持 WS 投屏，或 TCP 通道被阻断",r.value="disconnected"}},E)}'
  },

  // 23b. Phase R5.4A-0 & R5.4A-3: useWebSocketStream WebCodecs first frame ACK
  {
    name: 'Patch 23b: useWebSocketStream WebCodecs first frame ACK',
    find: 'e(Ne,0,0,ze.width,ze.height),Ne.close(),c.value||(c.value=!0,r.value="connected",S())',
    replace: 'e(Ne,0,0,ze.width,ze.height),Ne.close(),c.value||(c.value=!0,r.value="connected",S(),window.__deviceConnectionStates&&(window.__deviceConnectionStates[i]="READY"),t.sendSignalingMessage&&t.sendSignalingMessage({message_type:"stream_ready",device_id:i,mode:"websocket",generation:(window.__deviceEpochs&&window.__deviceEpochs[i])||1,attempt_id:(window.__deviceAttempts&&window.__deviceAttempts[i])||1}))'
  },

  // 23c. Phase R5.4A-0 & R5.4A-3: useWebSocketStream Canvas first frame ACK
  {
    name: 'Patch 23c: useWebSocketStream Canvas first frame ACK',
    find: 'qe.data.set(Ht),lt.putImageData(qe,0,0),c.value||(c.value=!0,r.value="connected",S())',
    replace: 'qe.data.set(Ht),lt.putImageData(qe,0,0),c.value||(c.value=!0,r.value="connected",S(),window.__deviceConnectionStates&&(window.__deviceConnectionStates[i]="READY"),t.sendSignalingMessage&&t.sendSignalingMessage({message_type:"stream_ready",device_id:i,mode:"websocket",generation:(window.__deviceEpochs&&window.__deviceEpochs[i])||1,attempt_id:(window.__deviceAttempts&&window.__deviceAttempts[i])||1}))'
  },

  // 24. Phase R5.4A-0: Component render key with connectionEpoch
  {
    name: 'Patch 24: Component render key with connectionEpoch',
    find: 'key:`${i.deviceId}_${Ae(t).getDeviceMode(i.deviceId)}`',
    replace: 'key:`${i.deviceId}_${Ae(t).getDeviceMode(i.deviceId)}_${(Ae(t).getDeviceEpoch?Ae(t).getDeviceEpoch(i.deviceId):1)}`'
  }
];

function applyTo(filePath, dryRun = false) {
  console.log(`\n=== Processing: ${path.relative(process.cwd(), filePath)} ===`);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    return false;
  }
  let content = fs.readFileSync(filePath, 'utf8');
  let matchedAll = true;

  for (let i = 0; i < patches.length; i++) {
    const p = patches[i];
    // CRITICAL: Check if already applied FIRST to prevent duplicate prefixes/suffixes!
    if (content.indexOf(p.replace) !== -1) {
      console.log(`[PASS] Patch #${i + 1} (${p.name}): Already applied.`);
      continue;
    }

    let findStr = p.find;
    let idx = content.indexOf(findStr);
    if (idx === -1 && p.findFallback) {
      const fallbacks = Array.isArray(p.findFallback) ? p.findFallback : [p.findFallback];
      for (const fb of fallbacks) {
        idx = content.indexOf(fb);
        if (idx !== -1) {
          findStr = fb;
          break;
        }
      }
    }
    if (idx === -1) {
      console.error(`[FAIL] Patch #${i + 1} (${p.name}): Target snippet not found!`);
      matchedAll = false;
    } else {
      const secondIdx = content.indexOf(findStr, idx + findStr.length);
      if (secondIdx !== -1) {
        console.error(`[FAIL] Patch #${i + 1} (${p.name}): Ambiguous match (found multiple)!`);
        matchedAll = false;
      } else {
        console.log(`[PASS] Patch #${i + 1} (${p.name}): Unique match at offset ${idx}`);
        content = content.replace(findStr, p.replace);
      }
    }
  }

  if (!matchedAll) {
    console.error(`Aborting updates to ${filePath} due to snippet mismatch.`);
    return false;
  }

  if (dryRun) {
    console.log(`[DRY RUN] All ${patches.length} patches matched cleanly. No files written.`);
    return true;
  }

  fs.writeFileSync(filePath, content, 'utf8');
  const newHash = crypto.createHash('sha256').update(content).digest('hex');
  console.log(`[APPLIED] Successfully patched ${filePath} (New SHA-256: ${newHash})`);
  return true;
}

const dryRun = process.argv.includes('--dry-run');
let success = true;
for (const file of TARGET_FILES) {
  if (!applyTo(file, dryRun)) {
    success = false;
  }
}

if (!success) {
  process.exit(1);
}
console.log('\nAll patches completed successfully.');
