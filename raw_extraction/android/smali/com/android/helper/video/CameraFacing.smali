.class public final enum Lcom/android/helper/video/CameraFacing;
.super Ljava/lang/Enum;
.source "CameraFacing.java"


# annotations
.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/video/CameraFacing;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/video/CameraFacing;

.field public static final enum BACK:Lcom/android/helper/video/CameraFacing;

.field public static final enum EXTERNAL:Lcom/android/helper/video/CameraFacing;

.field public static final enum FRONT:Lcom/android/helper/video/CameraFacing;


# instance fields
.field private final name:Ljava/lang/String;

.field private final value:I


# direct methods
.method private static synthetic $values()[Lcom/android/helper/video/CameraFacing;
    .locals 3

    const/4 v0, 0x3

    .line 6
    new-array v0, v0, [Lcom/android/helper/video/CameraFacing;

    sget-object v1, Lcom/android/helper/video/CameraFacing;->FRONT:Lcom/android/helper/video/CameraFacing;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/video/CameraFacing;->BACK:Lcom/android/helper/video/CameraFacing;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/video/CameraFacing;->EXTERNAL:Lcom/android/helper/video/CameraFacing;

    const/4 v2, 0x2

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 4

    .line 7
    new-instance v0, Lcom/android/helper/video/CameraFacing;

    const/4 v1, 0x0

    const-string v2, "front"

    const-string v3, "FRONT"

    invoke-direct {v0, v3, v1, v2, v1}, Lcom/android/helper/video/CameraFacing;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/video/CameraFacing;->FRONT:Lcom/android/helper/video/CameraFacing;

    .line 8
    new-instance v0, Lcom/android/helper/video/CameraFacing;

    const/4 v1, 0x1

    const-string v2, "back"

    const-string v3, "BACK"

    invoke-direct {v0, v3, v1, v2, v1}, Lcom/android/helper/video/CameraFacing;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/video/CameraFacing;->BACK:Lcom/android/helper/video/CameraFacing;

    .line 9
    new-instance v0, Lcom/android/helper/video/CameraFacing;

    const/4 v1, 0x2

    const-string v2, "external"

    const-string v3, "EXTERNAL"

    invoke-direct {v0, v3, v1, v2, v1}, Lcom/android/helper/video/CameraFacing;-><init>(Ljava/lang/String;ILjava/lang/String;I)V

    sput-object v0, Lcom/android/helper/video/CameraFacing;->EXTERNAL:Lcom/android/helper/video/CameraFacing;

    .line 6
    invoke-static {}, Lcom/android/helper/video/CameraFacing;->$values()[Lcom/android/helper/video/CameraFacing;

    move-result-object v0

    sput-object v0, Lcom/android/helper/video/CameraFacing;->$VALUES:[Lcom/android/helper/video/CameraFacing;

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

    .line 15
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    .line 16
    iput-object p3, p0, Lcom/android/helper/video/CameraFacing;->name:Ljava/lang/String;

    .line 17
    iput p4, p0, Lcom/android/helper/video/CameraFacing;->value:I

    return-void
.end method

.method public static findByName(Ljava/lang/String;)Lcom/android/helper/video/CameraFacing;
    .locals 5

    .line 25
    invoke-static {}, Lcom/android/helper/video/CameraFacing;->values()[Lcom/android/helper/video/CameraFacing;

    move-result-object v0

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    .line 26
    iget-object v4, v3, Lcom/android/helper/video/CameraFacing;->name:Ljava/lang/String;

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

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/video/CameraFacing;
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
    const-class v0, Lcom/android/helper/video/CameraFacing;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/video/CameraFacing;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/video/CameraFacing;
    .locals 1

    .line 6
    sget-object v0, Lcom/android/helper/video/CameraFacing;->$VALUES:[Lcom/android/helper/video/CameraFacing;

    invoke-virtual {v0}, [Lcom/android/helper/video/CameraFacing;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/video/CameraFacing;

    return-object v0
.end method


# virtual methods
.method value()I
    .locals 1

    .line 21
    iget v0, p0, Lcom/android/helper/video/CameraFacing;->value:I

    return v0
.end method
