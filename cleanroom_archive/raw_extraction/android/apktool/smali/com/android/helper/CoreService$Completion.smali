.class Lcom/android/helper/CoreService$Completion;
.super Ljava/lang/Object;
.source "CoreService.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/CoreService;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0xa
    name = "Completion"
.end annotation


# instance fields
.field private fatalError:Z

.field private running:I


# direct methods
.method constructor <init>(I)V
    .locals 0

    .line 53
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 54
    iput p1, p0, Lcom/android/helper/CoreService$Completion;->running:I

    return-void
.end method


# virtual methods
.method declared-synchronized addCompleted(Z)V
    .locals 2

    monitor-enter p0

    .line 58
    :try_start_0
    iget v0, p0, Lcom/android/helper/CoreService$Completion;->running:I

    const/4 v1, 0x1

    sub-int/2addr v0, v1

    iput v0, p0, Lcom/android/helper/CoreService$Completion;->running:I

    if-eqz p1, :cond_0

    .line 60
    iput-boolean v1, p0, Lcom/android/helper/CoreService$Completion;->fatalError:Z

    :cond_0
    if-eqz v0, :cond_1

    .line 62
    iget-boolean p1, p0, Lcom/android/helper/CoreService$Completion;->fatalError:Z

    if-eqz p1, :cond_2

    .line 63
    :cond_1
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    move-result-object p1

    invoke-virtual {p1}, Landroid/os/Looper;->quitSafely()V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 65
    :cond_2
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
