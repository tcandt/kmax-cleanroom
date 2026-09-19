.class public interface abstract Lcom/android/helper/audio/AudioCapture;
.super Ljava/lang/Object;
.source "AudioCapture.java"


# virtual methods
.method public abstract checkCompatibility()V
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation
.end method

.method public abstract read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I
.end method

.method public abstract start()V
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/audio/AudioCaptureException;
        }
    .end annotation
.end method

.method public abstract stop()V
.end method
