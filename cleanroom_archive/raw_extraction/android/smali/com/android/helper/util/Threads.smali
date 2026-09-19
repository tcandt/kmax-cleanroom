.class public final Lcom/android/helper/util/Threads;
.super Ljava/lang/Object;
.source "Threads.java"


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 9
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static executeSynchronouslyOn(Landroid/os/Handler;Ljava/util/concurrent/Callable;)Ljava/lang/Object;
    .locals 5
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<T:",
            "Ljava/lang/Object;",
            ">(",
            "Landroid/os/Handler;",
            "Ljava/util/concurrent/Callable<",
            "TT;>;)TT;"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Throwable;
        }
    .end annotation

    .line 15
    new-instance v0, Ljava/util/concurrent/Semaphore;

    const/4 v1, 0x0

    invoke-direct {v0, v1}, Ljava/util/concurrent/Semaphore;-><init>(I)V

    const/4 v2, 0x1

    .line 17
    new-array v3, v2, [Ljava/lang/Object;

    .line 18
    new-array v2, v2, [Ljava/lang/Throwable;

    .line 20
    new-instance v4, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;

    invoke-direct {v4, v3, p1, v2, v0}, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;-><init>([Ljava/lang/Object;Ljava/util/concurrent/Callable;[Ljava/lang/Throwable;Ljava/util/concurrent/Semaphore;)V

    invoke-virtual {p0, v4}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 31
    :try_start_0
    invoke-virtual {v0}, Ljava/util/concurrent/Semaphore;->acquire()V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 34
    :catch_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object p0

    invoke-virtual {p0}, Ljava/lang/Thread;->interrupt()V

    .line 37
    :goto_0
    aget-object p0, v2, v1

    if-nez p0, :cond_0

    .line 41
    aget-object p0, v3, v1

    return-object p0

    .line 38
    :cond_0
    throw p0
.end method

.method static synthetic lambda$executeSynchronouslyOn$0([Ljava/lang/Object;Ljava/util/concurrent/Callable;[Ljava/lang/Throwable;Ljava/util/concurrent/Semaphore;)V
    .locals 1

    const/4 v0, 0x0

    .line 22
    :try_start_0
    invoke-interface {p1}, Ljava/util/concurrent/Callable;->call()Ljava/lang/Object;

    move-result-object p1

    aput-object p1, p0, v0
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 26
    invoke-virtual {p3}, Ljava/util/concurrent/Semaphore;->release()V

    return-void

    :catchall_0
    move-exception p0

    .line 24
    :try_start_1
    aput-object p0, p2, v0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_1

    .line 26
    invoke-virtual {p3}, Ljava/util/concurrent/Semaphore;->release()V

    return-void

    :catchall_1
    move-exception p0

    invoke-virtual {p3}, Ljava/util/concurrent/Semaphore;->release()V

    .line 27
    throw p0
.end method
