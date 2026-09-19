.class public final Lcom/android/helper/control/DeviceMessageSender;
.super Ljava/lang/Object;
.source "DeviceMessageSender.java"


# instance fields
.field private final controlChannel:Lcom/android/helper/control/ControlChannel;

.field private final queue:Ljava/util/concurrent/BlockingQueue;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/concurrent/BlockingQueue<",
            "Lcom/android/helper/control/DeviceMessage;",
            ">;"
        }
    .end annotation
.end field

.field private thread:Ljava/lang/Thread;


# direct methods
.method public constructor <init>(Lcom/android/helper/control/ControlChannel;)V
    .locals 2

    .line 16
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 14
    new-instance v0, Ljava/util/concurrent/ArrayBlockingQueue;

    const/16 v1, 0x10

    invoke-direct {v0, v1}, Ljava/util/concurrent/ArrayBlockingQueue;-><init>(I)V

    iput-object v0, p0, Lcom/android/helper/control/DeviceMessageSender;->queue:Ljava/util/concurrent/BlockingQueue;

    .line 17
    iput-object p1, p0, Lcom/android/helper/control/DeviceMessageSender;->controlChannel:Lcom/android/helper/control/ControlChannel;

    return-void
.end method

.method private loop()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;,
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 27
    :goto_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->isInterrupted()Z

    move-result v0

    if-nez v0, :cond_0

    .line 28
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageSender;->queue:Ljava/util/concurrent/BlockingQueue;

    invoke-interface {v0}, Ljava/util/concurrent/BlockingQueue;->take()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/android/helper/control/DeviceMessage;

    .line 29
    iget-object v1, p0, Lcom/android/helper/control/DeviceMessageSender;->controlChannel:Lcom/android/helper/control/ControlChannel;

    invoke-virtual {v1, v0}, Lcom/android/helper/control/ControlChannel;->send(Lcom/android/helper/control/DeviceMessage;)V

    goto :goto_0

    :cond_0
    return-void
.end method


# virtual methods
.method public join()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 53
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageSender;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 54
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    :cond_0
    return-void
.end method

.method synthetic lambda$start$0$com-android-helper-control-DeviceMessageSender()V
    .locals 2

    .line 36
    const-string v0, "Device message sender stopped"

    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/control/DeviceMessageSender;->loop()V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 40
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    return-void

    :catchall_0
    move-exception v1

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 41
    throw v1

    .line 40
    :catch_0
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    return-void
.end method

.method public send(Lcom/android/helper/control/DeviceMessage;)V
    .locals 2

    .line 21
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageSender;->queue:Ljava/util/concurrent/BlockingQueue;

    invoke-interface {v0, p1}, Ljava/util/concurrent/BlockingQueue;->offer(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    .line 22
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Device message dropped: "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessage;->getType()I

    move-result p1

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method public start()V
    .locals 3

    .line 34
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/android/helper/control/DeviceMessageSender$$ExternalSyntheticLambda0;

    invoke-direct {v1, p0}, Lcom/android/helper/control/DeviceMessageSender$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/control/DeviceMessageSender;)V

    const-string v2, "control-send"

    invoke-direct {v0, v1, v2}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v0, p0, Lcom/android/helper/control/DeviceMessageSender;->thread:Ljava/lang/Thread;

    .line 43
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method

.method public stop()V
    .locals 1

    .line 47
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageSender;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 48
    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    :cond_0
    return-void
.end method
