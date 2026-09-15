.class final Lcom/android/helper/audio/AudioEncoder$EncoderCallback;
.super Landroid/media/MediaCodec$Callback;
.source "AudioEncoder.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/audio/AudioEncoder;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x12
    name = "EncoderCallback"
.end annotation


# instance fields
.field final synthetic this$0:Lcom/android/helper/audio/AudioEncoder;


# direct methods
.method private constructor <init>(Lcom/android/helper/audio/AudioEncoder;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x1010
        }
        names = {
            null
        }
    .end annotation

    .line 349
    iput-object p1, p0, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;->this$0:Lcom/android/helper/audio/AudioEncoder;

    invoke-direct {p0}, Landroid/media/MediaCodec$Callback;-><init>()V

    return-void
.end method

.method synthetic constructor <init>(Lcom/android/helper/audio/AudioEncoder;Lcom/android/helper/audio/AudioEncoder$1;)V
    .locals 0

    .line 349
    invoke-direct {p0, p1}, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;-><init>(Lcom/android/helper/audio/AudioEncoder;)V

    return-void
.end method


# virtual methods
.method public onError(Landroid/media/MediaCodec;Landroid/media/MediaCodec$CodecException;)V
    .locals 0

    .line 371
    const-string p1, "MediaCodec error"

    invoke-static {p1, p2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 372
    iget-object p1, p0, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;->this$0:Lcom/android/helper/audio/AudioEncoder;

    invoke-static {p1}, Lcom/android/helper/audio/AudioEncoder;->access$500(Lcom/android/helper/audio/AudioEncoder;)V

    return-void
.end method

.method public onInputBufferAvailable(Landroid/media/MediaCodec;I)V
    .locals 1

    .line 354
    :try_start_0
    iget-object p1, p0, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;->this$0:Lcom/android/helper/audio/AudioEncoder;

    invoke-static {p1}, Lcom/android/helper/audio/AudioEncoder;->access$400(Lcom/android/helper/audio/AudioEncoder;)Ljava/util/concurrent/BlockingQueue;

    move-result-object p1

    new-instance v0, Lcom/android/helper/audio/AudioEncoder$InputTask;

    invoke-direct {v0, p2}, Lcom/android/helper/audio/AudioEncoder$InputTask;-><init>(I)V

    invoke-interface {p1, v0}, Ljava/util/concurrent/BlockingQueue;->put(Ljava/lang/Object;)V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    .line 356
    :catch_0
    iget-object p1, p0, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;->this$0:Lcom/android/helper/audio/AudioEncoder;

    invoke-static {p1}, Lcom/android/helper/audio/AudioEncoder;->access$500(Lcom/android/helper/audio/AudioEncoder;)V

    return-void
.end method

.method public onOutputBufferAvailable(Landroid/media/MediaCodec;ILandroid/media/MediaCodec$BufferInfo;)V
    .locals 1

    .line 363
    :try_start_0
    iget-object p1, p0, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;->this$0:Lcom/android/helper/audio/AudioEncoder;

    invoke-static {p1}, Lcom/android/helper/audio/AudioEncoder;->access$600(Lcom/android/helper/audio/AudioEncoder;)Ljava/util/concurrent/BlockingQueue;

    move-result-object p1

    new-instance v0, Lcom/android/helper/audio/AudioEncoder$OutputTask;

    invoke-direct {v0, p2, p3}, Lcom/android/helper/audio/AudioEncoder$OutputTask;-><init>(ILandroid/media/MediaCodec$BufferInfo;)V

    invoke-interface {p1, v0}, Ljava/util/concurrent/BlockingQueue;->put(Ljava/lang/Object;)V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    .line 365
    :catch_0
    iget-object p1, p0, Lcom/android/helper/audio/AudioEncoder$EncoderCallback;->this$0:Lcom/android/helper/audio/AudioEncoder;

    invoke-static {p1}, Lcom/android/helper/audio/AudioEncoder;->access$500(Lcom/android/helper/audio/AudioEncoder;)V

    return-void
.end method

.method public onOutputFormatChanged(Landroid/media/MediaCodec;Landroid/media/MediaFormat;)V
    .locals 0

    return-void
.end method
