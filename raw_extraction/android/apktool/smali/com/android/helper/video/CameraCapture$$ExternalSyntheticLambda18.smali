.class public final synthetic Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda18;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/util/Comparator;


# instance fields
.field public final synthetic f$0:Ljava/lang/Float;


# direct methods
.method public synthetic constructor <init>(Ljava/lang/Float;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda18;->f$0:Ljava/lang/Float;

    return-void
.end method


# virtual methods
.method public final compare(Ljava/lang/Object;Ljava/lang/Object;)I
    .locals 1

    .line 0
    iget-object v0, p0, Lcom/android/helper/video/CameraCapture$$ExternalSyntheticLambda18;->f$0:Ljava/lang/Float;

    check-cast p1, Landroid/util/Size;

    check-cast p2, Landroid/util/Size;

    invoke-static {v0, p1, p2}, Lcom/android/helper/video/CameraCapture;->lambda$selectSize$2(Ljava/lang/Float;Landroid/util/Size;Landroid/util/Size;)I

    move-result p1

    return p1
.end method
