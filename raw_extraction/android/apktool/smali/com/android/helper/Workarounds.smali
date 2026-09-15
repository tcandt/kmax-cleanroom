.class public final Lcom/android/helper/Workarounds;
.super Ljava/lang/Object;
.source "Workarounds.java"


# static fields
.field private static final ACTIVITY_THREAD:Ljava/lang/Object;

.field private static final ACTIVITY_THREAD_CLASS:Ljava/lang/Class;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/Class<",
            "*>;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .locals 5

    .line 34
    :try_start_0
    const-string v0, "android.app.ActivityThread"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    sput-object v0, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD_CLASS:Ljava/lang/Class;

    const/4 v1, 0x0

    .line 35
    invoke-virtual {v0, v1}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v2

    const/4 v3, 0x1

    .line 36
    invoke-virtual {v2, v3}, Ljava/lang/reflect/Constructor;->setAccessible(Z)V

    .line 37
    invoke-virtual {v2, v1}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    sput-object v2, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD:Ljava/lang/Object;

    .line 40
    const-string v4, "sCurrentActivityThread"

    invoke-virtual {v0, v4}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v4

    .line 41
    invoke-virtual {v4, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 42
    invoke-virtual {v4, v1, v2}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 45
    const-string v1, "mSystemThread"

    invoke-virtual {v0, v1}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    .line 46
    invoke-virtual {v0, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 47
    invoke-virtual {v0, v2, v3}, Ljava/lang/reflect/Field;->setBoolean(Ljava/lang/Object;Z)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 49
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1
.end method

.method private constructor <init>()V
    .locals 0

    .line 53
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static apply()V
    .locals 2

    .line 58
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1f

    if-lt v0, v1, :cond_0

    .line 64
    invoke-static {}, Lcom/android/helper/Workarounds;->fillConfigurationController()V

    .line 69
    :cond_0
    sget-object v0, Landroid/os/Build;->BRAND:Ljava/lang/String;

    const-string v1, "ONYX"

    invoke-virtual {v0, v1}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_1

    .line 72
    invoke-static {}, Lcom/android/helper/Workarounds;->fillAppInfo()V

    .line 75
    :cond_1
    invoke-static {}, Lcom/android/helper/Workarounds;->fillAppContext()V

    return-void
.end method

.method public static createAudioRecord(IIIIII)Landroid/media/AudioRecord;
    .locals 27
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 159
    const-string v1, "Cannot create AudioRecord"

    .line 0
    const-string v0, "Error code "

    .line 159
    :try_start_0
    const-class v2, Landroid/media/AudioRecord;

    const/4 v3, 0x1

    new-array v4, v3, [Ljava/lang/Class;

    sget-object v5, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    const/4 v6, 0x0

    aput-object v5, v4, v6

    invoke-virtual {v2, v4}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v2

    .line 160
    invoke-virtual {v2, v3}, Ljava/lang/reflect/Constructor;->setAccessible(Z)V

    const-wide/16 v4, 0x0

    .line 161
    invoke-static {v4, v5}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v7

    new-array v8, v3, [Ljava/lang/Object;

    aput-object v7, v8, v6

    invoke-virtual {v2, v8}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Landroid/media/AudioRecord;

    .line 164
    const-class v7, Landroid/media/AudioRecord;

    const-string v8, "mRecordingState"

    invoke-virtual {v7, v8}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v7

    .line 165
    invoke-virtual {v7, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 166
    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v8

    invoke-virtual {v7, v2, v8}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 168
    invoke-static {}, Landroid/os/Looper;->myLooper()Landroid/os/Looper;

    move-result-object v7

    if-nez v7, :cond_0

    .line 170
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    move-result-object v7

    .line 174
    :cond_0
    const-class v8, Landroid/media/AudioRecord;

    const-string v9, "mInitializationLooper"

    invoke-virtual {v8, v9}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v8

    .line 175
    invoke-virtual {v8, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 176
    invoke-virtual {v8, v2, v7}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 180
    new-instance v7, Landroid/media/AudioAttributes$Builder;

    invoke-direct {v7}, Landroid/media/AudioAttributes$Builder;-><init>()V

    .line 181
    const-class v8, Landroid/media/AudioAttributes$Builder;

    const-string v9, "setInternalCapturePreset"

    new-array v10, v3, [Ljava/lang/Class;

    sget-object v11, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v11, v10, v6

    invoke-virtual {v8, v9, v10}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v8

    .line 182
    invoke-static/range {p0 .. p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    new-array v10, v3, [Ljava/lang/Object;

    aput-object v9, v10, v6

    invoke-virtual {v8, v7, v10}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 183
    invoke-virtual {v7}, Landroid/media/AudioAttributes$Builder;->build()Landroid/media/AudioAttributes;

    move-result-object v7

    .line 186
    const-class v8, Landroid/media/AudioRecord;

    const-string v9, "mAudioAttributes"

    invoke-virtual {v8, v9}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v8

    .line 187
    invoke-virtual {v8, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 188
    invoke-virtual {v8, v2, v7}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 191
    const-class v8, Landroid/media/AudioRecord;

    const-string v9, "audioParamCheck"

    const/4 v10, 0x3

    new-array v11, v10, [Ljava/lang/Class;

    sget-object v12, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v12, v11, v6

    aput-object v12, v11, v3

    const/4 v13, 0x2

    aput-object v12, v11, v13

    invoke-virtual {v8, v9, v11}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v8

    .line 192
    invoke-virtual {v8, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 193
    invoke-static/range {p0 .. p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    invoke-static/range {p1 .. p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v11

    invoke-static/range {p5 .. p5}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v12

    new-array v14, v10, [Ljava/lang/Object;

    aput-object v9, v14, v6

    aput-object v11, v14, v3

    aput-object v12, v14, v13

    invoke-virtual {v8, v2, v14}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 196
    const-class v8, Landroid/media/AudioRecord;

    const-string v9, "mChannelCount"

    invoke-virtual {v8, v9}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v8

    .line 197
    invoke-virtual {v8, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 198
    invoke-static/range {p3 .. p3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    invoke-virtual {v8, v2, v9}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 201
    const-class v8, Landroid/media/AudioRecord;

    const-string v9, "mChannelMask"

    invoke-virtual {v8, v9}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v8

    .line 202
    invoke-virtual {v8, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 203
    invoke-static/range {p4 .. p4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    invoke-virtual {v8, v2, v9}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    move/from16 v8, p1

    move/from16 v9, p2

    move/from16 v11, p5

    .line 205
    invoke-static {v8, v9, v11}, Landroid/media/AudioRecord;->getMinBufferSize(III)I

    move-result v9

    const/16 v11, 0x8

    mul-int/lit8 v9, v9, 0x8

    .line 209
    const-class v12, Landroid/media/AudioRecord;

    const-string v14, "audioBuffSizeCheck"

    new-array v15, v3, [Ljava/lang/Class;

    sget-object v16, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v16, v15, v6

    invoke-virtual {v12, v14, v15}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v12

    .line 210
    invoke-virtual {v12, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 211
    invoke-static {v9}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v14

    new-array v15, v3, [Ljava/lang/Object;

    aput-object v14, v15, v6

    invoke-virtual {v12, v2, v15}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 215
    filled-new-array {v8}, [I

    move-result-object v8

    .line 216
    filled-new-array {v6}, [I

    move-result-object v12

    .line 219
    sget v14, Landroid/os/Build$VERSION;->SDK_INT:I
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    const/16 v15, 0x1f

    const-class v16, [I

    move-wide/from16 v17, v4

    const-string v4, "native_setup"

    const/16 v19, 0x7

    const/16 v20, 0x6

    const/16 v21, 0x5

    const/16 v22, 0x4

    const/16 p0, 0x9

    const/16 v5, 0xa

    if-ge v14, v15, :cond_1

    .line 225
    :try_start_1
    const-class v14, Landroid/media/AudioRecord;

    new-array v15, v5, [Ljava/lang/Class;

    const-class v23, Ljava/lang/Object;

    aput-object v23, v15, v6

    aput-object v23, v15, v3

    aput-object v16, v15, v13

    sget-object v23, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v23, v15, v10

    aput-object v23, v15, v22

    aput-object v23, v15, v21

    aput-object v23, v15, v20

    aput-object v16, v15, v19

    const-class v16, Ljava/lang/String;

    aput-object v16, v15, v11

    sget-object v16, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    aput-object v16, v15, p0

    invoke-virtual {v14, v4, v15}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    .line 227
    invoke-virtual {v4, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 228
    new-instance v14, Ljava/lang/ref/WeakReference;

    invoke-direct {v14, v2}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    .line 229
    invoke-static/range {p4 .. p4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v15

    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v16

    invoke-virtual {v2}, Landroid/media/AudioRecord;->getAudioFormat()I

    move-result v23

    invoke-static/range {v23 .. v23}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v23

    invoke-static {v9}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v24

    invoke-virtual/range {v24 .. v24}, Lcom/android/helper/FakeContext;->getOpPackageName()Ljava/lang/String;

    move-result-object v24

    .line 230
    invoke-static/range {v17 .. v18}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v17

    new-array v5, v5, [Ljava/lang/Object;

    aput-object v14, v5, v6

    aput-object v7, v5, v3

    aput-object v8, v5, v13

    aput-object v15, v5, v10

    aput-object v16, v5, v22

    aput-object v23, v5, v21

    aput-object v9, v5, v20

    aput-object v12, v5, v19

    aput-object v24, v5, v11

    aput-object v17, v5, p0

    .line 228
    invoke-virtual {v4, v2, v5}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/lang/Integer;

    invoke-virtual {v4}, Ljava/lang/Integer;->intValue()I

    move-result v4

    const/16 v23, 0x0

    goto/16 :goto_1

    .line 233
    :cond_1
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v14

    invoke-virtual {v14}, Lcom/android/helper/FakeContext;->getAttributionSource()Landroid/content/AttributionSource;

    move-result-object v14

    .line 238
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Ljava/lang/Class;

    move-result-object v15

    const/16 p1, 0xa

    const-string v5, "asScopedParcelState"

    const/16 v23, 0x0

    const/4 v6, 0x0

    invoke-virtual {v15, v5, v6}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v5

    .line 239
    invoke-virtual {v5, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 241
    invoke-virtual {v5, v14, v6}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Ljava/lang/AutoCloseable;
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    .line 242
    :try_start_2
    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v14

    const-string v15, "getParcel"

    invoke-virtual {v14, v15, v6}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v14

    .line 243
    invoke-virtual {v14, v5, v6}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v6

    check-cast v6, Landroid/os/Parcel;

    .line 245
    sget v14, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v15, 0x22

    const/16 v24, 0x3

    const/16 v10, 0xb

    if-ge v14, v15, :cond_2

    .line 251
    const-class v14, Landroid/media/AudioRecord;

    new-array v15, v10, [Ljava/lang/Class;

    const-class v25, Ljava/lang/Object;

    aput-object v25, v15, v23

    aput-object v25, v15, v3

    aput-object v16, v15, v13

    sget-object v25, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v25, v15, v24

    aput-object v25, v15, v22

    aput-object v25, v15, v21

    aput-object v25, v15, v20

    aput-object v16, v15, v19

    const-class v16, Landroid/os/Parcel;

    aput-object v16, v15, v11

    sget-object v16, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    aput-object v16, v15, p0

    aput-object v25, v15, p1

    invoke-virtual {v14, v4, v15}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    .line 253
    invoke-virtual {v4, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 254
    new-instance v14, Ljava/lang/ref/WeakReference;

    invoke-direct {v14, v2}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    .line 255
    invoke-static/range {p4 .. p4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v15

    invoke-static/range {v23 .. v23}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v16

    invoke-virtual {v2}, Landroid/media/AudioRecord;->getAudioFormat()I

    move-result v25

    invoke-static/range {v25 .. v25}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v25

    invoke-static {v9}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    .line 256
    invoke-static/range {v17 .. v18}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v17

    invoke-static/range {v23 .. v23}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v18

    new-array v10, v10, [Ljava/lang/Object;

    aput-object v14, v10, v23

    aput-object v7, v10, v3

    aput-object v8, v10, v13

    aput-object v15, v10, v24

    aput-object v16, v10, v22

    aput-object v25, v10, v21

    aput-object v9, v10, v20

    aput-object v12, v10, v19

    aput-object v6, v10, v11

    aput-object v17, v10, p0

    aput-object v18, v10, p1

    .line 254
    invoke-virtual {v4, v2, v10}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/lang/Integer;

    invoke-virtual {v4}, Ljava/lang/Integer;->intValue()I

    move-result v4

    goto :goto_0

    .line 260
    :cond_2
    const-class v14, Landroid/media/AudioRecord;

    const/16 v15, 0xc

    const/16 p2, 0xb

    new-array v10, v15, [Ljava/lang/Class;

    const-class v25, Ljava/lang/Object;

    aput-object v25, v10, v23

    aput-object v25, v10, v3

    aput-object v16, v10, v13

    sget-object v25, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v25, v10, v24

    aput-object v25, v10, v22

    aput-object v25, v10, v21

    aput-object v25, v10, v20

    aput-object v16, v10, v19

    const-class v16, Landroid/os/Parcel;

    aput-object v16, v10, v11

    sget-object v16, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    aput-object v16, v10, p0

    aput-object v25, v10, p1

    aput-object v25, v10, p2

    invoke-virtual {v14, v4, v10}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    .line 262
    invoke-virtual {v4, v3}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 263
    new-instance v10, Ljava/lang/ref/WeakReference;

    invoke-direct {v10, v2}, Ljava/lang/ref/WeakReference;-><init>(Ljava/lang/Object;)V

    .line 264
    invoke-static/range {p4 .. p4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v14

    invoke-static/range {v23 .. v23}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v16

    invoke-virtual {v2}, Landroid/media/AudioRecord;->getAudioFormat()I

    move-result v25

    invoke-static/range {v25 .. v25}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v25

    invoke-static {v9}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v9

    .line 265
    invoke-static/range {v17 .. v18}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object v17

    invoke-static/range {v23 .. v23}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v18

    invoke-static/range {v23 .. v23}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v26

    new-array v15, v15, [Ljava/lang/Object;

    aput-object v10, v15, v23

    aput-object v7, v15, v3

    aput-object v8, v15, v13

    aput-object v14, v15, v24

    aput-object v16, v15, v22

    aput-object v25, v15, v21

    aput-object v9, v15, v20

    aput-object v12, v15, v19

    aput-object v6, v15, v11

    aput-object v17, v15, p0

    aput-object v18, v15, p1

    aput-object v26, v15, p2

    .line 263
    invoke-virtual {v4, v2, v15}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/lang/Integer;

    invoke-virtual {v4}, Ljava/lang/Integer;->intValue()I

    move-result v4
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    :goto_0
    if-eqz v5, :cond_3

    .line 267
    :try_start_3
    invoke-static {v5}, Lcom/android/helper/Workarounds$$ExternalSyntheticThrowIAE3;->m(Ljava/lang/Object;)V

    :cond_3
    :goto_1
    if-nez v4, :cond_4

    .line 276
    const-class v0, Landroid/media/AudioRecord;

    const-string v4, "mSampleRate"

    invoke-virtual {v0, v4}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    .line 277
    invoke-virtual {v0, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 278
    aget v4, v8, v23

    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v4

    invoke-virtual {v0, v2, v4}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 281
    const-class v0, Landroid/media/AudioRecord;

    const-string v4, "mSessionId"

    invoke-virtual {v0, v4}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    .line 282
    invoke-virtual {v0, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 283
    aget v4, v12, v23

    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v4

    invoke-virtual {v0, v2, v4}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 286
    const-class v0, Landroid/media/AudioRecord;

    const-string v4, "mState"

    invoke-virtual {v0, v4}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    .line 287
    invoke-virtual {v0, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 288
    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    invoke-virtual {v0, v2, v3}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    return-object v2

    .line 271
    :cond_4
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, " when initializing native AudioRecord object."

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 272
    new-instance v0, Ljava/lang/RuntimeException;

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_3
    .catch Ljava/lang/Exception; {:try_start_3 .. :try_end_3} :catch_0

    :catchall_0
    move-exception v0

    move-object v2, v0

    if-eqz v5, :cond_5

    .line 241
    :try_start_4
    invoke-static {v5}, Lcom/android/helper/Workarounds$$ExternalSyntheticThrowIAE3;->m(Ljava/lang/Object;)V
    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_1

    goto :goto_2

    :catchall_1
    move-exception v0

    :try_start_5
    invoke-virtual {v2, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_5
    :goto_2
    throw v2
    :try_end_5
    .catch Ljava/lang/Exception; {:try_start_5 .. :try_end_5} :catch_0

    :catch_0
    move-exception v0

    .line 292
    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 293
    new-instance v0, Lcom/android/helper/audio/AudioCaptureException;

    invoke-direct {v0}, Lcom/android/helper/audio/AudioCaptureException;-><init>()V

    throw v0
.end method

.method private static fillAppContext()V
    .locals 3

    .line 106
    :try_start_0
    const-class v0, Landroid/app/Application;

    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v1

    invoke-static {v0, v1}, Landroid/app/Instrumentation;->newApplication(Ljava/lang/Class;Landroid/content/Context;)Landroid/app/Application;

    move-result-object v0

    .line 109
    sget-object v1, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD_CLASS:Ljava/lang/Class;

    const-string v2, "mInitialApplication"

    invoke-virtual {v1, v2}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v1

    const/4 v2, 0x1

    .line 110
    invoke-virtual {v1, v2}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 111
    sget-object v2, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD:Ljava/lang/Object;

    invoke-virtual {v1, v2, v0}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-void

    :catchall_0
    move-exception v0

    .line 114
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Could not fill app context: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    return-void
.end method

.method private static fillAppInfo()V
    .locals 5

    .line 81
    :try_start_0
    const-string v0, "android.app.ActivityThread$AppBindData"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x0

    .line 82
    invoke-virtual {v0, v1}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v2

    const/4 v3, 0x1

    .line 83
    invoke-virtual {v2, v3}, Ljava/lang/reflect/Constructor;->setAccessible(Z)V

    .line 84
    invoke-virtual {v2, v1}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    .line 86
    new-instance v2, Landroid/content/pm/ApplicationInfo;

    invoke-direct {v2}, Landroid/content/pm/ApplicationInfo;-><init>()V

    .line 87
    const-string v4, "com.android.shell"

    iput-object v4, v2, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    .line 90
    const-string v4, "appInfo"

    invoke-virtual {v0, v4}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    .line 91
    invoke-virtual {v0, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 92
    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V

    .line 95
    sget-object v0, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD_CLASS:Ljava/lang/Class;

    const-string v2, "mBoundApplication"

    invoke-virtual {v0, v2}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v0

    .line 96
    invoke-virtual {v0, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 97
    sget-object v2, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD:Ljava/lang/Object;

    invoke-virtual {v0, v2, v1}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-void

    :catchall_0
    move-exception v0

    .line 100
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Could not fill app info: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    return-void
.end method

.method private static fillConfigurationController()V
    .locals 5

    .line 120
    :try_start_0
    const-string v0, "android.app.ConfigurationController"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 121
    const-string v1, "android.app.ActivityThreadInternal"

    invoke-static {v1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v1

    const/4 v2, 0x1

    .line 124
    new-array v3, v2, [Ljava/lang/Class;

    const/4 v4, 0x0

    aput-object v1, v3, v4

    invoke-virtual {v0, v3}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v0

    .line 125
    invoke-virtual {v0, v2}, Ljava/lang/reflect/Constructor;->setAccessible(Z)V

    .line 126
    sget-object v1, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD:Ljava/lang/Object;

    new-array v3, v2, [Ljava/lang/Object;

    aput-object v1, v3, v4

    invoke-virtual {v0, v3}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    .line 129
    sget-object v3, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD_CLASS:Ljava/lang/Class;

    const-string v4, "mConfigurationController"

    invoke-virtual {v3, v4}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v3

    .line 130
    invoke-virtual {v3, v2}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 131
    invoke-virtual {v3, v1, v0}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-void

    :catchall_0
    move-exception v0

    .line 133
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Could not fill configuration: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    return-void
.end method

.method static getSystemContext()Landroid/content/Context;
    .locals 4

    const/4 v0, 0x0

    .line 139
    :try_start_0
    sget-object v1, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD_CLASS:Ljava/lang/Class;

    const-string v2, "getSystemContext"

    invoke-virtual {v1, v2, v0}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    .line 140
    sget-object v2, Lcom/android/helper/Workarounds;->ACTIVITY_THREAD:Ljava/lang/Object;

    invoke-virtual {v1, v2, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/content/Context;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-object v1

    :catchall_0
    move-exception v1

    .line 143
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Could not get system context: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    return-object v0
.end method
