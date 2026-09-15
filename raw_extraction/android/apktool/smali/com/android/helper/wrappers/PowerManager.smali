.class public final Lcom/android/helper/wrappers/PowerManager;
.super Ljava/lang/Object;
.source "PowerManager.java"


# instance fields
.field private isScreenOnMethod:Ljava/lang/reflect/Method;

.field private final manager:Landroid/os/IInterface;


# direct methods
.method private constructor <init>(Landroid/os/IInterface;)V
    .locals 0

    .line 20
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 21
    iput-object p1, p0, Lcom/android/helper/wrappers/PowerManager;->manager:Landroid/os/IInterface;

    return-void
.end method

.method static create()Lcom/android/helper/wrappers/PowerManager;
    .locals 2

    .line 16
    const-string v0, "power"

    const-string v1, "android.os.IPowerManager"

    invoke-static {v0, v1}, Lcom/android/helper/wrappers/ServiceManager;->getService(Ljava/lang/String;Ljava/lang/String;)Landroid/os/IInterface;

    move-result-object v0

    .line 17
    new-instance v1, Lcom/android/helper/wrappers/PowerManager;

    invoke-direct {v1, v0}, Lcom/android/helper/wrappers/PowerManager;-><init>(Landroid/os/IInterface;)V

    return-object v1
.end method

.method private getIsScreenOnMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 25
    iget-object v0, p0, Lcom/android/helper/wrappers/PowerManager;->isScreenOnMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_1

    .line 26
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x22

    if-lt v0, v1, :cond_0

    .line 27
    iget-object v0, p0, Lcom/android/helper/wrappers/PowerManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "isDisplayInteractive"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/PowerManager;->isScreenOnMethod:Ljava/lang/reflect/Method;

    goto :goto_0

    .line 29
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/PowerManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const-string v1, "isInteractive"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/PowerManager;->isScreenOnMethod:Ljava/lang/reflect/Method;

    .line 32
    :cond_1
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/PowerManager;->isScreenOnMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method


# virtual methods
.method public isScreenOn(I)Z
    .locals 4

    const/4 v0, 0x0

    .line 38
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/PowerManager;->getIsScreenOnMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 39
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v3, 0x22

    if-lt v2, v3, :cond_0

    .line 40
    iget-object v2, p0, Lcom/android/helper/wrappers/PowerManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    const/4 v3, 0x1

    new-array v3, v3, [Ljava/lang/Object;

    aput-object p1, v3, v0

    invoke-virtual {v1, v2, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Boolean;

    invoke-virtual {p1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result p1

    return p1

    .line 42
    :cond_0
    iget-object p1, p0, Lcom/android/helper/wrappers/PowerManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x0

    invoke-virtual {v1, p1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Boolean;

    invoke-virtual {p1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result p1
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return p1

    :catch_0
    move-exception p1

    .line 44
    const-string v1, "Could not invoke method"

    invoke-static {v1, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method
