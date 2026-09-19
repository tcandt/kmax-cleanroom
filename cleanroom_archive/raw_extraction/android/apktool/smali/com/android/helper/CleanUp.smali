.class public final Lcom/android/helper/CleanUp;
.super Ljava/lang/Object;
.source "CleanUp.java"


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field private static final PENDING_CHANGE_DISPLAY_POWER:I = 0x1


# instance fields
.field private interrupted:Z

.field private pendingChanges:I

.field private pendingRestoreDisplayPower:Z

.field private thread:Ljava/lang/Thread;


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method private constructor <init>(Lcom/android/helper/Options;)V
    .locals 2

    .line 33
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 34
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/android/helper/CleanUp$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/CleanUp$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/CleanUp;Lcom/android/helper/Options;)V

    const-string p1, "cleanup"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v0, p0, Lcom/android/helper/CleanUp;->thread:Ljava/lang/Thread;

    .line 35
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method public static varargs main([Ljava/lang/String;)V
    .locals 11

    .line 191
    :try_start_0
    invoke-static {}, Landroid/system/Os;->setsid()I
    :try_end_0
    .catch Landroid/system/ErrnoException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception v0

    .line 193
    const-string v1, "setsid() failed"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 195
    :goto_0
    invoke-static {}, Lcom/android/helper/CleanUp;->unlinkSelf()V

    .line 198
    invoke-static {}, Lcom/android/helper/CleanUp;->prepareMainLooper()V

    .line 199
    invoke-static {}, Lcom/android/helper/Workarounds;->apply()V

    const/4 v0, 0x0

    .line 201
    aget-object v1, p0, v0

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    const/4 v2, 0x1

    .line 202
    aget-object v3, p0, v2

    invoke-static {v3}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v3

    const/4 v4, 0x2

    .line 203
    aget-object v4, p0, v4

    invoke-static {v4}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result v4

    const/4 v5, 0x3

    .line 204
    aget-object v5, p0, v5

    invoke-static {v5}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result v5

    const/4 v6, 0x4

    .line 205
    aget-object v6, p0, v6

    invoke-static {v6}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v6

    const/4 v7, 0x5

    .line 206
    aget-object p0, p0, v7

    invoke-static {p0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p0

    :cond_0
    const/4 v7, 0x0

    :goto_1
    const/4 v8, -0x1

    .line 214
    :try_start_1
    sget-object v9, Ljava/lang/System;->in:Ljava/io/InputStream;

    invoke-virtual {v9}, Ljava/io/InputStream;->read()I

    move-result v9
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_1

    if-eq v9, v8, :cond_1

    if-eqz v9, :cond_0

    const/4 v7, 0x1

    goto :goto_1

    :catch_1
    nop

    .line 223
    :cond_1
    const-string v9, "Cleaning up"

    invoke-static {v9}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 225
    const-string v9, "system"

    if-eqz v4, :cond_2

    .line 226
    const-string v4, "Disabling \"show touches\""

    invoke-static {v4}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 228
    :try_start_2
    const-string v4, "show_touches"

    const-string v10, "0"

    invoke-static {v9, v4, v10}, Lcom/android/helper/util/Settings;->putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_2
    .catch Lcom/android/helper/util/SettingsException; {:try_start_2 .. :try_end_2} :catch_2

    goto :goto_2

    :catch_2
    move-exception v4

    .line 230
    const-string v10, "Could not restore \"show_touches\""

    invoke-static {v10, v4}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_2
    :goto_2
    if-eq v3, v8, :cond_3

    .line 235
    const-string v4, "Restoring \"stay awake\""

    invoke-static {v4}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 237
    :try_start_3
    const-string v4, "global"

    const-string v10, "stay_on_while_plugged_in"

    invoke-static {v3}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v3

    invoke-static {v4, v10, v3}, Lcom/android/helper/util/Settings;->putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_3
    .catch Lcom/android/helper/util/SettingsException; {:try_start_3 .. :try_end_3} :catch_3

    goto :goto_3

    :catch_3
    move-exception v3

    .line 239
    const-string v4, "Could not restore \"stay_on_while_plugged_in\""

    invoke-static {v4, v3}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_3
    :goto_3
    if-eq v6, v8, :cond_4

    .line 244
    const-string v3, "Restoring \"screen off timeout\""

    invoke-static {v3}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 246
    :try_start_4
    const-string v3, "screen_off_timeout"

    invoke-static {v6}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v9, v3, v4}, Lcom/android/helper/util/Settings;->putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    :try_end_4
    .catch Lcom/android/helper/util/SettingsException; {:try_start_4 .. :try_end_4} :catch_4

    goto :goto_4

    :catch_4
    move-exception v3

    .line 248
    const-string v4, "Could not restore \"screen_off_timeout\""

    invoke-static {v4, v3}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_4
    :goto_4
    if-eq p0, v8, :cond_5

    .line 253
    const-string v3, "Restoring \"display IME policy\""

    invoke-static {v3}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 254
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v3

    invoke-virtual {v3, v1, p0}, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicy(II)V

    :cond_5
    if-eq v1, v8, :cond_6

    goto :goto_5

    :cond_6
    const/4 v1, 0x0

    .line 259
    :goto_5
    invoke-static {v1}, Lcom/android/helper/device/Device;->isScreenOn(I)Z

    move-result p0

    if-eqz p0, :cond_8

    if-eqz v5, :cond_7

    .line 261
    const-string p0, "Power off screen"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 262
    invoke-static {v1}, Lcom/android/helper/device/Device;->powerOffScreen(I)Z

    goto :goto_6

    :cond_7
    if-eqz v7, :cond_8

    .line 264
    const-string p0, "Restoring display power"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 265
    invoke-static {v1, v2}, Lcom/android/helper/device/Device;->setDisplayPower(IZ)Z

    .line 269
    :cond_8
    :goto_6
    invoke-static {v0}, Ljava/lang/System;->exit(I)V

    return-void
.end method

.method private static prepareMainLooper()V
    .locals 0

    .line 185
    invoke-static {}, Landroid/os/Looper;->prepareMainLooper()V

    return-void
.end method

.method private run(IIZZII)V
    .locals 9
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 127
    const-string v0, "app_process"

    const-string v1, "/"

    const-class v2, Lcom/android/helper/CleanUp;

    .line 130
    invoke-virtual {v2}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v2

    .line 131
    invoke-static {p1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v3

    .line 132
    invoke-static {p2}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v4

    .line 133
    invoke-static {p3}, Ljava/lang/String;->valueOf(Z)Ljava/lang/String;

    move-result-object v5

    .line 134
    invoke-static {p4}, Ljava/lang/String;->valueOf(Z)Ljava/lang/String;

    move-result-object v6

    .line 135
    invoke-static {p5}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v7

    .line 136
    invoke-static {p6}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v8

    filled-new-array/range {v0 .. v8}, [Ljava/lang/String;

    move-result-object p1

    .line 139
    new-instance p2, Ljava/lang/ProcessBuilder;

    invoke-direct {p2, p1}, Ljava/lang/ProcessBuilder;-><init>([Ljava/lang/String;)V

    .line 140
    invoke-virtual {p2}, Ljava/lang/ProcessBuilder;->environment()Ljava/util/Map;

    move-result-object p1

    const-string p3, "CLASSPATH"

    sget-object p4, Lcom/android/helper/CoreService;->SERVER_PATH:Ljava/lang/String;

    invoke-interface {p1, p3, p4}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 141
    invoke-virtual {p2}, Ljava/lang/ProcessBuilder;->start()Ljava/lang/Process;

    move-result-object p1

    .line 142
    invoke-virtual {p1}, Ljava/lang/Process;->getOutputStream()Ljava/io/OutputStream;

    move-result-object p1

    .line 147
    :cond_0
    :goto_0
    monitor-enter p0

    .line 148
    :goto_1
    :try_start_0
    iget-boolean p2, p0, Lcom/android/helper/CleanUp;->interrupted:Z

    if-nez p2, :cond_1

    iget p3, p0, Lcom/android/helper/CleanUp;->pendingChanges:I
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    if-nez p3, :cond_1

    .line 150
    :try_start_1
    invoke-virtual {p0}, Ljava/lang/Object;->wait()V
    :try_end_1
    .catch Ljava/lang/InterruptedException; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_1

    .line 152
    :catch_0
    :try_start_2
    new-instance p1, Ljava/lang/AssertionError;

    const-string p2, "Clean up thread MUST NOT be interrupted"

    invoke-direct {p1, p2}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p1

    :cond_1
    if-eqz p2, :cond_2

    .line 156
    monitor-exit p0

    return-void

    .line 158
    :cond_2
    iget p2, p0, Lcom/android/helper/CleanUp;->pendingChanges:I

    .line 159
    iget-boolean p3, p0, Lcom/android/helper/CleanUp;->pendingRestoreDisplayPower:Z

    const/4 p4, 0x0

    .line 160
    iput p4, p0, Lcom/android/helper/CleanUp;->pendingChanges:I

    .line 161
    monitor-exit p0
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    and-int/lit8 p2, p2, 0x1

    if-eqz p2, :cond_0

    .line 163
    invoke-virtual {p1, p3}, Ljava/io/OutputStream;->write(I)V

    .line 164
    invoke-virtual {p1}, Ljava/io/OutputStream;->flush()V

    goto :goto_0

    :catchall_0
    move-exception v0

    move-object p1, v0

    .line 161
    :try_start_3
    monitor-exit p0
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_0

    throw p1
.end method

.method private runCleanUp(Lcom/android/helper/Options;)V
    .locals 10

    .line 53
    const-string v0, "1"

    .line 54
    invoke-virtual {p1}, Lcom/android/helper/Options;->getShowTouches()Z

    move-result v1

    const-string v2, "system"

    if-eqz v1, :cond_0

    .line 56
    :try_start_0
    const-string v1, "show_touches"

    invoke-static {v2, v1, v0}, Lcom/android/helper/util/Settings;->getAndPutValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 58
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0
    :try_end_0
    .catch Lcom/android/helper/util/SettingsException; {:try_start_0 .. :try_end_0} :catch_0

    xor-int/lit8 v0, v0, 0x1

    move v6, v0

    goto :goto_0

    :catch_0
    move-exception v0

    .line 60
    const-string v1, "Could not change \"show_touches\""

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_0
    const/4 v0, 0x0

    const/4 v6, 0x0

    .line 65
    :goto_0
    invoke-virtual {p1}, Lcom/android/helper/Options;->getStayAwake()Z

    move-result v0

    const/4 v1, -0x1

    if-eqz v0, :cond_2

    .line 68
    :try_start_1
    const-string v0, "global"

    const-string v3, "stay_on_while_plugged_in"

    const/4 v4, 0x7

    invoke-static {v4}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v5

    invoke-static {v0, v3, v5}, Lcom/android/helper/util/Settings;->getAndPutValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0
    :try_end_1
    .catch Lcom/android/helper/util/SettingsException; {:try_start_1 .. :try_end_1} :catch_2

    .line 70
    :try_start_2
    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0
    :try_end_2
    .catch Ljava/lang/NumberFormatException; {:try_start_2 .. :try_end_2} :catch_1
    .catch Lcom/android/helper/util/SettingsException; {:try_start_2 .. :try_end_2} :catch_2

    if-eq v0, v4, :cond_1

    goto :goto_1

    :catch_1
    nop

    :cond_1
    const/4 v0, -0x1

    :goto_1
    move v5, v0

    goto :goto_2

    :catch_2
    move-exception v0

    .line 79
    const-string v3, "Could not change \"stay_on_while_plugged_in\""

    invoke-static {v3, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_2
    const/4 v5, -0x1

    .line 84
    :goto_2
    invoke-virtual {p1}, Lcom/android/helper/Options;->getScreenOffTimeout()I

    move-result v0

    if-eq v0, v1, :cond_4

    .line 87
    :try_start_3
    const-string v3, "screen_off_timeout"

    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v4

    invoke-static {v2, v3, v4}, Lcom/android/helper/util/Settings;->getAndPutValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2
    :try_end_3
    .catch Lcom/android/helper/util/SettingsException; {:try_start_3 .. :try_end_3} :catch_4

    .line 89
    :try_start_4
    invoke-static {v2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v2
    :try_end_4
    .catch Ljava/lang/NumberFormatException; {:try_start_4 .. :try_end_4} :catch_3
    .catch Lcom/android/helper/util/SettingsException; {:try_start_4 .. :try_end_4} :catch_4

    if-eq v2, v0, :cond_3

    goto :goto_3

    :catch_3
    nop

    :cond_3
    const/4 v2, -0x1

    :goto_3
    move v8, v2

    goto :goto_4

    :catch_4
    move-exception v0

    .line 98
    const-string v2, "Could not change \"screen_off_timeout\""

    invoke-static {v2, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :cond_4
    const/4 v8, -0x1

    .line 102
    :goto_4
    invoke-virtual {p1}, Lcom/android/helper/Options;->getDisplayId()I

    move-result v4

    if-lez v4, :cond_5

    .line 106
    invoke-virtual {p1}, Lcom/android/helper/Options;->getDisplayImePolicy()I

    move-result v0

    if-eq v0, v1, :cond_5

    .line 108
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v2

    invoke-virtual {v2, v4}, Lcom/android/helper/wrappers/WindowManager;->getDisplayImePolicy(I)I

    move-result v2

    if-eq v2, v0, :cond_5

    .line 110
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v1

    invoke-virtual {v1, v4, v0}, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicy(II)V

    move v9, v2

    goto :goto_5

    :cond_5
    const/4 v9, -0x1

    .line 116
    :goto_5
    invoke-virtual {p1}, Lcom/android/helper/Options;->getPowerOffScreenOnClose()Z

    move-result v7

    move-object v3, p0

    .line 119
    :try_start_5
    invoke-direct/range {v3 .. v9}, Lcom/android/helper/CleanUp;->run(IIZZII)V
    :try_end_5
    .catch Ljava/io/IOException; {:try_start_5 .. :try_end_5} :catch_5

    goto :goto_6

    :catch_5
    move-exception v0

    move-object p1, v0

    .line 121
    const-string v0, "Clean up I/O exception"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    :goto_6
    return-void
.end method

.method public static start(Lcom/android/helper/Options;)Lcom/android/helper/CleanUp;
    .locals 1

    .line 39
    new-instance v0, Lcom/android/helper/CleanUp;

    invoke-direct {v0, p0}, Lcom/android/helper/CleanUp;-><init>(Lcom/android/helper/Options;)V

    return-object v0
.end method

.method public static unlinkSelf()V
    .locals 2

    .line 177
    :try_start_0
    new-instance v0, Ljava/io/File;

    sget-object v1, Lcom/android/helper/CoreService;->SERVER_PATH:Ljava/lang/String;

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/io/File;->delete()Z
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    .line 179
    const-string v1, "Could not unlink server"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method


# virtual methods
.method public declared-synchronized interrupt()V
    .locals 1

    monitor-enter p0

    const/4 v0, 0x1

    .line 44
    :try_start_0
    iput-boolean v0, p0, Lcom/android/helper/CleanUp;->interrupted:Z

    .line 45
    invoke-virtual {p0}, Ljava/lang/Object;->notify()V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 46
    monitor-exit p0

    return-void

    :catchall_0
    move-exception v0

    :try_start_1
    monitor-exit p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    throw v0
.end method

.method public join()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 49
    iget-object v0, p0, Lcom/android/helper/CleanUp;->thread:Ljava/lang/Thread;

    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    return-void
.end method

.method synthetic lambda$new$0$com-android-helper-CleanUp(Lcom/android/helper/Options;)V
    .locals 0

    .line 34
    invoke-direct {p0, p1}, Lcom/android/helper/CleanUp;->runCleanUp(Lcom/android/helper/Options;)V

    return-void
.end method

.method public declared-synchronized setRestoreDisplayPower(Z)V
    .locals 0

    monitor-enter p0

    .line 170
    :try_start_0
    iput-boolean p1, p0, Lcom/android/helper/CleanUp;->pendingRestoreDisplayPower:Z

    .line 171
    iget p1, p0, Lcom/android/helper/CleanUp;->pendingChanges:I

    or-int/lit8 p1, p1, 0x1

    iput p1, p0, Lcom/android/helper/CleanUp;->pendingChanges:I

    .line 172
    invoke-virtual {p0}, Ljava/lang/Object;->notify()V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 173
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
