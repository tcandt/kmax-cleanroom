.class public final Lcom/android/helper/audio/AudioPlaybackCapture;
.super Ljava/lang/Object;
.source "AudioPlaybackCapture.java"

# interfaces
.implements Lcom/android/helper/audio/AudioCapture;


# instance fields
.field private fallbackDirectCapture:Lcom/android/helper/audio/AudioCapture;

.field private final keepPlayingOnDevice:Z

.field private reader:Lcom/android/helper/audio/AudioRecordReader;

.field private recorder:Landroid/media/AudioRecord;


# direct methods
.method public constructor <init>(Z)V
    .locals 0

    .line 27
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 28
    iput-boolean p1, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->keepPlayingOnDevice:Z

    return-void
.end method

.method private createAudioRecord()Landroid/media/AudioRecord;
    .locals 15
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 35
    const-string v0, "build"

    :try_start_0
    const-string v1, "android.media.audiopolicy.AudioMixingRule"

    invoke-static {v1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v1

    .line 36
    const-string v2, "android.media.audiopolicy.AudioMixingRule$Builder"

    invoke-static {v2}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v2

    const/4 v3, 0x0

    .line 39
    invoke-virtual {v2, v3}, Ljava/lang/Class;->getConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v4

    invoke-virtual {v4, v3}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    .line 42
    const-string v5, "MIX_ROLE_PLAYERS"

    invoke-virtual {v1, v5}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v5

    invoke-virtual {v5, v3}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result v5

    .line 43
    const-string v6, "setTargetMixRole"

    const/4 v7, 0x1

    new-array v8, v7, [Ljava/lang/Class;

    sget-object v9, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v10, 0x0

    aput-object v9, v8, v10

    invoke-virtual {v2, v6, v8}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v6

    .line 44
    invoke-static {v5}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v5

    new-array v8, v7, [Ljava/lang/Object;

    aput-object v5, v8, v10

    invoke-virtual {v6, v4, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 46
    const-string v5, "RULE_MATCH_ATTRIBUTE_USAGE"

    invoke-virtual {v1, v5}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v5

    invoke-virtual {v5, v3}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result v5

    .line 47
    const-string v6, "addMixRule"

    const/4 v8, 0x2

    new-array v9, v8, [Ljava/lang/Class;

    sget-object v11, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v11, v9, v10

    const-class v11, Ljava/lang/Object;

    aput-object v11, v9, v7

    invoke-virtual {v2, v6, v9}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v6

    const/16 v9, 0xe

    .line 49
    filled-new-array {v7, v9, v10}, [I

    move-result-object v9

    const/4 v11, 0x0

    :goto_0
    const/4 v12, 0x3

    if-ge v11, v12, :cond_0

    .line 54
    aget v12, v9, v11

    .line 55
    new-instance v13, Landroid/media/AudioAttributes$Builder;

    invoke-direct {v13}, Landroid/media/AudioAttributes$Builder;-><init>()V

    invoke-virtual {v13, v12}, Landroid/media/AudioAttributes$Builder;->setUsage(I)Landroid/media/AudioAttributes$Builder;

    move-result-object v12

    invoke-virtual {v12}, Landroid/media/AudioAttributes$Builder;->build()Landroid/media/AudioAttributes;

    move-result-object v12

    .line 56
    invoke-static {v5}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v13

    new-array v14, v8, [Ljava/lang/Object;

    aput-object v13, v14, v10

    aput-object v12, v14, v7

    invoke-virtual {v6, v4, v14}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    add-int/lit8 v11, v11, 0x1

    goto :goto_0

    .line 60
    :cond_0
    invoke-virtual {v2, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v5

    invoke-virtual {v5, v4, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v5

    .line 63
    const-string v6, "voiceCommunicationCaptureAllowed"

    new-array v8, v7, [Ljava/lang/Class;

    sget-object v9, Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;

    aput-object v9, v8, v10

    invoke-virtual {v2, v6, v8}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    .line 64
    invoke-static {v7}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v6

    new-array v8, v7, [Ljava/lang/Object;

    aput-object v6, v8, v10

    invoke-virtual {v2, v4, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 66
    const-string v2, "android.media.audiopolicy.AudioMix"

    invoke-static {v2}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v2

    .line 67
    const-string v4, "android.media.audiopolicy.AudioMix$Builder"

    invoke-static {v4}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v4

    .line 70
    new-array v6, v7, [Ljava/lang/Class;

    aput-object v1, v6, v10

    invoke-virtual {v4, v6}, Ljava/lang/Class;->getConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v1

    new-array v6, v7, [Ljava/lang/Object;

    aput-object v5, v6, v10

    invoke-virtual {v1, v6}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    .line 73
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    const-string v6, "setFormat"

    new-array v8, v7, [Ljava/lang/Class;

    const-class v9, Landroid/media/AudioFormat;

    aput-object v9, v8, v10

    invoke-virtual {v5, v6, v8}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v5

    .line 74
    invoke-static {}, Lcom/android/helper/audio/AudioConfig;->createAudioFormat()Landroid/media/AudioFormat;

    move-result-object v6

    new-array v8, v7, [Ljava/lang/Object;

    aput-object v6, v8, v10

    invoke-virtual {v5, v1, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 76
    iget-boolean v5, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->keepPlayingOnDevice:Z

    if-eqz v5, :cond_1

    const-string v5, "ROUTE_FLAG_LOOP_BACK_RENDER"

    goto :goto_1

    :cond_1
    const-string v5, "ROUTE_FLAG_LOOP_BACK"

    .line 77
    :goto_1
    invoke-virtual {v2, v5}, Ljava/lang/Class;->getField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v5

    invoke-virtual {v5, v3}, Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I

    move-result v5

    .line 80
    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v6

    const-string v8, "setRouteFlags"

    new-array v9, v7, [Ljava/lang/Class;

    sget-object v11, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v11, v9, v10

    invoke-virtual {v6, v8, v9}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v6

    .line 81
    invoke-static {v5}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v5

    new-array v8, v7, [Ljava/lang/Object;

    aput-object v5, v8, v10

    invoke-virtual {v6, v1, v8}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 84
    invoke-virtual {v4, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    invoke-virtual {v4, v1, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    .line 86
    const-string v4, "android.media.audiopolicy.AudioPolicy"

    invoke-static {v4}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v4

    .line 87
    const-string v5, "android.media.audiopolicy.AudioPolicy$Builder"

    invoke-static {v5}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v5

    .line 90
    new-array v6, v7, [Ljava/lang/Class;

    const-class v8, Landroid/content/Context;

    aput-object v8, v6, v10

    invoke-virtual {v5, v6}, Ljava/lang/Class;->getConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v6

    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v8

    new-array v9, v7, [Ljava/lang/Object;

    aput-object v8, v9, v10

    invoke-virtual {v6, v9}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v6

    .line 93
    const-string v8, "addMix"

    new-array v9, v7, [Ljava/lang/Class;

    aput-object v2, v9, v10

    invoke-virtual {v5, v8, v9}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v8

    .line 94
    new-array v9, v7, [Ljava/lang/Object;

    aput-object v1, v9, v10

    invoke-virtual {v8, v6, v9}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 97
    invoke-virtual {v5, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-virtual {v0, v6, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    .line 100
    const-class v5, Landroid/media/AudioManager;

    const-string v6, "registerAudioPolicyStatic"

    new-array v8, v7, [Ljava/lang/Class;

    aput-object v4, v8, v10

    invoke-virtual {v5, v6, v8}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v5

    .line 101
    invoke-virtual {v5, v7}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 102
    new-array v6, v7, [Ljava/lang/Object;

    aput-object v0, v6, v10

    invoke-virtual {v5, v3, v6}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Ljava/lang/Integer;

    invoke-virtual {v3}, Ljava/lang/Integer;->intValue()I

    move-result v3

    if-nez v3, :cond_2

    .line 108
    const-string v3, "createAudioRecordSink"

    new-array v5, v7, [Ljava/lang/Class;

    aput-object v2, v5, v10

    invoke-virtual {v4, v3, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    .line 109
    new-array v3, v7, [Ljava/lang/Object;

    aput-object v1, v3, v10

    invoke-virtual {v2, v0, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/media/AudioRecord;

    return-object v0

    .line 104
    :cond_2
    new-instance v0, Ljava/lang/RuntimeException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "registerAudioPolicy() returned "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0
    move-exception v0

    .line 111
    const-string v1, "Could not capture audio playback"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 112
    new-instance v0, Lcom/android/helper/audio/AudioCaptureException;

    invoke-direct {v0}, Lcom/android/helper/audio/AudioCaptureException;-><init>()V

    throw v0
.end method


# virtual methods
.method public checkCompatibility()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 120
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x21

    if-lt v0, v1, :cond_0

    return-void

    .line 121
    :cond_0
    const-string v0, "Audio disabled: audio playback capture source not supported before Android 13"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 122
    new-instance v0, Lcom/android/helper/audio/AudioCaptureException;

    invoke-direct {v0}, Lcom/android/helper/audio/AudioCaptureException;-><init>()V

    throw v0
.end method

.method public read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I
    .locals 1

    .line 155
    iget-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->fallbackDirectCapture:Lcom/android/helper/audio/AudioCapture;

    if-eqz v0, :cond_0

    .line 156
    invoke-interface {v0, p1, p2}, Lcom/android/helper/audio/AudioCapture;->read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I

    move-result p1

    return p1

    .line 158
    :cond_0
    iget-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->reader:Lcom/android/helper/audio/AudioRecordReader;

    invoke-virtual {v0, p1, p2}, Lcom/android/helper/audio/AudioRecordReader;->read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I

    move-result p1

    return p1
.end method

.method public start()V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 129
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/audio/AudioPlaybackCapture;->createAudioRecord()Landroid/media/AudioRecord;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->recorder:Landroid/media/AudioRecord;

    .line 130
    invoke-virtual {v0}, Landroid/media/AudioRecord;->startRecording()V

    .line 131
    new-instance v0, Lcom/android/helper/audio/AudioRecordReader;

    iget-object v1, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->recorder:Landroid/media/AudioRecord;

    invoke-direct {v0, v1}, Lcom/android/helper/audio/AudioRecordReader;-><init>(Landroid/media/AudioRecord;)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->reader:Lcom/android/helper/audio/AudioRecordReader;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 133
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "AudioPlaybackCapture failed, falling back to AudioDirectCapture(OUTPUT): "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 134
    new-instance v0, Lcom/android/helper/audio/AudioDirectCapture;

    sget-object v1, Lcom/android/helper/audio/AudioSource;->OUTPUT:Lcom/android/helper/audio/AudioSource;

    invoke-direct {v0, v1}, Lcom/android/helper/audio/AudioDirectCapture;-><init>(Lcom/android/helper/audio/AudioSource;)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->fallbackDirectCapture:Lcom/android/helper/audio/AudioCapture;

    .line 135
    invoke-interface {v0}, Lcom/android/helper/audio/AudioCapture;->checkCompatibility()V

    .line 136
    iget-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->fallbackDirectCapture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v0}, Lcom/android/helper/audio/AudioCapture;->start()V

    return-void
.end method

.method public stop()V
    .locals 1

    .line 142
    iget-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->fallbackDirectCapture:Lcom/android/helper/audio/AudioCapture;

    if-eqz v0, :cond_0

    .line 143
    invoke-interface {v0}, Lcom/android/helper/audio/AudioCapture;->stop()V

    return-void

    .line 146
    :cond_0
    iget-object v0, p0, Lcom/android/helper/audio/AudioPlaybackCapture;->recorder:Landroid/media/AudioRecord;

    if-eqz v0, :cond_1

    .line 148
    invoke-virtual {v0}, Landroid/media/AudioRecord;->release()V

    :cond_1
    return-void
.end method
