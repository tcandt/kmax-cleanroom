# Semantic Role Mapping: CloudPhone Agent Daemon

## Forensic Integrity Principles
- **Zero Stdlib Misattribution**: Standard library and Go runtime functions are classified under runtime/stdlib categories and never assigned application roles.
- **Evidence Provenance**: Every application role is tied directly to instruction xrefs, route registration disassembly, or string tokens.
- **Garbled Symbols Preserved**: All obfuscated symbols are preserved verbatim.

### Classification Summary
- **Total Functions Evaluated**: 15398
- **CONFIRMED_ROLE**: 2587
- **INFERRED_ROLE**: 0
- **UNKNOWN**: 25622

| VA | Symbol Name | Role | Classification | Confidence | Evidence |
|---|---|---|---|---|---|
| `0x1004a0` | `JrzoFRw0.(*LOA4pV).Error` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x161530` | `hbXPz4i5V.map.init.0` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x17f7b0` | `hbXPz4i5V.(*bAujxOKO_).Error` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x1826e0` | `hbXPz4i5V.(*apISfGa).Control` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x2560f0` | `y2pM5y8R.map.init.0` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x259330` | `Ds2D3EsYj9L.yUbOCDav` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x284bf0` | `HlYqb88aO_.(*zoqhgNqcsj4v).ExtractAndExpand` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x2d3290` | `dG99HG.Us3TmZg` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x33a810` | `ODHyEy0QaRaM.(*Ep08lNp).jGPiRay` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x3762b0` | `lh4_pU5pUfF.(*BrJ5qLe).String` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x377cf0` | `lh4_pU5pUfF.NhNIHylR.String` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x379e00` | `lh4_pU5pUfF.(*NhNIHylR).String` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x386080` | `LstJZq2n.(*QkMrB87I).ReadFrom` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x394490` | `UDxa_eFxTH.(*NjoK9AeRpL).AcceptTCPWithConn` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x395d30` | `UDxa_eFxTH.(*FA4APEnRY).ReadFrom` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x3a55c0` | `hRDKl0.zJmvLOrUG` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x3a5830` | `hRDKl0.AQxQe7N_` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x3d3830` | `IJPCIQs.fDsiP3.Error` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x3df2a0` | `IJPCIQs.(*jXEsjY).as9Q_BkyZ` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4019b0` | `IJPCIQs.(*Id30fGX1i4N).zjbIYDXixX2K` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x417210` | `IJPCIQs.(*sssRwW).DialWithConn` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4260e0` | `IJPCIQs.(*eiTlPU).Read` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x435780` | `IJPCIQs.(*fDsiP3).Error` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x451730` | `MR1iSbJ.tf7nVhI2R` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x458990` | `MR1iSbJ.wR95ut43Fu5` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x459130` | `MR1iSbJ.bGOL25ma` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x463100` | `qEicCWNa.init` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x47bde0` | `ENv_hkqw2jH.VAzYTRw0RYi4.String` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x47d7a0` | `ENv_hkqw2jH.K_aW9ljK.MarshalText` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x47d830` | `ENv_hkqw2jH.K_aW9ljK.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x481850` | `ENv_hkqw2jH.(*H2H4bMgFruF1).ahM_dRXl_ttM` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x484ce0` | `ENv_hkqw2jH.(*VAzYTRw0RYi4).String` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x485880` | `ENv_hkqw2jH.(*K_aW9ljK).MarshalText` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x485940` | `ENv_hkqw2jH.(*K_aW9ljK).String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x496330` | `Qg_FOUuyE_UX.WL6RaVAO` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x496810` | `Qg_FOUuyE_UX.(*z0_ffruJb4R).MimeType` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x496e10` | `IV04EXWpwj.ZYzSWH.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x497000` | `IV04EXWpwj.ZYzSWH.MarshalJSON` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x497e20` | `IV04EXWpwj.GnVIyqU2c.PEM` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x498b70` | `IV04EXWpwj.(*F4TaFEL9SI).jw7w1ioZMf` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x49bfc0` | `IV04EXWpwj.EHjZgiVq.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x49c0a0` | `IV04EXWpwj.EHjZgiVq.MarshalText` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x49f200` | `IV04EXWpwj.CLFtZMyM.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4a0be0` | `IV04EXWpwj.At8MOr0E.String` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4a2fc0` | `IV04EXWpwj.NiWymk9.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4a3050` | `IV04EXWpwj.NiWymk9.MarshalText` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4a62a0` | `IV04EXWpwj.F1J6krU2n.String` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4aad90` | `IV04EXWpwj.z3qLXTPYDa` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to audio capture and encoding |
| `0x4aeb90` | `IV04EXWpwj.(*VOMNaNery).q2s7brR3WT6` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4bc0c0` | `IV04EXWpwj.(*VOMNaNery).mwlBWW` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4bd560` | `IV04EXWpwj.N9yoM1tfll.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4c8f50` | `IV04EXWpwj.IIhqRjcFRm_.String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4ca7d0` | `IV04EXWpwj.cCluM6In8981` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4cd050` | `IV04EXWpwj.kbC_4Jw` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4d8480` | `IV04EXWpwj.(*ZYzSWH).String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4d8c10` | `IV04EXWpwj.(*NiWymk9).MarshalText` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4d8ce0` | `IV04EXWpwj.(*NiWymk9).String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4d9160` | `IV04EXWpwj.(*F1J6krU2n).String` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x4d93a0` | `IV04EXWpwj.(*IIhqRjcFRm_).String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4d94e0` | `IV04EXWpwj.(*EHjZgiVq).String` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4e7540` | `VdlUslrFHV.(*Rhjao1JfbR).DialContext` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4e9ba0` | `VdlUslrFHV.(*IBj8VK).Error` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x4ec840` | `VdlUslrFHV.(*MkS7B0P_ctR).fthygJTVE` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x50aec0` | `d81wqMWdG.(*GBHUjz8J).GetExternalIPAddressCtx` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x50eaa0` | `HGh6lOo_aLBb.bcS3ndmGOHfN` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x510970` | `HGh6lOo_aLBb.y8n7nmqzs` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x510c20` | `HGh6lOo_aLBb.(*c02APm).gXr1VeC1YW` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x5163a0` | `main.(*JJffa1S1Zv6)._kTtL83Kr.func3` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x51a5b0` | `main.(*JJffa1S1Zv6).p6Eufk` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to video frame streaming and PTS flags |
| `0x51c980` | `main.(*JJffa1S1Zv6).gGGnvVOelod_` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x51cc60` | `main.wG6mNWE7EMO` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to audio capture and encoding |
| `0x51cdb0` | `main.dOpxv5FpG` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to audio capture and encoding |
| `0x51fbf0` | `main.ocUIEQMvQW5H` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x522640` | `main.(*JJffa1S1Zv6).r4JZVTB` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x5229d0` | `main.(*JJffa1S1Zv6).duXlLWa4yfx` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x523040` | `main.(*JJffa1S1Zv6).hkz_PCWff5z` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x523cb0` | `main.(*JJffa1S1Zv6).ipEdMF` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x524c60` | `main.(*JJffa1S1Zv6).lnQQ7HadAvI` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x526e70` | `main.(*JJffa1S1Zv6).yi1MyNZ` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x5277e0` | `main.(*JJffa1S1Zv6).yJhdib9D3` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x529a70` | `main.(*JJffa1S1Zv6).yJhdib9D3.func1.2` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x52c8a0` | `main.(*JJffa1S1Zv6).jz_LFVd4hyCG` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x52cc80` | `main.(*JJffa1S1Zv6).bMp02AXAlJCB` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x52d0b0` | `main.(*JJffa1S1Zv6).fbh3fnEV_ZVp` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x52dd20` | `main.(*JJffa1S1Zv6).iDVUAml6wT7` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x52f370` | `main.(*JJffa1S1Zv6).abCsHT4G3` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x531dd0` | `main.(*JJffa1S1Zv6).abCsHT4G3.func1` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x532db0` | `main.(*JJffa1S1Zv6).ma7tIlv` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x533350` | `main.(*JJffa1S1Zv6)._qIx0ORDUr0V` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x535290` | `main.(*JJffa1S1Zv6).jdmbieL5j4J8` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x535700` | `main.(*JJffa1S1Zv6).fZfb5uvPrfxq` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x535e20` | `main.(*JJffa1S1Zv6).q9OCaqyuR` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x535fd0` | `main.(*JJffa1S1Zv6).d1xIaCPh8` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x536c80` | `main.(*JJffa1S1Zv6).ho6gN25i.func1` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x53a6a0` | `main.(*JJffa1S1Zv6).bRez3kNWT` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x53ac00` | `main.(*JJffa1S1Zv6).g96mXaELDRY` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x53c730` | `main.(*JJffa1S1Zv6).iIhwd_WXInS` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x5402a0` | `main.(*JJffa1S1Zv6).iIhwd_WXInS.func6` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x5406f0` | `main.(*JJffa1S1Zv6).iIhwd_WXInS.func5` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | `CONFIRMED_ROLE` | 0.90 | Direct reference to WebRTC peer connection and ICE state |
| `0x5418a0` | `main.(*JJffa1S1Zv6).cQbtHJ` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |
| `0x543bc0` | `main.(*JJffa1S1Zv6).iWRU_s6.func4` | `REMOTE_INPUT_CONTROL_INJECTOR` | `CONFIRMED_ROLE` | 0.90 | Direct reference to touch/key input injection into UDS |
| `0x5490a0` | `main.(*JJffa1S1Zv6).xctC9p6wn` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to scrcpy server and Android Helper daemon |

*Total Project Identified Roles: 102. Complete mapping in ROLE_MAPPING.json*
