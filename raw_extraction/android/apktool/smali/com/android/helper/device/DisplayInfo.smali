.class public final Lcom/android/helper/device/DisplayInfo;
.super Ljava/lang/Object;
.source "DisplayInfo.java"


# static fields
.field public static final FLAG_SUPPORTS_PROTECTED_BUFFERS:I = 0x1


# instance fields
.field private final displayId:I

.field private final dpi:I

.field private final flags:I

.field private final layerStack:I

.field private final rotation:I

.field private final size:Lcom/android/helper/device/Size;

.field private final uniqueId:Ljava/lang/String;


# direct methods
.method public constructor <init>(ILcom/android/helper/device/Size;IIIILjava/lang/String;)V
    .locals 0

    .line 14
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 15
    iput p1, p0, Lcom/android/helper/device/DisplayInfo;->displayId:I

    .line 16
    iput-object p2, p0, Lcom/android/helper/device/DisplayInfo;->size:Lcom/android/helper/device/Size;

    .line 17
    iput p3, p0, Lcom/android/helper/device/DisplayInfo;->rotation:I

    .line 18
    iput p4, p0, Lcom/android/helper/device/DisplayInfo;->layerStack:I

    .line 19
    iput p5, p0, Lcom/android/helper/device/DisplayInfo;->flags:I

    .line 20
    iput p6, p0, Lcom/android/helper/device/DisplayInfo;->dpi:I

    .line 21
    iput-object p7, p0, Lcom/android/helper/device/DisplayInfo;->uniqueId:Ljava/lang/String;

    return-void
.end method


# virtual methods
.method public getDisplayId()I
    .locals 1

    .line 25
    iget v0, p0, Lcom/android/helper/device/DisplayInfo;->displayId:I

    return v0
.end method

.method public getDpi()I
    .locals 1

    .line 45
    iget v0, p0, Lcom/android/helper/device/DisplayInfo;->dpi:I

    return v0
.end method

.method public getFlags()I
    .locals 1

    .line 41
    iget v0, p0, Lcom/android/helper/device/DisplayInfo;->flags:I

    return v0
.end method

.method public getLayerStack()I
    .locals 1

    .line 37
    iget v0, p0, Lcom/android/helper/device/DisplayInfo;->layerStack:I

    return v0
.end method

.method public getRotation()I
    .locals 1

    .line 33
    iget v0, p0, Lcom/android/helper/device/DisplayInfo;->rotation:I

    return v0
.end method

.method public getSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 29
    iget-object v0, p0, Lcom/android/helper/device/DisplayInfo;->size:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public getUniqueId()Ljava/lang/String;
    .locals 1

    .line 49
    iget-object v0, p0, Lcom/android/helper/device/DisplayInfo;->uniqueId:Ljava/lang/String;

    return-object v0
.end method
