.class public Lcom/android/helper/control/PointersState;
.super Ljava/lang/Object;
.source "PointersState.java"


# static fields
.field public static final MAX_POINTERS:I = 0xa


# instance fields
.field private final pointers:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/android/helper/control/Pointer;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method public constructor <init>()V
    .locals 1

    .line 10
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 14
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    return-void
.end method

.method private cleanUp()V
    .locals 2

    .line 98
    iget-object v0, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v0

    add-int/lit8 v0, v0, -0x1

    :goto_0
    if-ltz v0, :cond_1

    .line 99
    iget-object v1, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v1, v0}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/android/helper/control/Pointer;

    .line 100
    invoke-virtual {v1}, Lcom/android/helper/control/Pointer;->isUp()Z

    move-result v1

    if-eqz v1, :cond_0

    .line 101
    iget-object v1, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v1, v0}, Ljava/util/List;->remove(I)Ljava/lang/Object;

    :cond_0
    add-int/lit8 v0, v0, -0x1

    goto :goto_0

    :cond_1
    return-void
.end method

.method private indexOf(J)I
    .locals 4

    const/4 v0, 0x0

    .line 17
    :goto_0
    iget-object v1, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v1}, Ljava/util/List;->size()I

    move-result v1

    if-ge v0, v1, :cond_1

    .line 18
    iget-object v1, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v1, v0}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/android/helper/control/Pointer;

    .line 19
    invoke-virtual {v1}, Lcom/android/helper/control/Pointer;->getId()J

    move-result-wide v1

    cmp-long v3, v1, p1

    if-nez v3, :cond_0

    return v0

    :cond_0
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_1
    const/4 p1, -0x1

    return p1
.end method

.method private isLocalIdAvailable(I)Z
    .locals 3

    const/4 v0, 0x0

    const/4 v1, 0x0

    .line 27
    :goto_0
    iget-object v2, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v2}, Ljava/util/List;->size()I

    move-result v2

    if-ge v1, v2, :cond_1

    .line 28
    iget-object v2, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v2, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Lcom/android/helper/control/Pointer;

    .line 29
    invoke-virtual {v2}, Lcom/android/helper/control/Pointer;->getLocalId()I

    move-result v2

    if-ne v2, p1, :cond_0

    return v0

    :cond_0
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_1
    const/4 p1, 0x1

    return p1
.end method

.method private nextUnusedLocalId()I
    .locals 2

    const/4 v0, 0x0

    :goto_0
    const/16 v1, 0xa

    if-ge v0, v1, :cond_1

    .line 38
    invoke-direct {p0, v0}, Lcom/android/helper/control/PointersState;->isLocalIdAvailable(I)Z

    move-result v1

    if-eqz v1, :cond_0

    return v0

    :cond_0
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    return v0
.end method


# virtual methods
.method public get(I)Lcom/android/helper/control/Pointer;
    .locals 1

    .line 46
    iget-object v0, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v0, p1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Lcom/android/helper/control/Pointer;

    return-object p1
.end method

.method public getPointerIndex(J)I
    .locals 3

    .line 50
    invoke-direct {p0, p1, p2}, Lcom/android/helper/control/PointersState;->indexOf(J)I

    move-result v0

    const/4 v1, -0x1

    if-eq v0, v1, :cond_0

    return v0

    .line 55
    :cond_0
    iget-object v0, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v0

    const/16 v2, 0xa

    if-lt v0, v2, :cond_1

    return v1

    .line 60
    :cond_1
    invoke-direct {p0}, Lcom/android/helper/control/PointersState;->nextUnusedLocalId()I

    move-result v0

    if-eq v0, v1, :cond_2

    .line 64
    new-instance v1, Lcom/android/helper/control/Pointer;

    invoke-direct {v1, p1, p2, v0}, Lcom/android/helper/control/Pointer;-><init>(JI)V

    .line 65
    iget-object p1, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {p1, v1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    .line 67
    iget-object p1, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {p1}, Ljava/util/List;->size()I

    move-result p1

    add-int/lit8 p1, p1, -0x1

    return p1

    .line 62
    :cond_2
    new-instance p1, Ljava/lang/AssertionError;

    const-string p2, "pointers.size() < maxFingers implies that a local id is available"

    invoke-direct {p1, p2}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method

.method public update([Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;)I
    .locals 6

    .line 78
    iget-object v0, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v0}, Ljava/util/List;->size()I

    move-result v0

    const/4 v1, 0x0

    :goto_0
    if-ge v1, v0, :cond_0

    .line 80
    iget-object v2, p0, Lcom/android/helper/control/PointersState;->pointers:Ljava/util/List;

    invoke-interface {v2, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Lcom/android/helper/control/Pointer;

    .line 83
    aget-object v3, p1, v1

    invoke-virtual {v2}, Lcom/android/helper/control/Pointer;->getLocalId()I

    move-result v4

    iput v4, v3, Landroid/view/MotionEvent$PointerProperties;->id:I

    .line 85
    invoke-virtual {v2}, Lcom/android/helper/control/Pointer;->getPoint()Lcom/android/helper/device/Point;

    move-result-object v3

    .line 86
    aget-object v4, p2, v1

    invoke-virtual {v3}, Lcom/android/helper/device/Point;->getX()I

    move-result v5

    int-to-float v5, v5

    iput v5, v4, Landroid/view/MotionEvent$PointerCoords;->x:F

    .line 87
    aget-object v4, p2, v1

    invoke-virtual {v3}, Lcom/android/helper/device/Point;->getY()I

    move-result v3

    int-to-float v3, v3

    iput v3, v4, Landroid/view/MotionEvent$PointerCoords;->y:F

    .line 88
    aget-object v3, p2, v1

    invoke-virtual {v2}, Lcom/android/helper/control/Pointer;->getPressure()F

    move-result v2

    iput v2, v3, Landroid/view/MotionEvent$PointerCoords;->pressure:F

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 90
    :cond_0
    invoke-direct {p0}, Lcom/android/helper/control/PointersState;->cleanUp()V

    return v0
.end method
