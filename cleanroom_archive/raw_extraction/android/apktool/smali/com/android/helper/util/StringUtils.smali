.class public final Lcom/android/helper/util/StringUtils;
.super Ljava/lang/Object;
.source "StringUtils.java"


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 4
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static getUtf8TruncationIndex([BI)I
    .locals 2

    .line 9
    array-length v0, p0

    if-gt v0, p1, :cond_0

    return v0

    .line 15
    :cond_0
    :goto_0
    aget-byte v0, p0, p1

    and-int/lit16 v1, v0, 0x80

    if-eqz v1, :cond_1

    and-int/lit16 v0, v0, 0xc0

    const/16 v1, 0xc0

    if-eq v0, v1, :cond_1

    add-int/lit8 p1, p1, -0x1

    goto :goto_0

    :cond_1
    return p1
.end method
