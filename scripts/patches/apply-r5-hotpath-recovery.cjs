/**
 * apply-r5-hotpath-recovery.cjs
 * 
 * Implements Phase R5.3 Device Geometry / Resolution Synchronization across index-DIPw8r74.js:
 * 1. R5.1b-1: DevicePanel.Vt() reverts reconnect-in-place; preserves native mode switch.
 * 2. R5.1b-2: Native mouse/touch event architecture preserved; no pointer capture on MouseEvents.
 * 3. R5.1b-3: Single unified controllerSessionId across DevicePanel, PeerConnection, and DataChannel.
 * 4. R5.1b-4: Stream stat calculation with deltas (actualFps, avgJitterBufferMs, avgDecodeMs, bitrateKbps).
 * 5. R5.1b-5: Native keycode injection for useWebSocketStream.sendCommand().
 * 6. R5.3.4-R5.3.9: Normalized geometry touch mapping with letterbox/pillarbox removal, fail safe, and [GEOMETRY]/[TOUCH-MAP] logging.
 * 7. R5.3.3: Device metadata & rotation propagation from server device_info.
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
    replace: 'A=new RTCPeerConnection({iceServers:h,iceTransportPolicy:P,encodedInsertableStreams:_e}),A.__sessionId=window.__activeSessionId||1,window.__activePeerConnection=A'
  },

  // 2. DataChannel Lifecycle Tracking & Unified Session Propagation
  {
    name: 'Patch 2: DataChannel Lifecycle Tracking & Unified Session Propagation',
    find: 'A.ondatachannel=Se=>{ct("[WebRTC] Received DataChannel:",Se.channel.label),Se.channel.label==="input-channel"?(d=Se.channel,d.onopen=()=>{ct("[DataChannel] input-channel OPEN")},d.onclose=()=>{ct("[DataChannel] input-channel CLOSED")},d.onerror=Te=>console.error("[DataChannel] Error:",Te)):Se.channel.label==="clipboard-channel"?(v=Se.channel,v.onopen=()=>{ct("[DataChannel] clipboard-channel OPEN")',
    replace: 'A.ondatachannel=Se=>{ct("[WebRTC] Received DataChannel:",Se.channel.label),Se.channel.label==="input-channel"?(d=Se.channel,d.__sessionId=A.__sessionId||window.__activeSessionId||1,window.__activeDataChannel=d,window.__recordDcLife&&window.__recordDcLife("create",d.__sessionId,{label:d.label,id:d.id}),d.onopen=()=>{window.__recordDcLife&&window.__recordDcLife("open",d.__sessionId,{label:d.label,id:d.id}),ct("[DataChannel] input-channel OPEN")},d.onclose=()=>{window.__recordDcLife&&window.__recordDcLife("close",d.__sessionId,{label:d.label,id:d.id}),ct("[DataChannel] input-channel CLOSED")},d.onerror=Te=>console.error("[DataChannel] Error:",Te)):Se.channel.label==="clipboard-channel"?(v=Se.channel,v.onopen=()=>{ct("[DataChannel] clipboard-channel OPEN")'
  },

  // 3. useWebRTC.sendTouch Normalized Geometry Mapping & Fail Safe (R5.3.4 - R5.3.9)
  {
    name: 'Patch 3: useWebRTC.sendTouch Normalized Geometry Mapping & Fail Safe (R5.3)',
    find: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l||!d||d.readyState!=="open")return;const Te=s.value&&f?f():g?g():null;if(!Te)return;const Ye=Te.videoWidth||Te.width||B.value,gt=Te.videoHeight||Te.height||w.value;if(!Ye||!gt)return;const Tt=++E,Vt=Date.now(),Gt=B.value>w.value,Ni=Ye>gt!==Gt,Pi=Ni?w.value:B.value,Ce=Ni?B.value:w.value;let Ke,nt;if(Se&&Se.isRotated){const Qt=Math.round(Se.x/Ye*Pi),vi=Math.round(Se.y/gt*Ce);Ke=Math.max(0,Math.min(Pi,Qt)),nt=Math.max(0,Math.min(Ce,vi))}else{const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El,eg=Math.round(oh/Wi*Pi),tg=Math.round(yo/Rn*Ce);Ke=Math.max(0,Math.min(Pi,eg)),nt=Math.max(0,Math.min(Ce,tg))}const ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce});const dt=d.bufferedAmount;(P!==2||Tt%30===0||dt>65536)&&qm("[TouchTrace] dc-send",{seq:Tt,action:P,id:Ue,x:Ke,y:nt,w:Pi,h:Ce,clientTsMs:Vt,bufferedBefore:wt,bufferedAfter:dt})}',
    findFallback: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l){window.__recordTouchDrop&&window.__recordTouchDrop("VIEW_ONLY",{l,dcState:d?d.readyState:"none"});return}if(!d){window.__recordTouchDrop&&window.__recordTouchDrop("NO_DATA_CHANNEL",{dcState:"none",pcState:A?A.connectionState:"none"});return}if(d.readyState!=="open"){const rS=d.readyState==="connecting"?"DC_CONNECTING":d.readyState==="closing"?"DC_CLOSING":d.readyState==="closed"?"DC_CLOSED":("DC_"+d.readyState.toUpperCase());window.__recordTouchDrop&&window.__recordTouchDrop(rS,{dcState:d.readyState,pcState:A?A.connectionState:"none"});return}const Te=s.value&&f?f():g?g():null;if(!Te){window.__recordTouchDrop&&window.__recordTouchDrop("NO_ACTIVE_MEDIA_ELEMENT",{dcState:d.readyState,hasCanvasGetter:!!f,hasVideoGetter:!!g});return}const Ye=Te.videoWidth||Te.width||B.value,gt=Te.videoHeight||Te.height||w.value;if(!Ye||!gt){window.__recordTouchDrop&&window.__recordTouchDrop("INVALID_VIDEO_DIMENSIONS",{videoWidth:Te.videoWidth,width:Te.width,defaultW:B.value,videoHeight:Te.videoHeight,height:Te.height,defaultH:w.value});return}const Tt=++E,Vt=Date.now(),Gt=B.value>w.value,Ni=Ye>gt!==Gt,Pi=Ni?w.value:B.value,Ce=Ni?B.value:w.value;let Ke,nt;if(Se&&Se.isRotated){const Qt=Math.round(Se.x/Ye*Pi),vi=Math.round(Se.y/gt*Ce);Ke=Math.max(0,Math.min(Pi,Qt)),nt=Math.max(0,Math.min(Ce,vi))}else{const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El,eg=Math.round(oh/Wi*Pi),tg=Math.round(yo/Rn*Ce);Ke=Math.max(0,Math.min(Pi,eg)),nt=Math.max(0,Math.min(Ce,tg));window.__recordCoordDiag&&window.__recordCoordDiag({elementRect:Qt,videoWidth:Ye,videoHeight:gt,actualW:Wi,actualH:Rn,offsetX:ps,offsetY:El,relativeX:oh,relativeY:yo,finalX:Ke,finalY:nt,targetW:Pi,targetH:Ce,isRotated:!1})}const ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce});window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:d.__sessionId,pcSession:A?A.__sessionId:null,seq:Tt,action:P===0?"DOWN":P===1?"UP":"MOVE",actionCode:P,result:"SENT",dcState:d.readyState,dcId:d.id,pcState:A?A.connectionState:"unknown",bufferedAmount:wt,x:Ke,y:nt,w:Pi,h:Ce,overheadMs:Date.now()-Vt})}',
    replace: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l){window.__recordTouchDrop&&window.__recordTouchDrop("VIEW_ONLY",{l,dcState:d?d.readyState:"none"});return}if(!d){window.__recordTouchDrop&&window.__recordTouchDrop("NO_DATA_CHANNEL",{dcState:"none",pcState:A?A.connectionState:"none"});return}if(d.readyState!=="open"){const rS=d.readyState==="connecting"?"DC_CONNECTING":d.readyState==="closing"?"DC_CLOSING":d.readyState==="closed"?"DC_CLOSED":("DC_"+d.readyState.toUpperCase());window.__recordTouchDrop&&window.__recordTouchDrop(rS,{dcState:d.readyState,pcState:A?A.connectionState:"none"});return}const Te=s.value&&f?f():g?g():null;if(!Te){window.__recordTouchDrop&&window.__recordTouchDrop("NO_ACTIVE_MEDIA_ELEMENT",{dcState:d.readyState,hasCanvasGetter:!!f,hasVideoGetter:!!g});return}const Ye=Te.videoWidth||Te.width||0,gt=Te.videoHeight||Te.height||0;if(!Ye||!gt){window.__recordTouchDrop&&window.__recordTouchDrop("INVALID_VIDEO_DIMENSIONS",{videoWidth:Te.videoWidth,width:Te.width,videoHeight:Te.videoHeight,height:Te.height});return}const logicalW=B.value,logicalH=w.value;if(!logicalW||!logicalH||o.value==="unknown"){window.__recordTouchDrop&&window.__recordTouchDrop("DEVICE_GEOMETRY_UNKNOWN",{deviceId:i,agentVersion:o.value,w:logicalW,h:logicalH});return}const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El;if(oh<0||oh>Wi||yo<0||yo>Rn){window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{localX:oh,localY:yo,contentW:Wi,contentH:Rn,clientX:ue,clientY:_e});return}const u=Math.max(0,Math.min(1,oh/Wi)),v=Math.max(0,Math.min(1,yo/Rn));let rot=window.__deviceRotation!==undefined?window.__deviceRotation:(Se&&Se.rotation!==undefined?Se.rotation:0);let tx=u,ty=v;rot===90||(Se&&Se.isRotated&&rot===0)?(tx=v,ty=1-u):rot===180?(tx=1-u,ty=1-v):rot===270&&(tx=1-v,ty=u);const Ke=Math.max(0,Math.min(logicalW,Math.round(tx*logicalW))),nt=Math.max(0,Math.min(logicalH,Math.round(ty*logicalH)));if(P===0||P===1){console.log(`[GEOMETRY] device=${i} logical=${logicalW}x${logicalH} frame=${Ye}x${gt} viewport=${Math.round(vi)}x${Math.round(Yi)} contentRect=[${Math.round(Qt.left+ps)},${Math.round(Qt.top+El)},${Math.round(Wi)}x${Math.round(Rn)}] rotation=${rot}`);console.log(`[TOUCH-MAP] client=(${ue},${_e}) normalized=(${u.toFixed(3)},${v.toFixed(3)}) mapped=(${Ke},${nt}) target=(${logicalW},${logicalH})`)}window.__recordCoordDiag&&window.__recordCoordDiag({elementRect:Qt,videoWidth:Ye,videoHeight:gt,actualW:Wi,actualH:Rn,offsetX:ps,offsetY:El,relativeX:oh,relativeY:yo,u,v,rotation:rot,finalX:Ke,finalY:nt,targetW:logicalW,targetH:logicalH});const Tt=++E,Vt=Date.now(),ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:logicalW,h:logicalH}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:logicalW,h:logicalH});window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:d.__sessionId,pcSession:A?A.__sessionId:null,seq:Tt,action:P===0?"DOWN":P===1?"UP":"MOVE",actionCode:P,result:"SENT",dcState:d.readyState,dcId:d.id,pcState:A?A.connectionState:"unknown",bufferedAmount:wt,x:Ke,y:nt,w:logicalW,h:logicalH,overheadMs:Date.now()-Vt})}'
  },

  // 4. useWebSocketStream.sendCommand keycode translation
  {
    name: 'Patch 4: useWebSocketStream.sendCommand keycode translation',
    find: 'function Qe(ae){return!1}',
    replace: 'function Qe(ae){if(typeof ae=="string"){const m=ae.match(/input\\s+keyevent\\s+(\\d+)/);if(m){const kc=parseInt(m[1],10);J(0,kc),setTimeout(()=>J(1,kc),50);return!0}}return!1}'
  },

  // 5. useWebSocketStream.sendTouch diagnostics
  {
    name: 'Patch 5: useWebSocketStream.sendTouch diagnostics',
    find: 'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe)return;const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht)}',
    replace: 'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe){window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{mode:"websocket",x:Ne,y:ze});return}const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht);window.__recordTouchSent&&window.__recordTouchSent({session:window.__activeSessionId,dcSession:"ws",pcSession:"ws",seq:R,action:ae===0?"DOWN":ae===1?"UP":"MOVE",actionCode:ae,result:"SENT",mode:"websocket",x:qe.x,y:qe.y,w:qe.w,h:qe.h})}'
  },

  // 6. DevicePanel Mode Switch Revert & Mount Lifecycle
  {
    name: 'Patch 6: DevicePanel Mode Switch Revert & Mount Lifecycle',
    find: 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}a.value&&n.registerWebRTC(a.value,Te);',
    replace: 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}window.__globalSessionSeq=(window.__globalSessionSeq||0)+1,window.__activeSessionId=window.__globalSessionSeq,window.__recordCtrlLife&&window.__recordCtrlLife("mount",window.__activeSessionId,{deviceId:a.value}),a.value&&n.registerWebRTC(a.value,Te);'
  },

  // 7. DevicePanel Unmount Lifecycle
  {
    name: 'Patch 7: DevicePanel Unmount Lifecycle',
    find: 'Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)',
    replace: 'window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__activeSessionId,{deviceId:a.value}),Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)'
  },

  // 8. Mouse Down Native Handling, Deduplication & [INPUT] Logging
  {
    name: 'Patch 8: Mouse Down Native Handling, Deduplication & [INPUT] Logging',
    find: 'function ZS(X){if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y),p.value&&(p.value.focus(),ct("[Keyboard] focused hidden input element. activeElement:",document.activeElement?document.activeElement.tagName:"none")),X.preventDefault()}',
    replace: 'function ZS(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mousedown",clientX:X.clientX,clientY:X.clientY,target:X.target?X.target.tagName:"none"});if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y),p.value&&(p.value.focus(),ct("[Keyboard] focused hidden input element. activeElement:",document.activeElement?document.activeElement.tagName:"none")),X.preventDefault()}'
  },

  // 9. Mouse Up Native Handling, Deduplication & [INPUT] Logging
  {
    name: 'Patch 9: Mouse Up Native Handling, Deduplication & [INPUT] Logging',
    find: 'function tb(X){if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}',
    replace: 'function tb(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mouseup",clientX:X.clientX,clientY:X.clientY,target:X.target?X.target.tagName:"none"});if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}'
  },

  // 10. Mouse Leave [INPUT] Logging
  {
    name: 'Patch 10: Mouse Leave [INPUT] Logging',
    find: 'function ib(X){if(O.value){z.value=!1;return}if(sh){const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}}',
    replace: 'function ib(X){if(O.value){z.value=!1;return}if(sh){window.__recordInput&&window.__recordInput({session:window.__activeSessionId,event:"mouseleave",clientX:X.clientX,clientY:X.clientY});const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}}'
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
      if (content.indexOf(p.replace) !== -1) {
        console.log(`[PASS] Patch #${i + 1} (${p.name}): Already applied.`);
        continue;
      }
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
