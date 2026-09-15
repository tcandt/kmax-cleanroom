.class Lcom/android/helper/video/CameraCapture$2;
.super Landroid/hardware/camera2/CameraCaptureSession$StateCallback;
.source "CameraCapture.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/android/helper/video/CameraCapture;->createCaptureSession(Landroid/hardware/camera2/CameraDevice;Landroid/view/Surface;)Landroid/hardware/camera2/CameraCaptureSession;
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

    .line 397
    iput-object p1, p0, Lcom/android/helper/video/CameraCapture$2;->this$0:Lcom/android/helper/video/CameraCapture;

    iput-object p2, p0, Lcom/android/helper/video/CameraCapture$2;->val$future:Ljava/util/concurrent/CompletableFuture;

    invoke-direct {p0}, Landroid/hardware/camera2/CameraCaptureSession$StateCallback;-><init>()V

    return-void
.end method


# virtual methods
.method public onConfigureFailed(Landroid/hardware/camera2/CameraCaptureSession;)V
    .locals 2

    .line 405
    iget-object p1, p0, Lcom/android/helper/video/CameraCapture$2;->val$future:Ljava/util/concurrent/CompletableFuture;

    new-instance v0, Landroid/hardware/camera2/CameraAccessException;

    const/4 v1, 0x3

    invoke-direct {v0, v1}, Landroid/hardware/camera2/CameraAccessException;-><init>(I)V

    invoke-static {p1, v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/concurrent/CompletableFuture;Ljava/lang/Throwable;)Z

    return-void
.end method

.method public onConfigured(Landroid/hardware/camera2/CameraCaptureSession;)V
    .locals 1

    .line 400
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture$2;->val$future:Ljava/util/concurrent/CompletableFuture;

    invoke-static {v0, p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/concurrent/CompletableFuture;Ljava/lang/Object;)Z

    return-void
.end method
