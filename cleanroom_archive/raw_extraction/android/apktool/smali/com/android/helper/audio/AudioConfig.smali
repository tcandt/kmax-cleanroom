.class public final Lcom/android/helper/audio/AudioConfig;
.super Ljava/lang/Object;
.source "AudioConfig.java"


# static fields
.field public static final BYTES_PER_SAMPLE:I = 0x2

.field public static final CHANNELS:I = 0x2

.field public static final CHANNEL_CONFIG:I = 0xc

.field public static final CHANNEL_MASK:I = 0xc

.field public static final ENCODING:I = 0x2

.field public static final MAX_READ_SIZE:I = 0x1000

.field public static final SAMPLE_RATE:I = 0xbb80


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 18
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static createAudioFormat()Landroid/media/AudioFormat;
    .locals 2

    .line 23
    new-instance v0, Landroid/media/AudioFormat$Builder;

    invoke-direct {v0}, Landroid/media/AudioFormat$Builder;-><init>()V

    const/4 v1, 0x2

    .line 24
    invoke-virtual {v0, v1}, Landroid/media/AudioFormat$Builder;->setEncoding(I)Landroid/media/AudioFormat$Builder;

    const v1, 0xbb80

    .line 25
    invoke-virtual {v0, v1}, Landroid/media/AudioFormat$Builder;->setSampleRate(I)Landroid/media/AudioFormat$Builder;

    const/16 v1, 0xc

    .line 26
    invoke-virtual {v0, v1}, Landroid/media/AudioFormat$Builder;->setChannelMask(I)Landroid/media/AudioFormat$Builder;

    .line 27
    invoke-virtual {v0}, Landroid/media/AudioFormat$Builder;->build()Landroid/media/AudioFormat;

    move-result-object v0

    return-object v0
.end method
