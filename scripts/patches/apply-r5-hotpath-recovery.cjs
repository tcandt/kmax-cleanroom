/**
 * apply-r5-hotpath-recovery.cjs
 * 
 * Implements Phase R5 Direct Input Hot-Path Recovery across index-DIPw8r74.js:
 * 1. R5.2: useWebSocketStream.sendCommand() implements native inject_keycode translation (DOWN -> 50ms -> UP).
 * 2. R5.2: DevicePanel.Vt() rebinds active stream controller on mode switch.
 * 3. R5.3: useWebRTC.sendTouch() instruments explicit drop reasons (VIEW_ONLY, NO_DATA_CHANNEL, DC_CONNECTING, etc.).
 * 4. R5.4: PeerConnection, DataChannel and DevicePanel controller generation tracking (pcGen, dcGen, activeGen).
 * 5. R5.5: Pointer capture, deduplication (touch vs mouse), and pointer lifecycle logging.
 * 6. R5.6: Coordinate path diagnostic recording.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const TARGET_FILES = [
  path.resolve(__dirname, '../../reconstructed_source/web-app/public/assets/index-DIPw8r74.js'),
  path.resolve(__dirname, '../../reconstructed_source/web-app/dist/assets/index-DIPw8r74.js')
];

const patches = [
  // 1. PeerConnection Generation & Active PC Ref
  {
    name: 'R5.4: PeerConnection Creation Tracking',
    find: 'A=new RTCPeerConnection({iceServers:h,iceTransportPolicy:P,encodedInsertableStreams:_e})',
    replace: 'window.__pcGeneration=(window.__pcGeneration||0)+1,A=new RTCPeerConnection({iceServers:h,iceTransportPolicy:P,encodedInsertableStreams:_e}),window.__activePeerConnection=A'
  },

  // 2. DataChannel Lifecycle Tracking
  {
    name: 'R5.4: DataChannel Lifecycle Tracking',
    find: 'A.ondatachannel=Se=>{ct("[WebRTC] Received DataChannel:",Se.channel.label),Se.channel.label==="input-channel"?(d=Se.channel,d.onopen=()=>{ct("[DataChannel] input-channel OPEN")},d.onclose=()=>{ct("[DataChannel] input-channel CLOSED")},d.onerror=Te=>console.error("[DataChannel] Error:",Te)):Se.channel.label==="clipboard-channel"?(v=Se.channel,v.onopen=()=>{ct("[DataChannel] clipboard-channel OPEN")',
    replace: 'A.ondatachannel=Se=>{ct("[WebRTC] Received DataChannel:",Se.channel.label),Se.channel.label==="input-channel"?(window.__dcGeneration=(window.__dcGeneration||0)+1,d=Se.channel,window.__recordDcLife&&window.__recordDcLife("create",window.__dcGeneration,{label:d.label,id:d.id}),d.onopen=()=>{window.__recordDcLife&&window.__recordDcLife("open",window.__dcGeneration,{label:d.label,id:d.id}),ct("[DataChannel] input-channel OPEN")},d.onclose=()=>{window.__recordDcLife&&window.__recordDcLife("close",window.__dcGeneration,{label:d.label,id:d.id}),ct("[DataChannel] input-channel CLOSED")},d.onerror=Te=>console.error("[DataChannel] Error:",Te)):Se.channel.label==="clipboard-channel"?(v=Se.channel,v.onopen=()=>{ct("[DataChannel] clipboard-channel OPEN")'
  },

  // 3. useWebRTC.sendTouch Drop-Reason Diagnostics & Coordinate Recording
  {
    name: 'R5.3/R5.6: useWebRTC.sendTouch Drop Reasons & Diagnostics',
    find: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l||!d||d.readyState!=="open")return;const Te=s.value&&f?f():g?g():null;if(!Te)return;const Ye=Te.videoWidth||Te.width||B.value,gt=Te.videoHeight||Te.height||w.value;if(!Ye||!gt)return;const Tt=++E,Vt=Date.now(),Gt=B.value>w.value,Ni=Ye>gt!==Gt,Pi=Ni?w.value:B.value,Ce=Ni?B.value:w.value;let Ke,nt;if(Se&&Se.isRotated){const Qt=Math.round(Se.x/Ye*Pi),vi=Math.round(Se.y/gt*Ce);Ke=Math.max(0,Math.min(Pi,Qt)),nt=Math.max(0,Math.min(Ce,vi))}else{const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El,eg=Math.round(oh/Wi*Pi),tg=Math.round(yo/Rn*Ce);Ke=Math.max(0,Math.min(Pi,eg)),nt=Math.max(0,Math.min(Ce,tg))}const ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce});const dt=d.bufferedAmount;(P!==2||Tt%30===0||dt>65536)&&qm("[TouchTrace] dc-send",{seq:Tt,action:P,id:Ue,x:Ke,y:nt,w:Pi,h:Ce,clientTsMs:Vt,bufferedBefore:wt,bufferedAfter:dt})}',
    replace: 'function Ot(P,ue,_e,Ue=0,Se=null){if(l){window.__recordTouchDrop&&window.__recordTouchDrop("VIEW_ONLY",{l,dcState:d?d.readyState:"none"});return}if(!d){window.__recordTouchDrop&&window.__recordTouchDrop("NO_DATA_CHANNEL",{dcState:"none",pcState:A?A.connectionState:"none"});return}if(d.readyState!=="open"){const rS=d.readyState==="connecting"?"DC_CONNECTING":d.readyState==="closing"?"DC_CLOSING":d.readyState==="closed"?"DC_CLOSED":("DC_"+d.readyState.toUpperCase());window.__recordTouchDrop&&window.__recordTouchDrop(rS,{dcState:d.readyState,pcState:A?A.connectionState:"none"});return}const Te=s.value&&f?f():g?g():null;if(!Te){window.__recordTouchDrop&&window.__recordTouchDrop("NO_ACTIVE_MEDIA_ELEMENT",{dcState:d.readyState,hasCanvasGetter:!!f,hasVideoGetter:!!g});return}const Ye=Te.videoWidth||Te.width||B.value,gt=Te.videoHeight||Te.height||w.value;if(!Ye||!gt){window.__recordTouchDrop&&window.__recordTouchDrop("INVALID_VIDEO_DIMENSIONS",{videoWidth:Te.videoWidth,width:Te.width,defaultW:B.value,videoHeight:Te.videoHeight,height:Te.height,defaultH:w.value});return}const Tt=++E,Vt=Date.now(),Gt=B.value>w.value,Ni=Ye>gt!==Gt,Pi=Ni?w.value:B.value,Ce=Ni?B.value:w.value;let Ke,nt;if(Se&&Se.isRotated){const Qt=Math.round(Se.x/Ye*Pi),vi=Math.round(Se.y/gt*Ce);Ke=Math.max(0,Math.min(Pi,Qt)),nt=Math.max(0,Math.min(Ce,vi))}else{const Qt=Te.getBoundingClientRect(),vi=Qt.width,Yi=Qt.height,Fi=Ye/gt,Ln=vi/Yi;let Wi,Rn,ps,El;Ln>Fi?(Rn=Yi,Wi=Yi*Fi,ps=(vi-Wi)/2,El=0):(Wi=vi,Rn=vi/Fi,ps=0,El=(Yi-Rn)/2);const oh=ue-Qt.left-ps,yo=_e-Qt.top-El,eg=Math.round(oh/Wi*Pi),tg=Math.round(yo/Rn*Ce);Ke=Math.max(0,Math.min(Pi,eg)),nt=Math.max(0,Math.min(Ce,tg));window.__recordCoordDiag&&window.__recordCoordDiag({elementRect:Qt,videoWidth:Ye,videoHeight:gt,actualW:Wi,actualH:Rn,offsetX:ps,offsetY:El,relativeX:oh,relativeY:yo,finalX:Ke,finalY:nt,targetW:Pi,targetH:Ce,isRotated:!1})}const ut=JSON.stringify({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce}),wt=d.bufferedAmount;d.send(ut),S&&S({type:"touch",id:Ue,seq:Tt,client_ts_ms:Vt,action:P,x:Ke,y:nt,w:Pi,h:Ce,bufferedAmount:wt});window.__recordTouchSent&&window.__recordTouchSent({seq:Tt,action:P===0?"DOWN":P===1?"UP":"MOVE",actionCode:P,result:"SENT",dcState:d.readyState,dcId:d.id,pcState:A?A.connectionState:"unknown",bufferedAmount:wt,x:Ke,y:nt,w:Pi,h:Ce,ctrlGen:window.__ctrlGeneration,dcGen:window.__dcGeneration,overheadMs:Date.now()-Vt})}'
  },

  // 4. useWebSocketStream.sendCommand Translation (R5.2)
  {
    name: 'R5.2: useWebSocketStream.sendCommand keycode translation',
    find: 'function Qe(ae){return!1}',
    replace: 'function Qe(ae){if(typeof ae=="string"){const m=ae.match(/input\\s+keyevent\\s+(\\d+)/);if(m){const kc=parseInt(m[1],10);J(0,kc),setTimeout(()=>J(1,kc),50);return!0}}return!1}'
  },

  // 5. useWebSocketStream.sendTouch Diagnostic Hook
  {
    name: 'R5.3: useWebSocketStream.sendTouch diagnostics',
    find: 'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe)return;const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht)}',
    replace: 'function z(ae,Ne,ze,et=0,lt=null){const qe=fe(Ne,ze,lt);if(!qe){window.__recordTouchDrop&&window.__recordTouchDrop("OUTSIDE_RENDERED_CONTENT",{mode:"websocket",x:Ne,y:ze});return}const ht=Date.now();if(ae===2){const se=qe.x-T,he=qe.y-O,ge=se*se+he*he;if(ht-q<K&&ge<W)return;q=ht,T=qe.x,O=qe.y}else ae===0&&(R++,q=0,T=qe.x,O=qe.y);const Ht={type:"touch",action:ae,x:qe.x,y:qe.y,w:qe.w,h:qe.h,id:et,seq:R,client_ts_ms:ht};t.sendGroupControlEvent([i],Ht),_&&_(Ht);window.__recordTouchSent&&window.__recordTouchSent({seq:R,action:ae===0?"DOWN":ae===1?"UP":"MOVE",actionCode:ae,result:"SENT",mode:"websocket",x:qe.x,y:qe.y,w:qe.w,h:qe.h,ctrlGen:window.__ctrlGeneration})}'
  },

  // 6. DevicePanel Mode Switch Re-init & Mount Lifecycle (R5.2, R5.4)
  {
    name: 'R5.2/R5.4: DevicePanel Mode Switch Re-init & Mount Lifecycle',
    find: 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}a.value&&n.registerWebRTC(a.value,Te);',
    replace: 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X);a.value&&(Te.disconnect(),Se.value=Ue(a.value,T.value),n.registerWebRTC(a.value,Te),yo())}window.__ctrlGeneration=(window.__ctrlGeneration||0)+1,window.__recordCtrlLife&&window.__recordCtrlLife("mount",window.__ctrlGeneration,{deviceId:a.value}),a.value&&n.registerWebRTC(a.value,Te);'
  },

  // 7. DevicePanel Unmount Lifecycle (R5.4)
  {
    name: 'R5.4: DevicePanel Unmount Lifecycle',
    find: 'Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)',
    replace: 'window.__recordCtrlLife&&window.__recordCtrlLife("dispose",window.__ctrlGeneration,{deviceId:a.value}),Te.disconnect(),a.value&&n.unregisterWebRTC(a.value)'
  },

  // 8. DevicePanel Pointer Capture & Touch Deduplication (R5.5)
  {
    name: 'R5.5: Pointer Capture & Deduplication (down)',
    find: 'function ZS(X){if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y)',
    replace: 'function ZS(X){if(window.__lastTouchTs&&Date.now()-window.__lastTouchTs<500)return;if(O.value){V.value>1&&(z.value=!0,J.x=X.clientX,J.y=X.clientY,U.x=j.value,U.y=fe.value),X.preventDefault();return}if(X.button===1){Te.sendInjectKeycode(0,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(0,4),X.preventDefault();return}X.target&&X.target.setPointerCapture&&X.pointerId!==undefined&&X.target.setPointerCapture(X.pointerId);window.__recordPointer&&window.__recordPointer({event:"down",pointerId:X.pointerId,buttons:X.buttons,target:X.target?X.target.tagName:"none",insideVideo:!0,controllerGen:window.__ctrlGeneration});const Y=ys(X.clientX,X.clientY);sh=!0,n.focusDevice(a.value),Te.sendTouch(0,X.clientX,X.clientY,-1,Y)'
  },

  {
    name: 'R5.5: Pointer Release & Lifecycle (up)',
    find: 'function tb(X){if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}',
    replace: 'function tb(X){if(O.value){z.value=!1;return}if(X.button===1){Te.sendInjectKeycode(1,3),X.preventDefault();return}if(X.button===2){Te.sendInjectKeycode(1,4),X.preventDefault();return}X.target&&X.target.releasePointerCapture&&X.pointerId!==undefined&&X.target.releasePointerCapture(X.pointerId);window.__recordPointer&&window.__recordPointer({event:"up",pointerId:X.pointerId,buttons:X.buttons,target:X.target?X.target.tagName:"none",insideVideo:!0,controllerGen:window.__ctrlGeneration});const Y=ys(X.clientX,X.clientY);sh=!1,Te.sendTouch(1,X.clientX,X.clientY,-1,Y)}'
  },

  {
    name: 'R5.5: Touch Timestamp Marker for Deduplication',
    find: 'function rb(X){if(!O.value)for(let Y=0;Y<X.changedTouches.length;Y++){const pe=X.changedTouches[Y],Je=ys(pe.clientX,pe.clientY);Te.sendTouch(0,pe.clientX,pe.clientY,pe.identifier,Je)}}',
    replace: 'function rb(X){window.__lastTouchTs=Date.now();if(!O.value)for(let Y=0;Y<X.changedTouches.length;Y++){const pe=X.changedTouches[Y],Je=ys(pe.clientX,pe.clientY);Te.sendTouch(0,pe.clientX,pe.clientY,pe.identifier,Je)}}'
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
    const idx = content.indexOf(p.find);
    if (idx === -1) {
      console.error(`[FAIL] Patch #${i + 1} (${p.name}): Target snippet not found!`);
      matchedAll = false;
    } else {
      const secondIdx = content.indexOf(p.find, idx + p.find.length);
      if (secondIdx !== -1) {
        console.error(`[FAIL] Patch #${i + 1} (${p.name}): Ambiguous match (found multiple)!`);
        matchedAll = false;
      } else {
        console.log(`[PASS] Patch #${i + 1} (${p.name}): Unique match at offset ${idx}`);
        content = content.replace(p.find, p.replace);
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
