.class public abstract Lcom/android/helper/video/SurfaceCapture;
.super Ljava/lang/Object;
.source "SurfaceCapture.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/video/SurfaceCapture$CaptureListener;
    }
.end annotation


# instance fields
.field private listener:Lcom/android/helper/video/SurfaceCapture$CaptureListener;


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 13
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public abstract getSize()Lcom/android/helper/device/Size;
.end method

.method protected abstract init()V
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/device/ConfigurationException;,
            Ljava/io/IOException;
        }
    .end annotation
.end method

.method public final init(Lcom/android/helper/video/SurfaceCapture$CaptureListener;)V
    .locals 0
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/device/ConfigurationException;,
            Ljava/io/IOException;
        }
    .end annotation

    .line 32
    iput-object p1, p0, Lcom/android/helper/video/SurfaceCapture;->listener:Lcom/android/helper/video/SurfaceCapture$CaptureListener;

    .line 33
    invoke-virtual {p0}, Lcom/android/helper/video/SurfaceCapture;->init()V

    return-void
.end method

.method protected invalidate()V
    .locals 1

    .line 25
    iget-object v0, p0, Lcom/android/helper/video/SurfaceCapture;->listener:Lcom/android/helper/video/SurfaceCapture$CaptureListener;

    invoke-interface {v0}, Lcom/android/helper/video/SurfaceCapture$CaptureListener;->onInvalidated()V

    return-void
.end method

.method public isClosed()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public prepare()V
    .locals 0
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/device/ConfigurationException;,
            Ljava/io/IOException;
        }
    .end annotation

    return-void
.end method

.method public abstract release()V
.end method

.method public abstract requestInvalidate()V
.end method

.method public abstract setMaxSize(I)Z
.end method

.method public abstract start(Landroid/view/Surface;)V
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation
.end method

.method public stop()V
    .locals 0

    return-void
.end method
