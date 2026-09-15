.class public final Lcom/android/helper/device/Streamer;
.super Ljava/lang/Object;
.source "Streamer.java"


# static fields
.field private static final PACKET_FLAG_CONFIG:J = -0x8000000000000000L

.field private static final PACKET_FLAG_KEY_FRAME:J = 0x4000000000000000L


# instance fields
.field private final codec:Lcom/android/helper/util/Codec;

.field private final fd:Ljava/io/FileDescriptor;

.field private final headerBuffer:Ljava/nio/ByteBuffer;

.field private final sendCodecMeta:Z

.field private final sendFrameMeta:Z


# direct methods
.method public constructor <init>(Ljava/io/FileDescriptor;Lcom/android/helper/util/Codec;ZZ)V
    .locals 1

    .line 27
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/16 v0, 0xc

    .line 25
    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocate(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/device/Streamer;->headerBuffer:Ljava/nio/ByteBuffer;

    .line 28
    iput-object p1, p0, Lcom/android/helper/device/Streamer;->fd:Ljava/io/FileDescriptor;

    .line 29
    iput-object p2, p0, Lcom/android/helper/device/Streamer;->codec:Lcom/android/helper/util/Codec;

    .line 30
    iput-boolean p3, p0, Lcom/android/helper/device/Streamer;->sendCodecMeta:Z

    .line 31
    iput-boolean p4, p0, Lcom/android/helper/device/Streamer;->sendFrameMeta:Z

    return-void
.end method

.method private static fixFlacConfigPacket(Ljava/nio/ByteBuffer;)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 168
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->remaining()I

    move-result v0

    const/16 v1, 0x8

    if-lt v0, v1, :cond_2

    const/4 v0, 0x4

    .line 172
    new-array v1, v0, [B

    fill-array-data v1, :array_0

    .line 173
    new-array v0, v0, [B

    .line 174
    invoke-virtual {p0, v0}, Ljava/nio/ByteBuffer;->get([B)Ljava/nio/ByteBuffer;

    .line 175
    invoke-static {v0, v1}, Ljava/util/Arrays;->equals([B[B)Z

    move-result v0

    if-eqz v0, :cond_1

    .line 180
    sget-object v0, Ljava/nio/ByteOrder;->BIG_ENDIAN:Ljava/nio/ByteOrder;

    invoke-virtual {p0, v0}, Ljava/nio/ByteBuffer;->order(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;

    .line 182
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->getInt()I

    move-result v0

    .line 183
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->remaining()I

    move-result v1

    if-lt v1, v0, :cond_0

    .line 188
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->position()I

    move-result v1

    add-int/2addr v1, v0

    invoke-virtual {p0, v1}, Ljava/nio/ByteBuffer;->limit(I)Ljava/nio/Buffer;

    return-void

    .line 184
    :cond_0
    new-instance p0, Ljava/io/IOException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Not enough data in FLAC header (invalid size: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v0, ")"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 176
    :cond_1
    new-instance p0, Ljava/io/IOException;

    const-string v0, "FLAC header not found"

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 169
    :cond_2
    new-instance p0, Ljava/io/IOException;

    const-string v0, "Not enough data in FLAC config packet"

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    :array_0
    .array-data 1
        0x66t
        0x4ct
        0x61t
        0x43t
    .end array-data
.end method

.method private static fixOpusConfigPacket(Ljava/nio/ByteBuffer;)V
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 128
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->remaining()I

    move-result v0

    const/16 v1, 0x10

    if-lt v0, v1, :cond_3

    const/16 v0, 0x8

    .line 132
    new-array v1, v0, [B

    fill-array-data v1, :array_0

    .line 133
    new-array v0, v0, [B

    .line 134
    invoke-virtual {p0, v0}, Ljava/nio/ByteBuffer;->get([B)Ljava/nio/ByteBuffer;

    .line 135
    invoke-static {v0, v1}, Ljava/util/Arrays;->equals([B[B)Z

    move-result v0

    if-eqz v0, :cond_2

    .line 140
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->getLong()J

    move-result-wide v0

    const-wide/16 v2, 0x0

    cmp-long v4, v0, v2

    if-ltz v4, :cond_1

    const-wide/32 v2, 0x7fffffff

    cmp-long v4, v0, v2

    if-gez v4, :cond_1

    long-to-int v1, v0

    .line 146
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->remaining()I

    move-result v0

    if-lt v0, v1, :cond_0

    .line 151
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->position()I

    move-result v0

    add-int/2addr v0, v1

    invoke-virtual {p0, v0}, Ljava/nio/ByteBuffer;->limit(I)Ljava/nio/Buffer;

    return-void

    .line 147
    :cond_0
    new-instance p0, Ljava/io/IOException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v2, "Not enough data in OPUS header (invalid size: "

    invoke-direct {v0, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v1, ")"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 142
    :cond_1
    new-instance p0, Ljava/io/IOException;

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Invalid block size in OPUS header: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, v0, v1}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 136
    :cond_2
    new-instance p0, Ljava/io/IOException;

    const-string v0, "OPUS header not found"

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 129
    :cond_3
    new-instance p0, Ljava/io/IOException;

    const-string v0, "Not enough data in OPUS config packet"

    invoke-direct {p0, v0}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw p0

    :array_0
    .array-data 1
        0x41t
        0x4ft
        0x50t
        0x55t
        0x53t
        0x48t
        0x44t
        0x52t
    .end array-data
.end method

.method private writeFrameMeta(Ljava/io/FileDescriptor;IJZZ)V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 93
    iget-object v0, p0, Lcom/android/helper/device/Streamer;->headerBuffer:Ljava/nio/ByteBuffer;

    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->clear()Ljava/nio/Buffer;

    if-eqz p5, :cond_0

    const-wide/high16 p3, -0x8000000000000000L

    goto :goto_0

    :cond_0
    if-eqz p6, :cond_1

    const-wide/high16 p5, 0x4000000000000000L    # 2.0

    or-long/2addr p3, p5

    .line 105
    :cond_1
    :goto_0
    iget-object p5, p0, Lcom/android/helper/device/Streamer;->headerBuffer:Ljava/nio/ByteBuffer;

    invoke-virtual {p5, p3, p4}, Ljava/nio/ByteBuffer;->putLong(J)Ljava/nio/ByteBuffer;

    .line 106
    iget-object p3, p0, Lcom/android/helper/device/Streamer;->headerBuffer:Ljava/nio/ByteBuffer;

    invoke-virtual {p3, p2}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 107
    iget-object p2, p0, Lcom/android/helper/device/Streamer;->headerBuffer:Ljava/nio/ByteBuffer;

    invoke-virtual {p2}, Ljava/nio/ByteBuffer;->flip()Ljava/nio/Buffer;

    .line 108
    iget-object p2, p0, Lcom/android/helper/device/Streamer;->headerBuffer:Ljava/nio/ByteBuffer;

    invoke-static {p1, p2}, Lcom/android/helper/util/IO;->writeFully(Ljava/io/FileDescriptor;Ljava/nio/ByteBuffer;)V

    return-void
.end method


# virtual methods
.method public getCodec()Lcom/android/helper/util/Codec;
    .locals 1

    .line 35
    iget-object v0, p0, Lcom/android/helper/device/Streamer;->codec:Lcom/android/helper/util/Codec;

    return-object v0
.end method

.method public writeAudioHeader()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 39
    iget-boolean v0, p0, Lcom/android/helper/device/Streamer;->sendCodecMeta:Z

    if-eqz v0, :cond_0

    const/4 v0, 0x4

    .line 40
    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocate(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    .line 41
    iget-object v1, p0, Lcom/android/helper/device/Streamer;->codec:Lcom/android/helper/util/Codec;

    invoke-interface {v1}, Lcom/android/helper/util/Codec;->getId()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 42
    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->flip()Ljava/nio/Buffer;

    .line 43
    iget-object v1, p0, Lcom/android/helper/device/Streamer;->fd:Ljava/io/FileDescriptor;

    invoke-static {v1, v0}, Lcom/android/helper/util/IO;->writeFully(Ljava/io/FileDescriptor;Ljava/nio/ByteBuffer;)V

    :cond_0
    return-void
.end method

.method public writeDisableStream(Z)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/4 v0, 0x4

    .line 62
    new-array v1, v0, [B

    if-eqz p1, :cond_0

    const/4 p1, 0x3

    const/4 v2, 0x1

    .line 64
    aput-byte v2, v1, p1

    .line 66
    :cond_0
    iget-object p1, p0, Lcom/android/helper/device/Streamer;->fd:Ljava/io/FileDescriptor;

    const/4 v2, 0x0

    invoke-static {p1, v1, v2, v0}, Lcom/android/helper/util/IO;->writeFully(Ljava/io/FileDescriptor;[BII)V

    return-void
.end method

.method public writePacket(Ljava/nio/ByteBuffer;JZZ)V
    .locals 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    if-eqz p4, :cond_1

    .line 71
    iget-object v0, p0, Lcom/android/helper/device/Streamer;->codec:Lcom/android/helper/util/Codec;

    sget-object v1, Lcom/android/helper/audio/AudioCodec;->OPUS:Lcom/android/helper/audio/AudioCodec;

    if-ne v0, v1, :cond_0

    .line 72
    invoke-static {p1}, Lcom/android/helper/device/Streamer;->fixOpusConfigPacket(Ljava/nio/ByteBuffer;)V

    goto :goto_0

    .line 73
    :cond_0
    iget-object v0, p0, Lcom/android/helper/device/Streamer;->codec:Lcom/android/helper/util/Codec;

    sget-object v1, Lcom/android/helper/audio/AudioCodec;->FLAC:Lcom/android/helper/audio/AudioCodec;

    if-ne v0, v1, :cond_1

    .line 74
    invoke-static {p1}, Lcom/android/helper/device/Streamer;->fixFlacConfigPacket(Ljava/nio/ByteBuffer;)V

    .line 78
    :cond_1
    :goto_0
    iget-boolean v0, p0, Lcom/android/helper/device/Streamer;->sendFrameMeta:Z

    if-eqz v0, :cond_2

    .line 79
    iget-object v2, p0, Lcom/android/helper/device/Streamer;->fd:Ljava/io/FileDescriptor;

    invoke-virtual {p1}, Ljava/nio/ByteBuffer;->remaining()I

    move-result v3

    move-object v1, p0

    move-wide v4, p2

    move v6, p4

    move v7, p5

    invoke-direct/range {v1 .. v7}, Lcom/android/helper/device/Streamer;->writeFrameMeta(Ljava/io/FileDescriptor;IJZZ)V

    goto :goto_1

    :cond_2
    move-object v1, p0

    .line 82
    :goto_1
    iget-object p2, v1, Lcom/android/helper/device/Streamer;->fd:Ljava/io/FileDescriptor;

    invoke-static {p2, p1}, Lcom/android/helper/util/IO;->writeFully(Ljava/io/FileDescriptor;Ljava/nio/ByteBuffer;)V

    return-void
.end method

.method public writePacket(Ljava/nio/ByteBuffer;Landroid/media/MediaCodec$BufferInfo;)V
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 86
    iget-wide v2, p2, Landroid/media/MediaCodec$BufferInfo;->presentationTimeUs:J

    .line 87
    iget v0, p2, Landroid/media/MediaCodec$BufferInfo;->flags:I

    and-int/lit8 v0, v0, 0x2

    const/4 v1, 0x0

    const/4 v4, 0x1

    if-eqz v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v4, 0x0

    :goto_0
    const/4 v0, 0x1

    .line 88
    iget p2, p2, Landroid/media/MediaCodec$BufferInfo;->flags:I

    and-int/2addr p2, v0

    if-eqz p2, :cond_1

    const/4 v5, 0x1

    goto :goto_1

    :cond_1
    const/4 v5, 0x0

    :goto_1
    move-object v0, p0

    move-object v1, p1

    .line 89
    invoke-virtual/range {v0 .. v5}, Lcom/android/helper/device/Streamer;->writePacket(Ljava/nio/ByteBuffer;JZZ)V

    return-void
.end method

.method public writeVideoHeader(Lcom/android/helper/device/Size;)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 48
    iget-boolean v0, p0, Lcom/android/helper/device/Streamer;->sendCodecMeta:Z

    if-eqz v0, :cond_0

    const/16 v0, 0xc

    .line 49
    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocate(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    .line 50
    iget-object v1, p0, Lcom/android/helper/device/Streamer;->codec:Lcom/android/helper/util/Codec;

    invoke-interface {v1}, Lcom/android/helper/util/Codec;->getId()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 51
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getWidth()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 52
    invoke-virtual {p1}, Lcom/android/helper/device/Size;->getHeight()I

    move-result p1

    invoke-virtual {v0, p1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 53
    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->flip()Ljava/nio/Buffer;

    .line 54
    iget-object p1, p0, Lcom/android/helper/device/Streamer;->fd:Ljava/io/FileDescriptor;

    invoke-static {p1, v0}, Lcom/android/helper/util/IO;->writeFully(Ljava/io/FileDescriptor;Ljava/nio/ByteBuffer;)V

    :cond_0
    return-void
.end method
