.class public Lcom/android/helper/video/DisplaySizeMonitor;
.super Ljava/lang/Object;
.source "DisplaySizeMonitor.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/video/DisplaySizeMonitor$Listener;
    }
.end annotation


# static fields
.field static final synthetic $assertionsDisabled:Z

.field private static final USE_DEFAULT_METHOD:Z


# instance fields
.field private displayId:I

.field private displayListenerHandle:Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;

.field private displayWindowListener:Landroid/view/IDisplayWindowListener;

.field private handlerThread:Landroid/os/HandlerThread;

.field private listener:Lcom/android/helper/video/DisplaySizeMonitor$Listener;

.field private sessionDisplaySize:Lcom/android/helper/device/Size;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 28
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x22

    if-ge v0, v1, :cond_0

    const/4 v0, 0x1

    goto :goto_0

    :cond_0
    const/4 v0, 0x0

    :goto_0
    sput-boolean v0, Lcom/android/helper/video/DisplaySizeMonitor;->USE_DEFAULT_METHOD:Z

    return-void
.end method

.method public constructor <init>()V
    .locals 1

    .line 18
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/4 v0, -0x1

    .line 35
    iput v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayId:I

    return-void
.end method

.method static synthetic access$000(Lcom/android/helper/video/DisplaySizeMonitor;)V
    .locals 0

    .line 18
    invoke-direct {p0}, Lcom/android/helper/video/DisplaySizeMonitor;->checkDisplaySizeChanged()V

    return-void
.end method

.method private checkDisplaySizeChanged()V
    .locals 4

    .line 110
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    iget v1, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayId:I

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/DisplayManager;->getDisplayInfo(I)Lcom/android/helper/device/DisplayInfo;

    move-result-object v0

    .line 111
    const-string v1, "DisplaySizeMonitor: requestReset(): "

    if-nez v0, :cond_1

    .line 112
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v2, "DisplayInfo for "

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v2, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayId:I

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v2, " cannot be retrieved"

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 114
    sget-object v0, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {v0}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 115
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-direct {p0}, Lcom/android/helper/video/DisplaySizeMonitor;->getSessionDisplaySize()Lcom/android/helper/device/Size;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v1, " -> (unknown)"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->v(Ljava/lang/String;)V

    :cond_0
    const/4 v0, 0x0

    .line 117
    invoke-virtual {p0, v0}, Lcom/android/helper/video/DisplaySizeMonitor;->setSessionDisplaySize(Lcom/android/helper/device/Size;)V

    .line 118
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->listener:Lcom/android/helper/video/DisplaySizeMonitor$Listener;

    invoke-interface {v0}, Lcom/android/helper/video/DisplaySizeMonitor$Listener;->onDisplaySizeChanged()V

    return-void

    .line 120
    :cond_1
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getSize()Lcom/android/helper/device/Size;

    move-result-object v0

    .line 124
    invoke-direct {p0}, Lcom/android/helper/video/DisplaySizeMonitor;->getSessionDisplaySize()Lcom/android/helper/device/Size;

    move-result-object v2

    .line 127
    invoke-virtual {v0, v2}, Lcom/android/helper/device/Size;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-nez v3, :cond_3

    .line 129
    sget-object v3, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {v3}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v3

    if-eqz v3, :cond_2

    .line 130
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v1, " -> "

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lcom/android/helper/util/Ln;->v(Ljava/lang/String;)V

    .line 134
    :cond_2
    invoke-virtual {p0, v0}, Lcom/android/helper/video/DisplaySizeMonitor;->setSessionDisplaySize(Lcom/android/helper/device/Size;)V

    .line 135
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->listener:Lcom/android/helper/video/DisplaySizeMonitor$Listener;

    invoke-interface {v0}, Lcom/android/helper/video/DisplaySizeMonitor$Listener;->onDisplaySizeChanged()V

    return-void

    .line 136
    :cond_3
    sget-object v1, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {v1}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v1

    if-eqz v1, :cond_4

    .line 137
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "DisplaySizeMonitor: Size not changed ("

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v0, "): do not requestReset()"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->v(Ljava/lang/String;)V

    :cond_4
    return-void
.end method

.method private declared-synchronized getSessionDisplaySize()Lcom/android/helper/device/Size;
    .locals 1

    monitor-enter p0

    .line 102
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->sessionDisplaySize:Lcom/android/helper/device/Size;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    monitor-exit p0

    return-object v0

    :catchall_0
    move-exception v0

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v0
.end method


# virtual methods
.method synthetic lambda$start$0$com-android-helper-video-DisplaySizeMonitor(II)V
    .locals 2

    .line 54
    sget-object v0, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {v0}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 55
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "DisplaySizeMonitor: onDisplayChanged("

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, ")"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->v(Ljava/lang/String;)V

    :cond_0
    if-ne p2, p1, :cond_1

    .line 59
    invoke-direct {p0}, Lcom/android/helper/video/DisplaySizeMonitor;->checkDisplaySizeChanged()V

    :cond_1
    return-void
.end method

.method public declared-synchronized setSessionDisplaySize(Lcom/android/helper/device/Size;)V
    .locals 0

    monitor-enter p0

    .line 106
    :try_start_0
    iput-object p1, p0, Lcom/android/helper/video/DisplaySizeMonitor;->sessionDisplaySize:Lcom/android/helper/device/Size;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 107
    monitor-exit p0

    return-void

    :catchall_0
    move-exception p1

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw p1
.end method

.method public start(ILcom/android/helper/video/DisplaySizeMonitor$Listener;)V
    .locals 2

    .line 44
    iput-object p2, p0, Lcom/android/helper/video/DisplaySizeMonitor;->listener:Lcom/android/helper/video/DisplaySizeMonitor$Listener;

    .line 47
    iput p1, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayId:I

    .line 49
    sget-boolean p2, Lcom/android/helper/video/DisplaySizeMonitor;->USE_DEFAULT_METHOD:Z

    if-eqz p2, :cond_0

    .line 50
    new-instance p2, Landroid/os/HandlerThread;

    const-string v0, "DisplayListener"

    invoke-direct {p2, v0}, Landroid/os/HandlerThread;-><init>(Ljava/lang/String;)V

    iput-object p2, p0, Lcom/android/helper/video/DisplaySizeMonitor;->handlerThread:Landroid/os/HandlerThread;

    .line 51
    invoke-virtual {p2}, Landroid/os/HandlerThread;->start()V

    .line 52
    new-instance p2, Landroid/os/Handler;

    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->handlerThread:Landroid/os/HandlerThread;

    invoke-virtual {v0}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object v0

    invoke-direct {p2, v0}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    .line 53
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    new-instance v1, Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/video/DisplaySizeMonitor$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/video/DisplaySizeMonitor;I)V

    invoke-virtual {v0, v1, p2}, Lcom/android/helper/wrappers/DisplayManager;->registerDisplayListener(Lcom/android/helper/wrappers/DisplayManager$DisplayListener;Landroid/os/Handler;)Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayListenerHandle:Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;

    return-void

    .line 63
    :cond_0
    new-instance p2, Lcom/android/helper/video/DisplaySizeMonitor$1;

    invoke-direct {p2, p0, p1}, Lcom/android/helper/video/DisplaySizeMonitor$1;-><init>(Lcom/android/helper/video/DisplaySizeMonitor;I)V

    iput-object p2, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayWindowListener:Landroid/view/IDisplayWindowListener;

    .line 75
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object p1

    iget-object p2, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayWindowListener:Landroid/view/IDisplayWindowListener;

    invoke-virtual {p1, p2}, Lcom/android/helper/wrappers/WindowManager;->registerDisplayWindowListener(Landroid/view/IDisplayWindowListener;)[I

    return-void
.end method

.method public stopAndRelease()V
    .locals 2

    .line 86
    sget-boolean v0, Lcom/android/helper/video/DisplaySizeMonitor;->USE_DEFAULT_METHOD:Z

    if-eqz v0, :cond_1

    .line 88
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayListenerHandle:Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;

    if-eqz v0, :cond_0

    .line 89
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    iget-object v1, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayListenerHandle:Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/DisplayManager;->unregisterDisplayListener(Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;)V

    const/4 v0, 0x0

    .line 90
    iput-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayListenerHandle:Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;

    .line 93
    :cond_0
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->handlerThread:Landroid/os/HandlerThread;

    if-eqz v0, :cond_2

    .line 94
    invoke-virtual {v0}, Landroid/os/HandlerThread;->quitSafely()Z

    return-void

    .line 96
    :cond_1
    iget-object v0, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayWindowListener:Landroid/view/IDisplayWindowListener;

    if-eqz v0, :cond_2

    .line 97
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v0

    iget-object v1, p0, Lcom/android/helper/video/DisplaySizeMonitor;->displayWindowListener:Landroid/view/IDisplayWindowListener;

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/WindowManager;->unregisterDisplayWindowListener(Landroid/view/IDisplayWindowListener;)V

    :cond_2
    return-void
.end method
