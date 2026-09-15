.class public final enum Lcom/android/helper/device/Orientation;
.super Ljava/lang/Enum;
.source "Orientation.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/device/Orientation$Lock;
    }
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/device/Orientation;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/device/Orientation;

.field static final synthetic $assertionsDisabled:Z

.field public static final enum Flip0:Lcom/android/helper/device/Orientation;

.field public static final enum Flip180:Lcom/android/helper/device/Orientation;

.field public static final enum Flip270:Lcom/android/helper/device/Orientation;

.field public static final enum Flip90:Lcom/android/helper/device/Orientation;

.field public static final enum Orient0:Lcom/android/helper/device/Orientation;

.field public static final enum Orient180:Lcom/android/helper/device/Orientation;

.field public static final enum Orient270:Lcom/android/helper/device/Orientation;

.field public static final enum Orient90:Lcom/android/helper/device/Orientation;


# instance fields
.field private final name:Ljava/lang/String;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/device/Orientation;
    .locals 3

    const/16 v0, 0x8

    .line 3
    new-array v0, v0, [Lcom/android/helper/device/Orientation;

    sget-object v1, Lcom/android/helper/device/Orientation;->Orient0:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Orient90:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Orient180:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x2

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Orient270:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x3

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Flip0:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x4

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Flip90:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x5

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Flip180:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x6

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/device/Orientation;->Flip270:Lcom/android/helper/device/Orientation;

    const/4 v2, 0x7

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 4

    .line 6
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x0

    const-string v2, "0"

    const-string v3, "Orient0"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Orient0:Lcom/android/helper/device/Orientation;

    .line 7
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x1

    const-string v2, "90"

    const-string v3, "Orient90"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Orient90:Lcom/android/helper/device/Orientation;

    .line 8
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x2

    const-string v2, "180"

    const-string v3, "Orient180"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Orient180:Lcom/android/helper/device/Orientation;

    .line 9
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x3

    const-string v2, "270"

    const-string v3, "Orient270"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Orient270:Lcom/android/helper/device/Orientation;

    .line 10
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x4

    const-string v2, "flip0"

    const-string v3, "Flip0"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Flip0:Lcom/android/helper/device/Orientation;

    .line 11
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x5

    const-string v2, "flip90"

    const-string v3, "Flip90"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Flip90:Lcom/android/helper/device/Orientation;

    .line 12
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x6

    const-string v2, "flip180"

    const-string v3, "Flip180"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Flip180:Lcom/android/helper/device/Orientation;

    .line 13
    new-instance v0, Lcom/android/helper/device/Orientation;

    const/4 v1, 0x7

    const-string v2, "flip270"

    const-string v3, "Flip270"

    invoke-direct {v0, v3, v1, v2}, Lcom/android/helper/device/Orientation;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v0, Lcom/android/helper/device/Orientation;->Flip270:Lcom/android/helper/device/Orientation;

    .line 3
    invoke-static {}, Lcom/android/helper/device/Orientation;->$values()[Lcom/android/helper/device/Orientation;

    move-result-object v0

    sput-object v0, Lcom/android/helper/device/Orientation;->$VALUES:[Lcom/android/helper/device/Orientation;

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

    .line 21
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    .line 22
    iput-object p3, p0, Lcom/android/helper/device/Orientation;->name:Ljava/lang/String;

    return-void
.end method

.method public static fromRotation(I)Lcom/android/helper/device/Orientation;
    .locals 1

    rsub-int/lit8 p0, p0, 0x4

    .line 38
    rem-int/lit8 p0, p0, 0x4

    .line 39
    invoke-static {}, Lcom/android/helper/device/Orientation;->values()[Lcom/android/helper/device/Orientation;

    move-result-object v0

    aget-object p0, v0, p0

    return-object p0
.end method

.method public static getByName(Ljava/lang/String;)Lcom/android/helper/device/Orientation;
    .locals 5

    .line 26
    invoke-static {}, Lcom/android/helper/device/Orientation;->values()[Lcom/android/helper/device/Orientation;

    move-result-object v0

    array-length v1, v0

    const/4 v2, 0x0

    :goto_0
    if-ge v2, v1, :cond_1

    aget-object v3, v0, v2

    .line 27
    iget-object v4, v3, Lcom/android/helper/device/Orientation;->name:Ljava/lang/String;

    invoke-virtual {v4, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4

    if-eqz v4, :cond_0

    return-object v3

    :cond_0
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 32
    :cond_1
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Unknown orientation: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/device/Orientation;
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
    const-class v0, Lcom/android/helper/device/Orientation;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/device/Orientation;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/device/Orientation;
    .locals 1

    .line 3
    sget-object v0, Lcom/android/helper/device/Orientation;->$VALUES:[Lcom/android/helper/device/Orientation;

    invoke-virtual {v0}, [Lcom/android/helper/device/Orientation;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/device/Orientation;

    return-object v0
.end method


# virtual methods
.method public getRotation()I
    .locals 1

    .line 47
    invoke-virtual {p0}, Lcom/android/helper/device/Orientation;->ordinal()I

    move-result v0

    and-int/lit8 v0, v0, 0x3

    return v0
.end method

.method public isFlipped()Z
    .locals 1

    .line 43
    invoke-virtual {p0}, Lcom/android/helper/device/Orientation;->ordinal()I

    move-result v0

    and-int/lit8 v0, v0, 0x4

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method
