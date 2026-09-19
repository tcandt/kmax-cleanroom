.class public final Lcom/android/helper/CoreService;
.super Ljava/lang/Object;
.source "CoreService.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/CoreService$Completion;
    }
.end annotation


# static fields
.field static final synthetic $assertionsDisabled:Z

.field public static final SERVER_PATH:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 44
    const-string v0, "java.class.path"

    invoke-static {v0}, Ljava/lang/System;->getProperty(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    sget-object v1, Ljava/io/File;->pathSeparator:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x0

    .line 46
    aget-object v0, v0, v1

    sput-object v0, Lcom/android/helper/CoreService;->SERVER_PATH:Ljava/lang/String;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 68
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static varargs internalMain([Ljava/lang/String;)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 267
    invoke-static {}, Lcom/android/helper/CoreService;->prepareMainLooper()V

    .line 268
    invoke-static {}, Lcom/android/helper/Workarounds;->apply()V

    .line 270
    invoke-static {}, Ljava/lang/Thread;->getDefaultUncaughtExceptionHandler()Ljava/lang/Thread$UncaughtExceptionHandler;

    move-result-object v0

    .line 271
    new-instance v1, Lcom/android/helper/CoreService$$ExternalSyntheticLambda1;

    invoke-direct {v1, v0}, Lcom/android/helper/CoreService$$ExternalSyntheticLambda1;-><init>(Ljava/lang/Thread$UncaughtExceptionHandler;)V

    invoke-static {v1}, Ljava/lang/Thread;->setDefaultUncaughtExceptionHandler(Ljava/lang/Thread$UncaughtExceptionHandler;)V

    .line 278
    invoke-static {}, Lcom/android/helper/CoreService;->prepareMainLooper()V

    .line 280
    invoke-static {p0}, Lcom/android/helper/Options;->parse([Ljava/lang/String;)Lcom/android/helper/Options;

    move-result-object p0

    .line 282
    invoke-static {}, Lcom/android/helper/util/Ln;->disableSystemStreams()V

    .line 283
    invoke-virtual {p0}, Lcom/android/helper/Options;->getLogLevel()Lcom/android/helper/util/Ln$Level;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->initLogLevel(Lcom/android/helper/util/Ln$Level;)V

    .line 285
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Device: ["

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    sget-object v1, Landroid/os/Build;->MANUFACTURER:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "] "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    sget-object v1, Landroid/os/Build;->BRAND:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, " "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    sget-object v1, Landroid/os/Build;->MODEL:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, " (Android "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    sget-object v1, Landroid/os/Build$VERSION;->RELEASE:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, ")"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 287
    invoke-virtual {p0}, Lcom/android/helper/Options;->getList()Z

    move-result v0

    if-eqz v0, :cond_6

    .line 288
    invoke-virtual {p0}, Lcom/android/helper/Options;->getCleanup()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 289
    invoke-static {}, Lcom/android/helper/CleanUp;->unlinkSelf()V

    .line 292
    :cond_0
    invoke-virtual {p0}, Lcom/android/helper/Options;->getListEncoders()Z

    move-result v0

    if-eqz v0, :cond_1

    .line 293
    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildVideoEncoderListMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 294
    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildAudioEncoderListMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 296
    :cond_1
    invoke-virtual {p0}, Lcom/android/helper/Options;->getListDisplays()Z

    move-result v0

    if-eqz v0, :cond_2

    .line 297
    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildDisplayListMessage()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 299
    :cond_2
    invoke-virtual {p0}, Lcom/android/helper/Options;->getListCameras()Z

    move-result v0

    if-nez v0, :cond_3

    invoke-virtual {p0}, Lcom/android/helper/Options;->getListCameraSizes()Z

    move-result v0

    if-eqz v0, :cond_4

    .line 300
    :cond_3
    invoke-static {}, Lcom/android/helper/Workarounds;->apply()V

    .line 301
    invoke-virtual {p0}, Lcom/android/helper/Options;->getListCameraSizes()Z

    move-result v0

    invoke-static {v0}, Lcom/android/helper/util/LogUtils;->buildCameraListMessage(Z)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 303
    :cond_4
    invoke-virtual {p0}, Lcom/android/helper/Options;->getListApps()Z

    move-result p0

    if-eqz p0, :cond_5

    .line 304
    invoke-static {}, Lcom/android/helper/Workarounds;->apply()V

    .line 305
    const-string p0, "Processing Android apps... (this may take some time)"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 306
    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildAppListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    :cond_5
    return-void

    .line 313
    :cond_6
    :try_start_0
    invoke-static {p0}, Lcom/android/helper/CoreService;->scrcpy(Lcom/android/helper/Options;)V
    :try_end_0
    .catch Lcom/android/helper/device/ConfigurationException; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0
    return-void
.end method

.method static synthetic lambda$internalMain$1(Ljava/lang/Thread$UncaughtExceptionHandler;Ljava/lang/Thread;Ljava/lang/Throwable;)V
    .locals 2

    .line 272
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Exception on thread "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0, p2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    if-eqz p0, :cond_0

    .line 274
    invoke-interface {p0, p1, p2}, Ljava/lang/Thread$UncaughtExceptionHandler;->uncaughtException(Ljava/lang/Thread;Ljava/lang/Throwable;)V

    :cond_0
    return-void
.end method

.method static synthetic lambda$scrcpy$0(Lcom/android/helper/CoreService$Completion;Z)V
    .locals 0

    .line 190
    invoke-virtual {p0, p1}, Lcom/android/helper/CoreService$Completion;->addCompleted(Z)V

    return-void
.end method

.method public static varargs main([Ljava/lang/String;)V
    .locals 2

    const/4 v0, 0x0

    .line 254
    :try_start_0
    invoke-static {p0}, Lcom/android/helper/CoreService;->internalMain([Ljava/lang/String;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 262
    invoke-static {v0}, Ljava/lang/System;->exit(I)V

    return-void

    :catchall_0
    move-exception p0

    .line 256
    :try_start_1
    invoke-virtual {p0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    const/4 p0, 0x1

    .line 262
    invoke-static {p0}, Ljava/lang/System;->exit(I)V

    return-void

    :catchall_1
    move-exception p0

    invoke-static {v0}, Ljava/lang/System;->exit(I)V

    .line 263
    throw p0
.end method

.method private static prepareMainLooper()V
    .locals 4

    .line 236
    invoke-static {}, Landroid/os/Looper;->myLooper()Landroid/os/Looper;

    move-result-object v0

    if-nez v0, :cond_0

    .line 237
    invoke-static {}, Landroid/os/Looper;->prepare()V

    .line 239
    :cond_0
    const-class v0, Landroid/os/Looper;

    monitor-enter v0

    .line 242
    :try_start_0
    const-class v1, Landroid/os/Looper;

    const-string v2, "sMainLooper"

    invoke-virtual {v1, v2}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v1

    const/4 v2, 0x1

    .line 243
    invoke-virtual {v1, v2}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 244
    invoke-static {}, Landroid/os/Looper;->myLooper()Landroid/os/Looper;

    move-result-object v2

    const/4 v3, 0x0

    invoke-virtual {v1, v3, v2}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 248
    :try_start_1
    monitor-exit v0

    return-void

    :catchall_0
    move-exception v1

    goto :goto_0

    :catch_0
    move-exception v1

    .line 246
    new-instance v2, Ljava/lang/AssertionError;

    invoke-direct {v2, v1}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v2

    .line 248
    :goto_0
    monitor-exit v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v1
.end method

.method private static scrcpy(Lcom/android/helper/Options;)V
    .locals 14
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Lcom/android/helper/device/ConfigurationException;
        }
    .end annotation

    .line 73
    const-string v0, "WakeLock released successfully"

    const-string v1, "Failed to release WakeLock"

    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v3, 0x1f

    if-ge v2, v3, :cond_1

    invoke-virtual {p0}, Lcom/android/helper/Options;->getVideoSource()Lcom/android/helper/video/VideoSource;

    move-result-object v2

    sget-object v3, Lcom/android/helper/video/VideoSource;->CAMERA:Lcom/android/helper/video/VideoSource;

    if-eq v2, v3, :cond_0

    goto :goto_0

    .line 74
    :cond_0
    const-string p0, "Camera mirroring is not supported before Android 12"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 75
    new-instance p0, Lcom/android/helper/device/ConfigurationException;

    const-string v0, "Camera mirroring is not supported"

    invoke-direct {p0, v0}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 78
    :cond_1
    :goto_0
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v3, 0x1d

    if-ge v2, v3, :cond_4

    .line 79
    invoke-virtual {p0}, Lcom/android/helper/Options;->getNewDisplay()Lcom/android/helper/device/NewDisplay;

    move-result-object v2

    if-nez v2, :cond_3

    .line 83
    invoke-virtual {p0}, Lcom/android/helper/Options;->getDisplayImePolicy()I

    move-result v2

    const/4 v3, -0x1

    if-ne v2, v3, :cond_2

    goto :goto_1

    .line 84
    :cond_2
    const-string p0, "Display IME policy is not supported before Android 10"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 85
    new-instance p0, Lcom/android/helper/device/ConfigurationException;

    const-string v0, "Display IME policy is not supported"

    invoke-direct {p0, v0}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 80
    :cond_3
    const-string p0, "New virtual display is not supported before Android 10"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 81
    new-instance p0, Lcom/android/helper/device/ConfigurationException;

    const-string v0, "New virtual display is not supported"

    invoke-direct {p0, v0}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 91
    :cond_4
    :goto_1
    invoke-virtual {p0}, Lcom/android/helper/Options;->getCleanup()Z

    move-result v2

    const/4 v3, 0x0

    if-eqz v2, :cond_5

    .line 92
    invoke-static {p0}, Lcom/android/helper/CleanUp;->start(Lcom/android/helper/Options;)Lcom/android/helper/CleanUp;

    move-result-object v2

    goto :goto_2

    :cond_5
    move-object v2, v3

    .line 95
    :goto_2
    invoke-virtual {p0}, Lcom/android/helper/Options;->getScid()I

    .line 96
    invoke-virtual {p0}, Lcom/android/helper/Options;->isTunnelForward()Z

    .line 97
    invoke-virtual {p0}, Lcom/android/helper/Options;->getControl()Z

    move-result v4

    .line 98
    invoke-virtual {p0}, Lcom/android/helper/Options;->getVideo()Z

    move-result v5

    .line 99
    invoke-virtual {p0}, Lcom/android/helper/Options;->getAudio()Z

    move-result v6

    .line 100
    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendDummyByte()Z

    .line 102
    invoke-static {}, Lcom/android/helper/Workarounds;->apply()V

    .line 105
    invoke-virtual {p0}, Lcom/android/helper/Options;->getStayAwake()Z

    move-result v7

    if-eqz v7, :cond_7

    .line 107
    :try_start_0
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v7

    const-string v8, "power"

    invoke-virtual {v7, v8}, Lcom/android/helper/FakeContext;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v7

    check-cast v7, Landroid/os/PowerManager;

    if-eqz v7, :cond_6

    .line 109
    const-string v8, "scrcpy:stay_awake"

    const v9, 0x3000001a

    invoke-virtual {v7, v9, v8}, Landroid/os/PowerManager;->newWakeLock(ILjava/lang/String;)Landroid/os/PowerManager$WakeLock;

    move-result-object v7
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_1

    .line 110
    :try_start_1
    invoke-virtual {v7}, Landroid/os/PowerManager$WakeLock;->acquire()V

    .line 111
    const-string v8, "WakeLock acquired successfully to keep device awake"

    invoke-static {v8}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_5

    :catchall_0
    move-exception v8

    goto :goto_3

    .line 113
    :cond_6
    :try_start_2
    const-string v7, "PowerManager is null, cannot acquire WakeLock"

    invoke-static {v7}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_1

    goto :goto_4

    :catchall_1
    move-exception v8

    move-object v7, v3

    .line 116
    :goto_3
    const-string v9, "Failed to acquire WakeLock"

    invoke-static {v9, v8}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    goto :goto_5

    :cond_7
    :goto_4
    move-object v7, v3

    .line 120
    :goto_5
    new-instance v8, Ljava/util/ArrayList;

    invoke-direct {v8}, Ljava/util/ArrayList;-><init>()V

    .line 122
    invoke-static {p0}, Lcom/android/helper/device/DesktopConnection;->open(Lcom/android/helper/Options;)Lcom/android/helper/device/DesktopConnection;

    move-result-object v9

    .line 124
    :try_start_3
    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendDeviceMeta()Z

    move-result v10

    if-eqz v10, :cond_8

    .line 125
    invoke-static {}, Lcom/android/helper/device/Device;->getDeviceName()Ljava/lang/String;

    move-result-object v10

    invoke-virtual {v9, v10}, Lcom/android/helper/device/DesktopConnection;->sendDeviceMeta(Ljava/lang/String;)V

    :cond_8
    if-eqz v4, :cond_a

    .line 132
    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->getControlChannel()Lcom/android/helper/control/ControlChannel;

    move-result-object v3

    .line 133
    new-instance v4, Lcom/android/helper/control/Controller;

    invoke-direct {v4, v3, v2, p0}, Lcom/android/helper/control/Controller;-><init>(Lcom/android/helper/control/ControlChannel;Lcom/android/helper/CleanUp;Lcom/android/helper/Options;)V

    .line 134
    invoke-interface {v8, v4}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 137
    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->getTouchChannel()Lcom/android/helper/control/ControlChannel;

    move-result-object v3

    if-eqz v3, :cond_9

    .line 139
    new-instance v10, Lcom/android/helper/control/Controller;

    invoke-direct {v10, v3, v2, p0}, Lcom/android/helper/control/Controller;-><init>(Lcom/android/helper/control/ControlChannel;Lcom/android/helper/CleanUp;Lcom/android/helper/Options;)V

    .line 140
    invoke-interface {v8, v10}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    :cond_9
    move-object v3, v4

    :cond_a
    if-eqz v6, :cond_d

    .line 145
    invoke-virtual {p0}, Lcom/android/helper/Options;->getAudioCodec()Lcom/android/helper/audio/AudioCodec;

    move-result-object v4

    .line 146
    invoke-virtual {p0}, Lcom/android/helper/Options;->getAudioSource()Lcom/android/helper/audio/AudioSource;

    move-result-object v6

    .line 148
    invoke-virtual {v6}, Lcom/android/helper/audio/AudioSource;->isDirect()Z

    move-result v10

    if-eqz v10, :cond_b

    .line 149
    new-instance v10, Lcom/android/helper/audio/AudioDirectCapture;

    invoke-direct {v10, v6}, Lcom/android/helper/audio/AudioDirectCapture;-><init>(Lcom/android/helper/audio/AudioSource;)V

    goto :goto_6

    .line 151
    :cond_b
    new-instance v10, Lcom/android/helper/audio/AudioPlaybackCapture;

    invoke-virtual {p0}, Lcom/android/helper/Options;->getAudioDup()Z

    move-result v6

    invoke-direct {v10, v6}, Lcom/android/helper/audio/AudioPlaybackCapture;-><init>(Z)V

    .line 154
    :goto_6
    new-instance v6, Lcom/android/helper/device/Streamer;

    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->getAudioFd()Ljava/io/FileDescriptor;

    move-result-object v11

    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendCodecMeta()Z

    move-result v12

    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendFrameMeta()Z

    move-result v13

    invoke-direct {v6, v11, v4, v12, v13}, Lcom/android/helper/device/Streamer;-><init>(Ljava/io/FileDescriptor;Lcom/android/helper/util/Codec;ZZ)V

    .line 156
    sget-object v11, Lcom/android/helper/audio/AudioCodec;->RAW:Lcom/android/helper/audio/AudioCodec;

    if-ne v4, v11, :cond_c

    .line 157
    new-instance v4, Lcom/android/helper/audio/AudioRawRecorder;

    invoke-direct {v4, v10, v6}, Lcom/android/helper/audio/AudioRawRecorder;-><init>(Lcom/android/helper/audio/AudioCapture;Lcom/android/helper/device/Streamer;)V

    goto :goto_7

    .line 159
    :cond_c
    new-instance v4, Lcom/android/helper/audio/AudioEncoder;

    invoke-direct {v4, v10, v6, p0}, Lcom/android/helper/audio/AudioEncoder;-><init>(Lcom/android/helper/audio/AudioCapture;Lcom/android/helper/device/Streamer;Lcom/android/helper/Options;)V

    .line 161
    :goto_7
    invoke-interface {v8, v4}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    :cond_d
    if-eqz v5, :cond_10

    .line 165
    new-instance v4, Lcom/android/helper/device/Streamer;

    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->getVideoFd()Ljava/io/FileDescriptor;

    move-result-object v5

    invoke-virtual {p0}, Lcom/android/helper/Options;->getVideoCodec()Lcom/android/helper/video/VideoCodec;

    move-result-object v6

    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendCodecMeta()Z

    move-result v10

    .line 166
    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendFrameMeta()Z

    move-result v11

    invoke-direct {v4, v5, v6, v10, v11}, Lcom/android/helper/device/Streamer;-><init>(Ljava/io/FileDescriptor;Lcom/android/helper/util/Codec;ZZ)V

    .line 168
    invoke-virtual {p0}, Lcom/android/helper/Options;->getVideoSource()Lcom/android/helper/video/VideoSource;

    move-result-object v5

    sget-object v6, Lcom/android/helper/video/VideoSource;->DISPLAY:Lcom/android/helper/video/VideoSource;

    if-ne v5, v6, :cond_f

    .line 169
    invoke-virtual {p0}, Lcom/android/helper/Options;->getNewDisplay()Lcom/android/helper/device/NewDisplay;

    move-result-object v5

    if-eqz v5, :cond_e

    .line 171
    new-instance v5, Lcom/android/helper/video/NewDisplayCapture;

    invoke-direct {v5, v3, p0}, Lcom/android/helper/video/NewDisplayCapture;-><init>(Lcom/android/helper/video/VirtualDisplayListener;Lcom/android/helper/Options;)V

    goto :goto_8

    .line 174
    :cond_e
    new-instance v5, Lcom/android/helper/video/ScreenCapture;

    invoke-direct {v5, v3, p0}, Lcom/android/helper/video/ScreenCapture;-><init>(Lcom/android/helper/video/VirtualDisplayListener;Lcom/android/helper/Options;)V

    goto :goto_8

    .line 177
    :cond_f
    new-instance v5, Lcom/android/helper/video/CameraCapture;

    invoke-direct {v5, p0}, Lcom/android/helper/video/CameraCapture;-><init>(Lcom/android/helper/Options;)V

    .line 179
    :goto_8
    new-instance v6, Lcom/android/helper/video/SurfaceEncoder;

    invoke-direct {v6, v5, v4, p0}, Lcom/android/helper/video/SurfaceEncoder;-><init>(Lcom/android/helper/video/SurfaceCapture;Lcom/android/helper/device/Streamer;Lcom/android/helper/Options;)V

    .line 180
    invoke-interface {v8, v6}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    if-eqz v3, :cond_10

    .line 183
    invoke-virtual {v3, v5}, Lcom/android/helper/control/Controller;->setSurfaceCapture(Lcom/android/helper/video/SurfaceCapture;)V

    .line 187
    :cond_10
    new-instance p0, Lcom/android/helper/CoreService$Completion;

    invoke-interface {v8}, Ljava/util/List;->size()I

    move-result v3

    invoke-direct {p0, v3}, Lcom/android/helper/CoreService$Completion;-><init>(I)V

    .line 188
    invoke-interface {v8}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v3

    :goto_9
    invoke-interface {v3}, Ljava/util/Iterator;->hasNext()Z

    move-result v4

    if-eqz v4, :cond_11

    invoke-interface {v3}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Lcom/android/helper/AsyncProcessor;

    .line 189
    new-instance v5, Lcom/android/helper/CoreService$$ExternalSyntheticLambda0;

    invoke-direct {v5, p0}, Lcom/android/helper/CoreService$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/CoreService$Completion;)V

    invoke-interface {v4, v5}, Lcom/android/helper/AsyncProcessor;->start(Lcom/android/helper/AsyncProcessor$TerminationListener;)V

    goto :goto_9

    .line 194
    :cond_11
    invoke-static {}, Landroid/os/Looper;->loop()V
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_3

    if-eqz v7, :cond_12

    .line 198
    :try_start_4
    invoke-virtual {v7}, Landroid/os/PowerManager$WakeLock;->isHeld()Z

    move-result p0

    if-eqz p0, :cond_12

    .line 199
    invoke-virtual {v7}, Landroid/os/PowerManager$WakeLock;->release()V

    .line 200
    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V
    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_2

    goto :goto_a

    :catchall_2
    move-exception p0

    .line 203
    invoke-static {v1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_12
    :goto_a
    if-eqz v2, :cond_13

    .line 208
    invoke-virtual {v2}, Lcom/android/helper/CleanUp;->interrupt()V

    .line 210
    :cond_13
    invoke-interface {v8}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object p0

    :goto_b
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-eqz v0, :cond_14

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/android/helper/AsyncProcessor;

    .line 211
    invoke-interface {v0}, Lcom/android/helper/AsyncProcessor;->stop()V

    goto :goto_b

    .line 214
    :cond_14
    invoke-static {}, Lcom/android/helper/opengl/OpenGLRunner;->quit()V

    .line 216
    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->shutdown()V

    if-eqz v2, :cond_15

    .line 220
    :try_start_5
    invoke-virtual {v2}, Lcom/android/helper/CleanUp;->join()V

    .line 222
    :cond_15
    invoke-interface {v8}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object p0

    :goto_c
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    move-result v0

    if-eqz v0, :cond_16

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/android/helper/AsyncProcessor;

    .line 223
    invoke-interface {v0}, Lcom/android/helper/AsyncProcessor;->join()V

    goto :goto_c

    .line 225
    :cond_16
    invoke-static {}, Lcom/android/helper/opengl/OpenGLRunner;->join()V
    :try_end_5
    .catch Ljava/lang/InterruptedException; {:try_start_5 .. :try_end_5} :catch_0

    .line 230
    :catch_0
    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->close()V

    return-void

    :catchall_3
    move-exception p0

    if-eqz v7, :cond_17

    .line 198
    :try_start_6
    invoke-virtual {v7}, Landroid/os/PowerManager$WakeLock;->isHeld()Z

    move-result v3

    if-eqz v3, :cond_17

    .line 199
    invoke-virtual {v7}, Landroid/os/PowerManager$WakeLock;->release()V

    .line 200
    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V
    :try_end_6
    .catchall {:try_start_6 .. :try_end_6} :catchall_4

    goto :goto_d

    :catchall_4
    move-exception v0

    .line 203
    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_17
    :goto_d
    if-eqz v2, :cond_18

    .line 208
    invoke-virtual {v2}, Lcom/android/helper/CleanUp;->interrupt()V

    .line 210
    :cond_18
    invoke-interface {v8}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v0

    :goto_e
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v1

    if-eqz v1, :cond_19

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/android/helper/AsyncProcessor;

    .line 211
    invoke-interface {v1}, Lcom/android/helper/AsyncProcessor;->stop()V

    goto :goto_e

    .line 214
    :cond_19
    invoke-static {}, Lcom/android/helper/opengl/OpenGLRunner;->quit()V

    .line 216
    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->shutdown()V

    if-eqz v2, :cond_1a

    .line 220
    :try_start_7
    invoke-virtual {v2}, Lcom/android/helper/CleanUp;->join()V

    .line 222
    :cond_1a
    invoke-interface {v8}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v0

    :goto_f
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v1

    if-eqz v1, :cond_1b

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/android/helper/AsyncProcessor;

    .line 223
    invoke-interface {v1}, Lcom/android/helper/AsyncProcessor;->join()V

    goto :goto_f

    .line 225
    :cond_1b
    invoke-static {}, Lcom/android/helper/opengl/OpenGLRunner;->join()V
    :try_end_7
    .catch Ljava/lang/InterruptedException; {:try_start_7 .. :try_end_7} :catch_1

    .line 230
    :catch_1
    invoke-virtual {v9}, Lcom/android/helper/device/DesktopConnection;->close()V

    .line 231
    throw p0
.end method
