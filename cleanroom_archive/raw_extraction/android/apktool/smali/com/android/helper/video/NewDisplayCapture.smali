.class public Lcom/android/helper/video/NewDisplayCapture;
.super Lcom/android/helper/video/SurfaceCapture;
.source "NewDisplayCapture.java"


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field private static final VIRTUAL_DISPLAY_FLAG_ALWAYS_UNLOCKED:I = 0x1000

.field private static final VIRTUAL_DISPLAY_FLAG_DESTROY_CONTENT_ON_REMOVAL:I = 0x100

.field private static final VIRTUAL_DISPLAY_FLAG_DEVICE_DISPLAY_GROUP:I = 0x8000

.field private static final VIRTUAL_DISPLAY_FLAG_OWN_CONTENT_ONLY:I = 0x8

.field private static final VIRTUAL_DISPLAY_FLAG_OWN_DISPLAY_GROUP:I = 0x800

.field private static final VIRTUAL_DISPLAY_FLAG_OWN_FOCUS:I = 0x4000

.field private static final VIRTUAL_DISPLAY_FLAG_PRESENTATION:I = 0x2

.field private static final VIRTUAL_DISPLAY_FLAG_PUBLIC:I = 0x1

.field private static final VIRTUAL_DISPLAY_FLAG_ROTATES_WITH_CONTENT:I = 0x80

.field private static final VIRTUAL_DISPLAY_FLAG_SHOULD_SHOW_SYSTEM_DECORATIONS:I = 0x200

.field private static final VIRTUAL_DISPLAY_FLAG_SUPPORTS_TOUCH:I = 0x40

.field private static final VIRTUAL_DISPLAY_FLAG_TOUCH_FEEDBACK_DISABLED:I = 0x2000

.field private static final VIRTUAL_DISPLAY_FLAG_TRUSTED:I = 0x400


# instance fields
.field private final angle:F

.field private final captureOrientation:Lcom/android/helper/device/Orientation;

.field private final captureOrientationLocked:Z

.field private final crop:Landroid/graphics/Rect;

.field private displayImePolicy:I

.field private displaySize:Lcom/android/helper/device/Size;

.field private final displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

.field private displayTransform:Lcom/android/helper/util/AffineMatrix;

.field private dpi:I

.field private eventTransform:Lcom/android/helper/util/AffineMatrix;

.field private glRunner:Lcom/android/helper/opengl/OpenGLRunner;

.field private mainDisplayDpi:I

.field private mainDisplaySize:Lcom/android/helper/device/Size;

.field private maxSize:I

.field private final newDisplay:Lcom/android/helper/device/NewDisplay;

.field private physicalSize:Lcom/android/helper/device/Size;

.field private final vdDestroyContent:Z

.field private final vdListener:Lcom/android/helper/video/VirtualDisplayListener;

.field private final vdSystemDecorations:Z

.field private videoSize:Lcom/android/helper/device/Size;

.field private virtualDisplay:Landroid/hardware/display/VirtualDisplay;


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/video/VirtualDisplayListener;Lcom/android/helper/Options;)V
    .locals 1

    .line 68
    invoke-direct {p0}, Lcom/android/helper/video/SurfaceCapture;-><init>()V

    .line 44
    new-instance v0, Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-direct {v0}, Lcom/android/helper/video/DisplaySizeMonitor;-><init>()V

    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    .line 69
    iput-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->vdListener:Lcom/android/helper/video/VirtualDisplayListener;

    .line 70
    invoke-virtual {p2}, Lcom/android/helper/Options;->getNewDisplay()Lcom/android/helper/device/NewDisplay;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->newDisplay:Lcom/android/helper/device/NewDisplay;

    .line 72
    invoke-virtual {p2}, Lcom/android/helper/Options;->getMaxSize()I

    move-result p1

    iput p1, p0, Lcom/android/helper/video/NewDisplayCapture;->maxSize:I

    .line 73
    invoke-virtual {p2}, Lcom/android/helper/Options;->getDisplayImePolicy()I

    move-result p1

    iput p1, p0, Lcom/android/helper/video/NewDisplayCapture;->displayImePolicy:I

    .line 74
    invoke-virtual {p2}, Lcom/android/helper/Options;->getCrop()Landroid/graphics/Rect;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->crop:Landroid/graphics/Rect;

    .line 76
    invoke-virtual {p2}, Lcom/android/helper/Options;->getCaptureOrientationLock()Lcom/android/helper/device/Orientation$Lock;

    move-result-object p1

    sget-object v0, Lcom/android/helper/device/Orientation$Lock;->Unlocked:Lcom/android/helper/device/Orientation$Lock;

    if-eq p1, v0, :cond_0

    const/4 p1, 0x1

    goto :goto_0

    :cond_0
    const/4 p1, 0x0

    :goto_0
    iput-boolean p1, p0, Lcom/android/helper/video/NewDisplayCapture;->captureOrientationLocked:Z

    .line 77
    invoke-virtual {p2}, Lcom/android/helper/Options;->getCaptureOrientation()Lcom/android/helper/device/Orientation;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    .line 79
    invoke-virtual {p2}, Lcom/android/helper/Options;->getAngle()F

    move-result p1

    iput p1, p0, Lcom/android/helper/video/NewDisplayCapture;->angle:F

    .line 80
    invoke-virtual {p2}, Lcom/android/helper/Options;->getVDDestroyContent()Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/video/NewDisplayCapture;->vdDestroyContent:Z

    .line 81
    invoke-virtual {p2}, Lcom/android/helper/Options;->getVDSystemDecorations()Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/video/NewDisplayCapture;->vdSystemDecorations:Z

    return-void
.end method

.method private static scaleDpi(Lcom/android/helper/device/Size;ILcom/android/helper/device/Size;)I
    .locals 0

    .line 260
    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getMax()I

    move-result p0

    .line 261
    invoke-virtual {p2}, Lcom/android/helper/device/Size;->getMax()I

    move-result p2

    mul-int p1, p1, p2

    .line 262
    div-int/2addr p1, p0

    return p1
.end method


# virtual methods
.method public declared-synchronized getSize()Lcom/android/helper/device/Size;
    .locals 1

    monitor-enter p0

    .line 250
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->videoSize:Lcom/android/helper/device/Size;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    monitor-exit p0

    return-object v0

    :catchall_0
    move-exception v0

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v0
.end method

.method protected init()V
    .locals 3

    .line 86
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->newDisplay:Lcom/android/helper/device/NewDisplay;

    invoke-virtual {v0}, Lcom/android/helper/device/NewDisplay;->getSize()Lcom/android/helper/device/Size;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    .line 87
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->newDisplay:Lcom/android/helper/device/NewDisplay;

    invoke-virtual {v0}, Lcom/android/helper/device/NewDisplay;->getDpi()I

    move-result v0

    iput v0, p0, Lcom/android/helper/video/NewDisplayCapture;->dpi:I

    .line 88
    iget-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    if-eqz v1, :cond_1

    if-nez v0, :cond_0

    goto :goto_0

    :cond_0
    return-void

    .line 89
    :cond_1
    :goto_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/DisplayManager;->getDisplayInfo(I)Lcom/android/helper/device/DisplayInfo;

    move-result-object v0

    if-eqz v0, :cond_3

    .line 91
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplaySize:Lcom/android/helper/device/Size;

    .line 92
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getRotation()I

    move-result v1

    rem-int/lit8 v1, v1, 0x2

    if-eqz v1, :cond_2

    .line 93
    iget-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplaySize:Lcom/android/helper/device/Size;

    invoke-virtual {v1}, Lcom/android/helper/device/Size;->rotate()Lcom/android/helper/device/Size;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplaySize:Lcom/android/helper/device/Size;

    .line 95
    :cond_2
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getDpi()I

    move-result v0

    iput v0, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplayDpi:I

    return-void

    .line 97
    :cond_3
    const-string v0, "Main display not found, fallback to 1920x1080 240dpi"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 98
    new-instance v0, Lcom/android/helper/device/Size;

    const/16 v1, 0x780

    const/16 v2, 0x438

    invoke-direct {v0, v1, v2}, Lcom/android/helper/device/Size;-><init>(II)V

    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplaySize:Lcom/android/helper/device/Size;

    const/16 v0, 0xf0

    .line 99
    iput v0, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplayDpi:I

    return-void
.end method

.method public prepare()V
    .locals 7

    .line 107
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    const/4 v1, 0x0

    if-nez v0, :cond_2

    .line 108
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->newDisplay:Lcom/android/helper/device/NewDisplay;

    invoke-virtual {v0}, Lcom/android/helper/device/NewDisplay;->hasExplicitSize()Z

    move-result v0

    if-nez v0, :cond_0

    .line 109
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplaySize:Lcom/android/helper/device/Size;

    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    .line 111
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->newDisplay:Lcom/android/helper/device/NewDisplay;

    invoke-virtual {v0}, Lcom/android/helper/device/NewDisplay;->hasExplicitDpi()Z

    move-result v0

    if-nez v0, :cond_1

    .line 112
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplaySize:Lcom/android/helper/device/Size;

    iget v2, p0, Lcom/android/helper/video/NewDisplayCapture;->mainDisplayDpi:I

    iget-object v3, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-static {v0, v2, v3}, Lcom/android/helper/video/NewDisplayCapture;->scaleDpi(Lcom/android/helper/device/Size;ILcom/android/helper/device/Size;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/video/NewDisplayCapture;->dpi:I

    .line 115
    :cond_1
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->videoSize:Lcom/android/helper/device/Size;

    .line 118
    iget-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-virtual {v2, v0}, Lcom/android/helper/video/DisplaySizeMonitor;->setSessionDisplaySize(Lcom/android/helper/device/Size;)V

    const/4 v0, 0x0

    goto :goto_0

    .line 120
    :cond_2
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    iget-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    invoke-virtual {v2}, Landroid/hardware/display/VirtualDisplay;->getDisplay()Landroid/view/Display;

    move-result-object v2

    invoke-virtual {v2}, Landroid/view/Display;->getDisplayId()I

    move-result v2

    invoke-virtual {v0, v2}, Lcom/android/helper/wrappers/DisplayManager;->getDisplayInfo(I)Lcom/android/helper/device/DisplayInfo;

    move-result-object v0

    .line 121
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object v2

    iput-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    .line 122
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getDpi()I

    move-result v2

    iput v2, p0, Lcom/android/helper/video/NewDisplayCapture;->dpi:I

    .line 123
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getRotation()I

    move-result v0

    .line 126
    :goto_0
    new-instance v2, Lcom/android/helper/video/VideoFilter;

    iget-object v3, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-direct {v2, v3}, Lcom/android/helper/video/VideoFilter;-><init>(Lcom/android/helper/device/Size;)V

    .line 128
    iget-object v3, p0, Lcom/android/helper/video/NewDisplayCapture;->crop:Landroid/graphics/Rect;

    const/4 v4, 0x1

    if-eqz v3, :cond_4

    .line 129
    rem-int/lit8 v5, v0, 0x2

    if-eqz v5, :cond_3

    const/4 v5, 0x1

    goto :goto_1

    :cond_3
    const/4 v5, 0x0

    .line 130
    :goto_1
    invoke-virtual {v2, v3, v5}, Lcom/android/helper/video/VideoFilter;->addCrop(Landroid/graphics/Rect;Z)V

    .line 133
    :cond_4
    iget-boolean v3, p0, Lcom/android/helper/video/NewDisplayCapture;->captureOrientationLocked:Z

    iget-object v5, p0, Lcom/android/helper/video/NewDisplayCapture;->captureOrientation:Lcom/android/helper/device/Orientation;

    invoke-virtual {v2, v0, v3, v5}, Lcom/android/helper/video/VideoFilter;->addOrientation(IZLcom/android/helper/device/Orientation;)V

    .line 134
    iget v3, p0, Lcom/android/helper/video/NewDisplayCapture;->angle:F

    float-to-double v5, v3

    invoke-virtual {v2, v5, v6}, Lcom/android/helper/video/VideoFilter;->addAngle(D)V

    .line 136
    invoke-virtual {v2}, Lcom/android/helper/video/VideoFilter;->getOutputSize()Lcom/android/helper/device/Size;

    move-result-object v3

    .line 137
    invoke-virtual {v3}, Lcom/android/helper/device/Size;->isMultipleOf8()Z

    move-result v5

    if-eqz v5, :cond_5

    iget v5, p0, Lcom/android/helper/video/NewDisplayCapture;->maxSize:I

    if-eqz v5, :cond_7

    invoke-virtual {v3}, Lcom/android/helper/device/Size;->getMax()I

    move-result v5

    iget v6, p0, Lcom/android/helper/video/NewDisplayCapture;->maxSize:I

    if-le v5, v6, :cond_7

    .line 138
    :cond_5
    iget v5, p0, Lcom/android/helper/video/NewDisplayCapture;->maxSize:I

    if-eqz v5, :cond_6

    .line 139
    invoke-virtual {v3, v5}, Lcom/android/helper/device/Size;->limit(I)Lcom/android/helper/device/Size;

    move-result-object v3

    .line 141
    :cond_6
    invoke-virtual {v3}, Lcom/android/helper/device/Size;->round8()Lcom/android/helper/device/Size;

    move-result-object v3

    .line 142
    invoke-virtual {v2, v3}, Lcom/android/helper/video/VideoFilter;->addResize(Lcom/android/helper/device/Size;)V

    .line 145
    :cond_7
    invoke-virtual {v2}, Lcom/android/helper/video/VideoFilter;->getInverseTransform()Lcom/android/helper/util/AffineMatrix;

    move-result-object v3

    iput-object v3, p0, Lcom/android/helper/video/NewDisplayCapture;->eventTransform:Lcom/android/helper/util/AffineMatrix;

    .line 148
    invoke-virtual {v2}, Lcom/android/helper/video/VideoFilter;->getOutputSize()Lcom/android/helper/device/Size;

    move-result-object v2

    iput-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->videoSize:Lcom/android/helper/device/Size;

    .line 153
    rem-int/lit8 v2, v0, 0x2

    if-nez v2, :cond_8

    .line 154
    iget-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    iput-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->physicalSize:Lcom/android/helper/device/Size;

    goto :goto_2

    .line 156
    :cond_8
    iget-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-virtual {v2}, Lcom/android/helper/device/Size;->rotate()Lcom/android/helper/device/Size;

    move-result-object v2

    iput-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->physicalSize:Lcom/android/helper/device/Size;

    .line 158
    :goto_2
    new-instance v2, Lcom/android/helper/video/VideoFilter;

    iget-object v3, p0, Lcom/android/helper/video/NewDisplayCapture;->physicalSize:Lcom/android/helper/device/Size;

    invoke-direct {v2, v3}, Lcom/android/helper/video/VideoFilter;-><init>(Lcom/android/helper/device/Size;)V

    .line 159
    invoke-virtual {v2, v0}, Lcom/android/helper/video/VideoFilter;->addRotation(I)V

    .line 160
    invoke-virtual {v2}, Lcom/android/helper/video/VideoFilter;->getInverseTransform()Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    const/4 v2, 0x2

    .line 166
    new-array v2, v2, [Lcom/android/helper/util/AffineMatrix;

    aput-object v0, v2, v1

    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->eventTransform:Lcom/android/helper/util/AffineMatrix;

    aput-object v0, v2, v4

    invoke-static {v2}, Lcom/android/helper/util/AffineMatrix;->multiplyAll([Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displayTransform:Lcom/android/helper/util/AffineMatrix;

    return-void
.end method

.method public release()V
    .locals 1

    .line 240
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-virtual {v0}, Lcom/android/helper/video/DisplaySizeMonitor;->stopAndRelease()V

    .line 242
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    if-eqz v0, :cond_0

    .line 243
    invoke-virtual {v0}, Landroid/hardware/display/VirtualDisplay;->release()V

    const/4 v0, 0x0

    .line 244
    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    :cond_0
    return-void
.end method

.method public requestInvalidate()V
    .locals 0

    .line 267
    invoke-virtual {p0}, Lcom/android/helper/video/NewDisplayCapture;->invalidate()V

    return-void
.end method

.method public declared-synchronized setMaxSize(I)Z
    .locals 0

    monitor-enter p0

    .line 255
    :try_start_0
    iput p1, p0, Lcom/android/helper/video/NewDisplayCapture;->maxSize:I
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 256
    monitor-exit p0

    const/4 p1, 0x1

    return p1

    :catchall_0
    move-exception p1

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw p1
.end method

.method public start(Landroid/view/Surface;)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 211
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displayTransform:Lcom/android/helper/util/AffineMatrix;

    if-eqz v0, :cond_0

    .line 213
    new-instance v0, Lcom/android/helper/opengl/AffineOpenGLFilter;

    iget-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->displayTransform:Lcom/android/helper/util/AffineMatrix;

    invoke-direct {v0, v1}, Lcom/android/helper/opengl/AffineOpenGLFilter;-><init>(Lcom/android/helper/util/AffineMatrix;)V

    .line 214
    new-instance v1, Lcom/android/helper/opengl/OpenGLRunner;

    invoke-direct {v1, v0}, Lcom/android/helper/opengl/OpenGLRunner;-><init>(Lcom/android/helper/opengl/OpenGLFilter;)V

    iput-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    .line 215
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->physicalSize:Lcom/android/helper/device/Size;

    iget-object v2, p0, Lcom/android/helper/video/NewDisplayCapture;->videoSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1, v0, v2, p1}, Lcom/android/helper/opengl/OpenGLRunner;->start(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)Landroid/view/Surface;

    move-result-object p1

    .line 218
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    if-nez v0, :cond_1

    .line 219
    invoke-virtual {p0, p1}, Lcom/android/helper/video/NewDisplayCapture;->startNew(Landroid/view/Surface;)V

    goto :goto_0

    .line 221
    :cond_1
    invoke-virtual {v0, p1}, Landroid/hardware/display/VirtualDisplay;->setSurface(Landroid/view/Surface;)V

    .line 224
    :goto_0
    iget-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->vdListener:Lcom/android/helper/video/VirtualDisplayListener;

    if-eqz p1, :cond_2

    .line 225
    iget-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->videoSize:Lcom/android/helper/device/Size;

    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->eventTransform:Lcom/android/helper/util/AffineMatrix;

    iget-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-static {p1, v0, v1}, Lcom/android/helper/control/PositionMapper;->create(Lcom/android/helper/device/Size;Lcom/android/helper/util/AffineMatrix;Lcom/android/helper/device/Size;)Lcom/android/helper/control/PositionMapper;

    move-result-object p1

    .line 226
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->vdListener:Lcom/android/helper/video/VirtualDisplayListener;

    iget-object v1, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    invoke-virtual {v1}, Landroid/hardware/display/VirtualDisplay;->getDisplay()Landroid/view/Display;

    move-result-object v1

    invoke-virtual {v1}, Landroid/view/Display;->getDisplayId()I

    move-result v1

    invoke-interface {v0, v1, p1}, Lcom/android/helper/video/VirtualDisplayListener;->onNewVirtualDisplay(ILcom/android/helper/control/PositionMapper;)V

    :cond_2
    return-void
.end method

.method public startNew(Landroid/view/Surface;)V
    .locals 8

    const-string v0, "New display: "

    .line 177
    :try_start_0
    iget-boolean v1, p0, Lcom/android/helper/video/NewDisplayCapture;->vdDestroyContent:Z

    if-eqz v1, :cond_0

    const/16 v1, 0x1cb

    goto :goto_0

    :cond_0
    const/16 v1, 0xcb

    .line 180
    :goto_0
    iget-boolean v2, p0, Lcom/android/helper/video/NewDisplayCapture;->vdSystemDecorations:Z

    if-eqz v2, :cond_1

    or-int/lit16 v1, v1, 0x200

    .line 183
    :cond_1
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v3, 0x21

    if-lt v2, v3, :cond_3

    or-int/lit16 v2, v1, 0x3c00

    .line 188
    sget v3, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v4, 0x22

    if-lt v3, v4, :cond_2

    const v2, 0xfc00

    or-int/2addr v1, v2

    goto :goto_1

    :cond_2
    move v7, v2

    goto :goto_2

    :cond_3
    :goto_1
    move v7, v1

    .line 193
    :goto_2
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v1

    const-string v2, "scrcpy"

    iget-object v3, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    .line 194
    invoke-virtual {v3}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v3

    iget-object v4, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-virtual {v4}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v4

    iget v5, p0, Lcom/android/helper/video/NewDisplayCapture;->dpi:I

    move-object v6, p1

    invoke-virtual/range {v1 .. v7}, Lcom/android/helper/wrappers/DisplayManager;->createNewVirtualDisplay(Ljava/lang/String;IIILandroid/view/Surface;I)Landroid/hardware/display/VirtualDisplay;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/NewDisplayCapture;->virtualDisplay:Landroid/hardware/display/VirtualDisplay;

    .line 195
    invoke-virtual {p1}, Landroid/hardware/display/VirtualDisplay;->getDisplay()Landroid/view/Display;

    move-result-object p1

    invoke-virtual {p1}, Landroid/view/Display;->getDisplayId()I

    move-result p1

    .line 196
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-virtual {v0}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, "x"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySize:Lcom/android/helper/device/Size;

    invoke-virtual {v0}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, "/"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget v0, p0, Lcom/android/helper/video/NewDisplayCapture;->dpi:I

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, " (id="

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, ")"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 198
    iget v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displayImePolicy:I

    const/4 v1, -0x1

    if-eq v0, v1, :cond_4

    .line 199
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v0

    iget v1, p0, Lcom/android/helper/video/NewDisplayCapture;->displayImePolicy:I

    invoke-virtual {v0, p1, v1}, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicy(II)V

    .line 202
    :cond_4
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->displaySizeMonitor:Lcom/android/helper/video/DisplaySizeMonitor;

    new-instance v1, Lcom/android/helper/video/NewDisplayCapture$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0}, Lcom/android/helper/video/NewDisplayCapture$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/video/NewDisplayCapture;)V

    invoke-virtual {v0, p1, v1}, Lcom/android/helper/video/DisplaySizeMonitor;->start(ILcom/android/helper/video/DisplaySizeMonitor$Listener;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    move-object p1, v0

    .line 204
    const-string v0, "Could not create display"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 205
    new-instance p1, Ljava/lang/AssertionError;

    invoke-direct {p1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method

.method public stop()V
    .locals 1

    .line 232
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    if-eqz v0, :cond_0

    .line 233
    invoke-virtual {v0}, Lcom/android/helper/opengl/OpenGLRunner;->stopAndRelease()V

    const/4 v0, 0x0

    .line 234
    iput-object v0, p0, Lcom/android/helper/video/NewDisplayCapture;->glRunner:Lcom/android/helper/opengl/OpenGLRunner;

    :cond_0
    return-void
.end method
