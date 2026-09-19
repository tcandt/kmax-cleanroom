.class public final Lcom/android/helper/wrappers/ServiceManager;
.super Ljava/lang/Object;
.source "ServiceManager.java"


# static fields
.field private static final GET_SERVICE_METHOD:Ljava/lang/reflect/Method;

.field private static activityManager:Lcom/android/helper/wrappers/ActivityManager;

.field private static cameraManager:Landroid/hardware/camera2/CameraManager;

.field private static clipboardManager:Lcom/android/helper/wrappers/ClipboardManager;

.field private static displayManager:Lcom/android/helper/wrappers/DisplayManager;

.field private static inputManager:Lcom/android/helper/wrappers/InputManager;

.field private static powerManager:Lcom/android/helper/wrappers/PowerManager;

.field private static statusBarManager:Lcom/android/helper/wrappers/StatusBarManager;

.field private static windowManager:Lcom/android/helper/wrappers/WindowManager;


# direct methods
.method static constructor <clinit>()V
    .locals 5

    .line 21
    :try_start_0
    const-string v0, "android.os.ServiceManager"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    const-string v1, "getService"

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Class;

    const-class v3, Ljava/lang/String;

    const/4 v4, 0x0

    aput-object v3, v2, v4

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->GET_SERVICE_METHOD:Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 23
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

.method public static getActivityManager()Lcom/android/helper/wrappers/ActivityManager;
    .locals 1

    .line 95
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->activityManager:Lcom/android/helper/wrappers/ActivityManager;

    if-nez v0, :cond_0

    .line 96
    invoke-static {}, Lcom/android/helper/wrappers/ActivityManager;->create()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->activityManager:Lcom/android/helper/wrappers/ActivityManager;

    .line 98
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->activityManager:Lcom/android/helper/wrappers/ActivityManager;

    return-object v0
.end method

.method public static getCameraManager()Landroid/hardware/camera2/CameraManager;
    .locals 5

    .line 102
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->cameraManager:Landroid/hardware/camera2/CameraManager;

    if-nez v0, :cond_0

    .line 104
    :try_start_0
    const-class v0, Landroid/hardware/camera2/CameraManager;

    const/4 v1, 0x1

    new-array v2, v1, [Ljava/lang/Class;

    const-class v3, Landroid/content/Context;

    const/4 v4, 0x0

    aput-object v3, v2, v4

    invoke-virtual {v0, v2}, Ljava/lang/Class;->getDeclaredConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v0

    .line 105
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v2

    new-array v1, v1, [Ljava/lang/Object;

    aput-object v2, v1, v4

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/hardware/camera2/CameraManager;

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->cameraManager:Landroid/hardware/camera2/CameraManager;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception v0

    .line 107
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1

    .line 110
    :cond_0
    :goto_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->cameraManager:Landroid/hardware/camera2/CameraManager;

    return-object v0
.end method

.method public static getClipboardManager()Lcom/android/helper/wrappers/ClipboardManager;
    .locals 1

    .line 87
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->clipboardManager:Lcom/android/helper/wrappers/ClipboardManager;

    if-nez v0, :cond_0

    .line 89
    invoke-static {}, Lcom/android/helper/wrappers/ClipboardManager;->create()Lcom/android/helper/wrappers/ClipboardManager;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->clipboardManager:Lcom/android/helper/wrappers/ClipboardManager;

    .line 91
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->clipboardManager:Lcom/android/helper/wrappers/ClipboardManager;

    return-object v0
.end method

.method public static declared-synchronized getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;
    .locals 2

    const-class v0, Lcom/android/helper/wrappers/ServiceManager;

    monitor-enter v0

    .line 59
    :try_start_0
    sget-object v1, Lcom/android/helper/wrappers/ServiceManager;->displayManager:Lcom/android/helper/wrappers/DisplayManager;

    if-nez v1, :cond_0

    .line 60
    invoke-static {}, Lcom/android/helper/wrappers/DisplayManager;->create()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v1

    sput-object v1, Lcom/android/helper/wrappers/ServiceManager;->displayManager:Lcom/android/helper/wrappers/DisplayManager;

    .line 62
    :cond_0
    sget-object v1, Lcom/android/helper/wrappers/ServiceManager;->displayManager:Lcom/android/helper/wrappers/DisplayManager;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    monitor-exit v0

    return-object v1

    :catchall_0
    move-exception v1

    :try_start_1
    monitor-exit v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v1
.end method

.method public static getInputManager()Lcom/android/helper/wrappers/InputManager;
    .locals 1

    .line 66
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->inputManager:Lcom/android/helper/wrappers/InputManager;

    if-nez v0, :cond_0

    .line 67
    invoke-static {}, Lcom/android/helper/wrappers/InputManager;->create()Lcom/android/helper/wrappers/InputManager;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->inputManager:Lcom/android/helper/wrappers/InputManager;

    .line 69
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->inputManager:Lcom/android/helper/wrappers/InputManager;

    return-object v0
.end method

.method public static getPowerManager()Lcom/android/helper/wrappers/PowerManager;
    .locals 1

    .line 73
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->powerManager:Lcom/android/helper/wrappers/PowerManager;

    if-nez v0, :cond_0

    .line 74
    invoke-static {}, Lcom/android/helper/wrappers/PowerManager;->create()Lcom/android/helper/wrappers/PowerManager;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->powerManager:Lcom/android/helper/wrappers/PowerManager;

    .line 76
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->powerManager:Lcom/android/helper/wrappers/PowerManager;

    return-object v0
.end method

.method static getService(Ljava/lang/String;Ljava/lang/String;)Landroid/os/IInterface;
    .locals 6

    .line 42
    :try_start_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->GET_SERVICE_METHOD:Ljava/lang/reflect/Method;

    const/4 v1, 0x1

    new-array v2, v1, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p0, v2, v3

    const/4 p0, 0x0

    invoke-virtual {v0, p0, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/os/IBinder;

    .line 43
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p1, "$Stub"

    invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object p1

    const-string v2, "asInterface"

    new-array v4, v1, [Ljava/lang/Class;

    const-class v5, Landroid/os/IBinder;

    aput-object v5, v4, v3

    invoke-virtual {p1, v2, v4}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object p1

    .line 44
    new-array v1, v1, [Ljava/lang/Object;

    aput-object v0, v1, v3

    invoke-virtual {p1, p0, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Landroid/os/IInterface;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-object p0

    :catch_0
    move-exception p0

    .line 46
    new-instance p1, Ljava/lang/AssertionError;

    invoke-direct {p1, p0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1
.end method

.method public static getStatusBarManager()Lcom/android/helper/wrappers/StatusBarManager;
    .locals 1

    .line 80
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->statusBarManager:Lcom/android/helper/wrappers/StatusBarManager;

    if-nez v0, :cond_0

    .line 81
    invoke-static {}, Lcom/android/helper/wrappers/StatusBarManager;->create()Lcom/android/helper/wrappers/StatusBarManager;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->statusBarManager:Lcom/android/helper/wrappers/StatusBarManager;

    .line 83
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->statusBarManager:Lcom/android/helper/wrappers/StatusBarManager;

    return-object v0
.end method

.method public static getWindowManager()Lcom/android/helper/wrappers/WindowManager;
    .locals 1

    .line 51
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->windowManager:Lcom/android/helper/wrappers/WindowManager;

    if-nez v0, :cond_0

    .line 52
    invoke-static {}, Lcom/android/helper/wrappers/WindowManager;->create()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/ServiceManager;->windowManager:Lcom/android/helper/wrappers/WindowManager;

    .line 54
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/ServiceManager;->windowManager:Lcom/android/helper/wrappers/WindowManager;

    return-object v0
.end method
