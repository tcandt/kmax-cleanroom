.class public final Lcom/android/helper/device/NewDisplay;
.super Ljava/lang/Object;
.source "NewDisplay.java"


# instance fields
.field private dpi:I

.field private size:Lcom/android/helper/device/Size;


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 7
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/device/Size;I)V
    .locals 0

    .line 11
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 12
    iput-object p1, p0, Lcom/android/helper/device/NewDisplay;->size:Lcom/android/helper/device/Size;

    .line 13
    iput p2, p0, Lcom/android/helper/device/NewDisplay;->dpi:I

    return-void
.end method


# virtual methods
.method public getDpi()I
    .locals 1

    .line 21
    iget v0, p0, Lcom/android/helper/device/NewDisplay;->dpi:I

    return v0
.end method

.method public getSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 17
    iget-object v0, p0, Lcom/android/helper/device/NewDisplay;->size:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public hasExplicitDpi()Z
    .locals 1

    .line 29
    iget v0, p0, Lcom/android/helper/device/NewDisplay;->dpi:I

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method

.method public hasExplicitSize()Z
    .locals 1

    .line 25
    iget-object v0, p0, Lcom/android/helper/device/NewDisplay;->size:Lcom/android/helper/device/Size;

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method
