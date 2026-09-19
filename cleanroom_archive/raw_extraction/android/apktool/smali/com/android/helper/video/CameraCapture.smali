.class public Lcom/android/helper/video/CameraCapture;
.super Lcom/android/helper/video/SurfaceCapture;
.source "CameraCapture.java"


# static fields
.field static final synthetic $assertionsDisabled:Z

.field public static final VFLIP_MATRIX:[F


# instance fields
.field private final angle:F

.field private final aspectRatio:Lcom/android/helper/video/CameraAspectRatio;

.field private cameraDevice:Landroid/hardware/camera2/CameraDevice;

.field private cameraExecutor:Ljava/util/concurrent/Executor;

.field private final cameraFacing:Lcom/android/helper/video/CameraFacing;

.field private cameraHandler:Landroid/os/Handler;

.field private cameraId:Ljava/lang/String;

.field private cameraThread:Landroid/os/HandlerThread;

.field private final cameraZoom:F

.field private final captureOrientation:Lcom/android/helper/device/Orientation;

.field private captureSize:Lcom/android/helper/device/Size;

.field private final crop:Landroid/graphics/Rect;

.field private final disconnected:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private final explicitCameraId:Ljava/lang/String;

.field private final explicitSize:Lcom/android/helper/device/Size;

.field private final fps:I

.field private glRunner:Lcom/android/helper/opengl/OpenGLRunner;

.field private final highSpeed:Z

.field private maxSize:I

.field private transform:Lcom/android/helper/util/AffineMatrix;

.field private videoSize:Lcom/android/helper/device/Size;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    const/16 v0, 0x10

    .line 51
    new-array v0, v0, [F

    fill-array-data v0, :array_0

    sput-object v0, Lcom/android/helper/video/CameraCapture;->VFLIP_MATRIX:[F

    return-void

    :array_0
    .array-data 4
        0x3f800000    # 1.0f
        0x0
        0x0
        0x0
        0x0
        -0x40800000    # -1.0f
        0x0
        0x0
        0x0
        0x0
        0x3f800000    # 1.0f
        0x0
        0x0
        0x3f800000    # 1.0f
        0x0
        0x3f800000    # 1.0f
    .end array-data
.end method

.method public constructor <init>(Lcom/android/helper/Options;)V
    .locals 1

    .line 84
    invoke-direct {p0}, Lcom/android/helper/video/SurfaceCapture;-><init>()V

    .line 82
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-direct {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>()V

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->disconnected:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 85
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraId()Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->explicitCameraId:Ljava/lang/String;

    .line 86
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraFacing()Lcom/android/helper/video/CameraFacing;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraFacing:Lcom/android/helper/video/CameraFacing;

    .line 87
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraSize()Lcom/android/helper/device/Size;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->explicitSize:Lcom/android/helper/device/Size;

    .line 88
    invoke-virtual {p1}, Lcom/android/helper/Options;->getMaxSize()I

    move-result v0

    iput v0, p0, Lcom/android/helper/video/CameraCapture;->maxSize:I

    .line 89
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraAspectRatio()Lcom/android/helper/video/CameraAspectRatio;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->aspectRatio:Lcom/android/helper/video/CameraAspectRatio;

    .line 90
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraFps()I

    move-result v0

    iput v0, p0, Lcom/android/helper/video/CameraCapture;->fps:I

    .line 91
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraHighSpeed()Z

    move-result v0

    iput-boolean v0, p0, Lcom/android/helper/video/CameraCapture;->highSpeed:Z

    .line 92
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCrop()Landroid/graphics/Rect;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->crop:Landroid/graphics/Rect;

    .line 93
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCaptureOrientation()Lcom/android/helper/device/Orientation;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    .line 95
    invoke-virtual {p1}, Lcom/android/helper/Options;->getAngle()F

    move-result v0

    iput v0, p0, Lcom/android/helper/video/CameraCapture;->angle:F

    .line 96
    invoke-virtual {p1}, Lcom/android/helper/Options;->getCameraZoom()F

    move-result p1

    iput p1, p0, Lcom/android/helper/video/CameraCapture;->cameraZoom:F

    return-void
.end method

.method static synthetic access$000(Lcom/android/helper/video/CameraCapture;)Ljava/util/concurrent/atomic/AtomicBoolean;
    .locals 0

    .line 49
    iget-object p0, p0, Lcom/android/helper/video/CameraCapture;->disconnected:Ljava/util/concurrent/atomic/AtomicBoolean;

    return-object p0
.end method

.method private createCaptureRequest(Landroid/view/Surface;)Landroid/hardware/camera2/CaptureRequest;
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/hardware/camera2/CameraAccessException;
        }
    .end annotation

    const-string v0, "Camera hardware zoom ratio applied: "

    .line 419
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraDevice:Landroid/hardware/camera2/CameraDevice;

    const/4 v2, 0x3

    invoke-virtual {v1, v2}, Landroid/hardware/camera2/CameraDevice;->createCaptureRequest(I)Landroid/hardware/camera2/CaptureRequest$Builder;

    move-result-object v1

    .line 420
    invoke-virtual {v1, p1}, Landroid/hardware/camera2/CaptureRequest$Builder;->addTarget(Landroid/view/Surface;)V

    .line 422
    iget p1, p0, Lcom/android/helper/video/CameraCapture;->fps:I

    if-lez p1, :cond_0

    .line 423
    sget-object p1, Landroid/hardware/camera2/CaptureRequest;->CONTROL_AE_TARGET_FPS_RANGE:Landroid/hardware/camera2/CaptureRequest$Key;

    new-instance v2, Landroid/util/Range;

    iget v3, p0, Lcom/android/helper/video/CameraCapture;->fps:I

    invoke-static {v3}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    iget v4, p0, Lcom/android/helper/video/CameraCapture;->fps:I

    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v4

    invoke-direct {v2, v3, v4}, Landroid/util/Range;-><init>(Ljava/lang/Comparable;Ljava/lang/Comparable;)V

    invoke-virtual {v1, p1, v2}, Landroid/hardware/camera2/CaptureRequest$Builder;->set(Landroid/hardware/camera2/CaptureRequest$Key;Ljava/lang/Object;)V

    .line 426
    :cond_0
    sget p1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1e

    if-lt p1, v2, :cond_1

    iget p1, p0, Lcom/android/helper/video/CameraCapture;->cameraZoom:F

    const/4 v2, 0x0

    cmpl-float p1, p1, v2

    if-lez p1, :cond_1

    .line 428
    :try_start_0
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Landroid/hardware/camera2/CaptureRequest$Key;

    move-result-object p1

    iget v2, p0, Lcom/android/helper/video/CameraCapture;->cameraZoom:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    invoke-virtual {v1, p1, v2}, Landroid/hardware/camera2/CaptureRequest$Builder;->set(Landroid/hardware/camera2/CaptureRequest$Key;Ljava/lang/Object;)V

    .line 429
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v0, p0, Lcom/android/helper/video/CameraCapture;->cameraZoom:F

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(F)Ljava/lang/StringBuilder;

    const-string v0, "x"

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception p1

    .line 431
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v2, "Failed to set CONTROL_ZOOM_RATIO: "

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 435
    :cond_1
    :goto_0
    invoke-virtual {v1}, Landroid/hardware/camera2/CaptureRequest$Builder;->build()Landroid/hardware/camera2/CaptureRequest;

    move-result-object p1

    return-object p1
.end method

.method private createCaptureSession(Landroid/hardware/camera2/CameraDevice;Landroid/view/Surface;)Landroid/hardware/camera2/CameraCaptureSession;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/hardware/camera2/CameraAccessException;,
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 392
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Ljava/util/concurrent/CompletableFuture;

    move-result-object v0

    .line 393
    invoke-static {p2}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/view/Surface;)Landroid/hardware/camera2/params/OutputConfiguration;

    move-result-object p2

    const/4 v1, 0x1

    .line 394
    new-array v1, v1, [Landroid/hardware/camera2/params/OutputConfiguration;

    const/4 v2, 0x0

    aput-object p2, v1, v2

    invoke-static {v1}, Ljava/util/Arrays;->asList([Ljava/lang/Object;)Ljava/util/List;

    move-result-object p2

    .line 396
    iget-boolean v1, p0, Lcom/android/helper/video/CameraCapture;->highSpeed:Z

    .line 397
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()V

    iget-object v2, p0, Lcom/android/helper/video/CameraCapture;->cameraExecutor:Ljava/util/concurrent/Executor;

    new-instance v3, Lcom/android/helper/video/CameraCapture$2;

    invoke-direct {v3, p0, v0}, Lcom/android/helper/video/CameraCapture$2;-><init>(Lcom/android/helper/video/CameraCapture;Ljava/util/concurrent/CompletableFuture;)V

    invoke-static {v1, p2, v2, v3}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(ILjava/util/List;Ljava/util/concurrent/Executor;Landroid/hardware/camera2/CameraCaptureSession$StateCallback;)Landroid/hardware/camera2/params/SessionConfiguration;

    move-result-object p2

    .line 409
    invoke-static {p1, p2}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/hardware/camera2/CameraDevice;Landroid/hardware/camera2/params/SessionConfiguration;)V

    .line 412
    :try_start_0
    invoke-static {v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/concurrent/CompletableFuture;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/hardware/camera2/CameraCaptureSession;
    :try_end_0
    .catch Ljava/util/concurrent/ExecutionException; {:try_start_0 .. :try_end_0} :catch_0

    return-object p1

    :catch_0
    move-exception p1

    .line 414
    invoke-virtual {p1}, Ljava/util/concurrent/ExecutionException;->getCause()Ljava/lang/Throwable;

    move-result-object p1

    check-cast p1, Landroid/hardware/camera2/CameraAccessException;

    throw p1
.end method

.method static synthetic lambda$selectSize$0(ILandroid/util/Size;)Z
    .locals 1

    .line 225
    invoke-virtual {p1}, Landroid/util/Size;->getWidth()I

    move-result v0

    if-gt v0, p0, :cond_0

    invoke-virtual {p1}, Landroid/util/Size;->getHeight()I

    move-result p1

    if-gt p1, p0, :cond_0

    const/4 p0, 0x1

    return p0

    :cond_0
    const/4 p0, 0x0

    return p0
.end method

.method static synthetic lambda$selectSize$1(Ljava/lang/Float;Landroid/util/Size;)Z
    .locals 1

    .line 231
    invoke-virtual {p1}, Landroid/util/Size;->getWidth()I

    move-result v0

    int-to-float v0, v0

    invoke-virtual {p1}, Landroid/util/Size;->getHeight()I

    move-result p1

    int-to-float p1, p1

    div-float/2addr v0, p1

    .line 232
    invoke-virtual {p0}, Ljava/lang/Float;->floatValue()F

    move-result p0

    div-float/2addr v0, p0

    const p0, 0x3f666666    # 0.9f

    cmpl-float p0, v0, p0

    if-ltz p0, :cond_0

    const p0, 0x3f8ccccd    # 1.1f

    cmpg-float p0, v0, p0

    if-gtz p0, :cond_0

    const/4 p0, 0x1

    return p0

    :cond_0
    const/4 p0, 0x0

    return p0
.end method

.method static synthetic lambda$selectSize$2(Ljava/lang/Float;Landroid/util/Size;Landroid/util/Size;)I
    .locals 4

    .line 240
    invoke-virtual {p1}, Landroid/util/Size;->getWidth()I

    move-result v0

    invoke-virtual {p2}, Landroid/util/Size;->getWidth()I

    move-result v1

    invoke-static {v0, v1}, Ljava/lang/Integer;->compare(II)I

    move-result v0

    if-eqz v0, :cond_0

    return v0

    :cond_0
    if-eqz p0, :cond_1

    .line 247
    invoke-virtual {p1}, Landroid/util/Size;->getWidth()I

    move-result v0

    int-to-float v0, v0

    invoke-virtual {p1}, Landroid/util/Size;->getHeight()I

    move-result v1

    int-to-float v1, v1

    div-float/2addr v0, v1

    .line 248
    invoke-virtual {p0}, Ljava/lang/Float;->floatValue()F

    move-result v1

    div-float/2addr v0, v1

    const/high16 v1, 0x3f800000    # 1.0f

    sub-float v0, v1, v0

    .line 249
    invoke-static {v0}, Ljava/lang/Math;->abs(F)F

    move-result v0

    .line 251
    invoke-virtual {p2}, Landroid/util/Size;->getWidth()I

    move-result v2

    int-to-float v2, v2

    invoke-virtual {p2}, Landroid/util/Size;->getHeight()I

    move-result v3

    int-to-float v3, v3

    div-float/2addr v2, v3

    .line 252
    invoke-virtual {p0}, Ljava/lang/Float;->floatValue()F

    move-result p0

    div-float/2addr v2, p0

    sub-float/2addr v1, v2

    .line 253
    invoke-static {v1}, Ljava/lang/Math;->abs(F)F

    move-result p0

    .line 256
    invoke-static {p0, v0}, Ljava/lang/Float;->compare(FF)I

    move-result p0

    if-eqz p0, :cond_1

    return p0

    .line 263
    :cond_1
    invoke-virtual {p1}, Landroid/util/Size;->getHeight()I

    move-result p0

    invoke-virtual {p2}, Landroid/util/Size;->getHeight()I

    move-result p1

    invoke-static {p0, p1}, Ljava/lang/Integer;->compare(II)I

    move-result p0

    return p0
.end method

.method private openCamera(Ljava/lang/String;)Landroid/hardware/camera2/CameraDevice;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/hardware/camera2/CameraAccessException;,
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 345
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Ljava/util/concurrent/CompletableFuture;

    move-result-object v0

    .line 346
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getCameraManager()Landroid/hardware/camera2/CameraManager;

    move-result-object v1

    new-instance v2, Lcom/android/helper/video/CameraCapture$1;

    invoke-direct {v2, p0, v0}, Lcom/android/helper/video/CameraCapture$1;-><init>(Lcom/android/helper/video/CameraCapture;Ljava/util/concurrent/CompletableFuture;)V

    iget-object v3, p0, Lcom/android/helper/video/CameraCapture;->cameraHandler:Landroid/os/Handler;

    invoke-virtual {v1, p1, v2, v3}, Landroid/hardware/camera2/CameraManager;->openCamera(Ljava/lang/String;Landroid/hardware/camera2/CameraDevice$StateCallback;Landroid/os/Handler;)V

    .line 384
    :try_start_0
    invoke-static {v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/concurrent/CompletableFuture;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/hardware/camera2/CameraDevice;
    :try_end_0
    .catch Ljava/util/concurrent/ExecutionException; {:try_start_0 .. :try_end_0} :catch_0

    return-object p1

    :catch_0
    move-exception p1

    .line 386
    invoke-virtual {p1}, Ljava/util/concurrent/ExecutionException;->getCause()Ljava/lang/Throwable;

    move-result-object p1

    check-cast p1, Landroid/hardware/camera2/CameraAccessException;

    throw p1
.end method

.method private static resolveAspectRatio(Lcom/android/helper/video/CameraAspectRatio;Landroid/hardware/camera2/CameraCharacteristics;)Ljava/lang/Float;
    .locals 1

    if-nez p0, :cond_0

    const/4 p0, 0x0

    return-object p0

    .line 280
    :cond_0
    invoke-virtual {p0}, Lcom/android/helper/video/CameraAspectRatio;->isSensor()Z

    move-result v0

    if-eqz v0, :cond_1

    .line 281
    sget-object p0, Landroid/hardware/camera2/CameraCharacteristics;->SENSOR_INFO_ACTIVE_ARRAY_SIZE:Landroid/hardware/camera2/CameraCharacteristics$Key;

    invoke-virtual {p1, p0}, Landroid/hardware/camera2/CameraCharacteristics;->get(Landroid/hardware/camera2/CameraCharacteristics$Key;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Landroid/graphics/Rect;

    .line 282
    invoke-virtual {p0}, Landroid/graphics/Rect;->width()I

    move-result p1

    int-to-float p1, p1

    invoke-virtual {p0}, Landroid/graphics/Rect;->height()I

    move-result p0

    int-to-float p0, p0

    div-float/2addr p1, p0

    invoke-static {p1}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object p0

    return-object p0

    .line 285
    :cond_1
    invoke-virtual {p0}, Lcom/android/helper/video/CameraAspectRatio;->getAspectRatio()F

    move-result p0

    invoke-static {p0}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object p0

    return-object p0
.end method

.method private static selectCamera(Ljava/lang/String;Lcom/android/helper/video/CameraFacing;)Ljava/lang/String;
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/hardware/camera2/CameraAccessException;,
            Lcom/android/helper/device/ConfigurationException;
        }
    .end annotation

    .line 166
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getCameraManager()Landroid/hardware/camera2/CameraManager;

    move-result-object v0

    .line 168
    invoke-virtual {v0}, Landroid/hardware/camera2/CameraManager;->getCameraIdList()[Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    if-eqz p0, :cond_3

    .line 170
    invoke-static {v1}, Ljava/util/Arrays;->asList([Ljava/lang/Object;)Ljava/util/List;

    move-result-object p1

    invoke-interface {p1, p0}, Ljava/util/List;->contains(Ljava/lang/Object;)Z

    move-result p1

    if-nez p1, :cond_2

    .line 172
    array-length p1, v1

    const/4 v3, 0x0

    :goto_0
    if-ge v3, p1, :cond_1

    aget-object v4, v1, v3

    .line 174
    :try_start_0
    invoke-virtual {v0, v4}, Landroid/hardware/camera2/CameraManager;->getCameraCharacteristics(Ljava/lang/String;)Landroid/hardware/camera2/CameraCharacteristics;

    move-result-object v5

    .line 175
    invoke-static {v5}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/hardware/camera2/CameraCharacteristics;)Ljava/util/Set;

    move-result-object v5

    if-eqz v5, :cond_0

    .line 176
    invoke-interface {v5, p0}, Ljava/util/Set;->contains(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_0

    .line 177
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "Explicit camera ID "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v6, " is a physical sub-camera of logical "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v6, ", using parent logical camera"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-object v4

    :catch_0
    :cond_0
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    .line 183
    :cond_1
    new-instance p1, Ljava/lang/StringBuilder;

    const-string v0, "Camera with id "

    invoke-direct {p1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " not found\n"

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {v2}, Lcom/android/helper/util/LogUtils;->buildCameraListMessage(Z)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 184
    new-instance p0, Lcom/android/helper/device/ConfigurationException;

    const-string p1, "Camera id not found"

    invoke-direct {p0, p1}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw p0

    :cond_2
    return-object p0

    :cond_3
    const/4 p0, 0x0

    if-nez p1, :cond_5

    .line 191
    array-length p1, v1

    if-lez p1, :cond_4

    aget-object p0, v1, v2

    :cond_4
    return-object p0

    .line 194
    :cond_5
    array-length v3, v1

    :goto_1
    if-ge v2, v3, :cond_7

    aget-object v4, v1, v2

    .line 195
    invoke-virtual {v0, v4}, Landroid/hardware/camera2/CameraManager;->getCameraCharacteristics(Ljava/lang/String;)Landroid/hardware/camera2/CameraCharacteristics;

    move-result-object v5

    .line 197
    sget-object v6, Landroid/hardware/camera2/CameraCharacteristics;->LENS_FACING:Landroid/hardware/camera2/CameraCharacteristics$Key;

    invoke-virtual {v5, v6}, Landroid/hardware/camera2/CameraCharacteristics;->get(Landroid/hardware/camera2/CameraCharacteristics$Key;)Ljava/lang/Object;

    move-result-object v5

    check-cast v5, Ljava/lang/Integer;

    invoke-virtual {v5}, Ljava/lang/Integer;->intValue()I

    move-result v5

    .line 198
    invoke-virtual {p1}, Lcom/android/helper/video/CameraFacing;->value()I

    move-result v6

    if-ne v6, v5, :cond_6

    return-object v4

    :cond_6
    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_7
    return-object p0
.end method

.method private static selectSize(Ljava/lang/String;Lcom/android/helper/device/Size;ILcom/android/helper/video/CameraAspectRatio;Z)Lcom/android/helper/device/Size;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/hardware/camera2/CameraAccessException;
        }
    .end annotation

    if-eqz p1, :cond_0

    return-object p1

    .line 214
    :cond_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getCameraManager()Landroid/hardware/camera2/CameraManager;

    move-result-object p1

    .line 215
    invoke-virtual {p1, p0}, Landroid/hardware/camera2/CameraManager;->getCameraCharacteristics(Ljava/lang/String;)Landroid/hardware/camera2/CameraCharacteristics;

    move-result-object p0

    .line 217
    sget-object p1, Landroid/hardware/camera2/CameraCharacteristics;->SCALER_STREAM_CONFIGURATION_MAP:Landroid/hardware/camera2/CameraCharacteristics$Key;

    invoke-virtual {p0, p1}, Landroid/hardware/camera2/CameraCharacteristics;->get(Landroid/hardware/camera2/CameraCharacteristics$Key;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/hardware/camera2/params/StreamConfigurationMap;

    if-eqz p4, :cond_1

    .line 218
    invoke-virtual {p1}, Landroid/hardware/camera2/params/StreamConfigurationMap;->getHighSpeedVideoSizes()[Landroid/util/Size;

    move-result-object p1

    goto :goto_0

    :cond_1
    const-class p4, Landroid/media/MediaCodec;

    invoke-virtual {p1, p4}, Landroid/hardware/camera2/params/StreamConfigurationMap;->getOutputSizes(Ljava/lang/Class;)[Landroid/util/Size;

    move-result-object p1

    :goto_0
    const/4 p4, 0x0

    if-nez p1, :cond_2

    return-object p4

    .line 223
    :cond_2
    invoke-static {p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m([Ljava/lang/Object;)Ljava/util/stream/Stream;

    move-result-object p1

    if-lez p2, :cond_3

    .line 225
    new-instance v0, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda16;

    invoke-direct {v0, p2}, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda16;-><init>(I)V

    invoke-static {p1, v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/stream/Stream;Ljava/util/function/Predicate;)Ljava/util/stream/Stream;

    move-result-object p1

    .line 228
    :cond_3
    invoke-static {p3, p0}, Lcom/android/helper/video/CameraCapture;->resolveAspectRatio(Lcom/android/helper/video/CameraAspectRatio;Landroid/hardware/camera2/CameraCharacteristics;)Ljava/lang/Float;

    move-result-object p0

    if-eqz p0, :cond_4

    .line 230
    new-instance p2, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda17;

    invoke-direct {p2, p0}, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda17;-><init>(Ljava/lang/Float;)V

    invoke-static {p1, p2}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/stream/Stream;Ljava/util/function/Predicate;)Ljava/util/stream/Stream;

    move-result-object p1

    .line 238
    :cond_4
    new-instance p2, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda18;

    invoke-direct {p2, p0}, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda18;-><init>(Ljava/lang/Float;)V

    invoke-static {p1, p2}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/stream/Stream;Ljava/util/Comparator;)Ljava/util/Optional;

    move-result-object p0

    .line 266
    invoke-static {p0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/Optional;)Z

    move-result p1

    if-eqz p1, :cond_5

    .line 267
    invoke-static {p0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/util/Optional;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Landroid/util/Size;

    .line 268
    new-instance p1, Lcom/android/helper/device/Size;

    invoke-virtual {p0}, Landroid/util/Size;->getWidth()I

    move-result p2

    invoke-virtual {p0}, Landroid/util/Size;->getHeight()I

    move-result p0

    invoke-direct {p1, p2, p0}, Lcom/android/helper/device/Size;-><init>(II)V

    return-object p1

    :cond_5
    return-object p4
.end method

.method private setRepeatingRequest(Landroid/hardware/camera2/CameraCaptureSession;Landroid/hardware/camera2/CaptureRequest;)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/hardware/camera2/CameraAccessException;,
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 440
    new-instance v0, Lcom/android/helper/video/CameraCapture$3;

    invoke-direct {v0, p0}, Lcom/android/helper/video/CameraCapture$3;-><init>(Lcom/android/helper/video/CameraCapture;)V

    .line 452
    iget-boolean v1, p0, Lcom/android/helper/video/CameraCapture;->highSpeed:Z

    if-eqz v1, :cond_0

    .line 453
    invoke-static {p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Ljava/lang/Object;)Landroid/hardware/camera2/CameraConstrainedHighSpeedCaptureSession;

    move-result-object p1

    .line 454
    invoke-static {p1, p2}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/hardware/camera2/CameraConstrainedHighSpeedCaptureSession;Landroid/hardware/camera2/CaptureRequest;)Ljava/util/List;

    move-result-object p2

    .line 455
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraHandler:Landroid/os/Handler;

    invoke-static {p1, p2, v0, v1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/hardware/camera2/CameraConstrainedHighSpeedCaptureSession;Ljava/util/List;Landroid/hardware/camera2/CameraCaptureSession$CaptureCallback;Landroid/os/Handler;)I

    return-void

    .line 457
    :cond_0
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraHandler:Landroid/os/Handler;

    invoke-virtual {p1, p2, v0, v1}, Landroid/hardware/camera2/CameraCaptureSession;->setRepeatingRequest(Landroid/hardware/camera2/CaptureRequest;Landroid/hardware/camera2/CameraCaptureSession$CaptureCallback;Landroid/os/Handler;)I

    return-void
.end method


# virtual methods
.method public getSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 329
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->videoSize:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method protected init()V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/device/ConfigurationException;,
            Ljava/io/IOException;
        }
    .end annotation

    const-string v0, "Using camera \'"

    .line 101
    new-instance v1, Landroid/os/HandlerThread;

    const-string v2, "camera"

    invoke-direct {v1, v2}, Landroid/os/HandlerThread;-><init>(Ljava/lang/String;)V

    iput-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraThread:Landroid/os/HandlerThread;

    .line 102
    invoke-virtual {v1}, Landroid/os/HandlerThread;->start()V

    .line 103
    new-instance v1, Landroid/os/Handler;

    iget-object v2, p0, Lcom/android/helper/video/CameraCapture;->cameraThread:Landroid/os/HandlerThread;

    invoke-virtual {v2}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object v2

    invoke-direct {v1, v2}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    iput-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraHandler:Landroid/os/Handler;

    .line 104
    new-instance v1, Lcom/android/helper/util/HandlerExecutor;

    iget-object v2, p0, Lcom/android/helper/video/CameraCapture;->cameraHandler:Landroid/os/Handler;

    invoke-direct {v1, v2}, Lcom/android/helper/util/HandlerExecutor;-><init>(Landroid/os/Handler;)V

    iput-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraExecutor:Ljava/util/concurrent/Executor;

    .line 107
    :try_start_0
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->explicitCameraId:Ljava/lang/String;

    iget-object v2, p0, Lcom/android/helper/video/CameraCapture;->cameraFacing:Lcom/android/helper/video/CameraFacing;

    invoke-static {v1, v2}, Lcom/android/helper/video/CameraCapture;->selectCamera(Ljava/lang/String;Lcom/android/helper/video/CameraFacing;)Ljava/lang/String;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/video/CameraCapture;->cameraId:Ljava/lang/String;

    if-eqz v1, :cond_0

    .line 112
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraId:Ljava/lang/String;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v0, "\'"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 113
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraId:Ljava/lang/String;

    invoke-direct {p0, v0}, Lcom/android/helper/video/CameraCapture;->openCamera(Ljava/lang/String;)Landroid/hardware/camera2/CameraDevice;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraDevice:Landroid/hardware/camera2/CameraDevice;

    return-void

    .line 109
    :cond_0
    new-instance v0, Lcom/android/helper/device/ConfigurationException;

    const-string v1, "No matching camera found"

    invoke-direct {v0, v1}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_0
    .catch Landroid/hardware/camera2/CameraAccessException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0
    move-exception v0

    goto :goto_0

    :catch_1
    move-exception v0

    .line 115
    :goto_0
    new-instance v1, Ljava/io/IOException;

    invoke-direct {v1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/Throwable;)V

    throw v1
.end method

.method public isClosed()Z
    .locals 1

    .line 463
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->disconnected:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v0

    return v0
.end method

.method public prepare()V
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 122
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraId:Ljava/lang/String;

    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->explicitSize:Lcom/android/helper/device/Size;

    iget v2, p0, Lcom/android/helper/video/CameraCapture;->maxSize:I

    iget-object v3, p0, Lcom/android/helper/video/CameraCapture;->aspectRatio:Lcom/android/helper/video/CameraAspectRatio;

    iget-boolean v4, p0, Lcom/android/helper/video/CameraCapture;->highSpeed:Z

    invoke-static {v0, v1, v2, v3, v4}, Lcom/android/helper/video/CameraCapture;->selectSize(Ljava/lang/String;Lcom/android/helper/device/Size;ILcom/android/helper/video/CameraAspectRatio;Z)Lcom/android/helper/device/Size;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->captureSize:Lcom/android/helper/device/Size;
    :try_end_0
    .catch Landroid/hardware/camera2/CameraAccessException; {:try_start_0 .. :try_end_0} :catch_1

    if-eqz v0, :cond_5

    .line 130
    new-instance v0, Lcom/android/helper/video/VideoFilter;

    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->captureSize:Lcom/android/helper/device/Size;

    invoke-direct {v0, v1}, Lcom/android/helper/video/VideoFilter;-><init>(Lcom/android/helper/device/Size;)V

    .line 132
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->crop:Landroid/graphics/Rect;

    if-eqz v1, :cond_0

    const/4 v2, 0x0

    .line 133
    invoke-virtual {v0, v1, v2}, Lcom/android/helper/video/VideoFilter;->addCrop(Landroid/graphics/Rect;Z)V

    .line 136
    :cond_0
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    sget-object v2, Lcom/android/helper/device/Orientation;->Orient0:Lcom/android/helper/device/Orientation;

    if-eq v1, v2, :cond_1

    .line 137
    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    invoke-virtual {v0, v1}, Lcom/android/helper/video/VideoFilter;->addOrientation(Lcom/android/helper/device/Orientation;)V

    goto :goto_0

    .line 141
    :cond_1
    :try_start_1
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getCameraManager()Landroid/hardware/camera2/CameraManager;

    move-result-object v1

    .line 142
    iget-object v2, p0, Lcom/android/helper/video/CameraCapture;->cameraId:Ljava/lang/String;

    invoke-virtual {v1, v2}, Landroid/hardware/camera2/CameraManager;->getCameraCharacteristics(Ljava/lang/String;)Landroid/hardware/camera2/CameraCharacteristics;

    move-result-object v1

    .line 143
    sget-object v2, Landroid/hardware/camera2/CameraCharacteristics;->SENSOR_ORIENTATION:Landroid/hardware/camera2/CameraCharacteristics$Key;

    invoke-virtual {v1, v2}, Landroid/hardware/camera2/CameraCharacteristics;->get(Landroid/hardware/camera2/CameraCharacteristics$Key;)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Ljava/lang/Integer;

    .line 144
    sget-object v3, Landroid/hardware/camera2/CameraCharacteristics;->LENS_FACING:Landroid/hardware/camera2/CameraCharacteristics$Key;

    invoke-virtual {v1, v3}, Landroid/hardware/camera2/CameraCharacteristics;->get(Landroid/hardware/camera2/CameraCharacteristics$Key;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/lang/Integer;

    if-eqz v2, :cond_4

    .line 146
    invoke-virtual {v2}, Ljava/lang/Integer;->intValue()I

    move-result v1

    const/16 v3, 0x5a

    if-ne v1, v3, :cond_2

    .line 147
    sget-object v1, Lcom/android/helper/device/Orientation;->Orient90:Lcom/android/helper/device/Orientation;

    invoke-virtual {v0, v1}, Lcom/android/helper/video/VideoFilter;->addOrientation(Lcom/android/helper/device/Orientation;)V

    goto :goto_0

    .line 148
    :cond_2
    invoke-virtual {v2}, Ljava/lang/Integer;->intValue()I

    move-result v1

    const/16 v3, 0x10e

    if-ne v1, v3, :cond_3

    .line 149
    sget-object v1, Lcom/android/helper/device/Orientation;->Orient270:Lcom/android/helper/device/Orientation;

    invoke-virtual {v0, v1}, Lcom/android/helper/video/VideoFilter;->addOrientation(Lcom/android/helper/device/Orientation;)V

    goto :goto_0

    .line 150
    :cond_3
    invoke-virtual {v2}, Ljava/lang/Integer;->intValue()I

    move-result v1

    const/16 v2, 0xb4

    if-ne v1, v2, :cond_4

    .line 151
    sget-object v1, Lcom/android/helper/device/Orientation;->Orient180:Lcom/android/helper/device/Orientation;

    invoke-virtual {v0, v1}, Lcom/android/helper/video/VideoFilter;->addOrientation(Lcom/android/helper/device/Orientation;)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto :goto_0

    :catch_0
    move-exception v1

    .line 155
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Could not apply auto sensor orientation: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 159
    :cond_4
    :goto_0
    iget v1, p0, Lcom/android/helper/video/CameraCapture;->angle:F

    float-to-double v1, v1

    invoke-virtual {v0, v1, v2}, Lcom/android/helper/video/VideoFilter;->addAngle(D)V

    .line 161
    invoke-virtual {v0}, Lcom/android/helper/video/VideoFilter;->getInverseTransform()Lcom/android/helper/util/AffineMatrix;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/video/CameraCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    .line 162
    invoke-virtual {v0}, Lcom/android/helper/video/VideoFilter;->getOutputSize()Lcom/android/helper/device/Size;

    move-result-object v0

    iget v1, p0, Lcom/android/helper/video/CameraCapture;->maxSize:I

    invoke-virtual {v0, v1}, Lcom/android/helper/device/Size;->limit(I)Lcom/android/helper/device/Size;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/device/Size;->round8()Lcom/android/helper/device/Size;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->videoSize:Lcom/android/helper/device/Size;

    return-void

    .line 124
    :cond_5
    :try_start_2
    new-instance v0, Ljava/io/IOException;

    const-string v1, "Could not select camera size"

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_2
    .catch Landroid/hardware/camera2/CameraAccessException; {:try_start_2 .. :try_end_2} :catch_1

    :catch_1
    move-exception v0

    .line 127
    new-instance v1, Ljava/io/IOException;

    invoke-direct {v1, v0}, Ljava/io/IOException;-><init>(Ljava/lang/Throwable;)V

    throw v1
.end method

.method public release()V
    .locals 1

    .line 319
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraDevice:Landroid/hardware/camera2/CameraDevice;

    if-eqz v0, :cond_0

    .line 320
    invoke-virtual {v0}, Landroid/hardware/camera2/CameraDevice;->close()V

    .line 322
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraThread:Landroid/os/HandlerThread;

    if-eqz v0, :cond_1

    .line 323
    invoke-virtual {v0}, Landroid/os/HandlerThread;->quitSafely()Z

    :cond_1
    return-void
.end method

.method public requestInvalidate()V
    .locals 0

    return-void
.end method

.method public setMaxSize(I)Z
    .locals 1

    .line 334
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->explicitSize:Lcom/android/helper/device/Size;

    if-eqz v0, :cond_0

    const/4 p1, 0x0

    return p1

    .line 338
    :cond_0
    iput p1, p0, Lcom/android/helper/video/CameraCapture;->maxSize:I

    const/4 p1, 0x1

    return p1
.end method

.method public start(Landroid/view/Surface;)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 290
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    if-eqz v0, :cond_0

    .line 292
    new-instance v0, Lcom/android/helper/opengl/AffineOpenGLFilter;

    iget-object v1, p0, Lcom/android/helper/video/CameraCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-direct {v0, v1}, Lcom/android/helper/opengl/AffineOpenGLFilter;-><init>(Lcom/android/helper/util/AffineMatrix;)V

    .line 295
    new-instance v1, Lcom/android/helper/opengl/OpenGLRunner;

    sget-object v2, Lcom/android/helper/video/CameraCapture;->VFLIP_MATRIX:[F

    invoke-direct {v1, v0, v2}, Lcom/android/helper/opengl/OpenGLRunner;-><init>(Lcom/android/helper/opengl/OpenGLFilter;[F)V

    iput-object v1, p0, Lcom/android/helper/video/CameraCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    .line 296
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->captureSize:Lcom/android/helper/device/Size;

    iget-object v2, p0, Lcom/android/helper/video/CameraCapture;->videoSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1, v0, v2, p1}, Lcom/android/helper/opengl/OpenGLRunner;->start(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)Landroid/view/Surface;

    move-result-object p1

    .line 300
    :cond_0
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->cameraDevice:Landroid/hardware/camera2/CameraDevice;

    invoke-direct {p0, v0, p1}, Lcom/android/helper/video/CameraCapture;->createCaptureSession(Landroid/hardware/camera2/CameraDevice;Landroid/view/Surface;)Landroid/hardware/camera2/CameraCaptureSession;

    move-result-object v0

    .line 301
    invoke-direct {p0, p1}, Lcom/android/helper/video/CameraCapture;->createCaptureRequest(Landroid/view/Surface;)Landroid/hardware/camera2/CaptureRequest;

    move-result-object p1

    .line 302
    invoke-direct {p0, v0, p1}, Lcom/android/helper/video/CameraCapture;->setRepeatingRequest(Landroid/hardware/camera2/CameraCaptureSession;Landroid/hardware/camera2/CaptureRequest;)V
    :try_end_0
    .catch Landroid/hardware/camera2/CameraAccessException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    goto :goto_0

    :catch_1
    move-exception p1

    .line 304
    :goto_0
    invoke-virtual {p0}, Lcom/android/helper/video/CameraCapture;->stop()V

    .line 305
    new-instance v0, Ljava/io/IOException;

    invoke-direct {v0, p1}, Ljava/io/IOException;-><init>(Ljava/lang/Throwable;)V

    throw v0
.end method

.method public stop()V
    .locals 1

    .line 311
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    if-eqz v0, :cond_0

    .line 312
    invoke-virtual {v0}, Lcom/android/helper/opengl/OpenGLRunner;->stopAndRelease()V

    const/4 v0, 0x0

    .line 313
    iput-object v0, p0, Lcom/android/helper/video/CameraCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    :cond_0
    return-void
.end method
