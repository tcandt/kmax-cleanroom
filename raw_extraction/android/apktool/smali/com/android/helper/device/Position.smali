.class public Lcom/android/helper/device/Position;
.super Ljava/lang/Object;
.source "Position.java"


# instance fields
.field private final point:Lcom/android/helper/device/Point;

.field private final screenSize:Lcom/android/helper/device/Size;


# direct methods
.method public constructor <init>(IIII)V
    .locals 1

    .line 15
    new-instance v0, Lcom/android/helper/device/Point;

    invoke-direct {v0, p1, p2}, Lcom/android/helper/device/Point;-><init>(II)V

    new-instance p1, Lcom/android/helper/device/Size;

    invoke-direct {p1, p3, p4}, Lcom/android/helper/device/Size;-><init>(II)V

    invoke-direct {p0, v0, p1}, Lcom/android/helper/device/Position;-><init>(Lcom/android/helper/device/Point;Lcom/android/helper/device/Size;)V

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/device/Point;Lcom/android/helper/device/Size;)V
    .locals 0

    .line 9
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 10
    iput-object p1, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    .line 11
    iput-object p2, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    return-void
.end method


# virtual methods
.method public equals(Ljava/lang/Object;)Z
    .locals 4

    const/4 v0, 0x1

    if-ne p0, p1, :cond_0

    return v0

    :cond_0
    const/4 v1, 0x0

    if-eqz p1, :cond_2

    .line 44
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v2

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v3

    if-eq v2, v3, :cond_1

    goto :goto_0

    .line 47
    :cond_1
    check-cast p1, Lcom/android/helper/device/Position;

    .line 48
    iget-object v2, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    iget-object v3, p1, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-static {v2, v3}, Ljava/util/Objects;->equals(Ljava/lang/Object;Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_2

    iget-object v2, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    iget-object p1, p1, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-static {v2, p1}, Ljava/util/Objects;->equals(Ljava/lang/Object;Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_2

    return v0

    :cond_2
    :goto_0
    return v1
.end method

.method public getPoint()Lcom/android/helper/device/Point;
    .locals 1

    .line 19
    iget-object v0, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    return-object v0
.end method

.method public getScreenSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 23
    iget-object v0, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public hashCode()I
    .locals 4

    .line 53
    iget-object v0, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    const/4 v2, 0x2

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object v0, v2, v3

    const/4 v0, 0x1

    aput-object v1, v2, v0

    invoke-static {v2}, Ljava/util/Objects;->hash([Ljava/lang/Object;)I

    move-result v0

    return v0
.end method

.method public rotate(I)Lcom/android/helper/device/Position;
    .locals 4

    const/4 v0, 0x1

    if-eq p1, v0, :cond_2

    const/4 v0, 0x2

    if-eq p1, v0, :cond_1

    const/4 v0, 0x3

    if-eq p1, v0, :cond_0

    return-object p0

    .line 33
    :cond_0
    new-instance p1, Lcom/android/helper/device/Position;

    new-instance v0, Lcom/android/helper/device/Point;

    iget-object v1, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v1}, Lcom/android/helper/device/Point;->getY()I

    move-result v1

    iget-object v2, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v2}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v2

    iget-object v3, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v3}, Lcom/android/helper/device/Point;->getX()I

    move-result v3

    sub-int/2addr v2, v3

    invoke-direct {v0, v1, v2}, Lcom/android/helper/device/Point;-><init>(II)V

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1}, Lcom/android/helper/device/Size;->rotate()Lcom/android/helper/device/Size;

    move-result-object v1

    invoke-direct {p1, v0, v1}, Lcom/android/helper/device/Position;-><init>(Lcom/android/helper/device/Point;Lcom/android/helper/device/Size;)V

    return-object p1

    .line 31
    :cond_1
    new-instance p1, Lcom/android/helper/device/Position;

    new-instance v0, Lcom/android/helper/device/Point;

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v1

    iget-object v2, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v2}, Lcom/android/helper/device/Point;->getX()I

    move-result v2

    sub-int/2addr v1, v2

    iget-object v2, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v2}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v2

    iget-object v3, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v3}, Lcom/android/helper/device/Point;->getY()I

    move-result v3

    sub-int/2addr v2, v3

    invoke-direct {v0, v1, v2}, Lcom/android/helper/device/Point;-><init>(II)V

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-direct {p1, v0, v1}, Lcom/android/helper/device/Position;-><init>(Lcom/android/helper/device/Point;Lcom/android/helper/device/Size;)V

    return-object p1

    .line 29
    :cond_2
    new-instance p1, Lcom/android/helper/device/Position;

    new-instance v0, Lcom/android/helper/device/Point;

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v1

    iget-object v2, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v2}, Lcom/android/helper/device/Point;->getY()I

    move-result v2

    sub-int/2addr v1, v2

    iget-object v2, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v2}, Lcom/android/helper/device/Point;->getX()I

    move-result v2

    invoke-direct {v0, v1, v2}, Lcom/android/helper/device/Point;-><init>(II)V

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v1}, Lcom/android/helper/device/Size;->rotate()Lcom/android/helper/device/Size;

    move-result-object v1

    invoke-direct {p1, v0, v1}, Lcom/android/helper/device/Position;-><init>(Lcom/android/helper/device/Point;Lcom/android/helper/device/Size;)V

    return-object p1
.end method

.method public toString()Ljava/lang/String;
    .locals 2

    .line 58
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Position{point="

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget-object v1, p0, Lcom/android/helper/device/Position;->point:Lcom/android/helper/device/Point;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v1, ", screenSize="

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-object v1, p0, Lcom/android/helper/device/Position;->screenSize:Lcom/android/helper/device/Size;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const/16 v1, 0x7d

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
