.class public Lcom/android/helper/control/DeviceMessageWriter;
.super Ljava/lang/Object;
.source "DeviceMessageWriter.java"


# static fields
.field public static final CLIPBOARD_TEXT_MAX_LENGTH:I = 0x3fffb

.field private static final MESSAGE_MAX_SIZE:I = 0x40000


# instance fields
.field private final dos:Ljava/io/DataOutputStream;


# direct methods
.method public constructor <init>(Ljava/io/OutputStream;)V
    .locals 2

    .line 18
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 19
    new-instance v0, Ljava/io/DataOutputStream;

    new-instance v1, Ljava/io/BufferedOutputStream;

    invoke-direct {v1, p1}, Ljava/io/BufferedOutputStream;-><init>(Ljava/io/OutputStream;)V

    invoke-direct {v0, v1}, Ljava/io/DataOutputStream;-><init>(Ljava/io/OutputStream;)V

    iput-object v0, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    return-void
.end method


# virtual methods
.method public write(Lcom/android/helper/control/DeviceMessage;)V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 23
    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessage;->getType()I

    move-result v0

    .line 24
    iget-object v1, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    invoke-virtual {v1, v0}, Ljava/io/DataOutputStream;->writeByte(I)V

    if-eqz v0, :cond_2

    const/4 v1, 0x1

    if-eq v0, v1, :cond_1

    const/4 v1, 0x2

    if-ne v0, v1, :cond_0

    .line 37
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessage;->getId()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/io/DataOutputStream;->writeShort(I)V

    .line 38
    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessage;->getData()[B

    move-result-object p1

    .line 39
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    array-length v1, p1

    invoke-virtual {v0, v1}, Ljava/io/DataOutputStream;->writeShort(I)V

    .line 40
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    invoke-virtual {v0, p1}, Ljava/io/DataOutputStream;->write([B)V

    goto :goto_0

    .line 43
    :cond_0
    new-instance p1, Lcom/android/helper/control/ControlProtocolException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Unknown event type: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p1, v0}, Lcom/android/helper/control/ControlProtocolException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 34
    :cond_1
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessage;->getSequence()J

    move-result-wide v1

    invoke-virtual {v0, v1, v2}, Ljava/io/DataOutputStream;->writeLong(J)V

    goto :goto_0

    .line 27
    :cond_2
    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessage;->getText()Ljava/lang/String;

    move-result-object p1

    .line 28
    sget-object v0, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, v0}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    const v0, 0x3fffb

    .line 29
    invoke-static {p1, v0}, Lcom/android/helper/util/StringUtils;->getUtf8TruncationIndex([BI)I

    move-result v0

    .line 30
    iget-object v1, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    invoke-virtual {v1, v0}, Ljava/io/DataOutputStream;->writeInt(I)V

    .line 31
    iget-object v1, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    const/4 v2, 0x0

    invoke-virtual {v1, p1, v2, v0}, Ljava/io/DataOutputStream;->write([BII)V

    .line 45
    :goto_0
    iget-object p1, p0, Lcom/android/helper/control/DeviceMessageWriter;->dos:Ljava/io/DataOutputStream;

    invoke-virtual {p1}, Ljava/io/DataOutputStream;->flush()V

    return-void
.end method
