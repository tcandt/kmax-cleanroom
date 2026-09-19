.class public interface abstract Lcom/android/helper/AsyncProcessor;
.super Ljava/lang/Object;
.source "AsyncProcessor.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/AsyncProcessor$TerminationListener;
    }
.end annotation


# virtual methods
.method public abstract join()V
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation
.end method

.method public abstract start(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
.end method

.method public abstract stop()V
.end method
