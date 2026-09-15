.class public final Lcom/android/helper/device/Size;
.super Ljava/lang/Object;
.source "Size.java"


# static fields
.field static final synthetic $assertionsDisabled:Z


# instance fields
.field private final height:I

.field private final width:I


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>(II)V
    .locals 0

    .line 11
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 12
    iput p1, p0, Lcom/android/helper/device/Size;->width:I

    .line 13
    iput p2, p0, Lcom/android/helper/device/Size;->height:I

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

    .line 96
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v2

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v3

    if-eq v2, v3, :cond_1

    goto :goto_0

    .line 99
    :cond_1
    check-cast p1, Lcom/android/helper/device/Size;

    .line 100
    iget v2, p0, Lcom/android/helper/device/Size;->width:I

    iget v3, p1, Lcom/android/helper/device/Size;->width:I

    if-ne v2, v3, :cond_2

    iget v2, p0, Lcom/android/helper/device/Size;->height:I

    iget p1, p1, Lcom/android/helper/device/Size;->height:I

    if-ne v2, p1, :cond_2

    return v0

    :cond_2
    :goto_0
    return v1
.end method

.method public getHeight()I
    .locals 1

    .line 21
    iget v0, p0, Lcom/android/helper/device/Size;->height:I

    return v0
.end method

.method public getMax()I
    .locals 2

    .line 25
    iget v0, p0, Lcom/android/helper/device/Size;->width:I

    iget v1, p0, Lcom/android/helper/device/Size;->height:I

    invoke-static {v0, v1}, Ljava/lang/Math;->max(II)I

    move-result v0

    return v0
.end method

.method public getWidth()I
    .locals 1

    .line 17
    iget v0, p0, Lcom/android/helper/device/Size;->width:I

    return v0
.end method

.method public hashCode()I
    .locals 4

    .line 105
    iget v0, p0, Lcom/android/helper/device/Size;->width:I

    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v0

    iget v1, p0, Lcom/android/helper/device/Size;->height:I

    invoke-static {v1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

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

.method public isMultipleOf8()Z
    .locals 1

    .line 84
    iget v0, p0, Lcom/android/helper/device/Size;->width:I

    and-int/lit8 v0, v0, 0x7

    if-nez v0, :cond_0

    iget v0, p0, Lcom/android/helper/device/Size;->height:I

    and-int/lit8 v0, v0, 0x7

    if-nez v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method

.method public limit(I)Lcom/android/helper/device/Size;
    .locals 4

    if-nez p1, :cond_0

    goto :goto_2

    .line 41
    :cond_0
    iget v0, p0, Lcom/android/helper/device/Size;->height:I

    iget v1, p0, Lcom/android/helper/device/Size;->width:I

    if-le v0, v1, :cond_1

    const/4 v2, 0x1

    goto :goto_0

    :cond_1
    const/4 v2, 0x0

    :goto_0
    if-eqz v2, :cond_2

    move v3, v0

    goto :goto_1

    :cond_2
    move v3, v1

    :goto_1
    if-gt v3, p1, :cond_3

    :goto_2
    return-object p0

    :cond_3
    if-eqz v2, :cond_4

    move v0, v1

    :cond_4
    mul-int v0, v0, p1

    .line 50
    div-int/2addr v0, v3

    if-eqz v2, :cond_5

    move v1, v0

    goto :goto_3

    :cond_5
    move v1, p1

    :goto_3
    if-eqz v2, :cond_6

    goto :goto_4

    :cond_6
    move p1, v0

    .line 54
    :goto_4
    new-instance v0, Lcom/android/helper/device/Size;

    invoke-direct {v0, v1, p1}, Lcom/android/helper/device/Size;-><init>(II)V

    return-object v0
.end method

.method public rotate()Lcom/android/helper/device/Size;
    .locals 3

    .line 29
    new-instance v0, Lcom/android/helper/device/Size;

    iget v1, p0, Lcom/android/helper/device/Size;->height:I

    iget v2, p0, Lcom/android/helper/device/Size;->width:I

    invoke-direct {v0, v1, v2}, Lcom/android/helper/device/Size;-><init>(II)V

    return-object v0
.end method

.method public round8()Lcom/android/helper/device/Size;
    .locals 4

    .line 63
    invoke-virtual {p0}, Lcom/android/helper/device/Size;->isMultipleOf8()Z

    move-result v0

    if-eqz v0, :cond_0

    return-object p0

    .line 68
    :cond_0
    iget v0, p0, Lcom/android/helper/device/Size;->height:I

    iget v1, p0, Lcom/android/helper/device/Size;->width:I

    if-le v0, v1, :cond_1

    const/4 v2, 0x1

    goto :goto_0

    :cond_1
    const/4 v2, 0x0

    :goto_0
    if-eqz v2, :cond_2

    move v3, v0

    goto :goto_1

    :cond_2
    move v3, v1

    :goto_1
    if-eqz v2, :cond_3

    move v0, v1

    :cond_3
    and-int/lit8 v1, v3, -0x8

    add-int/lit8 v0, v0, 0x4

    and-int/lit8 v0, v0, -0x8

    if-le v0, v1, :cond_4

    move v0, v1

    :cond_4
    if-eqz v2, :cond_5

    move v3, v0

    goto :goto_2

    :cond_5
    move v3, v1

    :goto_2
    if-eqz v2, :cond_6

    goto :goto_3

    :cond_6
    move v1, v0

    .line 80
    :goto_3
    new-instance v0, Lcom/android/helper/device/Size;

    invoke-direct {v0, v3, v1}, Lcom/android/helper/device/Size;-><init>(II)V

    return-object v0
.end method

.method public toRect()Landroid/graphics/Rect;
    .locals 4

    .line 88
    new-instance v0, Landroid/graphics/Rect;

    iget v1, p0, Lcom/android/helper/device/Size;->width:I

    iget v2, p0, Lcom/android/helper/device/Size;->height:I

    const/4 v3, 0x0

    invoke-direct {v0, v3, v3, v1, v2}, Landroid/graphics/Rect;-><init>(IIII)V

    return-object v0
.end method

.method public toString()Ljava/lang/String;
    .locals 2

    .line 110
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    iget v1, p0, Lcom/android/helper/device/Size;->width:I

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, "x"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget v1, p0, Lcom/android/helper/device/Size;->height:I

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
