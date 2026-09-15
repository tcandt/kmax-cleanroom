.class public final Lcom/android/helper/control/ControlChannel;
.super Ljava/lang/Object;
.source "ControlChannel.java"


# instance fields
.field private final reader:Lcom/android/helper/control/ControlMessageReader;

.field private final writer:Lcom/android/helper/control/DeviceMessageWriter;


# direct methods
.method public constructor <init>(Ljava/io/InputStream;Ljava/io/OutputStream;)V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 12
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 13
    new-instance v0, Lcom/android/helper/control/ControlMessageReader;

    invoke-direct {v0, p1}, Lcom/android/helper/control/ControlMessageReader;-><init>(Ljava/io/InputStream;)V

    iput-object v0, p0, Lcom/android/helper/control/ControlChannel;->reader:Lcom/android/helper/control/ControlMessageReader;

    .line 14
    new-instance p1, Lcom/android/helper/control/DeviceMessageWriter;

    invoke-direct {p1, p2}, Lcom/android/helper/control/DeviceMessageWriter;-><init>(Ljava/io/OutputStream;)V

    iput-object p1, p0, Lcom/android/helper/control/ControlChannel;->writer:Lcom/android/helper/control/DeviceMessageWriter;

    return-void
.end method


# virtual methods
.method public recv()Lcom/android/helper/control/ControlMessage;
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 18
    iget-object v0, p0, Lcom/android/helper/control/ControlChannel;->reader:Lcom/android/helper/control/ControlMessageReader;

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessageReader;->read()Lcom/android/helper/control/ControlMessage;

    move-result-object v0

    return-object v0
.end method

.method public send(Lcom/android/helper/control/DeviceMessage;)V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 22
    iget-object v0, p0, Lcom/android/helper/control/ControlChannel;->writer:Lcom/android/helper/control/DeviceMessageWriter;

    invoke-virtual {v0, p1}, Lcom/android/helper/control/DeviceMessageWriter;->write(Lcom/android/helper/control/DeviceMessage;)V

    return-void
.end method
