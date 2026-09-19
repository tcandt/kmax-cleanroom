.class public Lcom/android/helper/util/AffineMatrix;
.super Ljava/lang/Object;
.source "AffineMatrix.java"


# static fields
.field public static final IDENTITY:Lcom/android/helper/util/AffineMatrix;


# instance fields
.field private final a:D

.field private final b:D

.field private final c:D

.field private final d:D

.field private final e:D

.field private final f:D


# direct methods
.method static constructor <clinit>()V
    .locals 13

    .line 31
    new-instance v0, Lcom/android/helper/util/AffineMatrix;

    const-wide/16 v9, 0x0

    const-wide/16 v11, 0x0

    const-wide/high16 v1, 0x3ff0000000000000L    # 1.0

    const-wide/16 v3, 0x0

    const-wide/16 v5, 0x0

    const-wide/high16 v7, 0x3ff0000000000000L    # 1.0

    invoke-direct/range {v0 .. v12}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    sput-object v0, Lcom/android/helper/util/AffineMatrix;->IDENTITY:Lcom/android/helper/util/AffineMatrix;

    return-void
.end method

.method public constructor <init>(DDDDDD)V
    .locals 0

    .line 42
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 43
    iput-wide p1, p0, Lcom/android/helper/util/AffineMatrix;->a:D

    .line 44
    iput-wide p3, p0, Lcom/android/helper/util/AffineMatrix;->b:D

    .line 45
    iput-wide p5, p0, Lcom/android/helper/util/AffineMatrix;->c:D

    .line 46
    iput-wide p7, p0, Lcom/android/helper/util/AffineMatrix;->d:D

    .line 47
    iput-wide p9, p0, Lcom/android/helper/util/AffineMatrix;->e:D

    .line 48
    iput-wide p11, p0, Lcom/android/helper/util/AffineMatrix;->f:D

    return-void
.end method

.method public static hflip()Lcom/android/helper/util/AffineMatrix;
    .locals 13

    .line 300
    new-instance v0, Lcom/android/helper/util/AffineMatrix;

    const-wide/high16 v9, 0x3ff0000000000000L    # 1.0

    const-wide/16 v11, 0x0

    const-wide/high16 v1, -0x4010000000000000L    # -1.0

    const-wide/16 v3, 0x0

    const-wide/16 v5, 0x0

    const-wide/high16 v7, 0x3ff0000000000000L    # 1.0

    invoke-direct/range {v0 .. v12}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v0
.end method

.method public static varargs multiplyAll([Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;
    .locals 4

    .line 123
    array-length v0, p0

    const/4 v1, 0x0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v0, :cond_1

    aget-object v3, p0, v2

    if-nez v1, :cond_0

    move-object v1, v3

    goto :goto_1

    .line 127
    :cond_0
    invoke-virtual {v1, v3}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v1

    :goto_1
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_1
    return-object v1
.end method

.method public static ndcFromPixels(Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;
    .locals 17

    .line 63
    invoke-virtual/range {p0 .. p0}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    int-to-double v0, v0

    .line 64
    invoke-virtual/range {p0 .. p0}, Lcom/android/helper/device/Size;->getHeight()I

    move-result v2

    int-to-double v2, v2

    .line 65
    new-instance v4, Lcom/android/helper/util/AffineMatrix;

    const-wide/high16 v5, 0x3ff0000000000000L    # 1.0

    div-double/2addr v5, v0

    const-wide/high16 v0, -0x4010000000000000L    # -1.0

    div-double v11, v0, v2

    const-wide/16 v13, 0x0

    const-wide/high16 v15, 0x3ff0000000000000L    # 1.0

    const-wide/16 v7, 0x0

    const-wide/16 v9, 0x0

    invoke-direct/range {v4 .. v16}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v4
.end method

.method public static ndcToPixels(Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;
    .locals 14

    .line 75
    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    int-to-double v2, v0

    .line 76
    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p0

    int-to-double v12, p0

    .line 77
    new-instance v1, Lcom/android/helper/util/AffineMatrix;

    neg-double v8, v12

    const-wide/16 v10, 0x0

    const-wide/16 v4, 0x0

    const-wide/16 v6, 0x0

    invoke-direct/range {v1 .. v13}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v1
.end method

.method public static reframe(DDDD)Lcom/android/helper/util/AffineMatrix;
    .locals 3

    const-wide/16 v0, 0x0

    cmpl-double v2, p4, v0

    if-eqz v2, :cond_0

    cmpl-double v2, p6, v0

    if-eqz v2, :cond_0

    const-wide/high16 v0, 0x3ff0000000000000L    # 1.0

    div-double p4, v0, p4

    div-double/2addr v0, p6

    .line 267
    invoke-static {p4, p5, v0, v1}, Lcom/android/helper/util/AffineMatrix;->scale(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object p4

    neg-double p0, p0

    neg-double p2, p2

    invoke-static {p0, p1, p2, p3}, Lcom/android/helper/util/AffineMatrix;->translate(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object p0

    invoke-virtual {p4, p0}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p0

    return-object p0

    .line 265
    :cond_0
    new-instance p0, Ljava/lang/IllegalArgumentException;

    new-instance p1, Ljava/lang/StringBuilder;

    const-string p2, "Cannot reframe to an empty area: "

    invoke-direct {p1, p2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1, p4, p5}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    const-string p2, "x"

    invoke-virtual {p1, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1, p6, p7}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p0, p1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method public static rotate(D)Lcom/android/helper/util/AffineMatrix;
    .locals 13

    .line 319
    invoke-static {p0, p1}, Ljava/lang/Math;->toRadians(D)D

    move-result-wide p0

    .line 320
    invoke-static {p0, p1}, Ljava/lang/Math;->cos(D)D

    move-result-wide v1

    .line 321
    invoke-static {p0, p1}, Ljava/lang/Math;->sin(D)D

    move-result-wide v3

    .line 322
    new-instance v0, Lcom/android/helper/util/AffineMatrix;

    neg-double v5, v3

    const-wide/16 v9, 0x0

    const-wide/16 v11, 0x0

    move-wide v7, v1

    invoke-direct/range {v0 .. v12}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v0
.end method

.method public static rotateOrtho(I)Lcom/android/helper/util/AffineMatrix;
    .locals 15

    if-eqz p0, :cond_3

    const/4 v0, 0x1

    if-eq p0, v0, :cond_2

    const/4 v0, 0x2

    if-eq p0, v0, :cond_1

    const/4 v0, 0x3

    if-ne p0, v0, :cond_0

    .line 288
    new-instance v1, Lcom/android/helper/util/AffineMatrix;

    const-wide/16 v10, 0x0

    const-wide/high16 v12, 0x3ff0000000000000L    # 1.0

    const-wide/16 v2, 0x0

    const-wide/high16 v4, -0x4010000000000000L    # -1.0

    const-wide/high16 v6, 0x3ff0000000000000L    # 1.0

    const-wide/16 v8, 0x0

    invoke-direct/range {v1 .. v13}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v1

    .line 290
    :cond_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid rotation: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 285
    :cond_1
    new-instance v1, Lcom/android/helper/util/AffineMatrix;

    const-wide/high16 v10, 0x3ff0000000000000L    # 1.0

    const-wide/high16 v12, 0x3ff0000000000000L    # 1.0

    const-wide/high16 v2, -0x4010000000000000L    # -1.0

    const-wide/16 v4, 0x0

    const-wide/16 v6, 0x0

    const-wide/high16 v8, -0x4010000000000000L    # -1.0

    invoke-direct/range {v1 .. v13}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v1

    .line 282
    :cond_2
    new-instance v2, Lcom/android/helper/util/AffineMatrix;

    const-wide/high16 v11, 0x3ff0000000000000L    # 1.0

    const-wide/16 v13, 0x0

    const-wide/16 v3, 0x0

    const-wide/high16 v5, 0x3ff0000000000000L    # 1.0

    const-wide/high16 v7, -0x4010000000000000L    # -1.0

    const-wide/16 v9, 0x0

    invoke-direct/range {v2 .. v14}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v2

    .line 279
    :cond_3
    sget-object p0, Lcom/android/helper/util/AffineMatrix;->IDENTITY:Lcom/android/helper/util/AffineMatrix;

    return-object p0
.end method

.method public static scale(DD)Lcom/android/helper/util/AffineMatrix;
    .locals 13

    .line 236
    new-instance v0, Lcom/android/helper/util/AffineMatrix;

    const-wide/16 v9, 0x0

    const-wide/16 v11, 0x0

    const-wide/16 v3, 0x0

    const-wide/16 v5, 0x0

    move-wide v1, p0

    move-wide v7, p2

    invoke-direct/range {v0 .. v12}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v0
.end method

.method public static scale(Lcom/android/helper/device/Size;Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;
    .locals 4

    .line 247
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    int-to-double v0, v0

    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v2

    int-to-double v2, v2

    div-double/2addr v0, v2

    .line 248
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p1

    int-to-double v2, p1

    invoke-virtual {p0}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p0

    int-to-double p0, p0

    div-double/2addr v2, p0

    .line 249
    invoke-static {v0, v1, v2, v3}, Lcom/android/helper/util/AffineMatrix;->scale(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object p0

    return-object p0
.end method

.method public static translate(DD)Lcom/android/helper/util/AffineMatrix;
    .locals 13

    .line 225
    new-instance v0, Lcom/android/helper/util/AffineMatrix;

    const-wide/16 v5, 0x0

    const-wide/high16 v7, 0x3ff0000000000000L    # 1.0

    const-wide/high16 v1, 0x3ff0000000000000L    # 1.0

    const-wide/16 v3, 0x0

    move-wide v9, p0

    move-wide v11, p2

    invoke-direct/range {v0 .. v12}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v0
.end method

.method public static vflip()Lcom/android/helper/util/AffineMatrix;
    .locals 13

    .line 309
    new-instance v0, Lcom/android/helper/util/AffineMatrix;

    const-wide/16 v9, 0x0

    const-wide/high16 v11, 0x3ff0000000000000L    # 1.0

    const-wide/high16 v1, 0x3ff0000000000000L    # 1.0

    const-wide/16 v3, 0x0

    const-wide/16 v5, 0x0

    const-wide/high16 v7, -0x4010000000000000L    # -1.0

    invoke-direct/range {v0 .. v12}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v0
.end method


# virtual methods
.method public apply(Lcom/android/helper/device/Point;)Lcom/android/helper/device/Point;
    .locals 9

    .line 87
    invoke-virtual {p1}, Lcom/android/helper/device/Point;->getX()I

    move-result v0

    .line 88
    invoke-virtual {p1}, Lcom/android/helper/device/Point;->getY()I

    move-result p1

    .line 89
    iget-wide v1, p0, Lcom/android/helper/util/AffineMatrix;->a:D

    int-to-double v3, v0

    mul-double v1, v1, v3

    iget-wide v5, p0, Lcom/android/helper/util/AffineMatrix;->c:D

    int-to-double v7, p1

    mul-double v5, v5, v7

    add-double/2addr v1, v5

    iget-wide v5, p0, Lcom/android/helper/util/AffineMatrix;->e:D

    add-double/2addr v1, v5

    double-to-int p1, v1

    .line 90
    iget-wide v0, p0, Lcom/android/helper/util/AffineMatrix;->b:D

    mul-double v0, v0, v3

    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->d:D

    mul-double v2, v2, v7

    add-double/2addr v0, v2

    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->f:D

    add-double/2addr v0, v2

    double-to-int v0, v0

    .line 91
    new-instance v1, Lcom/android/helper/device/Point;

    invoke-direct {v1, p1, v0}, Lcom/android/helper/device/Point;-><init>(II)V

    return-object v1
.end method

.method public fromCenter()Lcom/android/helper/util/AffineMatrix;
    .locals 3

    const-wide/high16 v0, 0x3fe0000000000000L    # 0.5

    .line 193
    invoke-static {v0, v1, v0, v1}, Lcom/android/helper/util/AffineMatrix;->translate(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    invoke-virtual {v0, p0}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    const-wide/high16 v1, -0x4020000000000000L    # -0.5

    invoke-static {v1, v2, v1, v2}, Lcom/android/helper/util/AffineMatrix;->translate(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object v1

    invoke-virtual {v0, v1}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v0

    return-object v0
.end method

.method public invert()Lcom/android/helper/util/AffineMatrix;
    .locals 23

    move-object/from16 v0, p0

    .line 171
    iget-wide v1, v0, Lcom/android/helper/util/AffineMatrix;->a:D

    iget-wide v3, v0, Lcom/android/helper/util/AffineMatrix;->d:D

    mul-double v5, v1, v3

    iget-wide v7, v0, Lcom/android/helper/util/AffineMatrix;->c:D

    iget-wide v9, v0, Lcom/android/helper/util/AffineMatrix;->b:D

    mul-double v11, v7, v9

    sub-double/2addr v5, v11

    const-wide/16 v11, 0x0

    cmpl-double v13, v5, v11

    if-nez v13, :cond_0

    const/4 v1, 0x0

    return-object v1

    :cond_0
    move-wide v11, v3

    div-double v3, v11, v5

    neg-double v13, v9

    div-double/2addr v13, v5

    move-wide v15, v1

    neg-double v1, v7

    div-double/2addr v1, v5

    move-wide/from16 v17, v9

    div-double v9, v15, v5

    move-wide/from16 v19, v1

    .line 181
    iget-wide v1, v0, Lcom/android/helper/util/AffineMatrix;->f:D

    mul-double v7, v7, v1

    move-wide/from16 v21, v1

    iget-wide v1, v0, Lcom/android/helper/util/AffineMatrix;->e:D

    mul-double v11, v11, v1

    sub-double/2addr v7, v11

    div-double v11, v7, v5

    mul-double v1, v1, v17

    mul-double v7, v15, v21

    sub-double/2addr v1, v7

    div-double/2addr v1, v5

    move-wide v5, v13

    move-wide v13, v1

    .line 184
    new-instance v2, Lcom/android/helper/util/AffineMatrix;

    move-wide/from16 v7, v19

    invoke-direct/range {v2 .. v14}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v2
.end method

.method public multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;
    .locals 27

    move-object/from16 v0, p0

    move-object/from16 v1, p1

    if-nez v1, :cond_0

    return-object v0

    .line 106
    :cond_0
    iget-wide v2, v0, Lcom/android/helper/util/AffineMatrix;->a:D

    iget-wide v4, v1, Lcom/android/helper/util/AffineMatrix;->a:D

    mul-double v6, v2, v4

    iget-wide v8, v0, Lcom/android/helper/util/AffineMatrix;->c:D

    iget-wide v10, v1, Lcom/android/helper/util/AffineMatrix;->b:D

    mul-double v12, v8, v10

    add-double v15, v6, v12

    .line 107
    iget-wide v6, v0, Lcom/android/helper/util/AffineMatrix;->b:D

    mul-double v4, v4, v6

    iget-wide v12, v0, Lcom/android/helper/util/AffineMatrix;->d:D

    mul-double v10, v10, v12

    add-double v17, v4, v10

    .line 108
    iget-wide v4, v1, Lcom/android/helper/util/AffineMatrix;->c:D

    mul-double v10, v2, v4

    move-wide/from16 v19, v2

    iget-wide v2, v1, Lcom/android/helper/util/AffineMatrix;->d:D

    mul-double v21, v8, v2

    add-double v10, v10, v21

    mul-double v4, v4, v6

    mul-double v2, v2, v12

    add-double v21, v4, v2

    .line 110
    iget-wide v2, v1, Lcom/android/helper/util/AffineMatrix;->e:D

    mul-double v4, v19, v2

    move-wide/from16 v19, v2

    iget-wide v1, v1, Lcom/android/helper/util/AffineMatrix;->f:D

    mul-double v8, v8, v1

    add-double/2addr v4, v8

    iget-wide v8, v0, Lcom/android/helper/util/AffineMatrix;->e:D

    add-double v23, v4, v8

    mul-double v6, v6, v19

    mul-double v12, v12, v1

    add-double/2addr v6, v12

    .line 111
    iget-wide v1, v0, Lcom/android/helper/util/AffineMatrix;->f:D

    add-double v25, v6, v1

    .line 112
    new-instance v14, Lcom/android/helper/util/AffineMatrix;

    move-wide/from16 v19, v10

    invoke-direct/range {v14 .. v26}, Lcom/android/helper/util/AffineMatrix;-><init>(DDDDDD)V

    return-object v14
.end method

.method public to4x4([F)V
    .locals 5

    .line 334
    iget-wide v0, p0, Lcom/android/helper/util/AffineMatrix;->a:D

    double-to-float v0, v0

    const/4 v1, 0x0

    aput v0, p1, v1

    .line 335
    iget-wide v0, p0, Lcom/android/helper/util/AffineMatrix;->b:D

    double-to-float v0, v0

    const/4 v1, 0x1

    aput v0, p1, v1

    const/4 v0, 0x2

    const/4 v1, 0x0

    .line 336
    aput v1, p1, v0

    const/4 v0, 0x3

    .line 337
    aput v1, p1, v0

    .line 340
    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->c:D

    double-to-float v0, v2

    const/4 v2, 0x4

    aput v0, p1, v2

    .line 341
    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->d:D

    double-to-float v0, v2

    const/4 v2, 0x5

    aput v0, p1, v2

    const/4 v0, 0x6

    .line 342
    aput v1, p1, v0

    const/4 v0, 0x7

    .line 343
    aput v1, p1, v0

    const/16 v0, 0x8

    .line 346
    aput v1, p1, v0

    const/16 v0, 0x9

    .line 347
    aput v1, p1, v0

    const/16 v0, 0xa

    const/high16 v2, 0x3f800000    # 1.0f

    .line 348
    aput v2, p1, v0

    const/16 v0, 0xb

    .line 349
    aput v1, p1, v0

    .line 352
    iget-wide v3, p0, Lcom/android/helper/util/AffineMatrix;->e:D

    double-to-float v0, v3

    const/16 v3, 0xc

    aput v0, p1, v3

    .line 353
    iget-wide v3, p0, Lcom/android/helper/util/AffineMatrix;->f:D

    double-to-float v0, v3

    const/16 v3, 0xd

    aput v0, p1, v3

    const/16 v0, 0xe

    .line 354
    aput v1, p1, v0

    const/16 v0, 0xf

    .line 355
    aput v2, p1, v0

    return-void
.end method

.method public to4x4()[F
    .locals 1

    const/16 v0, 0x10

    .line 364
    new-array v0, v0, [F

    .line 365
    invoke-virtual {p0, v0}, Lcom/android/helper/util/AffineMatrix;->to4x4([F)V

    return-object v0
.end method

.method public toString()Ljava/lang/String;
    .locals 4

    .line 53
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "["

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget-wide v1, p0, Lcom/android/helper/util/AffineMatrix;->a:D

    invoke-virtual {v0, v1, v2}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    const-string v1, ", "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->c:D

    invoke-virtual {v0, v2, v3}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->e:D

    invoke-virtual {v0, v2, v3}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    const-string v2, "; "

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->b:D

    invoke-virtual {v0, v2, v3}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-wide v2, p0, Lcom/android/helper/util/AffineMatrix;->d:D

    invoke-virtual {v0, v2, v3}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    iget-wide v1, p0, Lcom/android/helper/util/AffineMatrix;->f:D

    invoke-virtual {v0, v1, v2}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;

    const-string v1, "]"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public withAspectRatio(D)Lcom/android/helper/util/AffineMatrix;
    .locals 4

    const-wide/high16 v0, 0x3ff0000000000000L    # 1.0

    div-double v2, v0, p1

    .line 203
    invoke-static {v2, v3, v0, v1}, Lcom/android/helper/util/AffineMatrix;->scale(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object v2

    invoke-virtual {v2, p0}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object v2

    invoke-static {p1, p2, v0, v1}, Lcom/android/helper/util/AffineMatrix;->scale(DD)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    invoke-virtual {v2, p1}, Lcom/android/helper/util/AffineMatrix;->multiply(Lcom/android/helper/util/AffineMatrix;)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    return-object p1
.end method

.method public withAspectRatio(Lcom/android/helper/device/Size;)Lcom/android/helper/util/AffineMatrix;
    .locals 4

    .line 213
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v0

    int-to-double v0, v0

    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p1

    int-to-double v2, p1

    div-double/2addr v0, v2

    .line 214
    invoke-virtual {p0, v0, v1}, Lcom/android/helper/util/AffineMatrix;->withAspectRatio(D)Lcom/android/helper/util/AffineMatrix;

    move-result-object p1

    return-object p1
.end method
