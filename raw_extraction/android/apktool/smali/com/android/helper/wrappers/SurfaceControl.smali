.class public final Lcom/android/helper/wrappers/SurfaceControl;
.super Ljava/lang/Object;
.source "SurfaceControl.java"


# static fields
.field private static final CLASS:Ljava/lang/Class;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/Class<",
            "*>;"
        }
    .end annotation
.end field

.field public static final POWER_MODE_NORMAL:I = 0x2

.field public static final POWER_MODE_OFF:I

.field private static getBuiltInDisplayMethod:Ljava/lang/reflect/Method;

.field private static getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

.field private static getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

.field private static setDisplayPowerModeMethod:Ljava/lang/reflect/Method;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 25
    :try_start_0
    const-string v0, "android.view.SurfaceControl"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;
    :try_end_0
    .catch Ljava/lang/ClassNotFoundException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 27
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1
.end method

.method private constructor <init>()V
    .locals 0

    .line 36
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static closeTransaction()V
    .locals 3

    .line 50
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "closeTransaction"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-virtual {v0, v2, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 52
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1
.end method

.method public static createDisplay(Ljava/lang/String;Z)Landroid/os/IBinder;
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 82
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const/4 v1, 0x2

    new-array v2, v1, [Ljava/lang/Class;

    const-class v3, Ljava/lang/String;

    const/4 v4, 0x0

    aput-object v3, v2, v4

    sget-object v3, Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;

    const/4 v5, 0x1

    aput-object v3, v2, v5

    const-string v3, "createDisplay"

    invoke-virtual {v0, v3, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-static {p1}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object p1

    new-array v1, v1, [Ljava/lang/Object;

    aput-object p0, v1, v4

    aput-object p1, v1, v5

    const/4 p0, 0x0

    invoke-virtual {v0, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Landroid/os/IBinder;

    return-object p0
.end method

.method public static destroyDisplay(Landroid/os/IBinder;)V
    .locals 6

    .line 186
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "destroyDisplay"

    const/4 v2, 0x1

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Landroid/os/IBinder;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    new-array v1, v2, [Ljava/lang/Object;

    aput-object p0, v1, v5

    const/4 p0, 0x0

    invoke-virtual {v0, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p0

    .line 188
    new-instance v0, Ljava/lang/AssertionError;

    invoke-direct {v0, p0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v0
.end method

.method public static getBuiltInDisplay()Landroid/os/IBinder;
    .locals 5

    const/4 v0, 0x0

    .line 109
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getGetBuiltInDisplayMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 110
    sget v2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v3, 0x1d

    if-ge v2, v3, :cond_0

    const/4 v2, 0x0

    .line 112
    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    const/4 v4, 0x1

    new-array v4, v4, [Ljava/lang/Object;

    aput-object v3, v4, v2

    invoke-virtual {v1, v0, v4}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/os/IBinder;

    return-object v1

    .line 116
    :cond_0
    invoke-virtual {v1, v0, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/os/IBinder;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object v1

    :catch_0
    move-exception v1

    .line 118
    const-string v2, "Could not invoke method"

    invoke-static {v2, v1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method private static getGetBuiltInDisplayMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 86
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getBuiltInDisplayMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_1

    .line 89
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1d

    if-ge v0, v1, :cond_0

    .line 90
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "getBuiltInDisplay"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getBuiltInDisplayMethod:Ljava/lang/reflect/Method;

    goto :goto_0

    .line 92
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "getInternalDisplayToken"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getBuiltInDisplayMethod:Ljava/lang/reflect/Method;

    .line 95
    :cond_1
    :goto_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getBuiltInDisplayMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getGetPhysicalDisplayIdsMethod()Ljava/lang/reflect/Method;
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 141
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 142
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "getPhysicalDisplayIds"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

    .line 144
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayIdsMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getGetPhysicalDisplayTokenMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 124
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 125
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    sget-object v2, Ljava/lang/Long;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "getPhysicalDisplayToken"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

    .line 127
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayTokenMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method public static getPhysicalDisplayIds()[J
    .locals 3

    const/4 v0, 0x0

    .line 158
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getGetPhysicalDisplayIdsMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 159
    invoke-virtual {v1, v0, v0}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, [J
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object v1

    :catch_0
    move-exception v1

    .line 161
    const-string v2, "Could not invoke method"

    invoke-static {v2, v1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method public static getPhysicalDisplayToken(J)Landroid/os/IBinder;
    .locals 3

    const/4 v0, 0x0

    .line 132
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getGetPhysicalDisplayTokenMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 133
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

    .line 135
    const-string p1, "Could not invoke method"

    invoke-static {p1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method private static getSetDisplayPowerModeMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 167
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayPowerModeMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 168
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const/4 v1, 0x2

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Landroid/os/IBinder;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "setDisplayPowerMode"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayPowerModeMethod:Ljava/lang/reflect/Method;

    .line 170
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayPowerModeMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method public static hasGetBuildInDisplayMethod()Z
    .locals 1

    .line 100
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getGetBuiltInDisplayMethod()Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    const/4 v0, 0x1

    return v0

    :catch_0
    const/4 v0, 0x0

    return v0
.end method

.method public static hasGetPhysicalDisplayIdsMethod()Z
    .locals 1

    .line 149
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getGetPhysicalDisplayIdsMethod()Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    const/4 v0, 0x1

    return v0

    :catch_0
    const/4 v0, 0x0

    return v0
.end method

.method public static openTransaction()V
    .locals 3

    .line 42
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "openTransaction"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-virtual {v0, v2, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 44
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1
.end method

.method public static setDisplayLayerStack(Landroid/os/IBinder;I)V
    .locals 7

    .line 67
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "setDisplayLayerStack"

    const/4 v2, 0x2

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Landroid/os/IBinder;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v6, 0x1

    aput-object v4, v3, v6

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    new-array v1, v2, [Ljava/lang/Object;

    aput-object p0, v1, v5

    aput-object p1, v1, v6

    const/4 p0, 0x0

    invoke-virtual {v0, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p0

    .line 69
    new-instance p1, Ljava/lang/AssertionError;

    invoke-direct {p1, p0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method

.method public static setDisplayPowerMode(Landroid/os/IBinder;I)Z
    .locals 3

    const/4 v0, 0x0

    .line 175
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getSetDisplayPowerModeMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 176
    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    const/4 v2, 0x2

    new-array v2, v2, [Ljava/lang/Object;

    aput-object p0, v2, v0

    const/4 p0, 0x1

    aput-object p1, v2, p0

    const/4 p1, 0x0

    invoke-virtual {v1, p1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return p0

    :catch_0
    move-exception p0

    .line 179
    const-string p1, "Could not invoke method"

    invoke-static {p1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method

.method public static setDisplayProjection(Landroid/os/IBinder;ILandroid/graphics/Rect;Landroid/graphics/Rect;)V
    .locals 9

    .line 58
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "setDisplayProjection"

    const/4 v2, 0x4

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Landroid/os/IBinder;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v6, 0x1

    aput-object v4, v3, v6

    const-class v4, Landroid/graphics/Rect;

    const/4 v7, 0x2

    aput-object v4, v3, v7

    const/4 v8, 0x3

    aput-object v4, v3, v8

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    .line 59
    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    new-array v1, v2, [Ljava/lang/Object;

    aput-object p0, v1, v5

    aput-object p1, v1, v6

    aput-object p2, v1, v7

    aput-object p3, v1, v8

    const/4 p0, 0x0

    invoke-virtual {v0, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p0

    .line 61
    new-instance p1, Ljava/lang/AssertionError;

    invoke-direct {p1, p0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method

.method public static setDisplaySurface(Landroid/os/IBinder;Landroid/view/Surface;)V
    .locals 7

    .line 75
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/SurfaceControl;->CLASS:Ljava/lang/Class;

    const-string v1, "setDisplaySurface"

    const/4 v2, 0x2

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Landroid/os/IBinder;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    const-class v4, Landroid/view/Surface;

    const/4 v6, 0x1

    aput-object v4, v3, v6

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    new-array v1, v2, [Ljava/lang/Object;

    aput-object p0, v1, v5

    aput-object p1, v1, v6

    const/4 p0, 0x0

    invoke-virtual {v0, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p0

    .line 77
    new-instance p1, Ljava/lang/AssertionError;

    invoke-direct {p1, p0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method
