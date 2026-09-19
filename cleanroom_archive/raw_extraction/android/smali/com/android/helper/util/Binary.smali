.class public final Lcom/android/helper/util/Binary;
.super Ljava/lang/Object;
.source "Binary.java"


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 4
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static i16FixedPointToFloat(S)F
    .locals 1

    const/16 v0, 0x7fff

    if-ne p0, v0, :cond_0

    const/high16 p0, 0x3f800000    # 1.0f

    return p0

    :cond_0
    int-to-float p0, p0

    const/high16 v0, 0x47000000    # 32768.0f

    div-float/2addr p0, v0

    return p0
.end method

.method public static toUnsigned(B)I
    .locals 0

    and-int/lit16 p0, p0, 0xff

    return p0
.end method

.method public static toUnsigned(S)I
    .locals 1

    const v0, 0xffff

    and-int/2addr p0, v0

    return p0
.end method

.method public static u16FixedPointToFloat(S)F
    .locals 1

    .line 23
    invoke-static {p0}, Lcom/android/helper/util/Binary;->toUnsigned(S)I

    move-result p0

    const v0, 0xffff

    if-ne p0, v0, :cond_0

    const/high16 p0, 0x3f800000    # 1.0f

    return p0

    :cond_0
    int-to-float p0, p0

    const/high16 v0, 0x47800000    # 65536.0f

    div-float/2addr p0, v0

    return p0
.end method
