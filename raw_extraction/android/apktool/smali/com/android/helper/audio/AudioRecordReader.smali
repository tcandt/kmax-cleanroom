.class public Lcom/android/helper/audio/AudioRecordReader;
.super Ljava/lang/Object;
.source "AudioRecordReader.java"


# static fields
.field private static final ONE_SAMPLE_US:J = 0x15L


# instance fields
.field private nextPts:J

.field private previousPts:J

.field private previousRecorderTimestamp:J

.field private final recorder:Landroid/media/AudioRecord;

.field private final timestamp:Landroid/media/AudioTimestamp;


# direct methods
.method public constructor <init>(Landroid/media/AudioRecord;)V
    .locals 2

    .line 25
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 20
    new-instance v0, Landroid/media/AudioTimestamp;

    invoke-direct {v0}, Landroid/media/AudioTimestamp;-><init>()V

    iput-object v0, p0, Lcom/android/helper/audio/AudioRecordReader;->timestamp:Landroid/media/AudioTimestamp;

    const-wide/16 v0, -0x1

    .line 21
    iput-wide v0, p0, Lcom/android/helper/audio/AudioRecordReader;->previousRecorderTimestamp:J

    const-wide/16 v0, 0x0

    .line 22
    iput-wide v0, p0, Lcom/android/helper/audio/AudioRecordReader;->previousPts:J

    .line 23
    iput-wide v0, p0, Lcom/android/helper/audio/AudioRecordReader;->nextPts:J

    .line 26
    iput-object p1, p0, Lcom/android/helper/audio/AudioRecordReader;->recorder:Landroid/media/AudioRecord;

    return-void
.end method


# virtual methods
.method public read(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)I
    .locals 9

    .line 31
    iget-object v0, p0, Lcom/android/helper/audio/AudioRecordReader;->recorder:Landroid/media/AudioRecord;

    const/16 v1, 0x1000

    invoke-virtual {v0, p1, v1}, Landroid/media/AudioRecord;->read(Ljava/nio/ByteBuffer;I)I

    move-result v4

    if-gtz v4, :cond_0

    return v4

    .line 38
    :cond_0
    iget-object p1, p0, Lcom/android/helper/audio/AudioRecordReader;->recorder:Landroid/media/AudioRecord;

    iget-object v0, p0, Lcom/android/helper/audio/AudioRecordReader;->timestamp:Landroid/media/AudioTimestamp;

    const/4 v1, 0x0

    invoke-static {p1, v0, v1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/media/AudioRecord;Landroid/media/AudioTimestamp;I)I

    move-result p1

    const-wide/16 v0, 0x3e8

    const-wide/16 v2, 0x0

    if-nez p1, :cond_1

    .line 39
    iget-object p1, p0, Lcom/android/helper/audio/AudioRecordReader;->timestamp:Landroid/media/AudioTimestamp;

    iget-wide v5, p1, Landroid/media/AudioTimestamp;->nanoTime:J

    iget-wide v7, p0, Lcom/android/helper/audio/AudioRecordReader;->previousRecorderTimestamp:J

    cmp-long p1, v5, v7

    if-eqz p1, :cond_1

    .line 40
    iget-object p1, p0, Lcom/android/helper/audio/AudioRecordReader;->timestamp:Landroid/media/AudioTimestamp;

    iget-wide v5, p1, Landroid/media/AudioTimestamp;->nanoTime:J

    div-long/2addr v5, v0

    .line 41
    iget-object p1, p0, Lcom/android/helper/audio/AudioRecordReader;->timestamp:Landroid/media/AudioTimestamp;

    iget-wide v0, p1, Landroid/media/AudioTimestamp;->nanoTime:J

    iput-wide v0, p0, Lcom/android/helper/audio/AudioRecordReader;->previousRecorderTimestamp:J

    goto :goto_0

    .line 43
    :cond_1
    iget-wide v5, p0, Lcom/android/helper/audio/AudioRecordReader;->nextPts:J

    cmp-long p1, v5, v2

    if-nez p1, :cond_2

    .line 44
    const-string p1, "Could not get initial audio timestamp"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 45
    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v5

    div-long/2addr v5, v0

    iput-wide v5, p0, Lcom/android/helper/audio/AudioRecordReader;->nextPts:J

    .line 48
    :cond_2
    iget-wide v5, p0, Lcom/android/helper/audio/AudioRecordReader;->nextPts:J

    :goto_0
    int-to-long v0, v4

    const-wide/32 v7, 0xf4240

    mul-long v0, v0, v7

    const-wide/32 v7, 0x2ee00

    .line 51
    div-long/2addr v0, v7

    add-long/2addr v0, v5

    .line 52
    iput-wide v0, p0, Lcom/android/helper/audio/AudioRecordReader;->nextPts:J

    .line 54
    iget-wide v0, p0, Lcom/android/helper/audio/AudioRecordReader;->previousPts:J

    cmp-long p1, v0, v2

    if-eqz p1, :cond_3

    const-wide/16 v2, 0x15

    add-long v7, v0, v2

    cmp-long p1, v5, v7

    if-gez p1, :cond_3

    add-long v5, v0, v2

    .line 62
    :cond_3
    iput-wide v5, p0, Lcom/android/helper/audio/AudioRecordReader;->previousPts:J

    const/4 v3, 0x0

    const/4 v7, 0x0

    move-object v2, p2

    .line 64
    invoke-virtual/range {v2 .. v7}, Landroid/media/MediaCodec$BufferInfo;->set(IIJI)V

    return v4
.end method
