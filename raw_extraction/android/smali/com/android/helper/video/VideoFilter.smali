.class public Lcom/android/helper/video/VideoFilter;
.super Ljava/lang/Object;
.source "VideoFilter.java"


# instance fields
.field private size:Lcom/android/helper/device/Size;

.field private transform:Lcom/android/helper/util/AffineMatrix;


# direct methods
.method public constructor <init>(Lcom/android/helper/device/Size;)V
    .locals 0

    .line 14
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 15
    iput-object p1, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    return-void
.end method

.method private static transposeRect(Landroid/graphics/Rect;)Landroid/graphics/Rect;
    .locals 4

    .line 47
    new-instance v0, Landroid/graphics/Rect;

    iget v1, p0, Landroid/graphics/Rect;->top:I

    iget v2, p0, Landroid/graphics/Rect;->left:I

    iget v3, p0, Landroid/graphics/Rect;->bottom:I

    iget p0, p0, Landroid/graphics/Rect;->right:I

    invoke-direct {v0, v1, v2, v3, p0}, Landroid/graphics/Rect;-><init>(IIII)V

    return-object v0
.end method


# virtual methods
.method public addAngle(D)V
    .locals 3

    const-wide/16 v0, 0x0

    cmpl-double v2, p1, v0

    if-nez v2, :cond_0

    return-void

    :cond_0
    neg-double p1, p1

    .line 104
    invoke-static {p1, p2}, Lcom/android/helper/util/AffineMatrix;->rotate(D)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    iget-object p2, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    invoke-virtual {p1, p2}, Lcom/android/helper/util/AffineMatrix;->withAspectRatio(Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    invoke-virtual {p1}, Lcom/android/helper/util/AffineMatrix;->fromCenter()Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    iget-object p2, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-virtual {p1, p2}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    return-void
.end method

.method public addCrop(Landroid/graphics/Rect;Z)V
    .locals 16

    move-object/from16 v0, p0

    if-eqz p2, :cond_0

    .line 52
    invoke-static/range {p1 .. p1}, Lcom/android/helper/video/VideoFilter;->transposeRect(Landroid/graphics/Rect;)Landroid/graphics/Rect;

    move-result-object v1

    goto :goto_0

    :cond_0
    move-object/from16 v1, p1

    .line 55
    :goto_0
    iget-object v2, v0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    invoke-virtual {v2}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v2

    int-to-double v2, v2

    .line 56
    iget-object v4, v0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    invoke-virtual {v4}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v4

    int-to-double v4, v4

    .line 58
    iget v6, v1, Landroid/graphics/Rect;->left:I

    if-ltz v6, :cond_1

    iget v6, v1, Landroid/graphics/Rect;->top:I

    if-ltz v6, :cond_1

    iget v6, v1, Landroid/graphics/Rect;->right:I

    int-to-double v6, v6

    cmpl-double v8, v6, v2

    if-gtz v8, :cond_1

    iget v6, v1, Landroid/graphics/Rect;->bottom:I

    int-to-double v6, v6

    cmpl-double v8, v6, v4

    if-gtz v8, :cond_1

    .line 62
    iget v6, v1, Landroid/graphics/Rect;->left:I

    int-to-double v6, v6

    div-double v8, v6, v2

    .line 63
    iget v6, v1, Landroid/graphics/Rect;->bottom:I

    int-to-double v6, v6

    div-double/2addr v6, v4

    const-wide/high16 v10, 0x3ff0000000000000L    # 1.0

    sub-double/2addr v10, v6

    .line 64
    invoke-virtual {v1}, Landroid/graphics/Rect;->width()I

    move-result v6

    int-to-double v6, v6

    div-double v12, v6, v2

    .line 65
    invoke-virtual {v1}, Landroid/graphics/Rect;->height()I

    move-result v2

    int-to-double v2, v2

    div-double v14, v2, v4

    .line 67
    invoke-static/range {v8 .. v15}, Lcom/android/helper/util/AffineMatrix;->reframe(DDDD)Lcom/android/helper/util/AffineMatrix;

    move-result-object v2

    iget-object v3, v0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-virtual {v2, v3}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v2

    iput-object v2, v0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    .line 68
    new-instance v2, Lcom/android/helper/device/Size;

    invoke-virtual {v1}, Landroid/graphics/Rect;->width()I

    move-result v3

    invoke-virtual {v1}, Landroid/graphics/Rect;->height()I

    move-result v1

    invoke-direct {v2, v3, v1}, Lcom/android/helper/device/Size;-><init>(II)V

    iput-object v2, v0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    return-void

    .line 59
    :cond_1
    new-instance v2, Ljava/lang/IllegalArgumentException;

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "Crop "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v1, " exceeds the input area ("

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-object v1, v0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v1, ")"

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v2, v1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v2
.end method

.method public addOrientation(IZLcom/android/helper/device/Orientation;)V
    .locals 0

    if-eqz p2, :cond_0

    rsub-int/lit8 p1, p1, 0x4

    .line 93
    rem-int/lit8 p1, p1, 0x4

    .line 94
    invoke-virtual {p0, p1}, Lcom/android/helper/video/VideoFilter;->addRotation(I)V

    .line 96
    :cond_0
    invoke-virtual {p0, p3}, Lcom/android/helper/video/VideoFilter;->addOrientation(Lcom/android/helper/device/Orientation;)V

    return-void
.end method

.method public addOrientation(Lcom/android/helper/device/Orientation;)V
    .locals 2

    .line 83
    invoke-virtual {p1}, Lcom/android/helper/device/Orientation;->isFlipped()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 84
    invoke-static {}, Lcom/android/helper/util/AffineMatrix;->hflip()Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    iget-object v1, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-virtual {v0, v1}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    .line 86
    :cond_0
    invoke-virtual {p1}, Lcom/android/helper/device/Orientation;->getRotation()I

    move-result p1

    rsub-int/lit8 p1, p1, 0x4

    rem-int/lit8 p1, p1, 0x4

    .line 87
    invoke-virtual {p0, p1}, Lcom/android/helper/video/VideoFilter;->addRotation(I)V

    return-void
.end method

.method public addResize(Lcom/android/helper/device/Size;)V
    .locals 1

    .line 108
    iget-object v0, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    invoke-virtual {v0, p1}, Lcom/android/helper/device/Size;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    return-void

    .line 112
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    if-nez v0, :cond_1

    .line 115
    sget-object v0, Lcom/android/helper/util/AffineMatrix;->IDENTITY:Lcom/android/helper/util/AffineMatrix;

    iput-object v0, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    .line 117
    :cond_1
    iput-object p1, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    return-void
.end method

.method public addRotation(I)V
    .locals 2

    if-nez p1, :cond_0

    goto :goto_0

    .line 76
    :cond_0
    invoke-static {p1}, Lcom/android/helper/util/AffineMatrix;->rotateOrtho(I)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    iget-object v1, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    invoke-virtual {v0, v1}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    .line 77
    rem-int/lit8 p1, p1, 0x2

    if-eqz p1, :cond_1

    .line 78
    iget-object p1, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    invoke-virtual {p1}, Lcom/android/helper/device/Size;->rotate()Lcom/android/helper/device/Size;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    :cond_1
    :goto_0
    return-void
.end method

.method public getInverseTransform()Lcom/android/helper/util/AffineMatrix;
    .locals 1

    .line 40
    iget-object v0, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    if-nez v0, :cond_0

    const/4 v0, 0x0

    return-object v0

    .line 43
    :cond_0
    invoke-virtual {v0}, Lcom/android/helper/util/AffineMatrix;->invert()Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    return-object v0
.end method

.method public getOutputSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 19
    iget-object v0, p0, Lcom/android/helper/video/VideoFilter;->size:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public getTransform()Lcom/android/helper/util/AffineMatrix;
    .locals 1

    .line 23
    iget-object v0, p0, Lcom/android/helper/video/VideoFilter;->transform:Lcom/android/helper/util/AffineMatrix;

    return-object v0
.end method
