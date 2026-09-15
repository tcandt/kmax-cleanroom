# WebRTC Signaling: Function Role Mapping Matrix

- **Total Functions Mapped**: 7571
- **CONFIRMED_ROLE**: 5187
- **INFERRED_ROLE**: 60
- **UNKNOWN**: 2324

## Critical Handlers & Core Infrastructure (Top Verified Mappings)

| Binary Symbol (Exact Garbled) | Virtual Address | Offset | Semantic Role | Classification | Conf | Evidence Notes |
|---|---|---|---|---|---|---|
| `e.moduledataverify1` | `0x401080` | `0x1080` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x401220` | `0x1220` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `048` | `0x4012a0` | `0x12a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `restack_noctxt` | `0x4018e0` | `0x18e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `17728` | `0x401a40` | `0x1a40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ld` | `0x401a80` | `0x1a80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `etg` | `0x401ac0` | `0x1ac0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ime.gcWriteBarrier1` | `0x401b00` | `0x1b00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `er4` | `0x401b40` | `0x1b40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `anicSliceAcapU` | `0x401c20` | `0x1c20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `panicSlice3Acap` | `0x402160` | `0x2160` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `lrNoHeapPointers` | `0x402a20` | `0x2a20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `1` | `0x402ea0` | `0x2ea0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `me.(*itabTableType).add-fm` | `0x402f00` | `0x2f00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e.badmorestackg0` | `0x402fc0` | `0x2fc0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `tack` | `0x403420` | `0x3420` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `me.Frame` | `0x403460` | `0x3460` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ic` | `0x403620` | `0x3620` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `n` | `0x403640` | `0x3640` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Bits` | `0x403960` | `0x3960` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `han` | `0x4039a0` | `0x39a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e` | `0x4039e0` | `0x39e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `r` | `0x403be0` | `0x3be0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `cinl` | `0x403cc0` | `0x3cc0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `n2.Kind` | `0x403dc0` | `0x3dc0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `func9` | `0x403e40` | `0x3e40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `c6` | `0x403f20` | `0x3f20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `unc3` | `0x403fe0` | `0x3fe0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `RK93P` | `0x4044a0` | `0x44a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Type).Elem` | `0x404700` | `0x4700` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `nternal/abi.(*Type).ArrayType` | `0x4049a0` | `0x49a0` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `ype` | `0x404ba0` | `0x4ba0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `l/abi.(*Type).ChanDir` | `0x405380` | `0x5380` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `UJgLIQW.ccv52cQL` | `0x405dc0` | `0x5dc0` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `JI` | `0x405f60` | `0x5f60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `2.IsNil` | `0x406260` | `0x6260` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `JgLIQW.(*cpmy87LZ).Len` | `0x406940` | `0x6940` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `9YUc` | `0x406e60` | `0x6e60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `4gkv).Load` | `0x407220` | `0x7220` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ndSwapUintptr` | `0x4076c0` | `0x76c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Lock` | `0x407920` | `0x7920` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `).Load` | `0x407d60` | `0x7d60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `).Do` | `0x4081a0` | `0x81a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `rap2` | `0x4082a0` | `0x82a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `).Load` | `0x408780` | `0x8780` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `sfk` | `0x408a60` | `0x8a60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `nc.(*D2KbQ7Jm).RUnlock` | `0x409c60` | `0x9c60` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `).Unlock` | `0x409e60` | `0x9e60` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `n5ndG.Z3PHaB_JoCsv[go.shape.struct { sync.j1FeV8wl sync.rfkcV48C295l; sync.qAhzMe sync/atomic.MWFNLWQH; sync.nrHzNdLc uint32 }]` | `0x40a480` | `0xa480` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `tomic.MWFNLWQH; sync.nrHzNdLc uint32 }]` | `0x40a680` | `0xa680` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `.interface {}]).init` | `0x40b060` | `0xb060` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `aNKJ1pca[go.shape.interface {},go.shape.interface {}]; G9edjO.q0rQfniWP sync/atomic.YI1phr; G9edjO.lxZGntXagR G9edjO.BaXkKE; G9edjO.sR_iv8MG *G9edjO.t9w5Op[go.shape.interface {},go.shape.interface {}]; G9edjO.hWHxlv_We [16]sync/atomic.WgjJZ11[go.shape.struct { G9edjO.haTaT_U7 bool }] }]).Store` | `0x40b300` | `0xb300` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| `djO.haTaT_U7 bool }] }]).Store` | `0x40bba0` | `0xbba0` | **AUTH_LOGIN_HANDLER** | `CONFIRMED_ROLE` | 0.98 | References route '/api/login' and credentials validation strings |
| ` {}]` | `0x40be60` | `0xbe60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ad` | `0x40c8c0` | `0xc8c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `elete` | `0x40d760` | `0xd760` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ace {}]).Swap` | `0x40dea0` | `0xdea0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e {}]` | `0x40e020` | `0xe020` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x40e0a0` | `0xe0a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `{}]` | `0x40e760` | `0xe760` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `A` | `0x40e980` | `0xe980` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.Read` | `0x40ec20` | `0xec20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `re` | `0x40ed00` | `0xed00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x40ed80` | `0xed80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `6` | `0x40efa0` | `0xefa0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.Close` | `0x40f100` | `0xf100` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `X).Write` | `0x40f1e0` | `0xf1e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `DYbD).Lock` | `0x40fb40` | `0xfb40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x40fd80` | `0xfd80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `38wG` | `0x40ff40` | `0xff40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x4103a0` | `0x103a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `slite.Clone` | `0x410480` | `0x10480` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ap` | `0x410b80` | `0x10b80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `G` | `0x410e00` | `0x10e00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x410ea0` | `0x10ea0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x410ee0` | `0x10ee0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Z` | `0x4113a0` | `0x113a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `9` | `0x4117c0` | `0x117c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x411fc0` | `0x11fc0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `oly.(*WHHCC_eAm).Size` | `0x4121e0` | `0x121e0` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `oN5.pyyOVDP_3CfP` | `0x412580` | `0x12580` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `NftIm` | `0x4125e0` | `0x125e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `t` | `0x412640` | `0x12640` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `a0R).Reset` | `0x412660` | `0x12660` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Sya0R).Write` | `0x412e40` | `0x12e40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `_4JsI` | `0x413260` | `0x13260` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `jII8v` | `0x414240` | `0x14240` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `int8]` | `0x414980` | `0x14980` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `go.shape.[]uint8]` | `0x4149e0` | `0x149e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `lers` | `0x414b60` | `0x14b60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `bool }]).CompareAndSwap` | `0x415220` | `0x15220` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x4153a0` | `0x153a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Yt6]` | `0x415480` | `0x15480` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `FmpT` | `0x415da0` | `0x15da0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `0.func2` | `0x415e40` | `0x15e40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x415f40` | `0x15f40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `LWQH).Load-fm` | `0x416100` | `0x16100` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `q.sync/atomic.WgjJZ11[Np_4oPl7W.cCaCfUUfY]` | `0x416180` | `0x16180` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `4gzN).Grow` | `0x416380` | `0x16380` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x4167e0` | `0x167e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `*I3EypsoZ).Replace` | `0x416ce0` | `0x16ce0` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `MzrAJ.WUcabwlfTv` | `0x416d40` | `0x16d40` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `MzrAJ.(*htkZbzAn).WriteString` | `0x417100` | `0x17100` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `lace` | `0x417860` | `0x17860` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ce` | `0x417960` | `0x17960` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `eplace` | `0x417a20` | `0x17a20` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `ng` | `0x417f00` | `0x17f00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `v0BN` | `0x418220` | `0x18220` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e` | `0x418da0` | `0x18da0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Untpg` | `0x418e40` | `0x18e40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `GOYYa.init.0` | `0x419120` | `0x19120` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `EAppendUint64` | `0x419520` | `0x19520` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `et` | `0x4195c0` | `0x195c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `hW` | `0x419620` | `0x19620` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `nit.1` | `0x419720` | `0x19720` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `8fz0a).Write` | `0x419ac0` | `0x19ac0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `w).Read` | `0x41a400` | `0x1a400` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `init.0` | `0x41a5e0` | `0x1a5e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ry` | `0x41a720` | `0x1a720` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x41a960` | `0x1a960` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `NN` | `0x41ad00` | `0x1ad00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `PZsN).Write` | `0x41ade0` | `0x1ade0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `o.shape.*uint8]` | `0x41b2a0` | `0x1b2a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `vrulCSEA[go.shape.*uint8].func1.1` | `0x41b320` | `0x1b320` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `ror` | `0x41b580` | `0x1b580` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ypt` | `0x41b740` | `0x1b740` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Iyoj4` | `0x41b940` | `0x1b940` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `t` | `0x41ba20` | `0x1ba20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ePpEI` | `0x41bea0` | `0x1bea0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `KhjUPzzED.ik1lMLzV4Sb` | `0x41c440` | `0x1c440` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `xpand_key_192b` | `0x41cea0` | `0x1cea0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `rap1` | `0x41d9e0` | `0x1d9e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `S` | `0x41db40` | `0x1db40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `scall.init.0` | `0x41de40` | `0x1de40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `TKw_O` | `0x41df00` | `0x1df00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x41e0a0` | `0x1e0a0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x41e4e0` | `0x1e4e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `4VH9rNne` | `0x41e580` | `0x1e580` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `rT` | `0x41ff60` | `0x1ff60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `o` | `0x4201c0` | `0x201c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `1` | `0x420280` | `0x20280` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `r` | `0x420800` | `0x20800` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `qVo7pKK.eK6jSeW0Y` | `0x4208a0` | `0x208a0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `func1` | `0x420f80` | `0x20f80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `y` | `0x421300` | `0x21300` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ror` | `0x421380` | `0x21380` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `03` | `0x4217c0` | `0x217c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.kZbRy0u_Uas` | `0x4218c0` | `0x218c0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `` | `0x422020` | `0x22020` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Cju` | `0x422080` | `0x22080` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `SOuk` | `0x422500` | `0x22500` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ore` | `0x4225c0` | `0x225c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `uGSUj` | `0x422620` | `0x22620` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `o7pKK.hEMWfj7ais5I.mr71pZHDltp` | `0x4226a0` | `0x226a0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `ipSo2.Date` | `0x4238e0` | `0x238e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `fZqVo7pKK.vmwI5j7CV` | `0x423ae0` | `0x23ae0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `pSo2).UnmarshalBinary` | `0x424140` | `0x24140` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `7pKK.iCmrbvoFS` | `0x424d20` | `0x24d20` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `THn4WnGr` | `0x424de0` | `0x24de0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `o7pKK.a2beqmdHIr` | `0x425140` | `0x25140` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `time.GOROOT` | `0x4252e0` | `0x252e0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `VDgFy` | `0x425620` | `0x25620` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x4256e0` | `0x256e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `nc1` | `0x425800` | `0x25800` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `K.jdn1p8qr[go.shape.[]uint8]` | `0x425ca0` | `0x25ca0` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `.string].func1` | `0x425fc0` | `0x25fc0` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `2).MarshalBinary` | `0x426340` | `0x26340` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `KK.bxmaw4FS` | `0x426a80` | `0x26a80` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `L5EGCMjy.AJyKwQDR.Type` | `0x427140` | `0x27140` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `p` | `0x427860` | `0x27860` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `kxIi3QmYF7c.jm9zjyX[go.shape.interface { Info() (_iL5EGCMjy.ZILe19MeiT, error); IsDir() bool; Name() string; Type() _iL5EGCMjy.AJyKwQDR }]` | `0x428260` | `0x28260` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `bool; Name() string; Type() _iL5EGCMjy.AJyKwQDR }]` | `0x428580` | `0x28580` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `EGCMjy.AJyKwQDR }]` | `0x428840` | `0x28840` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `MeiT, error); IsDir() bool; Name() string; Type() _iL5EGCMjy.AJyKwQDR }]` | `0x428bc0` | `0x28bc0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `_iL5EGCMjy.AJyKwQDR }]` | `0x429260` | `0x29260` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `pNMRI_rnyZT[go.shape.interface { Info() (_iL5EGCMjy.ZILe19MeiT, error); IsDir() bool; Name() string; Type() _iL5EGCMjy.AJyKwQDR }]` | `0x429740` | `0x29740` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `QDR }]` | `0x42a020` | `0x2a020` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| ` string; Type() _iL5EGCMjy.AJyKwQDR }]` | `0x42a440` | `0x2a440` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `]` | `0x42ad40` | `0x2ad40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.init.func3` | `0x42afa0` | `0x2afa0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `l` | `0x42b040` | `0x2b040` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `wrap2` | `0x42b300` | `0x2b300` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e` | `0x42b680` | `0x2b680` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `3t` | `0x42b6e0` | `0x2b6e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `CKC` | `0x42bca0` | `0x2bca0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.SetReadDeadline` | `0x42be40` | `0x2be40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `p).Read` | `0x42c5c0` | `0x2c5c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `wrap1` | `0x42c780` | `0x2c780` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `up).Pread.func1` | `0x42c840` | `0x2c840` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `cDaa` | `0x42c940` | `0x2c940` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `1` | `0x42ca20` | `0x2ca20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `1` | `0x42cd80` | `0x2cd80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `nc1` | `0x42d180` | `0x2d180` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x42d400` | `0x2d400` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ap1` | `0x42d640` | `0x2d640` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `APEp36DMpup).Writev.deferwrap1` | `0x42d9e0` | `0x2d9e0` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `; KNC8w2g.cB_5iaen runtime.Cleanup }]` | `0x42eb40` | `0x2eb40` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `.1.1` | `0x42f560` | `0x2f560` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e.[]_iL5EGCMjy.JIk9ho1n,go.shape.interface { Info() (_iL5EGCMjy.ZILe19MeiT, error); IsDir() bool; Name() string; Type() _iL5EGCMjy.AJyKwQDR }]` | `0x42f700` | `0x2f700` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `QDR }]` | `0x42f960` | `0x2f960` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `xi).hayUQGqZk0` | `0x42f9c0` | `0x2f9c0` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `WpGI3.gUoaVNONKBq *[]uint8; uOfWpGI3.iskaamU9 int; uOfWpGI3.uFt3I1TW int }]).Load` | `0x42fa20` | `0x2fa20` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| ` }]).Load` | `0x42faa0` | `0x2faa0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `CompareAndSwap` | `0x42fc40` | `0x2fc40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `I6L2EDya` | `0x42fda0` | `0x2fda0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `L` | `0x42ff60` | `0x2ff60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `VDK` | `0x4301e0` | `0x301e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `oBzH` | `0x4309c0` | `0x309c0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `k` | `0x430c00` | `0x30c00` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `onn` | `0x431460` | `0x31460` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `p1` | `0x431740` | `0x31740` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `uint8]` | `0x431a20` | `0x31a20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e7jYZkdWxi).bC10yaZxDzY` | `0x431b60` | `0x31b60` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `S2` | `0x431f40` | `0x31f40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `aSwu6GK.func1` | `0x4320c0` | `0x320c0` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `Fdeq` | `0x4327e0` | `0x327e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.func2` | `0x432880` | `0x32880` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `ad` | `0x4330e0` | `0x330e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `3.LdUraO` | `0x433680` | `0x33680` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `3.jbSo04` | `0x4339c0` | `0x339c0` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `kO).Mode` | `0x433cc0` | `0x33cc0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `fWpGI3.(*AAe7jYZkdWxi).qFWuaLi64t` | `0x433d80` | `0x33d80` | **WEBSOCKET_UPGRADE_TRANSPORT** | `INFERRED_ROLE` | 0.85 | Calls Gorilla WebSocket connection upgrader |
| `` | `0x433e40` | `0x33e40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `*AAe7jYZkdWxi).n53r0c` | `0x434000` | `0x34000` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `7kO` | `0x434420` | `0x34420` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.Close` | `0x434ec0` | `0x34ec0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `Uj).Read` | `0x435a40` | `0x35a40` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `pGI3.(*iaCIUj).Readdir` | `0x435bc0` | `0x35bc0` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `).SetReadDeadline` | `0x436220` | `0x36220` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `OfWpGI3.iaCIUj.Stat` | `0x436380` | `0x36380` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `j).SyscallConn` | `0x4364c0` | `0x364c0` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `g` | `0x436a60` | `0x36a60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `pGI3.(*dUqjJe).WriteTo` | `0x436d80` | `0x36d80` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `d` | `0x436ec0` | `0x36ec0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `OfWpGI3.b5ZGiMdgs.Seek` | `0x437240` | `0x37240` | **DEVICE_SHARING_SUBMODULE** | `CONFIRMED_ROLE` | 0.95 | References share endpoints and shares.json persistence |
| `m` | `0x437c80` | `0x37c80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x437d80` | `0x37d80` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `d` | `0x437f20` | `0x37f20` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `tCoZK` | `0x437fc0` | `0x37fc0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `hal` | `0x438020` | `0x38020` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `nit.0` | `0x438500` | `0x38500` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x4385e0` | `0x385e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `9x1Cl` | `0x438760` | `0x38760` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `.Add` | `0x438a60` | `0x38a60` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `G4eqLETXG.(*PnXhyX).Multiply` | `0x438b20` | `0x38b20` | **AUTH_STATUS_HANDLER** | `CONFIRMED_ROLE` | 0.95 | References '/api/auth-status' and 'noAuth' payload |
| `U_` | `0x439080` | `0x39080` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `e` | `0x439240` | `0x39240` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `` | `0x4396e0` | `0x396e0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `eg` | `0x439fa0` | `0x39fa0` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
| `esWithClamping` | `0x43a600` | `0x3a600` | **STANDARD_LIBRARY_COMPONENT** | `CONFIRMED_ROLE` | 1.0 | Standard library / runtime symbol preserved in pclntab |
