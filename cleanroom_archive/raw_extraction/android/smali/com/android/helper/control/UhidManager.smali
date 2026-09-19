.class public final Lcom/android/helper/control/UhidManager;
.super Ljava/lang/Object;
.source "UhidManager.java"


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field private static final BUS_VIRTUAL:S = 0x6s

.field private static final INPUT_PORT:Ljava/lang/String;

.field private static final SIZE_OF_UHID_EVENT:I = 0x111c

.field private static final UHID_CREATE2:I = 0xb

.field private static final UHID_INPUT2:I = 0xc

.field private static final UHID_OUTPUT:I = 0x6


# instance fields
.field private final buffer:Ljava/nio/ByteBuffer;

.field private final displayUniqueId:Ljava/lang/String;

.field private final fds:Landroid/util/ArrayMap;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Landroid/util/ArrayMap<",
            "Ljava/lang/Integer;",
            "Ljava/io/FileDescriptor;",
            ">;"
        }
    .end annotation
.end field

.field private final queue:Landroid/os/MessageQueue;

.field private final sender:Lcom/android/helper/control/DeviceMessageSender;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 36
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "scrcpy:"

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Landroid/system/Os;->getpid()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sput-object v0, Lcom/android/helper/control/UhidManager;->INPUT_PORT:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/control/DeviceMessageSender;Ljava/lang/String;)V
    .locals 2

    .line 46
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 40
    new-instance v0, Landroid/util/ArrayMap;

    invoke-direct {v0}, Landroid/util/ArrayMap;-><init>()V

    iput-object v0, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    const/16 v0, 0x111c

    .line 41
    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocate(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    invoke-static {}, Ljava/nio/ByteOrder;->nativeOrder()Ljava/nio/ByteOrder;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->order(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/control/UhidManager;->buffer:Ljava/nio/ByteBuffer;

    .line 47
    iput-object p1, p0, Lcom/android/helper/control/UhidManager;->sender:Lcom/android/helper/control/DeviceMessageSender;

    .line 48
    iput-object p2, p0, Lcom/android/helper/control/UhidManager;->displayUniqueId:Ljava/lang/String;

    .line 49
    sget p1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 p2, 0x17

    if-lt p1, p2, :cond_0

    .line 50
    new-instance p1, Landroid/os/HandlerThread;

    const-string p2, "UHidManager"

    invoke-direct {p1, p2}, Landroid/os/HandlerThread;-><init>(Ljava/lang/String;)V

    .line 51
    invoke-virtual {p1}, Landroid/os/HandlerThread;->start()V

    .line 52
    invoke-virtual {p1}, Landroid/os/HandlerThread;->getLooper()Landroid/os/Looper;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/os/Looper;)Landroid/os/MessageQueue;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/control/UhidManager;->queue:Landroid/os/MessageQueue;

    return-void

    :cond_0
    const/4 p1, 0x0

    .line 54
    iput-object p1, p0, Lcom/android/helper/control/UhidManager;->queue:Landroid/os/MessageQueue;

    return-void
.end method

.method private addUniqueIdAssociation()V
    .locals 3

    .line 277
    invoke-direct {p0}, Lcom/android/helper/control/UhidManager;->mustUseInputPort()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 278
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getInputManager()Lcom/android/helper/wrappers/InputManager;

    move-result-object v0

    sget-object v1, Lcom/android/helper/control/UhidManager;->INPUT_PORT:Ljava/lang/String;

    iget-object v2, p0, Lcom/android/helper/control/UhidManager;->displayUniqueId:Ljava/lang/String;

    invoke-virtual {v0, v1, v2}, Lcom/android/helper/wrappers/InputManager;->addUniqueIdAssociationByPort(Ljava/lang/String;Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method private static buildUhidCreate2Req(IILjava/lang/String;[BLjava/lang/String;)[B
    .locals 3

    .line 187
    array-length v0, p3

    add-int/lit16 v0, v0, 0x118

    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocate(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    invoke-static {}, Ljava/nio/ByteOrder;->nativeOrder()Ljava/nio/ByteOrder;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->order(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;

    move-result-object v0

    const/16 v1, 0xb

    .line 188
    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 190
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    if-eqz v1, :cond_0

    const-string p2, "scrcpy"

    .line 191
    :cond_0
    sget-object v1, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p2, v1}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p2

    const/16 v1, 0x7f

    .line 192
    invoke-static {p2, v1}, Lcom/android/helper/util/StringUtils;->getUtf8TruncationIndex([BI)I

    move-result v1

    const/4 v2, 0x0

    .line 194
    invoke-virtual {v0, p2, v2, v1}, Ljava/nio/ByteBuffer;->put([BII)Ljava/nio/ByteBuffer;

    if-eqz p4, :cond_1

    const/16 p2, 0x84

    .line 197
    invoke-virtual {v0, p2}, Ljava/nio/ByteBuffer;->position(I)Ljava/nio/Buffer;

    .line 198
    sget-object p2, Ljava/nio/charset/StandardCharsets;->US_ASCII:Ljava/nio/charset/Charset;

    invoke-virtual {p4, p2}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p2

    .line 200
    invoke-virtual {v0, p2}, Ljava/nio/ByteBuffer;->put([B)Ljava/nio/ByteBuffer;

    :cond_1
    const/16 p2, 0x104

    .line 203
    invoke-virtual {v0, p2}, Ljava/nio/ByteBuffer;->position(I)Ljava/nio/Buffer;

    .line 204
    array-length p2, p3

    int-to-short p2, p2

    invoke-virtual {v0, p2}, Ljava/nio/ByteBuffer;->putShort(S)Ljava/nio/ByteBuffer;

    const/4 p2, 0x6

    .line 205
    invoke-virtual {v0, p2}, Ljava/nio/ByteBuffer;->putShort(S)Ljava/nio/ByteBuffer;

    .line 206
    invoke-virtual {v0, p0}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 207
    invoke-virtual {v0, p1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 208
    invoke-virtual {v0, v2}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 209
    invoke-virtual {v0, v2}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 210
    invoke-virtual {v0, p3}, Ljava/nio/ByteBuffer;->put([B)Ljava/nio/ByteBuffer;

    .line 211
    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->array()[B

    move-result-object p0

    return-object p0
.end method

.method private static buildUhidInput2Req([B)[B
    .locals 2

    .line 228
    array-length v0, p0

    add-int/lit8 v0, v0, 0x6

    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocate(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    invoke-static {}, Ljava/nio/ByteOrder;->nativeOrder()Ljava/nio/ByteOrder;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->order(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;

    move-result-object v0

    const/16 v1, 0xc

    .line 229
    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->putInt(I)Ljava/nio/ByteBuffer;

    .line 230
    array-length v1, p0

    int-to-short v1, v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->putShort(S)Ljava/nio/ByteBuffer;

    .line 231
    invoke-virtual {v0, p0}, Ljava/nio/ByteBuffer;->put([B)Ljava/nio/ByteBuffer;

    .line 232
    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->array()[B

    move-result-object p0

    return-object p0
.end method

.method private static close(Ljava/io/FileDescriptor;)V
    .locals 2

    .line 266
    :try_start_0
    invoke-static {p0}, Landroid/system/Os;->close(Ljava/io/FileDescriptor;)V
    :try_end_0
    .catch Landroid/system/ErrnoException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p0

    .line 268
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Failed to close uhid: "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0}, Landroid/system/ErrnoException;->getMessage()Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return-void
.end method

.method private static extractHidOutputData(Ljava/nio/ByteBuffer;)[B
    .locals 4

    .line 136
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->remaining()I

    move-result v0

    const/16 v1, 0x1003

    const/4 v2, 0x0

    if-ge v0, v1, :cond_0

    .line 137
    const-string p0, "Incomplete HID output"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-object v2

    .line 140
    :cond_0
    invoke-virtual {p0}, Ljava/nio/ByteBuffer;->position()I

    move-result v0

    const/16 v1, 0x1000

    add-int/2addr v0, v1

    invoke-virtual {p0, v0}, Ljava/nio/ByteBuffer;->getShort(I)S

    move-result v0

    const v3, 0xffff

    and-int/2addr v0, v3

    if-le v0, v1, :cond_1

    .line 142
    new-instance p0, Ljava/lang/StringBuilder;

    const-string v1, "Incorrect HID output size: "

    invoke-direct {p0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-object v2

    .line 145
    :cond_1
    new-array v0, v0, [B

    .line 146
    invoke-virtual {p0, v0}, Ljava/nio/ByteBuffer;->get([B)Ljava/nio/ByteBuffer;

    return-object v0
.end method

.method private mustUseInputPort()Z
    .locals 2

    .line 273
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x23

    if-lt v0, v1, :cond_0

    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->displayUniqueId:Ljava/lang/String;

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    return v0

    :cond_0
    const/4 v0, 0x0

    return v0
.end method

.method private registerUhidListener(ILjava/io/FileDescriptor;)V
    .locals 2

    .line 89
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x17

    if-lt v0, v1, :cond_0

    .line 90
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->queue:Landroid/os/MessageQueue;

    new-instance v1, Lcom/android/helper/control/UhidManager$$ExternalSyntheticLambda3;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/control/UhidManager$$ExternalSyntheticLambda3;-><init>(Lcom/android/helper/control/UhidManager;I)V

    const/4 p1, 0x1

    invoke-static {v0, p2, p1, v1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/os/MessageQueue;Ljava/io/FileDescriptor;ILandroid/os/MessageQueue$OnFileDescriptorEventListener;)V

    :cond_0
    return-void
.end method

.method private removeUniqueIdAssociation()V
    .locals 2

    .line 283
    invoke-direct {p0}, Lcom/android/helper/control/UhidManager;->mustUseInputPort()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 284
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getInputManager()Lcom/android/helper/wrappers/InputManager;

    move-result-object v0

    sget-object v1, Lcom/android/helper/control/UhidManager;->INPUT_PORT:Ljava/lang/String;

    invoke-virtual {v0, v1}, Lcom/android/helper/wrappers/InputManager;->removeUniqueIdAssociationByPort(Ljava/lang/String;)V

    :cond_0
    return-void
.end method

.method private unregisterUhidListener(Ljava/io/FileDescriptor;)V
    .locals 2

    .line 115
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x17

    if-lt v0, v1, :cond_0

    .line 116
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->queue:Landroid/os/MessageQueue;

    invoke-static {v0, p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/os/MessageQueue;Ljava/io/FileDescriptor;)V

    :cond_0
    return-void
.end method


# virtual methods
.method public close(I)V
    .locals 2

    .line 238
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/util/ArrayMap;->remove(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/io/FileDescriptor;

    if-eqz v0, :cond_1

    .line 240
    invoke-direct {p0, v0}, Lcom/android/helper/control/UhidManager;->unregisterUhidListener(Ljava/io/FileDescriptor;)V

    .line 241
    invoke-static {v0}, Lcom/android/helper/control/UhidManager;->close(Ljava/io/FileDescriptor;)V

    .line 243
    iget-object p1, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-virtual {p1}, Landroid/util/ArrayMap;->isEmpty()Z

    move-result p1

    if-eqz p1, :cond_0

    .line 245
    invoke-direct {p0}, Lcom/android/helper/control/UhidManager;->removeUniqueIdAssociation()V

    :cond_0
    return-void

    .line 248
    :cond_1
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Closing unknown UHID device: "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void
.end method

.method public closeAll()V
    .locals 2

    .line 253
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-virtual {v0}, Landroid/util/ArrayMap;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_0

    return-void

    .line 257
    :cond_0
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-virtual {v0}, Landroid/util/ArrayMap;->values()Ljava/util/Collection;

    move-result-object v0

    invoke-interface {v0}, Ljava/util/Collection;->iterator()Ljava/util/Iterator;

    move-result-object v0

    :goto_0
    invoke-interface {v0}, Ljava/util/Iterator;->hasNext()Z

    move-result v1

    if-eqz v1, :cond_1

    invoke-interface {v0}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Ljava/io/FileDescriptor;

    .line 258
    invoke-static {v1}, Lcom/android/helper/control/UhidManager;->close(Ljava/io/FileDescriptor;)V

    goto :goto_0

    .line 261
    :cond_1
    invoke-direct {p0}, Lcom/android/helper/control/UhidManager;->removeUniqueIdAssociation()V

    return-void
.end method

.method synthetic lambda$registerUhidListener$0$com-android-helper-control-UhidManager(ILjava/io/FileDescriptor;I)I
    .locals 1

    .line 92
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->buffer:Ljava/nio/ByteBuffer;

    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->clear()Ljava/nio/Buffer;

    .line 93
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->buffer:Ljava/nio/ByteBuffer;

    invoke-static {p2, v0}, Landroid/system/Os;->read(Ljava/io/FileDescriptor;Ljava/nio/ByteBuffer;)I

    move-result p2

    .line 94
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->buffer:Ljava/nio/ByteBuffer;

    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->flip()Ljava/nio/Buffer;

    if-lez p2, :cond_0

    .line 96
    iget-object p2, p0, Lcom/android/helper/control/UhidManager;->buffer:Ljava/nio/ByteBuffer;

    invoke-virtual {p2}, Ljava/nio/ByteBuffer;->getInt()I

    move-result p2

    const/4 v0, 0x6

    if-ne p2, v0, :cond_0

    .line 98
    iget-object p2, p0, Lcom/android/helper/control/UhidManager;->buffer:Ljava/nio/ByteBuffer;

    invoke-static {p2}, Lcom/android/helper/control/UhidManager;->extractHidOutputData(Ljava/nio/ByteBuffer;)[B

    move-result-object p2

    if-eqz p2, :cond_0

    .line 100
    invoke-static {p1, p2}, Lcom/android/helper/control/DeviceMessage;->createUhidOutput(I[B)Lcom/android/helper/control/DeviceMessage;

    move-result-object p1

    .line 101
    iget-object p2, p0, Lcom/android/helper/control/UhidManager;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {p2, p1}, Lcom/android/helper/control/DeviceMessageSender;->send(Lcom/android/helper/control/DeviceMessage;)V
    :try_end_0
    .catch Landroid/system/ErrnoException; {:try_start_0 .. :try_end_0} :catch_1
    .catch Ljava/io/InterruptedIOException; {:try_start_0 .. :try_end_0} :catch_0

    :cond_0
    return p3

    :catch_0
    move-exception p1

    goto :goto_0

    :catch_1
    move-exception p1

    .line 106
    :goto_0
    const-string p2, "Failed to read UHID output"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    const/4 p1, 0x0

    return p1
.end method

.method public open(IIILjava/lang/String;[B)V
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const-string v0, "Duplicate UHID id: "

    .line 60
    :try_start_0
    const-string v1, "/dev/uhid"

    sget v2, Landroid/system/OsConstants;->O_RDWR:I

    const/4 v3, 0x0

    invoke-static {v1, v2, v3}, Landroid/system/Os;->open(Ljava/lang/String;II)Ljava/io/FileDescriptor;

    move-result-object v1
    :try_end_0
    .catch Landroid/system/ErrnoException; {:try_start_0 .. :try_end_0} :catch_1

    .line 63
    :try_start_1
    iget-object v2, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-virtual {v2}, Landroid/util/ArrayMap;->isEmpty()Z

    move-result v2

    .line 65
    iget-object v4, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v5

    invoke-virtual {v4, v5, v1}, Landroid/util/ArrayMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v4

    check-cast v4, Ljava/io/FileDescriptor;

    if-eqz v4, :cond_0

    .line 67
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v5, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 68
    invoke-static {v4}, Lcom/android/helper/control/UhidManager;->close(Ljava/io/FileDescriptor;)V

    .line 71
    :cond_0
    invoke-direct {p0}, Lcom/android/helper/control/UhidManager;->mustUseInputPort()Z

    move-result v0

    if-eqz v0, :cond_1

    sget-object v0, Lcom/android/helper/control/UhidManager;->INPUT_PORT:Ljava/lang/String;

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    .line 72
    :goto_0
    invoke-static {p2, p3, p4, p5, v0}, Lcom/android/helper/control/UhidManager;->buildUhidCreate2Req(IILjava/lang/String;[BLjava/lang/String;)[B

    move-result-object p2

    .line 73
    array-length p3, p2

    invoke-static {v1, p2, v3, p3}, Landroid/system/Os;->write(Ljava/io/FileDescriptor;[BII)I

    if-eqz v2, :cond_2

    .line 76
    invoke-direct {p0}, Lcom/android/helper/control/UhidManager;->addUniqueIdAssociation()V

    .line 78
    :cond_2
    invoke-direct {p0, p1, v1}, Lcom/android/helper/control/UhidManager;->registerUhidListener(ILjava/io/FileDescriptor;)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0
    .catch Landroid/system/ErrnoException; {:try_start_1 .. :try_end_1} :catch_1

    return-void

    :catch_0
    move-exception p1

    .line 80
    :try_start_2
    invoke-static {v1}, Lcom/android/helper/control/UhidManager;->close(Ljava/io/FileDescriptor;)V

    .line 81
    throw p1
    :try_end_2
    .catch Landroid/system/ErrnoException; {:try_start_2 .. :try_end_2} :catch_1

    :catch_1
    move-exception p1

    .line 84
    new-instance p2, Ljava/io/IOException;

    invoke-direct {p2, p1}, Ljava/io/IOException;-><init>(Ljava/lang/Throwable;)V

    throw p2
.end method

.method public writeInput(I[B)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 151
    iget-object v0, p0, Lcom/android/helper/control/UhidManager;->fds:Landroid/util/ArrayMap;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-virtual {v0, v1}, Landroid/util/ArrayMap;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/io/FileDescriptor;

    if-nez v0, :cond_0

    .line 153
    new-instance p2, Ljava/lang/StringBuilder;

    const-string v0, "Unknown UHID id: "

    invoke-direct {p2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    .line 158
    :cond_0
    :try_start_0
    invoke-static {p2}, Lcom/android/helper/control/UhidManager;->buildUhidInput2Req([B)[B

    move-result-object p1

    .line 159
    array-length p2, p1

    const/4 v1, 0x0

    invoke-static {v0, p1, v1, p2}, Landroid/system/Os;->write(Ljava/io/FileDescriptor;[BII)I
    :try_end_0
    .catch Landroid/system/ErrnoException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 161
    new-instance p2, Ljava/io/IOException;

    invoke-direct {p2, p1}, Ljava/io/IOException;-><init>(Ljava/lang/Throwable;)V

    throw p2
.end method
