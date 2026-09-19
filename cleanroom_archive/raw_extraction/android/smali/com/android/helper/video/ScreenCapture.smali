.class public Lcom/android/helper/video/ScreenCapture;
.super Lcom/android/helper/video/SurfaceCapture;
.source "ScreenCapture.java"


# static fields
.field static final synthetic $assertionsDisabled:Z


# instance fields
.field private final angle:F

.field private captureOrientation:Lcom/android/helper/device/Orientation;

.field private captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

.field private final crop:Landroid/graphics/Rect;

.field private display:Landroid/os/IBinder;

.field private final displayId:I

.field private displayInfo:Lcom/android/helper/device/DisplayInfo;

.field private final displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

.field private glRunner:Lcom/android/helper/opengl/OpenGLRunner;

.field private maxSize:I

.field private transform:Lcom/android/helper/util/AffineMatrix;

.field private final vdListener:Lcom/android/helper/video/VirtualDisplayListener;

.field private videoSize:Lcom/android/helper/device/Size;

.field private virtualDisplay:Landroid/hardware/display/VirtualDisplay;


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/video/VirtualDisplayListener;Lcom/android/helper/Options;)V
    .locals 1

    .line 49
    invoke-direct {p0}, Lcom/android/helper/video/SurfaceCapture;-><init>()V

    .line 41
    new-instance v0, Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-direct {v0}, Lcom/android/helper/video/DisplaySizeMonitor;-><init>()V

    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    .line 50
    iput-object p1, p0, Lcom/android/helper/video/ScreenCapture;->vdListener:Lcom/android/helper/video/VirtualDisplayListener;

    .line 51
    invoke-virtual {p2}, Lcom/android/helper/Options;->getDisplayId()I

    move-result p1

    iput p1, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    .line 53
    invoke-virtual {p2}, Lcom/android/helper/Options;->getMaxSize()I

    move-result p1

    iput p1, p0, Lcom/android/helper/video/ScreenCapture;->maxSize:I

    .line 54
    invoke-virtual {p2}, Lcom/android/helper/Options;->getCrop()Landroid/graphics/Rect;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/ScreenCapture;->crop:Landroid/graphics/Rect;

    .line 55
    invoke-virtual {p2}, Lcom/android/helper/Options;->getCaptureOrientationLock()Lcom/android/helper/device/Orientation$Lock;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    .line 56
    invoke-virtual {p2}, Lcom/android/helper/Options;->getCaptureOrientation()Lcom/android/helper/device/Orientation;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    .line 59
    invoke-virtual {p2}, Lcom/android/helper/Options;->getAngle()F

    move-result p1

    iput p1, p0, Lcom/android/helper/video/ScreenCapture;->angle:F

    return-void
.end method

.method private static createDisplay()Landroid/os/IBinder;
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 199
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1e

    if-lt v0, v1, :cond_1

    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    if-ne v0, v1, :cond_0

    const-string v0, "S"

    sget-object v1, Landroid/os/Build$VERSION;->CODENAME:Ljava/lang/String;

    .line 200
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v0, 0x0

    goto :goto_1

    :cond_1
    :goto_0
    const/4 v0, 0x1

    .line 201
    :goto_1
    const-string v1, "monitor"

    invoke-static {v1, v0}, Lcom/android/helper/wrappers/SurfaceControl;->createDisplay(Ljava/lang/String;Z)Landroid/os/IBinder;

    move-result-object v0

    return-object v0
.end method

.method private static setDisplaySurface(Landroid/os/IBinder;Landroid/view/Surface;Landroid/graphics/Rect;Landroid/graphics/Rect;I)V
    .locals 0

    .line 205
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->openTransaction()V

    .line 207
    :try_start_0
    invoke-static {p0, p1}, Lcom/android/helper/wrappers/SurfaceControl;->setDisplaySurface(Landroid/os/IBinder;Landroid/view/Surface;)V

    const/4 p1, 0x0

    .line 208
    invoke-static {p0, p1, p2, p3}, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayProjection(Landroid/os/IBinder;ILandroid/graphics/Rect;Landroid/graphics/Rect;)V

    .line 209
    invoke-static {p0, p4}, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayLayerStack(Landroid/os/IBinder;I)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 211
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->closeTransaction()V

    return-void

    :catchall_0
    move-exception p0

    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->closeTransaction()V

    .line 212
    throw p0
.end method


# virtual methods
.method public getSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 187
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->videoSize:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public init()V
    .locals 3

    .line 64
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    iget v1, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    new-instance v2, Lcom/android/helper/video/ScreenCapture$$ExternalSyntheticLambda0;

    invoke-direct {v2, p0}, Lcom/android/helper/video/ScreenCapture$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/video/ScreenCapture;)V

    invoke-virtual {v0, v1, v2}, Lcom/android/helper/video/DisplaySizeMonitor;->start(ILcom/android/helper/video/DisplaySizeMonitor$Listener;)V

    return-void
.end method

.method public prepare()V
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/device/ConfigurationException;
        }
    .end annotation

    .line 69
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    iget v1, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/DisplayManager;->getDisplayInfo(I)Lcom/android/helper/device/DisplayInfo;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    if-eqz v0, :cond_5

    .line 75
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getFlags()I

    move-result v0

    const/4 v1, 0x1

    and-int/2addr v0, v1

    if-nez v0, :cond_0

    .line 76
    const-string v0, "Display doesn\'t have FLAG_SUPPORTS_PROTECTED_BUFFERS flag, mirroring can be restricted"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 79
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object v0

    .line 80
    iget-object v2, p0, Lcom/android/helper/video/ScreenCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-virtual {v2, v0}, Lcom/android/helper/video/DisplaySizeMonitor;->setSessionDisplaySize(Lcom/android/helper/device/Size;)V

    .line 82
    iget-object v2, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    sget-object v3, Lcom/android/helper/device/Orientation$Lock;->LockedInitial:Lcom/android/helper/device/Orientation$Lock;

    if-ne v2, v3, :cond_1

    .line 84
    sget-object v2, Lcom/android/helper/device/Orientation$Lock;->LockedValue:Lcom/android/helper/device/Orientation$Lock;

    iput-object v2, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    .line 85
    iget-object v2, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v2}, Lcom/android/helper/device/DisplayInfo;->getRotation()I

    move-result v2

    invoke-static {v2}, Lcom/android/helper/device/Orientation;->fromRotation(I)Lcom/android/helper/device/Orientation;

    move-result-object v2

    iput-object v2, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    .line 88
    :cond_1
    new-instance v2, Lcom/android/helper/video/VideoFilter;

    invoke-direct {v2, v0}, Lcom/android/helper/video/VideoFilter;-><init>(Lcom/android/helper/device/Size;)V

    .line 90
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->crop:Landroid/graphics/Rect;

    const/4 v3, 0x0

    if-eqz v0, :cond_3

    .line 91
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getRotation()I

    move-result v0

    rem-int/lit8 v0, v0, 0x2

    if-eqz v0, :cond_2

    const/4 v0, 0x1

    goto :goto_0

    :cond_2
    const/4 v0, 0x0

    .line 92
    :goto_0
    iget-object v4, p0, Lcom/android/helper/video/ScreenCapture;->crop:Landroid/graphics/Rect;

    invoke-virtual {v2, v4, v0}, Lcom/android/helper/video/VideoFilter;->addCrop(Landroid/graphics/Rect;Z)V

    .line 95
    :cond_3
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    sget-object v4, Lcom/android/helper/device/Orientation$Lock;->Unlocked:Lcom/android/helper/device/Orientation$Lock;

    if-eq v0, v4, :cond_4

    goto :goto_1

    :cond_4
    const/4 v1, 0x0

    .line 96
    :goto_1
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getRotation()I

    move-result v0

    iget-object v3, p0, Lcom/android/helper/video/ScreenCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    invoke-virtual {v2, v0, v1, v3}, Lcom/android/helper/video/VideoFilter;->addOrientation(IZLcom/android/helper/device/Orientation;)V

    .line 97
    iget v0, p0, Lcom/android/helper/video/ScreenCapture;->angle:F

    float-to-double v0, v0

    invoke-virtual {v2, v0, v1}, Lcom/android/helper/video/VideoFilter;->addAngle(D)V

    .line 99
    invoke-virtual {v2}, Lcom/android/helper/video/VideoFilter;->getInverseTransform()Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    .line 100
    invoke-virtual {v2}, Lcom/android/helper/video/VideoFilter;->getOutputSize()Lcom/android/helper/device/Size;

    move-result-object v0

    iget v1, p0, Lcom/android/helper/video/ScreenCapture;->maxSize:I

    invoke-virtual {v0, v1}, Lcom/android/helper/device/Size;->limit(I)Lcom/android/helper/device/Size;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/device/Size;->round8()Lcom/android/helper/device/Size;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->videoSize:Lcom/android/helper/device/Size;

    return-void

    .line 71
    :cond_5
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Display "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v1, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, " not found\n"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/android/helper/util/LogUtils;->buildDisplayListMessage()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 72
    new-instance v0, Lcom/android/helper/device/ConfigurationException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Unknown display id: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v2, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lcom/android/helper/device/ConfigurationException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method public release()V
    .locals 2

    .line 173
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-virtual {v0}, Lcom/android/helper/video/DisplaySizeMonitor;->stopAndRelease()V

    .line 175
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->display:Landroid/os/IBinder;

    const/4 v1, 0x0

    if-eqz v0, :cond_0

    .line 176
    invoke-static {v0}, Lcom/android/helper/wrappers/SurfaceControl;->destroyDisplay(Landroid/os/IBinder;)V

    .line 177
    iput-object v1, p0, Lcom/android/helper/video/ScreenCapture;->display:Landroid/os/IBinder;

    .line 179
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    if-eqz v0, :cond_1

    .line 180
    invoke-virtual {v0}, Landroid/hardware/display/VirtualDisplay;->release()V

    .line 181
    iput-object v1, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    :cond_1
    return-void
.end method

.method public requestInvalidate()V
    .locals 0

    .line 217
    invoke-virtual {p0}, Lcom/android/helper/video/ScreenCapture;->invalidate()V

    return-void
.end method

.method public setMaxSize(I)Z
    .locals 0

    .line 192
    iput p1, p0, Lcom/android/helper/video/ScreenCapture;->maxSize:I

    const/4 p1, 0x1

    return p1
.end method

.method public start(Landroid/view/Surface;)V
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 105
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->display:Landroid/os/IBinder;

    const/4 v1, 0x0

    if-eqz v0, :cond_0

    .line 106
    invoke-static {v0}, Lcom/android/helper/wrappers/SurfaceControl;->destroyDisplay(Landroid/os/IBinder;)V

    .line 107
    iput-object v1, p0, Lcom/android/helper/video/ScreenCapture;->display:Landroid/os/IBinder;

    .line 109
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    if-eqz v0, :cond_1

    .line 110
    invoke-virtual {v0}, Landroid/hardware/display/VirtualDisplay;->release()V

    .line 111
    iput-object v1, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    .line 115
    :cond_1
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    if-eqz v0, :cond_2

    .line 117
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object v0

    .line 119
    new-instance v1, Lcom/android/helper/opengl/AffineOpenGLFilter;

    iget-object v2, p0, Lcom/android/helper/video/ScreenCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-direct {v1, v2}, Lcom/android/helper/opengl/AffineOpenGLFilter;-><init>(Lcom/android/helper/util/AffineMatrix;)V

    .line 120
    new-instance v2, Lcom/android/helper/opengl/OpenGLRunner;

    invoke-direct {v2, v1}, Lcom/android/helper/opengl/OpenGLRunner;-><init>(Lcom/android/helper/opengl/OpenGLFilter;)V

    iput-object v2, p0, Lcom/android/helper/video/ScreenCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    .line 121
    iget-object v1, p0, Lcom/android/helper/video/ScreenCapture;->videoSize:Lcom/android/helper/device/Size;

    invoke-virtual {v2, v0, v1, p1}, Lcom/android/helper/opengl/OpenGLRunner;->start(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)Landroid/view/Surface;

    move-result-object p1

    goto :goto_0

    .line 124
    :cond_2
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->videoSize:Lcom/android/helper/device/Size;

    :goto_0
    move-object v6, p1

    move-object p1, v0

    .line 128
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v1

    const-string v2, "scrcpy"

    .line 129
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v3

    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v4

    iget v5, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    invoke-virtual/range {v1 .. v6}, Lcom/android/helper/wrappers/DisplayManager;->createVirtualDisplay(Ljava/lang/String;IIILandroid/view/Surface;)Landroid/hardware/display/VirtualDisplay;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    .line 130
    const-string v0, "Display: using DisplayManager API"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_1

    :catch_0
    move-exception v0

    move-object v1, v0

    .line 133
    :try_start_1
    invoke-static {}, Lcom/android/helper/video/ScreenCapture;->createDisplay()Landroid/os/IBinder;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->display:Landroid/os/IBinder;

    .line 135
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object v0

    .line 136
    iget-object v2, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {v2}, Lcom/android/helper/device/DisplayInfo;->getLayerStack()I

    move-result v2

    .line 137
    iget-object v3, p0, Lcom/android/helper/video/ScreenCapture;->display:Landroid/os/IBinder;

    invoke-virtual {v0}, Lcom/android/helper/device/Size;->toRect()Landroid/graphics/Rect;

    move-result-object v0

    invoke-virtual {p1}, Lcom/android/helper/device/Size;->toRect()Landroid/graphics/Rect;

    move-result-object v4

    invoke-static {v3, v6, v0, v4, v2}, Lcom/android/helper/video/ScreenCapture;->setDisplaySurface(Landroid/os/IBinder;Landroid/view/Surface;Landroid/graphics/Rect;Landroid/graphics/Rect;I)V

    .line 138
    const-string v0, "Display: using SurfaceControl API"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_1

    .line 146
    :goto_1
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->vdListener:Lcom/android/helper/video/VirtualDisplayListener;

    if-eqz v0, :cond_5

    .line 149
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    if-eqz v0, :cond_4

    iget v0, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    if-nez v0, :cond_3

    goto :goto_2

    .line 156
    :cond_3
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->videoSize:Lcom/android/helper/device/Size;

    iget-object v1, p0, Lcom/android/helper/video/ScreenCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-static {v0, v1, p1}, Lcom/android/helper/control/PositionMapper;->create(Lcom/android/helper/device/Size;Lcom/android/helper/util/AffineMatrix;Lcom/android/helper/device/Size;)Lcom/android/helper/control/PositionMapper;

    move-result-object p1

    .line 157
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    invoke-virtual {v0}, Landroid/hardware/display/VirtualDisplay;->getDisplay()Landroid/view/Display;

    move-result-object v0

    invoke-virtual {v0}, Landroid/view/Display;->getDisplayId()I

    move-result v0

    goto :goto_3

    .line 151
    :cond_4
    :goto_2
    iget-object p1, p0, Lcom/android/helper/video/ScreenCapture;->displayInfo:Lcom/android/helper/device/DisplayInfo;

    invoke-virtual {p1}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object p1

    .line 152
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->videoSize:Lcom/android/helper/device/Size;

    iget-object v1, p0, Lcom/android/helper/video/ScreenCapture;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-static {v0, v1, p1}, Lcom/android/helper/control/PositionMapper;->create(Lcom/android/helper/device/Size;Lcom/android/helper/util/AffineMatrix;Lcom/android/helper/device/Size;)Lcom/android/helper/control/PositionMapper;

    move-result-object p1

    .line 153
    iget v0, p0, Lcom/android/helper/video/ScreenCapture;->displayId:I

    .line 159
    :goto_3
    iget-object v1, p0, Lcom/android/helper/video/ScreenCapture;->vdListener:Lcom/android/helper/video/VirtualDisplayListener;

    invoke-interface {v1, v0, p1}, Lcom/android/helper/video/VirtualDisplayListener;->onNewVirtualDisplay(ILcom/android/helper/control/PositionMapper;)V

    :cond_5
    return-void

    :catch_1
    move-exception v0

    move-object p1, v0

    .line 140
    const-string v0, "Could not create display using DisplayManager"

    invoke-static {v0, v1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 141
    const-string v0, "Could not create display using SurfaceControl"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 142
    new-instance p1, Ljava/lang/AssertionError;

    const-string v0, "Could not create display"

    invoke-direct {p1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method

.method public stop()V
    .locals 1

    .line 165
    iget-object v0, p0, Lcom/android/helper/video/ScreenCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    if-eqz v0, :cond_0

    .line 166
    invoke-virtual {v0}, Lcom/android/helper/opengl/OpenGLRunner;->stopAndRelease()V

    const/4 v0, 0x0

    .line 167
    iput-object v0, p0, Lcom/android/helper/video/ScreenCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    :cond_0
    return-void
.end method
