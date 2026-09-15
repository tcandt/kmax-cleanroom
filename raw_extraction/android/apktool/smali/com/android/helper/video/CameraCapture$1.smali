.class Lcom/android/helper/video/CameraCapture$1;
.super Landroid/hardware/camera2/CameraDevice$StateCallback;
.source "CameraCapture.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/android/helper/video/CameraCapture;->openCamera(Ljava/lang/String;)Landroid/hardware/camera2/CameraDevice;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/android/helper/video/CameraCapture;

.field final synthetic val$future:Ljava/util/concurrent/CompletableFuture;


# direct methods
.method constructor <init>(Lcom/android/helper/video/CameraCapture;Ljava/util/concurrent/CompletableFuture;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010
        }
        names = {
            null,
            null
        }
    .end annotation

    .line 346
    iput-object p1, p0, Lcom/android/helper/video/CameraCapture$1;->this$0:Lcom/android/helper/video/CameraCapture;

    iput-object p2, p0, Lcom/android/helper/video/CameraCapture$1;->val$future:Ljava/util/concurrent/CompletableFuture;

    invoke-direct {p0}, Landroid/hardware/camera2/CameraDevice$StateCallback;-><init>()V

    return-void
.end method


# virtual methods
.method public onDisconnected(Landroid/hardware/camera2/CameraDevice;)V
    .locals 1

    .line 355
    const-string p1, "Camera disconnected"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 356
    iget-object p1, p0, Lcom/android/helper/video/CameraCapture$1;->this$0:Lcom/android/helper/video/CameraCapture;

    invoke-static {p1}, Lcom/android/helper/video/CameraCapture;->access$000(Lcom/android/helper/video/CameraCapture;)Ljava/util/concurrent/atomic/AtomicBoolean;

    move-result-object p1

    const/4 v0, 0x1

    invoke-virtual {p1, v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 357
    iget-object p1, p0, Lcom/android/helper/video/CameraCapture$1;->this$0:Lcom/android/helper/video/CameraCapture;

    invoke-virtual {p1}, Lcom/android/helper/video/CameraCapture;->invalidate()V

    return-void
.end method

.method public onError(Landroid/hardware/camera2/CameraDevice;I)V
    .locals 1

    const/4 p1, 0x1

    if-eq p2, p1, :cond_1

    const/4 v0, 0x2

    if-eq p2, v0, :cond_0

    const/4 v0, 0x3

    if-eq p2, v0, :cond_2

    const/4 p1, 0x3

    goto :goto_0

    :cond_0
    const/4 p1, 0x5

    goto :goto_0

    :cond_1
    const/4 p1, 0x4

    .line 379
    :cond_2
    :goto_0
    iget-object p2, p0, Lcom/android/helper/video/CameraCapture$1;->val$future:Ljava/util/concurrent/CompletableFuture;

    new-instance v0, Landroid/hardware/camera2/CameraAccessException;

    invoke-direct {v0, p1}, Landroid/hardware/camera2/CameraAccessException;-><init>(I)V

    invoke-static {p2, v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/concurrent/CompletableFuture;Ljava/lang/Throwable;)Z

    return-void
.end method

.method public onOpened(Landroid/hardware/camera2/CameraDevice;)V
    .locals 1

    .line 349
    const-string v0, "Camera opened successfully"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 350
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture$1;->val$future:Ljava/util/concurrent/CompletableFuture;

    invoke-static {v0, p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/concurrent/CompletableFuture;Ljava/lang/Object;)Z

    return-void
.end method
