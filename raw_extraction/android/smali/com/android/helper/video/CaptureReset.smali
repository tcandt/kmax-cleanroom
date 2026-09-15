.class public Lcom/android/helper/video/CaptureReset;
.super Ljava/lang/Object;
.source "CaptureReset.java"

# interfaces
.implements Lcom/android/helper/video/SurfaceCapture$CaptureListener;


# instance fields
.field private final reset:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private runningMediaCodec:Landroid/media/MediaCodec;


# direct methods
.method public constructor <init>()V
    .locals 1

    .line 7
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 9
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-direct {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>()V

    iput-object v0, p0, Lcom/android/helper/video/CaptureReset;->reset:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-void
.end method


# virtual methods
.method public consumeReset()Z
    .locals 2

    .line 15
    iget-object v0, p0, Lcom/android/helper/video/CaptureReset;->reset:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->getAndSet(Z)Z

    move-result v0

    return v0
.end method

.method public onInvalidated()V
    .locals 0

    .line 35
    invoke-virtual {p0}, Lcom/android/helper/video/CaptureReset;->reset()V

    return-void
.end method

.method public declared-synchronized reset()V
    .locals 2

    monitor-enter p0

    .line 19
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/video/CaptureReset;->reset:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 20
    iget-object v0, p0, Lcom/android/helper/video/CaptureReset;->runningMediaCodec:Landroid/media/MediaCodec;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v0, :cond_0

    .line 22
    :try_start_1
    invoke-virtual {v0}, Landroid/media/MediaCodec;->signalEndOfInputStream()V
    :try_end_1
    .catch Ljava/lang/IllegalStateException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    .line 27
    :catch_0
    :cond_0
    monitor-exit p0

    return-void

    :catchall_0
    move-exception v0

    :try_start_2
    monitor-exit p0
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    throw v0
.end method

.method public declared-synchronized setRunningMediaCodec(Landroid/media/MediaCodec;)V
    .locals 0

    monitor-enter p0

    .line 30
    :try_start_0
    iput-object p1, p0, Lcom/android/helper/video/CaptureReset;->runningMediaCodec:Landroid/media/MediaCodec;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 31
    monitor-exit p0

    return-void

    :catchall_0
    move-exception p1

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw p1
.end method
