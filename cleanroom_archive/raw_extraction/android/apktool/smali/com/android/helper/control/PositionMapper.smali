.class public final Lcom/android/helper/control/PositionMapper;
.super Ljava/lang/Object;
.source "PositionMapper.java"


# instance fields
.field private final videoSize:Lcom/android/helper/device/Size;

.field private final videoToDeviceMatrix:Lcom/android/helper/util/AffineMatrix;


# direct methods
.method public constructor <init>(Lcom/android/helper/device/Size;Lcom/android/helper/util/AffineMatrix;)V
    .locals 0

    .line 13
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 14
    iput-object p1, p0, Lcom/android/helper/control/PositionMapper;->videoSize:Lcom/android/helper/device/Size;

    .line 15
    iput-object p2, p0, Lcom/android/helper/control/PositionMapper;->videoToDeviceMatrix:Lcom/android/helper/util/AffineMatrix;

    return-void
.end method

.method public static create(Lcom/android/helper/device/Size;Lcom/android/helper/util/AffineMatrix;Lcom/android/helper/device/Size;)Lcom/android/helper/control/PositionMapper;
    .locals 1

    .line 19
    invoke-virtual {p0, p2}, Lcom/android/helper/device/Size;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    if-eqz p1, :cond_1

    .line 22
    :cond_0
    invoke-static {p0}, Lcom/android/helper/util/AffineMatrix;->ndcFromPixels(Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    .line 23
    invoke-static {p2}, Lcom/android/helper/util/AffineMatrix;->ndcToPixels(Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p2

    .line 24
    invoke-virtual {p2, p1}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    invoke-virtual {p1, v0}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    .line 27
    :cond_1
    new-instance p2, Lcom/android/helper/control/PositionMapper;

    invoke-direct {p2, p0, p1}, Lcom/android/helper/control/PositionMapper;-><init>(Lcom/android/helper/device/Size;Lcom/android/helper/util/AffineMatrix;)V

    return-object p2
.end method


# virtual methods
.method public getVideoSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 31
    iget-object v0, p0, Lcom/android/helper/control/PositionMapper;->videoSize:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public map(Lcom/android/helper/device/Position;)Lcom/android/helper/device/Point;
    .locals 2

    .line 35
    invoke-virtual {p1}, Lcom/android/helper/device/Position;->getScreenSize()Lcom/android/helper/device/Size;

    move-result-object v0

    .line 36
    iget-object v1, p0, Lcom/android/helper/control/PositionMapper;->videoSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1, v0}, Lcom/android/helper/device/Size;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    const/4 p1, 0x0

    return-object p1

    .line 42
    :cond_0
    invoke-virtual {p1}, Lcom/android/helper/device/Position;->getPoint()Lcom/android/helper/device/Point;

    move-result-object p1

    .line 43
    iget-object v0, p0, Lcom/android/helper/control/PositionMapper;->videoToDeviceMatrix:Lcom/android/helper/util/AffineMatrix;

    if-eqz v0, :cond_1

    .line 44
    invoke-virtual {v0, p1}, Lcom/android/helper/util/AffineMatrix;->apply(Lcom/android/helper/device/Point;)Lcom/android/helper/device/Point;

    move-result-object p1

    :cond_1
    return-object p1
.end method
