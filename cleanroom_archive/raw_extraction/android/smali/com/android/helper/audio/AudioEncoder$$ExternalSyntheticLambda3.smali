.class public final synthetic Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"

# interfaces
.implements Ljava/lang/Runnable;


# instance fields
.field public final synthetic f$0:Lcom/android/helper/audio/AudioEncoder;

.field public final synthetic f$1:Landroid/media/MediaCodec;


# direct methods
.method public synthetic constructor <init>(Lcom/android/helper/audio/AudioEncoder;Landroid/media/MediaCodec;)V
    .locals 0

    .line 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;->f$0:Lcom/android/helper/audio/AudioEncoder;

    iput-object p2, p0, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;->f$1:Landroid/media/MediaCodec;

    return-void
.end method


# virtual methods
.method public final run()V
    .locals 2

    .line 0
    iget-object v0, p0, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;->f$0:Lcom/android/helper/audio/AudioEncoder;

    iget-object v1, p0, Lcom/android/helper/audio/AudioEncoder$$ExternalSyntheticLambda3;->f$1:Landroid/media/MediaCodec;

    invoke-virtual {v0, v1}, Lcom/android/helper/audio/AudioEncoder;->lambda$encode$1$com-android-helper-audio-AudioEncoder(Landroid/media/MediaCodec;)V

    return-void
.end method
