.class public final synthetic Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Landroid/graphics/SurfaceTexture$OnFrameAvailableListener;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/opengl/OpenGLRunner;

.field public final synthetic f$1:Lcom/android/helper/device/Size;


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/opengl/OpenGLRunner;Lcom/android/helper/device/Size;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;->f$0:Lcom/android/helper/opengl/OpenGLRunner;

    iput-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;->f$1:Lcom/android/helper/device/Size;

    return-void
.end method


# virtual methods
.method public final onFrameAvailable(Landroid/graphics/SurfaceTexture;)V
    .locals 2

    .line 0
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;->f$0:Lcom/android/helper/opengl/OpenGLRunner;

    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda1;->f$1:Lcom/android/helper/device/Size;

    invoke-virtual {v0, v1, p1}, Lcom/android/helper/opengl/OpenGLRunner;->lambda$run$0$com-android-helper-opengl-OpenGLRunner(Lcom/android/helper/device/Size;Landroid/graphics/SurfaceTexture;)V

    return-void
.end method
