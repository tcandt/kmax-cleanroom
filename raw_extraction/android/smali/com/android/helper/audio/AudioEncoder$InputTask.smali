.class Lcom/android/helper/audio/AudioEncoder$InputTask;
.super Ljava/lang/Object;
.source "AudioEncoder.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/audio/AudioEncoder;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0xa
    name = "InputTask"
.end annotation


# instance fields
.field private final index:I


# direct methods
.method constructor <init>(I)V
    .locals 0

    .line 34
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 35
    iput p1, p0, Lcom/android/helper/audio/AudioEncoder$InputTask;->index:I

    return-void
.end method

.method static synthetic access$000(Lcom/android/helper/audio/AudioEncoder$InputTask;)I
    .locals 0

    .line 31
    iget p0, p0, Lcom/android/helper/audio/AudioEncoder$InputTask;->index:I

    return p0
.end method
