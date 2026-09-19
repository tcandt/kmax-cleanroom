.class Lcom/android/helper/opengl/OpenGLRunner$1;
.super Ljava/lang/Object;
.source "OpenGLRunner.java"

# interfaces
.implements Ljava/util/concurrent/Callable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/android/helper/opengl/OpenGLRunner;->start(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)Landroid/view/Surface;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Object;",
        "Ljava/util/concurrent/Callable<",
        "Ljava/lang/Void;",
        ">;"
    }
.end annotation


# instance fields
.field final synthetic this$0:Lcom/android/helper/opengl/OpenGLRunner;

.field final synthetic val$inputSize:Lcom/android/helper/device/Size;

.field final synthetic val$outputSize:Lcom/android/helper/device/Size;

.field final synthetic val$outputSurface:Landroid/view/Surface;


# direct methods
.method constructor <init>(Lcom/android/helper/opengl/OpenGLRunner;Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010,
            0x1010,
            0x1010
        }
        names = {
            null,
            null,
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 88
    iput-object p1, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->this$0:Lcom/android/helper/opengl/OpenGLRunner;

    iput-object p2, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->val$inputSize:Lcom/android/helper/device/Size;

    iput-object p3, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->val$outputSize:Lcom/android/helper/device/Size;

    iput-object p4, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->val$outputSurface:Landroid/view/Surface;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public bridge synthetic call()Ljava/lang/Object;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 88
    invoke-virtual {p0}, Lcom/android/helper/opengl/OpenGLRunner$1;->call()Ljava/lang/Void;

    move-result-object v0

    return-object v0
.end method

.method public call()Ljava/lang/Void;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 91
    iget-object v0, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->this$0:Lcom/android/helper/opengl/OpenGLRunner;

    iget-object v1, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->val$inputSize:Lcom/android/helper/device/Size;

    iget-object v2, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->val$outputSize:Lcom/android/helper/device/Size;

    iget-object v3, p0, Lcom/android/helper/opengl/OpenGLRunner$1;->val$outputSurface:Landroid/view/Surface;

    invoke-static {v0, v1, v2, v3}, Lcom/android/helper/opengl/OpenGLRunner;->access$000(Lcom/android/helper/opengl/OpenGLRunner;Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;Landroid/view/Surface;)V

    const/4 v0, 0x0

    return-object v0
.end method
