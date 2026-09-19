.class public final Lcom/android/helper/audio/AudioRawRecorder;
.super Ljava/lang/Object;
.source "AudioRawRecorder.java"

# interfaces
.implements Lcom/android/helper/AsyncProcessor;


# instance fields
.field private final capture:Lcom/android/helper/audio/AudioCapture;

.field private final streamer:Lcom/android/helper/device/Streamer;

.field private thread:Ljava/lang/Thread;


# direct methods
.method public constructor <init>(Lcom/android/helper/audio/AudioCapture;Lcom/android/helper/device/Streamer;)V
    .locals 0

    .line 22
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 23
    iput-object p1, p0, Lcom/android/helper/audio/AudioRawRecorder;->capture:Lcom/android/helper/audio/AudioCapture;

    .line 24
    iput-object p2, p0, Lcom/android/helper/audio/AudioRawRecorder;->streamer:Lcom/android/helper/device/Streamer;

    return-void
.end method

.method private record()V
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation

    .line 28
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1e

    const/4 v2, 0x0

    if-ge v0, v1, :cond_0

    .line 29
    const-string v0, "Audio disabled: it is not supported before Android 11"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 30
    iget-object v0, p0, Lcom/android/helper/audio/AudioRawRecorder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v0, v2}, Lcom/android/helper/device/Streamer;->writeDisableStream(Z)V

    return-void

    :cond_0
    const/16 v0, 0x1000

    .line 34
    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocateDirect(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    .line 35
    new-instance v1, Landroid/media/MediaCodec$BufferInfo;

    invoke-direct {v1}, Landroid/media/MediaCodec$BufferInfo;-><init>()V

    .line 39
    :try_start_0
    iget-object v3, p0, Lcom/android/helper/audio/AudioRawRecorder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v3}, Lcom/android/helper/audio/AudioCapture;->start()V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 46
    :try_start_1
    iget-object v3, p0, Lcom/android/helper/audio/AudioRawRecorder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v3}, Lcom/android/helper/device/Streamer;->writeAudioHeader()V

    .line 47
    :goto_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/Thread;->isInterrupted()Z

    move-result v3

    if-nez v3, :cond_2

    .line 48
    invoke-virtual {v0, v2}, Ljava/nio/ByteBuffer;->position(I)Ljava/nio/Buffer;

    .line 49
    iget-object v3, p0, Lcom/android/helper/audio/AudioRawRecorder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v3, v0, v1}, Lcom/android/helper/audio/AudioCapture;->read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I

    move-result v3

    if-ltz v3, :cond_1

    .line 53
    invoke-virtual {v0, v3}, Ljava/nio/ByteBuffer;->limit(I)Ljava/nio/Buffer;

    .line 55
    iget-object v3, p0, Lcom/android/helper/audio/AudioRawRecorder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v3, v0, v1}, Lcom/android/helper/device/Streamer;->writePacket(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)V

    goto :goto_0

    .line 51
    :cond_1
    new-instance v0, Ljava/io/IOException;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Could not read audio: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    .line 63
    :cond_2
    iget-object v0, p0, Lcom/android/helper/audio/AudioRawRecorder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v0}, Lcom/android/helper/audio/AudioCapture;->stop()V

    return-void

    :catchall_0
    move-exception v0

    .line 42
    :try_start_2
    iget-object v1, p0, Lcom/android/helper/audio/AudioRawRecorder;->streamer:Lcom/android/helper/device/Streamer;

    invoke-virtual {v1, v2}, Lcom/android/helper/device/Streamer;->writeDisableStream(Z)V

    .line 43
    throw v0
    :try_end_2
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_0
    .catchall {:try_start_2 .. :try_end_2} :catchall_1

    :catchall_1
    move-exception v0

    goto :goto_1

    :catch_0
    move-exception v0

    .line 59
    :try_start_3
    invoke-static {v0}, Lcom/android/helper/util/IO;->isBrokenPipe(Ljava/io/IOException;)Z

    move-result v1

    if-nez v1, :cond_3

    .line 60
    const-string v1, "Audio capture error"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_1

    .line 63
    :cond_3
    iget-object v0, p0, Lcom/android/helper/audio/AudioRawRecorder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v0}, Lcom/android/helper/audio/AudioCapture;->stop()V

    return-void

    :goto_1
    iget-object v1, p0, Lcom/android/helper/audio/AudioRawRecorder;->capture:Lcom/android/helper/audio/AudioCapture;

    invoke-interface {v1}, Lcom/android/helper/audio/AudioCapture;->stop()V

    .line 64
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

    .line 95
    iget-object v0, p0, Lcom/android/helper/audio/AudioRawRecorder;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 96
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    :cond_0
    return-void
.end method

.method synthetic lambda$start$0$com-android-helper-audio-AudioRawRecorder(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 4

    .line 70
    const-string v0, "Audio recorder stopped"

    const/4 v1, 0x0

    .line 72
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/audio/AudioRawRecorder;->record()V
    :try_end_0
    .catch Lcom/android/helper/audio/AudioCaptureException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 79
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 80
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    return-void

    :catchall_0
    move-exception v2

    .line 76
    :try_start_1
    const-string v3, "Audio recording error"

    invoke-static {v3, v2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    .line 79
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    const/4 v0, 0x1

    .line 80
    invoke-interface {p1, v0}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    goto :goto_0

    :catchall_1
    move-exception v2

    .line 79
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 80
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    .line 81
    throw v2

    .line 79
    :catch_0
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 80
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    :goto_0
    return-void
.end method

.method public start(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 2

    .line 69
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/android/helper/audio/AudioRawRecorder$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/audio/AudioRawRecorder$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/audio/AudioRawRecorder;Lcom/android/helper/AsyncProcessor$TerminationListener;)V

    const-string p1, "audio-raw"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v0, p0, Lcom/android/helper/audio/AudioRawRecorder;->thread:Ljava/lang/Thread;

    .line 83
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method public stop()V
    .locals 1

    .line 88
    iget-object v0, p0, Lcom/android/helper/audio/AudioRawRecorder;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 89
    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    :cond_0
    return-void
.end method
