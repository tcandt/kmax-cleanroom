.class public final synthetic Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:[Ljava/lang/Object;

.field public final synthetic f$1:Ljava/util/concurrent/Callable;

.field public final synthetic f$2:[Ljava/lang/Throwable;

.field public final synthetic f$3:Ljava/util/concurrent/Semaphore;


# direct methods
.method public synthetic constructor <init>([Ljava/lang/Object;Ljava/util/concurrent/Callable;[Ljava/lang/Throwable;Ljava/util/concurrent/Semaphore;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$0:[Ljava/lang/Object;

    iput-object p2, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$1:Ljava/util/concurrent/Callable;

    iput-object p3, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$2:[Ljava/lang/Throwable;

    iput-object p4, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$3:Ljava/util/concurrent/Semaphore;

    return-void
.end method


# virtual methods
.method public final run()V
    .locals 4

    .line 0
    iget-object v0, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$0:[Ljava/lang/Object;

    iget-object v1, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$1:Ljava/util/concurrent/Callable;

    iget-object v2, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$2:[Ljava/lang/Throwable;

    iget-object v3, p0, Lcom/android/helper/util/Threads$$ExternalSyntheticLambda0;->f$3:Ljava/util/concurrent/Semaphore;

    invoke-static {v0, v1, v2, v3}, Lcom/android/helper/util/Threads;->lambda$executeSynchronouslyOn$0([Ljava/lang/Object;Ljava/util/concurrent/Callable;[Ljava/lang/Throwable;Ljava/util/concurrent/Semaphore;)V

    return-void
.end method
