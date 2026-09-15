.class public final enum Lcom/android/helper/util/Codec$Type;
.super Ljava/lang/Enum;
.source "Codec.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/util/Codec;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x4019
    name = "Type"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/util/Codec$Type;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/util/Codec$Type;

.field public static final enum AUDIO:Lcom/android/helper/util/Codec$Type;

.field public static final enum VIDEO:Lcom/android/helper/util/Codec$Type;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/util/Codec$Type;
    .locals 3

    const/4 v0, 0x2

    .line 7
    new-array v0, v0, [Lcom/android/helper/util/Codec$Type;

    sget-object v1, Lcom/android/helper/util/Codec$Type;->VIDEO:Lcom/android/helper/util/Codec$Type;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/util/Codec$Type;->AUDIO:Lcom/android/helper/util/Codec$Type;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 3

    .line 8
    new-instance v0, Lcom/android/helper/util/Codec$Type;

    const-string v1, "VIDEO"

    const/4 v2, 0x0

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Codec$Type;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Codec$Type;->VIDEO:Lcom/android/helper/util/Codec$Type;

    .line 9
    new-instance v0, Lcom/android/helper/util/Codec$Type;

    const-string v1, "AUDIO"

    const/4 v2, 0x1

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Codec$Type;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Codec$Type;->AUDIO:Lcom/android/helper/util/Codec$Type;

    .line 7
    invoke-static {}, Lcom/android/helper/util/Codec$Type;->$values()[Lcom/android/helper/util/Codec$Type;

    move-result-object v0

    sput-object v0, Lcom/android/helper/util/Codec$Type;->$VALUES:[Lcom/android/helper/util/Codec$Type;

    return-void
.end method

.method private constructor <init>(Ljava/lang/String;I)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x1000,
            0x1000
        }
        names = {
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 7
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    return-void
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/util/Codec$Type;
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
    const-class v0, Lcom/android/helper/util/Codec$Type;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/util/Codec$Type;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/util/Codec$Type;
    .locals 1

    .line 7
    sget-object v0, Lcom/android/helper/util/Codec$Type;->$VALUES:[Lcom/android/helper/util/Codec$Type;

    invoke-virtual {v0}, [Lcom/android/helper/util/Codec$Type;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/util/Codec$Type;

    return-object v0
.end method
