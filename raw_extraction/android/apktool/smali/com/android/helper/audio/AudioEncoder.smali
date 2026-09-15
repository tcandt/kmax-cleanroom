.class public final Lcom/android/helper/audio/AudioEncoder;
.super Ljava/lang/Object;
.source "AudioEncoder.java"

# interfaces
.implements Lcom/android/helper/AsyncProcessor;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/audio/AudioEncoder$InputTask;,
        Lcom/android/helper/audio/AudioEncoder$OutputTask;,
        Lcom/android/helper/audio/AudioEncoder$EncoderCallback;
    }
.end annotation


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field private static final CHANNELS:I = 0x2

.field private static final SAMPLE_RATE:I = 0xbb80


# instance fields
.field private final bitRate:I

.field private final capture:Lcom/android/helper/audio/AudioCapture;

.field private final codecOptions:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;"
        }
    .end annotation
.end field

.field private final encoderName:Ljava/lang/String;

.field private ended:Z

.field private final inputTasks:Ljava/util/concurrent/BlockingQueue;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/concurrent/BlockingQueue<",
            "Lcom/android/helper/audio/AudioEncoder$InputTask;",
            ">;"
        }
    .end annotation
.end field

.field private inputThread:Ljava/lang/Thread;

.field private mediaCodecThread:Landroid/os/HandlerThread;

.field private final outputTasks:Ljava/util/concurrent/BlockingQueue;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/concurrent/BlockingQueue<",
            "Lcom/android/helper/audio/AudioEncoder$OutputTask;",
            ">;"
        }
    .end annotation
.end field

.field private outputThread:Ljava/lang/Thread;

.field private previousPts:J

.field private recreatePts:Z

.field private final streamer:Lcom/android/helper/device/Streamer;

.field private thread:Ljava/lang/Thread;


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/audio/AudioCapture;Lcom/android/helper/device/Streamer;Lcom/android/helper/Options;)V
    .locals 2

    .line 74
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 63
    new-instance v0, Ljava/util/concurrent/ArrayBlockingQueue;

    const/16 v1, 0x40

    invoke-direct {v0, v1}, Ljava/util/concurrent/ArrayBlockingQueue;-><init>(I)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->inputTasks:Ljava/util/concurrent/BlockingQueue;

    .line 64
    new-instance v0, Ljava/util/concurrent/ArrayBlockingQueue;

    invoke-direct {v0, v1}, Ljava/util/concurrent/ArrayBlockingQueue;-><init>(I)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->outputTasks:Ljava/util/concurrent/BlockingQueue;

    .line 75
    iput-object p1, p0, Lcom/android/helper/audio/AudioEncoder;->capture:Lcom/android/helper/audio/AudioCapture;

    .line 76
    iput-object p2, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    .line 77
    invoke-virtual {p3}, Lcom/android/helper/Options;->getAudioBitRate()I

    move-result p1

    iput p1, p0, Lcom/android/helper/audio/AudioEncoder;->bitRate:I

    .line 78
    invoke-virtual {p3}, Lcom/android/helper/Options;->getAudioCodecOptions()Ljava/util/List;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/audio/AudioEncoder;->codecOptions:Ljava/util/List;

    .line 79
    invoke-virtual {p3}, Lcom/android/helper/Options;->getAudioEncoder()Ljava/lang/String;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/audio/AudioEncoder;->encoderName:Ljava/lang/String;

    return-void
.end method

.method static synthetic access$400(Lcom/android/helper/audio/AudioEncoder;)Ljava/util/concurrent/BlockingQueue;
    .locals 0

    .line 29
    iget-object p0, p0, Lcom/android/helper/audio/AudioEncoder;->inputTasks:Ljava/util/concurrent/BlockingQueue;

    return-object p0
.end method

.method static synthetic access$500(Lcom/android/helper/audio/AudioEncoder;)V
    .locals 0

    .line 29
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    return-void
.end method

.method static synthetic access$600(Lcom/android/helper/audio/AudioEncoder;)Ljava/util/concurrent/BlockingQueue;
    .locals 0

    .line 29
    iget-object p0, p0, Lcom/android/helper/audio/AudioEncoder;->outputTasks:Ljava/util/concurrent/BlockingQueue;

    return-object p0
.end method

.method private static createFormat(Ljava/lang/String;ILjava/util/List;)Landroid/media/MediaFormat;
    .locals 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "I",
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;)",
            "Landroid/media/MediaFormat;"
        }
    .end annotation

    .line 83
    new-instance v0, Landroid/media/MediaFormat;

    invoke-direct {v0}, Landroid/media/MediaFormat;-><init>()V

    .line 84
    const-string v1, "mime"

    invoke-virtual {v0, v1, p0}, Landroid/media/MediaFormat;->setString(Ljava/lang/String;Ljava/lang/String;)V

    .line 85
    const-string p0, "bitrate"

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 86
    const-string p0, "channel-count"

    const/4 p1, 0x2

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 87
    const-string p0, "sample-rate"

    const p1, 0xbb80

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    if-eqz p2, :cond_0

    .line 90
    invoke-interface {p2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object p0

    :goto_0
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    move-result p1

    if-eqz p1, :cond_0

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Lcom/android/helper/util/CodecOption;

    .line 91
    invoke-virtual {p1}, Lcom/android/helper/util/CodecOption;->getKey()Ljava/lang/String;

    move-result-object p2

    .line 92
    invoke-virtual {p1}, Lcom/android/helper/util/CodecOption;->getValue()Ljava/lang/Object;

    move-result-object p1

    .line 93
    invoke-static {v0, p2, p1}, Lcom/android/helper/util/CodecUtils;->setCodecOption(Landroid/media/MediaFormat;Ljava/lang/String;Ljava/lang/Object;)V

    .line 94
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Audio codec option set: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p2, " ("

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object p2

    invoke-virtual {p2}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    move-result-object p2

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p2, ") = "

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_0
    return-object v0
.end method

.method private static createMediaCodec(Lcom/android/helper/util/Codec;Ljava/lang/String;)Landroid/media/MediaCodec;
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Lcom/android/helper/device/ConfigurationException;
        }
    .end annotation

    .line 320
    const-string v0, "\' for "

    .line 0
    const-string v1, "Incorrect encoder type: "

    const-string v2, "Audio encoder type for \""

    const-string v3, "Using audio encoder: \'"

    .line 320
    const-string v4, "\n"

    const-string v5, "\'"

    if-eqz p1, :cond_1

    .line 321
    new-instance v3, Ljava/lang/StringBuilder;

    const-string v6, "Creating audio encoder by name: \'"

    invoke-direct {v3, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v3}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 323
    :try_start_0
    invoke-static {p1}, Landroid/media/MediaCodec;->createByCodecName(Ljava/lang/String;)Landroid/media/MediaCodec;

    move-result-object v3

    .line 324
    invoke-static {v3}, Lcom/android/helper/util/Codec$-CC;->getMimeType(Landroid/media/MediaCodec;)Ljava/lang/String;

    move-result-object v5

    .line 325
    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v6, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6

    if-eqz v6, :cond_0

    return-object v3

    .line 326
    :cond_0
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, "\" ("

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, ") does not match codec type ("

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v2, ")"

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 327
    new-instance v2, Lcom/android/helper/device/ConfigurationException;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v2, v1}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw v2
    :try_end_0
    .catch Ljava/lang/IllegalArgumentException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0
    move-exception v1

    .line 334
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Could not create audio encoder \'"

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildAudioEncoderListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 335
    throw v1

    .line 331
    :catch_1
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Audio encoder \'"

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " not found\n"

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildAudioEncoderListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 332
    new-instance p0, Lcom/android/helper/device/ConfigurationException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Unknown encoder: "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 340
    :cond_1
    :try_start_1
    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Landroid/media/MediaCodec;->createEncoderByType(Ljava/lang/String;)Landroid/media/MediaCodec;

    move-result-object p1

    .line 341
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1}, Landroid/media/MediaCodec;->getName()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_3
    .catch Ljava/lang/IllegalArgumentException; {:try_start_1 .. :try_end_1} :catch_2

    return-object p1

    :catch_2
    move-exception p1

    goto :goto_0

    :catch_3
    move-exception p1

    .line 344
    :goto_0
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Could not create default audio encoder for "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildAudioEncoderListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 345
    throw p1
.end method

.method private encode()V
    .locals 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Lcom/android/helper/device/ConfigurationException;,
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 207
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1e

    const/4 v2, 0x0

    if-ge v0, v1, :cond_0

    .line 208
    const-string v0, "Audio disabled: it is not supported before Android 11"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 209
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v0, v2}, Lcom/android/helper/device/Streamer;->writeDisableStream(Z)V

    return-void

    :cond_0
    const/4 v0, 0x1

    const/4 v1, 0x0

    .line 217
    :try_start_0
    iget-object v3, p0, Lcom/android/helper/audio/AudioEncoder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v3}, Lcom/android/helper/audio/AudioCapture;->checkCompatibility()V

    .line 219
    iget-object v3, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v3}, Lcom/android/helper/device/Streamer;->getCodec()Lcom/android/helper/util/Codec;

    move-result-object v3

    .line 220
    iget-object v4, p0, Lcom/android/helper/audio/AudioEncoder;->encoderName:Ljava/lang/String;

    invoke-static {v3, v4}, Lcom/android/helper/audio/AudioEncoder;->createMediaCodec(Lcom/android/helper/util/Codec;Ljava/lang/String;)Landroid/media/MediaCodec;

    move-result-object v4
    :try_end_0
    .catch Lcom/android/helper/device/ConfigurationException; {:try_start_0 .. :try_end_0} :catch_3
    .catchall {:try_start_0 .. :try_end_0} :catchall_2

    .line 225
    :try_start_1
    invoke-static {v4}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/MediaCodec;)Ljava/lang/String;

    move-result-object v5

    .line 226
    const-string v6, "c2.android.opus.encoder"

    invoke-virtual {v6, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6

    if-nez v6, :cond_2

    const-string v6, "c2.android.flac.encoder"

    invoke-virtual {v6, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_1

    goto :goto_0

    :cond_1
    const/4 v5, 0x0

    goto :goto_1

    :cond_2
    :goto_0
    const/4 v5, 0x1

    :goto_1
    iput-boolean v5, p0, Lcom/android/helper/audio/AudioEncoder;->recreatePts:Z

    .line 228
    new-instance v5, Landroid/os/HandlerThread;

    const-string v6, "media-codec"

    invoke-direct {v5, v6}, Landroid/os/HandlerThread;-><init>(Ljava/lang/String;)V

    iput-object v5, p0, Lcom/android/helper/audio/AudioEncoder;->mediaCodecThread:Landroid/os/HandlerThread;

    .line 229
    invoke-virtual {v5}, Landroid/os/HandlerThread;->start()V

    .line 231
    invoke-interface {v3}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object v3

    iget v5, p0, Lcom/android/helper/audio/AudioEncoder;->bitRate:I

    iget-object v6, p0, Lcom/android/helper/audio/AudioEncoder;->codecOptions:Ljava/util/List;

    invoke-static {v3, v5, v6}, Lcom/android/helper/audio/AudioEncoder;->createFormat(Ljava/lang/String;ILjava/util/List;)Landroid/media/MediaFormat;

    move-result-object v3

    .line 232
    new-instance v5, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;

    invoke-direct {v5, p0, v1}, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;-><init>(Lcom/android/helper/audio/AudioEncoder;Lcom/android/helper/audio/AudioEncoder$1;)V

    new-instance v6, Landroid/os/Handler;

    iget-object v7, p0, Lcom/android/helper/audio/AudioEncoder;->mediaCodecThread:Landroid/os/HandlerThread;

    invoke-virtual {v7}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object v7

    invoke-direct {v6, v7}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    invoke-static {v4, v5, v6}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/MediaCodec;Landroid/media/MediaCodec$Callback;Landroid/os/Handler;)V

    .line 233
    invoke-virtual {v4, v3, v1, v1, v0}, Landroid/media/MediaCodec;->configure(Landroid/media/MediaFormat;Landroid/view/Surface;Landroid/media/MediaCrypto;I)V

    .line 235
    iget-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v1}, Lcom/android/helper/audio/AudioCapture;->start()V

    .line 238
    new-instance v1, Ljava/lang/Thread;

    new-instance v3, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;

    invoke-direct {v3, p0, v4}, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;-><init>(Lcom/android/helper/audio/AudioEncoder;Landroid/media/MediaCodec;)V

    const-string v5, "audio-in"

    invoke-direct {v1, v3, v5}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->inputThread:Ljava/lang/Thread;

    .line 248
    new-instance v1, Ljava/lang/Thread;

    new-instance v3, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda4;

    invoke-direct {v3, p0, v4}, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda4;-><init>(Lcom/android/helper/audio/AudioEncoder;Landroid/media/MediaCodec;)V

    const-string v5, "audio-out"

    invoke-direct {v1, v3, v5}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->outputThread:Ljava/lang/Thread;

    .line 263
    invoke-virtual {v4}, Landroid/media/MediaCodec;->start()V
    :try_end_1
    .catch Lcom/android/helper/device/ConfigurationException; {:try_start_1 .. :try_end_1} :catch_2
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    .line 265
    :try_start_2
    iget-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->inputThread:Ljava/lang/Thread;

    invoke-virtual {v1}, Ljava/lang/Thread;->start()V

    .line 266
    iget-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->outputThread:Ljava/lang/Thread;

    invoke-virtual {v1}, Ljava/lang/Thread;->start()V

    .line 268
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->waitEnded()V
    :try_end_2
    .catch Lcom/android/helper/device/ConfigurationException; {:try_start_2 .. :try_end_2} :catch_1
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    .line 279
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->mediaCodecThread:Landroid/os/HandlerThread;

    if-eqz v0, :cond_3

    .line 280
    invoke-virtual {v0}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object v0

    if-eqz v0, :cond_3

    .line 282
    invoke-virtual {v0}, Landroid/os/Looper;->quitSafely()V

    .line 285
    :cond_3
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->inputThread:Ljava/lang/Thread;

    if-eqz v0, :cond_4

    .line 286
    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    .line 288
    :cond_4
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->outputThread:Ljava/lang/Thread;

    if-eqz v0, :cond_5

    .line 289
    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    .line 293
    :cond_5
    :try_start_3
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->mediaCodecThread:Landroid/os/HandlerThread;

    if-eqz v0, :cond_6

    .line 294
    invoke-virtual {v0}, Landroid/os/HandlerThread;->join()V

    .line 296
    :cond_6
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->inputThread:Ljava/lang/Thread;

    if-eqz v0, :cond_7

    .line 297
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    .line 299
    :cond_7
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->outputThread:Ljava/lang/Thread;

    if-eqz v0, :cond_8

    .line 300
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V
    :try_end_3
    .catch Ljava/lang/InterruptedException; {:try_start_3 .. :try_end_3} :catch_0

    :cond_8
    if-eqz v4, :cond_9

    .line 309
    invoke-virtual {v4}, Landroid/media/MediaCodec;->stop()V

    .line 311
    invoke-virtual {v4}, Landroid/media/MediaCodec;->release()V

    .line 313
    :cond_9
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->capture:Lcom/android/helper/audio/AudioCapture;

    if-eqz v0, :cond_a

    .line 314
    invoke-interface {v0}, Lcom/android/helper/audio/AudioCapture;->stop()V

    :cond_a
    return-void

    :catch_0
    move-exception v0

    .line 304
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1

    :catchall_0
    move-exception v1

    move-object v0, v1

    const/4 v1, 0x1

    goto :goto_3

    :catch_1
    move-exception v1

    const/4 v2, 0x1

    goto :goto_4

    :catchall_1
    move-exception v0

    goto :goto_2

    :catch_2
    move-exception v1

    goto :goto_4

    :catchall_2
    move-exception v0

    move-object v4, v1

    :goto_2
    const/4 v1, 0x0

    .line 275
    :goto_3
    :try_start_4
    iget-object v3, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v3, v2}, Lcom/android/helper/device/Streamer;->writeDisableStream(Z)V

    .line 276
    throw v0
    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_3

    :catchall_3
    move-exception v0

    goto :goto_5

    :catch_3
    move-exception v3

    move-object v4, v1

    move-object v1, v3

    .line 271
    :goto_4
    :try_start_5
    iget-object v3, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v3, v0}, Lcom/android/helper/device/Streamer;->writeDisableStream(Z)V

    .line 272
    throw v1
    :try_end_5
    .catchall {:try_start_5 .. :try_end_5} :catchall_4

    :catchall_4
    move-exception v0

    move v1, v2

    .line 279
    :goto_5
    iget-object v2, p0, Lcom/android/helper/audio/AudioEncoder;->mediaCodecThread:Landroid/os/HandlerThread;

    if-eqz v2, :cond_b

    .line 280
    invoke-virtual {v2}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object v2

    if-eqz v2, :cond_b

    .line 282
    invoke-virtual {v2}, Landroid/os/Looper;->quitSafely()V

    .line 285
    :cond_b
    iget-object v2, p0, Lcom/android/helper/audio/AudioEncoder;->inputThread:Ljava/lang/Thread;

    if-eqz v2, :cond_c

    .line 286
    invoke-virtual {v2}, Ljava/lang/Thread;->interrupt()V

    .line 288
    :cond_c
    iget-object v2, p0, Lcom/android/helper/audio/AudioEncoder;->outputThread:Ljava/lang/Thread;

    if-eqz v2, :cond_d

    .line 289
    invoke-virtual {v2}, Ljava/lang/Thread;->interrupt()V

    .line 293
    :cond_d
    :try_start_6
    iget-object v2, p0, Lcom/android/helper/audio/AudioEncoder;->mediaCodecThread:Landroid/os/HandlerThread;

    if-eqz v2, :cond_e

    .line 294
    invoke-virtual {v2}, Landroid/os/HandlerThread;->join()V

    .line 296
    :cond_e
    iget-object v2, p0, Lcom/android/helper/audio/AudioEncoder;->inputThread:Ljava/lang/Thread;

    if-eqz v2, :cond_f

    .line 297
    invoke-virtual {v2}, Ljava/lang/Thread;->join()V

    .line 299
    :cond_f
    iget-object v2, p0, Lcom/android/helper/audio/AudioEncoder;->outputThread:Ljava/lang/Thread;

    if-eqz v2, :cond_10

    .line 300
    invoke-virtual {v2}, Ljava/lang/Thread;->join()V
    :try_end_6
    .catch Ljava/lang/InterruptedException; {:try_start_6 .. :try_end_6} :catch_4

    :cond_10
    if-eqz v4, :cond_12

    if-eqz v1, :cond_11

    .line 309
    invoke-virtual {v4}, Landroid/media/MediaCodec;->stop()V

    .line 311
    :cond_11
    invoke-virtual {v4}, Landroid/media/MediaCodec;->release()V

    .line 313
    :cond_12
    iget-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->capture:Lcom/android/helper/audio/AudioCapture;

    if-eqz v1, :cond_13

    .line 314
    invoke-interface {v1}, Lcom/android/helper/audio/AudioCapture;->stop()V

    .line 316
    :cond_13
    throw v0

    :catch_4
    move-exception v0

    .line 304
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1
.end method

.method private declared-synchronized end()V
    .locals 1

    monitor-enter p0

    const/4 v0, 0x1

    .line 191
    :try_start_0
    iput-boolean v0, p0, Lcom/android/helper/audio/AudioEncoder;->ended:Z

    .line 192
    invoke-virtual {p0}, Ljava/lang/Object;->notify()V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 193
    monitor-exit p0

    return-void

    :catchall_0
    move-exception v0

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v0
.end method

.method private fixTimestamp(Landroid/media/MediaCodec$BufferInfo;)V
    .locals 7

    .line 137
    iget v0, p1, Landroid/media/MediaCodec$BufferInfo;->flags:I

    and-int/lit8 v0, v0, 0x2

    if-eqz v0, :cond_0

    return-void

    .line 142
    :cond_0
    iget-wide v0, p1, Landroid/media/MediaCodec$BufferInfo;->presentationTimeUs:J

    .line 143
    iget-wide v2, p0, Lcom/android/helper/audio/AudioEncoder;->previousPts:J

    const-wide/16 v4, 0x0

    cmp-long v6, v2, v4

    if-eqz v6, :cond_1

    .line 144
    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v2

    const-wide/16 v4, 0x3e8

    div-long/2addr v2, v4

    .line 146
    iget-wide v4, p0, Lcom/android/helper/audio/AudioEncoder;->previousPts:J

    sub-long v4, v0, v4

    sub-long/2addr v2, v4

    .line 147
    iput-wide v2, p1, Landroid/media/MediaCodec$BufferInfo;->presentationTimeUs:J

    .line 150
    :cond_1
    iput-wide v0, p0, Lcom/android/helper/audio/AudioEncoder;->previousPts:J

    return-void
.end method

.method private inputThread(Landroid/media/MediaCodec;Lcom/android/helper/audio/AudioCapture;)V
    .locals 10
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 103
    new-instance v0, Landroid/media/MediaCodec$BufferInfo;

    invoke-direct {v0}, Landroid/media/MediaCodec$BufferInfo;-><init>()V

    .line 105
    :goto_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Thread;->isInterrupted()Z

    move-result v1

    if-nez v1, :cond_1

    .line 106
    iget-object v1, p0, Lcom/android/helper/audio/AudioEncoder;->inputTasks:Ljava/util/concurrent/BlockingQueue;

    invoke-interface {v1}, Ljava/util/concurrent/BlockingQueue;->take()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/android/helper/audio/AudioEncoder$InputTask;

    .line 107
    invoke-static {v1}, Lcom/android/helper/audio/AudioEncoder$InputTask;->access$000(Lcom/android/helper/audio/AudioEncoder$InputTask;)I

    move-result v2

    invoke-virtual {p1, v2}, Landroid/media/MediaCodec;->getInputBuffer(I)Ljava/nio/ByteBuffer;

    move-result-object v2

    .line 108
    invoke-interface {p2, v2, v0}, Lcom/android/helper/audio/AudioCapture;->read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I

    move-result v2

    if-lez v2, :cond_0

    .line 113
    invoke-static {v1}, Lcom/android/helper/audio/AudioEncoder$InputTask;->access$000(Lcom/android/helper/audio/AudioEncoder$InputTask;)I

    move-result v4

    iget v5, v0, Landroid/media/MediaCodec$BufferInfo;->offset:I

    iget v6, v0, Landroid/media/MediaCodec$BufferInfo;->size:I

    iget-wide v7, v0, Landroid/media/MediaCodec$BufferInfo;->presentationTimeUs:J

    iget v9, v0, Landroid/media/MediaCodec$BufferInfo;->flags:I

    move-object v3, p1

    invoke-virtual/range {v3 .. v9}, Landroid/media/MediaCodec;->queueInputBuffer(IIIJI)V

    goto :goto_0

    .line 110
    :cond_0
    new-instance p1, Ljava/io/IOException;

    new-instance p2, Ljava/lang/StringBuilder;

    const-string v0, "Could not read audio: "

    invoke-direct {p2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_1
    return-void
.end method

.method private outputThread(Landroid/media/MediaCodec;)V
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 118
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v0}, Lcom/android/helper/device/Streamer;->writeAudioHeader()V

    .line 120
    :goto_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->isInterrupted()Z

    move-result v0

    if-nez v0, :cond_1

    .line 121
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->outputTasks:Ljava/util/concurrent/BlockingQueue;

    invoke-interface {v0}, Ljava/util/concurrent/BlockingQueue;->take()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/android/helper/audio/AudioEncoder$OutputTask;

    .line 122
    invoke-static {v0}, Lcom/android/helper/audio/AudioEncoder$OutputTask;->access$100(Lcom/android/helper/audio/AudioEncoder$OutputTask;)I

    move-result v1

    invoke-virtual {p1, v1}, Landroid/media/MediaCodec;->getOutputBuffer(I)Ljava/nio/ByteBuffer;

    move-result-object v1

    const/4 v2, 0x0

    .line 124
    :try_start_0
    iget-boolean v3, p0, Lcom/android/helper/audio/AudioEncoder;->recreatePts:Z

    if-eqz v3, :cond_0

    .line 125
    invoke-static {v0}, Lcom/android/helper/audio/AudioEncoder$OutputTask;->access$200(Lcom/android/helper/audio/AudioEncoder$OutputTask;)Landroid/media/MediaCodec$BufferInfo;

    move-result-object v3

    invoke-direct {p0, v3}, Lcom/android/helper/audio/AudioEncoder;->fixTimestamp(Landroid/media/MediaCodec$BufferInfo;)V

    .line 127
    :cond_0
    iget-object v3, p0, Lcom/android/helper/audio/AudioEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-static {v0}, Lcom/android/helper/audio/AudioEncoder$OutputTask;->access$200(Lcom/android/helper/audio/AudioEncoder$OutputTask;)Landroid/media/MediaCodec$BufferInfo;

    move-result-object v4

    invoke-virtual {v3, v1, v4}, Lcom/android/helper/device/Streamer;->writePacket(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 129
    invoke-static {v0}, Lcom/android/helper/audio/AudioEncoder$OutputTask;->access$100(Lcom/android/helper/audio/AudioEncoder$OutputTask;)I

    move-result v0

    invoke-virtual {p1, v0, v2}, Landroid/media/MediaCodec;->releaseOutputBuffer(IZ)V

    goto :goto_0

    :catchall_0
    move-exception v1

    invoke-static {v0}, Lcom/android/helper/audio/AudioEncoder$OutputTask;->access$100(Lcom/android/helper/audio/AudioEncoder$OutputTask;)I

    move-result v0

    invoke-virtual {p1, v0, v2}, Landroid/media/MediaCodec;->releaseOutputBuffer(IZ)V

    .line 130
    throw v1

    :cond_1
    return-void
.end method

.method private declared-synchronized waitEnded()V
    .locals 1

    monitor-enter p0

    .line 197
    :goto_0
    :try_start_0
    iget-boolean v0, p0, Lcom/android/helper/audio/AudioEncoder;->ended:Z

    if-nez v0, :cond_0

    .line 198
    invoke-virtual {p0}, Ljava/lang/Object;->wait()V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    goto :goto_0

    :catchall_0
    move-exception v0

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v0

    .line 203
    :catch_0
    :cond_0
    monitor-exit p0

    return-void
.end method


# virtual methods
.method public join()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 185
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 186
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    :cond_0
    return-void
.end method

.method synthetic lambda$encode$1$com-android-helper-audio-AudioEncoder(Landroid/media/MediaCodec;)V
    .locals 1

    .line 240
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-direct {p0, p1, v0}, Lcom/android/helper/audio/AudioEncoder;->inputThread(Landroid/media/MediaCodec;Lcom/android/helper/audio/AudioCapture;)V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 244
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    return-void

    :catchall_0
    move-exception p1

    goto :goto_1

    :catch_0
    move-exception p1

    goto :goto_0

    :catch_1
    move-exception p1

    .line 242
    :goto_0
    :try_start_1
    const-string v0, "Audio capture error"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    .line 244
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    return-void

    :goto_1
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    .line 245
    throw p1
.end method

.method synthetic lambda$encode$2$com-android-helper-audio-AudioEncoder(Landroid/media/MediaCodec;)V
    .locals 1

    .line 250
    :try_start_0
    invoke-direct {p0, p1}, Lcom/android/helper/audio/AudioEncoder;->outputThread(Landroid/media/MediaCodec;)V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 259
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    return-void

    :catchall_0
    move-exception p1

    goto :goto_0

    :catch_0
    move-exception p1

    .line 255
    :try_start_1
    invoke-static {p1}, Lcom/android/helper/util/IO;->isBrokenPipe(Ljava/io/IOException;)Z

    move-result v0

    if-nez v0, :cond_0

    .line 256
    const-string v0, "Audio encoding error"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_1

    .line 259
    :goto_0
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    .line 260
    throw p1

    .line 259
    :catch_1
    :cond_0
    :goto_1
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    return-void
.end method

.method synthetic lambda$start$0$com-android-helper-audio-AudioEncoder(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 5

    .line 156
    const-string v0, "Audio encoder stopped"

    const/4 v1, 0x1

    const/4 v2, 0x0

    .line 158
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->encode()V
    :try_end_0
    .catch Lcom/android/helper/device/ConfigurationException; {:try_start_0 .. :try_end_0} :catch_2
    .catch Lcom/android/helper/audio/AudioCaptureException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 168
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 169
    invoke-interface {p1, v2}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    return-void

    :catchall_0
    move-exception v1

    goto :goto_0

    :catch_0
    move-exception v3

    .line 165
    :try_start_1
    const-string v4, "Audio encoding error"

    invoke-static {v4, v3}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_1

    .line 168
    :goto_0
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 169
    invoke-interface {p1, v2}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    .line 170
    throw v1

    .line 168
    :catch_1
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 169
    invoke-interface {p1, v2}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    goto :goto_2

    .line 168
    :catch_2
    :goto_1
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 169
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    :goto_2
    return-void
.end method

.method public start(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 2

    .line 155
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda2;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda2;-><init>(Lcom/android/helper/audio/AudioEncoder;Lcom/android/helper/AsyncProcessor$TerminationListener;)V

    const-string p1, "audio-encoder"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->thread:Ljava/lang/Thread;

    .line 172
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method public stop()V
    .locals 1

    .line 177
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 179
    invoke-direct {p0}, Lcom/android/helper/audio/AudioEncoder;->end()V

    :cond_0
    return-void
.end method
