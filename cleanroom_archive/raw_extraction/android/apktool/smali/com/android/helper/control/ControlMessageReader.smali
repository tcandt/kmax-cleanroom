.class public Lcom/android/helper/control/ControlMessageReader;
.super Ljava/lang/Object;
.source "ControlMessageReader.java"


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field public static final CLIPBOARD_TEXT_MAX_LENGTH:I = 0x3fff2

.field public static final INJECT_TEXT_MAX_LENGTH:I = 0x12c

.field private static final MESSAGE_MAX_SIZE:I = 0x40000


# instance fields
.field private final dis:Ljava/io/DataInputStream;


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>(Ljava/io/InputStream;)V
    .locals 2

    .line 21
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 22
    new-instance v0, Ljava/io/DataInputStream;

    new-instance v1, Ljava/io/BufferedInputStream;

    invoke-direct {v1, p1}, Ljava/io/BufferedInputStream;-><init>(Ljava/io/InputStream;)V

    invoke-direct {v0, v1}, Ljava/io/DataInputStream;-><init>(Ljava/io/InputStream;)V

    iput-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    return-void
.end method

.method private parseBackOrScreenOnEvent()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 131
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedByte()I

    move-result v0

    .line 132
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createBackOrScreenOn(I)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseBufferLength(I)I
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/4 v0, 0x0

    const/4 v1, 0x0

    :goto_0
    if-ge v0, p1, :cond_0

    shl-int/lit8 v1, v1, 0x8

    .line 84
    iget-object v2, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v2}, Ljava/io/DataInputStream;->readUnsignedByte()I

    move-result v2

    or-int/2addr v1, v2

    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_0
    return v1
.end method

.method private parseByteArray(I)[B
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 100
    invoke-direct {p0, p1}, Lcom/android/helper/control/ControlMessageReader;->parseBufferLength(I)I

    move-result p1

    .line 101
    new-array p1, p1, [B

    .line 102
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0, p1}, Ljava/io/DataInputStream;->readFully([B)V

    return-object p1
.end method

.method private parseGetClipboard()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 136
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedByte()I

    move-result v0

    .line 137
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createGetClipboard(I)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseInjectKeycode()Lcom/android/helper/control/ControlMessage;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 73
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedByte()I

    move-result v0

    .line 74
    iget-object v1, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v1}, Ljava/io/DataInputStream;->readInt()I

    move-result v1

    .line 75
    iget-object v2, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v2}, Ljava/io/DataInputStream;->readInt()I

    move-result v2

    .line 76
    iget-object v3, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v3}, Ljava/io/DataInputStream;->readInt()I

    move-result v3

    .line 77
    invoke-static {v0, v1, v2, v3}, Lcom/android/helper/control/ControlMessage;->createInjectKeycode(IIII)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseInjectScrollEvent()Lcom/android/helper/control/ControlMessage;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 122
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parsePosition()Lcom/android/helper/device/Position;

    move-result-object v0

    .line 124
    iget-object v1, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v1}, Ljava/io/DataInputStream;->readShort()S

    move-result v1

    invoke-static {v1}, Lcom/android/helper/util/Binary;->i16FixedPointToFloat(S)F

    move-result v1

    const/high16 v2, 0x41800000    # 16.0f

    mul-float v1, v1, v2

    .line 125
    iget-object v3, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v3}, Ljava/io/DataInputStream;->readShort()S

    move-result v3

    invoke-static {v3}, Lcom/android/helper/util/Binary;->i16FixedPointToFloat(S)F

    move-result v3

    mul-float v3, v3, v2

    .line 126
    iget-object v2, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v2}, Ljava/io/DataInputStream;->readInt()I

    move-result v2

    .line 127
    invoke-static {v0, v1, v3, v2}, Lcom/android/helper/control/ControlMessage;->createInjectScrollEvent(Lcom/android/helper/device/Position;FFI)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseInjectText()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 107
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseString()Ljava/lang/String;

    move-result-object v0

    .line 108
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createInjectText(Ljava/lang/String;)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseInjectTouchEvent()Lcom/android/helper/control/ControlMessage;
    .locals 8
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 112
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedByte()I

    move-result v1

    .line 113
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readLong()J

    move-result-wide v2

    .line 114
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parsePosition()Lcom/android/helper/device/Position;

    move-result-object v4

    .line 115
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readShort()S

    move-result v0

    invoke-static {v0}, Lcom/android/helper/util/Binary;->u16FixedPointToFloat(S)F

    move-result v5

    .line 116
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readInt()I

    move-result v6

    .line 117
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readInt()I

    move-result v7

    .line 118
    invoke-static/range {v1 .. v7}, Lcom/android/helper/control/ControlMessage;->createInjectTouchEvent(IJLcom/android/helper/device/Position;FII)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parsePosition()Lcom/android/helper/device/Position;
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 178
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readInt()I

    move-result v0

    .line 179
    iget-object v1, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v1}, Ljava/io/DataInputStream;->readInt()I

    move-result v1

    .line 180
    iget-object v2, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v2}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v2

    .line 181
    iget-object v3, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v3}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v3

    .line 182
    new-instance v4, Lcom/android/helper/device/Position;

    invoke-direct {v4, v0, v1, v2, v3}, Lcom/android/helper/device/Position;-><init>(IIII)V

    return-object v4
.end method

.method private parseSetBitrate()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 68
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readInt()I

    move-result v0

    .line 69
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createSetBitrate(I)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseSetClipboard()Lcom/android/helper/control/ControlMessage;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 141
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readLong()J

    move-result-wide v0

    .line 142
    iget-object v2, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v2}, Ljava/io/DataInputStream;->readByte()B

    move-result v2

    if-eqz v2, :cond_0

    const/4 v2, 0x1

    goto :goto_0

    :cond_0
    const/4 v2, 0x0

    .line 143
    :goto_0
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseString()Ljava/lang/String;

    move-result-object v3

    .line 144
    invoke-static {v0, v1, v3, v2}, Lcom/android/helper/control/ControlMessage;->createSetClipboard(JLjava/lang/String;Z)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseSetDisplayPower()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 148
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readBoolean()Z

    move-result v0

    .line 149
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createSetDisplayPower(Z)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseStartApp()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/4 v0, 0x1

    .line 173
    invoke-direct {p0, v0}, Lcom/android/helper/control/ControlMessageReader;->parseString(I)Ljava/lang/String;

    move-result-object v0

    .line 174
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createStartApp(Ljava/lang/String;)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseString()Ljava/lang/String;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/4 v0, 0x4

    .line 96
    invoke-direct {p0, v0}, Lcom/android/helper/control/ControlMessageReader;->parseString(I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private parseString(I)Ljava/lang/String;
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 91
    invoke-direct {p0, p1}, Lcom/android/helper/control/ControlMessageReader;->parseByteArray(I)[B

    move-result-object p1

    .line 92
    new-instance v0, Ljava/lang/String;

    sget-object v1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {v0, p1, v1}, Ljava/lang/String;-><init>([BLjava/nio/charset/Charset;)V

    return-object v0
.end method

.method private parseUhidCreate()Lcom/android/helper/control/ControlMessage;
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 153
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v0

    .line 154
    iget-object v1, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v1}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v1

    .line 155
    iget-object v2, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v2}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v2

    const/4 v3, 0x1

    .line 156
    invoke-direct {p0, v3}, Lcom/android/helper/control/ControlMessageReader;->parseString(I)Ljava/lang/String;

    move-result-object v3

    const/4 v4, 0x2

    .line 157
    invoke-direct {p0, v4}, Lcom/android/helper/control/ControlMessageReader;->parseByteArray(I)[B

    move-result-object v4

    .line 158
    invoke-static {v0, v1, v2, v3, v4}, Lcom/android/helper/control/ControlMessage;->createUhidCreate(IIILjava/lang/String;[B)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseUhidDestroy()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 168
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v0

    .line 169
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createUhidDestroy(I)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method private parseUhidInput()Lcom/android/helper/control/ControlMessage;
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 162
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedShort()I

    move-result v0

    const/4 v1, 0x2

    .line 163
    invoke-direct {p0, v1}, Lcom/android/helper/control/ControlMessageReader;->parseByteArray(I)[B

    move-result-object v1

    .line 164
    invoke-static {v0, v1}, Lcom/android/helper/control/ControlMessage;->createUhidInput(I[B)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method


# virtual methods
.method public read()Lcom/android/helper/control/ControlMessage;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 26
    iget-object v0, p0, Lcom/android/helper/control/ControlMessageReader;->dis:Ljava/io/DataInputStream;

    invoke-virtual {v0}, Ljava/io/DataInputStream;->readUnsignedByte()I

    move-result v0

    packed-switch v0, :pswitch_data_0

    .line 63
    new-instance v1, Lcom/android/helper/control/ControlProtocolException;

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Unknown event type: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Lcom/android/helper/control/ControlProtocolException;-><init>(Ljava/lang/String;)V

    throw v1

    .line 61
    :pswitch_0
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseSetBitrate()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 59
    :pswitch_1
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseStartApp()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 57
    :pswitch_2
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseUhidDestroy()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 55
    :pswitch_3
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseUhidInput()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 53
    :pswitch_4
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseUhidCreate()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 43
    :pswitch_5
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseSetDisplayPower()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 41
    :pswitch_6
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseSetClipboard()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 39
    :pswitch_7
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseGetClipboard()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 51
    :pswitch_8
    invoke-static {v0}, Lcom/android/helper/control/ControlMessage;->createEmpty(I)Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 37
    :pswitch_9
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseBackOrScreenOnEvent()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 35
    :pswitch_a
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseInjectScrollEvent()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 33
    :pswitch_b
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseInjectTouchEvent()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 31
    :pswitch_c
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseInjectText()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    .line 29
    :pswitch_d
    invoke-direct {p0}, Lcom/android/helper/control/ControlMessageReader;->parseInjectKeycode()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_d
        :pswitch_c
        :pswitch_b
        :pswitch_a
        :pswitch_9
        :pswitch_8
        :pswitch_8
        :pswitch_8
        :pswitch_7
        :pswitch_6
        :pswitch_5
        :pswitch_8
        :pswitch_4
        :pswitch_3
        :pswitch_2
        :pswitch_8
        :pswitch_1
        :pswitch_8
        :pswitch_8
        :pswitch_0
    .end packed-switch
.end method
