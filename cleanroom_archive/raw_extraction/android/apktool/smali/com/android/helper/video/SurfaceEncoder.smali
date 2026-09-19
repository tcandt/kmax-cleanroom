.class public Lcom/android/helper/video/SurfaceEncoder;
.super Ljava/lang/Object;
.source "SurfaceEncoder.java"

# interfaces
.implements Lcom/android/helper/AsyncProcessor;


# static fields
.field private static final DEFAULT_I_FRAME_INTERVAL:I = 0xa

.field private static final KEY_MAX_FPS_TO_ENCODER:Ljava/lang/String; = "max-fps-to-encoder"

.field private static final MAX_CONSECUTIVE_ERRORS:I = 0x3

.field private static final MAX_SIZE_FALLBACK:[I

.field private static final REPEAT_FRAME_DELAY_US:I = 0x186a0

.field private static activeCodec:Landroid/media/MediaCodec;

.field private static final codecLock:Ljava/lang/Object;

.field private static pendingKeyFrame:Z


# instance fields
.field private final capture:Lcom/android/helper/video/SurfaceCapture;

.field private final codecOptions:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;"
        }
    .end annotation
.end field

.field private consecutiveErrors:I

.field private final downsizeOnError:Z

.field private final encoderName:Ljava/lang/String;

.field private firstFrameSent:Z

.field private final maxFps:F

.field private final reset:Lcom/android/helper/video/CaptureReset;

.field private final stopped:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private final streamer:Lcom/android/helper/device/Streamer;

.field private thread:Ljava/lang/Thread;

.field private final videoBitRate:I


# direct methods
.method static constructor <clinit>()V
    .locals 1

    const/4 v0, 0x6

    .line 36
    new-array v0, v0, [I

    fill-array-data v0, :array_0

    sput-object v0, Lcom/android/helper/video/SurfaceEncoder;->MAX_SIZE_FALLBACK:[I

    .line 57
    new-instance v0, Ljava/lang/Object;

    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    sput-object v0, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    return-void

    :array_0
    .array-data 4
        0xa00
        0x780
        0x640
        0x500
        0x400
        0x320
    .end array-data
.end method

.method public constructor <init>(Lcom/android/helper/video/SurfaceCapture;Lcom/android/helper/device/Streamer;Lcom/android/helper/Options;)V
    .locals 1

    .line 96
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 51
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-direct {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>()V

    iput-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->stopped:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 53
    new-instance v0, Lcom/android/helper/video/CaptureReset;

    invoke-direct {v0}, Lcom/android/helper/video/CaptureReset;-><init>()V

    iput-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    .line 97
    iput-object p1, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    .line 98
    iput-object p2, p0, Lcom/android/helper/video/SurfaceEncoder;->streamer:Lcom/android/helper/device/Streamer;

    .line 99
    invoke-virtual {p3}, Lcom/android/helper/Options;->getVideoBitRate()I

    move-result p1

    iput p1, p0, Lcom/android/helper/video/SurfaceEncoder;->videoBitRate:I

    .line 100
    invoke-virtual {p3}, Lcom/android/helper/Options;->getMaxFps()F

    move-result p1

    iput p1, p0, Lcom/android/helper/video/SurfaceEncoder;->maxFps:F

    .line 101
    invoke-virtual {p3}, Lcom/android/helper/Options;->getVideoCodecOptions()Ljava/util/List;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/SurfaceEncoder;->codecOptions:Ljava/util/List;

    .line 102
    invoke-virtual {p3}, Lcom/android/helper/Options;->getVideoEncoder()Ljava/lang/String;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/SurfaceEncoder;->encoderName:Ljava/lang/String;

    .line 103
    invoke-virtual {p3}, Lcom/android/helper/Options;->getDownsizeOnError()Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/video/SurfaceEncoder;->downsizeOnError:Z

    return-void
.end method

.method private static chooseMaxSizeFallback(Lcom/android/helper/device/Size;)I
    .locals 5

    .line 258
    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p0

    invoke-static {v0, p0}, Ljava/lang/Math;->max(II)I

    move-result p0

    .line 259
    sget-object v0, Lcom/android/helper/video/SurfaceEncoder;->MAX_SIZE_FALLBACK:[I

    array-length v1, v0

    const/4 v2, 0x0

    const/4 v3, 0x0

    :goto_0
    if-ge v3, v1, :cond_1

    aget v4, v0, v3

    if-ge v4, p0, :cond_0

    return v4

    :cond_0
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    :cond_1
    return v2
.end method

.method private static createFormat(Ljava/lang/String;IFLjava/util/List;)Landroid/media/MediaFormat;
    .locals 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "IF",
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;)",
            "Landroid/media/MediaFormat;"
        }
    .end annotation

    .line 362
    new-instance v0, Landroid/media/MediaFormat;

    invoke-direct {v0}, Landroid/media/MediaFormat;-><init>()V

    .line 363
    const-string v1, "mime"

    invoke-virtual {v0, v1, p0}, Landroid/media/MediaFormat;->setString(Ljava/lang/String;Ljava/lang/String;)V

    .line 364
    const-string p0, "bitrate"

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 366
    const-string p0, "frame-rate"

    const/16 p1, 0x3c

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 367
    const-string p0, "color-format"

    const p1, 0x7f000789

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 368
    sget p0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 p1, 0x18

    if-lt p0, p1, :cond_0

    .line 369
    const-string p0, "color-range"

    const/4 p1, 0x2

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 371
    :cond_0
    const-string p0, "i-frame-interval"

    const/16 p1, 0xa

    invoke-virtual {v0, p0, p1}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 373
    const-string p0, "repeat-previous-frame-after"

    const-wide/32 v1, 0x186a0

    invoke-virtual {v0, p0, v1, v2}, Landroid/media/MediaFormat;->setLong(Ljava/lang/String;J)V

    const/4 p0, 0x0

    cmpl-float p0, p2, p0

    if-lez p0, :cond_1

    .line 378
    const-string p0, "max-fps-to-encoder"

    invoke-virtual {v0, p0, p2}, Landroid/media/MediaFormat;->setFloat(Ljava/lang/String;F)V

    :cond_1
    if-eqz p3, :cond_2

    .line 382
    invoke-interface {p3}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object p0

    :goto_0
    invoke-interface {p0}, Ljava/util/Iterator;->hasNext()Z

    move-result p1

    if-eqz p1, :cond_2

    invoke-interface {p0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Lcom/android/helper/util/CodecOption;

    .line 383
    invoke-virtual {p1}, Lcom/android/helper/util/CodecOption;->getKey()Ljava/lang/String;

    move-result-object p2

    .line 384
    invoke-virtual {p1}, Lcom/android/helper/util/CodecOption;->getValue()Ljava/lang/Object;

    move-result-object p1

    .line 385
    invoke-static {v0, p2, p1}, Lcom/android/helper/util/CodecUtils;->setCodecOption(Landroid/media/MediaFormat;Ljava/lang/String;Ljava/lang/Object;)V

    .line 386
    new-instance p3, Ljava/lang/StringBuilder;

    const-string v1, "Video codec option set: "

    invoke-direct {p3, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p3, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p2, " ("

    invoke-virtual {p3, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object p2

    invoke-virtual {p2}, Ljava/lang/Class;->getSimpleName()Ljava/lang/String;

    move-result-object p2

    invoke-virtual {p3, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p2, ") = "

    invoke-virtual {p3, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {p3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_2
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

    .line 332
    const-string v0, "\' for "

    .line 0
    const-string v1, "Incorrect encoder type: "

    const-string v2, "Video encoder type for \""

    const-string v3, "Using video encoder: \'"

    .line 332
    const-string v4, "\n"

    const-string v5, "\'"

    if-eqz p1, :cond_1

    .line 333
    new-instance v3, Ljava/lang/StringBuilder;

    const-string v6, "Creating encoder by name: \'"

    invoke-direct {v3, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v3}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 335
    :try_start_0
    invoke-static {p1}, Landroid/media/MediaCodec;->createByCodecName(Ljava/lang/String;)Landroid/media/MediaCodec;

    move-result-object v3

    .line 336
    invoke-static {v3}, Lcom/android/helper/util/Codec$-CC;->getMimeType(Landroid/media/MediaCodec;)Ljava/lang/String;

    move-result-object v5

    .line 337
    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v6, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v6

    if-eqz v6, :cond_0

    return-object v3

    .line 338
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

    .line 339
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

    .line 346
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Could not create video encoder \'"

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildVideoEncoderListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 347
    throw v1

    .line 343
    :catch_1
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Video encoder \'"

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " not found\n"

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildVideoEncoderListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 344
    new-instance p0, Lcom/android/helper/device/ConfigurationException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Unknown encoder: "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 352
    :cond_1
    :try_start_1
    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Landroid/media/MediaCodec;->createEncoderByType(Ljava/lang/String;)Landroid/media/MediaCodec;

    move-result-object p1

    .line 353
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

    .line 356
    :goto_0
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Could not create default video encoder for "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-interface {p0}, Lcom/android/helper/util/Codec;->getName()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildVideoEncoderListMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 357
    throw p1
.end method

.method private encode(Landroid/media/MediaCodec;Lcom/android/helper/device/Streamer;)V
    .locals 29
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    move-object/from16 v1, p0

    move-object/from16 v2, p1

    .line 270
    new-instance v0, Landroid/media/MediaCodec$BufferInfo;

    invoke-direct {v0}, Landroid/media/MediaCodec$BufferInfo;-><init>()V

    .line 272
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v3

    const-wide/16 v7, 0x0

    const-wide/16 v9, 0x0

    .line 277
    :goto_0
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v11

    const-wide/16 v13, -0x1

    .line 278
    invoke-virtual {v2, v0, v13, v14}, Landroid/media/MediaCodec;->dequeueOutputBuffer(Landroid/media/MediaCodec$BufferInfo;J)I

    move-result v13

    .line 279
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v14

    const-wide/16 v16, 0x0

    .line 281
    :try_start_0
    iget v6, v0, Landroid/media/MediaCodec$BufferInfo;->flags:I

    and-int/lit8 v6, v6, 0x4

    if-eqz v6, :cond_0

    const/4 v6, 0x1

    goto :goto_1

    :cond_0
    const/4 v6, 0x0

    :goto_1
    if-ltz v13, :cond_9

    const/16 v19, 0x1

    .line 282
    iget v5, v0, Landroid/media/MediaCodec$BufferInfo;->size:I

    if-lez v5, :cond_9

    .line 283
    invoke-virtual {v2, v13}, Landroid/media/MediaCodec;->getOutputBuffer(I)Ljava/nio/ByteBuffer;

    move-result-object v5

    move-wide/from16 v20, v3

    .line 285
    iget v3, v0, Landroid/media/MediaCodec$BufferInfo;->flags:I

    and-int/lit8 v3, v3, 0x2

    if-eqz v3, :cond_1

    const/4 v3, 0x1

    goto :goto_2

    :cond_1
    const/4 v3, 0x0

    .line 286
    :goto_2
    iget v4, v0, Landroid/media/MediaCodec$BufferInfo;->flags:I

    and-int/lit8 v4, v4, 0x1

    if-eqz v4, :cond_2

    const/4 v4, 0x1

    goto :goto_3

    :cond_2
    const/4 v4, 0x0

    :goto_3
    if-nez v3, :cond_3

    move/from16 v22, v3

    const/4 v3, 0x1

    .line 289
    iput-boolean v3, v1, Lcom/android/helper/video/SurfaceEncoder;->firstFrameSent:Z

    const/4 v3, 0x0

    .line 290
    iput v3, v1, Lcom/android/helper/video/SurfaceEncoder;->consecutiveErrors:I

    const-wide/16 v23, 0x1

    add-long v7, v7, v23

    goto :goto_4

    :cond_3
    move/from16 v22, v3

    .line 294
    :goto_4
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v23

    move-object/from16 v3, p2

    .line 295
    invoke-virtual {v3, v5, v0}, Lcom/android/helper/device/Streamer;->writePacket(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)V

    .line 296
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v25

    cmp-long v5, v9, v16

    if-nez v5, :cond_4

    move-wide/from16 v9, v16

    goto :goto_5

    :cond_4
    sub-long v9, v14, v9

    :goto_5
    sub-long v11, v14, v11

    move-wide/from16 v27, v14

    sub-long v14, v25, v23

    if-nez v22, :cond_6

    .line 301
    sget-object v5, Lcom/android/helper/util/Ln$Level;->DEBUG:Lcom/android/helper/util/Ln$Level;

    invoke-static {v5}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v5

    if-eqz v5, :cond_6

    if-nez v4, :cond_5

    const-wide/16 v22, 0xc8

    cmp-long v5, v9, v22

    if-gez v5, :cond_5

    cmp-long v5, v11, v22

    if-gez v5, :cond_5

    const-wide/16 v22, 0x14

    cmp-long v5, v14, v22

    if-ltz v5, :cond_6

    .line 302
    :cond_5
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "VideoTrace encoder-out frame="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v7, v8}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v1, " pts="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-wide/from16 v22, v7

    iget-wide v7, v0, Landroid/media/MediaCodec$BufferInfo;->presentationTimeUs:J

    invoke-virtual {v5, v7, v8}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v1, " size="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget v1, v0, Landroid/media/MediaCodec$BufferInfo;->size:I

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, " key="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(Z)Ljava/lang/StringBuilder;

    const-string v1, " dequeue_ms="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v11, v12}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v1, " write_ms="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v14, v15}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v1, " inter_ms="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v9, v10}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v1, " eos="

    invoke-virtual {v5, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Z)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    goto :goto_6

    :cond_6
    move-wide/from16 v22, v7

    :goto_6
    const-wide/16 v4, 0x78

    .line 313
    rem-long v7, v22, v4

    cmp-long v1, v7, v16

    if-nez v1, :cond_8

    .line 314
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v4

    sub-long v7, v4, v20

    cmp-long v1, v7, v16

    if-lez v1, :cond_7

    const v1, 0x47ea6000    # 120000.0f

    long-to-float v7, v7

    div-float/2addr v1, v7

    .line 318
    new-instance v7, Ljava/lang/StringBuilder;

    invoke-direct {v7}, Ljava/lang/StringBuilder;-><init>()V

    const-string v8, "Encoder Stats: FPS="

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v8, "%.1f"

    invoke-static {v1}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v1

    const/4 v9, 0x1

    new-array v9, v9, [Ljava/lang/Object;

    const/16 v18, 0x0

    aput-object v1, v9, v18

    invoke-static {v8, v9}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v7, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :cond_7
    move-wide/from16 v20, v4

    :cond_8
    move-wide/from16 v7, v22

    move-wide/from16 v9, v27

    goto :goto_7

    :cond_9
    move-wide/from16 v20, v3

    move-object/from16 v3, p2

    :goto_7
    if-ltz v13, :cond_a

    const/4 v1, 0x0

    .line 325
    invoke-virtual {v2, v13, v1}, Landroid/media/MediaCodec;->releaseOutputBuffer(IZ)V

    :cond_a
    if-eqz v6, :cond_b

    return-void

    :cond_b
    move-object/from16 v1, p0

    move-wide/from16 v3, v20

    goto/16 :goto_0

    :catchall_0
    move-exception v0

    const/4 v1, 0x0

    if-ltz v13, :cond_c

    invoke-virtual {v2, v13, v1}, Landroid/media/MediaCodec;->releaseOutputBuffer(IZ)V

    .line 327
    :cond_c
    throw v0
.end method

.method private prepareRetry(Lcom/android/helper/device/Size;)Z
    .locals 4

    .line 222
    iget-boolean v0, p0, Lcom/android/helper/video/SurfaceEncoder;->firstFrameSent:Z

    const/4 v1, 0x1

    const/4 v2, 0x0

    if-eqz v0, :cond_1

    .line 223
    iget p1, p0, Lcom/android/helper/video/SurfaceEncoder;->consecutiveErrors:I

    add-int/2addr p1, v1

    iput p1, p0, Lcom/android/helper/video/SurfaceEncoder;->consecutiveErrors:I

    const/4 v0, 0x3

    if-lt p1, v0, :cond_0

    return v2

    :cond_0
    const-wide/16 v2, 0x32

    .line 230
    invoke-static {v2, v3}, Landroid/os/SystemClock;->sleep(J)V

    return v1

    .line 234
    :cond_1
    iget-boolean v0, p0, Lcom/android/helper/video/SurfaceEncoder;->downsizeOnError:Z

    if-nez v0, :cond_2

    return v2

    .line 241
    :cond_2
    invoke-static {p1}, Lcom/android/helper/video/SurfaceEncoder;->chooseMaxSizeFallback(Lcom/android/helper/device/Size;)I

    move-result p1

    if-nez p1, :cond_3

    return v2

    .line 247
    :cond_3
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v0, p1}, Lcom/android/helper/video/SurfaceCapture;->setMaxSize(I)Z

    move-result v0

    if-nez v0, :cond_4

    return v2

    .line 253
    :cond_4
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v2, "Retrying with -m"

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p1, "..."

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    return v1
.end method

.method public static requestKeyFrame()V
    .locals 8

    .line 60
    const-string v0, "KeyframeTrace request-sync-frame write_ms="

    const-string v1, "KeyframeTrace request-sync-frame failed: "

    sget-object v2, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    monitor-enter v2

    .line 61
    :try_start_0
    sget-object v3, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v3, :cond_0

    .line 63
    :try_start_1
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v3

    .line 64
    new-instance v5, Landroid/os/Bundle;

    invoke-direct {v5}, Landroid/os/Bundle;-><init>()V

    .line 65
    const-string v6, "request-sync"

    const/4 v7, 0x0

    invoke-virtual {v5, v6, v7}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 66
    sget-object v6, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    invoke-virtual {v6, v5}, Landroid/media/MediaCodec;->setParameters(Landroid/os/Bundle;)V

    .line 67
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v6

    sub-long/2addr v6, v3

    invoke-virtual {v5, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_1
    .catch Ljava/lang/IllegalStateException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_0

    :catch_0
    move-exception v0

    .line 69
    :try_start_2
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/IllegalStateException;->getMessage()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    goto :goto_0

    :cond_0
    const/4 v0, 0x1

    .line 72
    sput-boolean v0, Lcom/android/helper/video/SurfaceEncoder;->pendingKeyFrame:Z

    .line 73
    const-string v0, "KeyframeTrace request-sync-frame deferred: no active codec yet, marked pending"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 75
    :goto_0
    monitor-exit v2

    return-void

    :catchall_0
    move-exception v0

    monitor-exit v2
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    throw v0
.end method

.method public static setVideoBitrate(I)V
    .locals 8

    const-string v0, "BweTrace set-bitrate bitrate="

    const-string v1, "BweTrace set-bitrate failed: "

    const-string v2, "BweTrace set-bitrate skipped: no active codec bitrate="

    .line 79
    sget-object v3, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    monitor-enter v3

    .line 80
    :try_start_0
    sget-object v4, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v4, :cond_0

    .line 82
    :try_start_1
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v4

    .line 83
    new-instance v2, Landroid/os/Bundle;

    invoke-direct {v2}, Landroid/os/Bundle;-><init>()V

    .line 84
    const-string v6, "video-bitrate"

    invoke-virtual {v2, v6, p0}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 85
    sget-object v6, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    invoke-virtual {v6, v2}, Landroid/media/MediaCodec;->setParameters(Landroid/os/Bundle;)V

    .line 86
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p0, " write_ms="

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide v6

    sub-long/2addr v6, v4

    invoke-virtual {v2, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_1
    .catch Ljava/lang/IllegalStateException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_0

    :catch_0
    move-exception p0

    .line 88
    :try_start_2
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0}, Ljava/lang/IllegalStateException;->getMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    goto :goto_0

    .line 91
    :cond_0
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 93
    :goto_0
    monitor-exit v3

    return-void

    :catchall_0
    move-exception p0

    monitor-exit v3
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    throw p0
.end method

.method private streamCapture()V
    .locals 14
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Lcom/android/helper/device/ConfigurationException;
        }
    .end annotation

    .line 107
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v0}, Lcom/android/helper/device/Streamer;->getCodec()Lcom/android/helper/util/Codec;

    move-result-object v0

    .line 108
    iget-object v1, p0, Lcom/android/helper/video/SurfaceEncoder;->encoderName:Ljava/lang/String;

    invoke-static {v0, v1}, Lcom/android/helper/video/SurfaceEncoder;->createMediaCodec(Lcom/android/helper/util/Codec;Ljava/lang/String;)Landroid/media/MediaCodec;

    move-result-object v1

    .line 109
    invoke-interface {v0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object v2

    iget v3, p0, Lcom/android/helper/video/SurfaceEncoder;->videoBitRate:I

    iget v4, p0, Lcom/android/helper/video/SurfaceEncoder;->maxFps:F

    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->codecOptions:Ljava/util/List;

    invoke-static {v2, v3, v4, v5}, Lcom/android/helper/video/SurfaceEncoder;->createFormat(Ljava/lang/String;IFLjava/util/List;)Landroid/media/MediaFormat;

    move-result-object v2

    .line 111
    iget-object v3, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    iget-object v4, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v3, v4}, Lcom/android/helper/video/SurfaceCapture;->init(Lcom/android/helper/video/SurfaceCapture$CaptureListener;)V

    const/4 v3, 0x0

    const/4 v4, 0x0

    .line 118
    :cond_0
    :try_start_0
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v5}, Lcom/android/helper/video/CaptureReset;->consumeReset()Z

    .line 119
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v5}, Lcom/android/helper/video/SurfaceCapture;->prepare()V

    .line 120
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v5}, Lcom/android/helper/video/SurfaceCapture;->getSize()Lcom/android/helper/device/Size;

    move-result-object v5

    const/4 v6, 0x1

    if-nez v4, :cond_1

    .line 122
    iget-object v4, p0, Lcom/android/helper/video/SurfaceEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v4, v5}, Lcom/android/helper/device/Streamer;->writeVideoHeader(Lcom/android/helper/device/Size;)V

    const/4 v4, 0x1

    .line 126
    :cond_1
    const-string v7, "width"

    invoke-virtual {v5}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v8

    invoke-virtual {v2, v7, v8}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 127
    const-string v7, "height"

    invoke-virtual {v5}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v8

    invoke-virtual {v2, v7, v8}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_9

    const/4 v7, 0x0

    .line 134
    :try_start_1
    invoke-virtual {v1, v2, v7, v7, v6}, Landroid/media/MediaCodec;->configure(Landroid/media/MediaFormat;Landroid/view/Surface;Landroid/media/MediaCrypto;I)V
    :try_end_1
    .catch Landroid/media/MediaCodec$CodecException; {:try_start_1 .. :try_end_1} :catch_3
    .catch Ljava/lang/IllegalStateException; {:try_start_1 .. :try_end_1} :catch_2
    .catch Ljava/lang/IllegalArgumentException; {:try_start_1 .. :try_end_1} :catch_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_4

    :catchall_0
    move-exception v0

    move-object v8, v7

    :goto_0
    const/4 v6, 0x0

    :goto_1
    const/4 v10, 0x0

    goto/16 :goto_d

    :catch_0
    move-exception v8

    goto :goto_2

    :catch_1
    move-exception v8

    goto :goto_2

    :catch_2
    move-exception v8

    :goto_2
    move-object v9, v7

    :goto_3
    const/4 v10, 0x0

    const/4 v11, 0x0

    goto/16 :goto_b

    :catch_3
    move-exception v8

    .line 136
    :try_start_2
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->codecOptions:Ljava/util/List;

    if-eqz v9, :cond_6

    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->codecOptions:Ljava/util/List;

    invoke-interface {v9}, Ljava/util/List;->isEmpty()Z

    move-result v9

    if-nez v9, :cond_6

    .line 137
    new-instance v9, Ljava/lang/StringBuilder;

    invoke-direct {v9}, Ljava/lang/StringBuilder;-><init>()V

    const-string v10, "Codec configuration failed with custom options, retrying with default format fallback. Error: "

    invoke-virtual {v9, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v8}, Landroid/media/MediaCodec$CodecException;->getMessage()Ljava/lang/String;

    move-result-object v8

    invoke-virtual {v9, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-static {v8}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 138
    invoke-interface {v0}, Lcom/android/helper/util/Codec;->getMimeType()Ljava/lang/String;

    move-result-object v8

    iget v9, p0, Lcom/android/helper/video/SurfaceEncoder;->videoBitRate:I

    iget v10, p0, Lcom/android/helper/video/SurfaceEncoder;->maxFps:F

    invoke-static {v8, v9, v10, v7}, Lcom/android/helper/video/SurfaceEncoder;->createFormat(Ljava/lang/String;IFLjava/util/List;)Landroid/media/MediaFormat;

    move-result-object v8

    .line 139
    const-string v9, "width"

    invoke-virtual {v5}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v10

    invoke-virtual {v8, v9, v10}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 140
    const-string v9, "height"

    invoke-virtual {v5}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v10

    invoke-virtual {v8, v9, v10}, Landroid/media/MediaFormat;->setInteger(Ljava/lang/String;I)V

    .line 141
    invoke-virtual {v1, v8, v7, v7, v6}, Landroid/media/MediaCodec;->configure(Landroid/media/MediaFormat;Landroid/view/Surface;Landroid/media/MediaCrypto;I)V

    .line 146
    :goto_4
    invoke-virtual {v1}, Landroid/media/MediaCodec;->createInputSurface()Landroid/view/Surface;

    move-result-object v8
    :try_end_2
    .catch Ljava/lang/IllegalStateException; {:try_start_2 .. :try_end_2} :catch_2
    .catch Ljava/lang/IllegalArgumentException; {:try_start_2 .. :try_end_2} :catch_1
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_0
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    .line 148
    :try_start_3
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v9, v8}, Lcom/android/helper/video/SurfaceCapture;->start(Landroid/view/Surface;)V
    :try_end_3
    .catch Ljava/lang/IllegalStateException; {:try_start_3 .. :try_end_3} :catch_e
    .catch Ljava/lang/IllegalArgumentException; {:try_start_3 .. :try_end_3} :catch_d
    .catch Ljava/io/IOException; {:try_start_3 .. :try_end_3} :catch_c
    .catchall {:try_start_3 .. :try_end_3} :catchall_5

    .line 151
    :try_start_4
    invoke-virtual {v1}, Landroid/media/MediaCodec;->start()V
    :try_end_4
    .catch Ljava/lang/IllegalStateException; {:try_start_4 .. :try_end_4} :catch_b
    .catch Ljava/lang/IllegalArgumentException; {:try_start_4 .. :try_end_4} :catch_a
    .catch Ljava/io/IOException; {:try_start_4 .. :try_end_4} :catch_9
    .catchall {:try_start_4 .. :try_end_4} :catchall_4

    .line 154
    :try_start_5
    sget-object v9, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    monitor-enter v9
    :try_end_5
    .catch Ljava/lang/IllegalStateException; {:try_start_5 .. :try_end_5} :catch_8
    .catch Ljava/lang/IllegalArgumentException; {:try_start_5 .. :try_end_5} :catch_7
    .catch Ljava/io/IOException; {:try_start_5 .. :try_end_5} :catch_6
    .catchall {:try_start_5 .. :try_end_5} :catchall_3

    .line 155
    :try_start_6
    sput-object v1, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    .line 156
    sget-boolean v10, Lcom/android/helper/video/SurfaceEncoder;->pendingKeyFrame:Z

    if-eqz v10, :cond_2

    .line 157
    sput-boolean v3, Lcom/android/helper/video/SurfaceEncoder;->pendingKeyFrame:Z
    :try_end_6
    .catchall {:try_start_6 .. :try_end_6} :catchall_2

    .line 159
    :try_start_7
    new-instance v10, Landroid/os/Bundle;

    invoke-direct {v10}, Landroid/os/Bundle;-><init>()V

    .line 160
    const-string v11, "request-sync"

    invoke-virtual {v10, v11, v3}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 161
    sget-object v11, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    invoke-virtual {v11, v10}, Landroid/media/MediaCodec;->setParameters(Landroid/os/Bundle;)V

    .line 162
    const-string v10, "KeyframeTrace request-sync-frame (deferred) applied successfully"

    invoke-static {v10}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_7
    .catch Ljava/lang/IllegalStateException; {:try_start_7 .. :try_end_7} :catch_4
    .catchall {:try_start_7 .. :try_end_7} :catchall_2

    goto :goto_5

    :catch_4
    move-exception v10

    .line 164
    :try_start_8
    new-instance v11, Ljava/lang/StringBuilder;

    invoke-direct {v11}, Ljava/lang/StringBuilder;-><init>()V

    const-string v12, "KeyframeTrace request-sync-frame (deferred) failed: "

    invoke-virtual {v11, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v10}, Ljava/lang/IllegalStateException;->getMessage()Ljava/lang/String;

    move-result-object v10

    invoke-virtual {v11, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v11}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v10

    invoke-static {v10}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 167
    :cond_2
    :goto_5
    monitor-exit v9
    :try_end_8
    .catchall {:try_start_8 .. :try_end_8} :catchall_2

    .line 170
    :try_start_9
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v9, v1}, Lcom/android/helper/video/CaptureReset;->setRunningMediaCodec(Landroid/media/MediaCodec;)V

    .line 172
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->stopped:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v9}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v9

    if-eqz v9, :cond_4

    :cond_3
    const/4 v6, 0x0

    goto :goto_6

    .line 175
    :cond_4
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v9}, Lcom/android/helper/video/CaptureReset;->consumeReset()Z

    move-result v9

    if-nez v9, :cond_5

    .line 178
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-direct {p0, v1, v9}, Lcom/android/helper/video/SurfaceEncoder;->encode(Landroid/media/MediaCodec;Lcom/android/helper/device/Streamer;)V

    .line 181
    :cond_5
    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->stopped:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v9}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v9

    if-nez v9, :cond_3

    iget-object v9, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v9}, Lcom/android/helper/video/SurfaceCapture;->isClosed()Z

    move-result v5
    :try_end_9
    .catch Ljava/lang/IllegalStateException; {:try_start_9 .. :try_end_9} :catch_8
    .catch Ljava/lang/IllegalArgumentException; {:try_start_9 .. :try_end_9} :catch_7
    .catch Ljava/io/IOException; {:try_start_9 .. :try_end_9} :catch_6
    .catchall {:try_start_9 .. :try_end_9} :catchall_3

    if-nez v5, :cond_3

    .line 194
    :goto_6
    :try_start_a
    sget-object v5, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    monitor-enter v5
    :try_end_a
    .catchall {:try_start_a .. :try_end_a} :catchall_9

    .line 195
    :try_start_b
    sput-object v7, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    .line 196
    sput-boolean v3, Lcom/android/helper/video/SurfaceEncoder;->pendingKeyFrame:Z

    .line 197
    monitor-exit v5
    :try_end_b
    .catchall {:try_start_b .. :try_end_b} :catchall_1

    .line 198
    :try_start_c
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v5, v7}, Lcom/android/helper/video/CaptureReset;->setRunningMediaCodec(Landroid/media/MediaCodec;)V

    .line 200
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v5}, Lcom/android/helper/video/SurfaceCapture;->stop()V
    :try_end_c
    .catchall {:try_start_c .. :try_end_c} :catchall_9

    .line 204
    :try_start_d
    invoke-virtual {v1}, Landroid/media/MediaCodec;->stop()V
    :try_end_d
    .catch Ljava/lang/IllegalStateException; {:try_start_d .. :try_end_d} :catch_5
    .catchall {:try_start_d .. :try_end_d} :catchall_9

    .line 209
    :catch_5
    :try_start_e
    invoke-virtual {v1}, Landroid/media/MediaCodec;->reset()V

    if-eqz v8, :cond_9

    .line 211
    invoke-virtual {v8}, Landroid/view/Surface;->release()V
    :try_end_e
    .catchall {:try_start_e .. :try_end_e} :catchall_9

    goto/16 :goto_c

    :catchall_1
    move-exception v0

    .line 197
    :try_start_f
    monitor-exit v5
    :try_end_f
    .catchall {:try_start_f .. :try_end_f} :catchall_1

    :try_start_10
    throw v0
    :try_end_10
    .catchall {:try_start_10 .. :try_end_10} :catchall_9

    :catchall_2
    move-exception v10

    .line 167
    :try_start_11
    monitor-exit v9
    :try_end_11
    .catchall {:try_start_11 .. :try_end_11} :catchall_2

    :try_start_12
    throw v10
    :try_end_12
    .catch Ljava/lang/IllegalStateException; {:try_start_12 .. :try_end_12} :catch_8
    .catch Ljava/lang/IllegalArgumentException; {:try_start_12 .. :try_end_12} :catch_7
    .catch Ljava/io/IOException; {:try_start_12 .. :try_end_12} :catch_6
    .catchall {:try_start_12 .. :try_end_12} :catchall_3

    :catchall_3
    move-exception v0

    const/4 v10, 0x1

    goto/16 :goto_d

    :catch_6
    move-exception v9

    goto :goto_7

    :catch_7
    move-exception v9

    goto :goto_7

    :catch_8
    move-exception v9

    :goto_7
    move-object v10, v9

    move-object v9, v8

    move-object v8, v10

    const/4 v10, 0x1

    goto :goto_9

    :catchall_4
    move-exception v0

    goto/16 :goto_1

    :catch_9
    move-exception v9

    goto :goto_8

    :catch_a
    move-exception v9

    goto :goto_8

    :catch_b
    move-exception v9

    :goto_8
    move-object v10, v9

    move-object v9, v8

    move-object v8, v10

    const/4 v10, 0x0

    :goto_9
    const/4 v11, 0x1

    goto :goto_b

    :catchall_5
    move-exception v0

    goto/16 :goto_0

    :catch_c
    move-exception v9

    goto :goto_a

    :catch_d
    move-exception v9

    goto :goto_a

    :catch_e
    move-exception v9

    :goto_a
    move-object v10, v9

    move-object v9, v8

    move-object v8, v10

    goto/16 :goto_3

    .line 143
    :cond_6
    :try_start_13
    throw v8
    :try_end_13
    .catch Ljava/lang/IllegalStateException; {:try_start_13 .. :try_end_13} :catch_2
    .catch Ljava/lang/IllegalArgumentException; {:try_start_13 .. :try_end_13} :catch_1
    .catch Ljava/io/IOException; {:try_start_13 .. :try_end_13} :catch_0
    .catchall {:try_start_13 .. :try_end_13} :catchall_0

    .line 184
    :goto_b
    :try_start_14
    invoke-static {v8}, Lcom/android/helper/util/IO;->isBrokenPipe(Ljava/lang/Exception;)Z

    move-result v12

    if-nez v12, :cond_b

    .line 188
    new-instance v12, Ljava/lang/StringBuilder;

    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    const-string v13, "Capture/encoding error: "

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v8}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v13

    invoke-virtual {v13}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v13

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v13, ": "

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v8}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v13

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v12

    invoke-static {v12}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 189
    invoke-direct {p0, v5}, Lcom/android/helper/video/SurfaceEncoder;->prepareRetry(Lcom/android/helper/device/Size;)Z

    move-result v5
    :try_end_14
    .catchall {:try_start_14 .. :try_end_14} :catchall_7

    if-eqz v5, :cond_a

    .line 194
    :try_start_15
    sget-object v5, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    monitor-enter v5
    :try_end_15
    .catchall {:try_start_15 .. :try_end_15} :catchall_9

    .line 195
    :try_start_16
    sput-object v7, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    .line 196
    sput-boolean v3, Lcom/android/helper/video/SurfaceEncoder;->pendingKeyFrame:Z

    .line 197
    monitor-exit v5
    :try_end_16
    .catchall {:try_start_16 .. :try_end_16} :catchall_6

    .line 198
    :try_start_17
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v5, v7}, Lcom/android/helper/video/CaptureReset;->setRunningMediaCodec(Landroid/media/MediaCodec;)V

    if-eqz v11, :cond_7

    .line 200
    iget-object v5, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v5}, Lcom/android/helper/video/SurfaceCapture;->stop()V
    :try_end_17
    .catchall {:try_start_17 .. :try_end_17} :catchall_9

    :cond_7
    if-eqz v10, :cond_8

    .line 204
    :try_start_18
    invoke-virtual {v1}, Landroid/media/MediaCodec;->stop()V
    :try_end_18
    .catch Ljava/lang/IllegalStateException; {:try_start_18 .. :try_end_18} :catch_f
    .catchall {:try_start_18 .. :try_end_18} :catchall_9

    .line 209
    :catch_f
    :cond_8
    :try_start_19
    invoke-virtual {v1}, Landroid/media/MediaCodec;->reset()V

    if-eqz v9, :cond_9

    .line 211
    invoke-virtual {v9}, Landroid/view/Surface;->release()V
    :try_end_19
    .catchall {:try_start_19 .. :try_end_19} :catchall_9

    :cond_9
    :goto_c
    if-nez v6, :cond_0

    .line 216
    invoke-virtual {v1}, Landroid/media/MediaCodec;->release()V

    .line 217
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v0}, Lcom/android/helper/video/SurfaceCapture;->release()V

    return-void

    :catchall_6
    move-exception v0

    .line 197
    :try_start_1a
    monitor-exit v5
    :try_end_1a
    .catchall {:try_start_1a .. :try_end_1a} :catchall_6

    :try_start_1b
    throw v0
    :try_end_1b
    .catchall {:try_start_1b .. :try_end_1b} :catchall_9

    .line 190
    :cond_a
    :try_start_1c
    throw v8

    .line 186
    :cond_b
    throw v8
    :try_end_1c
    .catchall {:try_start_1c .. :try_end_1c} :catchall_7

    :catchall_7
    move-exception v0

    move-object v8, v9

    move v6, v11

    .line 194
    :goto_d
    :try_start_1d
    sget-object v2, Lcom/android/helper/video/SurfaceEncoder;->codecLock:Ljava/lang/Object;

    monitor-enter v2
    :try_end_1d
    .catchall {:try_start_1d .. :try_end_1d} :catchall_9

    .line 195
    :try_start_1e
    sput-object v7, Lcom/android/helper/video/SurfaceEncoder;->activeCodec:Landroid/media/MediaCodec;

    .line 196
    sput-boolean v3, Lcom/android/helper/video/SurfaceEncoder;->pendingKeyFrame:Z

    .line 197
    monitor-exit v2
    :try_end_1e
    .catchall {:try_start_1e .. :try_end_1e} :catchall_8

    .line 198
    :try_start_1f
    iget-object v2, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v2, v7}, Lcom/android/helper/video/CaptureReset;->setRunningMediaCodec(Landroid/media/MediaCodec;)V

    if-eqz v6, :cond_c

    .line 200
    iget-object v2, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v2}, Lcom/android/helper/video/SurfaceCapture;->stop()V
    :try_end_1f
    .catchall {:try_start_1f .. :try_end_1f} :catchall_9

    :cond_c
    if-eqz v10, :cond_d

    .line 204
    :try_start_20
    invoke-virtual {v1}, Landroid/media/MediaCodec;->stop()V
    :try_end_20
    .catch Ljava/lang/IllegalStateException; {:try_start_20 .. :try_end_20} :catch_10
    .catchall {:try_start_20 .. :try_end_20} :catchall_9

    .line 209
    :catch_10
    :cond_d
    :try_start_21
    invoke-virtual {v1}, Landroid/media/MediaCodec;->reset()V

    if-eqz v8, :cond_e

    .line 211
    invoke-virtual {v8}, Landroid/view/Surface;->release()V

    .line 213
    :cond_e
    throw v0
    :try_end_21
    .catchall {:try_start_21 .. :try_end_21} :catchall_9

    :catchall_8
    move-exception v0

    .line 197
    :try_start_22
    monitor-exit v2
    :try_end_22
    .catchall {:try_start_22 .. :try_end_22} :catchall_8

    :try_start_23
    throw v0
    :try_end_23
    .catchall {:try_start_23 .. :try_end_23} :catchall_9

    :catchall_9
    move-exception v0

    .line 216
    invoke-virtual {v1}, Landroid/media/MediaCodec;->release()V

    .line 217
    iget-object v1, p0, Lcom/android/helper/video/SurfaceEncoder;->capture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v1}, Lcom/android/helper/video/SurfaceCapture;->release()V

    .line 218
    throw v0
.end method


# virtual methods
.method public join()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 427
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 428
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    :cond_0
    return-void
.end method

.method synthetic lambda$start$0$com-android-helper-video-SurfaceEncoder(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 4

    .line 398
    const-string v0, "Screen streaming stopped"

    invoke-static {}, Landroid/os/Looper;->prepare()V

    const/4 v1, 0x1

    .line 401
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/video/SurfaceEncoder;->streamCapture()V
    :try_end_0
    .catch Lcom/android/helper/device/ConfigurationException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 410
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 411
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    return-void

    :catchall_0
    move-exception v2

    goto :goto_0

    :catch_0
    move-exception v2

    .line 406
    :try_start_1
    invoke-static {v2}, Lcom/android/helper/util/IO;->isBrokenPipe(Ljava/io/IOException;)Z

    move-result v3

    if-nez v3, :cond_0

    .line 407
    const-string v3, "Video encoding error"

    invoke-static {v3, v2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_1

    .line 410
    :goto_0
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 411
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    .line 412
    throw v2

    .line 410
    :catch_1
    :cond_0
    :goto_1
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 411
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    return-void
.end method

.method public start(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 2

    .line 395
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/video/SurfaceEncoder;Lcom/android/helper/AsyncProcessor$TerminationListener;)V

    const-string p1, "video"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->thread:Ljava/lang/Thread;

    .line 414
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method public stop()V
    .locals 2

    .line 419
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 420
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->stopped:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 421
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder;->reset:Lcom/android/helper/video/CaptureReset;

    invoke-virtual {v0}, Lcom/android/helper/video/CaptureReset;->reset()V

    :cond_0
    return-void
.end method
