.class public final synthetic Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/opengl/OpenGLRunner;

.field public final synthetic f$1:Ljava/util/concurrent/Semaphore;


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/opengl/OpenGLRunner;Ljava/util/concurrent/Semaphore;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/opengl/OpenGLRunner;

    iput-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;->f$1:Ljava/util/concurrent/Semaphore;

    return-void
.end method


# virtual methods
.method public final run()V
    .locals 2

    .line 0
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/opengl/OpenGLRunner;

    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner$$ExternalSyntheticLambda0;->f$1:Ljava/util/concurrent/Semaphore;

    invoke-virtual {v0, v1}, Lcom/android/helper/opengl/OpenGLRunner;->lambda$stopAndRelease$1$com-android-helper-opengl-OpenGLRunner(Ljava/util/concurrent/Semaphore;)V

    return-void
.end method
