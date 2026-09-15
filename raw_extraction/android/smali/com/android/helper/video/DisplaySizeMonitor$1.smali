.class Lcom/android/helper/video/DisplaySizeMonitor$1;
.super Lcom/android/helper/wrappers/DisplayWindowListener;
.source "DisplaySizeMonitor.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/android/helper/video/DisplaySizeMonitor;->start(ILcom/android/helper/video/DisplaySizeMonitor$Listener;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/android/helper/video/DisplaySizeMonitor;

.field final synthetic val$displayId:I


# direct methods
.method constructor <init>(Lcom/android/helper/video/DisplaySizeMonitor;I)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010
        }
        names = {
            null,
            null
        }
    .end annotation

    .line 63
    iput-object p1, p0, Lcom/android/helper/video/DisplaySizeMonitor$1;->this$0:Lcom/android/helper/video/DisplaySizeMonitor;

    iput p2, p0, Lcom/android/helper/video/DisplaySizeMonitor$1;->val$displayId:I

    invoke-direct {p0}, Lcom/android/helper/wrappers/DisplayWindowListener;-><init>()V

    return-void
.end method


# virtual methods
.method public onDisplayConfigurationChanged(ILandroid/content/res/Configuration;)V
    .locals 1

    .line 66
    sget-object p2, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {p2}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result p2

    if-eqz p2, :cond_0

    .line 67
    new-instance p2, Ljava/lang/StringBuilder;

    const-string v0, "DisplaySizeMonitor: onDisplayConfigurationChanged("

    invoke-direct {p2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, ")"

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-static {p2}, Lcom/android/helper/util/Ln;->v(Ljava/lang/String;)V

    .line 70
    :cond_0
    iget p2, p0, Lcom/android/helper/video/DisplaySizeMonitor$1;->val$displayId:I

    if-ne p1, p2, :cond_1

    .line 71
    iget-object p1, p0, Lcom/android/helper/video/DisplaySizeMonitor$1;->this$0:Lcom/android/helper/video/DisplaySizeMonitor;

    invoke-static {p1}, Lcom/android/helper/video/DisplaySizeMonitor;->access$000(Lcom/android/helper/video/DisplaySizeMonitor;)V

    :cond_1
    return-void
.end method
