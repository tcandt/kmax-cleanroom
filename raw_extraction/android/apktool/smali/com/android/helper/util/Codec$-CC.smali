.class public final synthetic Lcom/android/helper/util/Codec$-CC;
.super Ljava/lang/Object;
.source "Codec.java"


# direct methods
.method public static getMimeType(Landroid/media/MediaCodec;)Ljava/lang/String;
    .locals 1

    .line 21
    invoke-virtual {p0}, Landroid/media/MediaCodec;->getCodecInfo()Landroid/media/MediaCodecInfo;

    move-result-object p0

    invoke-virtual {p0}, Landroid/media/MediaCodecInfo;->getSupportedTypes()[Ljava/lang/String;

    move-result-object p0

    .line 22
    array-length v0, p0

    if-lez v0, :cond_0

    const/4 v0, 0x0

    aget-object p0, p0, v0

    return-object p0

    :cond_0
    const/4 p0, 0x0

    return-object p0
.end method
