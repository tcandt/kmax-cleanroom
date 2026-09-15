.class public Lcom/android/helper/audio/AudioDirectCapture;
.super Ljava/lang/Object;
.source "AudioDirectCapture.java"

# interfaces
.implements Lcom/android/helper/audio/AudioCapture;


# static fields
.field private static final CHANNELS:I = 0x2

.field private static final CHANNEL_CONFIG:I = 0xc

.field private static final CHANNEL_MASK:I = 0xc

.field private static final ENCODING:I = 0x2

.field private static final SAMPLE_RATE:I = 0xbb80


# instance fields
.field private final audioSource:I

.field private reader:Lcom/android/helper/audio/AudioRecordReader;

.field private recorder:Landroid/media/AudioRecord;


# direct methods
.method public constructor <init>(Lcom/android/helper/audio/AudioSource;)V
    .locals 0

    .line 33
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 34
    invoke-virtual {p1}, Lcom/android/helper/audio/AudioSource;->getDirectAudioSource()I

    move-result p1

    iput p1, p0, Lcom/android/helper/audio/AudioDirectCapture;->audioSource:I

    return-void
.end method

.method private static createAudioRecord(I)Landroid/media/AudioRecord;
    .locals 3

    .line 40
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Landroid/media/AudioRecord$Builder;

    move-result-object v0

    .line 41
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1f

    if-lt v1, v2, :cond_0

    .line 43
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/AudioRecord$Builder;Landroid/content/Context;)Landroid/media/AudioRecord$Builder;

    .line 45
    :cond_0
    invoke-static {v0, p0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/AudioRecord$Builder;I)Landroid/media/AudioRecord$Builder;

    .line 46
    invoke-static {}, Lcom/android/helper/audio/AudioConfig;->createAudioFormat()Landroid/media/AudioFormat;

    move-result-object p0

    invoke-static {v0, p0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/AudioRecord$Builder;Landroid/media/AudioFormat;)Landroid/media/AudioRecord$Builder;

    const/16 p0, 0xc

    const/4 v1, 0x2

    const v2, 0xbb80

    .line 47
    invoke-static {v2, p0, v1}, Landroid/media/AudioRecord;->getMinBufferSize(III)I

    move-result p0

    if-lez p0, :cond_1

    mul-int/lit8 p0, p0, 0x8

    .line 50
    invoke-static {v0, p0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m$1(Landroid/media/AudioRecord$Builder;I)Landroid/media/AudioRecord$Builder;

    .line 53
    :cond_1
    invoke-static {v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/AudioRecord$Builder;)Landroid/media/AudioRecord;

    move-result-object p0

    return-object p0
.end method

.method private startRecording()V
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 96
    :try_start_0
    iget v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->audioSource:I

    invoke-static {v0}, Lcom/android/helper/audio/AudioDirectCapture;->createAudioRecord(I)Landroid/media/AudioRecord;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->recorder:Landroid/media/AudioRecord;
    :try_end_0
    .catch Ljava/lang/NullPointerException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 101
    :catch_0
    iget v1, p0, Lcom/android/helper/audio/AudioDirectCapture;->audioSource:I

    const/16 v5, 0xc

    const/4 v6, 0x2

    const v2, 0xbb80

    const/16 v3, 0xc

    const/4 v4, 0x2

    invoke-static/range {v1 .. v6}, Lcom/android/helper/Workarounds;->createAudioRecord(IIIIII)Landroid/media/AudioRecord;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->recorder:Landroid/media/AudioRecord;

    .line 103
    :goto_0
    iget-object v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->recorder:Landroid/media/AudioRecord;

    invoke-virtual {v0}, Landroid/media/AudioRecord;->startRecording()V

    .line 104
    new-instance v0, Lcom/android/helper/audio/AudioRecordReader;

    iget-object v1, p0, Lcom/android/helper/audio/AudioDirectCapture;->recorder:Landroid/media/AudioRecord;

    invoke-direct {v0, v1}, Lcom/android/helper/audio/AudioRecordReader;-><init>(Landroid/media/AudioRecord;)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->reader:Lcom/android/helper/audio/AudioRecordReader;

    return-void
.end method

.method private static startWorkaroundAndroid11()V
    .locals 4

    .line 63
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.intent.action.MAIN"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    const/high16 v1, 0x10000000

    .line 64
    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 65
    const-string v1, "android.intent.category.LAUNCHER"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;

    .line 66
    new-instance v1, Landroid/content/ComponentName;

    const-string v2, "com.android.shell"

    const-string v3, "com.android.shell.HeapDumpActivity"

    invoke-direct {v1, v2, v3}, Landroid/content/ComponentName;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/content/Intent;->setComponent(Landroid/content/ComponentName;)Landroid/content/Intent;

    .line 67
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v1

    invoke-virtual {v1, v0}, Lcom/android/helper/wrappers/ActivityManager;->startActivity(Landroid/content/Intent;)I

    return-void
.end method

.method private static stopWorkaroundAndroid11()V
    .locals 2

    .line 71
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v0

    const-string v1, "com.android.shell"

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/ActivityManager;->forceStopPackage(Ljava/lang/String;)V

    return-void
.end method

.method private tryStartRecording(II)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    :goto_0
    add-int/lit8 v0, p1, -0x1

    if-lez p1, :cond_1

    int-to-long v1, p2

    .line 77
    invoke-static {v1, v2}, Landroid/os/SystemClock;->sleep(J)V

    .line 79
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/audio/AudioDirectCapture;->startRecording()V
    :try_end_0
    .catch Ljava/lang/UnsupportedOperationException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_1

    :catch_0
    if-eqz v0, :cond_0

    .line 88
    const-string p1, "Failed to start audio capture, retrying..."

    invoke-static {p1}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    move p1, v0

    goto :goto_0

    .line 83
    :cond_0
    const-string p1, "Failed to start audio capture"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 84
    const-string p1, "On Android 11, audio capture must be started in the foreground, make sure that the device is unlocked when starting scrcpy."

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 86
    new-instance p1, Lcom/android/helper/audio/AudioCaptureException;

    invoke-direct {p1}, Lcom/android/helper/audio/AudioCaptureException;-><init>()V

    throw p1

    :cond_1
    :goto_1
    return-void
.end method


# virtual methods
.method public checkCompatibility()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 109
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1e

    if-lt v0, v1, :cond_0

    return-void

    .line 110
    :cond_0
    const-string v0, "Audio disabled: it is not supported before Android 11"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 111
    new-instance v0, Lcom/android/helper/audio/AudioCaptureException;

    invoke-direct {v0}, Lcom/android/helper/audio/AudioCaptureException;-><init>()V

    throw v0
.end method

.method public read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I
    .locals 1

    .line 140
    iget-object v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->reader:Lcom/android/helper/audio/AudioRecordReader;

    invoke-virtual {v0, p1, p2}, Lcom/android/helper/audio/AudioRecordReader;->read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I

    move-result p1

    return p1
.end method

.method public start()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 117
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1e

    if-ne v0, v1, :cond_0

    .line 118
    invoke-static {}, Lcom/android/helper/audio/AudioDirectCapture;->startWorkaroundAndroid11()V

    const/4 v0, 0x5

    const/16 v1, 0x64

    .line 120
    :try_start_0
    invoke-direct {p0, v0, v1}, Lcom/android/helper/audio/AudioDirectCapture;->tryStartRecording(II)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 122
    invoke-static {}, Lcom/android/helper/audio/AudioDirectCapture;->stopWorkaroundAndroid11()V

    return-void

    :catchall_0
    move-exception v0

    invoke-static {}, Lcom/android/helper/audio/AudioDirectCapture;->stopWorkaroundAndroid11()V

    .line 123
    throw v0

    .line 125
    :cond_0
    invoke-direct {p0}, Lcom/android/helper/audio/AudioDirectCapture;->startRecording()V

    return-void
.end method

.method public stop()V
    .locals 1

    .line 131
    iget-object v0, p0, Lcom/android/helper/audio/AudioDirectCapture;->recorder:Landroid/media/AudioRecord;

    if-eqz v0, :cond_0

    .line 133
    invoke-virtual {v0}, Landroid/media/AudioRecord;->release()V

    :cond_0
    return-void
.end method
