.class public final synthetic Lcom/android/helper/video/NewDisplayCapture$$ExternalSyntheticLambda0;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Lcom/android/helper/video/DisplaySizeMonitor$Listener;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/video/NewDisplayCapture;


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/video/NewDisplayCapture;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/video/NewDisplayCapture$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/video/NewDisplayCapture;

    return-void
.end method


# virtual methods
.method public final onDisplaySizeChanged()V
    .locals 1

    .line 0
    iget-object v0, p0, Lcom/android/helper/video/NewDisplayCapture$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/video/NewDisplayCapture;

    invoke-virtual {v0}, Lcom/android/helper/video/SurfaceCapture;->invalidate()V

    return-void
.end method
