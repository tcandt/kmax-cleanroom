.class public final Lcom/android/helper/wrappers/DisplayControl;
.super Ljava/lang/Object;
.source "DisplayControl.java"


# static fields
.field private static final CLASS:Ljava/lang/Class;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/Class<",
            "*>;"
        }
    .end annotation
.end field

.field private static getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

.field private static getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;


# direct methods
.method static constructor <clinit>()V
    .locals 14

    const/4 v0, 0x0

    .line 22
    :try_start_0
    const-string v1, "com.android.internal.os.ClassLoaderFactory"

    invoke-static {v1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v1

    .line 23
    const-string v2, "createClassLoader"

    const/4 v3, 0x7

    new-array v4, v3, [Ljava/lang/Class;

    const-class v5, Ljava/lang/String;

    const/4 v6, 0x0

    aput-object v5, v4, v6

    const/4 v7, 0x1

    aput-object v5, v4, v7

    const/4 v8, 0x2

    aput-object v5, v4, v8

    const-class v9, Ljava/lang/ClassLoader;

    const/4 v10, 0x3

    aput-object v9, v4, v10

    sget-object v9, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v11, 0x4

    aput-object v9, v4, v11

    sget-object v9, Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;

    const/4 v12, 0x5

    aput-object v9, v4, v12

    const/4 v9, 0x6

    aput-object v5, v4, v9

    invoke-virtual {v1, v2, v4}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    .line 26
    const-string v2, "SYSTEMSERVERCLASSPATH"

    invoke-static {v2}, Landroid/system/Os;->getenv(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 28
    invoke-static {}, Ljava/lang/ClassLoader;->getSystemClassLoader()Ljava/lang/ClassLoader;

    move-result-object v4

    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v5

    invoke-static {v7}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v13

    new-array v3, v3, [Ljava/lang/Object;

    aput-object v2, v3, v6

    aput-object v0, v3, v7

    aput-object v0, v3, v8

    aput-object v4, v3, v10

    aput-object v5, v3, v11

    aput-object v13, v3, v12

    aput-object v0, v3, v9

    .line 27
    invoke-virtual {v1, v0, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/lang/ClassLoader;

    .line 30
    const-string v2, "com.android.server.display.DisplayControl"

    invoke-virtual {v1, v2}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 32
    const-class v1, Ljava/lang/Runtime;

    const-string v2, "loadLibrary0"

    new-array v3, v8, [Ljava/lang/Class;

    const-class v4, Ljava/lang/Class;

    aput-object v4, v3, v6

    const-class v4, Ljava/lang/String;

    aput-object v4, v3, v7

    invoke-virtual {v1, v2, v3}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    .line 33
    invoke-virtual {v1, v7}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 34
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v2

    new-array v3, v8, [Ljava/lang/Object;

    aput-object v0, v3, v6

    const-string v4, "android_servers"

    aput-object v4, v3, v7

    invoke-virtual {v1, v2, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    goto :goto_0

    :catchall_0
    move-exception v1

    .line 36
    const-string v2, "Could not initialize DisplayControl"

    invoke-static {v2, v1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 39
    :goto_0
    sput-object v0, Lcom/android/helper/wrappers/DisplayControl;->CLASS:Ljava/lang/Class;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 45
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static getGetPhysicalDisplayIdsMethod()Ljava/lang/reflect/Method;
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 67
    sget-object v0, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 68
    sget-object v0, Lcom/android/helper/wrappers/DisplayControl;->CLASS:Ljava/lang/Class;

    const-string v1, "getPhysicalDisplayIds"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

    .line 70
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getGetPhysicalDisplayTokenMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 50
    sget-object v0, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 51
    sget-object v0, Lcom/android/helper/wrappers/DisplayControl;->CLASS:Ljava/lang/Class;

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    sget-object v2, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "getPhysicalDisplayToken"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

    .line 53
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method public static getPhysicalDisplayIds()[J
    .locals 3

    const/4 v0, 0x0

    .line 75
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/DisplayControl;->getGetPhysicalDisplayIdsMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 76
    invoke-virtual {v1, v0, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, [J
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object v1

    :catch_0
    move-exception v1

    .line 78
    const-string v2, "Could not invoke method"

    invoke-static {v2, v1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method public static getPhysicalDisplayToken(J)Landroid/os/IBinder;
    .locals 3

    const/4 v0, 0x0

    .line 58
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/DisplayControl;->getGetPhysicalDisplayTokenMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 59
    invoke-static {p0, p1}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object p0

    const/4 p1, 0x1

    new-array p1, p1, [Ljava/lang/Object;

    const/4 v2, 0x0

    aput-object p0, p1, v2

    invoke-virtual {v1, v0, p1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Landroid/os/IBinder;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object p0

    :catch_0
    move-exception p0

    .line 61
    const-string p1, "Could not invoke method"

    invoke-static {p1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method
