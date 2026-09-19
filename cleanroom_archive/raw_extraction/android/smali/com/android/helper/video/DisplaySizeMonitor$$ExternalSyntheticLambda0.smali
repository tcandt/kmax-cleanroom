.class public final synthetic Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Lcom/android/helper/wrappers/DisplayManager$DisplayListener;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/video/DisplaySizeMonitor;

.field public final synthetic f$1:I


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/video/DisplaySizeMonitor;I)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/video/DisplaySizeMonitor;

    iput p2, p0, Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;->f$1:I

    return-void
.end method


# virtual methods
.method public final onDisplayChanged(I)V
    .locals 2

    .line 0
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/video/DisplaySizeMonitor;

    iget v1, p0, Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;->f$1:I

    invoke-virtual {v0, v1, p1}, Lcom/android/helper/video/DisplaySizeMonitor;->lambda$start$0$com-android-helper-video-DisplaySizeMonitor(II)V

    return-void
.end method
