.class public final synthetic Lcom/android/helper/CoreService$$ExternalSyntheticLambda0;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Lcom/android/helper/AsyncProcessor$TerminationListener;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/CoreService$Completion;


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/CoreService$Completion;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/CoreService$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/CoreService$Completion;

    return-void
.end method


# virtual methods
.method public final onTerminated(Z)V
    .locals 1

    .line 0
    iget-object v0, p0, Lcom/android/helper/CoreService$$ExternalSyntheticLambda0;->f$0:Lcom/android/helper/CoreService$Completion;

    invoke-static {v0, p1}, Lcom/android/helper/CoreService;->lambda$scrcpy$0(Lcom/android/helper/CoreService$Completion;Z)V

    return-void
.end method
