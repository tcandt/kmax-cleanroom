.class public final Lcom/android/helper/opengl/OpenGLRunner;
.super Ljava/lang/Object;
.source "OpenGLRunner.java"


# static fields
.field private static handler:Landroid/os/Handler;

.field private static handlerThread:Landroid/os/HandlerThread;

.field private static quit:Z


# instance fields
.field private eglContext:Landroid/opengl/EGLContext;

.field private eglDisplay:Landroid/opengl/EGLDisplay;

.field private eglSurface:Landroid/opengl/EGLSurface;

.field private final filter:Lcom/android/helper/opengl/OpenGLFilter;

.field private inputSurface:Landroid/view/Surface;

.field private final overrideTransformMatrix:[F

.field private stopped:Z

.field private surfaceTexture:Landroid/graphics/SurfaceTexture;

.field private textureId:I


# direct methods
.method public constructor <init>(Lcom/android/helper/opengl/OpenGLFilter;)V
    .locals 1

    const/4 v0, 0x0

    .line 47
    invoke-direct {p0, p1, v0}, Lcom/android/helper/opengl/OpenGLRunner;-><init>(Lcom/android/helper/opengl/OpenGLFilter;[F)V

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/opengl/OpenGLFilter;[F)V
    .locals 0

    .line 41
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 42
    iput-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->filter:Lcom/android/helper/opengl/OpenGLFilter;

    .line 43
    iput-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner;->overrideTransformMatrix:[F

    return-void
.end method

.method static synthetic access$000(Lcom/android/helper/opengl/OpenGLRunner;Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)V
    .locals 0
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/opengl/OpenGLException;
        }
    .end annotation

    .line 22
    invoke-direct {p0, p1, p2, p3}, Lcom/android/helper/opengl/OpenGLRunner;->run(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)V

    return-void
.end method

.method public static declared-synchronized initOnce()V
    .locals 3

    const-class v0, Lcom/android/helper/opengl/OpenGLRunner;

    monitor-enter v0

    .line 51
    :try_start_0
    sget-object v1, Lcom/android/helper/opengl/OpenGLRunner;->handlerThread:Landroid/os/HandlerThread;

    if-nez v1, :cond_1

    .line 52
    sget-boolean v1, Lcom/android/helper/opengl/OpenGLRunner;->quit:Z

    if-nez v1, :cond_0

    .line 55
    new-instance v1, Landroid/os/HandlerThread;

    const-string v2, "OpenGLRunner"

    invoke-direct {v1, v2}, Landroid/os/HandlerThread;-><init>(Ljava/lang/String;)V

    sput-object v1, Lcom/android/helper/opengl/OpenGLRunner;->handlerThread:Landroid/os/HandlerThread;

    .line 56
    invoke-virtual {v1}, Landroid/os/HandlerThread;->start()V

    .line 57
    new-instance v1, Landroid/os/Handler;

    sget-object v2, Lcom/android/helper/opengl/OpenGLRunner;->handlerThread:Landroid/os/HandlerThread;

    invoke-virtual {v2}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object v2

    invoke-direct {v1, v2}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    sput-object v1, Lcom/android/helper/opengl/OpenGLRunner;->handler:Landroid/os/Handler;

    goto :goto_0

    .line 53
    :cond_0
    new-instance v1, Ljava/lang/IllegalStateException;

    const-string v2, "Could not init OpenGLRunner after it is quit"

    invoke-direct {v1, v2}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw v1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 59
    :cond_1
    :goto_0
    monitor-exit v0

    return-void

    :catchall_0
    move-exception v1

    :try_start_1
    monitor-exit v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v1
.end method

.method public static join()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 74
    const-class v0, Lcom/android/helper/opengl/OpenGLRunner;

    monitor-enter v0

    .line 75
    :try_start_0
    sget-object v1, Lcom/android/helper/opengl/OpenGLRunner;->handlerThread:Landroid/os/HandlerThread;

    .line 76
    monitor-exit v0
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v1, :cond_0

    .line 78
    invoke-virtual {v1}, Landroid/os/HandlerThread;->join()V

    :cond_0
    return-void

    :catchall_0
    move-exception v1

    .line 76
    :try_start_1
    monitor-exit v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v1
.end method

.method public static quit()V
    .locals 3

    .line 63
    const-class v0, Lcom/android/helper/opengl/OpenGLRunner;

    monitor-enter v0

    .line 64
    :try_start_0
    sget-object v1, Lcom/android/helper/opengl/OpenGLRunner;->handlerThread:Landroid/os/HandlerThread;

    const/4 v2, 0x1

    .line 65
    sput-boolean v2, Lcom/android/helper/opengl/OpenGLRunner;->quit:Z

    .line 66
    monitor-exit v0
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v1, :cond_0

    .line 68
    invoke-virtual {v1}, Landroid/os/HandlerThread;->quitSafely()Z

    :cond_0
    return-void

    :catchall_0
    move-exception v1

    .line 66
    :try_start_1
    monitor-exit v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v1
.end method

.method private render(Lcom/android/helper/device/Size;)V
    .locals 3

    .line 195
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p1

    const/4 v1, 0x0

    invoke-static {v1, v1, v0, p1}, Landroid/opengl/GLES20;->glViewport(IIII)V

    .line 196
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 198
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    invoke-virtual {p1}, Landroid/graphics/SurfaceTexture;->updateTexImage()V

    .line 201
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->overrideTransformMatrix:[F

    if-eqz p1, :cond_0

    goto :goto_0

    :cond_0
    const/16 p1, 0x10

    .line 204
    new-array p1, p1, [F

    .line 205
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    invoke-virtual {v0, p1}, Landroid/graphics/SurfaceTexture;->getTransformMatrix([F)V

    .line 208
    :goto_0
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->filter:Lcom/android/helper/opengl/OpenGLFilter;

    iget v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->textureId:I

    invoke-interface {v0, v1, p1}, Lcom/android/helper/opengl/OpenGLFilter;->draw(I[F)V

    .line 210
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglSurface:Landroid/opengl/EGLSurface;

    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    invoke-virtual {v1}, Landroid/graphics/SurfaceTexture;->getTimestamp()J

    move-result-wide v1

    invoke-static {p1, v0, v1, v2}, Landroid/opengl/EGLExt;->eglPresentationTimeANDROID(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLSurface;J)Z

    .line 211
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglSurface:Landroid/opengl/EGLSurface;

    invoke-static {p1, v0}, Landroid/opengl/EGL14;->eglSwapBuffers(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLSurface;)Z

    return-void
.end method

.method private run(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)V
    .locals 13
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/opengl/OpenGLException;
        }
    .end annotation

    const/4 v0, 0x0

    .line 107
    invoke-static {v0}, Landroid/opengl/EGL14;->eglGetDisplay(I)Landroid/opengl/EGLDisplay;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    .line 108
    sget-object v2, Landroid/opengl/EGL14;->EGL_NO_DISPLAY:Landroid/opengl/EGLDisplay;

    if-eq v1, v2, :cond_5

    const/4 v1, 0x2

    .line 112
    new-array v2, v1, [I

    .line 113
    iget-object v3, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    const/4 v4, 0x1

    invoke-static {v3, v2, v0, v2, v4}, Landroid/opengl/EGL14;->eglInitialize(Landroid/opengl/EGLDisplay;[II[II)Z

    move-result v2

    if-eqz v2, :cond_4

    const/16 v2, 0xb

    .line 118
    new-array v6, v2, [I

    fill-array-data v6, :array_0

    const/4 v10, 0x1

    .line 127
    new-array v8, v10, [Landroid/opengl/EGLConfig;

    .line 128
    new-array v11, v4, [I

    .line 129
    iget-object v5, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    const/4 v9, 0x0

    const/4 v12, 0x0

    const/4 v7, 0x0

    invoke-static/range {v5 .. v12}, Landroid/opengl/EGL14;->eglChooseConfig(Landroid/opengl/EGLDisplay;[II[Landroid/opengl/EGLConfig;II[II)Z

    .line 130
    aget v2, v11, v0

    if-lez v2, :cond_3

    .line 134
    aget-object v2, v8, v0

    const/16 v3, 0x3098

    const/16 v5, 0x3038

    .line 137
    filled-new-array {v3, v1, v5}, [I

    move-result-object v1

    .line 141
    iget-object v3, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    sget-object v6, Landroid/opengl/EGL14;->EGL_NO_CONTEXT:Landroid/opengl/EGLContext;

    invoke-static {v3, v2, v6, v1, v0}, Landroid/opengl/EGL14;->eglCreateContext(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLConfig;Landroid/opengl/EGLContext;[II)Landroid/opengl/EGLContext;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglContext:Landroid/opengl/EGLContext;

    if-eqz v1, :cond_2

    .line 147
    filled-new-array {v5}, [I

    move-result-object v1

    .line 150
    iget-object v3, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    move-object/from16 v5, p3

    invoke-static {v3, v2, v5, v1, v0}, Landroid/opengl/EGL14;->eglCreateWindowSurface(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLConfig;Ljava/lang/Object;[II)Landroid/opengl/EGLSurface;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglSurface:Landroid/opengl/EGLSurface;

    if-eqz v1, :cond_1

    .line 157
    iget-object v2, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object v3, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglContext:Landroid/opengl/EGLContext;

    invoke-static {v2, v1, v1, v3}, Landroid/opengl/EGL14;->eglMakeCurrent(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLSurface;Landroid/opengl/EGLSurface;Landroid/opengl/EGLContext;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 164
    new-array v1, v4, [I

    .line 165
    invoke-static {v4, v1, v0}, Landroid/opengl/GLES20;->glGenTextures(I[II)V

    .line 166
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 167
    aget v0, v1, v0

    iput v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->textureId:I

    const/16 v0, 0x2801

    const v1, 0x8d65

    const/16 v2, 0x2601

    .line 169
    invoke-static {v1, v0, v2}, Landroid/opengl/GLES20;->glTexParameteri(III)V

    .line 170
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const/16 v0, 0x2800

    .line 171
    invoke-static {v1, v0, v2}, Landroid/opengl/GLES20;->glTexParameteri(III)V

    .line 172
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const/16 v0, 0x2802

    const v2, 0x812f

    .line 173
    invoke-static {v1, v0, v2}, Landroid/opengl/GLES20;->glTexParameteri(III)V

    .line 174
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const/16 v0, 0x2803

    .line 175
    invoke-static {v1, v0, v2}, Landroid/opengl/GLES20;->glTexParameteri(III)V

    .line 176
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 178
    new-instance v0, Landroid/graphics/SurfaceTexture;

    iget v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->textureId:I

    invoke-direct {v0, v1}, Landroid/graphics/SurfaceTexture;-><init>(I)V

    iput-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    .line 179
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v1

    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p1

    invoke-virtual {v0, v1, p1}, Landroid/graphics/SurfaceTexture;->setDefaultBufferSize(II)V

    .line 180
    new-instance p1, Landroid/view/Surface;

    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    invoke-direct {p1, v0}, Landroid/view/Surface;-><init>(Landroid/graphics/SurfaceTexture;)V

    iput-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->inputSurface:Landroid/view/Surface;

    .line 182
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->filter:Lcom/android/helper/opengl/OpenGLFilter;

    invoke-interface {p1}, Lcom/android/helper/opengl/OpenGLFilter;->init()V

    .line 184
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    new-instance v0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;

    invoke-direct {v0, p0, p2}, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;-><init>(Lcom/android/helper/opengl/OpenGLRunner;Lcom/android/helper/device/Size;)V

    sget-object p2, Lcom/android/helper/opengl/OpenGLRunner;->handler:Landroid/os/Handler;

    invoke-virtual {p1, v0, p2}, Landroid/graphics/SurfaceTexture;->setOnFrameAvailableListener(Landroid/graphics/SurfaceTexture$OnFrameAvailableListener;Landroid/os/Handler;)V

    return-void

    .line 158
    :cond_0
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglSurface:Landroid/opengl/EGLSurface;

    invoke-static {p1, p2}, Landroid/opengl/EGL14;->eglDestroySurface(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLSurface;)Z

    .line 159
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglContext:Landroid/opengl/EGLContext;

    invoke-static {p1, p2}, Landroid/opengl/EGL14;->eglDestroyContext(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLContext;)Z

    .line 160
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    invoke-static {p1}, Landroid/opengl/EGL14;->eglTerminate(Landroid/opengl/EGLDisplay;)Z

    .line 161
    new-instance p1, Lcom/android/helper/opengl/OpenGLException;

    const-string p2, "Failed to make EGL context current"

    invoke-direct {p1, p2}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 152
    :cond_1
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglContext:Landroid/opengl/EGLContext;

    invoke-static {p1, p2}, Landroid/opengl/EGL14;->eglDestroyContext(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLContext;)Z

    .line 153
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    invoke-static {p1}, Landroid/opengl/EGL14;->eglTerminate(Landroid/opengl/EGLDisplay;)Z

    .line 154
    new-instance p1, Lcom/android/helper/opengl/OpenGLException;

    const-string p2, "Failed to create EGL window surface"

    invoke-direct {p1, p2}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 143
    :cond_2
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    invoke-static {p1}, Landroid/opengl/EGL14;->eglTerminate(Landroid/opengl/EGLDisplay;)Z

    .line 144
    new-instance p1, Lcom/android/helper/opengl/OpenGLException;

    const-string p2, "Failed to create EGL context"

    invoke-direct {p1, p2}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 131
    :cond_3
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    invoke-static {p1}, Landroid/opengl/EGL14;->eglTerminate(Landroid/opengl/EGLDisplay;)Z

    .line 132
    new-instance p1, Lcom/android/helper/opengl/OpenGLException;

    const-string p2, "Unable to find ES2 EGL config"

    invoke-direct {p1, p2}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 114
    :cond_4
    new-instance p1, Lcom/android/helper/opengl/OpenGLException;

    const-string p2, "Unable to initialize EGL14"

    invoke-direct {p1, p2}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 109
    :cond_5
    new-instance p1, Lcom/android/helper/opengl/OpenGLException;

    const-string p2, "Unable to get EGL14 display"

    invoke-direct {p1, p2}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw p1

    nop

    :array_0
    .array-data 4
        0x3024
        0x8
        0x3023
        0x8
        0x3022
        0x8
        0x3021
        0x8
        0x3040
        0x4
        0x3038
    .end array-data
.end method


# virtual methods
.method synthetic lambda$run$0$com-android-helper-opengl-OpenGLRunner(Lcom/android/helper/device/Size;Landroid/graphics/SurfaceTexture;)V
    .locals 0

    .line 185
    iget-boolean p2, p0, Lcom/android/helper/opengl/OpenGLRunner;->stopped:Z

    if-eqz p2, :cond_0

    return-void

    .line 190
    :cond_0
    invoke-direct {p0, p1}, Lcom/android/helper/opengl/OpenGLRunner;->render(Lcom/android/helper/device/Size;)V

    return-void
.end method

.method synthetic lambda$stopAndRelease$1$com-android-helper-opengl-OpenGLRunner(Ljava/util/concurrent/Semaphore;)V
    .locals 4

    .line 0
    const/4 v0, 0x1

    .line 218
    iput-boolean v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->stopped:Z

    .line 219
    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    const/4 v2, 0x0

    sget-object v3, Lcom/android/helper/opengl/OpenGLRunner;->handler:Landroid/os/Handler;

    invoke-virtual {v1, v2, v3}, Landroid/graphics/SurfaceTexture;->setOnFrameAvailableListener(Landroid/graphics/SurfaceTexture$OnFrameAvailableListener;Landroid/os/Handler;)V

    .line 221
    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->filter:Lcom/android/helper/opengl/OpenGLFilter;

    invoke-interface {v1}, Lcom/android/helper/opengl/OpenGLFilter;->release()V

    .line 223
    iget v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->textureId:I

    filled-new-array {v1}, [I

    move-result-object v1

    const/4 v2, 0x0

    .line 224
    invoke-static {v0, v1, v2}, Landroid/opengl/GLES20;->glDeleteTextures(I[II)V

    .line 225
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 227
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglSurface:Landroid/opengl/EGLSurface;

    invoke-static {v0, v1}, Landroid/opengl/EGL14;->eglDestroySurface(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLSurface;)Z

    .line 228
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglContext:Landroid/opengl/EGLContext;

    invoke-static {v0, v1}, Landroid/opengl/EGL14;->eglDestroyContext(Landroid/opengl/EGLDisplay;Landroid/opengl/EGLContext;)Z

    .line 229
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    invoke-static {v0}, Landroid/opengl/EGL14;->eglTerminate(Landroid/opengl/EGLDisplay;)Z

    .line 230
    sget-object v0, Landroid/opengl/EGL14;->EGL_NO_DISPLAY:Landroid/opengl/EGLDisplay;

    iput-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglDisplay:Landroid/opengl/EGLDisplay;

    .line 231
    sget-object v0, Landroid/opengl/EGL14;->EGL_NO_CONTEXT:Landroid/opengl/EGLContext;

    iput-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglContext:Landroid/opengl/EGLContext;

    .line 232
    sget-object v0, Landroid/opengl/EGL14;->EGL_NO_SURFACE:Landroid/opengl/EGLSurface;

    iput-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->eglSurface:Landroid/opengl/EGLSurface;

    .line 233
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->surfaceTexture:Landroid/graphics/SurfaceTexture;

    invoke-virtual {v0}, Landroid/graphics/SurfaceTexture;->release()V

    .line 234
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner;->inputSurface:Landroid/view/Surface;

    invoke-virtual {v0}, Landroid/view/Surface;->release()V

    .line 236
    invoke-virtual {p1}, Ljava/util/concurrent/Semaphore;->release()V

    return-void
.end method

.method public start(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)Landroid/view/Surface;
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/opengl/OpenGLException;
        }
    .end annotation

    .line 83
    invoke-static {}, Lcom/android/helper/opengl/OpenGLRunner;->initOnce()V

    .line 88
    :try_start_0
    sget-object v0, Lcom/android/helper/opengl/OpenGLRunner;->handler:Landroid/os/Handler;

    new-instance v1, Lcom/android/helper/opengl/OpenGLRunner$1;

    invoke-direct {v1, p0, p1, p2, p3}, Lcom/android/helper/opengl/OpenGLRunner$1;-><init>(Lcom/android/helper/opengl/OpenGLRunner;Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)V

    invoke-static {v0, v1}, Lcom/android/helper/util/Threads;->executeSynchronouslyOn(Landroid/os/Handler;Ljava/util/concurrent/Callable;)Ljava/lang/Object;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 103
    iget-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner;->inputSurface:Landroid/view/Surface;

    return-object p1

    :catchall_0
    move-exception p1

    .line 96
    instance-of p2, p1, Lcom/android/helper/opengl/OpenGLException;

    if-eqz p2, :cond_0

    .line 97
    check-cast p1, Lcom/android/helper/opengl/OpenGLException;

    throw p1

    .line 99
    :cond_0
    new-instance p2, Lcom/android/helper/opengl/OpenGLException;

    const-string p3, "Asynchronous OpenGL runner init failed"

    invoke-direct {p2, p3, p1}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;Ljava/lang/Throwable;)V

    throw p2
.end method

.method public stopAndRelease()V
    .locals 3

    .line 215
    new-instance v0, Ljava/util/concurrent/Semaphore;

    const/4 v1, 0x0

    invoke-direct {v0, v1}, Ljava/util/concurrent/Semaphore;-><init>(I)V

    .line 217
    sget-object v1, Lcom/android/helper/opengl/OpenGLRunner;->handler:Landroid/os/Handler;

    new-instance v2, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;

    invoke-direct {v2, p0, v0}, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/opengl/OpenGLRunner;Ljava/util/concurrent/Semaphore;)V

    invoke-virtual {v1, v2}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 240
    :try_start_0
    invoke-virtual {v0}, Ljava/util/concurrent/Semaphore;->acquire()V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    .line 243
    :catch_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    return-void
.end method
