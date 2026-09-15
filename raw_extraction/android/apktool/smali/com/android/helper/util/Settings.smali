.class public final Lcom/android/helper/util/Settings;
.super Ljava/lang/Object;
.source "Settings.java"


# static fields
.field public static final TABLE_GLOBAL:Ljava/lang/String; = "global"

.field public static final TABLE_SECURE:Ljava/lang/String; = "secure"

.field public static final TABLE_SYSTEM:Ljava/lang/String; = "system"


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 12
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static getAndPutValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/util/SettingsException;
        }
    .end annotation

    .line 30
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/wrappers/ActivityManager;->createSettingsProvider()Lcom/android/helper/wrappers/ContentProvider;

    move-result-object v0

    .line 31
    :try_start_0
    invoke-virtual {v0, p0, p1}, Lcom/android/helper/wrappers/ContentProvider;->getValue(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 32
    invoke-virtual {p2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_0

    .line 33
    invoke-virtual {v0, p0, p1, p2}, Lcom/android/helper/wrappers/ContentProvider;->putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :cond_0
    if-eqz v0, :cond_1

    .line 36
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ContentProvider;->close()V

    :cond_1
    return-object v1

    :catchall_0
    move-exception p0

    if-eqz v0, :cond_2

    .line 30
    :try_start_1
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ContentProvider;->close()V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    goto :goto_0

    :catchall_1
    move-exception p1

    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_2
    :goto_0
    throw p0
.end method

.method public static getValue(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/util/SettingsException;
        }
    .end annotation

    .line 17
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/wrappers/ActivityManager;->createSettingsProvider()Lcom/android/helper/wrappers/ContentProvider;

    move-result-object v0

    .line 18
    :try_start_0
    invoke-virtual {v0, p0, p1}, Lcom/android/helper/wrappers/ContentProvider;->getValue(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v0, :cond_0

    .line 19
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ContentProvider;->close()V

    :cond_0
    return-object p0

    :catchall_0
    move-exception p0

    if-eqz v0, :cond_1

    .line 17
    :try_start_1
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ContentProvider;->close()V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    goto :goto_0

    :catchall_1
    move-exception p1

    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_1
    :goto_0
    throw p0
.end method

.method public static putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/util/SettingsException;
        }
    .end annotation

    .line 23
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/wrappers/ActivityManager;->createSettingsProvider()Lcom/android/helper/wrappers/ContentProvider;

    move-result-object v0

    .line 24
    :try_start_0
    invoke-virtual {v0, p0, p1, p2}, Lcom/android/helper/wrappers/ContentProvider;->putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-eqz v0, :cond_0

    .line 25
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ContentProvider;->close()V

    :cond_0
    return-void

    :catchall_0
    move-exception p0

    if-eqz v0, :cond_1

    .line 23
    :try_start_1
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ContentProvider;->close()V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    goto :goto_0

    :catchall_1
    move-exception p1

    invoke-virtual {p0, p1}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :cond_1
    :goto_0
    throw p0
.end method
