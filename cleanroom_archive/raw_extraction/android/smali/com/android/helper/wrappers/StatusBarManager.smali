.class public final Lcom/android/helper/wrappers/StatusBarManager;
.super Ljava/lang/Object;
.source "StatusBarManager.java"


# instance fields
.field private collapsePanelsMethod:Ljava/lang/reflect/Method;

.field private expandNotificationPanelMethodCustomVersion:Z

.field private expandNotificationsPanelMethod:Ljava/lang/reflect/Method;

.field private expandSettingsPanelMethod:Ljava/lang/reflect/Method;

.field private expandSettingsPanelMethodNewVersion:Z

.field private final manager:Landroid/os/IInterface;


# direct methods
.method private constructor <init>(Landroid/os/IInterface;)V
    .locals 1

    .line 23
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/4 v0, 0x1

    .line 15
    iput-boolean v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethodNewVersion:Z

    .line 24
    iput-object p1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    return-void
.end method

.method static create()Lcom/android/helper/wrappers/StatusBarManager;
    .locals 2

    .line 19
    const-string v0, "statusbar"

    const-string v1, "com.android.internal.statusbar.IStatusBarService"

    invoke-static {v0, v1}, Lcom/android/helper/wrappers/ServiceManager;->getService(Ljava/lang/String;Ljava/lang/String;)Landroid/os/IInterface;

    move-result-object v0

    .line 20
    new-instance v1, Lcom/android/helper/wrappers/StatusBarManager;

    invoke-direct {v1, v0}, Lcom/android/helper/wrappers/StatusBarManager;-><init>(Landroid/os/IInterface;)V

    return-object v1
.end method

.method private getCollapsePanelsMethod()Ljava/lang/reflect/Method;
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 55
    iget-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->collapsePanelsMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 56
    iget-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const-string v1, "collapsePanels"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->collapsePanelsMethod:Ljava/lang/reflect/Method;

    .line 58
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->collapsePanelsMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getExpandNotificationsPanelMethod()Ljava/lang/reflect/Method;
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 28
    const-string v0, "expandNotificationsPanel"

    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationsPanelMethod:Ljava/lang/reflect/Method;

    if-nez v1, :cond_0

    .line 30
    :try_start_0
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const/4 v2, 0x0

    invoke-virtual {v1, v0, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationsPanelMethod:Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 33
    :catch_0
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const/4 v2, 0x1

    new-array v3, v2, [Ljava/lang/Class;

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    invoke-virtual {v1, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationsPanelMethod:Ljava/lang/reflect/Method;

    .line 34
    iput-boolean v2, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationPanelMethodCustomVersion:Z

    .line 37
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationsPanelMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getExpandSettingsPanel()Ljava/lang/reflect/Method;
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 41
    const-string v0, "expandSettingsPanel"

    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethod:Ljava/lang/reflect/Method;

    if-nez v1, :cond_0

    const/4 v1, 0x0

    .line 44
    :try_start_0
    iget-object v2, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v2

    const/4 v3, 0x1

    new-array v3, v3, [Ljava/lang/Class;

    const-class v4, Ljava/lang/String;

    aput-object v4, v3, v1

    invoke-virtual {v2, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    iput-object v2, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethod:Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 47
    :catch_0
    iget-object v2, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v2

    const/4 v3, 0x0

    invoke-virtual {v2, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethod:Ljava/lang/reflect/Method;

    .line 48
    iput-boolean v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethodNewVersion:Z

    .line 51
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method


# virtual methods
.method public collapsePanels()V
    .locals 3

    .line 91
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/StatusBarManager;->getCollapsePanelsMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 92
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 94
    const-string v1, "Could not invoke method"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public expandNotificationsPanel()V
    .locals 5

    .line 63
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/StatusBarManager;->getExpandNotificationsPanelMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 64
    iget-boolean v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationPanelMethodCustomVersion:Z

    if-eqz v1, :cond_0

    .line 65
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x0

    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    const/4 v4, 0x1

    new-array v4, v4, [Ljava/lang/Object;

    aput-object v3, v4, v2

    invoke-virtual {v0, v1, v4}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 67
    :cond_0
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 70
    const-string v1, "Could not invoke method"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public expandSettingsPanel()V
    .locals 5

    .line 76
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/StatusBarManager;->getExpandSettingsPanel()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 77
    iget-boolean v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanelMethodNewVersion:Z

    const/4 v2, 0x0

    if-eqz v1, :cond_0

    .line 79
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    const/4 v3, 0x1

    new-array v3, v3, [Ljava/lang/Object;

    const/4 v4, 0x0

    aput-object v2, v3, v4

    invoke-virtual {v0, v1, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 82
    :cond_0
    iget-object v1, p0, Lcom/android/helper/wrappers/StatusBarManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 85
    const-string v1, "Could not invoke method"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method
