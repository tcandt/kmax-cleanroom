.class public final enum Lcom/android/helper/video/VideoCodec;
.super Ljava/lang/Enum;
.source "VideoCodec.java"

# interfaces
.implements Lcom/android/helper/util/Codec;


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/video/VideoCodec;",
        ">;",
        "Lcom/android/helper/util/Codec;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/video/VideoCodec;

.field public static final enum AV1:Lcom/android/helper/video/VideoCodec;

.field public static final enum H264:Lcom/android/helper/video/VideoCodec;

.field public static final enum H265:Lcom/android/helper/video/VideoCodec;


# instance fields
.field private final id:I

.field private final mimeType:Ljava/lang/String;

.field private final name:Ljava/lang/String;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/video/VideoCodec;
    .locals 3

    const/4 v0, 0x3

    .line 8
    new-array v0, v0, [Lcom/android/helper/video/VideoCodec;

    sget-object v1, Lcom/android/helper/video/VideoCodec;->H264:Lcom/android/helper/video/VideoCodec;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/video/VideoCodec;->H265:Lcom/android/helper/video/VideoCodec;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/video/VideoCodec;->AV1:Lcom/android/helper/video/VideoCodec;

    const/4 v2, 0x2

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 8

    .line 9
    new-instance v0, Lcom/android/helper/video/VideoCodec;

    const-string v4, "h264"

    const-string v5, "video/avc"

    const-string v1, "H264"

    const/4 v2, 0x0

    const v3, 0x68323634

    invoke-direct/range {v0 .. v5}, Lcom/android/helper/video/VideoCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v0, Lcom/android/helper/video/VideoCodec;->H264:Lcom/android/helper/video/VideoCodec;

    .line 10
    new-instance v1, Lcom/android/helper/video/VideoCodec;

    const-string v5, "h265"

    const-string v6, "video/hevc"

    const-string v2, "H265"

    const/4 v3, 0x1

    const v4, 0x68323635

    invoke-direct/range {v1 .. v6}, Lcom/android/helper/video/VideoCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v1, Lcom/android/helper/video/VideoCodec;->H265:Lcom/android/helper/video/VideoCodec;

    .line 11
    new-instance v2, Lcom/android/helper/video/VideoCodec;

    const-string v6, "av1"

    const-string v7, "video/av01"

    const-string v3, "AV1"

    const/4 v4, 0x2

    const v5, 0x617631

    invoke-direct/range {v2 .. v7}, Lcom/android/helper/video/VideoCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v2, Lcom/android/helper/video/VideoCodec;->AV1:Lcom/android/helper/video/VideoCodec;

    .line 8
    invoke-static {}, Lcom/android/helper/video/VideoCodec;->$values()[Lcom/android/helper/video/VideoCodec;

    move-result-object v0

    sput-object v0, Lcom/android/helper/video/VideoCodec;->$VALUES:[Lcom/android/helper/video/VideoCodec;

    return-void
.end method

.method private constructor <init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x1000,
            0x1000,
            0x0,
            0x0,
            0x0
        }
        names = {
            null,
            null,
            null,
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(I",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ")V"
        }
    .end annotation

    .line 18
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    .line 19
    iput p3, p0, Lcom/android/helper/video/VideoCodec;->id:I

    .line 20
    iput-object p4, p0, Lcom/android/helper/video/VideoCodec;->name:Ljava/lang/String;

    .line 21
    iput-object p5, p0, Lcom/android/helper/video/VideoCodec;->mimeType:Ljava/lang/String;

    return-void
.end method

.method public static findByName(Ljava/lang/String;)Lcom/android/helper/video/VideoCodec;
    .locals 5

    .line 45
    invoke-static {}, Lcom/android/helper/video/VideoCodec;->values()[Lcom/android/helper/video/VideoCodec;

    move-result-object v0

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    .line 46
    iget-object v4, v3, Lcom/android/helper/video/VideoCodec;->name:Ljava/lang/String;

    invoke-virtual {v4, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4

    if-eqz v4, :cond_0

    return-object v3

    :cond_0
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_1
    const/4 p0, 0x0

    return-object p0
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/video/VideoCodec;
    .locals 1
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8000
        }
        names = {
            null
        }
    .end annotation

    .line 8
    const-class v0, Lcom/android/helper/video/VideoCodec;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/video/VideoCodec;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/video/VideoCodec;
    .locals 1

    .line 8
    sget-object v0, Lcom/android/helper/video/VideoCodec;->$VALUES:[Lcom/android/helper/video/VideoCodec;

    invoke-virtual {v0}, [Lcom/android/helper/video/VideoCodec;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/video/VideoCodec;

    return-object v0
.end method


# virtual methods
.method public getId()I
    .locals 1

    .line 31
    iget v0, p0, Lcom/android/helper/video/VideoCodec;->id:I

    return v0
.end method

.method public getMimeType()Ljava/lang/String;
    .locals 1

    .line 41
    iget-object v0, p0, Lcom/android/helper/video/VideoCodec;->mimeType:Ljava/lang/String;

    return-object v0
.end method

.method public getName()Ljava/lang/String;
    .locals 1

    .line 36
    iget-object v0, p0, Lcom/android/helper/video/VideoCodec;->name:Ljava/lang/String;

    return-object v0
.end method

.method public getType()Lcom/android/helper/util/Codec$Type;
    .locals 1

    .line 26
    sget-object v0, Lcom/android/helper/util/Codec$Type;->VIDEO:Lcom/android/helper/util/Codec$Type;

    return-object v0
.end method
