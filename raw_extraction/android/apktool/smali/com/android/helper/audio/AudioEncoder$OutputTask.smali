.class Lcom/android/helper/audio/AudioEncoder$OutputTask;
.super Ljava/lang/Object;
.source "AudioEncoder.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/audio/AudioEncoder;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0xa
    name = "OutputTask"
.end annotation


# instance fields
.field private final bufferInfo:Landroid/media/MediaCodec$BufferInfo;

.field private final index:I


# direct methods
.method constructor <init>(ILandroid/media/MediaCodec$BufferInfo;)V
    .locals 0

    .line 43
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 44
    iput p1, p0, Lcom/android/helper/audio/AudioEncoder$OutputTask;->index:I

    .line 45
    iput-object p2, p0, Lcom/android/helper/audio/AudioEncoder$OutputTask;->bufferInfo:Landroid/media/MediaCodec$BufferInfo;

    return-void
.end method

.method static synthetic access$100(Lcom/android/helper/audio/AudioEncoder$OutputTask;)I
    .locals 0

    .line 39
    iget p0, p0, Lcom/android/helper/audio/AudioEncoder$OutputTask;->index:I

    return p0
.end method

.method static synthetic access$200(Lcom/android/helper/audio/AudioEncoder$OutputTask;)Landroid/media/MediaCodec$BufferInfo;
    .locals 0

    .line 39
    iget-object p0, p0, Lcom/android/helper/audio/AudioEncoder$OutputTask;->bufferInfo:Landroid/media/MediaCodec$BufferInfo;

    return-object p0
.end method
