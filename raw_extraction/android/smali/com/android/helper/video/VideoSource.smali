.class public final enum Lcom/android/helper/video/VideoSource;
.super Ljava/lang/Enum;
.source "VideoSource.java"


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/video/VideoSource;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/video/VideoSource;

.field public static final enum CAMERA:Lcom/android/helper/video/VideoSource;

.field public static final enum DISPLAY:Lcom/android/helper/video/VideoSource;


# instance fields
.field private final name:Ljava/lang/String;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/video/VideoSource;
    .locals 3

    const/4 v0, 0x2

    .line 3
    new-array v0, v0, [Lcom/android/helper/video/VideoSource;

    sget-object v1, Lcom/android/helper/video/VideoSource;->DISPLAY:Lcom/android/helper/video/VideoSource;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/video/VideoSource;->CAMERA:Lcom/android/helper/video/VideoSource;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 4

    .line 4
    new-instance v0, Lcom/android/helper/video/VideoSource;

    const/4 v1, 0x0

    const-string v2, "display"

    const-string v3, "DISPLAY"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/video/VideoSource;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/video/VideoSource;->DISPLAY:Lcom/android/helper/video/VideoSource;

    .line 5
    new-instance v0, Lcom/android/helper/video/VideoSource;

    const/4 v1, 0x1

    const-string v2, "camera"

    const-string v3, "CAMERA"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/video/VideoSource;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/video/VideoSource;->CAMERA:Lcom/android/helper/video/VideoSource;

    .line 3
    invoke-static {}, Lcom/android/helper/video/VideoSource;->$values()[Lcom/android/helper/video/VideoSource;

    move-result-object v0

    sput-object v0, Lcom/android/helper/video/VideoSource;->$VALUES:[Lcom/android/helper/video/VideoSource;

    return-void
.end method

.method private constructor <init>(Ljava/lang/String;ILjava/lang/String;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x1000,
            0x1000,
            0x0
        }
        names = {
            null,
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            ")V"
        }
    .end annotation

    .line 9
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    .line 10
    iput-object p3, p0, Lcom/android/helper/video/VideoSource;->name:Ljava/lang/String;

    return-void
.end method

.method public static findByName(Ljava/lang/String;)Lcom/android/helper/video/VideoSource;
    .locals 5

    .line 14
    invoke-static {}, Lcom/android/helper/video/VideoSource;->values()[Lcom/android/helper/video/VideoSource;

    move-result-object v0

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    .line 15
    iget-object v4, v3, Lcom/android/helper/video/VideoSource;->name:Ljava/lang/String;

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

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/video/VideoSource;
    .locals 1
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8000
        }
        names = {
            null
        }
    .end annotation

    .line 3
    const-class v0, Lcom/android/helper/video/VideoSource;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/video/VideoSource;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/video/VideoSource;
    .locals 1

    .line 3
    sget-object v0, Lcom/android/helper/video/VideoSource;->$VALUES:[Lcom/android/helper/video/VideoSource;

    invoke-virtual {v0}, [Lcom/android/helper/video/VideoSource;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/video/VideoSource;

    return-object v0
.end method
