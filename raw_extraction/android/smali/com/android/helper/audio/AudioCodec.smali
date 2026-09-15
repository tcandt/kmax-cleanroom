.class public final enum Lcom/android/helper/audio/AudioCodec;
.super Ljava/lang/Enum;
.source "AudioCodec.java"

# interfaces
.implements Lcom/android/helper/util/Codec;


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/audio/AudioCodec;",
        ">;",
        "Lcom/android/helper/util/Codec;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/audio/AudioCodec;

.field public static final enum AAC:Lcom/android/helper/audio/AudioCodec;

.field public static final enum FLAC:Lcom/android/helper/audio/AudioCodec;

.field public static final enum OPUS:Lcom/android/helper/audio/AudioCodec;

.field public static final enum RAW:Lcom/android/helper/audio/AudioCodec;


# instance fields
.field private final id:I

.field private final mimeType:Ljava/lang/String;

.field private final name:Ljava/lang/String;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/audio/AudioCodec;
    .locals 3

    const/4 v0, 0x4

    .line 7
    new-array v0, v0, [Lcom/android/helper/audio/AudioCodec;

    sget-object v1, Lcom/android/helper/audio/AudioCodec;->OPUS:Lcom/android/helper/audio/AudioCodec;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioCodec;->AAC:Lcom/android/helper/audio/AudioCodec;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioCodec;->FLAC:Lcom/android/helper/audio/AudioCodec;

    const/4 v2, 0x2

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioCodec;->RAW:Lcom/android/helper/audio/AudioCodec;

    const/4 v2, 0x3

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 9

    .line 8
    new-instance v0, Lcom/android/helper/audio/AudioCodec;

    const-string v4, "opus"

    const-string v5, "audio/opus"

    const-string v1, "OPUS"

    const/4 v2, 0x0

    const v3, 0x6f707573

    invoke-direct/range {v0 .. v5}, Lcom/android/helper/audio/AudioCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v0, Lcom/android/helper/audio/AudioCodec;->OPUS:Lcom/android/helper/audio/AudioCodec;

    .line 9
    new-instance v1, Lcom/android/helper/audio/AudioCodec;

    const-string v5, "aac"

    const-string v6, "audio/mp4a-latm"

    const-string v2, "AAC"

    const/4 v3, 0x1

    const v4, 0x616163

    invoke-direct/range {v1 .. v6}, Lcom/android/helper/audio/AudioCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v1, Lcom/android/helper/audio/AudioCodec;->AAC:Lcom/android/helper/audio/AudioCodec;

    .line 10
    new-instance v2, Lcom/android/helper/audio/AudioCodec;

    const-string v6, "flac"

    const-string v7, "audio/flac"

    const-string v3, "FLAC"

    const/4 v4, 0x2

    const v5, 0x666c6163

    invoke-direct/range {v2 .. v7}, Lcom/android/helper/audio/AudioCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v2, Lcom/android/helper/audio/AudioCodec;->FLAC:Lcom/android/helper/audio/AudioCodec;

    .line 11
    new-instance v3, Lcom/android/helper/audio/AudioCodec;

    const-string v7, "raw"

    const-string v8, "audio/raw"

    const-string v4, "RAW"

    const/4 v5, 0x3

    const v6, 0x726177

    invoke-direct/range {v3 .. v8}, Lcom/android/helper/audio/AudioCodec;-><init>(Ljava/lang/String;IILjava/lang/String;Ljava/lang/String;)V

    sput-object v3, Lcom/android/helper/audio/AudioCodec;->RAW:Lcom/android/helper/audio/AudioCodec;

    .line 7
    invoke-static {}, Lcom/android/helper/audio/AudioCodec;->$values()[Lcom/android/helper/audio/AudioCodec;

    move-result-object v0

    sput-object v0, Lcom/android/helper/audio/AudioCodec;->$VALUES:[Lcom/android/helper/audio/AudioCodec;

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

    .line 17
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    .line 18
    iput p3, p0, Lcom/android/helper/audio/AudioCodec;->id:I

    .line 19
    iput-object p4, p0, Lcom/android/helper/audio/AudioCodec;->name:Ljava/lang/String;

    .line 20
    iput-object p5, p0, Lcom/android/helper/audio/AudioCodec;->mimeType:Ljava/lang/String;

    return-void
.end method

.method public static findByName(Ljava/lang/String;)Lcom/android/helper/audio/AudioCodec;
    .locals 5

    .line 44
    invoke-static {}, Lcom/android/helper/audio/AudioCodec;->values()[Lcom/android/helper/audio/AudioCodec;

    move-result-object v0

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    .line 45
    iget-object v4, v3, Lcom/android/helper/audio/AudioCodec;->name:Ljava/lang/String;

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

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/audio/AudioCodec;
    .locals 1
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8000
        }
        names = {
            null
        }
    .end annotation

    .line 7
    const-class v0, Lcom/android/helper/audio/AudioCodec;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/audio/AudioCodec;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/audio/AudioCodec;
    .locals 1

    .line 7
    sget-object v0, Lcom/android/helper/audio/AudioCodec;->$VALUES:[Lcom/android/helper/audio/AudioCodec;

    invoke-virtual {v0}, [Lcom/android/helper/audio/AudioCodec;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/audio/AudioCodec;

    return-object v0
.end method


# virtual methods
.method public getId()I
    .locals 1

    .line 30
    iget v0, p0, Lcom/android/helper/audio/AudioCodec;->id:I

    return v0
.end method

.method public getMimeType()Ljava/lang/String;
    .locals 1

    .line 40
    iget-object v0, p0, Lcom/android/helper/audio/AudioCodec;->mimeType:Ljava/lang/String;

    return-object v0
.end method

.method public getName()Ljava/lang/String;
    .locals 1

    .line 35
    iget-object v0, p0, Lcom/android/helper/audio/AudioCodec;->name:Ljava/lang/String;

    return-object v0
.end method

.method public getType()Lcom/android/helper/util/Codec$Type;
    .locals 1

    .line 25
    sget-object v0, Lcom/android/helper/util/Codec$Type;->AUDIO:Lcom/android/helper/util/Codec$Type;

    return-object v0
.end method
