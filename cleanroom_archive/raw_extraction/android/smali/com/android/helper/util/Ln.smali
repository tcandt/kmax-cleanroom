.class public final Lcom/android/helper/util/Ln;
.super Ljava/lang/Object;
.source "Ln.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/util/Ln$NullOutputStream;,
        Lcom/android/helper/util/Ln$Level;
    }
.end annotation


# static fields
.field private static final CONSOLE_ERR:Ljava/io/PrintStream;

.field private static final CONSOLE_OUT:Ljava/io/PrintStream;

.field private static final PREFIX:Ljava/lang/String; = "[server] "

.field private static final TAG:Ljava/lang/String; = "scrcpy"

.field private static threshold:Lcom/android/helper/util/Ln$Level;


# direct methods
.method static constructor <clinit>()V
    .locals 3

    .line 19
    new-instance v0, Ljava/io/PrintStream;

    new-instance v1, Ljava/io/FileOutputStream;

    sget-object v2, Ljava/io/FileDescriptor;->out:Ljava/io/FileDescriptor;

    invoke-direct {v1, v2}, Ljava/io/FileOutputStream;-><init>(Ljava/io/FileDescriptor;)V

    invoke-direct {v0, v1}, Ljava/io/PrintStream;-><init>(Ljava/io/OutputStream;)V

    sput-object v0, Lcom/android/helper/util/Ln;->CONSOLE_OUT:Ljava/io/PrintStream;

    .line 20
    new-instance v0, Ljava/io/PrintStream;

    new-instance v1, Ljava/io/FileOutputStream;

    sget-object v2, Ljava/io/FileDescriptor;->err:Ljava/io/FileDescriptor;

    invoke-direct {v1, v2}, Ljava/io/FileOutputStream;-><init>(Ljava/io/FileDescriptor;)V

    invoke-direct {v0, v1}, Ljava/io/PrintStream;-><init>(Ljava/io/OutputStream;)V

    sput-object v0, Lcom/android/helper/util/Ln;->CONSOLE_ERR:Ljava/io/PrintStream;

    .line 26
    sget-object v0, Lcom/android/helper/util/Ln$Level;->INFO:Lcom/android/helper/util/Ln$Level;

    sput-object v0, Lcom/android/helper/util/Ln;->threshold:Lcom/android/helper/util/Ln$Level;

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 28
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static d(Ljava/lang/String;)V
    .locals 3

    .line 61
    sget-object v0, Lcom/android/helper/util/Ln$Level;->DEBUG:Lcom/android/helper/util/Ln$Level;

    invoke-static {v0}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 62
    const-string v0, "scrcpy"

    invoke-static {v0, p0}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 63
    sget-object v0, Lcom/android/helper/util/Ln;->CONSOLE_OUT:Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "[server] DEBUG: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const/16 p0, 0xa

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method public static disableSystemStreams()V
    .locals 2

    .line 33
    new-instance v0, Ljava/io/PrintStream;

    new-instance v1, Lcom/android/helper/util/Ln$NullOutputStream;

    invoke-direct {v1}, Lcom/android/helper/util/Ln$NullOutputStream;-><init>()V

    invoke-direct {v0, v1}, Ljava/io/PrintStream;-><init>(Ljava/io/OutputStream;)V

    .line 34
    invoke-static {v0}, Ljava/lang/System;->setOut(Ljava/io/PrintStream;)V

    .line 35
    invoke-static {v0}, Ljava/lang/System;->setErr(Ljava/io/PrintStream;)V

    return-void
.end method

.method public static e(Ljava/lang/String;)V
    .locals 1

    const/4 v0, 0x0

    .line 103
    invoke-static {p0, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public static e(Ljava/lang/String;Ljava/lang/Throwable;)V
    .locals 3

    const-string v0, "[server] ERROR: "

    .line 91
    sget-object v1, Lcom/android/helper/util/Ln$Level;->ERROR:Lcom/android/helper/util/Ln$Level;

    invoke-static {v1}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 92
    const-string v1, "scrcpy"

    invoke-static {v1, p0, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 93
    sget-object v1, Lcom/android/helper/util/Ln;->CONSOLE_ERR:Ljava/io/PrintStream;

    monitor-enter v1

    .line 94
    :try_start_0
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const/16 p0, 0xa

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    if-eqz p1, :cond_0

    .line 96
    invoke-virtual {p1, v1}, Ljava/lang/Throwable;->printStackTrace(Ljava/io/PrintStream;)V

    .line 98
    :cond_0
    monitor-exit v1

    return-void

    :catchall_0
    move-exception p0

    monitor-exit v1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw p0

    :cond_1
    return-void
.end method

.method public static i(Ljava/lang/String;)V
    .locals 3

    .line 68
    sget-object v0, Lcom/android/helper/util/Ln$Level;->INFO:Lcom/android/helper/util/Ln$Level;

    invoke-static {v0}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 69
    const-string v0, "scrcpy"

    invoke-static {v0, p0}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 70
    sget-object v0, Lcom/android/helper/util/Ln;->CONSOLE_OUT:Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "[server] INFO: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const/16 p0, 0xa

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method public static initLogLevel(Lcom/android/helper/util/Ln$Level;)V
    .locals 0

    .line 46
    sput-object p0, Lcom/android/helper/util/Ln;->threshold:Lcom/android/helper/util/Ln$Level;

    return-void
.end method

.method public static isEnabled(Lcom/android/helper/util/Ln$Level;)Z
    .locals 1

    .line 50
    invoke-virtual {p0}, Lcom/android/helper/util/Ln$Level;->ordinal()I

    move-result p0

    sget-object v0, Lcom/android/helper/util/Ln;->threshold:Lcom/android/helper/util/Ln$Level;

    invoke-virtual {v0}, Lcom/android/helper/util/Ln$Level;->ordinal()I

    move-result v0

    if-lt p0, v0, :cond_0

    const/4 p0, 0x1

    return p0

    :cond_0
    const/4 p0, 0x0

    return p0
.end method

.method public static v(Ljava/lang/String;)V
    .locals 3

    .line 54
    sget-object v0, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {v0}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 55
    const-string v0, "scrcpy"

    invoke-static {v0, p0}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;)I

    .line 56
    sget-object v0, Lcom/android/helper/util/Ln;->CONSOLE_OUT:Ljava/io/PrintStream;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "[server] VERBOSE: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const/16 p0, 0xa

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method public static w(Ljava/lang/String;)V
    .locals 1

    const/4 v0, 0x0

    .line 87
    invoke-static {p0, v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public static w(Ljava/lang/String;Ljava/lang/Throwable;)V
    .locals 3

    const-string v0, "[server] WARN: "

    .line 75
    sget-object v1, Lcom/android/helper/util/Ln$Level;->WARN:Lcom/android/helper/util/Ln$Level;

    invoke-static {v1}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 76
    const-string v1, "scrcpy"

    invoke-static {v1, p0, p1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 77
    sget-object v1, Lcom/android/helper/util/Ln;->CONSOLE_ERR:Ljava/io/PrintStream;

    monitor-enter v1

    .line 78
    :try_start_0
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const/16 p0, 0xa

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    if-eqz p1, :cond_0

    .line 80
    invoke-virtual {p1, v1}, Ljava/lang/Throwable;->printStackTrace(Ljava/io/PrintStream;)V

    .line 82
    :cond_0
    monitor-exit v1

    return-void

    :catchall_0
    move-exception p0

    monitor-exit v1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw p0

    :cond_1
    return-void
.end method
