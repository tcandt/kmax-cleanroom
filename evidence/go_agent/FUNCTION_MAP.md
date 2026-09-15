# CloudPhone Agent: Forensic Function Map

- **Total Functions**: 15398
- **Functions with pclntab Entries**: 15398 (100%)
- **Readable Runtime/Pion/Stdlib Functions**: 25
- **Garbled Project Functions**: 15373
- **High Confidence Identified**: 25
- **Medium Confidence Inferred**: 1407
- **Unknown / Low Confidence**: 13966
- **Total Callgraph Nodes**: 10473
- **Total Unique Directed Edges**: 52168

## 1. Project Functions (Garbled with Inferred Roles & Call Relationships)

| Virtual Address | Offset | Symbol Name (Garbled Intact) | Inferred Role | Conf | Callers | Callees | Sample Callees |
|---|---|---|---|---|---|---|---|
| `0x11000` | `0x1000` | `sDST` | UNKNOWN | `LOW` | 0 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x111d0` | `0x11d0` | `n` | UNKNOWN | `LOW` | 7 | 3 | `nmarshal, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x11260` | `0x1260` | `m).MarshalText` | UNKNOWN | `LOW` | 0 | 3 | `a9eldi, nmarshal, .func12` |
| `0x112f0` | `0x12f0` | `m).Nanosecond` | UNKNOWN | `LOW` | 0 | 2 | `a9eldi, nmarshal` |
| `0x11360` | `0x1360` | `).String` | UNKNOWN | `LOW` | 4 | 5 | `n).SupportsCertificate.func1.1, g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x11370` | `0x1370` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x11380` | `0x1380` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x11390` | `0x1390` | `uxzMSJ.(*Gr1e3YXm).YearDay` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x113a0` | `0x13a0` | `xzMSJ.(*EyxjVy5TS).String` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x113b0` | `0x13b0` | `J.(*A3uOOsj).Hours` | UNKNOWN | `LOW` | 0 | 2 | `nmarshal, .func12` |
| `0x11440` | `0x1440` | `xzMSJ.(*A3uOOsj).Minutes` | UNKNOWN | `LOW` | 6 | 0 | `None` |
| `0x11450` | `0x1450` | `Osj).Round` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x11460` | `0x1460` | `uncate` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11470` | `0x1470` | `pe:.eq.eFuxzMSJ.N1wqhWvurWU` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11480` | `0x1480` | `.eq.[1]eFuxzMSJ.mhpXcnu1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11490` | `0x1490` | `Rott4Cld).aXafDbwNmFO9` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x114a0` | `0x14a0` | `HMKC` | UNKNOWN | `LOW` | 0 | 5 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x11560` | `0x1560` | `tlbpLd9E.String` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11590` | `0x1590` | `VUDQtlbpLd9E.Perm` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x115c0` | `0x15c0` | `BzaOT988ib).Unwrap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x115f0` | `0x15f0` | `.jN0LXaQcmz7[go.shape.interface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11600` | `0x1600` | `me() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11630` | `0x1630` | `nfo() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x116b0` | `0x16b0` | `lbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11720` | `0x1720` | `sDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11740` | `0x1740` | `erface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11760` | `0x1760` | `4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11780` | `0x1780` | `ZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x117a0` | `0x17a0` | `D6d[go.shape.interface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x117c0` | `0x17c0` | `ng; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x117d0` | `0x17d0` | `X4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x117e0` | `0x17e0` | `ZfhK.wbgAan[go.shape.interface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x117f0` | `0x17f0` | `e() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 4 | 0 | `None` |
| `0x118b0` | `0x18b0` | `fo() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 4 | 2 | `e() string; Type() e1lTH4kX4.VUDQtlbpLd9E }], .func12` |
| `0x11910` | `0x1910` | `bpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11920` | `0x1920` | `IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11950` | `0x1950` | `ape.interface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 2 | `nmarshal, .func12` |
| `0x119e0` | `0x19e0` | `) e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11a00` | `0x1a00` | `Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 3 | `nmarshal, TDZ1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Add, .func12` |
| `0x11ad0` | `0x1ad0` | `IJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11b20` | `0x1b20` | `X4.(*VUDQtlbpLd9E).IsDir` | UNKNOWN | `LOW` | 0 | 2 | `TDZ1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Add, .func12` |
| `0x11be0` | `0x1be0` | `erm` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11bf0` | `0x1bf0` | `zFFm.Zi5cUmVt4Y` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11c10` | `0x1c10` | `8VcpQaUl).noSQoelnaG` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11c20` | `0x1c20` | `FrtJw1aVrww.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11c30` | `0x1c30` | `pe.interface { Chdir(string); Getenv(string); Open(string); Stat(string) }]).Load` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11c40` | `0x1c40` | `.C18E02Q` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11c50` | `0x1c50` | `fgGBp.FyJecF` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x11c60` | `0x1c60` | `C5JX` | UNKNOWN | `LOW` | 0 | 2 | `a9eldi, .func12` |
| `0x11cf0` | `0x1cf0` | `jLYF7KXE[go.shape.bool].func4` | UNKNOWN | `LOW` | 3 | 2 | `a9eldi, .func12` |
| `0x11db0` | `0x1db0` | `nit.JyjLYF7KXE[go.shape.bool].func4.1.1` | UNKNOWN | `LOW` | 24 | 4 | `ndvfuQ.go, PhLv.(*BSsluADyuaT).re5I39ze, a9eldi` |
| `0x11e80` | `0x1e80` | `.init.func3` | UNKNOWN | `LOW` | 6 | 3 | `PhLv.(*BSsluADyuaT).re5I39ze, a9eldi, .func12` |
| `0x11fa0` | `0x1fa0` | `rzoFRw0.(*QxDWTF).gUasaKKCA` | UNKNOWN | `LOW` | 7 | 8 | `WPs1, 3vJC5GCZyE).Size, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x12380` | `0x2380` | `q1b[go.shape.int64]` | UNKNOWN | `LOW` | 0 | 2 | `JLkK.go, .func12` |
| `0x123c0` | `0x23c0` | `r.deferwrap2` | UNKNOWN | `LOW` | 0 | 3 | `nmarshal, g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x12480` | `0x2480` | `t` | UNKNOWN | `LOW` | 30 | 35 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x12500` | `0x2500` | `.(*LOA4pV).Temporary` | UNKNOWN | `LOW` | 0 | 2 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x12580` | `0x2580` | `YoBNeAKaHS5).fQXsiMYX6d` | UNKNOWN | `LOW` | 0 | 2 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x12600` | `0x2600` | `xDWTF).Fsync.deferwrap1` | UNKNOWN | `LOW` | 0 | 3 | `jLYF7KXE[go.shape.bool].func4, g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x12670` | `0x2670` | `9RUCg` | UNKNOWN | `LOW` | 0 | 2 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x126f0` | `0x26f0` | `S5).iRJfrWPN9` | UNKNOWN | `LOW` | 0 | 2 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x12770` | `0x2770` | `4Cs08s9j).init` | UNKNOWN | `LOW` | 0 | 3 | `nit.JyjLYF7KXE[go.shape.bool].func4.1.1, g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x127e0` | `0x27e0` | `JrzoFRw0.(*iVwH4Cs08s9j).i64FwBgl1Vh6` | UNKNOWN | `LOW` | 0 | 3 | `a9eldi, g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x128a0` | `0x28a0` | `SetReadDeadline` | UNKNOWN | `LOW` | 0 | 3 | `.init.func3, g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x12910` | `0x2910` | `deferwrap1` | UNKNOWN | `LOW` | 4 | 13 | `Czb2.pFmiMjuOz, er, r7ZbfT` |
| `0x12920` | `0x2920` | `*QxDWTF).Fchown` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12940` | `0x2940` | `oFRw0.(*QxDWTF).Ftruncate` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12970` | `0x2970` | `e.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12980` | `0x2980` | `FRw0.(*QxDWTF).Init` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x129f0` | `0x29f0` | `oFRw0.(*A8U96i).aG1NlX4` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12a00` | `0x2a00` | `0.(*QxDWTF).SetBlocking` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12a10` | `0x2a10` | `d` | UNKNOWN | `LOW` | 15 | 55 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x12a30` | `0x2a30` | `EdwnjV` | UNKNOWN | `LOW` | 0 | 5 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x12b10` | `0x2b10` | `WTF).Read.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12b20` | `0x2b20` | `w0.(*QxDWTF).Pread.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12b30` | `0x2b30` | `eadFrom.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12b50` | `0x2b50` | `erwrap1` | UNKNOWN | `LOW` | 1 | 4 | `ne, orHJ20Z.init.EIYgRcen.func11.1.1, eadDeadline` |
| `0x12b60` | `0x2b60` | `oFRw0.(*QxDWTF).ReadMsg` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12b90` | `0x2b90` | `Inet4` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12ba0` | `0x2ba0` | `0.(*QxDWTF).ReadMsgInet6.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12bd0` | `0x2bd0` | `Y8iFZ8VNCV` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12bf0` | `0x2bf0` | `.(*QxDWTF).Pwrite` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12c00` | `0x2c00` | `).WriteToInet4` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12c10` | `0x2c10` | `6` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12c20` | `0x2c20` | `F).WriteTo.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12c40` | `0x2c40` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x12cc0` | `0x2cc0` | `*QxDWTF).WriteMsgInet6` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12cd0` | `0x2cd0` | `cept` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12cf0` | `0x2cf0` | `chmod.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12d20` | `0x2d20` | `WTF).Fstat.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12d30` | `0x2d30` | `).Dup` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12d40` | `0x2d40` | `WriteOnce` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12d50` | `0x2d50` | `QxDWTF).RawRead.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12d70` | `0x2d70` | `wrap1` | UNKNOWN | `LOW` | 4 | 20 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x12e50` | `0x2e50` | `*QxDWTF).Fchdir` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12e60` | `0x2e60` | `ll.ZAgOaxatxC` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12e70` | `0x2e70` | `(*QxDWTF).Seek.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12e90` | `0x2e90` | `FRw0.gjNGkpS7YV.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12ea0` | `0x2ea0` | `zoFRw0.xp1kFExTlw` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12eb0` | `0x2eb0` | `tsockoptInt.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12ee0` | `0x2ee0` | `0.(*QxDWTF).SetsockoptInet4Addr.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12f00` | `0x2f00` | `WZOFLGz6` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12f10` | `0x2f10` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x12f20` | `0x2f20` | `l.A_7LEUJHdY` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12f30` | `0x2f30` | `ptByte` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12f50` | `0x2f50` | `).SetsockoptIPMreq` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12fd0` | `0x2fd0` | `w0.(*QxDWTF).SetsockoptIPv6Mreq` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x12fe0` | `0x2fe0` | `erwrap1` | UNKNOWN | `LOW` | 1 | 4 | `ne, orHJ20Z.init.EIYgRcen.func11.1.1, eadDeadline` |
| `0x13000` | `0x3000` | `.upXJjU` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13030` | `0x3030` | `erwrap1` | UNKNOWN | `LOW` | 1 | 4 | `ne, orHJ20Z.init.EIYgRcen.func11.1.1, eadDeadline` |
| `0x13040` | `0x3040` | `w0.(*QxDWTF).Writev` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13050` | `0x3050` | `pTasb7T.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13060` | `0x3060` | `en runtime.Cleanup },go.shape.struct { JrzoFRw0.mecc4WFcVhT int; JrzoFRw0.dDolgEKP int; JrzoFRw0.pOTMcseg6T int }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13080` | `0x3080` | `JrzoFRw0.pOTMcseg6T int }]` | UNKNOWN | `LOW` | 0 | 5 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x13160` | `0x3160` | `JrzoFRw0.cB_5iaen runtime.Cleanup }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13170` | `0x3170` | `PhKLC1; JrzoFRw0.cB_5iaen runtime.Cleanup },go.shape.struct { JrzoFRw0.mecc4WFcVhT int; JrzoFRw0.dDolgEKP int; JrzoFRw0.pOTMcseg6T int }].func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13180` | `0x3180` | `JrzoFRw0.dDolgEKP int; JrzoFRw0.pOTMcseg6T int }].func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x131a0` | `0x31a0` | `0.(*vM9QE3).Temporary` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x131b0` | `0x31b0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x131e0` | `0x31e0` | `.JyjLYF7KXE[go.shape.interface { Error() string }].func2` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x131f0` | `0x31f0` | `ape.interface { Error() string }].func2.1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13210` | `0x3210` | ` Error() string }].func2.1.1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13220` | `0x3220` | `k.(*Jv5AQC2N).Readdirnames` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13230` | `0x3230` | `5U[go.shape.[]e1lTH4kX4.Ek0lADb,go.shape.interface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13240` | `0x3240` | `); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13260` | `0x3260` | `wrap1` | UNKNOWN | `LOW` | 4 | 20 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x132e0` | `0x32e0` | `A7[go.shape.struct { piExaqMUk.bHP15Jr sync.CC4ebv5yI; piExaqMUk.gUoaVNONKBq *[]uint8; piExaqMUk.iskaamU9 int; piExaqMUk.uFt3I1TW int }]).Load` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x132f0` | `0x32f0` | `iExaqMUk.iskaamU9 int; piExaqMUk.uFt3I1TW int }]).Load` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13310` | `0x3310` | `struct { piExaqMUk.bHP15Jr sync.CC4ebv5yI; piExaqMUk.gUoaVNONKBq *[]uint8; piExaqMUk.iskaamU9 int; piExaqMUk.uFt3I1TW int }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13340` | `0x3340` | `aamU9 int; piExaqMUk.uFt3I1TW int }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13350` | `0x3350` | `f2AK` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x133c0` | `0x33c0` | `8Pjg` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x133d0` | `0x33d0` | `piExaqMUk.IHmRs00qIFh` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x133e0` | `0x33e0` | `rror` | UNKNOWN | `LOW` | 4 | 10 | `Czb2.pFmiMjuOz, ZWj4kZX).Bits, nmarshal` |
| `0x13400` | `0x3400` | `.sEMPtiFrA` | UNKNOWN | `LOW` | 0 | 5 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x134e0` | `0x34e0` | `fCws1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x134f0` | `0x34f0` | `iExaqMUk.(*AjL2uw1).uTDUdbd` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13500` | `0x3500` | `k.(*AjL2uw1).z9RJVqBa98x` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13520` | `0x3520` | `Uk.(*AjL2uw1).Signal` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13530` | `0x3530` | `EDZHgE).f7tuxqOFIH_v` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13560` | `0x3560` | `qMUk.(*EDZHgE).Exited` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13570` | `0x3570` | `*EDZHgE).tpXHd7` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x135a0` | `0x35a0` | `HgE).SysUsage` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x135c0` | `0x35c0` | `.CZsYKv4klw` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x135d0` | `0x35d0` | `MUk.(*EDZHgE).ExitCode` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x135e0` | `0x35e0` | `aqMUk.(*AjL2uw1).b7TMUTN` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x135f0` | `0x35f0` | `.func1` | UNKNOWN | `LOW` | 9 | 17 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x13610` | `0x3610` | `Nd` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13690` | `0x3690` | `xaqMUk.(*Jv5AQC2N).Name` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x136a0` | `0x36a0` | `xaqMUk.(*Jv5AQC2N).sbOEnBOYI` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x136c0` | `0x36c0` | `piExaqMUk.(*Jv5AQC2N).ReadFrom` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x136f0` | `0x36f0` | `(*Jv5AQC2N).Write` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13700` | `0x3700` | `QC2N).WriteAt` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13770` | `0x3770` | `KHNp.WriteTo` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13780` | `0x3780` | `teString` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13790` | `0x3790` | `MnKNVBP31` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x137b0` | `0x37b0` | `HPxIARsJ` | UNKNOWN | `LOW` | 0 | 5 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x13890` | `0x3890` | `e` | UNKNOWN | `LOW` | 10 | 14 | `F).HashFunc, cHKW1j5, y0QaRaM.s7MdT0m]).Len` |
| `0x138a0` | `0x38a0` | `.(*Jv5AQC2N).SyscallConn` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x138b0` | `0x38b0` | `2N).fH4EyuwheF` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x138d0` | `0x38d0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x138e0` | `0x38e0` | `qMUk.(*Jv5AQC2N).caBw_Q7` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13910` | `0x3910` | `aqMUk.(*Jv5AQC2N).Sync` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13920` | `0x3920` | `aqMUk.(*Jv5AQC2N).qGXS8LYN` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13950` | `0x3950` | `Yy3YdIJWmv` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13970` | `0x3970` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x13980` | `0x3980` | `hape.struct { piExaqMUk.bHP15Jr sync.CC4ebv5yI; piExaqMUk.gUoaVNONKBq *[]uint8; piExaqMUk.iskaamU9 int; piExaqMUk.uFt3I1TW int }]).Swap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13990` | `0x3990` | `k.iskaamU9 int; piExaqMUk.uFt3I1TW int }]).Swap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x139b0` | `0x39b0` | `k.(*Jv5AQC2N).v3qePa` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13a30` | `0x3a30` | `nFEg.func2` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13a40` | `0x3a40` | `mRS` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13a60` | `0x3a60` | `Uk.(*_KAHUEj9iR).Type` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13a90` | `0x3a90` | `MUk.vS4bhfP7wXh` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13aa0` | `0x3aa0` | `4W[go.shape.string]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13ab0` | `0x3ab0` | `MUk.FC0QCu` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13ac0` | `0x3ac0` | `MUk.qq3x9X1J` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13ae0` | `0x3ae0` | `2uw1).hcuX75l` | UNKNOWN | `LOW` | 0 | 5 | `1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO, XaCXVM` |
| `0x13bc0` | `0x3bc0` | `k.(*AjL2uw1).hcuX75l.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13bd0` | `0x3bd0` | `iExaqMUk.(*AjL2uw1).nzdmFZarXIg.deferwrap1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13be0` | `0x3be0` | `ExaqMUk.vqeaqDax2mL.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13c00` | `0x3c00` | `init.0` | UNKNOWN | `LOW` | 1 | 9 | `.string]).Load, ZWj4kZX).Bits, AcDK_Fy.J9R_6Iy_9rFh.IsPrivate` |
| `0x13c10` | `0x3c10` | `tvz0oTJOB11Z).Read` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13c40` | `0x3c40` | `gxCGl7` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13c50` | `0x3c50` | `Uk.bwto6nt.dgrq7eNH8LB.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13c80` | `0x3c80` | `beYa5d6bEx.func2` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13ca0` | `0x3ca0` | `iExaqMUk.vT2yz2zIM3Vt` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13cb0` | `0x3cb0` | `ror` | UNKNOWN | `LOW` | 4 | 11 | `nmarshal, .func12, hape.map[string]bool,go.shape.string,go.shape.bool]` |
| `0x13cc0` | `0x3cc0` | `dE_cla` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13cd0` | `0x3cd0` | `0obh` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13cf0` | `0x3cf0` | `dn.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13d70` | `0x3d70` | `ap1` | UNKNOWN | `LOW` | 9 | 35 | `2t, gLI7afn.tG2qGKZ9XTg.func2, hfqa).rVpdr6N.func18.1` |
| `0x13dc0` | `0x3dc0` | `aqMUk.lyDlrJ` | UNKNOWN | `LOW` | 0 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x13e00` | `0x3e00` | `LhP47).IsDir` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x13e50` | `0x3e50` | `me` | UNKNOWN | `LOW` | 1 | 3 | `Uk.(*Jv5AQC2N).jH8qI8n.func1, .func1, .func12` |
| `0x13ea0` | `0x3ea0` | `.func1` | UNKNOWN | `LOW` | 9 | 17 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x14360` | `0x4360` | `Uk.(*Jv5AQC2N).jH8qI8n.func1` | UNKNOWN | `LOW` | 1 | 5 | `er, T1bAJ.JgiPo3aUOjR]).IsOnCurve, .JgiPo3aUOjR]).ScalarBaseMult` |
| `0x144c0` | `0x44c0` | `v5AQC2N).bMhuSltM` | UNKNOWN | `LOW` | 1 | 2 | `TK, .func12` |
| `0x146b0` | `0x46b0` | `TK` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x146c0` | `0x46c0` | `dGeAj` | UNKNOWN | `LOW` | 0 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x14760` | `0x4760` | `3` | UNKNOWN | `LOW` | 2 | 20 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12, WPs1` |
| `0x14a20` | `0x4a20` | `ExaqMUk._KAHUEj9iR` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14a40` | `0x4a40` | `HGbkKFMs3j0 int; piExaqMUk.ip4V3qc sync/atomic.JQTbW6; piExaqMUk.mCRvXSBXF sync.GHMC0H; piExaqMUk.ublAZg7 *piExaqMUk.h6XK8OCcPf; piExaqMUk.dvNWEG runtime.Cleanup },go.shape.*uint8]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x14a60` | `0x4a60` | `XF sync.GHMC0H; piExaqMUk.ublAZg7 *piExaqMUk.h6XK8OCcPf; piExaqMUk.dvNWEG runtime.Cleanup },go.shape.*uint8]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14a70` | `0x4a70` | `p },go.shape.*uint8]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14a80` | `0x4a80` | `p4V3qc sync/atomic.JQTbW6; piExaqMUk.mCRvXSBXF sync.GHMC0H; piExaqMUk.ublAZg7 *piExaqMUk.h6XK8OCcPf; piExaqMUk.dvNWEG runtime.Cleanup }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14a90` | `0x4a90` | `.h6XK8OCcPf; piExaqMUk.dvNWEG runtime.Cleanup }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14ae0` | `0x4ae0` | `bkKFMs3j0 int; piExaqMUk.ip4V3qc sync/atomic.JQTbW6; piExaqMUk.mCRvXSBXF sync.GHMC0H; piExaqMUk.ublAZg7 *piExaqMUk.h6XK8OCcPf; piExaqMUk.dvNWEG runtime.Cleanup },go.shape.*uint8].func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14b10` | `0x4b10` | `ExaqMUk.ublAZg7 *piExaqMUk.h6XK8OCcPf; piExaqMUk.dvNWEG runtime.Cleanup },go.shape.*uint8].func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14b50` | `0x4b50` | `8].func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14b60` | `0x4b60` | `dSwap` | UNKNOWN | `LOW` | 2 | 13 | `uDeMp8Izpi_.CloseWrite, tgJfPz.GcNk7f, XPz4i5V.(*uDeMp8Izpi_).File` |
| `0x14b70` | `0x4b70` | `aoAHGE]).Store` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14bc0` | `0x4bc0` | `I; piExaqMUk.gUoaVNONKBq *[]uint8; piExaqMUk.iskaamU9 int; piExaqMUk.uFt3I1TW int }]).Store` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14bf0` | `0x4bf0` | `ore` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14c30` | `0x4c30` | `MUk.hE4zYmsduX.Chdir` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14c40` | `0x4c40` | `(*hE4zYmsduX).Chmod` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14c50` | `0x4c50` | `E4zYmsduX.Close` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14c80` | `0x4c80` | `sduX).Fd` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14cb0` | `0x4cb0` | `d` | UNKNOWN | `LOW` | 15 | 55 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x14cd0` | `0x4cd0` | `t` | UNKNOWN | `LOW` | 30 | 35 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x14ce0` | `0x4ce0` | `dir` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14cf0` | `0x4cf0` | `sduX).Readdirnames` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14d00` | `0x4d00` | `YmsduX.SetDeadline` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14d10` | `0x4d10` | `ine` | UNKNOWN | `LOW` | 1 | 10 | `HG.(*vDaxb15Nv).p7dCoEqanwpz, er, .UnmarshalCompressed` |
| `0x14d20` | `0x4d20` | `MUk.(*hE4zYmsduX).SetWriteDeadline` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14d70` | `0x4d70` | `t` | UNKNOWN | `LOW` | 30 | 35 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x14dc0` | `0x4dc0` | `n` | UNKNOWN | `LOW` | 7 | 3 | `nmarshal, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x14df0` | `0x4df0` | `uX).Truncate` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14e20` | `0x4e20` | `uX.WriteAt` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14e50` | `0x4e50` | `hE4zYmsduX).WriteString` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14e90` | `0x4e90` | `xaqMUk.(*jscKHNp).WriteTo` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14ea0` | `0x4ea0` | `qMUk.r4lsz9gTdp.Chmod` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14eb0` | `0x4eb0` | `.(*r4lsz9gTdp).Chown` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14f00` | `0x4f00` | `r4lsz9gTdp.Fd` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14f30` | `0x4f30` | `p).Name` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14f70` | `0x4f70` | `At` | UNKNOWN | `LOW` | 9 | 5 | `.JgiPo3aUOjR]).ScalarBaseMult, nmarshal, .func12` |
| `0x14f80` | `0x4f80` | `eadDir` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14f90` | `0x4f90` | `dp.Readdir` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14fa0` | `0x4fa0` | `*r4lsz9gTdp).Readdirnames` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x14fb0` | `0x4fb0` | `Uk.r4lsz9gTdp.SetDeadline` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15000` | `0x5000` | `adDeadline` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15030` | `0x5030` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x15070` | `0x5070` | `dp).Stat` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x15080` | `0x5080` | `callConn` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x15090` | `0x5090` | `4lsz9gTdp).Truncate` | UNKNOWN | `LOW` | 0 | 2 | `big.(*JEyvNEwJVta).j5_9oxK, .func12` |
| `0x150d0` | `0x50d0` | `4lsz9gTdp.WriteAt` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15120` | `0x5120` | `qMUk.(*r4lsz9gTdp).WriteString` | UNKNOWN | `LOW` | 0 | 2 | `, .func12` |
| `0x15170` | `0x5170` | `-fm` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15180` | `0x5180` | `xe_j_u89O0.init.func1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15190` | `0x5190` | `pe.int]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x151a0` | `0x51a0` | `*lEQVhJzFZ).Error` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x151b0` | `0x51b0` | `N` | UNKNOWN | `LOW` | 1 | 3 | `hbXPz4i5V.(*u8EpLV).vE6v0Cgfuuwo.func1, .func12, dlUslrFHV.(*kDHjay8BxfB).Write` |
| `0x151d0` | `0x51d0` | `3.YNsqENKAax0` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x151f0` | `0x51f0` | `j_u89O0.(*gxe_j_u89O0).keHEsE` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15200` | `0x5200` | `.aaX63upJFzxV` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15330` | `0x5330` | `xe_j_u89O0.(*gxe_j_u89O0).dq825aEHL` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x15340` | `0x5340` | `(*gxe_j_u89O0).yzbM5vIqmuf` | UNKNOWN | `LOW` | 19 | 0 | `None` |
| `0x15350` | `0x5350` | `89O0).d4iIwyAn2_Mf` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x15360` | `0x5360` | `CKAaFG` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x15420` | `0x5420` | `j_u89O0.(*gxe_j_u89O0).llThRogAirOU` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x15440` | `0x5440` | `(*gxe_j_u89O0).hjFGwuAXG3` | UNKNOWN | `LOW` | 542 | 0 | `None` |
| `0x15580` | `0x5580` | `q17wdMHkQqV.Vt6RH2Y` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x15590` | `0x5590` | `IsVur0` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x157a0` | `0x57a0` | `wdMHkQqV.B63ntXMLm2` | UNKNOWN | `LOW` | 19 | 0 | `None` |
| `0x157b0` | `0x57b0` | `89O0.(*gxe_j_u89O0).gcYExTiArY` | UNKNOWN | `LOW` | 46 | 0 | `None` |
| `0x15890` | `0x5890` | `zh` | UNKNOWN | `LOW` | 8 | 0 | `None` |
| `0x159a0` | `0x59a0` | `gxe_j_u89O0.(*gxe_j_u89O0).pVHK96hna1` | UNKNOWN | `LOW` | 1 | 2 | `4CM, .func12` |
| `0x15a30` | `0x5a30` | `JAChiupaThd).Width` | UNKNOWN | `LOW` | 3 | 2 | `4CM, .func12` |
| `0x15aa0` | `0x5aa0` | `g` | UNKNOWN | `LOW` | 7 | 31 | `4CM, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x15b20` | `0x5b20` | `CVu36do` | UNKNOWN | `LOW` | 2 | 2 | `4CM, .func12` |
| `0x15ba0` | `0x5ba0` | `4CM` | UNKNOWN | `LOW` | 15 | 0 | `None` |
| `0x15bf0` | `0x5bf0` | `wcY` | UNKNOWN | `LOW` | 1 | 3 | `4CM, ndRTCPReader, .func12` |
| `0x15cb0` | `0x5cb0` | `u89O0.(*vJAChiupaThd).bA5qVw1acD` | UNKNOWN | `LOW` | 1 | 12 | `(*vJAChiupaThd).bofWvs.deferwrap4, 3vJC5GCZyE).Size, JAChiupaThd).Width` |
| `0x15ff0` | `0x5ff0` | `upaThd).eG6kmtHd` | UNKNOWN | `LOW` | 1 | 4 | `aThd).iUYDYm, L, ndRTCPReader` |
| `0x16110` | `0x6110` | `L` | UNKNOWN | `LOW` | 2 | 10 | `CVu36do, 89O0.(*vJAChiupaThd).mdaG2p8, alarMult` |
| `0x161e0` | `0x61e0` | `89O0.(*vJAChiupaThd).mdaG2p8` | UNKNOWN | `LOW` | 1 | 5 | `wdMHkQqV.B63ntXMLm2, _dZ59.iujecbY5, zh` |
| `0x162b0` | `0x62b0` | `aThd).iUYDYm` | UNKNOWN | `LOW` | 1 | 4 | `CVu36do, H, alarMult` |
| `0x16380` | `0x6380` | `H` | UNKNOWN | `LOW` | 1 | 7 | `wdMHkQqV.B63ntXMLm2, xe_j_u89O0.(*gxe_j_u89O0).dq825aEHL, _dZ59.iujecbY5` |
| `0x16580` | `0x6580` | `(*vJAChiupaThd).bofWvs.deferwrap4` | UNKNOWN | `LOW` | 1 | 10 | `ChiupaThd).p9INJ2Z0Wff, 9O0.(*vJAChiupaThd).bofWvs.deferwrap2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x16730` | `0x6730` | `9O0.(*vJAChiupaThd).bofWvs.deferwrap2` | UNKNOWN | `LOW` | 1 | 4 | `JAChiupaThd).Width, j_u89O0.(*vJAChiupaThd).t1BbmaSdTP, 4CM` |
| `0x168c0` | `0x68c0` | `j_u89O0.(*vJAChiupaThd).t1BbmaSdTP` | UNKNOWN | `LOW` | 1 | 8 | `.fshnkE83T3z[go.shape.int], gLI7afn.tG2qGKZ9XTg.func2, wdMHkQqV.B63ntXMLm2` |
| `0x16c40` | `0x6c40` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x16d80` | `0x6d80` | `ChiupaThd).p9INJ2Z0Wff` | UNKNOWN | `LOW` | 1 | 10 | `JAChiupaThd).Width, hd).q3knoe9m6N7, 4CM` |
| `0x16fc0` | `0x6fc0` | `hd).q3knoe9m6N7` | UNKNOWN | `LOW` | 1 | 8 | `.fshnkE83T3z[go.shape.int], gLI7afn.tG2qGKZ9XTg.func2, wdMHkQqV.B63ntXMLm2` |
| `0x17570` | `0x7570` | `gxe_j_u89O0.(*vJAChiupaThd).ojztHzz78Q` | UNKNOWN | `LOW` | 1 | 3 | `nmarshal, ndRTCPReader, .func12` |
| `0x17700` | `0x7700` | `[go.shape.int]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x17710` | `0x7710` | `.fshnkE83T3z[go.shape.int]` | UNKNOWN | `LOW` | 2 | 5 | `3vJC5GCZyE).Size, wdMHkQqV.B63ntXMLm2, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x17950` | `0x7950` | `nt]` | UNKNOWN | `LOW` | 0 | 2 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x17b80` | `0x7b80` | `ZqlIeq[go.shape.int]` | UNKNOWN | `LOW` | 2 | 7 | `er, fo, WPs1` |
| `0x17df0` | `0x7df0` | `e:.eq.gxe_j_u89O0.gxe_j_u89O0` | UNKNOWN | `LOW` | 1 | 4 | `WPs1, .UnmarshalCompressed, nmarshal` |
| `0x18080` | `0x8080` | `al3Wq.(*Lh9YvVPl_).Cap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x18090` | `0x8090` | `_al3Wq.(*Lh9YvVPl_).Grow` | UNKNOWN | `LOW` | 0 | 2 | `tring, .func12` |
| `0x180e0` | `0x80e0` | `l3Wq.(*Lh9YvVPl_).WriteByte` | UNKNOWN | `LOW` | 2 | 4 | `bindRemoteStream, VoOQ5c.(*OJTGDxy5).qOxwxJuAkW, ead` |
| `0x181f0` | `0x81f0` | `tring` | UNKNOWN | `LOW` | 7 | 20 | `bindRemoteStream, 5).Grow, ead` |
| `0x18300` | `0x8300` | `ead` | UNKNOWN | `LOW` | 5 | 2 | `.func12, bool }]).Store` |
| `0x18450` | `0x8450` | `qa).UnreadByte` | UNKNOWN | `LOW` | 0 | 3 | `3Wq.(*ZSyGVFRWwqa).Seek, big.(*jQPv4OsZGfd).ReadByte, .func12` |
| `0x184c0` | `0x84c0` | `3Wq.(*ZSyGVFRWwqa).Seek` | UNKNOWN | `LOW` | 1 | 6 | `bindRemoteStream, *pbzEUI0Eh).n3q2Pf, _al3Wq.(*ZwDsNXg8D).a29xmtTKTOB` |
| `0x18670` | `0x8670` | `_al3Wq.(*ZwDsNXg8D).a29xmtTKTOB` | UNKNOWN | `LOW` | 2 | 5 | `big.(*jQPv4OsZGfd).ReadByte, ocLmfCzb2.jRXdcvNGv.deferwrap1, .UnmarshalCompressed` |
| `0x18940` | `0x8940` | `*pbzEUI0Eh).n3q2Pf` | UNKNOWN | `LOW` | 6 | 3 | `ig.r2WKg40vITA, .UnmarshalCompressed, .func12` |
| `0x189c0` | `0x89c0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x18b30` | `0x8b30` | `String` | UNKNOWN | `LOW` | 15 | 34 | `bindRemoteStream, oOQ5c.(*OJTGDxy5).zGWejRL, GcJWf` |
| `0x18cc0` | `0x8cc0` | `GcJWf` | UNKNOWN | `LOW` | 1 | 3 | `).Params, *jQPv4OsZGfd).Width, .func12` |
| `0x18eb0` | `0x8eb0` | `bvaYlEgi).WriteString` | UNKNOWN | `LOW` | 1 | 5 | `bindRemoteStream, _al3Wq.(*wX2IWC).Replace, fo` |
| `0x19000` | `0x9000` | `_al3Wq.(*wX2IWC).Replace` | UNKNOWN | `LOW` | 1 | 2 | `*jQPv4OsZGfd).Width, .func12` |
| `0x19070` | `0x9070` | `R` | UNKNOWN | `LOW` | 2 | 14 | `bindRemoteStream, er, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` |
| `0x192f0` | `0x92f0` | `shStrRev[go.shape.string]` | UNKNOWN | `LOW` | 4 | 3 | `shStrRev[go.shape.string], jLYF7KXE[go.shape.bool].func4, .func12` |
| `0x19530` | `0x9530` | `q.vQf0rXZL` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x19540` | `0x9540` | `F971c5fr` | UNKNOWN | `LOW` | 0 | 3 | `.jyMbeRUWPs1.func1, .G2Rzf5wkmWe[go.shape.[]string,go.shape.string], .func12` |
| `0x195a0` | `0x95a0` | `.My6aKoRuk` | UNKNOWN | `LOW` | 1 | 2 | `bindRemoteStream, .func12` |
| `0x19730` | `0x9730` | `G_al3Wq.C427BWj` | UNKNOWN | `LOW` | 1 | 2 | `bindRemoteStream, .func12` |
| `0x198b0` | `0x98b0` | `CaTXX7o` | UNKNOWN | `LOW` | 1 | 3 | `bindRemoteStream, .UnmarshalCompressed, .func12` |
| `0x19a50` | `0x9a50` | `al3Wq.fDwsvyH` | UNKNOWN | `LOW` | 2 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x19ca0` | `0x9ca0` | `s90ObvaYlEgi` | UNKNOWN | `LOW` | 1 | 4 | `(*gxe_j_u89O0).hjFGwuAXG3, .UnmarshalCompressed, bindRemoteStream` |
| `0x19ef0` | `0x9ef0` | `*ZwDsNXg8D).kqxbE_` | UNKNOWN | `LOW` | 4 | 4 | `er, vhGg, ma.(*MydupPsvCWhi).SetExtension` |
| `0x19fc0` | `0x9fc0` | `vhGg` | UNKNOWN | `LOW` | 1 | 4 | `ig.r2WKg40vITA, .UnmarshalCompressed, ma.(*MydupPsvCWhi).SetExtension` |
| `0x1a0f0` | `0xa0f0` | `*OJTGDxy5).String` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1a100` | `0xa100` | `OJTGDxy5).Available` | UNKNOWN | `LOW` | 0 | 2 | `VoOQ5c.(*OJTGDxy5).qOxwxJuAkW, .func12` |
| `0x1a180` | `0xa180` | `VoOQ5c.(*OJTGDxy5).qOxwxJuAkW` | UNKNOWN | `LOW` | 2 | 1 | `.func12` |
| `0x1a340` | `0xa340` | `5).Grow` | UNKNOWN | `LOW` | 1 | 1 | `.func12` |
| `0x1a4f0` | `0xa4f0` | `OJTGDxy5).ReadFrom` | UNKNOWN | `LOW` | 1 | 6 | `big.(*jQPv4OsZGfd).ReadByte, cZw7cVoOQ5c.(*OJTGDxy5).ReadRune, ocLmfCzb2.jRXdcvNGv.deferwrap1` |
| `0x1a8b0` | `0xa8b0` | `JTGDxy5).WriteByte` | UNKNOWN | `LOW` | 3 | 4 | `.UnmarshalCompressed, big.(*jQPv4OsZGfd).ReadByte, ma.(*MydupPsvCWhi).SetExtension` |
| `0x1aa80` | `0xaa80` | `oOQ5c.(*OJTGDxy5).zGWejRL` | UNKNOWN | `LOW` | 1 | 3 | `).Params, *jQPv4OsZGfd).Width, .func12` |
| `0x1ad40` | `0xad40` | `cZw7cVoOQ5c.(*OJTGDxy5).ReadRune` | UNKNOWN | `LOW` | 4 | 2 | `arBaseMult, .func12` |
| `0x1b100` | `0xb100` | `y5).UnreadByte` | UNKNOWN | `LOW` | 1 | 3 | `*jQPv4OsZGfd).Width, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x1b250` | `0xb250` | `VoOQ5c.AL_XT2` | UNKNOWN | `LOW` | 2 | 3 | `.UnmarshalCompressed, fo, .func12` |
| `0x1b370` | `0xb370` | `FBi1AS` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1b380` | `0xb380` | `VoOQ5c.ATouuaoXmMj` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1b390` | `0xb390` | `e` | UNKNOWN | `LOW` | 10 | 14 | `F).HashFunc, cHKW1j5, y0QaRaM.s7MdT0m]).Len` |
| `0x1b3a0` | `0xb3a0` | `VoOQ5c.DHlB8ChW` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1b3b0` | `0xb3b0` | `VoOQ5c.JLZr6D_Tdv5r` | UNKNOWN | `LOW` | 1 | 2 | `l3Wq.(*Lh9YvVPl_).WriteByte, .func12` |
| `0x1b4b0` | `0xb4b0` | `VoOQ5c.kvqwQm` | UNKNOWN | `LOW` | 4 | 6 | `bindRemoteStream, .UnmarshalCompressed, VoOQ5c.JLZr6D_Tdv5r` |
| `0x1bb90` | `0xbb90` | `.uJMX_tKf` | UNKNOWN | `LOW` | 6 | 3 | `oNLf).Read, Nggdir, .func12` |
| `0x1bc00` | `0xbc00` | `Nggdir` | UNKNOWN | `LOW` | 1 | 4 | `*ZwDsNXg8D).kqxbE_, e:.eq.gxe_j_u89O0.gxe_j_u89O0, JTGDxy5).WriteByte` |
| `0x1bde0` | `0xbde0` | `oNLf).Read` | UNKNOWN | `LOW` | 1 | 4 | `*ZwDsNXg8D).kqxbE_, .UnmarshalCompressed, JTGDxy5).WriteByte` |
| `0x1bfb0` | `0xbfb0` | `5c.(*WoouI2oNLf).UnreadByte` | UNKNOWN | `LOW` | 1 | 6 | `er, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store, ig.r2WKg40vITA` |
| `0x1c0e0` | `0xc0e0` | `.UnreadRune` | UNKNOWN | `LOW` | 0 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, SwY3L.iYPHrB4Qx` |
| `0x1c450` | `0xc450` | `.(*WoouI2oNLf).Reset` | UNKNOWN | `LOW` | 23 | 2 | `bindRemoteStream, .func12` |
| `0x1c680` | `0xc680` | `lg.IndexRabinKarp[go.shape.[]uint8]` | UNKNOWN | `LOW` | 29 | 2 | `bindRemoteStream, .func12` |
| `0x1c8d0` | `0xc8d0` | `bytealg.LastIndexRabinKarp[go.shape.[]uint8]` | UNKNOWN | `LOW` | 28 | 8 | `bindRemoteStream, *pbzEUI0Eh).n3q2Pf, ` |
| `0x1cc70` | `0xcc70` | `8]` | UNKNOWN | `LOW` | 12 | 2 | `String, .func12` |
| `0x1cce0` | `0xcce0` | `nternal/abi.TypeFor[go.shape.interface { UnmarshalText([]uint8) error }]` | UNKNOWN | `LOW` | 24 | 2 | `bindRemoteStream, .func12` |
| `0x1cf10` | `0xcf10` | `[go.shape.string]` | UNKNOWN | `LOW` | 51 | 2 | `bindRemoteStream, .func12` |
| `0x1d150` | `0xd150` | `ce { MarshalJSON() ([]uint8, error) }]` | UNKNOWN | `LOW` | 29 | 8 | `bindRemoteStream, *pbzEUI0Eh).n3q2Pf, ` |
| `0x1d4f0` | `0xd4f0` | `JSON() ([]uint8, error) }]` | UNKNOWN | `LOW` | 16 | 8 | `bindRemoteStream, *pbzEUI0Eh).n3q2Pf, ` |
| `0x1d870` | `0xd870` | `error) }]` | UNKNOWN | `LOW` | 31 | 2 | `String, .func12` |
| `0x1d8e0` | `0xd8e0` | `flect.F5Cl4yr[go.shape.interface { IsZero() bool }]` | UNKNOWN | `LOW` | 90 | 4 | `al3Wq.fDwsvyH, bindRemoteStream, (*gxe_j_u89O0).hjFGwuAXG3` |
| `0x1db40` | `0xdb40` | `ace { IsZero() bool }]` | UNKNOWN | `LOW` | 120 | 4 | `al3Wq.fDwsvyH, bindRemoteStream, (*gxe_j_u89O0).hjFGwuAXG3` |
| `0x1ddc0` | `0xddc0` | `g1gLI7afn.(*OeNad6bZ).Error` | UNKNOWN | `LOW` | 179 | 10 | `bindRemoteStream, *pbzEUI0Eh).n3q2Pf, ` |
| `0x1e280` | `0xe280` | `gLI7afn.(*hoPo9j).jEnbT0HO` | UNKNOWN | `LOW` | 35 | 2 | `String, .func12` |
| `0x1e2f0` | `0xe2f0` | `afn.Jm9yxRyNa.Int64` | UNKNOWN | `LOW` | 48 | 5 | `bindRemoteStream, ead, shStrRev[go.shape.string]` |
| `0x1e590` | `0xe590` | `.(*aUYNELk).qHRDJIx` | UNKNOWN | `LOW` | 64 | 5 | `bindRemoteStream, ead, shStrRev[go.shape.string]` |
| `0x1e840` | `0xe840` | `7afn.(*aUYNELk).iBwI1vT` | UNKNOWN | `LOW` | 78 | 10 | `bindRemoteStream, *pbzEUI0Eh).n3q2Pf, ` |
| `0x1ed30` | `0xed30` | `n.boZMM8IEDER0` | UNKNOWN | `LOW` | 0 | 4 | `.jyMbeRUWPs1.func1, .G2Rzf5wkmWe[go.shape.[]string,go.shape.string], g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x1edc0` | `0xedc0` | `*aUYNELk).vgkIF_Q0` | UNKNOWN | `LOW` | 0 | 2 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x1ee30` | `0xee30` | `(*aUYNELk).mJARruOiY0FJ` | UNKNOWN | `LOW` | 0 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x1ee90` | `0xee90` | `float64]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1ef20` | `0xef20` | `k).nWkVFlQfjgcn` | UNKNOWN | `LOW` | 1 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x1efb0` | `0xefb0` | `UFbRG_TnI` | UNKNOWN | `LOW` | 0 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x1f0a0` | `0xf0a0` | `I7afn.DHv0l91EF4j` | UNKNOWN | `LOW` | 48 | 8 | `IsVur0, (*gxe_j_u89O0).hjFGwuAXG3, 89O0.(*gxe_j_u89O0).gcYExTiArY` |
| `0x1f590` | `0xf590` | `AGvvnXggHNZ).Error` | UNKNOWN | `LOW` | 24 | 4 | `I7afn.DHv0l91EF4j, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, alarMult` |
| `0x1f660` | `0xf660` | `NChRP_).hfa_fEWpPx` | UNKNOWN | `LOW` | 1 | 5 | `(*gxe_j_u89O0).hjFGwuAXG3, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, nmarshal` |
| `0x1f8b0` | `0xf8b0` | `hnNChRP_).eZq0_PR9BX` | UNKNOWN | `LOW` | 2 | 3 | `nc3, 5V.fQMajfD4, .func12` |
| `0x1fab0` | `0xfab0` | `c(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1fac0` | `0xfac0` | `jLYF7KXE[go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1fad0` | `0xfad0` | `nc3` | UNKNOWN | `LOW` | 1 | 2 | `eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store, .func12` |
| `0x1fb30` | `0xfb30` | `gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.func4` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1fb70` | `0xfb70` | `17HF.sSMWWX17HF.JyjLYF7KXE[go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.func4.1` | UNKNOWN | `LOW` | 3 | 2 | `).udJ65d50YY4, .func12` |
| `0x1fc00` | `0xfc00` | `fn.b8iVIvuIKM)].func3.func4.1` | UNKNOWN | `LOW` | 0 | 2 | `).udJ65d50YY4, .func12` |
| `0x1fc70` | `0xfc70` | `[go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.1` | UNKNOWN | `LOW` | 5 | 2 | `).udJ65d50YY4, .func12` |
| `0x1fd20` | `0xfd20` | `gLI7afn.sSMWWX17HF.JyjLYF7KXE[go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.1.1` | UNKNOWN | `LOW` | 1 | 3 | `).udJ65d50YY4, [go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.1, .func12` |
| `0x1fe00` | `0xfe00` | `I7afn.b8iVIvuIKM)].func3.1.1` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x1fe10` | `0xfe10` | `hULJkWJD9ek` | UNKNOWN | `LOW` | 1 | 2 | `).udJ65d50YY4, .func12` |
| `0x1ff60` | `0xff60` | `).udJ65d50YY4` | UNKNOWN | `LOW` | 6 | 0 | `None` |
| `0x201d0` | `0x101d0` | `dJ7jD6k` | UNKNOWN | `LOW` | 1 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x20210` | `0x10210` | `LI7afn.a16n9Q` | UNKNOWN | `LOW` | 0 | 2 | `.UnmarshalCompressed, .func12` |
| `0x203d0` | `0x103d0` | `MHkQqV.QaM0Et` | UNKNOWN | `LOW` | 0 | 2 | `ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x20410` | `0x10410` | `7VE` | UNKNOWN | `LOW` | 0 | 2 | `txbdkX[go.shape.*uint8]).nIKoXvk5, .func12` |
| `0x20450` | `0x10450` | `hape.[]g1gLI7afn.fTKp1rOJ_eC,go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 0 | 2 | `txbdkX[go.shape.*uint8]).nIKoXvk5, .func12` |
| `0x20490` | `0x10490` | `LI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 0 | 2 | `txbdkX[go.shape.*uint8]).nIKoXvk5, .func12` |
| `0x204d0` | `0x104d0` | `pr` | UNKNOWN | `LOW` | 0 | 1 | `txbdkX[go.shape.*uint8]).nIKoXvk5` |
| `0x20500` | `0x10500` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x20540` | `0x10540` | `IOkfwE81E.wQ6e481ZBAw` | UNKNOWN | `LOW` | 2 | 3 | `ey.(*E_o3jWSJ).Debug, txbdkX[go.shape.*uint8]).nIKoXvk5, .func12` |
| `0x20610` | `0x10610` | `1gLI7afn.fUjCPwSf1l.wQ6e481ZBAw` | UNKNOWN | `LOW` | 2 | 3 | `ey.(*E_o3jWSJ).Debug, txbdkX[go.shape.*uint8]).nIKoXvk5, .func12` |
| `0x206e0` | `0x106e0` | `ciiO` | UNKNOWN | `LOW` | 1 | 2 | `IOkfwE81E.wQ6e481ZBAw, .func12` |
| `0x20740` | `0x10740` | `gLI7afn.wE9ja0k` | UNKNOWN | `LOW` | 1 | 2 | `1gLI7afn.fUjCPwSf1l.wQ6e481ZBAw, .func12` |
| `0x207a0` | `0x107a0` | `gLI7afn.cTWUXDm` | UNKNOWN | `LOW` | 2 | 6 | `ig.AZ16TxnuI94E, YLuQc.init, .G2Rzf5wkmWe[go.shape.[]string,go.shape.string]` |
| `0x208c0` | `0x108c0` | `a3).Error` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x208d0` | `0x108d0` | `gLI7afn.(*hoPo9j).udJ65d50YY4` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x208f0` | `0x108f0` | `yY` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x20910` | `0x10910` | `LI7afn.qxnQFa` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x20930` | `0x10930` | `fn.xxx6XtKpia` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x20950` | `0x10950` | `54KD2NXj` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x20980` | `0x10980` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x209a0` | `0x109a0` | `.cylZLSE` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x209c0` | `0x109c0` | `aGd9EZzLcQ` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x209e0` | `0x109e0` | `kUpGjEz` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x20a00` | `0x10a00` | `nqdin4bSd9` | UNKNOWN | `LOW` | 0 | 2 | `(*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x20a60` | `0x10a60` | `Voh` | UNKNOWN | `LOW` | 0 | 2 | `gLI7afn.tG2qGKZ9XTg.func2, .func12` |
| `0x20ac0` | `0x10ac0` | `code.deferwrap1` | UNKNOWN | `LOW` | 0 | 2 | `c3rRAu_qo, .func12` |
| `0x20b20` | `0x10b20` | `c3rRAu_qo` | UNKNOWN | `LOW` | 40 | 5 | `YLuQc.init, .G2Rzf5wkmWe[go.shape.[]string,go.shape.string], CM).gOnlTiS` |
| `0x20be0` | `0x10be0` | `gLI7afn.tG2qGKZ9XTg.func2` | UNKNOWN | `LOW` | 349 | 5 | `YLuQc.init, .G2Rzf5wkmWe[go.shape.[]string,go.shape.string], CM).gOnlTiS` |
| `0x20cb0` | `0x10cb0` | `afn.tG2qGKZ9XTg.func5` | UNKNOWN | `LOW` | 1 | 2 | `b1Wr6XtTC_d).SetDeadline, .func12` |
| `0x20d60` | `0x10d60` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x20dd0` | `0x10dd0` | `unc1` | UNKNOWN | `LOW` | 3 | 25 | `abi.Type,go.shape.interface {}]).Store, 4fQfOR).Err, Y41KqyoVl).Deadline` |
| `0x21020` | `0x11020` | `g` | UNKNOWN | `LOW` | 7 | 31 | `4CM, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x21090` | `0x11090` | `gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x210f0` | `0x110f0` | `n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 7 | 2 | `tgJfPz.GcNk7f, Z.init.JyjLYF7KXE[go.shape.*uint8].func8.1.1` |
| `0x21190` | `0x11190` | `Loj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `shape.*uint8].func7, cHKW1j5` |
| `0x211f0` | `0x111f0` | `GxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 5 | 11 | `tgJfPz.GcNk7f, J20Z.init.JyjLYF7KXE[go.shape.*uint8].func7.1.1, .func12` |
| `0x21270` | `0x11270` | `gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `0Z.init.func2, cHKW1j5` |
| `0x212b0` | `0x112b0` | `Ia` | UNKNOWN | `LOW` | 4 | 3 | `JyjLYF7KXE[go.shape.*uint8].func10.1.1, tgJfPz.GcNk7f, nt; hbXPz4i5V.sSSkltnfCZ eFuxzMSJ.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load` |
| `0x213b0` | `0x113b0` | `LXaQcmz7[go.shape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `JyjLYF7KXE[go.shape.*uint8].func10.1.1, cHKW1j5` |
| `0x21410` | `0x11410` | `EowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 1 | `Compressed` |
| `0x21510` | `0x11510` | `HfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 6 | `u89O0.(*vJAChiupaThd).bA5qVw1acD, bXPz4i5V.xUgqHZic, reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x215f0` | `0x115f0` | `.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 3 | `bXPz4i5V.xUgqHZic, reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x21710` | `0x11710` | `MFSxVA }]` | UNKNOWN | `LOW` | 86 | 6 | `er, Czb2.pFmiMjuOz, .UnmarshalCompressed` |
| `0x218f0` | `0x118f0` | `OOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 46 | 1 | ` bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x21920` | `0x11920` | ` bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 3 | 19 | `bool }]).Store, .func12.1.1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x21e90` | `0x11e90` | `QDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, cHKW1j5` |
| `0x21ee0` | `0x11ee0` | `vLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 7 | `bool }]).Store, OQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], ).Params` |
| `0x22050` | `0x12050` | `R8ZfhK.egSC9prc[go.shape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x22090` | `0x12090` | `7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x22170` | `0x12170` | `OQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 3 | `.Type,go.shape.interface {}]).All.func1, 3vJC5GCZyE).Size, .func12` |
| `0x221f0` | `0x121f0` | `afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 4 | `.Type,go.shape.interface {}]).All.func1, 3vJC5GCZyE).Size, .func12` |
| `0x22270` | `0x12270` | `) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 90 | 11 | `bool }]).Store, hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` |
| `0x22680` | `0x12680` | `.hNllH7[go.shape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x226c0` | `0x126c0` | `owOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 8 | `KAN61n).pvqcm0, .func12, QO` |
| `0x22750` | `0x12750` | `fD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 66 | 1 | `g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x22770` | `0x12770` | `JnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 11 | 1 | `g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x227a0` | `0x127a0` | `g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 4 | 23 | `bool }]).Store, KAN61n).pvqcm0, owOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x22db0` | `0x12db0` | `W2AZ[go.shape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, cHKW1j5` |
| `0x22e00` | `0x12e00` | `uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 8 | `bool }]).Store, afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], big.gi8_Va_kvS` |
| `0x22ff0` | `0x12ff0` | `gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x23030` | `0x13030` | `1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x230a0` | `0x130a0` | `LYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 35 | 2 | ` bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x230f0` | `0x130f0` | `8ZfhK.sLpwrgD6d[go.shape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 59 | 2 | `g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x23140` | `0x13140` | `; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 6 | 6 | `KAN61n).pvqcm0, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x231f0` | `0x131f0` | `fn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 4 | `er, i5V.(*mheejkbo8).yfw6D0U3os, Eac` |
| `0x23210` | `0x13210` | `; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 5 | `20Z.tcu6kPP7, , .func12.1.1` |
| `0x23360` | `0x13360` | `8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 9 | `20Z.tcu6kPP7, 3vJC5GCZyE).Size, nmarshal` |
| `0x234a0` | `0x134a0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x23660` | `0x13660` | `; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 6 | 6 | `KAN61n).pvqcm0, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x23770` | `0x13770` | `fn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 4 | `er, i5V.(*mheejkbo8).yfw6D0U3os, Eac` |
| `0x237e0` | `0x137e0` | `afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 4 | `.Type,go.shape.interface {}]).All.func1, 3vJC5GCZyE).Size, .func12` |
| `0x23890` | `0x13890` | `8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 9 | `20Z.tcu6kPP7, 3vJC5GCZyE).Size, nmarshal` |
| `0x23cc0` | `0x13cc0` | `fn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 3 | `tgJfPz.GcNk7f, tQ0xKHZgC5j.init.func1, jkbo8).wNv3ibD.(*mheejkbo8).cQjpP4oK.func1` |
| `0x23d80` | `0x13d80` | `owOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 8 | `KAN61n).pvqcm0, .func12, QO` |
| `0x23ea0` | `0x13ea0` | `LI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 4 | `).Params, reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], tQ0xKHZgC5j.init.func1` |
| `0x23fd0` | `0x13fd0` | `u func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 3 | `eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store, YT1bAJ.DKyyIy]).UnmarshalCompressed, cHKW1j5` |
| `0x24020` | `0x14020` | `afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 5 | 4 | `(*gxe_j_u89O0).hjFGwuAXG3, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, eam` |
| `0x24140` | `0x14140` | `.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 5 | `WPs1, 3vJC5GCZyE).Size, Compressed` |
| `0x242e0` | `0x142e0` | `y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x242f0` | `0x142f0` | `lect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 7 | `YLuQc.init, _dZ59.V9eEq1UH8aq0, (*gxe_j_u89O0).hjFGwuAXG3` |
| `0x24580` | `0x14580` | `unc(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x24590` | `0x14590` | `uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 2 | `.G2Rzf5wkmWe[go.shape.[]string,go.shape.string], .func12` |
| `0x245f0` | `0x145f0` | `EowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 1 | `Compressed` |
| `0x24600` | `0x14600` | `HfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 6 | `u89O0.(*vJAChiupaThd).bA5qVw1acD, bXPz4i5V.xUgqHZic, reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x24660` | `0x14660` | `kJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x24670` | `0x14670` | ` g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x24680` | `0x14680` | `Gg0xE5[go.shape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x24690` | `0x14690` | `fn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x246a0` | `0x146a0` | `G0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 5 | `jMcnw, _dZ59.iujecbY5, 3vJC5GCZyE).Size` |
| `0x24cc0` | `0x14cc0` | `OGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 11 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, XPz4i5V.ISwY3L.IsPrivate, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x25040` | `0x15040` | ` g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 12 | `YLuQc.init, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x255e0` | `0x155e0` | `uct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 4 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x256c0` | `0x156c0` | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 818 | 13 | `CM, ingIndex.func1, OYkL_dZ59.w4yXDH7e` |
| `0x25970` | `0x15970` | `[]int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 3 | 6 | `WPs1, func1, er` |
| `0x25ab0` | `0x15ab0` | `GxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 5 | 11 | `tgJfPz.GcNk7f, J20Z.init.JyjLYF7KXE[go.shape.*uint8].func7.1.1, .func12` |
| `0x25c70` | `0x15c70` | `I7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 2 | `hape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x25d10` | `0x15d10` | `hape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 2 | 2 | `hape.struct { g1gLI7afn.twnIiV string; g1gLI7afn.htEowOOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x25df0` | `0x15df0` | `string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x26050` | `0x16050` | `1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x260a0` | `0x160a0` | `l; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x260f0` | `0x160f0` | `fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x261f0` | `0x161f0` | `.shape.string]` | UNKNOWN | `LOW` | 6 | 5 | `er, .UnmarshalCompressed, WPs1` |
| `0x263c0` | `0x163c0` | `C; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 1 | 2 | `WPs1, .func12` |
| `0x264c0` | `0x164c0` | `uct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x26530` | `0x16530` | `c[go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 2 | 5 | `Czb2.pFmiMjuOz, R8ZfhK.hNllH7[go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }], EyvNEwJVta).ti68CiX` |
| `0x266b0` | `0x166b0` | `R8ZfhK.hNllH7[go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x26720` | `0x16720` | ` string }]` | UNKNOWN | `LOW` | 1 | 10 | `3jtsJa5G, sa7.(*UdymEtYSFZ).Sum, nit.JyjLYF7KXE[go.shape.bool].func4.1.1` |
| `0x26ab0` | `0x16ab0` | `1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 86 | 5 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, c[go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` |
| `0x26ba0` | `0x16ba0` | `n.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 83 | 4 | `er, ma.(*MydupPsvCWhi).SetExtension, giPo3aUOjR]).Unmarshal` |
| `0x26c40` | `0x16c40` | `t { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 54 | 4 | `er, ma.(*MydupPsvCWhi).SetExtension, giPo3aUOjR]).Unmarshal` |
| `0x26cf0` | `0x16cf0` | `.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 30 | 4 | `er, ma.(*MydupPsvCWhi).SetExtension, ).Params` |
| `0x26d70` | `0x16d70` | `hK.csaeyMUBaFR[go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 219 | 3 | `Czb2.pFmiMjuOz, big.gi8_Va_kvS, .func12` |
| `0x26de0` | `0x16de0` | `_ string }]` | UNKNOWN | `LOW` | 52 | 3 | `Czb2.pFmiMjuOz, 3vJC5GCZyE).Size, .func12` |
| `0x26e50` | `0x16e50` | `1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 86 | 5 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, c[go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` |
| `0x26ed0` | `0x16ed0` | `flect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 138 | 2 | `Czb2.pFmiMjuOz, .func12` |
| `0x26f50` | `0x16f50` | `I7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 226 | 7 | `wOFdCgZ, truct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }], EyvNEwJVta).ti68CiX` |
| `0x27120` | `0x17120` | `truct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }]` | UNKNOWN | `LOW` | 1 | 4 | `Czb2.pFmiMjuOz, nmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO` |
| `0x27310` | `0x17310` | `Wex[go.shape.[]uint8]` | UNKNOWN | `LOW` | 13 | 5 | `wOFdCgZ, fn.(*Jm9yxRyNa).Float64, EyvNEwJVta).ti68CiX` |
| `0x27510` | `0x17510` | `fn.(*Jm9yxRyNa).Float64` | UNKNOWN | `LOW` | 1 | 4 | `Czb2.pFmiMjuOz, nmarshal, Lv.(*BSsluADyuaT).xmHeAsfrPO` |
| `0x27720` | `0x17720` | `7afn.(*hnNChRP_).Available` | UNKNOWN | `LOW` | 0 | 2 | `eam, .func12` |
| `0x27760` | `0x17760` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x27810` | `0x17810` | `afn.(*hnNChRP_).Len` | UNKNOWN | `LOW` | 1 | 4 | `rY_VpYFfo.xmGgHO, .(*zop57OMF).Len, eam` |
| `0x27890` | `0x17890` | `NChRP_).ReadByte` | UNKNOWN | `LOW` | 16 | 7 | `nit.func6, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x27950` | `0x17950` | `n.(*hnNChRP_).ReadRune` | UNKNOWN | `LOW` | 5 | 4 | `5V.init.func2, Compressed, eam` |
| `0x27a30` | `0x17a30` | `I7afn.(*hnNChRP_).String` | UNKNOWN | `LOW` | 2 | 3 | `.func12.1.1, 5V.init.func2, Compressed` |
| `0x27bc0` | `0x17bc0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x27c30` | `0x17c30` | `eByte` | UNKNOWN | `LOW` | 2 | 5 | `r, I7afn.(*hnNChRP_).String, a8FS97_S8.(*yMbC6m3zgkq).Is` |
| `0x27cb0` | `0x17cb0` | `hRP_).WriteTo` | UNKNOWN | `LOW` | 1 | 1 | `5V.init.func2` |
| `0x27d50` | `0x17d50` | `1ZBAw-fm` | UNKNOWN | `LOW` | 1 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x27e20` | `0x17e20` | `81ZBAw-fm` | UNKNOWN | `LOW` | 3 | 2 | `hhHS85O.wQ6e481ZBAw-fm, .func12` |
| `0x27e60` | `0x17e60` | `hhHS85O.wQ6e481ZBAw-fm` | UNKNOWN | `LOW` | 186 | 7 | `20Z.tcu6kPP7, o.shape.*uint8]).IsOnCurve, .func12.1.1` |
| `0x282f0` | `0x182f0` | `ype:.eq.struct { g1gLI7afn.bfKPgnM1e_j interface {}; g1gLI7afn.n2x2VU6Gus int }` | UNKNOWN | `LOW` | 3 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x28330` | `0x18330` | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` | UNKNOWN | `LOW` | 194 | 5 | `YOV__Rt.init, aF9g0geqI.Error, eam` |
| `0x28580` | `0x18580` | `YOV__Rt.init` | UNKNOWN | `LOW` | 1 | 3 | `nit.func6, l; AcDK_Fy.kCEV3Lu09HcR string }]], .func12` |
| `0x288b0` | `0x188b0` | `Prefix` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x28920` | `0x18920` | `gs` | UNKNOWN | `LOW` | 1 | 10 | `_Fy.bOJFoVB]]).Load, .shape.interface {}]).CompareAndDelete, abi.Type,interface {}]]).Store` |
| `0x28c70` | `0x18c70` | `tput.deferwrap1` | UNKNOWN | `LOW` | 1 | 20 | `omic.ILxa0fgA7[string], abi.Type,interface {}]).Delete, face {}]).CompareAndSwap` |
| `0x29250` | `0x19250` | `aYOV__Rt.(*C9tFSBPDcz8s).Output` | UNKNOWN | `LOW` | 1 | 3 | `abi.Type,interface {}]).LoadOrStore, GxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12` |
| `0x29350` | `0x19350` | `FSBPDcz8s).rCrKT0p2Li` | UNKNOWN | `LOW` | 1 | 5 | `y.(*J9R_6Iy_9rFh).As16, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x29430` | `0x19430` | `.string]).Load` | UNKNOWN | `LOW` | 4 | 10 | `atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load, abi.Type,go.shape.interface {}]).dJaxqgYz, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x29630` | `0x19630` | `cz8s).rCrKT0p2Li.deferwrap2` | UNKNOWN | `LOW` | 1 | 6 | `.string]).Load, AcDK_Fy.J9R_6Iy_9rFh.IsPrivate, nc1` |
| `0x29930` | `0x19930` | `init.0` | UNKNOWN | `LOW` | 1 | 9 | `.string]).Load, ZWj4kZX).Bits, AcDK_Fy.J9R_6Iy_9rFh.IsPrivate` |
| `0x29c50` | `0x19c50` | `t.(*C9tFSBPDcz8s).Printf` | UNKNOWN | `LOW` | 1 | 10 | `.string]).Load, ZWj4kZX).Bits, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` |
| `0x29fa0` | `0x19fa0` | `8s).Println` | UNKNOWN | `LOW` | 1 | 10 | `.string]).Load, ZWj4kZX).Bits, .UnmarshalCompressed` |
| `0x2a2f0` | `0x1a2f0` | `aYOV__Rt.(*C9tFSBPDcz8s).Fatal.func1` | UNKNOWN | `LOW` | 1 | 8 | `abi.Type,go.shape.interface {}]).LoadAndDelete, ).Params, AcDK_Fy.J9R_6Iy_9rFh.IsPrivate` |
| `0x2a560` | `0x1a560` | `SBPDcz8s).Fatalf.func1` | UNKNOWN | `LOW` | 1 | 2 | `hape.string]).CompareAndSwap, .func12` |
| `0x2a640` | `0x1a640` | `alln.func1` | UNKNOWN | `LOW` | 1 | 4 | `QmBRaybD).MarshalSize, ).ReplaceAllFunc.func1, { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` |
| `0x2a7c0` | `0x1a7c0` | `V__Rt.(*C9tFSBPDcz8s).Panicf` | UNKNOWN | `LOW` | 1 | 2 | `atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }], .func12` |
| `0x2a830` | `0x1a830` | `PDcz8s).Panicln` | UNKNOWN | `LOW` | 1 | 3 | `ZWj4kZX).Bits, tQ0xKHZgC5j.init.func1, .func12` |
| `0x2a8d0` | `0x1a8d0` | `er` | UNKNOWN | `LOW` | 2116 | 2 | `Czb2.pFmiMjuOz, .func12` |
| `0x2a920` | `0x1a920` | `nc1` | UNKNOWN | `LOW` | 17 | 22 | `t.0.func1.1, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }, eam` |
| `0x2aa00` | `0x1aa00` | `t.0.func1.1` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x2ab00` | `0x1ab00` | `hape.string]).CompareAndSwap` | UNKNOWN | `LOW` | 17 | 1 | `tgJfPz.GcNk7f` |
| `0x2ab50` | `0x1ab50` | `A7[go.shape.string]).Swap` | UNKNOWN | `LOW` | 0 | 2 | `, cHKW1j5` |
| `0x2aba0` | `0x1aba0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x2aea0` | `0x1aea0` | `omic.ILxa0fgA7[string]` | UNKNOWN | `LOW` | 1 | 3 | `abi.Type,interface {}]).CompareAndDelete, abi.Type,interface {}]).LoadAndDelete, .func12` |
| `0x2afe0` | `0x1afe0` | `TNQIbbeMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).Clear` | UNKNOWN | `LOW` | 98 | 3 | `VoOQ5c.AL_XT2, VoOQ5c.kvqwQm, .func12` |
| `0x2b050` | `0x1b050` | `bbeMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).init` | UNKNOWN | `LOW` | 98 | 2 | `VoOQ5c.kvqwQm, .func12` |
| `0x2b090` | `0x1b090` | `[go.shape.struct { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 52 | 1 | `abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` |
| `0x2b0c0` | `0x1b0c0` | `pe,go.shape.interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 279 | 1 | `abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` |
| `0x2b0f0` | `0x1b0f0` | `xZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 1 | 5 | `abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load, 3vJC5GCZyE).Size, .UnmarshalCompressed` |
| `0x2b200` | `0x1b200` | `e.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 6 | 2 | `abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load, ZWj4kZX).Bits` |
| `0x2b260` | `0x1b260` | `fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 2 | 2 | `abi.Type,go.shape.interface {}], abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` |
| `0x2b2f0` | `0x1b2f0` | `pe.*internal/abi.Type,go.shape.interface {}]` | UNKNOWN | `LOW` | 2 | 2 | `g4539QfP4.I0k13OdARF, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` |
| `0x2b3e0` | `0x1b3e0` | `l/abi.Type,go.shape.interface {}]).hgL7yVryk7PQ` | UNKNOWN | `LOW` | 2 | 1 | `g4539QfP4.I0k13OdARF` |
| `0x2b460` | `0x1b460` | `l/abi.Type,go.shape.interface {}]).zkOaisuYQdz` | UNKNOWN | `LOW` | 3 | 1 | `g4539QfP4.I0k13OdARF` |
| `0x2b5c0` | `0x1b5c0` | ` ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[go.shape.*internal/abi.Type,go.shape.interface {}]]; ftFU4ooB64P.iHUS8Mhyvow go.shape.*internal/abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 2 | 2 | `g4539QfP4.I0k13OdARF, pqx).ListenPacket` |
| `0x2b7f0` | `0x1b7f0` | `ace {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[go.shape.*internal/abi.Type,go.shape.interface {}]]; ftFU4ooB64P.iHUS8Mhyvow go.shape.*internal/abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` | UNKNOWN | `LOW` | 9 | 6 | `abi.Type,go.shape.interface {}]).hgL7yVryk7PQ, fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store, abi.Type,go.shape.interface {}]).zkOaisuYQdz` |
| `0x2bb10` | `0x1bb10` | `al/abi.Type,go.shape.interface {}]]; ftFU4ooB64P.iHUS8Mhyvow go.shape.*internal/abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` | UNKNOWN | `LOW` | 2 | 5 | `abi.Type,go.shape.interface {}]).hgL7yVryk7PQ, fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store, abi.Type,go.shape.interface {}]).zkOaisuYQdz` |
| `0x2bc80` | `0x1bc80` | `; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load` | UNKNOWN | `LOW` | 2 | 3 | `abi.Type,go.shape.interface {}]).Range, ZWj4kZX).Bits, .func12` |
| `0x2bd20` | `0x1bd20` | `.*internal/abi.Type,go.shape.interface {}]).Range` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x2bd70` | `0x1bd70` | `t { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x2be30` | `0x1be30` | `erface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 1 | 1 | `g4539QfP4.I0k13OdARF` |
| `0x2bfd0` | `0x1bfd0` | `ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x2bff0` | `0x1bff0` | `.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 2 | 3 | `atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load, eam, .func12` |
| `0x2c160` | `0x1c160` | `truct { ftFU4ooB64P.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 1 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x2c330` | `0x1c330` | `al/abi.Type,go.shape.interface {}]).All` | UNKNOWN | `LOW` | 1 | 1 | `).wwih4t` |
| `0x2c4b0` | `0x1c4b0` | `.Type,go.shape.interface {}]).All.func1` | UNKNOWN | `LOW` | 2 | 9 | `g4539QfP4.I0k13OdARF, ).wwih4t, YLuQc.init` |
| `0x2c690` | `0x1c690` | `.Type,go.shape.interface {}]).i_1IGq` | UNKNOWN | `LOW` | 1 | 6 | `hape.string]).CompareAndSwap, o.shape.interface {}]).w76WXyqw, eam` |
| `0x2c770` | `0x1c770` | `o.shape.interface {}]).w76WXyqw` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 2 | `pqx).ListenPacket, .func12` |
| `0x2cb80` | `0x1cb80` | `.shape.interface {}]).CompareAndDelete` | UNKNOWN | `LOW` | 2 | 3 | `tgJfPz.GcNk7f, t.0.func1.1, .func12` |
| `0x2ccd0` | `0x1ccd0` | `Qdz[go.shape.*internal/abi.Type,go.shape.interface {}]).dJaxqgYz` | UNKNOWN | `LOW` | 1 | 8 | `abi.Type,go.shape.interface {}], Y41KqyoVl).Deadline, .jvqY41KqyoVl.Err` |
| `0x2cf70` | `0x1cf70` | `ja[go.shape.*internal/abi.Type,go.shape.interface {}]).LoadAndDelete` | UNKNOWN | `LOW` | 1 | 10 | `kimj_, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Load, Y41KqyoVl).Deadline` |
| `0x2d180` | `0x1d180` | `beMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).CompareAndSwap` | UNKNOWN | `LOW` | 2 | 6 | `Y41KqyoVl).Deadline, .jvqY41KqyoVl.Err, abi.Type,go.shape.interface {}]` |
| `0x2d3e0` | `0x1d3e0` | `TNQIbbeMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).CompareAndSwap.deferwrap1` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 4 | 9 | `abi.Type,go.shape.interface {}]).CompareAndSwap, MnoAPhGe1).Start.func1, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x2d4d0` | `0x1d4d0` | `1` | UNKNOWN | `LOW` | 25 | 39 | `kimj_, QmBRaybD).MarshalSize, *JZdvaRJ).MarshalSize` |
| `0x2da10` | `0x1da10` | `U4ooB64P.eiP1MjiFEXkM[go.shape.*internal/abi.Type,go.shape.interface {}]` | UNKNOWN | `LOW` | 2 | 4 | `ytR.wizKus.Value, 9.xIe1xMNMiPk[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }], eam` |
| `0x2daf0` | `0x1daf0` | `NQIbbeMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).Swap.deferwrap1` | UNKNOWN | `LOW` | 1 | 4 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Load, ; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load, nmarshal` |
| `0x2db80` | `0x1db80` | `4P.(*TNQIbbeMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).iYWWH_bL` | UNKNOWN | `LOW` | 1 | 1 | `.func12` |
| `0x2dc60` | `0x1dc60` | `{}]).iYWWH_bL` | UNKNOWN | `LOW` | 1 | 2 | `eam, .func12` |
| `0x2dcf0` | `0x1dcf0` | `8apb = ftFU4ooB64P.ihCa8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[go.shape.*internal/abi.Type,go.shape.interface {}]]; ftFU4ooB64P.iHUS8Mhyvow go.shape.*internal/abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store` | UNKNOWN | `LOW` | 1 | 9 | `arBaseMult, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x2def0` | `0x1def0` | `64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[go.shape.*internal/abi.Type,go.shape.interface {}]]; ftFU4ooB64P.iHUS8Mhyvow go.shape.*internal/abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store` | UNKNOWN | `LOW` | 2 | 7 | `abi.Type,go.shape.interface {}]).iYWWH_bL, abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Store, 1ay1Swi` |
| `0x2dfb0` | `0x1dfb0` | `ape.interface {}]]; ftFU4ooB64P.iHUS8Mhyvow go.shape.*internal/abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store` | UNKNOWN | `LOW` | 1 | 16 | `abi.Type,go.shape.interface {}]).x7kCPkLMq, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x2e5b0` | `0x1e5b0` | ` ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store` | UNKNOWN | `LOW` | 0 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x2e810` | `0x1e810` | `.*internal/abi.Type,go.shape.interface {}]).LoadOrStore` | UNKNOWN | `LOW` | 0 | 3 | `ool; AcDK_Fy.kCEV3Lu09HcR string }].Value, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }], cHKW1j5` |
| `0x2ed10` | `0x1ed10` | `ja[go.shape.*internal/abi.Type,go.shape.interface {}]).Load` | UNKNOWN | `LOW` | 1 | 5 | `.UnmarshalCompressed, , nmarshal` |
| `0x2ef60` | `0x1ef60` | `.shape.*internal/abi.Type,go.shape.interface {}]).eZbw9kK` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, TMuEM).Add` |
| `0x2f150` | `0x1f150` | `hape.*internal/abi.Type,go.shape.interface {}]).eZbw9kK.deferwrap1` | UNKNOWN | `LOW` | 1 | 6 | `ne, , eam` |
| `0x2f4b0` | `0x1f4b0` | `[go.shape.*internal/abi.Type,go.shape.interface {}]).t6WqWh` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, Pz4i5V.(*Gf_aZ0Zk).File` |
| `0x2f6a0` | `0x1f6a0` | `pe.*internal/abi.Type,go.shape.interface {}]).aCWu2P_8aZb` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x2f700` | `0x1f700` | `.*internal/abi.Type,go.shape.interface {}]).y1UJwuTdmMqa` | UNKNOWN | `LOW` | 6 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, EZsdym0` |
| `0x2f840` | `0x1f840` | `*internal/abi.Type,go.shape.interface {}]).jTfYNzI` | UNKNOWN | `LOW` | 0 | 5 | `, abi.Type,go.shape.interface {}]).eZbw9kK, ).Params` |
| `0x2faa0` | `0x1faa0` | `Mcja[*internal/abi.Type,interface {}]).Clear` | UNKNOWN | `LOW` | 8 | 2 | `4fQfOR).Err, abi.Type,interface {}]).Delete` |
| `0x2fb30` | `0x1fb30` | `e,interface {}]).Range` | UNKNOWN | `LOW` | 3 | 2 | `4fQfOR).Err, GxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x2fbc0` | `0x1fbc0` | `tFU4ooB64P.(*TNQIbbeMcja[*internal/abi.Type,interface {}]).CompareAndDelete` | UNKNOWN | `LOW` | 4 | 3 | `4fQfOR).Err, Type,interface {}]).Load, .func12` |
| `0x2fc40` | `0x1fc40` | `(*TNQIbbeMcja[*internal/abi.Type,interface {}]).Delete` | UNKNOWN | `LOW` | 2 | 6 | `n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x2fd10` | `0x1fd10` | `e.*internal/abi.Type,go.shape.interface {}]).Delete` | UNKNOWN | `LOW` | 1 | 5 | `rHJ20Z.init.func5.1, n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], uDeMp8Izpi_.SetKeepAlive` |
| `0x2fec0` | `0x1fec0` | `abi.Type,interface {}]).LoadAndDelete` | UNKNOWN | `LOW` | 4 | 4 | `n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], uDeMp8Izpi_.SetKeepAlive, eam` |
| `0x2ff80` | `0x1ff80` | `face {}]).CompareAndSwap` | UNKNOWN | `LOW` | 4 | 2 | `rHJ20Z.init.func5.1, .func12` |
| `0x30000` | `0x20000` | `p` | UNKNOWN | `LOW` | 10 | 8 | `rHJ20Z.init.func5.1, eam, .func12` |
| `0x30080` | `0x20080` | `eMcja[go.shape.*internal/abi.Type,go.shape.interface {}]).Store` | UNKNOWN | `LOW` | 3 | 3 | `4CM, rHJ20Z.init.func5.1, .func12` |
| `0x30100` | `0x20100` | `a[*internal/abi.Type,interface {}]).LoadOrStore` | UNKNOWN | `LOW` | 4 | 3 | `n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], uDeMp8Izpi_.SetKeepAlive, .func12` |
| `0x30190` | `0x20190` | `Type,interface {}]).Load` | UNKNOWN | `LOW` | 1 | 12 | `n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], uDeMp8Izpi_.SetKeepAlive, p` |
| `0x302d0` | `0x202d0` | `ype,interface {}]]).CompareAndSwap` | UNKNOWN | `LOW` | 1 | 12 | `WPs1, .UnmarshalCompressed, jMcnw` |
| `0x31ab0` | `0x21ab0` | `ct { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x31ac0` | `0x21ac0` | `ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 1 | 7 | `hhHS85O.wQ6e481ZBAw-fm, hape.string]).CompareAndSwap, T1bAJ.JgiPo3aUOjR]).IsOnCurve` |
| `0x31d70` | `0x21d70` | `j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 1 | 2 | `EZsdym0, .func12` |
| `0x31e00` | `0x21e00` | `rface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x31e90` | `0x21e90` | `l/abi.Type,interface {}]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 1 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x31f10` | `0x21f10` | `U4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]]).Swap` | UNKNOWN | `LOW` | 0 | 14 | `hhHS85O.wQ6e481ZBAw-fm, .UnmarshalCompressed, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x32420` | `0x22420` | `.(*ILxa0fgA7[go.shape.struct { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Swap` | UNKNOWN | `LOW` | 3 | 0 | `None` |
| `0x324d0` | `0x224d0` | `.Type,interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Swap` | UNKNOWN | `LOW` | 9 | 11 | `rY_VpYFfo.xmGgHO, wOFdCgZ, tgJfPz.GcNk7f` |
| `0x32ab0` | `0x22ab0` | `.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Swap` | UNKNOWN | `LOW` | 0 | 4 | `atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Store, atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Load, eam` |
| `0x32b60` | `0x22b60` | `kOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Swap` | UNKNOWN | `LOW` | 0 | 3 | `VAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Store, [AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Load, cHKW1j5` |
| `0x32bd0` | `0x22bd0` | `ync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Swap` | UNKNOWN | `LOW` | 1 | 4 | `.JgiPo3aUOjR]).ScalarBaseMult, .UnmarshalCompressed, eam` |
| `0x32ca0` | `0x22ca0` | `c/atomic.(*ILxa0fgA7[ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]]).Store` | UNKNOWN | `LOW` | 12 | 7 | `ZWj4kZX).Bits, hape.string]).CompareAndSwap, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x32df0` | `0x22df0` | `nc/atomic.(*ILxa0fgA7[go.shape.struct { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Store` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x32e10` | `0x22e10` | `ernal/abi.Type,interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Store` | UNKNOWN | `LOW` | 1 | 4 | `3lU.AppendTo, t, Fy.lSiQS70uuAy` |
| `0x32eb0` | `0x22eb0` | `HiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Store` | UNKNOWN | `LOW` | 1 | 6 | `MFSxVA }], er, ).Params` |
| `0x32fa0` | `0x22fa0` | `P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Store` | UNKNOWN | `LOW` | 0 | 2 | `atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load, cHKW1j5` |
| `0x33000` | `0x23000` | `_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Store` | UNKNOWN | `LOW` | 0 | 2 | `.deferwrap1, cHKW1j5` |
| `0x33060` | `0x23060` | `.Store` | UNKNOWN | `LOW` | 0 | 2 | `.func12.1.1, .func12` |
| `0x33110` | `0x23110` | `e,interface {}]]).Load` | UNKNOWN | `LOW` | 4 | 8 | `abi.Type,interface {}]] }]).Load, abi.Type,interface {}]] }]).Load, tQ0xKHZgC5j.init.func1` |
| `0x332a0` | `0x232a0` | `B64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Load` | UNKNOWN | `LOW` | 1 | 4 | `TMuEM).Add, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x33390` | `0x23390` | `niWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Load` | UNKNOWN | `LOW` | 7 | 2 | `RaEDZ0J3lU.Port, .func12` |
| `0x334e0` | `0x234e0` | `4P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Load` | UNKNOWN | `LOW` | 7 | 25 | `).Params, abi.Type,interface {}]] }]).Load, L bool; AcDK_Fy.kCEV3Lu09HcR string }]` |
| `0x33bd0` | `0x23bd0` | `v_We [16]sync/atomic.ILxa0fgA7[ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]] }]).Load` | UNKNOWN | `LOW` | 0 | 3 | `i5V.(*bAujxOKO_).Is, e,interface {}]]).Load, cHKW1j5` |
| `0x33c70` | `0x23c70` | `i.Type,interface {}]] }]).Load` | UNKNOWN | `LOW` | 0 | 2 | `*bAujxOKO_).Error, cHKW1j5` |
| `0x33cc0` | `0x23cc0` | `4P.ihCa8apb[*internal/abi.Type,interface {}]]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 2 | `.UnmarshalCompressed, cHKW1j5` |
| `0x33d20` | `0x23d20` | `dSwap` | UNKNOWN | `LOW` | 2 | 13 | `uDeMp8Izpi_.CloseWrite, tgJfPz.GcNk7f, XPz4i5V.(*uDeMp8Izpi_).File` |
| `0x34060` | `0x24060` | `terface {}]]).Swap` | UNKNOWN | `LOW` | 0 | 3 | `.func12.1.1, i5V.(*bAujxOKO_).Is, cHKW1j5` |
| `0x34120` | `0x24120` | `l/abi.Type,interface {}]]).Store` | UNKNOWN | `LOW` | 0 | 2 | `B4Uc, cHKW1j5` |
| `0x341d0` | `0x241d0` | `a8apb[*internal/abi.Type,interface {}]]).Load` | UNKNOWN | `LOW` | 0 | 2 | `*bAujxOKO_).Error, cHKW1j5` |
| `0x34220` | `0x24220` | `0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 4 | `cpajYcj).Close, 4i5V.gARftz0v7, CtiT` |
| `0x34290` | `0x24290` | `pareAndSwap` | UNKNOWN | `LOW` | 1 | 32 | `.func12.1.1, ).Params, cpajYcj).Close` |
| `0x35200` | `0x25200` | `.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 4 | `cpajYcj).Close, 4i5V.gARftz0v7, CtiT` |
| `0x35270` | `0x25270` | ` sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 2 | `i5V.(*bAujxOKO_).Is, cHKW1j5` |
| `0x352c0` | `0x252c0` | `terface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 4 | `abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store, abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store, abi.Type,interface {}]]).Store` |
| `0x35390` | `0x25390` | `kdOCPY interface {} }]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 2 | ` ftFU4ooB64P.xukdOCPY interface {} }]).Swap, cHKW1j5` |
| `0x353d0` | `0x253d0` | `tFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]).Swap` | UNKNOWN | `LOW` | 1 | 6 | `MFSxVA }], fD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], er` |
| `0x35560` | `0x25560` | `*ILxa0fgA7[go.shape.struct { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Swap` | UNKNOWN | `LOW` | 0 | 2 | `abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Swap, cHKW1j5` |
| `0x355c0` | `0x255c0` | `ype,interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Swap` | UNKNOWN | `LOW` | 1 | 17 | `).Params, er, OOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x35a80` | `0x25a80` | `nal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Swap` | UNKNOWN | `LOW` | 0 | 8 | `cpajYcj).Close, 1ay1Swi, XPz4i5V.hguC61sqr.Err` |
| `0x35c00` | `0x25c00` | ` ftFU4ooB64P.xukdOCPY interface {} }]).Swap` | UNKNOWN | `LOW` | 1 | 17 | `abi.Type,interface {}]], ).Params, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` |
| `0x35ff0` | `0x25ff0` | `*internal/abi.Type,interface {}]]).Store` | UNKNOWN | `LOW` | 1 | 11 | `hhHS85O.wQ6e481ZBAw-fm, .UnmarshalCompressed, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x362b0` | `0x262b0` | `ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Store` | UNKNOWN | `LOW` | 1 | 6 | `V.fEj8wTHqB, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x363c0` | `0x263c0` | ` ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Store` | UNKNOWN | `LOW` | 1 | 5 | `EyvNEwJVta).ti68CiX, hhHS85O.wQ6e481ZBAw-fm, ).Params` |
| `0x36580` | `0x26580` | `l/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Store` | UNKNOWN | `LOW` | 2 | 2 | `nmarshal, .func12` |
| `0x36800` | `0x26800` | `CPY interface {} }]).Store` | UNKNOWN | `LOW` | 2 | 3 | `abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load, eam, .func12` |
| `0x368f0` | `0x268f0` | `e,interface {}]]).Load` | UNKNOWN | `LOW` | 4 | 8 | `abi.Type,interface {}]] }]).Load, abi.Type,interface {}]] }]).Load, tQ0xKHZgC5j.init.func1` |
| `0x369d0` | `0x269d0` | `ftFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]; ftFU4ooB64P.t38u7pkY sync/atomic.ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load` | UNKNOWN | `LOW` | 2 | 3 | `abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load, eam, .func12` |
| `0x36ad0` | `0x26ad0` | `ILxa0fgA7[ftFU4ooB64P.gmfw5hm[*internal/abi.Type,interface {}]]; ftFU4ooB64P.iHUS8Mhyvow *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load` | UNKNOWN | `LOW` | 3 | 4 | `abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load, abi.Type,interface {}], eam` |
| `0x36d50` | `0x26d50` | ` *internal/abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x36e00` | `0x26e00` | `a0fgA7[ftFU4ooB64P.zkOaisuYQdz[*internal/abi.Type,interface {}]]` | UNKNOWN | `LOW` | 1 | 3 | `abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load, eam, .func12` |
| `0x36f60` | `0x26f60` | `OaisuYQdz[*internal/abi.Type,interface {}]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x37010` | `0x27010` | `pe,interface {}]` | UNKNOWN | `LOW` | 4 | 7 | `eam, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x37270` | `0x27270` | `nterface {}]]` | UNKNOWN | `LOW` | 2 | 2 | `.UnmarshalCompressed, .func12` |
| `0x37470` | `0x27470` | `nternal/abi.Type,interface {}]]` | UNKNOWN | `LOW` | 1 | 7 | `i5V.(*YMbT3l).c_f7b5n.gowrap2, XPz4i5V.(*priWRezQsI).lEvYyBEt, .ISwY3L.Mask` |
| `0x37530` | `0x27530` | `tFU4ooB64P.ihCa8apb[*internal/abi.Type,interface {}]]` | UNKNOWN | `LOW` | 0 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, t2q.Size` |
| `0x37650` | `0x27650` | `ape.*internal/abi.Type,go.shape.interface {}]` | UNKNOWN | `LOW` | 2 | 12 | `atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }], tgJfPz.GcNk7f, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` |
| `0x37ac0` | `0x27ac0` | `.gmfw5hm[go.shape.*internal/abi.Type,go.shape.interface {}]]` | UNKNOWN | `LOW` | 0 | 7 | `cpajYcj).Close, V.e39Yl0, .ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` |
| `0x37bf0` | `0x27bf0` | `FU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]` | UNKNOWN | `LOW` | 1 | 2 | `ool; AcDK_Fy.kCEV3Lu09HcR string }].Value, .func12` |
| `0x37c90` | `0x27c90` | `tomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, mapH.(*QcMnoAPhGe1).nPxKD4G.func1` |
| `0x37dd0` | `0x27dd0` | `a8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 1 | 16 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, ool; AcDK_Fy.kCEV3Lu09HcR string }].Value` |
| `0x38100` | `0x28100` | `mic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 2 | 4 | `rFh.Is6, ool; AcDK_Fy.kCEV3Lu09HcR string }].Value, pqx).ListenPacket` |
| `0x381b0` | `0x281b0` | `ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 1 | 10 | `).Params, QmBRaybD).MarshalSize, C2.(*TWr_tJSkG90s).Unmarshal` |
| `0x38810` | `0x28810` | `hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 0 | 2 | `atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }, cHKW1j5` |
| `0x38850` | `0x28850` | `P.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 0 | 2 | `.UnmarshalCompressed, cHKW1j5` |
| `0x388b0` | `0x288b0` | `B64P.ihCa8apb = ftFU4ooB64P.ihCa8apb[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 1 | 15 | `).Params, .func12.1.1, cpajYcj).Close` |
| `0x38c60` | `0x28c60` | ` ftFU4ooB64P.q0rQfniWP sync/atomic.ZlSOM4CcHiIw; ftFU4ooB64P.lxZGntXagR ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, Pz4i5V.(*Gf_aZ0Zk).File, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x38cf0` | `0x28cf0` | `ftFU4ooB64P.OxTfod9sV_j; ftFU4ooB64P.sR_iv8MG *ftFU4ooB64P.zkOaisuYQdz[go.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, TMuEM).Add` |
| `0x38e60` | `0x28e60` | `o.shape.*internal/abi.Type,go.shape.interface {}]; ftFU4ooB64P.hWHxlv_We [16]sync/atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, Pz4i5V.sAeZmU, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x39080` | `0x29080` | `.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 1 | 20 | `apH.(*FlCj9pZvT).Exited, ool; AcDK_Fy.kCEV3Lu09HcR string }].Value, indSubmatch` |
| `0x39660` | `0x29660` | `k2` | UNKNOWN | `LOW` | 1 | 6 | `*FlCj9pZvT).UserTime, ool; AcDK_Fy.kCEV3Lu09HcR string }].Value, cDK_Fy.J9R_6Iy_9rFh.Unmap` |
| `0x39880` | `0x29880` | `1ay1Swi` | UNKNOWN | `LOW` | 2 | 9 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, ).wwih4t` |
| `0x39d10` | `0x29d10` | `Fh.BitLen` | UNKNOWN | `LOW` | 1 | 8 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, ).wwih4t` |
| `0x39f80` | `0x29f80` | `ool; AcDK_Fy.kCEV3Lu09HcR string }].Value` | UNKNOWN | `LOW` | 10 | 4 | `atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Store, rY_VpYFfo.xmGgHO, _9rFh.IsLoopback` |
| `0x3a0c0` | `0x2a0c0` | `rFh.Is6` | UNKNOWN | `LOW` | 4 | 10 | `abi.Type,go.shape.interface {}], abi.Type,go.shape.interface {}]).zkOaisuYQdz, rY_VpYFfo.xmGgHO` |
| `0x3a3c0` | `0x2a3c0` | `cDK_Fy.J9R_6Iy_9rFh.Unmap` | UNKNOWN | `LOW` | 2 | 5 | `atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Store, tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, _9rFh.IsLoopback` |
| `0x3a5a0` | `0x2a5a0` | `Unicast` | UNKNOWN | `LOW` | 2 | 3 | `rY_VpYFfo.xmGgHO, _9rFh.IsLoopback, .func12` |
| `0x3a620` | `0x2a620` | `_9rFh.IsLoopback` | UNKNOWN | `LOW` | 5 | 11 | `abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Store, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x3a990` | `0x2a990` | `ulticast` | UNKNOWN | `LOW` | 9 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x3ad10` | `0x2ad10` | `AcDK_Fy.J9R_6Iy_9rFh.IsPrivate` | UNKNOWN | `LOW` | 5 | 2 | `arBaseMult, eam` |
| `0x3ae70` | `0x2ae70` | `specified` | UNKNOWN | `LOW` | 1 | 3 | `rY_VpYFfo.xmGgHO, _9rFh.IsLoopback, .func12` |
| `0x3af30` | `0x2af30` | `Fy.lSiQS70uuAy` | UNKNOWN | `LOW` | 1 | 2 | `J3lU.Compare, .func12` |
| `0x3aff0` | `0x2aff0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x3b2e0` | `0x2b2e0` | `.J9R_6Iy_9rFh.Next` | UNKNOWN | `LOW` | 3 | 2 | `32, .func12` |
| `0x3b4d0` | `0x2b4d0` | `Fh.Prev` | UNKNOWN | `LOW` | 1 | 10 | `32, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x3b880` | `0x2b880` | `QU` | UNKNOWN | `LOW` | 3 | 3 | `i5V.hN4TcGifv }], nmarshal, .func12` |
| `0x3ba00` | `0x2ba00` | `endTo` | UNKNOWN | `LOW` | 1 | 8 | `.func12.1.1, abi.Type; ftFU4ooB64P.xukdOCPY interface {} }]).Load, ` |
| `0x3bdd0` | `0x2bdd0` | `Fy.J9R_6Iy_9rFh.glrtZI_S` | UNKNOWN | `LOW` | 1 | 3 | `QmBRaybD).MarshalSize, wdC2.UzX65jNFzwr.String, .func12` |
| `0x3bf20` | `0x2bf20` | `y4JEEFu` | UNKNOWN | `LOW` | 1 | 3 | `0J3lU).UnmarshalBinary, eam, .func12` |
| `0x3c060` | `0x2c060` | `Iy_9rFh).UnmarshalText` | UNKNOWN | `LOW` | 4 | 4 | `QmBRaybD).MarshalSize, wdC2.UzX65jNFzwr.String, .J9R_6Iy_9rFh.Next` |
| `0x3c210` | `0x2c210` | `32` | UNKNOWN | `LOW` | 6 | 2 | `9rFh.eBH8XrxlJa, .func12` |
| `0x3c2c0` | `0x2c2c0` | `9rFh.eBH8XrxlJa` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x3c390` | `0x2c390` | `RaEDZ0J3lU.Port` | UNKNOWN | `LOW` | 2 | 8 | `32, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x3c510` | `0x2c510` | `J3lU.Compare` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x3c5f0` | `0x2c5f0` | `3lU.AppendTo` | UNKNOWN | `LOW` | 1 | 3 | `afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], zh, .func12` |
| `0x3c690` | `0x2c690` | `t` | UNKNOWN | `LOW` | 30 | 35 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x3c760` | `0x2c760` | `inary` | UNKNOWN | `LOW` | 2 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, SwY3L.iYPHrB4Qx` |
| `0x3c860` | `0x2c860` | `0J3lU).UnmarshalBinary` | UNKNOWN | `LOW` | 3 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, SwY3L.iYPHrB4Qx` |
| `0x3c960` | `0x2c960` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x3ca60` | `0x2ca60` | `asked` | UNKNOWN | `LOW` | 0 | 8 | `J3lU.Compare, .J9R_6Iy_9rFh.Next, QmBRaybD).MarshalSize` |
| `0x3cbb0` | `0x2cbb0` | `ka.aygzIfP83V` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x3ccd0` | `0x2ccd0` | `R` | UNKNOWN | `LOW` | 2 | 14 | `bindRemoteStream, er, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` |
| `0x3ce90` | `0x2ce90` | `t` | UNKNOWN | `LOW` | 30 | 35 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x3cf20` | `0x2cf20` | `lBinary` | UNKNOWN | `LOW` | 3 | 7 | `hhHS85O.wQ6e481ZBAw-fm, Pz4i5V.(*Gf_aZ0Zk).File, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x3cfc0` | `0x2cfc0` | `ape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).f7389394q` | UNKNOWN | `LOW` | 1 | 10 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12.1.1` |
| `0x3d1f0` | `0x2d1f0` | `c.(*ILxa0fgA7[go.shape.struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 1 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x3d250` | `0x2d250` | `{ AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, eam` |
| `0x3d3c0` | `0x2d3c0` | `SOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 1 | 6 | `R, OOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], t` |
| `0x3d490` | `0x2d490` | `AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 2 | 3 | `K_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load, tgJfPz.GcNk7f, .func12` |
| `0x3d580` | `0x2d580` | `]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load` | UNKNOWN | `LOW` | 0 | 2 | `cR string }]).sAix4nb7Lahv, cHKW1j5` |
| `0x3d5e0` | `0x2d5e0` | ` }]).Load` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x3d7a0` | `0x2d7a0` | `cR string }]).sAix4nb7Lahv` | UNKNOWN | `LOW` | 1 | 14 | `hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load, h.AcDK_Fy.bOJFoVB` |
| `0x3db40` | `0x2db40` | `l }]).Load` | UNKNOWN | `LOW` | 1 | 2 | `eam, .func12` |
| `0x3dcb0` | `0x2dcb0` | `iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 1 | 9 | `l }]).Load, nmarshal, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x3df90` | `0x2df90` | `7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 1 | 2 | `DK_Fy.(*GkDvDOF).Bits, .func12` |
| `0x3e0a0` | `0x2e0a0` | `AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 1 | 2 | `_Fy.(*GkDvDOF).AppendBinary, .func12` |
| `0x3e110` | `0x2e110` | `K_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 1 | 2 | `arBaseMult, .func12` |
| `0x3e380` | `0x2e380` | `NtBd9.(*anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).nMPQIFVao` | UNKNOWN | `LOW` | 2 | 3 | `9HcR string }]).tFNbDK7jM, arBaseMult, .func12` |
| `0x3e460` | `0x2e460` | ` }]).nMPQIFVao` | UNKNOWN | `LOW` | 2 | 3 | `.kCEV3Lu09HcR string }], arBaseMult, .func12` |
| `0x3e5a0` | `0x2e5a0` | `vNtBd9.(*aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).aAdrZVI` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x3e5f0` | `0x2e5f0` | `).aAdrZVI` | UNKNOWN | `LOW` | 1 | 2 | `arBaseMult, .func12` |
| `0x3e6c0` | `0x2e6c0` | `9HcR string }]).tFNbDK7jM` | UNKNOWN | `LOW` | 1 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x3e7b0` | `0x2e7b0` | `.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 1 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x3e890` | `0x2e890` | `NtBd9.anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x3e980` | `0x2e980` | `]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 3 | 4 | `A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, nmarshal, eam` |
| `0x3ea90` | `0x2ea90` | `NT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 1 | 3 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, nmarshal, .func12` |
| `0x3ebb0` | `0x2ebb0` | `.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 1 | 4 | `A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, nmarshal, eam` |
| `0x3ed10` | `0x2ed10` | `tr }]).Store` | UNKNOWN | `LOW` | 2 | 3 | `tr }]).Store, nmarshal, .func12` |
| `0x3edf0` | `0x2edf0` | `Lu09HcR string }]).LoadOrStore` | UNKNOWN | `LOW` | 1 | 3 | `_CaZZztHL).Deadline, nmarshal, .func12` |
| `0x3efd0` | `0x2efd0` | `ool; AcDK_Fy.kCEV3Lu09HcR string }]).LoadOrStore.func1` | UNKNOWN | `LOW` | 5 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x3f1a0` | `0x2f1a0` | `uct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).LoadOrStore.deferwrap1` | UNKNOWN | `LOW` | 1 | 6 | `L bool; AcDK_Fy.kCEV3Lu09HcR string }], fwImFp.Done, lBinary` |
| `0x3f290` | `0x2f290` | `.deferwrap1` | UNKNOWN | `LOW` | 10 | 20 | `.UnmarshalCompressed, hhHS85O.wQ6e481ZBAw-fm, OOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x3f450` | `0x2f450` | `9HcR string },go.shape.struct {}]` | UNKNOWN | `LOW` | 4 | 2 | `eam, .func12` |
| `0x3f530` | `0x2f530` | `L bool; AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 6 | 12 | `Lu09HcR string }]).LoadOrStore, 9HcR string },go.shape.struct {}], 9.xIe1xMNMiPk[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` |
| `0x3f830` | `0x2f830` | `t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1` | UNKNOWN | `LOW` | 8 | 6 | `9HcR string },go.shape.struct {}], ool; AcDK_Fy.kCEV3Lu09HcR string }]).LoadOrStore.func1, 9.xIe1xMNMiPk[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` |
| `0x3f9b0` | `0x2f9b0` | `9.xIe1xMNMiPk[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 5 | 23 | `QmBRaybD).MarshalSize, wwdC2.(*JZdvaRJ).DestinationSSRC, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store` |
| `0x40900` | `0x30900` | `ARgPyV0av.A5a5ssp1Sy5c[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 0 | 9 | `YTKDW).Header, (*FCH3YTKDW).DestinationSSRC, ybD).Unmarshal` |
| `0x409a0` | `0x309a0` | `AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 0 | 9 | `YTKDW).Header, (*FCH3YTKDW).DestinationSSRC, ybD).Unmarshal` |
| `0x40a40` | `0x30a40` | `uct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).Load` | UNKNOWN | `LOW` | 0 | 6 | `hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap, y.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap` |
| `0x40af0` | `0x30af0` | `.(*nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).pVkimj_` | UNKNOWN | `LOW` | 1 | 10 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, 6Ae9cBgZT).Contains` |
| `0x40e00` | `0x30e00` | `kimj_` | UNKNOWN | `LOW` | 2 | 5 | `QmBRaybD).MarshalSize, *JZdvaRJ).MarshalSize, L bool; AcDK_Fy.kCEV3Lu09HcR string }]` |
| `0x41090` | `0x31090` | `tring }].Value` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x41150` | `0x31150` | `Lu09HcR string }]).bokhuL6d` | UNKNOWN | `LOW` | 3 | 3 | `A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, .func12` |
| `0x411b0` | `0x311b0` | `vNtBd9.(*d78RFxqBDAf[AcDK_Fy.bOJFoVB]).LoadOrStore` | UNKNOWN | `LOW` | 2 | 6 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, Lu09HcR string }]).bokhuL6d` |
| `0x412c0` | `0x312c0` | `).Load` | UNKNOWN | `LOW` | 1 | 7 | `Lu09HcR string }]).bokhuL6d, 3vJC5GCZyE).Size, QU` |
| `0x41470` | `0x31470` | `mic.(*ILxa0fgA7[go.shape.struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 2 | 5 | `Lu09HcR string }]).bokhuL6d, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap` |
| `0x41540` | `0x31540` | `B]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 4 | 3 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, .func12` |
| `0x41680` | `0x31680` | `y.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 2 | 5 | `ic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap, A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` |
| `0x41750` | `0x31750` | `A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` | UNKNOWN | `LOW` | 7 | 9 | `hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap, y.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap` |
| `0x41970` | `0x31970` | `*ILxa0fgA7[vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]]).Swap` | UNKNOWN | `LOW` | 0 | 2 | `tomic.(*ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }]).CompareAndSwap, cHKW1j5` |
| `0x419d0` | `0x319d0` | `ILxa0fgA7[go.shape.struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap` | UNKNOWN | `LOW` | 5 | 3 | `, eam, .func12` |
| `0x41a40` | `0x31a40` | `tBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap` | UNKNOWN | `LOW` | 5 | 3 | `, eam, .func12` |
| `0x41ab0` | `0x31ab0` | `oVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap` | UNKNOWN | `LOW` | 2 | 2 | `eam, .func12` |
| `0x41b80` | `0x31b80` | `ic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap` | UNKNOWN | `LOW` | 1 | 5 | `A7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, 3vJC5GCZyE).Size, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Swap` |
| `0x41c20` | `0x31c20` | `9.aWLnXGq[AcDK_Fy.bOJFoVB]]).Store` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, eam` |
| `0x41d30` | `0x31d30` | `ct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, tgJfPz.GcNk7f` |
| `0x41e10` | `0x31e10` | `mic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store` | UNKNOWN | `LOW` | 0 | 3 | `atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap, PQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).CompareAndSwap, cHKW1j5` |
| `0x41ec0` | `0x31ec0` | `FoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store` | UNKNOWN | `LOW` | 0 | 7 | `abi.Type,interface {}]).Clear, 3vJC5GCZyE).Size, e,interface {}]).Range` |
| `0x42050` | `0x32050` | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store` | UNKNOWN | `LOW` | 10 | 0 | `None` |
| `0x420f0` | `0x320f0` | `_Fy.bOJFoVB]]).Load` | UNKNOWN | `LOW` | 1 | 3 | `abi.Type,interface {}]] }]).Swap, VB].LoadOrStore, .func12` |
| `0x42360` | `0x32360` | `9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Load` | UNKNOWN | `LOW` | 1 | 7 | `QmBRaybD).MarshalSize, *JZdvaRJ).MarshalSize, hhHS85O.wQ6e481ZBAw-fm` |
| `0x42760` | `0x32760` | `7udFO *vNtBd9.aWLnXGq[AcDK_Fy.bOJFoVB]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Load` | UNKNOWN | `LOW` | 1 | 11 | `ool; AcDK_Fy.kCEV3Lu09HcR string }]).LoadOrStore.func1, QmBRaybD).MarshalSize, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x42ba0` | `0x32ba0` | `GE5q [16]sync/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Load` | UNKNOWN | `LOW` | 2 | 2 | `tgJfPz.GcNk7f, .func12` |
| `0x42c20` | `0x32c20` | `.(*ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]]).CompareAndSwap` | UNKNOWN | `LOW` | 0 | 3 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Load, ARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB].Value, cHKW1j5` |
| `0x42cb0` | `0x32cb0` | `tomic.(*ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }]).CompareAndSwap` | UNKNOWN | `LOW` | 3 | 3 | `ARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB].Value, eam, .r6TygsBh.Len` |
| `0x42d20` | `0x32d20` | `(*ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]]).Swap` | UNKNOWN | `LOW` | 1 | 2 | `arBaseMult, .func12` |
| `0x42df0` | `0x32df0` | `struct { vNtBd9.haTaT_U7 bool }]).Swap` | UNKNOWN | `LOW` | 1 | 3 | `eam, arBaseMult, .func12` |
| `0x42f30` | `0x32f30` | `y.bOJFoVB]]).Store` | UNKNOWN | `LOW` | 1 | 3 | `abi.Type,interface {}]]).Store, nmarshal, .r6TygsBh.Len` |
| `0x43020` | `0x33020` | `ARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB].Value` | UNKNOWN | `LOW` | 2 | 20 | `hhHS85O.wQ6e481ZBAw-fm, *RaEDZ0J3lU).AppendText, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x436f0` | `0x336f0` | `.bOJFoVB]]).CompareAndSwap` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 8 | `FoVB]]).Swap, struct { vNtBd9.haTaT_U7 bool }]).Swap, 9.SsaRalsj[AcDK_Fy.bOJFoVB].Value` |
| `0x439c0` | `0x339c0` | `= vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).CompareAndSwap` | UNKNOWN | `LOW` | 1 | 10 | `tput.deferwrap1, abi.Type,interface {}]).CompareAndDelete, Y41KqyoVl).Deadline` |
| `0x43cf0` | `0x33cf0` | `PQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).CompareAndSwap` | UNKNOWN | `LOW` | 4 | 6 | `QmBRaybD).MarshalSize, AllLiteral.func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x43e50` | `0x33e50` | `bm5AkyfJ uintptr }]).CompareAndSwap` | UNKNOWN | `LOW` | 3 | 15 | `4fQfOR).Err, Y41KqyoVl).Deadline, .jvqY41KqyoVl.Err` |
| `0x44260` | `0x34260` | `FoVB]]).Swap` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x442b0` | `0x342b0` | `O2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap` | UNKNOWN | `LOW` | 7 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x443f0` | `0x343f0` | `y.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap` | UNKNOWN | `LOW` | 6 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, 6Ae9cBgZT).Contains` |
| `0x444e0` | `0x344e0` | `tr }]).Swap` | UNKNOWN | `LOW` | 6 | 7 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x44730` | `0x34730` | `c.(*ILxa0fgA7[go.shape.struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 2 | 7 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x44940` | `0x34940` | `; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 1 | 9 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x44b60` | `0x34b60` | `VAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Store` | UNKNOWN | `LOW` | 1 | 4 | `atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Store, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x44c20` | `0x34c20` | `c.(*ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]).Load` | UNKNOWN | `LOW` | 6 | 7 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x44d90` | `0x34d90` | `struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]; vNtBd9.iMu7Km82nd sync/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 7 | 6 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x44ed0` | `0x34ed0` | `c/atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 1 | 2 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, .func12` |
| `0x45010` | `0x35010` | `[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Load` | UNKNOWN | `LOW` | 2 | 6 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x452f0` | `0x352f0` | `{ AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x453d0` | `0x353d0` | ` AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 1 | 3 | `TMuEM).Add, hhHS85O.wQ6e481ZBAw-fm, .func12` |
| `0x45510` | `0x35510` | `.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, Pz4i5V.(*Gf_aZ0Zk).File, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x455a0` | `0x355a0` | `nc/atomic.(*ILxa0fgA7[go.shape.struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 1 | 11 | `atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store, hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store` |
| `0x457c0` | `0x357c0` | `.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 1 | 7 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x459c0` | `0x359c0` | `tomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 2 | 3 | `txbdkX[go.shape.*uint8]).nIKoXvk5, hape.string]).CompareAndSwap, .func12` |
| `0x45ae0` | `0x35ae0` | `L bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 1 | 6 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x45ba0` | `0x35ba0` | `GE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store` | UNKNOWN | `LOW` | 1 | 7 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, abi.Type,interface {}]] }]).CompareAndSwap` |
| `0x45f60` | `0x35f60` | `9.SsaRalsj[AcDK_Fy.bOJFoVB].Value` | UNKNOWN | `LOW` | 4 | 6 | `hhHS85O.wQ6e481ZBAw-fm, vNtBd9.(*aO37lcef1[AcDK_Fy.bOJFoVB]).Load, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x46300` | `0x36300` | `(*WV9UuS[AcDK_Fy.bOJFoVB]).Value` | UNKNOWN | `LOW` | 1 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x463d0` | `0x363d0` | `vNtBd9.(*aO37lcef1[AcDK_Fy.bOJFoVB]).Load` | UNKNOWN | `LOW` | 1 | 5 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, abi.Type,interface {}]).Clear, hhHS85O.wQ6e481ZBAw-fm` |
| `0x464a0` | `0x364a0` | `VB].LoadOrStore` | UNKNOWN | `LOW` | 1 | 11 | `.UnmarshalCompressed, ).Value, 6Iy_9rFh).String` |
| `0x46650` | `0x36650` | `.AppendBinary` | UNKNOWN | `LOW` | 1 | 12 | `DK_Fy.(*J9R_6Iy_9rFh).WithZone, AcDK_Fy.kCEV3Lu09HcR string }]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.o7bm5AkyfJ uintptr }]).Load, ring` |
| `0x468c0` | `0x368c0` | `y.(*J9R_6Iy_9rFh).As16` | UNKNOWN | `LOW` | 1 | 6 | `hhHS85O.wQ6e481ZBAw-fm, Kus).Done, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x46a20` | `0x36a20` | `Fy.(*J9R_6Iy_9rFh).BitLen` | UNKNOWN | `LOW` | 6 | 10 | `tBd9.nMPQIFVao[AcDK_Fy.bOJFoVB], ZWj4kZX).Bits, Iy_9rFh).Next` |
| `0x46ee0` | `0x36ee0` | `DK_Fy.(*J9R_6Iy_9rFh).Is4In6` | UNKNOWN | `LOW` | 1 | 6 | `.Error, h.AcDK_Fy.bOJFoVB, NtBd9.(*anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).nMPQIFVao` |
| `0x47210` | `0x37210` | `lUnicast` | UNKNOWN | `LOW` | 1 | 3 | `Deadline, arBaseMult, .func12` |
| `0x472d0` | `0x372d0` | `kLocalMulticast` | UNKNOWN | `LOW` | 2 | 15 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]], lUnicast, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x47b60` | `0x37b60` | `pback` | UNKNOWN | `LOW` | 0 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x47c90` | `0x37c90` | `R_6Iy_9rFh).IsUnspecified` | UNKNOWN | `LOW` | 1 | 12 | `atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]], kLocalMulticast, DK_Fy.(*J9R_6Iy_9rFh).Is4In6` |
| `0x47ee0` | `0x37ee0` | `cDK_Fy.(*J9R_6Iy_9rFh).MarshalBinary` | UNKNOWN | `LOW` | 1 | 5 | `shalText,  }]).nMPQIFVao, Fy.(*J9R_6Iy_9rFh).BitLen` |
| `0x48210` | `0x38210` | `Iy_9rFh).Next` | UNKNOWN | `LOW` | 1 | 2 | `nmarshal, .func12` |
| `0x48340` | `0x38340` | `6Iy_9rFh).String` | UNKNOWN | `LOW` | 1 | 4 | `abi.Type,interface {}]).LoadOrStore, .UnmarshalCompressed, eam` |
| `0x48480` | `0x38480` | `DK_Fy.(*J9R_6Iy_9rFh).WithZone` | UNKNOWN | `LOW` | 1 | 15 | `ror, ring, tR.DjbdQE3l` |
| `0x489b0` | `0x389b0` | `_Fy.(*GkDvDOF).AppendBinary` | UNKNOWN | `LOW` | 2 | 12 | `ring, tR.DjbdQE3l, abi.Type,interface {}]).CompareAndDelete` |
| `0x48c90` | `0x38c90` | `DK_Fy.(*GkDvDOF).Bits` | UNKNOWN | `LOW` | 1 | 3 | `abi.Type,interface {}]).LoadOrStore, .UnmarshalCompressed, .func12` |
| `0x48d30` | `0x38d30` | `(*GkDvDOF).IsValid` | UNKNOWN | `LOW` | 1 | 2 | `Fy.(*GkDvDOF).Masked, .func12` |
| `0x48de0` | `0x38de0` | `Fy.(*GkDvDOF).Masked` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x48ea0` | `0x38ea0` | `T0FZMNmhD).Error` | UNKNOWN | `LOW` | 2 | 5 | ` }]).nMPQIFVao, K_Fy.(*RaEDZ0J3lU).IsValid, Fy.(*J9R_6Iy_9rFh).BitLen` |
| `0x490a0` | `0x390a0` | `*RaEDZ0J3lU).AppendText` | UNKNOWN | `LOW` | 1 | 7 | `kLocalMulticast, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]], Fy.(*J9R_6Iy_9rFh).BitLen` |
| `0x49350` | `0x39350` | `K_Fy.(*RaEDZ0J3lU).IsValid` | UNKNOWN | `LOW` | 4 | 2 | `arBaseMult, .func12` |
| `0x49490` | `0x39490` | `shalText` | UNKNOWN | `LOW` | 3 | 4 | `ZWj4kZX).Bits, 1g.(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Unmarshal, arBaseMult` |
| `0x49610` | `0x39610` | `.Error` | UNKNOWN | `LOW` | 13 | 5 | `arBaseMult, .func12, (*gxe_j_u89O0).hjFGwuAXG3` |
| `0x49790` | `0x39790` | `tBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x49950` | `0x39950` | `nc/atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]]` | UNKNOWN | `LOW` | 3 | 3 | `vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]], K_Fy.bOJFoVB]], .func12` |
| `0x49a00` | `0x39a00` | `vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x49ae0` | `0x39ae0` | `K_Fy.bOJFoVB]]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x49bc0` | `0x39bc0` | `h.AcDK_Fy.bOJFoVB` | UNKNOWN | `LOW` | 2 | 3 | `K_Fy.(*RaEDZ0J3lU).IsValid, shalText, .func12` |
| `0x49c30` | `0x39c30` | `mic.ILxa0fgA7[go.shape.struct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 1 | 3 | `hape.string]).CompareAndSwap, eam, .func12` |
| `0x49cd0` | `0x39cd0` | `{ AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 1 | 2 | `eam, .func12` |
| `0x49d40` | `0x39d40` | `SOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 3 | 2 | `eam, .func12` |
| `0x49db0` | `0x39db0` | `AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 1 | 2 | `eam, .func12` |
| `0x49e20` | `0x39e20` | `]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]` | UNKNOWN | `LOW` | 2 | 9 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]).Clear, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4a250` | `0x3a250` | `ruct { vNtBd9.anIeJO2iz9g = vNtBd9.anIeJO2iz9g[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 2 | 5 | `hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4a380` | `0x3a380` | `.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.vuaExWN1E sync/atomic.ZlSOM4CcHiIw; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 2 | 3 | `atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }], nmarshal, .func12` |
| `0x4a470` | `0x3a470` | `w; vNtBd9.wUCcDa7udFO *vNtBd9.aWLnXGq[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4a560` | `0x3a560` | ` bool; AcDK_Fy.kCEV3Lu09HcR string }]; vNtBd9.cyc3LPxgSyIq sync.CC4ebv5yI; vNtBd9.dlQQdGE5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 1 | 9 | `func1, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }], atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]` |
| `0x4a720` | `0x3a720` | `E5q [16]sync/atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }` | UNKNOWN | `LOW` | 0 | 2 | `atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Store, cHKW1j5` |
| `0x4a760` | `0x3a760` | `bool }] }` | UNKNOWN | `LOW` | 1 | 5 | `atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }], hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4a860` | `0x3a860` | `Lu09HcR string }]` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x4a910` | `0x3a910` | `ool }]` | UNKNOWN | `LOW` | 2 | 14 | `ZqlIeq[go.shape.int32], func1, .vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` |
| `0x4ab80` | `0x3ab80` | `.vNtBd9.nMPQIFVao[go.shape.struct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 1 | 5 | `CM, KEOvQk, StartCond` |
| `0x4ad70` | `0x3ad70` | `]` | UNKNOWN | `LOW` | 7 | 22 | `.func12.1.1, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x4ae00` | `0x3ae00` | `l; AcDK_Fy.kCEV3Lu09HcR string }]]` | UNKNOWN | `LOW` | 1 | 2 | `.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }], .func12` |
| `0x4af90` | `0x3af90` | `.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]` | UNKNOWN | `LOW` | 1 | 3 | `tgJfPz.GcNk7f, nmarshal, .func12` |
| `0x4b070` | `0x3b070` | `ZL bool; AcDK_Fy.kCEV3Lu09HcR string }` | UNKNOWN | `LOW` | 0 | 4 | `indSubmatch, KcotjIqdR.(*Laxp2QOnMe2a).FindAllString, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x4b140` | `0x3b140` | `aF9g0geqI.Error` | UNKNOWN | `LOW` | 1 | 4 | `p_.Deadline, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve, nmarshal` |
| `0x4b2b0` | `0x3b2b0` | `p_.Deadline` | UNKNOWN | `LOW` | 2 | 5 | `atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }], atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }], hhHS85O.wQ6e481ZBAw-fm` |
| `0x4b3f0` | `0x3b3f0` | `wizKus.String` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x4b400` | `0x3b400` | `0ytR.EjkuJwt` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x4b410` | `0x3b410` | `CazCzTylI` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x4b460` | `0x3b460` | `aO3lL0ytR.(*lJ_CaZZztHL).Done.deferwrap1` | UNKNOWN | `LOW` | 1 | 3 | `ZztHL)._avZ_Q7jcT, eam, .func12` |
| `0x4b4d0` | `0x3b4d0` | `ZztHL)._avZ_Q7jcT` | UNKNOWN | `LOW` | 2 | 2 | `Z_Q7jcT.func1, .func12` |
| `0x4b670` | `0x3b670` | `Z_Q7jcT.func1` | UNKNOWN | `LOW` | 1 | 11 | `YT47X.String, tgJfPz.GcNk7f, .UnmarshalCompressed` |
| `0x4b820` | `0x3b820` | `L).ggO9UNZ3VT7` | UNKNOWN | `LOW` | 0 | 3 | `ne, nmarshal, cHKW1j5` |
| `0x4b890` | `0x3b890` | `ne` | UNKNOWN | `LOW` | 85 | 10 | `WPs1, indSubmatch, KcotjIqdR.(*Laxp2QOnMe2a).FindAllString` |
| `0x4ba40` | `0x3ba40` | `gPXZK` | UNKNOWN | `LOW` | 4 | 4 | `4i5V.onlt3vXM.Error, tgJfPz.GcNk7f, *GFanmdO8dYdH).Temporary` |
| `0x4bb80` | `0x3bb80` | `R.AgPXZK.func1` | UNKNOWN | `LOW` | 0 | 6 | `.UnmarshalCompressed, estinationSSRC, c1` |
| `0x4bc80` | `0x3bc80` | `ring` | UNKNOWN | `LOW` | 7 | 17 | `eam, .func12, 0Z.CRgkYGl[go.shape.*JYT1bAJ.GUY8D0aEy].no8oNaHYnRI[go.shape.*JYT1bAJ.GUY8D0aEy].func2` |
| `0x4bcf0` | `0x3bcf0` | `tR.DjbdQE3l` | UNKNOWN | `LOW` | 2 | 2 | `eam, .func12` |
| `0x4bdc0` | `0x3bdc0` | `).Value` | UNKNOWN | `LOW` | 1 | 3 | `hape.string]).CompareAndSwap, .UnmarshalCompressed, .func12` |
| `0x4be50` | `0x3be50` | `ror` | UNKNOWN | `LOW` | 4 | 11 | `nmarshal, .func12, hape.map[string]bool,go.shape.string,go.shape.bool]` |
| `0x4bf50` | `0x3bf50` | `Deadline` | UNKNOWN | `LOW` | 1 | 3 | `ror, nmarshal, .func12` |
| `0x4c050` | `0x3c050` | `L0ytR.wizKus.Deadline` | UNKNOWN | `LOW` | 1 | 12 | `ror, 3vJC5GCZyE).Size, hape.string]).CompareAndSwap` |
| `0x4c4a0` | `0x3c4a0` | `Kus).Done` | UNKNOWN | `LOW` | 1 | 4 | `hape.string]).CompareAndSwap, 3vJC5GCZyE).Size, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x4c570` | `0x3c570` | `ytR.wizKus.Value` | UNKNOWN | `LOW` | 4 | 7 | `.(*qNql8ATr).Done, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, hhHS85O.wQ6e481ZBAw-fm` |
| `0x4c770` | `0x3c770` | `_CaZZztHL).Deadline` | UNKNOWN | `LOW` | 2 | 2 | `, .func12` |
| `0x4c950` | `0x3c950` | `fwImFp.Done` | UNKNOWN | `LOW` | 1 | 8 | `, eam, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x4cad0` | `0x3cad0` | `lL0ytR.ffwImFp.Value` | UNKNOWN | `LOW` | 1 | 2 | `hape.string]).CompareAndSwap, .func12` |
| `0x4cbb0` | `0x3cbb0` | `.(*qNql8ATr).Done` | UNKNOWN | `LOW` | 1 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x4cc80` | `0x3cc80` | `l8ATr).Value` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x4cc90` | `0x3cc90` | `4fQfOR).Err` | UNKNOWN | `LOW` | 8 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x4cd50` | `0x3cd50` | `Y41KqyoVl).Deadline` | UNKNOWN | `LOW` | 9 | 8 | `hhHS85O.wQ6e481ZBAw-fm, nmarshal, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x4ce60` | `0x3ce60` | `.jvqY41KqyoVl.Err` | UNKNOWN | `LOW` | 9 | 7 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x4cf20` | `0x3cf20` | `kkbtL).ix6eJnUtw21` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x4d060` | `0x3d060` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x4d070` | `0x3d070` | `).wwih4t` | UNKNOWN | `LOW` | 7 | 1 | `tgJfPz.GcNk7f` |
| `0x4d0d0` | `0x3d0d0` | `B4Uc` | UNKNOWN | `LOW` | 6 | 9 | `Unicast, , rY_VpYFfo.xmGgHO` |
| `0x4d3d0` | `0x3d3d0` | `1_9` | UNKNOWN | `LOW` | 5 | 0 | `None` |
| `0x4d470` | `0x3d470` | `bxHo` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x4d510` | `0x3d510` | `*REGwhN0w0eUN).MXResource` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, sL, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4d5a0` | `0x3d5a0` | `EGwhN0w0eUN).PTRResource` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, 1_9, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4d660` | `0x3d660` | `Resource` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x4d820` | `0x3d820` | `*REGwhN0w0eUN).AAAAResource` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x4d8c0` | `0x3d8c0` | `x6eJnUtw21` | UNKNOWN | `LOW` | 3 | 2 | `tgJfPz.GcNk7f, .func12` |
| `0x4d920` | `0x3d920` | `).OPTResource` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x4d960` | `0x3d960` | `cO4).ix6eJnUtw21` | UNKNOWN | `LOW` | 1 | 3 | `TMuEM).Add, eam, .func12` |
| `0x4db50` | `0x3db50` | `.Finish` | UNKNOWN | `LOW` | 3 | 6 | `hhHS85O.wQ6e481ZBAw-fm, 1_9, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4de20` | `0x3de20` | `XxZk5yMz` | UNKNOWN | `LOW` | 0 | 3 | `.Finish, n.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }], .func12` |
| `0x4dea0` | `0x3dea0` | `Jid9HOJll` | UNKNOWN | `LOW` | 0 | 3 | `.Finish, n.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }], .func12` |
| `0x4df20` | `0x3df20` | `UdOhYv).ix6eJnUtw21` | UNKNOWN | `LOW` | 0 | 3 | `.Finish, n.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }], .func12` |
| `0x4dfa0` | `0x3dfa0` | `hQnJv.cTlADbQXm` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, hape.string]).CompareAndSwap, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x4e0b0` | `0x3e0b0` | `sL` | UNKNOWN | `LOW` | 1 | 8 | `4CM, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x4e260` | `0x3e260` | `.DoChan.gowrap1` | UNKNOWN | `LOW` | 1 | 3 | `.(*zop57OMF).Len, 4CM, .func12` |
| `0x4e300` | `0x3e300` | `SaX.(*NsWPchGD).ForgetUnshared.deferwrap1` | UNKNOWN | `LOW` | 1 | 2 | `4CM, .func12` |
| `0x4e370` | `0x3e370` | `i5V.C9QITNV4ixi` | UNKNOWN | `LOW` | 2 | 8 | `JYT1bAJ.(*TCYzSpw).Add, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x4e490` | `0x3e490` | `i5V.init.EIYgRcen.func7.1` | UNKNOWN | `LOW` | 4 | 13 | `gxe_j_u89O0.(*gxe_j_u89O0).pVHK96hna1, or, bxHo` |
| `0x4e800` | `0x3e800` | `5V.init.func2` | UNKNOWN | `LOW` | 3 | 1 | `Al[go.shape.*JYT1bAJ.DKyyIy]` |
| `0x4e890` | `0x3e890` | `nit.func6` | UNKNOWN | `LOW` | 2 | 2 | `Al[go.shape.*JYT1bAJ.DKyyIy], tgJfPz.GcNk7f` |
| `0x4e910` | `0x3e910` | `.(*imjbVH0I7c).m1iJJwlO4` | UNKNOWN | `LOW` | 0 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, t2q.Size` |
| `0x4e990` | `0x3e990` | `bXPz4i5V.xUgqHZic` | UNKNOWN | `LOW` | 3 | 3 | `e.*JYT1bAJ.DKyyIy], alarMult, .func12` |
| `0x4ea80` | `0x3ea80` | `,go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 1 | 8 | `orHJ20Z.init.EIYgRcen.func11.1.1, .(*Lb1Wr6XtTC_d).o3Eao_wGk, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x4ebe0` | `0x3ebe0` | `XPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 0 | 2 | `], cHKW1j5` |
| `0x4ec60` | `0x3ec60` | `Pz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 1 | 12 | `*icpajYcj).LocalAddr, .UnmarshalCompressed, KQ.(*N3vJC5GCZyE).Nat` |
| `0x4eed0` | `0x3eed0` | `*icpajYcj).LocalAddr` | UNKNOWN | `LOW` | 1 | 4 | `Qzr8, .UnmarshalCompressed, nmarshal` |
| `0x4f010` | `0x3f010` | `5V.wxapACNj` | UNKNOWN | `LOW` | 1 | 6 | `KQ.(*N3vJC5GCZyE).Nat, or, ` |
| `0x4f120` | `0x3f120` | `llQxe` | UNKNOWN | `LOW` | 0 | 4 | `bXPz4i5V.xUgqHZic, 5V.wxapACNj, g` |
| `0x4f170` | `0x3f170` | `34Dwh).v_YAYAghVIR` | UNKNOWN | `LOW` | 1 | 5 | `KQ.(*N3vJC5GCZyE).Nat, or, ` |
| `0x4f240` | `0x3f240` | `XPz4i5V.(*ke34Dwh).lDryR_cxCM` | UNKNOWN | `LOW` | 2 | 3 | `fhK.jk2XsnVPM[go.shape.string], ZX).fMHAulaw, .func12` |
| `0x4f290` | `0x3f290` | `nc1` | UNKNOWN | `LOW` | 17 | 22 | `t.0.func1.1, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }, eam` |
| `0x4f310` | `0x3f310` | `ct { hbXPz4i5V.t168Wlq7 []string; hbXPz4i5V.dWtrpejzqf []string; hbXPz4i5V.hMx5puF2VMG int; hbXPz4i5V.sSSkltnfCZ eFuxzMSJ.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load` | UNKNOWN | `LOW` | 1 | 1 | `Ia` |
| `0x4f370` | `0x3f370` | `nt; hbXPz4i5V.sSSkltnfCZ eFuxzMSJ.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load` | UNKNOWN | `LOW` | 1 | 2 | `].func10, tgJfPz.GcNk7f` |
| `0x4f3e0` | `0x3f3e0` | `l; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load` | UNKNOWN | `LOW` | 2 | 3 | `, 7KQ.(*ZWj4kZX).f6bVc_uVm, .func12` |
| `0x4f440` | `0x3f440` | `bXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load` | UNKNOWN | `LOW` | 1 | 10 | `OK7KQ.aDvjUG, tVarTime, OK7KQ.caI7u0GXQge` |
| `0x4f760` | `0x3f760` | `bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load` | UNKNOWN | `LOW` | 1 | 6 | `4CM, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x4f9f0` | `0x3f9f0` | `iaoOaLpN bool }]).Load` | UNKNOWN | `LOW` | 16 | 4 | `CM, nxvAjr).bmW27aIB17zH, eam` |
| `0x4fac0` | `0x3fac0` | `mMKGlMZz.func1` | UNKNOWN | `LOW` | 2 | 2 | `eam, .func12` |
| `0x4fb20` | `0x3fb20` | `.j0AKPEC3zrM` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4fbb0` | `0x3fbb0` | `z4i5V.(*YMbT3l).kOKllJU86S` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4fc40` | `0x3fc40` | `*YLYtpMxe_SvW).hdZoaa` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4fcd0` | `0x3fcd0` | `Pz4i5V.(*J6Gcsld4).MultipathTCP` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4fd60` | `0x3fd60` | `a).tHL3lgPnC` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4fdf0` | `0x3fdf0` | `z4i5V.(*J6Gcsld4).DialContext` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4fe80` | `0x3fe80` | `XPaPuI` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4ff10` | `0x3ff10` | `(*u8EpLV).gDOxT5V2eRB` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x4ffa0` | `0x3ffa0` | `p4` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x50030` | `0x40030` | `XPz4i5V.(*u8EpLV).gDOxT5V2eRB.func1` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x500c0` | `0x400c0` | `.(*u8EpLV).iiLcfJxM` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x50150` | `0x40150` | `V).zpsx24n.func1` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x501e0` | `0x401e0` | `thTCP` | UNKNOWN | `LOW` | 0 | 4 | `iaoOaLpN bool }]).Load, _ string }], ma.(*MydupPsvCWhi).SetExtension` |
| `0x50270` | `0x40270` | `a9eldi` | UNKNOWN | `LOW` | 31 | 3 | `iaoOaLpN bool }]).Load, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x502d0` | `0x402d0` | `pqx).ListenPacket` | UNKNOWN | `LOW` | 69 | 3 | `mMKGlMZz.func1, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x50330` | `0x40330` | `i5V.eXjLW2JW` | UNKNOWN | `LOW` | 6 | 4 | `*FaSa1kE64).haSAaVZT, X[*JYT1bAJ.JgiPo3aUOjR]).Double, eam` |
| `0x503f0` | `0x403f0` | `4ce` | UNKNOWN | `LOW` | 4 | 3 | `ma.(*MydupPsvCWhi).SetExtension, eam, .func12` |
| `0x504c0` | `0x404c0` | `ape.*uint8]` | UNKNOWN | `LOW` | 9 | 7 | `, .JgiPo3aUOjR]).ScalarBaseMult, .func12` |
| `0x505b0` | `0x405b0` | `iIYA,go.shape.*uint8]` | UNKNOWN | `LOW` | 19 | 1 | `eam` |
| `0x50610` | `0x40610` | `*FaSa1kE64).haSAaVZT` | UNKNOWN | `LOW` | 1 | 9 | `hhHS85O.wQ6e481ZBAw-fm, ).Params, er` |
| `0x50810` | `0x40810` | `GHjbChz).SetEDNS0` | UNKNOWN | `LOW` | 1 | 10 | `).Params, giPo3aUOjR]).Unmarshal, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` |
| `0x50ae0` | `0x40ae0` | `5V.fQMajfD4` | UNKNOWN | `LOW` | 645 | 3 | `Pz4i5V.(*YMbT3l).iiabYAB8go, s3eGTB1pswT).init, .func12` |
| `0x50b70` | `0x40b70` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x50d30` | `0x40d30` | `swer` | UNKNOWN | `LOW` | 2 | 7 | `swer, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x50e50` | `0x40e50` | `SkipAllAuthorities` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x50e60` | `0x40e60` | `nalHeader` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x50e70` | `0x40e70` | `Pz4i5V.(*YMbT3l).iiabYAB8go` | UNKNOWN | `LOW` | 2 | 5 | `.UnmarshalCompressed, ).Params, X[*JYT1bAJ.JgiPo3aUOjR]).Double` |
| `0x50fd0` | `0x40fd0` | `s3eGTB1pswT).init` | UNKNOWN | `LOW` | 2 | 8 | `.UnmarshalCompressed, ).Params,  hbXPz4i5V.dWtrpejzqf []string; hbXPz4i5V.hMx5puF2VMG int; hbXPz4i5V.sSSkltnfCZ eFuxzMSJ.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` |
| `0x51180` | `0x41180` | ` hbXPz4i5V.dWtrpejzqf []string; hbXPz4i5V.hMx5puF2VMG int; hbXPz4i5V.sSSkltnfCZ eFuxzMSJ.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` | UNKNOWN | `LOW` | 2 | 2 | `tgJfPz.GcNk7f, .func12` |
| `0x51200` | `0x41200` | `.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` | UNKNOWN | `LOW` | 0 | 5 | `indSubmatch, nMe2a).FindSubmatchIndex, MO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` |
| `0x51340` | `0x41340` | `MO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` | UNKNOWN | `LOW` | 1 | 6 | `r).rbvbqSXq, .UnmarshalCompressed, a9eldi` |
| `0x515b0` | `0x415b0` | `eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` | UNKNOWN | `LOW` | 39 | 0 | `None` |
| `0x515f0` | `0x415f0` | `gSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store` | UNKNOWN | `LOW` | 0 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x51660` | `0x41660` | `bool }]).Store` | UNKNOWN | `LOW` | 25 | 4 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, tgJfPz.GcNk7f, zN3TrI24I` |
| `0x516f0` | `0x416f0` | `bXPz4i5V.(*s3eGTB1pswT).lcyN8Ohw5B9.deferwrap1` | UNKNOWN | `LOW` | 0 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x51760` | `0x41760` | `B1pswT).sXbd0tPFqWQ0` | UNKNOWN | `LOW` | 0 | 11 | `CM, r).rbvbqSXq, .UnmarshalCompressed` |
| `0x51a30` | `0x41a30` | `zN3TrI24I` | UNKNOWN | `LOW` | 2 | 1 | `tgJfPz.GcNk7f` |
| `0x51a90` | `0x41a90` | `Zx2Sm` | UNKNOWN | `LOW` | 0 | 5 | `.(*ZWj4kZX).SetUint, .1, unc2.deferwrap1` |
| `0x51b20` | `0x41b20` | `s68i` | UNKNOWN | `LOW` | 1 | 2 | `tgJfPz.GcNk7f, evZ).MarshalText` |
| `0x51ba0` | `0x41ba0` | `.(*YMbT3l).lHHtPt2D1b.func3.gowrap1` | UNKNOWN | `LOW` | 0 | 4 | `.1, swer, unc2.deferwrap1` |
| `0x51c90` | `0x41c90` | `.1` | UNKNOWN | `LOW` | 4 | 17 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x51e30` | `0x41e30` | `unc2.deferwrap1` | UNKNOWN | `LOW` | 2 | 11 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x52190` | `0x42190` | `T3l).yjHB9zX` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x521b0` | `0x421b0` | `fc.deferwrap1` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x522e0` | `0x422e0` | `5V.(*mheejkbo8).Close` | UNKNOWN | `LOW` | 1 | 2 | `CM, .func12` |
| `0x52380` | `0x42380` | `heejkbo8).Read` | UNKNOWN | `LOW` | 1 | 1 | `CM` |
| `0x523c0` | `0x423c0` | `i5V.(*mheejkbo8).yfw6D0U3os` | UNKNOWN | `LOW` | 1 | 8 | `giPo3aUOjR]).Unmarshal, er, .UnmarshalCompressed` |
| `0x525b0` | `0x425b0` | `Eac` | UNKNOWN | `LOW` | 1 | 3 | `hf9RoG, giPo3aUOjR]).Unmarshal, .func12` |
| `0x52680` | `0x42680` | `hf9RoG` | UNKNOWN | `LOW` | 2 | 5 | `d, .UnmarshalCompressed, atomic.ILxa0fgA7[go.shape.struct { ftFU4ooB64P.haTaT_U7 bool }] }]).Store` |
| `0x52780` | `0x42780` | `.(*mheejkbo8).firDkDJYzj` | UNKNOWN | `LOW` | 1 | 5 | `ma.(*MydupPsvCWhi).SetExtension, YLuQc.init, .G2Rzf5wkmWe[go.shape.[]string,go.shape.string]` |
| `0x52890` | `0x42890` | `d` | UNKNOWN | `LOW` | 15 | 55 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x52bc0` | `0x42bc0` | `mheejkbo8).SetWriteDeadline` | UNKNOWN | `LOW` | 0 | 2 | `V.(*mheejkbo8).wRTEtQKX9, cHKW1j5` |
| `0x52c10` | `0x42c10` | `Pz4i5V.(*mheejkbo8).amMlbhuQY.func2` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.jqiHN7bSEwca, cHKW1j5` |
| `0x52c50` | `0x42c50` | `huQY.func1` | UNKNOWN | `LOW` | 1 | 5 | `9.SsaRalsj[AcDK_Fy.bOJFoVB].Value, 3vJC5GCZyE).Size, EyvNEwJVta).ti68CiX` |
| `0x52da0` | `0x42da0` | `Pz4i5V.jqiHN7bSEwca` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, abi.Type,interface {}]]).Store, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x52f30` | `0x42f30` | `V.(*mheejkbo8).wRTEtQKX9` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, eam` |
| `0x53100` | `0x43100` | `V.e39Yl0` | UNKNOWN | `LOW` | 2 | 15 | `bT3l).vYtEfu, V.(*YMbT3l).pcPuvCGTGV, .func12.1.1` |
| `0x535f0` | `0x435f0` | `aRqEWB5xH66` | UNKNOWN | `LOW` | 2 | 10 | `V.(*YMbT3l).pcPuvCGTGV, Pz4i5V.sAeZmU, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x537a0` | `0x437a0` | `bXPz4i5V.avNDhyVs.deferwrap1` | UNKNOWN | `LOW` | 0 | 1 | `tQ0xKHZgC5j.init.func1` |
| `0x537f0` | `0x437f0` | `.(*ZOL1a3wcbJA).Addrs` | UNKNOWN | `LOW` | 0 | 9 | `CM, hG.qVED1belCV, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x538a0` | `0x438a0` | `XPz4i5V.BNOfD2CCJ` | UNKNOWN | `LOW` | 1 | 9 | `CM, _pbNwhG.frg6VKd324v, KEOvQk` |
| `0x53c10` | `0x43c10` | `5GhhJ7` | UNKNOWN | `LOW` | 1 | 5 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, 3vJC5GCZyE).Size` |
| `0x53d90` | `0x43d90` | `XPz4i5V.(*priWRezQsI).lEvYyBEt` | UNKNOWN | `LOW` | 166 | 2 | `hhHS85O.wQ6e481ZBAw-fm, .func12` |
| `0x53e10` | `0x43e10` | `bXPz4i5V.jP7NLOA9Bd9g` | UNKNOWN | `LOW` | 164 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x53e70` | `0x43e70` | `4i5V.ghVqRVnl_Y` | UNKNOWN | `LOW` | 5 | 5 | `5GhhJ7, 3vJC5GCZyE).Size, etWriteDeadline` |
| `0x53f70` | `0x43f70` | `jmJpBM.deferwrap1` | UNKNOWN | `LOW` | 14 | 2 | `4i5V.mkwDVaH0Iu, .func12` |
| `0x53fb0` | `0x43fb0` | `p1` | UNKNOWN | `LOW` | 126 | 5 | `4i5V.mkwDVaH0Iu, .func12, I).AddTo` |
| `0x53ff0` | `0x43ff0` | `XPz4i5V.ISwY3L.IsPrivate` | UNKNOWN | `LOW` | 6 | 2 | `4i5V.mkwDVaH0Iu, .func12` |
| `0x54050` | `0x44050` | `ulticast` | UNKNOWN | `LOW` | 9 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x542b0` | `0x442b0` | `4i5V.ISwY3L.IsGlobalUnicast` | UNKNOWN | `LOW` | 2 | 5 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, ulticast` |
| `0x54330` | `0x44330` | `.ISwY3L.Mask` | UNKNOWN | `LOW` | 86 | 3 | `4i5V.ghVqRVnl_Y, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, .func12` |
| `0x54410` | `0x44410` | `SwY3L.iYPHrB4Qx` | UNKNOWN | `LOW` | 44 | 3 | `4i5V.mkwDVaH0Iu, .ISwY3L.Mask, .func12` |
| `0x54470` | `0x44470` | `Y3L).UnmarshalText` | UNKNOWN | `LOW` | 57 | 3 | `4i5V.ghVqRVnl_Y, nmarshal, .func12` |
| `0x54590` | `0x44590` | `t2q.Size` | UNKNOWN | `LOW` | 21 | 2 | `Y3L).UnmarshalText, .func12` |
| `0x545d0` | `0x445d0` | `6Ae9cBgZT).Contains` | UNKNOWN | `LOW` | 4 | 2 | `Y3L).UnmarshalText, .func12` |
| `0x54610` | `0x44610` | `4i5V.mkwDVaH0Iu` | UNKNOWN | `LOW` | 166 | 2 | `4i5V.ghVqRVnl_Y, .func12` |
| `0x54660` | `0x44660` | `pMxe_SvW).String` | UNKNOWN | `LOW` | 1 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, SwY3L.iYPHrB4Qx` |
| `0x54700` | `0x44700` | `SyscallConn` | UNKNOWN | `LOW` | 2 | 12 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, p1, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x54940` | `0x44940` | `TQS77dB3UiY` | UNKNOWN | `LOW` | 0 | 18 | `tgJfPz.GcNk7f, .func12.1.1, .SetDeadline` |
| `0x54d40` | `0x44d40` | `5V.(*FYlgJgI).WriteToIP` | UNKNOWN | `LOW` | 0 | 2 | `jkbo8).wNv3ibD.(*mheejkbo8).cQjpP4oK.func1, cHKW1j5` |
| `0x54d80` | `0x44d80` | `4i5V.(*FYlgJgI).WriteTo` | UNKNOWN | `LOW` | 0 | 2 | `giPo3aUOjR]).Unmarshal, .func12` |
| `0x54e10` | `0x44e10` | `hbXPz4i5V.zSKTc9G` | UNKNOWN | `LOW` | 0 | 2 | `EZsdym0, .func12` |
| `0x54e50` | `0x44e50` | `(*YLYtpMxe_SvW).knE17ria2` | UNKNOWN | `LOW` | 0 | 10 | `.UnmarshalCompressed, .func12.1.1, abi.Type,interface {}]] }]).Load` |
| `0x54f50` | `0x44f50` | `Cv8` | UNKNOWN | `LOW` | 0 | 1 | `tQ0xKHZgC5j.init.func1` |
| `0x54f80` | `0x44f80` | `bXPz4i5V.(*FYlgJgI).firDkDJYzj` | UNKNOWN | `LOW` | 1 | 1 | `tQ0xKHZgC5j.init.func1` |
| `0x54fd0` | `0x44fd0` | `6G1wg0` | UNKNOWN | `LOW` | 5 | 10 | `hhHS85O.wQ6e481ZBAw-fm, ).Params, eam` |
| `0x55270` | `0x45270` | `i0` | UNKNOWN | `LOW` | 6 | 10 | `jMcnw, .UnmarshalCompressed, ).Params` |
| `0x55540` | `0x45540` | `d` | UNKNOWN | `LOW` | 15 | 55 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x55580` | `0x45580` | `bXPz4i5V.L_lrJFgcrN` | UNKNOWN | `LOW` | 1 | 2 | `eam, .func12` |
| `0x555c0` | `0x455c0` | `*YMbT3l).iYaqneYV3.func1` | UNKNOWN | `LOW` | 0 | 2 | `ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x55600` | `0x45600` | `4i5V.(*bZ6OrsyByy0).faVJLQa8.deferwrap1` | UNKNOWN | `LOW` | 0 | 1 | `bT3l).LookupHost` |
| `0x55630` | `0x45630` | `Pz4i5V.of2NkKPmGS7o` | UNKNOWN | `LOW` | 0 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x55710` | `0x45710` | `i5V.hA5dQp71LFt5` | UNKNOWN | `LOW` | 0 | 1 | `etWriteDeadline` |
| `0x55740` | `0x45740` | `bT3l).LookupHost` | UNKNOWN | `LOW` | 1 | 4 | `init.func8, ScalarMult, etWriteDeadline` |
| `0x55810` | `0x45810` | `.(*YMbT3l).LookupNetIP` | UNKNOWN | `LOW` | 2 | 8 | `hhHS85O.wQ6e481ZBAw-fm, jMcnw, .UnmarshalCompressed` |
| `0x559a0` | `0x459a0` | `V.fEj8wTHqB` | UNKNOWN | `LOW` | 3 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x55a50` | `0x45a50` | `i5V.(*YMbT3l).c_f7b5n.gowrap2` | UNKNOWN | `LOW` | 3 | 1 | `.func12` |
| `0x55af0` | `0x45af0` | `b5n.gowrap1` | UNKNOWN | `LOW` | 1 | 5 | `.(*cunxvAjr).w_2fNT, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, PhLv.(*BSsluADyuaT).re5I39ze` |
| `0x55c50` | `0x45c50` | `Port` | UNKNOWN | `LOW` | 0 | 38 | `alTo, 1ZBAw-fm, b5n.gowrap1` |
| `0x561d0` | `0x461d0` | `4i5V.(*YMbT3l).nIXyKDwRRthU` | UNKNOWN | `LOW` | 1 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, SwY3L.iYPHrB4Qx` |
| `0x56290` | `0x46290` | `T3l).h0eCh8AiGxYh` | UNKNOWN | `LOW` | 2 | 3 | `4i5V.(*YMbT3l).nIXyKDwRRthU, eam, .func12` |
| `0x56300` | `0x46300` | `l).uOKkKLBBJ84d` | UNKNOWN | `LOW` | 2 | 11 | `func1, hhHS85O.wQ6e481ZBAw-fm, T3l).h0eCh8AiGxYh` |
| `0x56560` | `0x46560` | `MbT3l).LookupAddr` | UNKNOWN | `LOW` | 1 | 2 | `.UnmarshalCompressed, .func12` |
| `0x565d0` | `0x465d0` | `z4i5V.(*YMbT3l).bW2b6Kw` | UNKNOWN | `LOW` | 2 | 2 | `).Params, .func12` |
| `0x56630` | `0x46630` | `Pz4i5V.sAeZmU` | UNKNOWN | `LOW` | 12 | 13 | `QmBRaybD).MarshalSize, CtiT, _).hup5blt59hNV` |
| `0x568d0` | `0x468d0` | `4i5V.rmFyLW` | UNKNOWN | `LOW` | 1 | 3 | `k9tYis59M, Pz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], .func12` |
| `0x569b0` | `0x469b0` | `V.(*YMbT3l).pcPuvCGTGV` | UNKNOWN | `LOW` | 3 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, t2q.Size` |
| `0x56d40` | `0x46d40` | `bT3l).vYtEfu` | UNKNOWN | `LOW` | 1 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x56e60` | `0x46e60` | `CtiT` | UNKNOWN | `LOW` | 29 | 5 | `tgJfPz.GcNk7f, .func12.1.1, 20Z.tcu6kPP7` |
| `0x571b0` | `0x471b0` | `6k` | UNKNOWN | `LOW` | 1 | 7 | `6SE).MatchEmptyWidth, cHKW1j5, kse52mwumii.Xtk_Ta_AUS8` |
| `0x571f0` | `0x471f0` | `z4i5V.(*icpajYcj).Read` | UNKNOWN | `LOW` | 0 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x57270` | `0x47270` | `cpajYcj).Close` | UNKNOWN | `LOW` | 9 | 4 | `CtiT, eam, nmarshal` |
| `0x57310` | `0x47310` | `i5V.(*icpajYcj).SetReadDeadline` | UNKNOWN | `LOW` | 1 | 2 | `eam, .func12` |
| `0x573f0` | `0x473f0` | `Ycj).SetReadBuffer` | UNKNOWN | `LOW` | 1 | 3 | `6SE).MatchEmptyWidth, eam, .func12` |
| `0x574e0` | `0x474e0` | `4i5V.onlt3vXM.Error` | UNKNOWN | `LOW` | 2 | 5 | `uDeMp8Izpi_.CloseWrite, .UnmarshalCompressed, tgJfPz.GcNk7f` |
| `0x575e0` | `0x475e0` | `FanmdO8dYdH).Error` | UNKNOWN | `LOW` | 0 | 2 | `*bAujxOKO_).Error, cHKW1j5` |
| `0x57640` | `0x47640` | `*GFanmdO8dYdH).Temporary` | UNKNOWN | `LOW` | 2 | 4 | `tgJfPz.GcNk7f, ).Params, XPz4i5V.(*uDeMp8Izpi_).File` |
| `0x57740` | `0x47740` | `U05KcRRRTrFW).Timeout` | UNKNOWN | `LOW` | 0 | 2 | `i5V.(*bAujxOKO_).Is, cHKW1j5` |
| `0x57790` | `0x47790` | `i5V.(*VMXiXAZ).Error` | UNKNOWN | `LOW` | 2 | 3 | `uDeMp8Izpi_.CloseWrite, 4i5V.onlt3vXM.Error, .func12` |
| `0x57800` | `0x47800` | `5V.ZL3KSP9Oi.Error` | UNKNOWN | `LOW` | 2 | 3 | `*GFanmdO8dYdH).Temporary, XPz4i5V.(*uDeMp8Izpi_).File, .func12` |
| `0x57870` | `0x47870` | `*bAujxOKO_).Error` | UNKNOWN | `LOW` | 3 | 14 | `cpajYcj).Close, QmBRaybD).MarshalSize, eader` |
| `0x57e00` | `0x47e00` | `i5V.(*bAujxOKO_).Is` | UNKNOWN | `LOW` | 4 | 14 | `i5V.init.EIYgRcen.func7.1, Pz4i5V.(*Gf_aZ0Zk).File, hhHS85O.wQ6e481ZBAw-fm` |
| `0x58120` | `0x48120` | `ESGPm1).Temporary` | UNKNOWN | `LOW` | 0 | 2 | `9F5Zj, ` |
| `0x581a0` | `0x481a0` | `9F5Zj` | UNKNOWN | `LOW` | 1 | 8 | `NWVI.(*A0pGSa).Mult32, XPz4i5V.(*ke34Dwh).lDryR_cxCM, ` |
| `0x582b0` | `0x482b0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x58310` | `0x48310` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x58610` | `0x48610` | `4i5V.gARftz0v7` | UNKNOWN | `LOW` | 3 | 11 | `hhHS85O.wQ6e481ZBAw-fm, .UnmarshalCompressed, Pz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` |
| `0x58b70` | `0x48b70` | `V.(*UsaK2C9O).Read` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, NChRP_).ReadByte, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x58c70` | `0x48c70` | `XPz4i5V.(*mDpfdzqKmEF).lcyN8Ohw5B9` | UNKNOWN | `LOW` | 2 | 14 | `od, ape.*uint8], hhHS85O.wQ6e481ZBAw-fm` |
| `0x58f50` | `0x48f50` | `qKmEF).lcyN8Ohw5B9.deferwrap1` | UNKNOWN | `LOW` | 0 | 2 | `mapH.(*QcMnoAPhGe1).nPxKD4G.func1, cHKW1j5` |
| `0x58fa0` | `0x48fa0` | `WQ0` | UNKNOWN | `LOW` | 2 | 12 | `etWriteDeadline, .(*ZWj4kZX).SetUint, orHJ20Z.init.EIYgRcen.func11.1.1` |
| `0x591b0` | `0x491b0` | `bXPz4i5V.vabEXmnK` | UNKNOWN | `LOW` | 1 | 2 | `DWTK.kVyQ82JOayK.func1, .func12` |
| `0x59260` | `0x49260` | `DWTK.kVyQ82JOayK.func1` | UNKNOWN | `LOW` | 1 | 7 | `XPz4i5V.(*mDpfdzqKmEF).lcyN8Ohw5B9, etDeadline, CtiT` |
| `0x59410` | `0x49410` | `mjbVH0I7c).uF12Ibgdq` | UNKNOWN | `LOW` | 2 | 11 | `QmBRaybD).MarshalSize, CtiT, dC2.M7XB_IfPUd` |
| `0x59690` | `0x49690` | `A8` | UNKNOWN | `LOW` | 2 | 2 | `k9tYis59M, 20Z.tcu6kPP7` |
| `0x597b0` | `0x497b0` | `dGaLpqVl6` | UNKNOWN | `LOW` | 1 | 1 | `A8` |
| `0x59880` | `0x49880` | `XPz4i5V.ghH9sBg` | UNKNOWN | `LOW` | 2 | 1 | `A8` |
| `0x59910` | `0x49910` | `1` | UNKNOWN | `LOW` | 25 | 39 | `kimj_, QmBRaybD).MarshalSize, *JZdvaRJ).MarshalSize` |
| `0x59aa0` | `0x49aa0` | `z4i5V.(*apISfGa).Read` | UNKNOWN | `LOW` | 2 | 6 | `od, Compressed, ).SetNoDelay` |
| `0x59b80` | `0x49b80` | `*apISfGa).Network` | UNKNOWN | `LOW` | 2 | 2 | `1, .func12` |
| `0x59ca0` | `0x49ca0` | `Pz4i5V.k_QobMJaaT` | UNKNOWN | `LOW` | 0 | 6 | `hhHS85O.wQ6e481ZBAw-fm, rc[go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x59dc0` | `0x49dc0` | `y5AupxR7N` | UNKNOWN | `LOW` | 4 | 7 | `hhHS85O.wQ6e481ZBAw-fm, i5V.(*ISwY3L).DefaultMask, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x59ec0` | `0x49ec0` | `nvNIgV` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x59ed0` | `0x49ed0` | `heejkbo8).k9azrvO` | UNKNOWN | `LOW` | 4 | 8 | `hhHS85O.wQ6e481ZBAw-fm, .IsMulticast, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x5a1a0` | `0x4a1a0` | `.ub8nc3aV0kl` | UNKNOWN | `LOW` | 4 | 8 | `heejkbo8).k9azrvO, hhHS85O.wQ6e481ZBAw-fm, NChRP_).ReadByte` |
| `0x5a610` | `0x4a610` | `Ooyo` | UNKNOWN | `LOW` | 2 | 13 | `5V.kmkzOSevZ, .ub8nc3aV0kl, w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` |
| `0x5a830` | `0x4a830` | `Pz4i5V.uQviHbu_xu` | UNKNOWN | `LOW` | 1 | 6 | `w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], 5V.kmkzOSevZ, NChRP_).ReadByte` |
| `0x5a8d0` | `0x4a8d0` | `8IFn).Network` | UNKNOWN | `LOW` | 1 | 8 | `5V.kmkzOSevZ, hhHS85O.wQ6e481ZBAw-fm, .func12.1.1` |
| `0x5aa10` | `0x4aa10` | `*EJfmL1P).SyscallConn` | UNKNOWN | `LOW` | 4 | 8 | `ZztHL)._avZ_Q7jcT, .UnmarshalCompressed, CtiT` |
| `0x5abf0` | `0x4abf0` | `5V.(*EJfmL1P).CloseRead` | UNKNOWN | `LOW` | 1 | 35 | `z4i5V.(*YMbT3l).bW2b6Kw, V.(*UsaK2C9O).Read, 2Rzf5wkmWe[go.shape.[]int32,go.shape.int32]` |
| `0x5c140` | `0x4c140` | `mL1P).CloseWrite` | UNKNOWN | `LOW` | 0 | 3 | `i5V.init.EIYgRcen.func7.1, Pz4i5V.(*Gf_aZ0Zk).File, .func12` |
| `0x5c2b0` | `0x4c2b0` | `inger` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 5 | `2Rzf5wkmWe[go.shape.[]int32,go.shape.int32], LocalAddr, nmarshal` |
| `0x5c700` | `0x4c700` | `V.(*EJfmL1P).SetNoDelay` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, *ISwY3L).MarshalText, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x5c870` | `0x4c870` | `.Cj0rprKNs5` | UNKNOWN | `LOW` | 1 | 2 | `nmarshal, .func12` |
| `0x5c980` | `0x4c980` | `(*Gf_aZ0Zk).vTQS77dB3UiY` | UNKNOWN | `LOW` | 1 | 7 | `hhHS85O.wQ6e481ZBAw-fm, *ISwY3L).MarshalText, inary` |
| `0x5cbc0` | `0x4cbc0` | `eptTCP` | UNKNOWN | `LOW` | 3 | 3 | `i5V.C9QITNV4ixi, WI, .func12` |
| `0x5cc30` | `0x4cc30` | `iJJwlO4` | UNKNOWN | `LOW` | 1 | 3 | `WI, eam, .func12` |
| `0x5cce0` | `0x4cce0` | `Pz4i5V.(*Gf_aZ0Zk).File` | UNKNOWN | `LOW` | 10 | 8 | `QmBRaybD).MarshalSize, CtiT, _).hup5blt59hNV` |
| `0x5d0e0` | `0x4d0e0` | `qSbCBjtu` | UNKNOWN | `LOW` | 7 | 12 | `Ooyo, *EJfmL1P).SyscallConn, Pz4i5V.uQviHbu_xu` |
| `0x5d350` | `0x4d350` | `a2` | UNKNOWN | `LOW` | 0 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x5d3a0` | `0x4d3a0` | `gCTB` | UNKNOWN | `LOW` | 0 | 10 | `QmBRaybD).MarshalSize, 77ZY9, rshal` |
| `0x5d670` | `0x4d670` | `hbXPz4i5V.(*u8EpLV).vE6v0Cgfuuwo.func1` | UNKNOWN | `LOW` | 4 | 15 | `QmBRaybD).MarshalSize, dC2.(*WbMJSfJ).Unmarshal, CtiT` |
| `0x5d990` | `0x4d990` | `N` | UNKNOWN | `LOW` | 1 | 3 | `hbXPz4i5V.(*u8EpLV).vE6v0Cgfuuwo.func1, .func12, dlUslrFHV.(*kDHjay8BxfB).Write` |
| `0x5d9d0` | `0x4d9d0` | `L1P).SetKeepAliveConfig` | UNKNOWN | `LOW` | 0 | 3 | `OU7NWVI.aXHDgGZZvF, hbXPz4i5V.(*u8EpLV).vE6v0Cgfuuwo.func1, .func12` |
| `0x5da50` | `0x4da50` | `z4i5V.fzyyQtNjDN` | UNKNOWN | `LOW` | 0 | 2 | `hbXPz4i5V.(*u8EpLV).vE6v0Cgfuuwo.func1, .func12` |
| `0x5da90` | `0x4da90` | `3jvb5lTw).Network` | UNKNOWN | `LOW` | 1 | 15 | `CM, i5V.(*icpajYcj).SetReadDeadline, QmBRaybD).MarshalSize` |
| `0x5dd70` | `0x4dd70` | `hbXPz4i5V.kmkzOSevZ.Network` | UNKNOWN | `LOW` | 0 | 6 | `QmBRaybD).MarshalSize, dC2.(*WbMJSfJ).Unmarshal, CtiT` |
| `0x5ded0` | `0x4ded0` | `_d).ReadFromUDP` | UNKNOWN | `LOW` | 0 | 4 | `QmBRaybD).MarshalSize, nmarshal, tQ0xKHZgC5j.init.func1` |
| `0x5dfb0` | `0x4dfb0` | `tTC_d).ReadFrom` | UNKNOWN | `LOW` | 0 | 3 | `ReadMsgUDP, qSbCBjtu, .func12` |
| `0x5dff0` | `0x4dff0` | `ReadMsgUDP` | UNKNOWN | `LOW` | 1 | 13 | `CtiT, YT47X.String, ).Params` |
| `0x5e320` | `0x4e320` | `oUDP` | UNKNOWN | `LOW` | 2 | 1 | `eam` |
| `0x5e390` | `0x4e390` | `Pz4i5V.(*Lb1Wr6XtTC_d).WriteTo` | UNKNOWN | `LOW` | 1 | 4 | `QmBRaybD).MarshalSize, oUDP, CtiT` |
| `0x5e5e0` | `0x4e5e0` | `tTC_d).WriteMsgUDPAddrPort` | UNKNOWN | `LOW` | 0 | 2 | `LPGP__.DestinationSSRC, cHKW1j5` |
| `0x5e6a0` | `0x4e6a0` | `4i5V.zqbZM9wZ` | UNKNOWN | `LOW` | 0 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x5e750` | `0x4e750` | `qP3jvb5lTw).knE17ria2` | UNKNOWN | `LOW` | 0 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x5e800` | `0x4e800` | `4i5V.(*Lb1Wr6XtTC_d).fXQhQBBl` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, NChRP_).ReadByte, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x5e890` | `0x4e890` | `i5V.(*Lb1Wr6XtTC_d).hf9RoG` | UNKNOWN | `LOW` | 0 | 7 | `hhHS85O.wQ6e481ZBAw-fm, QmBRaybD).MarshalSize, .Header` |
| `0x5eae0` | `0x4eae0` | `.(*Lb1Wr6XtTC_d).firDkDJYzj` | UNKNOWN | `LOW` | 0 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x5ebc0` | `0x4ebc0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x5eca0` | `0x4eca0` | `*u8EpLV).kFFRY7SAjO_6.func1` | UNKNOWN | `LOW` | 0 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x5ed70` | `0x4ed70` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x5ee50` | `0x4ee50` | `bXPz4i5V.(*PavbnH).hdZoaa` | UNKNOWN | `LOW` | 0 | 3 | `wdC2.(*J4eijR).PacketList.func1, nSSRC, cHKW1j5` |
| `0x5eeb0` | `0x4eeb0` | `Pz4i5V.(*NYfrrNOGp).CloseRead` | UNKNOWN | `LOW` | 0 | 2 | `aO3lL0ytR.(*lJ_CaZZztHL).Done.deferwrap1, cHKW1j5` |
| `0x5eef0` | `0x4eef0` | `hbXPz4i5V.(*NYfrrNOGp).ReadFromUnix` | UNKNOWN | `LOW` | 1 | 4 | `QmBRaybD).MarshalSize, tgJfPz.GcNk7f, .dSMl4sq_Ui[go.shape.*uint8]` |
| `0x5f130` | `0x4f130` | `p).ReadMsgUnix` | UNKNOWN | `LOW` | 0 | 2 | `3UiY, cHKW1j5` |
| `0x5f180` | `0x4f180` | `vbnH).oeV1ypu3` | UNKNOWN | `LOW` | 1 | 1 | `tgJfPz.GcNk7f` |
| `0x5f200` | `0x4f200` | `i5V.(*YaahJAwWdIk).SyscallConn` | UNKNOWN | `LOW` | 0 | 3 | `.Header, lSize, cHKW1j5` |
| `0x5f260` | `0x4f260` | `3UiY` | UNKNOWN | `LOW` | 1 | 6 | `hhHS85O.wQ6e481ZBAw-fm, .IsMulticast, NChRP_).ReadByte` |
| `0x5f320` | `0x4f320` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x5f620` | `0x4f620` | `etDeadline` | UNKNOWN | `LOW` | 4 | 3 | `er, tgJfPz.GcNk7f, .func12` |
| `0x5f6e0` | `0x4f6e0` | `rYxO5oY4EP` | UNKNOWN | `LOW` | 0 | 2 | `.(*FlCj9pZvT).Error, cHKW1j5` |
| `0x5f730` | `0x4f730` | `EZsdym0` | UNKNOWN | `LOW` | 107 | 2 | `tgJfPz.GcNk7f, .func12` |
| `0x5f790` | `0x4f790` | `p).k45foJQqSg` | UNKNOWN | `LOW` | 0 | 4 | `QO, Y3L).To16, WI` |
| `0x5f800` | `0x4f800` | `QO` | UNKNOWN | `LOW` | 2 | 13 | `bool }]).Store, z4i5V.(*YaahJAwWdIk).SetUnlinkOnClose, etDeadline` |
| `0x5fd50` | `0x4fd50` | `kamlWNZ0` | UNKNOWN | `LOW` | 1 | 9 | `WPs1, ne, ZqlIeq[go.shape.int32]` |
| `0x5ff70` | `0x4ff70` | `.ayV54N` | UNKNOWN | `LOW` | 1 | 5 | `mapH.(*QcMnoAPhGe1).nPxKD4G.func1, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x601a0` | `0x501a0` | `z4i5V.(*YaahJAwWdIk).SetUnlinkOnClose` | UNKNOWN | `LOW` | 1 | 4 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, hhHS85O.wQ6e481ZBAw-fm, tgJfPz.GcNk7f` |
| `0x60380` | `0x50380` | `sqDkAj_3QE).dGzMCJiTgB4.func1` | UNKNOWN | `LOW` | 0 | 2 | `.(*FlCj9pZvT).Error, cHKW1j5` |
| `0x603d0` | `0x503d0` | `jRN` | UNKNOWN | `LOW` | 0 | 2 | `mapH.(*QcMnoAPhGe1).nPxKD4G.func1, cHKW1j5` |
| `0x60420` | `0x50420` | `jYcj).o3Eao_wGk` | UNKNOWN | `LOW` | 1 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x605c0` | `0x505c0` | `Kr2TJo.fjzI9oE9i.func1` | UNKNOWN | `LOW` | 1 | 2 | `*apISfGa).Network, ma.(*MydupPsvCWhi).SetExtension` |
| `0x60640` | `0x50640` | `T3l).c_f7b5n.func3` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x60680` | `0x50680` | `jkbo8).wNv3ibD.(*mheejkbo8).cQjpP4oK.func1` | UNKNOWN | `LOW` | 3 | 1 | `tgJfPz.GcNk7f` |
| `0x606f0` | `0x506f0` | `.(*mheejkbo8).cQjpP4oK.func1` | UNKNOWN | `LOW` | 1 | 3 | `eam, .func12, .(*mheejkbo8).cQjpP4oK.func1` |
| `0x60730` | `0x50730` | `.(*mheejkbo8).cQjpP4oK.func1` | UNKNOWN | `LOW` | 1 | 3 | `eam, .func12, .(*mheejkbo8).cQjpP4oK.func1` |
| `0x60770` | `0x50770` | `kbo8).cQjpP4oK.func2` | UNKNOWN | `LOW` | 1 | 2 | `kbo8).cQjpP4oK.func2, .func12` |
| `0x607b0` | `0x507b0` | `jpP4oK.func3` | UNKNOWN | `LOW` | 1 | 2 | `jpP4oK.func3, .func12` |
| `0x607f0` | `0x507f0` | `unc4` | UNKNOWN | `LOW` | 1 | 11 | `unc4, .func12, ) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x60830` | `0x50830` | `Pz4i5V.(*mheejkbo8).ayV54N.(*mheejkbo8).cQjpP4oK.func1` | UNKNOWN | `LOW` | 1 | 2 | `Pz4i5V.(*mheejkbo8).ayV54N.(*mheejkbo8).cQjpP4oK.func1, .func12` |
| `0x60870` | `0x50870` | `kbo8).ayV54N.(*mheejkbo8).cQjpP4oK.func2` | UNKNOWN | `LOW` | 1 | 2 | `kbo8).ayV54N.(*mheejkbo8).cQjpP4oK.func2, .func12` |
| `0x608b0` | `0x508b0` | `oHchGZM` | UNKNOWN | `LOW` | 1 | 2 | `oHchGZM, .func12` |
| `0x608f0` | `0x508f0` | `.hbXPz4i5V.PavbnH` | UNKNOWN | `LOW` | 1 | 8 | `indSubmatch, KcotjIqdR.(*Laxp2QOnMe2a).FindAllString, ; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x60cc0` | `0x50cc0` | `hbXPz4i5V.UZ5DG6R8U` | UNKNOWN | `LOW` | 1 | 7 | `.JgiPo3aUOjR]).ScalarBaseMult, , .shape.interface {}]).CompareAndDelete` |
| `0x60e70` | `0x50e70` | `Pz4i5V.WHL6oI983` | UNKNOWN | `LOW` | 1 | 9 | `.(*hU7W8yU6aQ).g6mJ7e, B4Uc, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap` |
| `0x610d0` | `0x510d0` | `jN0LXaQcmz7[go.shape.*uint8]` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 0 | 6 | `abi.Type,go.shape.interface {}]).CompareAndSwap, MnoAPhGe1).Start.func1, 81ZBAw-fm` |
| `0x61140` | `0x51140` | `]` | UNKNOWN | `LOW` | 7 | 22 | `.func12.1.1, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x61220` | `0x51220` | `fhK.q4UKcORW2AZ[go.shape.*uint8]` | UNKNOWN | `LOW` | 2 | 25 | `QmBRaybD).MarshalSize, dC2.GxhnYyL_G.DestinationSSRC, .func12.1.1` |
| `0x61be0` | `0x51be0` | `ape.*uint8]` | UNKNOWN | `LOW` | 9 | 7 | `, .JgiPo3aUOjR]).ScalarBaseMult, .func12` |
| `0x61cd0` | `0x51cd0` | `.dSMl4sq_Ui[go.shape.*uint8]` | UNKNOWN | `LOW` | 2 | 1 | `tgJfPz.GcNk7f` |
| `0x61d60` | `0x51d60` | `o.shape.*uint8]` | UNKNOWN | `LOW` | 0 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x61e10` | `0x51e10` | `5V.kmkzOSevZ` | UNKNOWN | `LOW` | 6 | 4 | `QmBRaybD).MarshalSize, nYyL_G.Marshal, 4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` |
| `0x61ef0` | `0x51ef0` | `4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 1 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, t2q.Size` |
| `0x62000` | `0x52000` | `w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 4 | 4 | `hhHS85O.wQ6e481ZBAw-fm, rc[go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x62090` | `0x52090` | `rc[go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 5 | 13 | `V.fEj8wTHqB, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, bool }]).Store` |
| `0x62410` | `0x52410` | `i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 0 | 9 | `YT47X.String, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x62530` | `0x52530` | `.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 0 | 17 | `hhHS85O.wQ6e481ZBAw-fm, rc[go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x62a60` | `0x52a60` | `Pz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 1 | 8 | `hhHS85O.wQ6e481ZBAw-fm, i5V.hN4TcGifv }], .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x62e40` | `0x52e40` | `Pz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 3 | 2 | `i5V.hN4TcGifv }], .func12` |
| `0x62ee0` | `0x52ee0` | `i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 3 | 2 | `l; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load, .func12` |
| `0x62ff0` | `0x52ff0` | `pMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 2 | 13 | `.func12.1.1, hhHS85O.wQ6e481ZBAw-fm, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x63800` | `0x53800` | `_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 1 | 3 | `dr, EZsdym0, .func12` |
| `0x63860` | `0x53860` | `6VfE[go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 0 | 8 | `.UnmarshalCompressed, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x639f0` | `0x539f0` | `z4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x63b70` | `0x53b70` | `Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }]` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, heejkbo8).k9azrvO` |
| `0x63d00` | `0x53d00` | `i5V.(*ISwY3L).DefaultMask` | UNKNOWN | `LOW` | 1 | 2 | `rc[go.shape.struct { hbXPz4i5V.pmsjGu92pk hbXPz4i5V.YLYtpMxe_SvW; hbXPz4i5V.mUA6lVDi6s1 hbXPz4i5V.hN4TcGifv; hbXPz4i5V.w80SaW9_Z AcDK_Fy.J9R_6Iy_9rFh; hbXPz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], .func12` |
| `0x63d70` | `0x53d70` | `hbXPz4i5V.(*ISwY3L).IsInterfaceLocalMulticast` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 2 | `pqx).ListenPacket, .func12` |
| `0x63ee0` | `0x53ee0` | `bXPz4i5V.(*ISwY3L).IsLinkLocalUnicast` | UNKNOWN | `LOW` | 4 | 5 | `.func12.1.1, eam, nmarshal` |
| `0x64120` | `0x54120` | `.IsMulticast` | UNKNOWN | `LOW` | 7 | 5 | `.func12.1.1, pe,interface {}], nmarshal` |
| `0x642e0` | `0x542e0` | `*ISwY3L).MarshalText` | UNKNOWN | `LOW` | 5 | 2 | `.IsMulticast, .func12` |
| `0x64350` | `0x54350` | `Y3L).To16` | UNKNOWN | `LOW` | 3 | 2 | `ing, .func12` |
| `0x64460` | `0x54460` | `ing` | UNKNOWN | `LOW` | 1 | 6 | `, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x64640` | `0x54640` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x646c0` | `0x546c0` | `XPz4i5V.hguC61sqr.Err` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x64850` | `0x54850` | `*onlt3vXM).Is` | UNKNOWN | `LOW` | 1 | 2 | `k9tYis59M, .func12` |
| `0x64a10` | `0x54a10` | `LocalAddr` | UNKNOWN | `LOW` | 1 | 3 | `*onlt3vXM).Is, eam, .func12` |
| `0x64b00` | `0x54b00` | `.SetDeadline` | UNKNOWN | `LOW` | 1 | 12 | `.func12.1.1, CM, G.(*cunxvAjr).w3bZX5dLo` |
| `0x64f20` | `0x54f20` | `Pz4i5V.(*EJfmL1P).SetWriteBuffer` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 2 | `pqx).ListenPacket, .func12` |
| `0x64ff0` | `0x54ff0` | `1P).Write` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 2 | `pqx).ListenPacket, .func12` |
| `0x650f0` | `0x550f0` | `.File` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 4 | 14 | `1P).Write, Pz4i5V.(*EJfmL1P).SetWriteBuffer, 3vJC5GCZyE).Size` |
| `0x65690` | `0x55690` | `teAddr` | UNKNOWN | `LOW` | 3 | 5 | `YlgJgI).SetReadDeadline, eam, .func12` |
| `0x65700` | `0x55700` | `YlgJgI).SetReadDeadline` | UNKNOWN | `LOW` | 2 | 2 | `NChRP_).ReadByte, .func12` |
| `0x65790` | `0x55790` | `eDeadline` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 11 | `eByte, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve, eam` |
| `0x65d80` | `0x55d80` | `TC_d).Close` | UNKNOWN | `LOW` | 1 | 13 | `hhHS85O.wQ6e481ZBAw-fm, bool }]).Store, 34Dwh).v_YAYAghVIR` |
| `0x660d0` | `0x560d0` | `alAddr` | UNKNOWN | `LOW` | 2 | 9 | `.func12.1.1, .func12, X[*JYT1bAJ.JgiPo3aUOjR]).Double` |
| `0x661c0` | `0x561c0` | `b1Wr6XtTC_d).SetDeadline` | UNKNOWN | `LOW` | 2 | 5 | `hhHS85O.wQ6e481ZBAw-fm, bool }]).Store, [go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.1` |
| `0x66280` | `0x56280` | `5V.(*Lb1Wr6XtTC_d).SetReadDeadline` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, bool }]).Store, gLI7afn.sSMWWX17HF.JyjLYF7KXE[go.shape.func(*g1gLI7afn.hnNChRP_, reflect.V8CvLYzyC, g1gLI7afn.b8iVIvuIKM)].func3.1.1` |
| `0x66300` | `0x56300` | `fer` | UNKNOWN | `LOW` | 2 | 11 | `b1Wr6XtTC_d).SetDeadline, 5V.(*Lb1Wr6XtTC_d).SetReadDeadline, ).udJ65d50YY4` |
| `0x663d0` | `0x563d0` | `.(*Lb1Wr6XtTC_d).o3Eao_wGk` | UNKNOWN | `LOW` | 1 | 2 | `k9tYis59M, .func12` |
| `0x66470` | `0x56470` | `z4i5V.(*NYfrrNOGp).LocalAddr` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .func12.1.1, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x66500` | `0x56500` | `dr` | UNKNOWN | `LOW` | 3 | 4 | `er, .UnmarshalCompressed, ` |
| `0x66620` | `0x56620` | `YfrrNOGp).SetReadDeadline` | UNKNOWN | `LOW` | 2 | 2 | `EXo).Read, .func12` |
| `0x666e0` | `0x566e0` | `etWriteDeadline` | UNKNOWN | `LOW` | 6 | 1 | `JYT1bAJ.(*TCYzSpw).Add` |
| `0x66780` | `0x56780` | `(*ZL3KSP9Oi).Error` | UNKNOWN | `LOW` | 1 | 3 | `.UnmarshalCompressed, Pz4i5V.xDXndpy2 hbXPz4i5V.hN4TcGifv }], .func12` |
| `0x667f0` | `0x567f0` | `4i5V.(*hpuMRcNgd4l).ReadFrom` | UNKNOWN | `LOW` | 1 | 5 | `WPs1, .UnmarshalCompressed, .(*cunxvAjr).w_2fNT` |
| `0x66920` | `0x56920` | `vEXo).Close` | UNKNOWN | `LOW` | 1 | 5 | `WPs1, .UnmarshalCompressed, .v5SQds4Q` |
| `0x66a70` | `0x56a70` | `ad` | UNKNOWN | `LOW` | 1 | 10 | `eam, .func12, 2t` |
| `0x66ce0` | `0x56ce0` | `ite` | UNKNOWN | `LOW` | 0 | 4 | `ad, Z1g.(*txbdkX[*JYT1bAJ.TCYzSpw]).Params, eam` |
| `0x67140` | `0x57140` | `vEXo.LocalAddr` | UNKNOWN | `LOW` | 1 | 2 | `XKvEXo.SetDeadline, .func12` |
| `0x67290` | `0x57290` | `5V.(*zMqXKvEXo).MultipathTCP` | UNKNOWN | `LOW` | 1 | 6 | `er, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .UnmarshalCompressed` |
| `0x67340` | `0x57340` | `EXo).Read` | UNKNOWN | `LOW` | 1 | 4 | `ey.(*E_o3jWSJ).Debug, XKvEXo.SetDeadline, flect.F5Cl4yr[go.shape.interface { IsZero() bool }]` |
| `0x67470` | `0x57470` | `XKvEXo.SetDeadline` | UNKNOWN | `LOW` | 2 | 9 | `89O0.(*gxe_j_u89O0).gcYExTiArY, flect.F5Cl4yr[go.shape.interface { IsZero() bool }], g1gLI7afn.(*OeNad6bZ).Error` |
| `0x67830` | `0x57830` | `bXPz4i5V.(*zMqXKvEXo).SetKeepAlive` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x67870` | `0x57870` | `qXKvEXo).SetKeepAliveConfig` | UNKNOWN | `LOW` | 2 | 1 | `(*txbdkX[*JYT1bAJ.GUY8D0aEy]).Params` |
| `0x678a0` | `0x578a0` | `od` | UNKNOWN | `LOW` | 2 | 2 | `tgJfPz.GcNk7f, .func12` |
| `0x67950` | `0x57950` | `MqXKvEXo).SetLinger` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, n.(*hnNChRP_).ReadRune` |
| `0x67a00` | `0x57a00` | `).SetNoDelay` | UNKNOWN | `LOW` | 2 | 5 | `hhHS85O.wQ6e481ZBAw-fm, NChRP_).ReadByte, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x67b30` | `0x57b30` | `z4i5V.zMqXKvEXo.SetReadDeadline` | UNKNOWN | `LOW` | 1 | 3 | `hhHS85O.wQ6e481ZBAw-fm, nmarshal, .func12` |
| `0x67c00` | `0x57c00` | `Xo.SetWriteBuffer` | UNKNOWN | `LOW` | 3 | 3 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, nmarshal, .func12` |
| `0x67ce0` | `0x57ce0` | `line` | UNKNOWN | `LOW` | 0 | 2 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x67d90` | `0x57d90` | `*zMqXKvEXo).SyscallConn` | UNKNOWN | `LOW` | 81 | 26 | `.func12.1.1, bool }]).Store, KAN61n).pvqcm0` |
| `0x68ea0` | `0x58ea0` | `.zMqXKvEXo.WriteTo` | UNKNOWN | `LOW` | 0 | 2 | `Xo.SetWriteBuffer, cHKW1j5` |
| `0x68ee0` | `0x58ee0` | `KvEXo.o3Eao_wGk` | UNKNOWN | `LOW` | 0 | 2 | `Xo.SetWriteBuffer, cHKW1j5` |
| `0x68f20` | `0x58f20` | `wazZan).WriteTo` | UNKNOWN | `LOW` | 3 | 3 | `.func12.1.1, tgJfPz.GcNk7f, .func12` |
| `0x68fb0` | `0x58fb0` | `Mp8Izpi_.CloseRead` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x68ff0` | `0x58ff0` | `uDeMp8Izpi_.CloseWrite` | UNKNOWN | `LOW` | 11 | 10 | `6G1wg0, .func12.1.1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x69380` | `0x59380` | `XPz4i5V.(*uDeMp8Izpi_).File` | UNKNOWN | `LOW` | 9 | 8 | `hhHS85O.wQ6e481ZBAw-fm, V.uDeMp8Izpi_.Read, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x69620` | `0x59620` | `alAddr` | UNKNOWN | `LOW` | 2 | 9 | `.func12.1.1, .func12, X[*JYT1bAJ.JgiPo3aUOjR]).Double` |
| `0x699f0` | `0x599f0` | `V.uDeMp8Izpi_.Read` | UNKNOWN | `LOW` | 1 | 7 | `.func12.1.1, .UnmarshalCompressed, ).Params` |
| `0x69d30` | `0x59d30` | `V.(*uDeMp8Izpi_).ReadFrom` | UNKNOWN | `LOW` | 2 | 4 | `X[*JYT1bAJ.JgiPo3aUOjR]).Double, .UnmarshalCompressed, eam` |
| `0x69e80` | `0x59e80` | `teAddr` | UNKNOWN | `LOW` | 3 | 5 | `YlgJgI).SetReadDeadline, eam, .func12` |
| `0x69fd0` | `0x59fd0` | `uDeMp8Izpi_.SetKeepAlive` | UNKNOWN | `LOW` | 6 | 3 | `3vJC5GCZyE).Size, 4CM, .func12` |
| `0x6a100` | `0x5a100` | `KeepAliveConfig` | UNKNOWN | `LOW` | 1 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x6a8b0` | `0x5a8b0` | `pAlivePeriod` | UNKNOWN | `LOW` | 1 | 2 | `5V.(*mheejkbo8).Close, .func12` |
| `0x6a9a0` | `0x5a9a0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x6aa00` | `0x5aa00` | `zpi_).SetNoDelay` | UNKNOWN | `LOW` | 1 | 4 | `Ia, ct { hbXPz4i5V.t168Wlq7 []string; hbXPz4i5V.dWtrpejzqf []string; hbXPz4i5V.hMx5puF2VMG int; hbXPz4i5V.sSSkltnfCZ eFuxzMSJ.A3uOOsj; hbXPz4i5V.iEWfcYh int; hbXPz4i5V.j6arB0ou bool; hbXPz4i5V.nWkHMO bool; hbXPz4i5V.vz0uLMSA27c []string; hbXPz4i5V.hv7mKOEyckF error; hbXPz4i5V.pMzMLqn eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Load, nc1` |
| `0x6ac10` | `0x5ac10` | `fer` | UNKNOWN | `LOW` | 2 | 11 | `b1Wr6XtTC_d).SetDeadline, 5V.(*Lb1Wr6XtTC_d).SetReadDeadline, ).udJ65d50YY4` |
| `0x6ad70` | `0x5ad70` | `ne` | UNKNOWN | `LOW` | 85 | 10 | `WPs1, indSubmatch, KcotjIqdR.(*Laxp2QOnMe2a).FindAllString` |
| `0x6add0` | `0x5add0` | `.SetWriteBuffer` | UNKNOWN | `LOW` | 0 | 3 | `q[go.shape.string], evZ).MarshalText, .func12` |
| `0x6ae30` | `0x5ae30` | `8Izpi_).SetWriteDeadline` | UNKNOWN | `LOW` | 1 | 3 | `XPz4i5V.BNOfD2CCJ, , .func12` |
| `0x6af40` | `0x5af40` | `allConn` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x6b020` | `0x5b020` | `.o3Eao_wGk` | UNKNOWN | `LOW` | 0 | 12 | `V.Te158rafFSOp, allConn, X[*JYT1bAJ.TCYzSpw]).ScalarBaseMult` |
| `0x6b240` | `0x5b240` | `N16T).Network` | UNKNOWN | `LOW` | 1 | 2 | `8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], alarMult` |
| `0x6b300` | `0x5b300` | `.Addr` | UNKNOWN | `LOW` | 1 | 1 | `8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x6b350` | `0x5b350` | `zOSevZ.AppendText` | UNKNOWN | `LOW` | 1 | 1 | `mGPBoF).Bytes` |
| `0x6b5a0` | `0x5b5a0` | `5V.(*kmkzOSevZ).AppendTo` | UNKNOWN | `LOW` | 0 | 9 | `X[*JYT1bAJ.TCYzSpw]).ScalarBaseMult, WQ0, i5V.(*mDpfdzqKmEF).init-fm` |
| `0x6b650` | `0x5b650` | `z4i5V.kmkzOSevZ.IsValid` | UNKNOWN | `LOW` | 1 | 23 | `8Izpi_).SetWriteDeadline, heejkbo8).Read, q[go.shape.string]` |
| `0x6bdb0` | `0x5bdb0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x6c0b0` | `0x5c0b0` | `evZ).MarshalText` | UNKNOWN | `LOW` | 5 | 6 | `APZ.P4wNb1l__6O, Wj4kZX).jtFlMI7Jr, 20Z.tcu6kPP7` |
| `0x6c140` | `0x5c140` | `zOSevZ).Port` | UNKNOWN | `LOW` | 1 | 5 | `APZ.P4wNb1l__6O, nc1, Wj4kZX).jtFlMI7Jr` |
| `0x6c280` | `0x5c280` | `evZ).UnmarshalBinary` | UNKNOWN | `LOW` | 1 | 4 | `MFSxVA }], .UnmarshalCompressed, EZsdym0` |
| `0x6c370` | `0x5c370` | `i5V.(*mDpfdzqKmEF).init-fm` | UNKNOWN | `LOW` | 1 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x6c4a0` | `0x5c4a0` | `.init-fm` | UNKNOWN | `LOW` | 1 | 6 | `etWriteDeadline, .(*ZWj4kZX).SetUint, WQ0` |
| `0x6c530` | `0x5c530` | `V.Te158rafFSOp` | UNKNOWN | `LOW` | 1 | 4 | `allConn, *uint8].func9, nc1` |
| `0x6c6d0` | `0x5c6d0` | `H2wAPZ.PlU0elqRnPE` | UNKNOWN | `LOW` | 4 | 1 | `orHJ20Z.init.EIYgRcen.func11.1.1` |
| `0x6c740` | `0x5c740` | `APZ.P4wNb1l__6O` | UNKNOWN | `LOW` | 2 | 2 | `orHJ20Z.init.EIYgRcen.func11.1.1, nmarshal` |
| `0x6c7d0` | `0x5c7d0` | `fhK.jk2XsnVPM[go.shape.string]` | UNKNOWN | `LOW` | 1 | 3 | `ng], tring], .func12` |
| `0x6c810` | `0x5c810` | `ng]` | UNKNOWN | `LOW` | 1 | 3 | `mGPBoF).Bytes, g], .func12` |
| `0x6c920` | `0x5c920` | `tring]` | UNKNOWN | `LOW` | 1 | 3 | `orHJ20Z.init.EIYgRcen.func11.1.1, nmarshal, .func12` |
| `0x6ca30` | `0x5ca30` | `g]` | UNKNOWN | `LOW` | 3 | 1 | `mGPBoF).Bytes` |
| `0x6caa0` | `0x5caa0` | `g]` | UNKNOWN | `LOW` | 3 | 1 | `mGPBoF).Bytes` |
| `0x6cae0` | `0x5cae0` | `q[go.shape.string]` | UNKNOWN | `LOW` | 3 | 4 | `NChRP_).ReadByte, eam, nmarshal` |
| `0x6cdb0` | `0x5cdb0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x6cdf0` | `0x5cdf0` | `tGhIXa.Error` | UNKNOWN | `LOW` | 3 | 2 | `ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x6ce30` | `0x5ce30` | `.QHJ1A8S` | UNKNOWN | `LOW` | 45 | 6 | `Czb2.pFmiMjuOz, abi.Type; ftFU4ooB64P.xukdOCPY go.shape.interface {} }]).Load, ZWj4kZX).Bits` |
| `0x6cf80` | `0x5cf80` | `.bqlafi` | UNKNOWN | `LOW` | 1 | 2 | `3vJC5GCZyE).Size, .func12` |
| `0x6d030` | `0x5d030` | `fcpURXGrF` | UNKNOWN | `LOW` | 2 | 6 | `tomic.(*ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }]).CompareAndSwap, atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap, eam` |
| `0x6d1a0` | `0x5d1a0` | `1` | UNKNOWN | `LOW` | 25 | 39 | `kimj_, QmBRaybD).MarshalSize, *JZdvaRJ).MarshalSize` |
| `0x6d320` | `0x5d320` | `4CDeQgf6l` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, fcpURXGrF, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x6d430` | `0x5d430` | `H5pmapH.(*QcMnoAPhGe1).Start.gowrap1` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, 1, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x6d540` | `0x5d540` | `MnoAPhGe1).Start.func1` | UNKNOWN | `LOW` | 2 | 4 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, hhHS85O.wQ6e481ZBAw-fm, 1` |
| `0x6d630` | `0x5d630` | `.(*FlCj9pZvT).Error` | UNKNOWN | `LOW` | 4 | 12 | `abi.Type,interface {}]).Clear, eam, hhHS85O.wQ6e481ZBAw-fm` |
| `0x6d9f0` | `0x5d9f0` | `mapH.(*QcMnoAPhGe1).nPxKD4G.func1` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 6 | 19 | `QmBRaybD).MarshalSize, dStringIndex, PQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).CompareAndSwap` |
| `0x6ddb0` | `0x5ddb0` | `1).CombinedOutput` | UNKNOWN | `LOW` | 1 | 9 | `nxvAjr).bmW27aIB17zH, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x6df70` | `0x5df70` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x6e190` | `0x5e190` | `P).hDaNvFfHTHg` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x6e230` | `0x5e230` | `H.ih1h4g7o` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x6e300` | `0x5e300` | `GBp.BmrZP6Lu0CZc` | UNKNOWN | `LOW` | 1 | 4 | `hhHS85O.wQ6e481ZBAw-fm, 3vJC5GCZyE).Size, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x6e480` | `0x5e480` | `Z.QBdLRD1QIZf` | UNKNOWN | `LOW` | 2 | 11 | `.(*FlCj9pZvT).Error, 3vJC5GCZyE).Size, P).hDaNvFfHTHg` |
| `0x6e870` | `0x5e870` | `RXi09bf9qp.func1` | UNKNOWN | `LOW` | 0 | 20 | `OU7NWVI.aXHDgGZZvF, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x6f180` | `0x5f180` | `5pmapH.(*tGhIXa).Error` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x6f190` | `0x5f190` | `apH.FlCj9pZvT.ExitCode` | UNKNOWN | `LOW` | 1 | 3 | `.UnmarshalCompressed, eam, .func12` |
| `0x6f230` | `0x5f230` | `apH.(*FlCj9pZvT).Exited` | UNKNOWN | `LOW` | 2 | 5 | `CM, Z.QBdLRD1QIZf, eam` |
| `0x6f430` | `0x5f430` | `j9pZvT.String` | UNKNOWN | `LOW` | 0 | 5 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, hhHS85O.wQ6e481ZBAw-fm, atomic.ILxa0fgA7[vNtBd9.nMPQIFVao[AcDK_Fy.bOJFoVB]]; vNtBd9.vPxVAI3 sxARgPyV0av.WV9UuS[AcDK_Fy.bOJFoVB]; vNtBd9.o7bm5AkyfJ uintptr }]).Swap` |
| `0x6f5a0` | `0x5f5a0` | `HvH5pmapH.(*FlCj9pZvT).Success` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x6f670` | `0x5f670` | `pZvT).Sys` | UNKNOWN | `LOW` | 1 | 2 | `vT.SystemTime, .func12` |
| `0x6f6e0` | `0x5f6e0` | `vT.SystemTime` | UNKNOWN | `LOW` | 2 | 10 | `nxvAjr).bmW27aIB17zH, (*gxe_j_u89O0).hjFGwuAXG3, r).rbvbqSXq` |
| `0x6f9d0` | `0x5f9d0` | `*FlCj9pZvT).UserTime` | UNKNOWN | `LOW` | 2 | 13 | `r).rbvbqSXq, 4, vT.SystemTime` |
| `0x6ffb0` | `0x5ffb0` | `ring; HvH5pmapH.zkXOOnCWMGDG string }` | UNKNOWN | `LOW` | 1 | 3 | `g4539QfP4.I0k13OdARF, eam, .func12` |
| `0x700b0` | `0x600b0` | `_dZ59.V9eEq1UH8aq0` | UNKNOWN | `LOW` | 20 | 5 | `whG.(*olJ4OFE).init, 3vJC5GCZyE).Size, nmarshal` |
| `0x702a0` | `0x602a0` | `.G2Rzf5wkmWe[go.shape.[]string,go.shape.string]` | UNKNOWN | `LOW` | 330 | 2 | `_dZ59.V9eEq1UH8aq0, .func12` |
| `0x70310` | `0x60310` | `OYkL_dZ59.w4yXDH7e` | UNKNOWN | `LOW` | 141 | 2 | `_dZ59.V9eEq1UH8aq0, .func12` |
| `0x703a0` | `0x603a0` | `kL_dZ59.gX7Vqx7a` | UNKNOWN | `LOW` | 70 | 2 | `_dZ59.V9eEq1UH8aq0, .func12` |
| `0x70440` | `0x60440` | `t` | UNKNOWN | `LOW` | 30 | 35 | `g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .func12, afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x704f0` | `0x604f0` | `OYkL_dZ59.uFiLQG` | UNKNOWN | `LOW` | 3 | 6 | `rror, 3vJC5GCZyE).Size, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x70690` | `0x60690` | `59.sdlp9P6o8` | UNKNOWN | `LOW` | 1 | 2 | `OYkL_dZ59.uFiLQG, .func12` |
| `0x70700` | `0x60700` | `p0NyMuGp` | UNKNOWN | `LOW` | 3 | 2 | `OYkL_dZ59.uFiLQG, .func12` |
| `0x70790` | `0x60790` | `wsG` | UNKNOWN | `LOW` | 1 | 2 | `OYkL_dZ59.uFiLQG, .func12` |
| `0x70830` | `0x60830` | `_dZ59.iujecbY5` | UNKNOWN | `LOW` | 296 | 5 | `Czb2.pFmiMjuOz, 3vJC5GCZyE).Size, PhLv.(*BSsluADyuaT).re5I39ze` |
| `0x70930` | `0x60930` | `whG.(*olJ4OFE).init` | UNKNOWN | `LOW` | 2 | 6 | `Czb2.pFmiMjuOz, PhLv.(*BSsluADyuaT).re5I39ze, v.(*BSsluADyuaT).laBGaoMIprT` |
| `0x70a00` | `0x60a00` | `lJ4OFE).kt2D2uRS` | UNKNOWN | `LOW` | 54 | 3 | `rror, 3vJC5GCZyE).Size, .func12` |
| `0x70ac0` | `0x60ac0` | `E).c2SpeNgT5RF` | UNKNOWN | `LOW` | 5 | 5 | `Lv.(*YRHkfNcuic).Read, pbNwhG.(*cunxvAjr).osC2Nb, nmarshal` |
| `0x70c50` | `0x60c50` | `4OFE).jAmeDuA0l6S` | UNKNOWN | `LOW` | 9 | 5 | `YRHkfNcuic).Sum, whG.(*olJ4OFE).init, alarMult` |
| `0x70dc0` | `0x60dc0` | `FE).v6zjDlfi` | UNKNOWN | `LOW` | 13 | 6 | `Czb2.pFmiMjuOz, YRHkfNcuic).Sum, alarMult` |
| `0x70e80` | `0x60e80` | `rror` | UNKNOWN | `LOW` | 4 | 10 | `Czb2.pFmiMjuOz, ZWj4kZX).Bits, nmarshal` |
| `0x70ff0` | `0x60ff0` | `pbNwhG.(*cunxvAjr).osC2Nb` | UNKNOWN | `LOW` | 1 | 6 | `Czb2.pFmiMjuOz, ZWj4kZX).Bits, nmarshal` |
| `0x71170` | `0x61170` | `NwhG.(*cunxvAjr).oyMuVL` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 3 | `zh, pqx).ListenPacket, .func12` |
| `0x713b0` | `0x613b0` | `.(*cunxvAjr).w_2fNT` | UNKNOWN | `LOW` | 8 | 1 | `89O0.(*gxe_j_u89O0).gcYExTiArY` |
| `0x71440` | `0x61440` | `.lnSyLh` | UNKNOWN | `LOW` | 0 | 1 | `etWriteDeadline` |
| `0x71470` | `0x61470` | `jr).azHtBc` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 6 | 16 | `.UnmarshalCompressed, CM, 3WHtY` |
| `0x71b50` | `0x61b50` | `3WHtY` | UNKNOWN | `LOW` | 1 | 5 | `ZwwdC2.(*LybotAM).raW2BUr, .v5SQds4Q, jMcnw` |
| `0x71d50` | `0x61d50` | `gF` | UNKNOWN | `LOW` | 1 | 7 | `er, jMcnw, .UnmarshalCompressed` |
| `0x71f90` | `0x61f90` | `r).rbvbqSXq` | UNKNOWN | `LOW` | 22 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x720a0` | `0x620a0` | `nxvAjr).bmW27aIB17zH` | UNKNOWN | `LOW` | 24 | 3 | `.(*cunxvAjr).w_2fNT, nmarshal, .func12` |
| `0x72130` | `0x62130` | `pbNwhG.(*cunxvAjr).gdM_kqpA` | UNKNOWN | `LOW` | 2 | 4 | `ingIndex.func1, OYkL_dZ59.w4yXDH7e, nxvAjr).bmW27aIB17zH` |
| `0x72240` | `0x62240` | `lRU` | UNKNOWN | `LOW` | 1 | 2 | `r).rbvbqSXq, .func12` |
| `0x722f0` | `0x622f0` | `z9j91YTQFT` | UNKNOWN | `LOW` | 6 | 14 | `r).rbvbqSXq, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x72900` | `0x62900` | `G.(*cunxvAjr).w3bZX5dLo` | UNKNOWN | `LOW` | 1 | 6 | `nxvAjr).bmW27aIB17zH, ingIndex.func1, OYkL_dZ59.w4yXDH7e` |
| `0x729f0` | `0x629f0` | `uN` | UNKNOWN | `LOW` | 1 | 3 | `.(*cunxvAjr).w_2fNT, nmarshal, .func12` |
| `0x72ac0` | `0x62ac0` | `hG.qVED1belCV` | UNKNOWN | `LOW` | 2 | 4 | `r).rbvbqSXq, stIs).Prefix, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x72c10` | `0x62c10` | `4` | UNKNOWN | `LOW` | 35 | 5 | `z9j91YTQFT, .func12, RhbuqSe).SetBytes` |
| `0x72c90` | `0x62c90` | `vPx37` | UNKNOWN | `LOW` | 2 | 2 | `z9j91YTQFT, .func12` |
| `0x72d10` | `0x62d10` | `_pbNwhG.frg6VKd324v` | UNKNOWN | `LOW` | 1 | 2 | `z9j91YTQFT, .func12` |
| `0x72d90` | `0x62d90` | `stIs).Prefix` | UNKNOWN | `LOW` | 2 | 3 | `X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, nmarshal, .func12` |
| `0x72f70` | `0x62f70` | `StartCond` | UNKNOWN | `LOW` | 5 | 4 | `r).rbvbqSXq, vPx37, nmarshal` |
| `0x73050` | `0x63050` | `6SE).MatchEmptyWidth` | UNKNOWN | `LOW` | 3 | 7 | `hhHS85O.wQ6e481ZBAw-fm, bool }]).Store, apNames` |
| `0x73240` | `0x63240` | `yF99uxur2E` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x73280` | `0x63280` | `77ZY9` | UNKNOWN | `LOW` | 1 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x732f0` | `0x632f0` | `ZfhK.FHnq5D2[go.shape.[]*_pbNwhG.AO6hizBt,go.shape.[]*_pbNwhG.AO6hizBt,go.shape.*uint8,go.shape.*uint8]` | UNKNOWN | `LOW` | 1 | 6 | `hhHS85O.wQ6e481ZBAw-fm, apNames, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x733a0` | `0x633a0` | `o.shape.*uint8]` | UNKNOWN | `LOW` | 0 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x733e0` | `0x633e0` | `apNames` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x73470` | `0x63470` | `ype:.eq._pbNwhG.WvT4Au` | UNKNOWN | `LOW` | 2 | 7 | `tBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).Store, t { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string },go.shape.struct {}].func1, hhHS85O.wQ6e481ZBAw-fm` |
| `0x736f0` | `0x636f0` | `.(*zop57OMF).Len` | UNKNOWN | `LOW` | 3 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, t2q.Size` |
| `0x73800` | `0x63800` | `nVCH` | UNKNOWN | `LOW` | 3 | 5 | `otjIqdR.(*gzU6yKL3Sva).tMxOhk2t6J, UnvqODmxW8, nmarshal` |
| `0x73960` | `0x63960` | `dR.(*Laxp2QOnMe2a).qUHJAu` | UNKNOWN | `LOW` | 0 | 2 | `ROHTU_).init, .func12` |
| `0x739c0` | `0x639c0` | `szSKcotjIqdR.(*Laxp2QOnMe2a).x0NnmRb` | UNKNOWN | `LOW` | 0 | 3 | `tgJfPz.GcNk7f, n.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }], .func12` |
| `0x73a50` | `0x63a50` | `.init` | UNKNOWN | `LOW` | 0 | 2 | `Pz4i5V.sAeZmU, cHKW1j5` |
| `0x73a90` | `0x63a90` | `L3Sva).gprGzMrYnCxj` | UNKNOWN | `LOW` | 2 | 7 | `*REGwhN0w0eUN).MXResource, .UnmarshalCompressed, jMcnw` |
| `0x73c10` | `0x63c10` | `IqdR.l9FYju` | UNKNOWN | `LOW` | 2 | 4 | `.func12.1.1, tgJfPz.GcNk7f, hhHS85O.wQ6e481ZBAw-fm` |
| `0x73cb0` | `0x63cb0` | `qdR.(*eROHTU_).bbIL5PbQcVn` | UNKNOWN | `LOW` | 0 | 2 | `R.(*Laxp2QOnMe2a).Longest, cHKW1j5` |
| `0x73cf0` | `0x63cf0` | `SKcotjIqdR.eAAF2Z5` | UNKNOWN | `LOW` | 4 | 6 | `hhHS85O.wQ6e481ZBAw-fm, IqdR.l9FYju, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x73eb0` | `0x63eb0` | `otjIqdR.(*gzU6yKL3Sva).tMxOhk2t6J` | UNKNOWN | `LOW` | 1 | 7 | `).Params, .UnmarshalCompressed, UnvqODmxW8` |
| `0x74030` | `0x64030` | `ROHTU_).init` | UNKNOWN | `LOW` | 6 | 10 | `hhHS85O.wQ6e481ZBAw-fm, IqdR.l9FYju, .JgiPo3aUOjR]).ScalarBaseMult` |
| `0x74410` | `0x64410` | `KcotjIqdR.sSOGZ5AedN` | UNKNOWN | `LOW` | 0 | 2 | `R.(*Laxp2QOnMe2a).Longest, cHKW1j5` |
| `0x74450` | `0x64450` | `sSOGZ5AedN.func1` | UNKNOWN | `LOW` | 2 | 7 | `hhHS85O.wQ6e481ZBAw-fm, szSKcotjIqdR.(*hU7W8yU6aQ).hkSuwwhWsuW, L3Sva).gprGzMrYnCxj` |
| `0x746b0` | `0x646b0` | `szSKcotjIqdR.(*hU7W8yU6aQ).hkSuwwhWsuW` | UNKNOWN | `LOW` | 1 | 8 | `hhHS85O.wQ6e481ZBAw-fm, nVCH, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x74900` | `0x64900` | `.(*hU7W8yU6aQ).g6mJ7e` | UNKNOWN | `LOW` | 1 | 3 | `).Params, L3Sva).gprGzMrYnCxj, .func12` |
| `0x74a20` | `0x64a20` | `S7kXiYoS73` | UNKNOWN | `LOW` | 1 | 9 | `hhHS85O.wQ6e481ZBAw-fm, .UnmarshalCompressed, ).Params` |
| `0x74d30` | `0x64d30` | `2Rzf5wkmWe[go.shape.[]int32,go.shape.int32]` | UNKNOWN | `LOW` | 2 | 7 | `.func12.1.1, hhHS85O.wQ6e481ZBAw-fm, S7kXiYoS73` |
| `0x74f90` | `0x64f90` | `57uaBi` | UNKNOWN | `LOW` | 1 | 6 | `.go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, hhHS85O.wQ6e481ZBAw-fm, nVCH` |
| `0x75110` | `0x65110` | `R.(*Laxp2QOnMe2a).Longest` | UNKNOWN | `LOW` | 4 | 8 | `nVCH, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .UnmarshalCompressed` |
| `0x754a0` | `0x654a0` | `KcotjIqdR.yUDCEydsPnYO` | UNKNOWN | `LOW` | 2 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x75580` | `0x65580` | `IqdR.(*Laxp2QOnMe2a).tbETsaNEF` | UNKNOWN | `LOW` | 1 | 4 | `.UnmarshalCompressed, nmarshal, eam` |
| `0x75700` | `0x65700` | `UnvqODmxW8` | UNKNOWN | `LOW` | 3 | 6 | `.UnmarshalCompressed, nmarshal, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x75940` | `0x65940` | `*Laxp2QOnMe2a).SubexpNames` | UNKNOWN | `LOW` | 1 | 2 | `UnvqODmxW8, .func12` |
| `0x759c0` | `0x659c0` | `KAN61n).pvqcm0` | UNKNOWN | `LOW` | 4 | 6 | `bool }]).Store, hhHS85O.wQ6e481ZBAw-fm, .func12.1.1` |
| `0x75ae0` | `0x65ae0` | `szSKcotjIqdR.(*b2cOtKAN61n).s2Yp4weF` | UNKNOWN | `LOW` | 0 | 2 | `R.(*Laxp2QOnMe2a).Longest, cHKW1j5` |
| `0x75b20` | `0x65b20` | `.f_yXdhVvsk` | UNKNOWN | `LOW` | 2 | 6 | `bool }]).Store, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x75ca0` | `0x65ca0` | `otjIqdR.(*biz1ihZnrpX).joitGIi3` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, eam` |
| `0x75da0` | `0x65da0` | `szSKcotjIqdR.(*biz1ihZnrpX).f_yXdhVvsk` | UNKNOWN | `LOW` | 0 | 5 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, e,interface {}]).Range` |
| `0x75ef0` | `0x65ef0` | `0` | UNKNOWN | `LOW` | 0 | 4 | `cpajYcj).Close, 4i5V.gARftz0v7, CtiT` |
| `0x75f60` | `0x65f60` | `).joitGIi3` | UNKNOWN | `LOW` | 0 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, cHKW1j5` |
| `0x75fe0` | `0x65fe0` | `7k).f_yXdhVvsk` | UNKNOWN | `LOW` | 0 | 6 | `20Z.tcu6kPP7, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x76150` | `0x66150` | `*Laxp2QOnMe2a).MatchReader` | UNKNOWN | `LOW` | 0 | 5 | `tgJfPz.GcNk7f, jMcnw, .UnmarshalCompressed` |
| `0x762f0` | `0x662f0` | `2QOnMe2a).MatchString` | UNKNOWN | `LOW` | 0 | 6 | `cpajYcj).Close, V.e39Yl0, wwdC2.(*Xomdvgk8IUZ).Marshal` |
| `0x763f0` | `0x663f0` | `Laxp2QOnMe2a).ReplaceAllString` | UNKNOWN | `LOW` | 1 | 2 | `y6zzEDRR).Marshal, .func12` |
| `0x76590` | `0x66590` | `otjIqdR.(*Laxp2QOnMe2a).ReplaceAllLiteralString` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x76650` | `0x66650` | `e2a).ReplaceAllLiteralString.func1` | UNKNOWN | `LOW` | 1 | 5 | `KcotjIqdR.(*Laxp2QOnMe2a).ReplaceAllStringFunc.func1, fD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], ) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x766c0` | `0x666c0` | `KcotjIqdR.(*Laxp2QOnMe2a).ReplaceAllStringFunc.func1` | UNKNOWN | `LOW` | 2 | 4 | `hhHS85O.wQ6e481ZBAw-fm, LYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x76740` | `0x66740` | `YaW7Lh` | UNKNOWN | `LOW` | 2 | 5 | `hhHS85O.wQ6e481ZBAw-fm, ).Params, ) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x767d0` | `0x667d0` | `unc1` | UNKNOWN | `LOW` | 3 | 25 | `abi.Type,go.shape.interface {}]).Store, 4fQfOR).Err, Y41KqyoVl).Deadline` |
| `0x76890` | `0x66890` | `AllLiteral.func1` | UNKNOWN | `LOW` | 3 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x76920` | `0x66920` | `).ReplaceAllFunc.func1` | UNKNOWN | `LOW` | 1 | 4 | `.V15kIRyX7X, jYYtfpHkV.(*VFIaf3e_1KX).HashFunc, tKeZwwdC2.iWMrajC` |
| `0x769e0` | `0x669e0` | `tjIqdR.(*Laxp2QOnMe2a).gaWGJ3x` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x76a60` | `0x66a60` | `Me2a).FindIndex` | UNKNOWN | `LOW` | 1 | 4 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, eam` |
| `0x76b20` | `0x66b20` | `dStringIndex` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x76ba0` | `0x66ba0` | `indSubmatch` | UNKNOWN | `LOW` | 9 | 12 | `CM, g, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x76e50` | `0x66e50` | `g` | UNKNOWN | `LOW` | 7 | 31 | `4CM, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x771b0` | `0x671b0` | `nMe2a).FindSubmatchIndex` | UNKNOWN | `LOW` | 5 | 14 | `CM, z9j91YTQFT, g` |
| `0x774d0` | `0x674d0` | `Laxp2QOnMe2a).FindStringSubmatchIndex` | UNKNOWN | `LOW` | 2 | 8 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x77600` | `0x67600` | `ex` | UNKNOWN | `LOW` | 2 | 2 | `r).rbvbqSXq, .func12` |
| `0x77690` | `0x67690` | `otjIqdR.(*Laxp2QOnMe2a).FindAllIndex` | UNKNOWN | `LOW` | 2 | 3 | `).d4HqCATIjjo, nmarshal, .func12` |
| `0x77780` | `0x67780` | `KcotjIqdR.(*Laxp2QOnMe2a).FindAllString` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 5 | 10 | `nMe2a).FindSubmatchIndex, otjIqdR.(*Laxp2QOnMe2a).FindAllIndex, ex` |
| `0x77a30` | `0x67a30` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x77e70` | `0x67e70` | `ingIndex.func1` | UNKNOWN | `LOW` | 5 | 3 | `89O0.(*gxe_j_u89O0).gcYExTiArY, nmarshal, .func12` |
| `0x77f70` | `0x67f70` | `.FindAllSubmatch.func1` | UNKNOWN | `LOW` | 3 | 5 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x78070` | `0x68070` | `Laxp2QOnMe2a).FindAllSubmatchIndex.func1` | UNKNOWN | `LOW` | 2 | 4 | `CM, 2], tch` |
| `0x78120` | `0x68120` | `tch` | UNKNOWN | `LOW` | 2 | 12 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x78310` | `0x68310` | `).FindAllStringSubmatchIndex` | UNKNOWN | `LOW` | 1 | 2 | `c1, .func12` |
| `0x78390` | `0x68390` | `c1` | UNKNOWN | `LOW` | 21 | 19 | `, Laxp2QOnMe2a).FindAllSubmatchIndex.func1, E[go.shape.int32]` |
| `0x785c0` | `0x685c0` | `dR.(*Laxp2QOnMe2a).MarshalText` | UNKNOWN | `LOW` | 0 | 7 | `indSubmatch, j3[go.shape.int32], XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x78700` | `0x68700` | `j3[go.shape.int32]` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 1 | 22 | `nMe2a).FindSubmatchIndex, ex, KEOvQk` |
| `0x78e00` | `0x68e00` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x78e80` | `0x68e80` | `E[go.shape.int32]` | UNKNOWN | `LOW` | 1 | 9 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x79040` | `0x69040` | `32]` | UNKNOWN | `LOW` | 1 | 13 | `KEOvQk, JYT1bAJ.(*DKyyIy).mfCdZz, nxvAjr).bmW27aIB17zH` |
| `0x79220` | `0x69220` | `OP[go.shape.int32]` | UNKNOWN | `LOW` | 0 | 3 | `indSubmatch, KcotjIqdR.(*Laxp2QOnMe2a).FindAllString, cHKW1j5` |
| `0x792c0` | `0x692c0` | `ZqlIeq[go.shape.int32]` | UNKNOWN | `LOW` | 3 | 3 | `indSubmatch, KcotjIqdR.(*Laxp2QOnMe2a).FindAllString, .func12` |
| `0x79370` | `0x69370` | `2]` | UNKNOWN | `LOW` | 2 | 2 | `.jTfCNVqcgC, .func12` |
| `0x79420` | `0x69420` | `.jTfCNVqcgC` | UNKNOWN | `LOW` | 2 | 4 | `nxvAjr).bmW27aIB17zH, 89O0.(*gxe_j_u89O0).gcYExTiArY, SKcotjIqdR.(*xB6FOKu).MatchRunePos` |
| `0x79600` | `0x69600` | `SKcotjIqdR.(*xB6FOKu).MatchRunePos` | UNKNOWN | `LOW` | 1 | 3 | `X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, alarMult, .func12` |
| `0x797c0` | `0x697c0` | `estinationSSRC` | UNKNOWN | `LOW` | 5 | 17 | `.func12.1.1, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x79ba0` | `0x69ba0` | `*IpYWV0x6S).MarshalSize` | UNKNOWN | `LOW` | 3 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, p1, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x79ca0` | `0x69ca0` | `arshal` | UNKNOWN | `LOW` | 3 | 22 | `YT47X.String, XPz4i5V.(*priWRezQsI).lEvYyBEt, p1` |
| `0x79df0` | `0x69df0` | `bEWS2r).d4HqCATIjjo` | UNKNOWN | `LOW` | 2 | 6 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, Y3L).UnmarshalText` |
| `0x79f60` | `0x69f60` | `SSRC` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x79fb0` | `0x69fb0` | `YT47X.String` | UNKNOWN | `LOW` | 8 | 3 | `CM, nxvAjr).bmW27aIB17zH, .func12` |
| `0x7a110` | `0x6a110` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x7a220` | `0x6a220` | `wy).raW2BUr` | UNKNOWN | `LOW` | 2 | 10 | `ZwwdC2.(*LybotAM).raW2BUr, .(*cunxvAjr).w_2fNT, XPz4i5V.(*priWRezQsI).lEvYyBEt` |
| `0x7a3a0` | `0x6a3a0` | `ZwwdC2.(*LybotAM).raW2BUr` | UNKNOWN | `LOW` | 4 | 1 | `.func12` |
| `0x7a430` | `0x6a430` | `).d4HqCATIjjo` | UNKNOWN | `LOW` | 1 | 2 | `nmarshal, .func12` |
| `0x7a500` | `0x6a500` | `wfuAsc).DestinationSSRC` | UNKNOWN | `LOW` | 3 | 5 | `r, .func12.1.1, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x7a6c0` | `0x6a6c0` | `r` | UNKNOWN | `LOW` | 15 | 33 | `mdvgk8IUZ.MarshalSize, qXKvEXo).SetKeepAliveConfig, oUDP` |
| `0x7a710` | `0x6a710` | `C2.(*TEisJDbqKF).raW2BUr` | UNKNOWN | `LOW` | 3 | 1 | `tgJfPz.GcNk7f` |
| `0x7a760` | `0x6a760` | `S4MScSHsVYm).d4HqCATIjjo` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, YKN).Header, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x7a7d0` | `0x6a7d0` | `mdvgk8IUZ.MarshalSize` | UNKNOWN | `LOW` | 1 | 6 | `tgJfPz.GcNk7f, .func12.1.1, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x7aac0` | `0x6aac0` | `nmarshal` | UNKNOWN | `LOW` | 1390 | 9 | `hhHS85O.wQ6e481ZBAw-fm, YKN).Header, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x7abb0` | `0x6abb0` | `tionSSRC` | UNKNOWN | `LOW` | 1 | 2 | `eam, nmarshal` |
| `0x7ac60` | `0x6ac60` | `YKN).Header` | UNKNOWN | `LOW` | 7 | 2 | `tionSSRC, .r6TygsBh.Len` |
| `0x7ad10` | `0x6ad10` | `C2.(*I9aU8YKN).String` | UNKNOWN | `LOW` | 1 | 8 | `big.(*JEyvNEwJVta).j5_9oxK, teAddr, KcotjIqdR.(*Laxp2QOnMe2a).ReplaceAllStringFunc.func1` |
| `0x7ae10` | `0x6ae10` | `MEJQEUL4B.Marshal` | UNKNOWN | `LOW` | 1 | 8 | `, eDeadline, r` |
| `0x7b350` | `0x6b350` | `MEJQEUL4B).Header` | UNKNOWN | `LOW` | 1 | 2 | `tgJfPz.GcNk7f, .func12` |
| `0x7b3c0` | `0x6b3c0` | `SRC` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, YKN).Header, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x7b450` | `0x6b450` | `TDCxk82bm` | UNKNOWN | `LOW` | 1 | 4 | `.func12.1.1, 20Z.tcu6kPP7, .File` |
| `0x7b6e0` | `0x6b6e0` | `.V15kIRyX7X` | UNKNOWN | `LOW` | 30 | 4 | `tKeZwwdC2.(*IN48S9wcT).String, tring, arBaseMult` |
| `0x7b9e0` | `0x6b9e0` | `tKeZwwdC2.iWMrajC` | UNKNOWN | `LOW` | 30 | 3 | `wfuAsc).DestinationSSRC, arBaseMult, .func12` |
| `0x7baa0` | `0x6baa0` | `.Unmarshal` | UNKNOWN | `LOW` | 1 | 3 | `tKeZwwdC2.(*QQmBRaybD).Marshal, String, .func12` |
| `0x7bb30` | `0x6bb30` | `xLZ).String` | UNKNOWN | `LOW` | 3 | 4 | `txbdkX[go.shape.*uint8]).nIKoXvk5, (*I4jsF4Ok).Unmarshal, (*gxe_j_u89O0).hjFGwuAXG3` |
| `0x7bcf0` | `0x6bcf0` | `(*I4jsF4Ok).Unmarshal` | UNKNOWN | `LOW` | 1 | 3 | `arshal, 3vJC5GCZyE).Size, .func12` |
| `0x7bda0` | `0x6bda0` | `tKeZwwdC2.(*I4jsF4Ok).DestinationSSRC` | UNKNOWN | `LOW` | 3 | 3 | `big.(*JEyvNEwJVta).j5_9oxK, ntKeZwwdC2.FCH3YTKDW.Marshal, .func12` |
| `0x7be10` | `0x6be10` | `arshal` | UNKNOWN | `LOW` | 3 | 22 | `YT47X.String, XPz4i5V.(*priWRezQsI).lEvYyBEt, p1` |
| `0x7bf40` | `0x6bf40` | `estinationSSRC` | UNKNOWN | `LOW` | 5 | 17 | `.func12.1.1, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x7c0e0` | `0x6c0e0` | `ntKeZwwdC2.FCH3YTKDW.Marshal` | UNKNOWN | `LOW` | 1 | 3 | `e,interface {}]).Range, big.(*JEyvNEwJVta).j5_9oxK, .func12` |
| `0x7c1a0` | `0x6c1a0` | `alTo` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x7c1b0` | `0x6c1b0` | `YTKDW).Header` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x7c1c0` | `0x6c1c0` | `(*FCH3YTKDW).DestinationSSRC` | UNKNOWN | `LOW` | 2 | 1 | `QmBRaybD).MarshalSize` |
| `0x7c200` | `0x6c200` | `QmBRaybD).MarshalSize` | UNKNOWN | `LOW` | 44 | 0 | `None` |
| `0x7c300` | `0x6c300` | `ybD).Unmarshal` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x7c310` | `0x6c310` | `wwdC2.FE4etc.Marshal` | UNKNOWN | `LOW` | 2 | 0 | `None` |
| `0x7c390` | `0x6c390` | `dC2.GxhnYyL_G.DestinationSSRC` | UNKNOWN | `LOW` | 2 | 4 | `.V15kIRyX7X, wwdC2.(*Xomdvgk8IUZ).Marshal, tKeZwwdC2.iWMrajC` |
| `0x7c440` | `0x6c440` | `lSize` | UNKNOWN | `LOW` | 2 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7c4e0` | `0x6c4e0` | `nYyL_G.Marshal` | UNKNOWN | `LOW` | 2 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7c550` | `0x6c550` | `RnE7d5H9U2eV.String` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7c5d0` | `0x6c5d0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x7c690` | `0x6c690` | `KeZwwdC2.IN48S9wcT.Marshal` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7c710` | `0x6c710` | `eader` | UNKNOWN | `LOW` | 1 | 6 | `.V15kIRyX7X, y6zzEDRR).Marshal, wwdC2.(*Xomdvgk8IUZ).Marshal` |
| `0x7c810` | `0x6c810` | `C2.IN48S9wcT.String` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7c870` | `0x6c870` | `*JZdvaRJ).MarshalSize` | UNKNOWN | `LOW` | 3 | 2 | `eam, .func12` |
| `0x7c8f0` | `0x6c8f0` | `wwdC2.(*JZdvaRJ).DestinationSSRC` | UNKNOWN | `LOW` | 2 | 4 | `.V15kIRyX7X, wwdC2.(*Xomdvgk8IUZ).Marshal, tKeZwwdC2.iWMrajC` |
| `0x7c9e0` | `0x6c9e0` | `Marshal` | UNKNOWN | `LOW` | 3 | 5 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, eam` |
| `0x7caa0` | `0x6caa0` | `C2.(*TWr_tJSkG90s).Unmarshal` | UNKNOWN | `LOW` | 1 | 4 | `.V15kIRyX7X, wwdC2.(*Xomdvgk8IUZ).Marshal, tKeZwwdC2.iWMrajC` |
| `0x7cb40` | `0x6cb40` | `rshal` | UNKNOWN | `LOW` | 7 | 7 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7cba0` | `0x6cba0` | `w9COl4y00.Len` | UNKNOWN | `LOW` | 1 | 5 | `.V15kIRyX7X, .Unmarshal, wwdC2.(*Xomdvgk8IUZ).Marshal` |
| `0x7ccd0` | `0x6ccd0` | `nSSRC` | UNKNOWN | `LOW` | 3 | 4 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, nmarshal` |
| `0x7cde0` | `0x6cde0` | `nmarshal` | UNKNOWN | `LOW` | 1390 | 9 | `hhHS85O.wQ6e481ZBAw-fm, YKN).Header, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x7ce40` | `0x6ce40` | `dC2.(*WbMJSfJ).Unmarshal` | UNKNOWN | `LOW` | 4 | 5 | `.V15kIRyX7X, wwdC2.(*Xomdvgk8IUZ).Marshal, tKeZwwdC2.iWMrajC` |
| `0x7cf30` | `0x6cf30` | `rshal` | UNKNOWN | `LOW` | 7 | 7 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7d030` | `0x6d030` | `_).hup5blt59hNV` | UNKNOWN | `LOW` | 6 | 5 | `pYs, .V15kIRyX7X, wwdC2.(*Xomdvgk8IUZ).Marshal` |
| `0x7d120` | `0x6d120` | `pYs` | UNKNOWN | `LOW` | 1 | 3 | `tring, arBaseMult, .func12` |
| `0x7d270` | `0x6d270` | `LPGP__.DestinationSSRC` | UNKNOWN | `LOW` | 2 | 4 | `.V15kIRyX7X, wwdC2.(*Xomdvgk8IUZ).Marshal, tKeZwwdC2.iWMrajC` |
| `0x7d350` | `0x6d350` | `wdC2.(*J4eijR).PacketList.func1` | UNKNOWN | `LOW` | 2 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7d3e0` | `0x6d3e0` | `.Header` | UNKNOWN | `LOW` | 5 | 5 | `tKeZwwdC2.(*IN48S9wcT).String, .V15kIRyX7X, tKeZwwdC2.iWMrajC` |
| `0x7d5e0` | `0x6d5e0` | `wdC2.UzX65jNFzwr.String` | UNKNOWN | `LOW` | 2 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7d650` | `0x6d650` | `lf4m` | UNKNOWN | `LOW` | 1 | 4 | `32, .V15kIRyX7X, tKeZwwdC2.iWMrajC` |
| `0x7d700` | `0x6d700` | `w9COl4y00` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7d7b0` | `0x6d7b0` | `dC2.M7XB_IfPUd` | UNKNOWN | `LOW` | 1 | 3 | `.V15kIRyX7X, tKeZwwdC2.iWMrajC, .func12` |
| `0x7d810` | `0x6d810` | `9aU8YKN).Marshal` | UNKNOWN | `LOW` | 2 | 8 | `tgJfPz.GcNk7f, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x7d930` | `0x6d930` | `wwdC2.(*IpYWV0x6S).DestinationSSRC` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, YKN).Header` |
| `0x7da20` | `0x6da20` | `wwdC2.(*Xomdvgk8IUZ).Marshal` | UNKNOWN | `LOW` | 11 | 16 | `, tring, (*txbdkX[*JYT1bAJ.GUY8D0aEy]).Params` |
| `0x7dde0` | `0x6dde0` | `String` | UNKNOWN | `LOW` | 15 | 34 | `bindRemoteStream, oOQ5c.(*OJTGDxy5).zGWejRL, GcJWf` |
| `0x7de50` | `0x6de50` | `Type` | UNKNOWN | `LOW` | 1 | 8 | `WPs1, arshal, C2.(*TEisJDbqKF).raW2BUr` |
| `0x7df30` | `0x6df30` | `arshal` | UNKNOWN | `LOW` | 3 | 22 | `YT47X.String, XPz4i5V.(*priWRezQsI).lEvYyBEt, p1` |
| `0x7e430` | `0x6e430` | `).Marshal` | UNKNOWN | `LOW` | 1 | 7 | `WPs1, er, .UnmarshalCompressed` |
| `0x7e620` | `0x6e620` | `m).MarshalSize` | UNKNOWN | `LOW` | 1 | 2 | `y6zzEDRR).Marshal, .func12` |
| `0x7e730` | `0x6e730` | `*FCH3YTKDW).MarshalSize` | INFERRED_ROLE: Process Execution & Scrcpy Helper Watchdog | `MEDIUM` | 1 | 6 | `3vJC5GCZyE).Size, CM, KEOvQk` |
| `0x7ea00` | `0x6ea00` | `tKeZwwdC2.(*QQmBRaybD).Marshal` | UNKNOWN | `LOW` | 1 | 3 | `CM, r).rbvbqSXq, .func12` |
| `0x7eac0` | `0x6eac0` | `tring` | UNKNOWN | `LOW` | 7 | 20 | `bindRemoteStream, 5).Grow, ead` |
| `0x7eb90` | `0x6eb90` | `C2.(*GxhnYyL_G).Marshal` | UNKNOWN | `LOW` | 1 | 2 | `tKeZwwdC2.(*IN48S9wcT).String, eam` |
| `0x7ed20` | `0x6ed20` | `tKeZwwdC2.(*IN48S9wcT).String` | UNKNOWN | `LOW` | 3 | 7 | `wfuAsc).DestinationSSRC, XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu` |
| `0x7edd0` | `0x6edd0` | `tring` | UNKNOWN | `LOW` | 7 | 20 | `bindRemoteStream, 5).Grow, ead` |
| `0x7eeb0` | `0x6eeb0` | `y6zzEDRR).Marshal` | UNKNOWN | `LOW` | 3 | 3 | `xLZ).String, tgJfPz.GcNk7f, .func12` |
| `0x7ef50` | `0x6ef50` | `wdC2.(*WbMJSfJ).Marshal` | UNKNOWN | `LOW` | 0 | 2 | `wwdC2.(*TkLPGP__).DestinationSSRC, cHKW1j5` |
| `0x7ef90` | `0x6ef90` | `wwdC2.(*TkLPGP__).DestinationSSRC` | UNKNOWN | `LOW` | 1 | 8 | `hhHS85O.wQ6e481ZBAw-fm, r, 3vJC5GCZyE).Size` |
| `0x7f1f0` | `0x6f1f0` | `String` | UNKNOWN | `LOW` | 15 | 34 | `bindRemoteStream, oOQ5c.(*OJTGDxy5).zGWejRL, GcJWf` |
| `0x7f260` | `0x6f260` | `aPa.Size` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, YKN).Header, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x7f2e0` | `0x6f2e0` | `f3e_1KX.String` | UNKNOWN | `LOW` | 1 | 8 | `r, PPT).Select, .func12.1.1` |
| `0x7f6b0` | `0x6f6b0` | `_1KX.Available` | UNKNOWN | `LOW` | 0 | 4 | `hhHS85O.wQ6e481ZBAw-fm, YKN).Header, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x7f720` | `0x6f720` | `jYYtfpHkV.(*VFIaf3e_1KX).HashFunc` | UNKNOWN | `LOW` | 1 | 2 | `xLZ).String, .func12` |
| `0x7f780` | `0x6f780` | `).Size` | UNKNOWN | `LOW` | 1 | 5 | `vW7sa, C2.(*TEisJDbqKF).raW2BUr, tKeZwwdC2.(*I4jsF4Ok).DestinationSSRC` |
| `0x7f840` | `0x6f840` | `vW7sa` | UNKNOWN | `LOW` | 2 | 8 | `YLuQc.init, r, 3vJC5GCZyE).Size` |
| `0x7fc60` | `0x6fc60` | `YLuQc.init` | UNKNOWN | `LOW` | 15 | 4 | `sa7.(*UdymEtYSFZ).Sum, nit.JyjLYF7KXE[go.shape.bool].func4.1.1, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed` |
| `0x7fcf0` | `0x6fcf0` | `a7.(*UdymEtYSFZ).MarshalBinary` | UNKNOWN | `LOW` | 1 | 3 | `nit.JyjLYF7KXE[go.shape.bool].func4.1.1, sa7.(*UdymEtYSFZ).Sum, .func12` |
| `0x7fe10` | `0x6fe10` | `g4539QfP4.I0k13OdARF` | UNKNOWN | `LOW` | 7 | 3 | `20Z.tcu6kPP7, hape.string]).CompareAndSwap, tgJfPz.GcNk7f` |
| `0x7ff10` | `0x6ff10` | `fP4.C1QrTPUK` | UNKNOWN | `LOW` | 0 | 2 | `6sa7.(*UdymEtYSFZ).Size, cHKW1j5` |
| `0x7ff50` | `0x6ff50` | `fP4.XFicoAq` | UNKNOWN | `LOW` | 1 | 0 | `None` |
| `0x80010` | `0x70010` | `6sa7.(*UdymEtYSFZ).Size` | UNKNOWN | `LOW` | 2 | 4 | `fP4.XFicoAq, 6sa7.(*UdymEtYSFZ).Size, eam` |
| `0x801e0` | `0x701e0` | `sa7.(*UdymEtYSFZ).Sum` | UNKNOWN | `LOW` | 8 | 10 | `hhHS85O.wQ6e481ZBAw-fm, lg.IndexRabinKarp[go.shape.[]uint8], .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x80410` | `0x70410` | `3jtsJa5G` | UNKNOWN | `LOW` | 4 | 10 | `.(*WoouI2oNLf).Reset, hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x80690` | `0x70690` | `7.hQaTbS2A` | UNKNOWN | `LOW` | 2 | 11 | `hhHS85O.wQ6e481ZBAw-fm, .(*WoouI2oNLf).Reset, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x80860` | `0x70860` | `Zrr.Dtha4J1a` | UNKNOWN | `LOW` | 2 | 4 | `sa7.(*UdymEtYSFZ).Sum, nit.JyjLYF7KXE[go.shape.bool].func4.1.1, a9eldi` |
| `0x809a0` | `0x709a0` | `vll` | UNKNOWN | `LOW` | 1 | 10 | `rwrap1, jMcnw, .UnmarshalCompressed` |
| `0x80e70` | `0x70e70` | `.(*BSsluADyuaT).Reset` | UNKNOWN | `LOW` | 2 | 19 | `.(*aUYNELk).qHRDJIx, 7afn.(*aUYNELk).iBwI1vT, YLuQc.init` |
| `0x81910` | `0x71910` | `PhLv.(*BSsluADyuaT).re5I39ze` | UNKNOWN | `LOW` | 51 | 2 | `ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x81950` | `0x71950` | `v.(*BSsluADyuaT).laBGaoMIprT` | UNKNOWN | `LOW` | 36 | 2 | `ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x81990` | `0x71990` | `Lv.(*BSsluADyuaT).xmHeAsfrPO` | UNKNOWN | `LOW` | 35 | 2 | `(*BSsluADyuaT).emSuhA0qQG, .func12` |
| `0x819d0` | `0x719d0` | `(*BSsluADyuaT).emSuhA0qQG` | UNKNOWN | `LOW` | 1 | 3 | `iaoOaLpN bool }]).Load, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x81a30` | `0x71a30` | `XaCXVM` | UNKNOWN | `LOW` | 22 | 2 | `T).AppendBinary, .func12` |
| `0x81a70` | `0x71a70` | `T).AppendBinary` | UNKNOWN | `LOW` | 1 | 3 | `iaoOaLpN bool }]).Load, ma.(*MydupPsvCWhi).SetExtension, .func12` |
| `0x81ad0` | `0x71ad0` | `rLPhLv.e7LUen9MwX` | UNKNOWN | `LOW` | 1 | 2 | `Lv.(*YRHkfNcuic).Read, .func12` |
| `0x81b60` | `0x71b60` | `Lv.(*YRHkfNcuic).Read` | UNKNOWN | `LOW` | 59 | 3 | `nmarshal, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, .func12` |
| `0x81d70` | `0x71d70` | `YRHkfNcuic).Sum` | UNKNOWN | `LOW` | 2 | 2 | `nmarshal, .func12` |
| `0x81f00` | `0x71f00` | `it.0` | UNKNOWN | `LOW` | 1 | 6 | `.JgiPo3aUOjR]).ScalarBaseMult, .UnmarshalCompressed, ).Params` |
| `0x822e0` | `0x722e0` | `endBinary` | UNKNOWN | `LOW` | 1 | 3 | `.(*cunxvAjr).w_2fNT, (*gxe_j_u89O0).hjFGwuAXG3, .func12` |
| `0x823e0` | `0x723e0` | `` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 339 | 508 | `wdMHkQqV.B63ntXMLm2, X[*JYT1bAJ.GUY8D0aEy]).UnmarshalCompressed, g.(*txbdkX[*JYT1bAJ.DKyyIy]).IsOnCurve` |
| `0x82670` | `0x72670` | `(*ZgzpIy).Write` | UNKNOWN | `LOW` | 0 | 3 | `.(*cunxvAjr).w_2fNT, (*gxe_j_u89O0).hjFGwuAXG3, cHKW1j5` |
| `0x827e0` | `0x727e0` | `Qzr8` | UNKNOWN | `LOW` | 1 | 4 | `it.0, endBinary, ` |
| `0x82880` | `0x72880` | `g` | UNKNOWN | `LOW` | 7 | 31 | `4CM, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x82930` | `0x72930` | `P0.(*WAhBTuo).Write` | INFERRED_ROLE: Scrcpy IPC / UNIX Domain Socket Handler | `MEDIUM` | 1 | 10 | `hhHS85O.wQ6e481ZBAw-fm, n.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }], uDeMp8Izpi_.SetKeepAlive` |
| `0x82bd0` | `0x72bd0` | `ze` | UNKNOWN | `LOW` | 1 | 5 | `hhHS85O.wQ6e481ZBAw-fm, jMcnw, .UnmarshalCompressed` |
| `0x82cc0` | `0x72cc0` | `.(*WAhBTuo).Clone` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x82cd0` | `0x72cd0` | `y[go.shape.*uint8]` | UNKNOWN | `LOW` | 0 | 3 | `hhHS85O.wQ6e481ZBAw-fm, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }, .func12` |
| `0x82d60` | `0x72d60` | `BdJky[go.shape.*uint8].func1.1` | UNKNOWN | `LOW` | 0 | 4 | `QmBRaybD).MarshalSize, C2.(*GxhnYyL_G).Marshal, arBaseMult` |
| `0x82ed0` | `0x72ed0` | `gh974_.init.0` | UNKNOWN | `LOW` | 0 | 7 | `Kr2TJo.fjzI9oE9i.func1, orHJ20Z.init.EIYgRcen.func11.1.1, OOTxat []uint8; g1gLI7afn.qeClHPX string; g1gLI7afn.xS9t6y string; g1gLI7afn.gOQi0jGiHfD bool; g1gLI7afn.dshPgaG0 []int; g1gLI7afn.iTFItOFLoj reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` |
| `0x83190` | `0x73190` | `hy.(*DhFBCMe3PJYf).BlockSize` | UNKNOWN | `LOW` | 0 | 7 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, .ISwY3L.Mask` |
| `0x83330` | `0x73330` | `rypt` | UNKNOWN | `LOW` | 0 | 2 | `eam, .func12` |
| `0x83370` | `0x73370` | `JFg58S7` | UNKNOWN | `LOW` | 0 | 5 | `hhHS85O.wQ6e481ZBAw-fm, *ISwY3L).MarshalText, heejkbo8).k9azrvO` |
| `0x834a0` | `0x734a0` | `hJa8jDkB).doDi4LPXB` | UNKNOWN | `LOW` | 0 | 2 | `eam, .func12` |
| `0x834e0` | `0x734e0` | `1` | UNKNOWN | `LOW` | 25 | 39 | `kimj_, QmBRaybD).MarshalSize, *JZdvaRJ).MarshalSize` |
| `0x834f0` | `0x734f0` | `yptBlocks` | UNKNOWN | `LOW` | 0 | 2 | `1, .func12` |
| `0x83540` | `0x73540` | `y.inZsbVxFsIMC` | UNKNOWN | `LOW` | 0 | 2 | `.(*ZWj4kZX).SetUint, .func12` |
| `0x83580` | `0x73580` | `ryptBlocks` | UNKNOWN | `LOW` | 1 | 5 | `eFuxzMSJ.Gr1e3YXm; hbXPz4i5V.feOwrZ5kjh uint32; hbXPz4i5V.r3cU4RY4JW3U bool; hbXPz4i5V.bgSUEw60y bool; hbXPz4i5V.uBD9wJITPYLd bool; hbXPz4i5V.ziaoOaLpN bool }]).Store, OYkL_dZ59.w4yXDH7e, eam` |
| `0x83650` | `0x73650` | `GZa0Y` | UNKNOWN | `LOW` | 0 | 2 | `eam, .func12` |
| `0x83690` | `0x73690` | `treamAt` | UNKNOWN | `LOW` | 0 | 2 | `B4Uc, .func12` |
| `0x836d0` | `0x736d0` | `g` | UNKNOWN | `LOW` | 7 | 31 | `4CM, .func12, hhHS85O.wQ6e481ZBAw-fm` |
| `0x837e0` | `0x737e0` | `.func1` | UNKNOWN | `LOW` | 9 | 17 | `XPz4i5V.(*priWRezQsI).lEvYyBEt, 4i5V.mkwDVaH0Iu, bXPz4i5V.jP7NLOA9Bd9g` |
| `0x83860` | `0x73860` | `HHhy.aL7exbDahgtu` | UNKNOWN | `LOW` | 0 | 3 | `.func12.1.1, atomic.ILxa0fgA7[go.shape.struct { vNtBd9.haTaT_U7 bool }] }]).Load, .func12` |
| `0x83940` | `0x73940` | `F` | UNKNOWN | `LOW` | 1 | 6 | `UnmarshalText, .func12, _dZ59.iujecbY5` |
| `0x839b0` | `0x739b0` | `aH.GWyY0vbk2uSQ` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x839c0` | `0x739c0` | `V7v34` | UNKNOWN | `LOW` | 0 | 0 | `None` |
| `0x839d0` | `0x739d0` | `enL).Seed` | UNKNOWN | `LOW` | 0 | 2 | `, .func12` |
| `0x83a50` | `0x73a50` | `utUint64` | UNKNOWN | `LOW` | 0 | 2 | `nterface {}]], .func12` |
| `0x83a90` | `0x73a90` | `S6pX.(*UbEeJCenL).AppendBinary` | UNKNOWN | `LOW` | 0 | 4 | `abi.Type,go.shape.interface {}]).CompareAndSwap.deferwrap1, tgJfPz.GcNk7f, ).Params` |
| `0x83b80` | `0x73b80` | `lBinary` | UNKNOWN | `LOW` | 3 | 7 | `hhHS85O.wQ6e481ZBAw-fm, Pz4i5V.(*Gf_aZ0Zk).File, .go.shape.struct { g1gLI7afn.a_3dNPvD reflect.V8CvLYzyC; g1gLI7afn.tmNOZlU_ string }` |
| `0x83c00` | `0x73c00` | `S6pX.UbEeJCenL` | UNKNOWN | `LOW` | 0 | 2 | `FSBPDcz8s).rCrKT0p2Li, .func12` |
| `0x83c40` | `0x73c40` | `D6_JWRA).Uint64` | UNKNOWN | `LOW` | 0 | 3 | `B4Uc, atomic.ILxa0fgA7[vNtBd9.anIeJO2iz9g[AcDK_Fy.bOJFoVB]] }]).CompareAndSwap, .func12` |
| `0x83cf0` | `0x73cf0` | `3M9ICypivII` | UNKNOWN | `LOW` | 0 | 2 | `uct { AcDK_Fy.amNT3JZL bool; AcDK_Fy.kCEV3Lu09HcR string }]).LoadOrStore.deferwrap1, .func12` |

## 2. Sample Runtime & WebRTC Library Functions

| Virtual Address | Offset | Symbol Name | Inferred Role | Conf |
|---|---|---|---|---|
| `0x119f0` | `0x19f0` | `go.shape.interface { Info() (e1lTH4kX4.NIJruoQeZA, error); IsDir() bool; Name() string; Type() e1lTH4kX4.VUDQtlbpLd9E }]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x179c0` | `0x79c0` | `go.shape.int]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x21670` | `0x11670` | `reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x23f20` | `0x13f20` | `reflect.N0218qV5; g1gLI7afn.qDzkJnQDO bool; g1gLI7afn.rAsOGVGxqL bool; g1gLI7afn.sCXGKuwu func(reflect.V8CvLYzyC) bool; g1gLI7afn.wFv2uagJG bool; g1gLI7afn.fW6iyQpIVK4K g1gLI7afn.uNNgMFSxVA }]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x2cc40` | `0x1cc40` | `internal/abi.Type,go.shape.interface {}]).gmfw5hm` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x2e890` | `0x1e890` | `internal/abi.Type,go.shape.interface {}]).x7kCPkLMq` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x2ea10` | `0x1ea10` | `internal/abi.Type,go.shape.interface {}]).LoadOrStore.deferwrap1` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x854b0` | `0x754b0` | `math/big.(*JEyvNEwJVta).AndNot` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x85fe0` | `0x75fe0` | `math/big.hRocLmfCzb2.nzGwRZaB2m` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x8e800` | `0x7e800` | `go.shape.*JYT1bAJ.TCYzSpw]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x8e9f0` | `0x7e9f0` | `go.shape.*JYT1bAJ.TCYzSpw].func1` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x91f90` | `0x81f90` | `reflect.F5Cl4yr[go.shape.*uint8]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x961d0` | `0x861d0` | `go.shape.*JYT1bAJ.DKyyIy]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x9ad10` | `0x8ad10` | `go.shape.struct { nRX2Gawi2c3r.e_3sKa [32]uint8; nRX2Gawi2c3r.ezqCmloNOgS [32]uint8; nRX2Gawi2c3r.gEmR6cP9 VcWDxyqoc.ZDWeTvCB; nRX2Gawi2c3r.cbL2XPG [32]uint8 }]).Get` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0xa0810` | `0x90810` | `ostname` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0xb2cf0` | `0xa2cf0` | `go.shape.*uint8]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0xb5be0` | `0xa5be0` | `go.shape.uint16]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x131f20` | `0x121f20` | `go.shape.int32]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x14a060` | `0x13a060` | `go.shape.*uint8]).jtqPyn9qP` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x150630` | `0x140630` | `go.shape.map[string]func(string, *dG99HG.DzMtLjG) IJPCIQs.WEqQoyDTxY,go.shape.string,go.shape.func(string, *dG99HG.DzMtLjG) IJPCIQs.WEqQoyDTxY]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x154be0` | `0x144be0` | `go.shape.[]string,go.shape.string]` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x1c5930` | `0x1b5930` | `ion\""; HlfE6o2anmA uint32 "json:\"keycode\""; M_MllM7O uint32 "json:\"repeat\""; MusK0Kao4ol uint32 "json:\"meta\"" }` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x3fa550` | `0x3ea550` | `os.go` | RUNTIME_STDLIB: OS Subsystem & Process | `HIGH` |
| `0x4be650` | `0x4ae650` | `os8.go` | RUNTIME_STDLIB: Standard Library | `HIGH` |
| `0x4c6c50` | `0x4b6c50` | `go.go` | RUNTIME_STDLIB: Standard Library | `HIGH` |
