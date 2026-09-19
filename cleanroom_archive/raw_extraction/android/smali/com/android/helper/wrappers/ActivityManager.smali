.class public final Lcom/android/helper/wrappers/ActivityManager;
.super Ljava/lang/Object;
.source "ActivityManager.java"


# instance fields
.field private forceStopPackageMethod:Ljava/lang/reflect/Method;

.field private getContentProviderExternalMethod:Ljava/lang/reflect/Method;

.field private getContentProviderExternalMethodNewVersion:Z

.field private final manager:Landroid/os/IInterface;

.field private removeContentProviderExternalMethod:Ljava/lang/reflect/Method;

.field private startActivityAsUserMethod:Ljava/lang/reflect/Method;


# direct methods
.method private constructor <init>(Landroid/os/IInterface;)V
    .locals 1

    .line 42
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/4 v0, 0x1

    .line 24
    iput-boolean v0, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethodNewVersion:Z

    .line 43
    iput-object p1, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    return-void
.end method

.method static create()Lcom/android/helper/wrappers/ActivityManager;
    .locals 3

    .line 33
    :try_start_0
    const-string v0, "android.app.ActivityManagerNative"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 34
    const-string v1, "getDefault"

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    .line 35
    invoke-virtual {v0, v2, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/os/IInterface;

    .line 36
    new-instance v1, Lcom/android/helper/wrappers/ActivityManager;

    invoke-direct {v1, v0}, Lcom/android/helper/wrappers/ActivityManager;-><init>(Landroid/os/IInterface;)V
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object v1

    :catch_0
    move-exception v0

    .line 38
    new-instance v1, Ljava/lang/AssertionError;

    invoke-direct {v1, v0}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw v1
.end method

.method private getForceStopPackageMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 151
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->forceStopPackageMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 152
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x2

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Ljava/lang/String;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "forceStopPackage"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->forceStopPackageMethod:Ljava/lang/reflect/Method;

    .line 154
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->forceStopPackageMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getGetContentProviderExternalMethod()Ljava/lang/reflect/Method;
    .locals 9
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 47
    const-string v0, "getContentProviderExternal"

    iget-object v1, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethod:Ljava/lang/reflect/Method;

    if-nez v1, :cond_0

    const/4 v1, 0x2

    const/4 v2, 0x1

    const/4 v3, 0x3

    const/4 v4, 0x0

    .line 49
    :try_start_0
    iget-object v5, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    const/4 v6, 0x4

    new-array v6, v6, [Ljava/lang/Class;

    const-class v7, Ljava/lang/String;

    aput-object v7, v6, v4

    sget-object v8, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v8, v6, v2

    const-class v8, Landroid/os/IBinder;

    aput-object v8, v6, v1

    aput-object v7, v6, v3

    .line 50
    invoke-virtual {v5, v0, v6}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v5

    iput-object v5, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethod:Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 53
    :catch_0
    iget-object v5, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v5}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v5

    new-array v3, v3, [Ljava/lang/Class;

    const-class v6, Ljava/lang/String;

    aput-object v6, v3, v4

    sget-object v6, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v6, v3, v2

    const-class v2, Landroid/os/IBinder;

    aput-object v2, v3, v1

    invoke-virtual {v5, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethod:Ljava/lang/reflect/Method;

    .line 54
    iput-boolean v4, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethodNewVersion:Z

    .line 57
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getRemoveContentProviderExternalMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 61
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->removeContentProviderExternalMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 62
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x2

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Ljava/lang/String;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-class v2, Landroid/os/IBinder;

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "removeContentProviderExternal"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->removeContentProviderExternalMethod:Ljava/lang/reflect/Method;

    .line 64
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->removeContentProviderExternalMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getStartActivityAsUserMethod()Ljava/lang/reflect/Method;
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;,
            Ljava/lang/ClassNotFoundException;
        }
    .end annotation

    .line 113
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->startActivityAsUserMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 114
    const-string v0, "android.app.IApplicationThread"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 115
    const-string v1, "android.app.ProfilerInfo"

    invoke-static {v1}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v1

    .line 116
    iget-object v2, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v2}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v2

    const/16 v3, 0xb

    new-array v3, v3, [Ljava/lang/Class;

    const/4 v4, 0x0

    aput-object v0, v3, v4

    const-class v0, Ljava/lang/String;

    const/4 v4, 0x1

    aput-object v0, v3, v4

    const-class v4, Landroid/content/Intent;

    const/4 v5, 0x2

    aput-object v4, v3, v5

    const/4 v4, 0x3

    aput-object v0, v3, v4

    const-class v4, Landroid/os/IBinder;

    const/4 v5, 0x4

    aput-object v4, v3, v5

    const/4 v4, 0x5

    aput-object v0, v3, v4

    sget-object v0, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v4, 0x6

    aput-object v0, v3, v4

    const/4 v4, 0x7

    aput-object v0, v3, v4

    const/16 v4, 0x8

    aput-object v1, v3, v4

    const-class v1, Landroid/os/Bundle;

    const/16 v4, 0x9

    aput-object v1, v3, v4

    const/16 v1, 0xa

    aput-object v0, v3, v1

    .line 117
    const-string v0, "startActivityAsUser"

    invoke-virtual {v2, v0, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->startActivityAsUserMethod:Ljava/lang/reflect/Method;

    .line 120
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ActivityManager;->startActivityAsUserMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method


# virtual methods
.method public createSettingsProvider()Lcom/android/helper/wrappers/ContentProvider;
    .locals 4

    .line 104
    new-instance v0, Landroid/os/Binder;

    invoke-direct {v0}, Landroid/os/Binder;-><init>()V

    .line 105
    const-string v1, "settings"

    invoke-virtual {p0, v1, v0}, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternal(Ljava/lang/String;Landroid/os/IBinder;)Landroid/content/IContentProvider;

    move-result-object v2

    if-nez v2, :cond_0

    const/4 v0, 0x0

    return-object v0

    .line 109
    :cond_0
    new-instance v3, Lcom/android/helper/wrappers/ContentProvider;

    invoke-direct {v3, p0, v2, v1, v0}, Lcom/android/helper/wrappers/ContentProvider;-><init>(Lcom/android/helper/wrappers/ActivityManager;Ljava/lang/Object;Ljava/lang/String;Landroid/os/IBinder;)V

    return-object v3
.end method

.method public forceStopPackage(Ljava/lang/String;)V
    .locals 5

    .line 159
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/ActivityManager;->getForceStopPackageMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 160
    iget-object v1, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    const/4 v2, -0x2

    invoke-static {v2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    const/4 v3, 0x2

    new-array v3, v3, [Ljava/lang/Object;

    const/4 v4, 0x0

    aput-object p1, v3, v4

    const/4 p1, 0x1

    aput-object v2, v3, p1

    invoke-virtual {v0, v1, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-void

    :catchall_0
    move-exception p1

    .line 162
    const-string v0, "Could not invoke method"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public getContentProviderExternal(Ljava/lang/String;Landroid/os/IBinder;)Landroid/content/IContentProvider;
    .locals 8

    const/4 v0, 0x0

    .line 70
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/ActivityManager;->getGetContentProviderExternalMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 72
    iget-boolean v2, p0, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternalMethodNewVersion:Z

    const/4 v3, 0x2

    const/4 v4, 0x3

    const/4 v5, 0x1

    const/4 v6, 0x0

    if-eqz v2, :cond_0

    .line 74
    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    const/4 v7, 0x4

    new-array v7, v7, [Ljava/lang/Object;

    aput-object p1, v7, v6

    aput-object v2, v7, v5

    aput-object p2, v7, v3

    aput-object v0, v7, v4

    goto :goto_0

    .line 77
    :cond_0
    invoke-static {v6}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    new-array v7, v4, [Ljava/lang/Object;

    aput-object p1, v7, v6

    aput-object v2, v7, v5

    aput-object p2, v7, v3

    .line 80
    :goto_0
    iget-object p1, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v1, p1, v7}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    if-nez p1, :cond_1

    return-object v0

    .line 85
    :cond_1
    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object p2

    const-string v1, "provider"

    invoke-virtual {p2, v1}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object p2

    .line 86
    invoke-virtual {p2, v5}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 87
    invoke-virtual {p2, p1}, Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/content/IContentProvider;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object p1

    :catch_0
    move-exception p1

    .line 89
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method removeContentProviderExternal(Ljava/lang/String;Landroid/os/IBinder;)V
    .locals 4

    .line 96
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/ActivityManager;->getRemoveContentProviderExternalMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 97
    iget-object v1, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x2

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    const/4 p1, 0x1

    aput-object p2, v2, p1

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 99
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public startActivity(Landroid/content/Intent;)I
    .locals 1

    const/4 v0, 0x0

    .line 124
    invoke-virtual {p0, p1, v0}, Lcom/android/helper/wrappers/ActivityManager;->startActivity(Landroid/content/Intent;Landroid/os/Bundle;)I

    move-result p1

    return p1
.end method

.method public startActivity(Landroid/content/Intent;Landroid/os/Bundle;)I
    .locals 10

    const/4 v0, 0x0

    .line 130
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/ActivityManager;->getStartActivityAsUserMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 131
    iget-object v2, p0, Lcom/android/helper/wrappers/ActivityManager;->manager:Landroid/os/IInterface;

    .line 139
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v3

    .line 140
    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v4

    const/4 v5, -0x2

    .line 143
    invoke-static {v5}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v5

    const/16 v6, 0xb

    new-array v6, v6, [Ljava/lang/Object;

    const/4 v7, 0x0

    aput-object v7, v6, v0

    const-string v8, "com.android.shell"

    const/4 v9, 0x1

    aput-object v8, v6, v9

    const/4 v8, 0x2

    aput-object p1, v6, v8

    const/4 p1, 0x3

    aput-object v7, v6, p1

    const/4 p1, 0x4

    aput-object v7, v6, p1

    const/4 p1, 0x5

    aput-object v7, v6, p1

    const/4 p1, 0x6

    aput-object v3, v6, p1

    const/4 p1, 0x7

    aput-object v4, v6, p1

    const/16 p1, 0x8

    aput-object v7, v6, p1

    const/16 p1, 0x9

    aput-object p2, v6, p1

    const/16 p1, 0xa

    aput-object v5, v6, p1

    .line 131
    invoke-virtual {v1, v2, v6}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Integer;

    invoke-virtual {p1}, Ljava/lang/Integer;->intValue()I

    move-result p1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return p1

    :catchall_0
    move-exception p1

    .line 145
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method
