.class public final Lcom/android/helper/video/CameraAspectRatio;
.super Ljava/lang/Object;
.source "CameraAspectRatio.java"


# static fields
.field private static final SENSOR:F = -1.0f


# instance fields
.field private ar:F


# direct methods
.method private constructor <init>(F)V
    .locals 0

    .line 8
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 9
    iput p1, p0, Lcom/android/helper/video/CameraAspectRatio;->ar:F

    return-void
.end method

.method public static fromFloat(F)Lcom/android/helper/video/CameraAspectRatio;
    .locals 3

    const/4 v0, 0x0

    cmpg-float v0, p0, v0

    if-ltz v0, :cond_0

    .line 16
    new-instance v0, Lcom/android/helper/video/CameraAspectRatio;

    invoke-direct {v0, p0}, Lcom/android/helper/video/CameraAspectRatio;-><init>(F)V

    return-object v0

    .line 14
    :cond_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid aspect ratio: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(F)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method public static fromFraction(II)Lcom/android/helper/video/CameraAspectRatio;
    .locals 3

    if-lez p0, :cond_0

    if-lez p1, :cond_0

    .line 23
    new-instance v0, Lcom/android/helper/video/CameraAspectRatio;

    int-to-float p0, p0

    int-to-float p1, p1

    div-float/2addr p0, p1

    invoke-direct {v0, p0}, Lcom/android/helper/video/CameraAspectRatio;-><init>(F)V

    return-object v0

    .line 21
    :cond_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid aspect ratio: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p0, ":"

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method public static sensorAspectRatio()Lcom/android/helper/video/CameraAspectRatio;
    .locals 2

    .line 27
    new-instance v0, Lcom/android/helper/video/CameraAspectRatio;

    const/high16 v1, -0x40800000    # -1.0f

    invoke-direct {v0, v1}, Lcom/android/helper/video/CameraAspectRatio;-><init>(F)V

    return-object v0
.end method


# virtual methods
.method public getAspectRatio()F
    .locals 1

    .line 35
    iget v0, p0, Lcom/android/helper/video/CameraAspectRatio;->ar:F

    return v0
.end method

.method public isSensor()Z
    .locals 2

    .line 31
    iget v0, p0, Lcom/android/helper/video/CameraAspectRatio;->ar:F

    const/high16 v1, -0x40800000    # -1.0f

    cmpl-float v0, v0, v1

    if-nez v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method
