.class public Lcom/android/helper/control/Pointer;
.super Ljava/lang/Object;
.source "Pointer.java"


# instance fields
.field private final id:J

.field private final localId:I

.field private point:Lcom/android/helper/device/Point;

.field private pressure:F

.field private up:Z


# direct methods
.method public constructor <init>(JI)V
    .locals 0

    .line 21
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 22
    iput-wide p1, p0, Lcom/android/helper/control/Pointer;->id:J

    .line 23
    iput p3, p0, Lcom/android/helper/control/Pointer;->localId:I

    return-void
.end method


# virtual methods
.method public getId()J
    .locals 2

    .line 27
    iget-wide v0, p0, Lcom/android/helper/control/Pointer;->id:J

    return-wide v0
.end method

.method public getLocalId()I
    .locals 1

    .line 31
    iget v0, p0, Lcom/android/helper/control/Pointer;->localId:I

    return v0
.end method

.method public getPoint()Lcom/android/helper/device/Point;
    .locals 1

    .line 35
    iget-object v0, p0, Lcom/android/helper/control/Pointer;->point:Lcom/android/helper/device/Point;

    return-object v0
.end method

.method public getPressure()F
    .locals 1

    .line 43
    iget v0, p0, Lcom/android/helper/control/Pointer;->pressure:F

    return v0
.end method

.method public isUp()Z
    .locals 1

    .line 51
    iget-boolean v0, p0, Lcom/android/helper/control/Pointer;->up:Z

    return v0
.end method

.method public setPoint(Lcom/android/helper/device/Point;)V
    .locals 0

    .line 39
    iput-object p1, p0, Lcom/android/helper/control/Pointer;->point:Lcom/android/helper/device/Point;

    return-void
.end method

.method public setPressure(F)V
    .locals 0

    .line 47
    iput p1, p0, Lcom/android/helper/control/Pointer;->pressure:F

    return-void
.end method

.method public setUp(Z)V
    .locals 0

    .line 55
    iput-boolean p1, p0, Lcom/android/helper/control/Pointer;->up:Z

    return-void
.end method
