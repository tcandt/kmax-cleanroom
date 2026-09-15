.class public final enum Lcom/android/helper/audio/AudioSource;
.super Ljava/lang/Enum;
.source "AudioSource.java"


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/audio/AudioSource;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/audio/AudioSource;

.field public static final enum MIC:Lcom/android/helper/audio/AudioSource;

.field public static final enum MIC_CAMCORDER:Lcom/android/helper/audio/AudioSource;

.field public static final enum MIC_UNPROCESSED:Lcom/android/helper/audio/AudioSource;

.field public static final enum MIC_VOICE_COMMUNICATION:Lcom/android/helper/audio/AudioSource;

.field public static final enum MIC_VOICE_RECOGNITION:Lcom/android/helper/audio/AudioSource;

.field public static final enum OUTPUT:Lcom/android/helper/audio/AudioSource;

.field public static final enum PLAYBACK:Lcom/android/helper/audio/AudioSource;

.field public static final enum VOICE_CALL:Lcom/android/helper/audio/AudioSource;

.field public static final enum VOICE_CALL_DOWNLINK:Lcom/android/helper/audio/AudioSource;

.field public static final enum VOICE_CALL_UPLINK:Lcom/android/helper/audio/AudioSource;

.field public static final enum VOICE_PERFORMANCE:Lcom/android/helper/audio/AudioSource;


# instance fields
.field private final directAudioSource:I

.field private final name:Ljava/lang/String;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/audio/AudioSource;
    .locals 3

    const/16 v0, 0xb

    .line 6
    new-array v0, v0, [Lcom/android/helper/audio/AudioSource;

    sget-object v1, Lcom/android/helper/audio/AudioSource;->OUTPUT:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->MIC:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->PLAYBACK:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x2

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->MIC_UNPROCESSED:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x3

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->MIC_CAMCORDER:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x4

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->MIC_VOICE_RECOGNITION:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x5

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->MIC_VOICE_COMMUNICATION:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x6

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->VOICE_CALL:Lcom/android/helper/audio/AudioSource;

    const/4 v2, 0x7

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->VOICE_CALL_UPLINK:Lcom/android/helper/audio/AudioSource;

    const/16 v2, 0x8

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->VOICE_CALL_DOWNLINK:Lcom/android/helper/audio/AudioSource;

    const/16 v2, 0x9

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/audio/AudioSource;->VOICE_PERFORMANCE:Lcom/android/helper/audio/AudioSource;

    const/16 v2, 0xa

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 10

    .line 8
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "OUTPUT"

    const/4 v2, 0x0

    const-string v3, "output"

    const/16 v4, 0x8

    invoke-direct {v0, v1, v2, v3, v4}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->OUTPUT:Lcom/android/helper/audio/AudioSource;

    .line 9
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const/4 v1, 0x1

    const-string v2, "mic"

    const-string v3, "MIC"

    invoke-direct {v0, v3, v1, v2, v1}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->MIC:Lcom/android/helper/audio/AudioSource;

    .line 10
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "playback"

    const/4 v2, -0x1

    const-string v3, "PLAYBACK"

    const/4 v5, 0x2

    invoke-direct {v0, v3, v5, v1, v2}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->PLAYBACK:Lcom/android/helper/audio/AudioSource;

    .line 11
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "MIC_UNPROCESSED"

    const/4 v2, 0x3

    const-string v3, "mic-unprocessed"

    const/16 v6, 0x9

    invoke-direct {v0, v1, v2, v3, v6}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->MIC_UNPROCESSED:Lcom/android/helper/audio/AudioSource;

    .line 12
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "MIC_CAMCORDER"

    const/4 v3, 0x4

    const-string v7, "mic-camcorder"

    const/4 v8, 0x5

    invoke-direct {v0, v1, v3, v7, v8}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->MIC_CAMCORDER:Lcom/android/helper/audio/AudioSource;

    .line 13
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "MIC_VOICE_RECOGNITION"

    const-string v7, "mic-voice-recognition"

    const/4 v9, 0x6

    invoke-direct {v0, v1, v8, v7, v9}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->MIC_VOICE_RECOGNITION:Lcom/android/helper/audio/AudioSource;

    .line 14
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "MIC_VOICE_COMMUNICATION"

    const-string v7, "mic-voice-communication"

    const/4 v8, 0x7

    invoke-direct {v0, v1, v9, v7, v8}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->MIC_VOICE_COMMUNICATION:Lcom/android/helper/audio/AudioSource;

    .line 15
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "VOICE_CALL"

    const-string v7, "voice-call"

    invoke-direct {v0, v1, v8, v7, v3}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->VOICE_CALL:Lcom/android/helper/audio/AudioSource;

    .line 16
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "VOICE_CALL_UPLINK"

    const-string v3, "voice-call-uplink"

    invoke-direct {v0, v1, v4, v3, v5}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->VOICE_CALL_UPLINK:Lcom/android/helper/audio/AudioSource;

    .line 17
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const-string v1, "VOICE_CALL_DOWNLINK"

    const-string v3, "voice-call-downlink"

    invoke-direct {v0, v1, v6, v3, v2}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->VOICE_CALL_DOWNLINK:Lcom/android/helper/audio/AudioSource;

    .line 18
    new-instance v0, Lcom/android/helper/audio/AudioSource;

    const/16 v1, 0xa

    const-string v2, "voice-performance"

    const-string v3, "VOICE_PERFORMANCE"

    invoke-direct {v0, v3, v1, v2, v1}, Lcom/android/helper/audio/AudioSource;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/audio/AudioSource;->VOICE_PERFORMANCE:Lcom/android/helper/audio/AudioSource;

    .line 6
    invoke-static {}, Lcom/android/helper/audio/AudioSource;->$values()[Lcom/android/helper/audio/AudioSource;

    move-result-object v0

    sput-object v0, Lcom/android/helper/audio/AudioSource;->$VALUES:[Lcom/android/helper/audio/AudioSource;

    return-void
.end method

.method private constructor <init>(Ljava/lang/String;ILjava/lang/String;I)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x1000,
            0x1000,
            0x0,
            0x0
        }
        names = {
            null,
            null,
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "I)V"
        }
    .end annotation

    .line 23
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    .line 24
    iput-object p3, p0, Lcom/android/helper/audio/AudioSource;->name:Ljava/lang/String;

    .line 25
    iput p4, p0, Lcom/android/helper/audio/AudioSource;->directAudioSource:I

    return-void
.end method

.method public static findByName(Ljava/lang/String;)Lcom/android/helper/audio/AudioSource;
    .locals 5

    .line 37
    invoke-static {}, Lcom/android/helper/audio/AudioSource;->values()[Lcom/android/helper/audio/AudioSource;

    move-result-object v0

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    .line 38
    iget-object v4, v3, Lcom/android/helper/audio/AudioSource;->name:Ljava/lang/String;

    invoke-virtual {p0, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

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

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/audio/AudioSource;
    .locals 1
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8000
        }
        names = {
            null
        }
    .end annotation

    .line 6
    const-class v0, Lcom/android/helper/audio/AudioSource;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/audio/AudioSource;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/audio/AudioSource;
    .locals 1

    .line 6
    sget-object v0, Lcom/android/helper/audio/AudioSource;->$VALUES:[Lcom/android/helper/audio/AudioSource;

    invoke-virtual {v0}, [Lcom/android/helper/audio/AudioSource;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/audio/AudioSource;

    return-object v0
.end method


# virtual methods
.method public getDirectAudioSource()I
    .locals 1

    .line 33
    iget v0, p0, Lcom/android/helper/audio/AudioSource;->directAudioSource:I

    return v0
.end method

.method public isDirect()Z
    .locals 1

    .line 29
    sget-object v0, Lcom/android/helper/audio/AudioSource;->PLAYBACK:Lcom/android/helper/audio/AudioSource;

    if-eq p0, v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method
