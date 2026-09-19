.class public final enum Lcom/android/helper/util/Ln$Level;
.super Ljava/lang/Enum;
.source "Ln.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/util/Ln;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x4019
    name = "Level"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum<",
        "Lcom/android/helper/util/Ln$Level;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic $VALUES:[Lcom/android/helper/util/Ln$Level;

.field public static final enum DEBUG:Lcom/android/helper/util/Ln$Level;

.field public static final enum ERROR:Lcom/android/helper/util/Ln$Level;

.field public static final enum INFO:Lcom/android/helper/util/Ln$Level;

.field public static final enum VERBOSE:Lcom/android/helper/util/Ln$Level;

.field public static final enum WARN:Lcom/android/helper/util/Ln$Level;


# direct methods
.method private static synthetic $values()[Lcom/android/helper/util/Ln$Level;
    .locals 3

    const/4 v0, 0x5

    .line 22
    new-array v0, v0, [Lcom/android/helper/util/Ln$Level;

    sget-object v1, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    const/4 v2, 0x0

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/util/Ln$Level;->DEBUG:Lcom/android/helper/util/Ln$Level;

    const/4 v2, 0x1

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/util/Ln$Level;->INFO:Lcom/android/helper/util/Ln$Level;

    const/4 v2, 0x2

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/util/Ln$Level;->WARN:Lcom/android/helper/util/Ln$Level;

    const/4 v2, 0x3

    aput-object v1, v0, v2

    sget-object v1, Lcom/android/helper/util/Ln$Level;->ERROR:Lcom/android/helper/util/Ln$Level;

    const/4 v2, 0x4

    aput-object v1, v0, v2

    return-object v0
.end method

.method static constructor <clinit>()V
    .locals 3

    .line 23
    new-instance v0, Lcom/android/helper/util/Ln$Level;

    const-string v1, "VERBOSE"

    const/4 v2, 0x0

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Ln$Level;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    new-instance v0, Lcom/android/helper/util/Ln$Level;

    const-string v1, "DEBUG"

    const/4 v2, 0x1

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Ln$Level;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Ln$Level;->DEBUG:Lcom/android/helper/util/Ln$Level;

    new-instance v0, Lcom/android/helper/util/Ln$Level;

    const-string v1, "INFO"

    const/4 v2, 0x2

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Ln$Level;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Ln$Level;->INFO:Lcom/android/helper/util/Ln$Level;

    new-instance v0, Lcom/android/helper/util/Ln$Level;

    const-string v1, "WARN"

    const/4 v2, 0x3

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Ln$Level;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Ln$Level;->WARN:Lcom/android/helper/util/Ln$Level;

    new-instance v0, Lcom/android/helper/util/Ln$Level;

    const-string v1, "ERROR"

    const/4 v2, 0x4

    invoke-direct {v0, v1, v2}, Lcom/android/helper/util/Ln$Level;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/android/helper/util/Ln$Level;->ERROR:Lcom/android/helper/util/Ln$Level;

    .line 22
    invoke-static {}, Lcom/android/helper/util/Ln$Level;->$values()[Lcom/android/helper/util/Ln$Level;

    move-result-object v0

    sput-object v0, Lcom/android/helper/util/Ln$Level;->$VALUES:[Lcom/android/helper/util/Ln$Level;

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

    .line 22
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    return-void
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/android/helper/util/Ln$Level;
    .locals 1
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8000
        }
        names = {
            null
        }
    .end annotation

    .line 22
    const-class v0, Lcom/android/helper/util/Ln$Level;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object p0

    check-cast p0, Lcom/android/helper/util/Ln$Level;

    return-object p0
.end method

.method public static values()[Lcom/android/helper/util/Ln$Level;
    .locals 1

    .line 22
    sget-object v0, Lcom/android/helper/util/Ln$Level;->$VALUES:[Lcom/android/helper/util/Ln$Level;

    invoke-virtual {v0}, [Lcom/android/helper/util/Ln$Level;->clone()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [Lcom/android/helper/util/Ln$Level;

    return-object v0
.end method
