.class public final synthetic Lcom/android/helper/util/LogUtils$$ExternalSyntheticLambda5;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/util/Comparator;


# direct methods
.method public synthetic constructor <init>()V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public final compare(Ljava/lang/Object;Ljava/lang/Object;)I
    .locals 0

    .line 0
    check-cast p1, Lcom/android/helper/device/DeviceApp;

    check-cast p2, Lcom/android/helper/device/DeviceApp;

    invoke-static {p1, p2}, Lcom/android/helper/util/LogUtils;->lambda$buildAppListMessage$0(Lcom/android/helper/device/DeviceApp;Lcom/android/helper/device/DeviceApp;)I

    move-result p1

    return p1
.end method
