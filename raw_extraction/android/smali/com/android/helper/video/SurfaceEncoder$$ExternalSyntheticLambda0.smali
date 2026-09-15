.class public final synthetic Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/video/SurfaceEncoder;

.field public final synthetic f$1:Lcom/android/helper/AsyncProcessor$TerminationListener;


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/video/SurfaceEncoder;Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/video/SurfaceEncoder;

    iput-object p2, p0, Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;->f$1:Lcom/android/helper/AsyncProcessor$TerminationListener;

    return-void
.end method


# virtual methods
.method public final run()V
    .locals 2

    .line 0
    iget-object v0, p0, Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/video/SurfaceEncoder;

    iget-object v1, p0, Lcom/android/helper/video/SurfaceEncoder$$ExternalSyntheticLambda0;->f$1:Lcom/android/helper/AsyncProcessor$TerminationListener;

    invoke-virtual {v0, v1}, Lcom/android/helper/video/SurfaceEncoder;->lambda$start$0$com-android-helper-video-SurfaceEncoder(Lcom/android/helper/AsyncProcessor$TerminationListener;)V

    return-void
.end method
