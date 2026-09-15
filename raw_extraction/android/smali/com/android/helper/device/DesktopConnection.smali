.class public final Lcom/android/helper/device/DesktopConnection;
.super Ljava/lang/Object;
.source "DesktopConnection.java"

# interfaces
.implements Ljava/io/Closeable;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/device/DesktopConnection$SocketWrapper;,
        Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;,
        Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;
    }
.end annotation


# static fields
.field private static final DEVICE_NAME_FIELD_LENGTH:I = 0x40

.field private static final SOCKET_NAME_PREFIX:Ljava/lang/String; = "scrcpy"


# instance fields
.field private final audioFd:Ljava/io/FileDescriptor;

.field private final audioSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

.field private final controlChannel:Lcom/android/helper/control/ControlChannel;

.field private final controlSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

.field private final touchChannel:Lcom/android/helper/control/ControlChannel;

.field private final touchSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

.field private final videoFd:Ljava/io/FileDescriptor;

.field private final videoSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;


# direct methods
.method private constructor <init>(Lcom/android/helper/device/DesktopConnection$SocketWrapper;Lcom/android/helper/device/DesktopConnection$SocketWrapper;Lcom/android/helper/device/DesktopConnection$SocketWrapper;Lcom/android/helper/device/DesktopConnection$SocketWrapper;)V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 129
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 130
    iput-object p1, p0, Lcom/android/helper/device/DesktopConnection;->videoSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    .line 131
    iput-object p2, p0, Lcom/android/helper/device/DesktopConnection;->audioSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    .line 132
    iput-object p3, p0, Lcom/android/helper/device/DesktopConnection;->controlSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    .line 133
    iput-object p4, p0, Lcom/android/helper/device/DesktopConnection;->touchSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    const/4 v0, 0x0

    if-eqz p1, :cond_0

    .line 135
    invoke-interface {p1}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getFileDescriptor()Ljava/io/FileDescriptor;

    move-result-object p1

    goto :goto_0

    :cond_0
    move-object p1, v0

    :goto_0
    iput-object p1, p0, Lcom/android/helper/device/DesktopConnection;->videoFd:Ljava/io/FileDescriptor;

    if-eqz p2, :cond_1

    .line 136
    invoke-interface {p2}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getFileDescriptor()Ljava/io/FileDescriptor;

    move-result-object p1

    goto :goto_1

    :cond_1
    move-object p1, v0

    :goto_1
    iput-object p1, p0, Lcom/android/helper/device/DesktopConnection;->audioFd:Ljava/io/FileDescriptor;

    if-eqz p3, :cond_2

    .line 137
    new-instance p1, Lcom/android/helper/control/ControlChannel;

    invoke-interface {p3}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getInputStream()Ljava/io/InputStream;

    move-result-object p2

    invoke-interface {p3}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object p3

    invoke-direct {p1, p2, p3}, Lcom/android/helper/control/ControlChannel;-><init>(Ljava/io/InputStream;Ljava/io/OutputStream;)V

    goto :goto_2

    :cond_2
    move-object p1, v0

    :goto_2
    iput-object p1, p0, Lcom/android/helper/device/DesktopConnection;->controlChannel:Lcom/android/helper/control/ControlChannel;

    if-eqz p4, :cond_3

    .line 138
    new-instance v0, Lcom/android/helper/control/ControlChannel;

    invoke-interface {p4}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getInputStream()Ljava/io/InputStream;

    move-result-object p1

    invoke-interface {p4}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object p2

    invoke-direct {v0, p1, p2}, Lcom/android/helper/control/ControlChannel;-><init>(Ljava/io/InputStream;Ljava/io/OutputStream;)V

    :cond_3
    iput-object v0, p0, Lcom/android/helper/device/DesktopConnection;->touchChannel:Lcom/android/helper/control/ControlChannel;

    return-void
.end method

.method private static connectLocal(Ljava/lang/String;)Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 142
    new-instance v0, Landroid/net/LocalSocket;

    invoke-direct {v0}, Landroid/net/LocalSocket;-><init>()V

    .line 143
    new-instance v1, Landroid/net/LocalSocketAddress;

    invoke-direct {v1, p0}, Landroid/net/LocalSocketAddress;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/net/LocalSocket;->connect(Landroid/net/LocalSocketAddress;)V

    .line 144
    new-instance p0, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    invoke-direct {p0, v0}, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;-><init>(Landroid/net/LocalSocket;)V

    return-object p0
.end method

.method private static connectNet(I)Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 148
    new-instance v0, Ljava/net/Socket;

    const-string v1, "127.0.0.1"

    invoke-direct {v0, v1, p0}, Ljava/net/Socket;-><init>(Ljava/lang/String;I)V

    .line 149
    new-instance p0, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    invoke-direct {p0, v0}, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;-><init>(Ljava/net/Socket;)V

    return-object p0
.end method

.method private getFirstSocket()Lcom/android/helper/device/DesktopConnection$SocketWrapper;
    .locals 1

    .line 258
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->videoSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_0

    return-object v0

    .line 259
    :cond_0
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->audioSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_1

    return-object v0

    .line 260
    :cond_1
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->controlSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    return-object v0
.end method

.method private static getSocketName(I)Ljava/lang/String;
    .locals 3

    const/4 v0, -0x1

    .line 153
    const-string v1, "scrcpy"

    if-ne p0, v0, :cond_0

    return-object v1

    .line 156
    :cond_0
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p0

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Object;

    const/4 v2, 0x0

    aput-object p0, v1, v2

    const-string p0, "_%08x"

    invoke-static {p0, v1}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method

.method public static open(Lcom/android/helper/Options;)Lcom/android/helper/device/DesktopConnection;
    .locals 9
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 162
    invoke-virtual {p0}, Lcom/android/helper/Options;->getScid()I

    move-result v0

    .line 163
    invoke-virtual {p0}, Lcom/android/helper/Options;->isTunnelForward()Z

    move-result v1

    .line 164
    invoke-virtual {p0}, Lcom/android/helper/Options;->getVideo()Z

    move-result v2

    .line 165
    invoke-virtual {p0}, Lcom/android/helper/Options;->getAudio()Z

    move-result v3

    .line 166
    invoke-virtual {p0}, Lcom/android/helper/Options;->getControl()Z

    move-result v4

    .line 167
    invoke-virtual {p0}, Lcom/android/helper/Options;->getSendDummyByte()Z

    move-result v5

    .line 168
    invoke-virtual {p0}, Lcom/android/helper/Options;->getPort()I

    move-result v6

    const/4 v7, 0x0

    if-eqz v1, :cond_c

    const/4 v0, 0x0

    if-lez v6, :cond_6

    .line 178
    :try_start_0
    new-instance p0, Ljava/net/ServerSocket;

    invoke-direct {p0}, Ljava/net/ServerSocket;-><init>()V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_b
    .catch Ljava/lang/RuntimeException; {:try_start_0 .. :try_end_0} :catch_a

    const/4 v1, 0x1

    .line 179
    :try_start_1
    invoke-virtual {p0, v1}, Ljava/net/ServerSocket;->setReuseAddress(Z)V

    .line 180
    new-instance v1, Ljava/net/InetSocketAddress;

    invoke-direct {v1, v6}, Ljava/net/InetSocketAddress;-><init>(I)V

    invoke-virtual {p0, v1}, Ljava/net/ServerSocket;->bind(Ljava/net/SocketAddress;)V

    if-eqz v2, :cond_0

    .line 182
    invoke-virtual {p0}, Ljava/net/ServerSocket;->accept()Ljava/net/Socket;

    move-result-object v1

    .line 183
    new-instance v2, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    invoke-direct {v2, v1}, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;-><init>(Ljava/net/Socket;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_3

    if-eqz v5, :cond_1

    .line 185
    :try_start_2
    invoke-interface {v2}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/io/OutputStream;->write(I)V

    const/4 v5, 0x0

    goto :goto_0

    :cond_0
    move-object v2, v7

    :cond_1
    :goto_0
    if-eqz v3, :cond_2

    .line 190
    invoke-virtual {p0}, Ljava/net/ServerSocket;->accept()Ljava/net/Socket;

    move-result-object v1

    .line 191
    new-instance v3, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    invoke-direct {v3, v1}, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;-><init>(Ljava/net/Socket;)V
    :try_end_2
    .catchall {:try_start_2 .. :try_end_2} :catchall_0

    if-eqz v5, :cond_3

    .line 193
    :try_start_3
    invoke-interface {v3}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/io/OutputStream;->write(I)V

    const/4 v5, 0x0

    goto :goto_1

    :catchall_0
    move-exception v0

    move-object v3, v7

    goto :goto_3

    :cond_2
    move-object v3, v7

    :cond_3
    :goto_1
    if-eqz v4, :cond_4

    .line 198
    invoke-virtual {p0}, Ljava/net/ServerSocket;->accept()Ljava/net/Socket;

    move-result-object v1

    .line 199
    new-instance v4, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    invoke-direct {v4, v1}, Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;-><init>(Ljava/net/Socket;)V
    :try_end_3
    .catchall {:try_start_3 .. :try_end_3} :catchall_2

    if-eqz v5, :cond_5

    .line 201
    :try_start_4
    invoke-interface {v4}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/io/OutputStream;->write(I)V
    :try_end_4
    .catchall {:try_start_4 .. :try_end_4} :catchall_1

    goto :goto_2

    :catchall_1
    move-exception v0

    goto :goto_4

    :catchall_2
    move-exception v0

    move-object v4, v7

    goto :goto_4

    :cond_4
    move-object v4, v7

    .line 205
    :cond_5
    :goto_2
    :try_start_5
    invoke-virtual {p0}, Ljava/net/ServerSocket;->close()V
    :try_end_5
    .catch Ljava/io/IOException; {:try_start_5 .. :try_end_5} :catch_1
    .catch Ljava/lang/RuntimeException; {:try_start_5 .. :try_end_5} :catch_0

    move-object p0, v7

    move-object v7, v4

    goto/16 :goto_1c

    :catchall_3
    move-exception v0

    move-object v2, v7

    move-object v3, v2

    :goto_3
    move-object v4, v3

    .line 178
    :goto_4
    :try_start_6
    invoke-virtual {p0}, Ljava/net/ServerSocket;->close()V
    :try_end_6
    .catchall {:try_start_6 .. :try_end_6} :catchall_4

    goto :goto_5

    :catchall_4
    move-exception p0

    :try_start_7
    invoke-virtual {v0, p0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_5
    throw v0
    :try_end_7
    .catch Ljava/io/IOException; {:try_start_7 .. :try_end_7} :catch_1
    .catch Ljava/lang/RuntimeException; {:try_start_7 .. :try_end_7} :catch_0

    :catch_0
    move-exception p0

    goto :goto_6

    :catch_1
    move-exception p0

    :goto_6
    move-object v1, v4

    goto/16 :goto_13

    :cond_6
    if-eqz v2, :cond_8

    .line 209
    :try_start_8
    new-instance v1, Landroid/net/LocalServerSocket;

    invoke-virtual {p0}, Lcom/android/helper/Options;->getVideoSocket()Ljava/lang/String;

    move-result-object v2

    invoke-direct {v1, v2}, Landroid/net/LocalServerSocket;-><init>(Ljava/lang/String;)V
    :try_end_8
    .catch Ljava/io/IOException; {:try_start_8 .. :try_end_8} :catch_b
    .catch Ljava/lang/RuntimeException; {:try_start_8 .. :try_end_8} :catch_a

    .line 210
    :try_start_9
    new-instance v2, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    invoke-virtual {v1}, Landroid/net/LocalServerSocket;->accept()Landroid/net/LocalSocket;

    move-result-object v6

    invoke-direct {v2, v6}, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;-><init>(Landroid/net/LocalSocket;)V
    :try_end_9
    .catchall {:try_start_9 .. :try_end_9} :catchall_6

    if-eqz v5, :cond_7

    .line 212
    :try_start_a
    invoke-interface {v2}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object v6

    invoke-virtual {v6, v0}, Ljava/io/OutputStream;->write(I)V
    :try_end_a
    .catchall {:try_start_a .. :try_end_a} :catchall_5

    goto :goto_7

    :catchall_5
    move-exception p0

    goto :goto_8

    .line 214
    :cond_7
    :goto_7
    :try_start_b
    invoke-virtual {v1}, Landroid/net/LocalServerSocket;->close()V
    :try_end_b
    .catch Ljava/io/IOException; {:try_start_b .. :try_end_b} :catch_7
    .catch Ljava/lang/RuntimeException; {:try_start_b .. :try_end_b} :catch_6

    goto :goto_a

    :catchall_6
    move-exception p0

    move-object v2, v7

    .line 209
    :goto_8
    :try_start_c
    invoke-virtual {v1}, Landroid/net/LocalServerSocket;->close()V
    :try_end_c
    .catchall {:try_start_c .. :try_end_c} :catchall_7

    goto :goto_9

    :catchall_7
    move-exception v0

    :try_start_d
    invoke-virtual {p0, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_9
    throw p0

    :cond_8
    move-object v2, v7

    :goto_a
    if-eqz v3, :cond_a

    .line 217
    new-instance v1, Landroid/net/LocalServerSocket;

    invoke-virtual {p0}, Lcom/android/helper/Options;->getAudioSocket()Ljava/lang/String;

    move-result-object v3

    invoke-direct {v1, v3}, Landroid/net/LocalServerSocket;-><init>(Ljava/lang/String;)V
    :try_end_d
    .catch Ljava/io/IOException; {:try_start_d .. :try_end_d} :catch_7
    .catch Ljava/lang/RuntimeException; {:try_start_d .. :try_end_d} :catch_6

    .line 218
    :try_start_e
    new-instance v3, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    invoke-virtual {v1}, Landroid/net/LocalServerSocket;->accept()Landroid/net/LocalSocket;

    move-result-object v6

    invoke-direct {v3, v6}, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;-><init>(Landroid/net/LocalSocket;)V
    :try_end_e
    .catchall {:try_start_e .. :try_end_e} :catchall_9

    if-eqz v5, :cond_9

    .line 220
    :try_start_f
    invoke-interface {v3}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getOutputStream()Ljava/io/OutputStream;

    move-result-object v5

    invoke-virtual {v5, v0}, Ljava/io/OutputStream;->write(I)V
    :try_end_f
    .catchall {:try_start_f .. :try_end_f} :catchall_8

    goto :goto_b

    :catchall_8
    move-exception p0

    goto :goto_c

    .line 222
    :cond_9
    :goto_b
    :try_start_10
    invoke-virtual {v1}, Landroid/net/LocalServerSocket;->close()V
    :try_end_10
    .catch Ljava/io/IOException; {:try_start_10 .. :try_end_10} :catch_9
    .catch Ljava/lang/RuntimeException; {:try_start_10 .. :try_end_10} :catch_8

    goto :goto_e

    :catchall_9
    move-exception p0

    move-object v3, v7

    .line 217
    :goto_c
    :try_start_11
    invoke-virtual {v1}, Landroid/net/LocalServerSocket;->close()V
    :try_end_11
    .catchall {:try_start_11 .. :try_end_11} :catchall_a

    goto :goto_d

    :catchall_a
    move-exception v0

    :try_start_12
    invoke-virtual {p0, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_d
    throw p0

    :cond_a
    move-object v3, v7

    :goto_e
    if-eqz v4, :cond_b

    .line 225
    new-instance v0, Landroid/net/LocalServerSocket;

    invoke-virtual {p0}, Lcom/android/helper/Options;->getControlSocket()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Landroid/net/LocalServerSocket;-><init>(Ljava/lang/String;)V
    :try_end_12
    .catch Ljava/io/IOException; {:try_start_12 .. :try_end_12} :catch_9
    .catch Ljava/lang/RuntimeException; {:try_start_12 .. :try_end_12} :catch_8

    .line 226
    :try_start_13
    new-instance v1, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    invoke-virtual {v0}, Landroid/net/LocalServerSocket;->accept()Landroid/net/LocalSocket;

    move-result-object v4

    invoke-direct {v1, v4}, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;-><init>(Landroid/net/LocalSocket;)V
    :try_end_13
    .catchall {:try_start_13 .. :try_end_13} :catchall_b

    .line 227
    :try_start_14
    invoke-virtual {v0}, Landroid/net/LocalServerSocket;->close()V
    :try_end_14
    .catch Ljava/io/IOException; {:try_start_14 .. :try_end_14} :catch_5
    .catch Ljava/lang/RuntimeException; {:try_start_14 .. :try_end_14} :catch_4

    goto :goto_10

    :catchall_b
    move-exception p0

    .line 225
    :try_start_15
    invoke-virtual {v0}, Landroid/net/LocalServerSocket;->close()V
    :try_end_15
    .catchall {:try_start_15 .. :try_end_15} :catchall_c

    goto :goto_f

    :catchall_c
    move-exception v0

    :try_start_16
    invoke-virtual {p0, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_f
    throw p0
    :try_end_16
    .catch Ljava/io/IOException; {:try_start_16 .. :try_end_16} :catch_9
    .catch Ljava/lang/RuntimeException; {:try_start_16 .. :try_end_16} :catch_8

    :cond_b
    move-object v1, v7

    .line 230
    :goto_10
    :try_start_17
    new-instance v0, Landroid/net/LocalServerSocket;

    invoke-virtual {p0}, Lcom/android/helper/Options;->getTouchSocket()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Landroid/net/LocalServerSocket;-><init>(Ljava/lang/String;)V
    :try_end_17
    .catch Ljava/io/IOException; {:try_start_17 .. :try_end_17} :catch_5
    .catch Ljava/lang/RuntimeException; {:try_start_17 .. :try_end_17} :catch_4

    .line 231
    :try_start_18
    new-instance p0, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    invoke-virtual {v0}, Landroid/net/LocalServerSocket;->accept()Landroid/net/LocalSocket;

    move-result-object v4

    invoke-direct {p0, v4}, Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;-><init>(Landroid/net/LocalSocket;)V
    :try_end_18
    .catchall {:try_start_18 .. :try_end_18} :catchall_d

    .line 232
    :try_start_19
    invoke-virtual {v0}, Landroid/net/LocalServerSocket;->close()V
    :try_end_19
    .catch Ljava/io/IOException; {:try_start_19 .. :try_end_19} :catch_3
    .catch Ljava/lang/RuntimeException; {:try_start_19 .. :try_end_19} :catch_2

    move-object v7, v1

    goto/16 :goto_1c

    :catch_2
    move-exception v0

    goto :goto_11

    :catch_3
    move-exception v0

    :goto_11
    move-object v7, v0

    move-object v0, p0

    move-object p0, v7

    goto :goto_16

    :catchall_d
    move-exception p0

    .line 230
    :try_start_1a
    invoke-virtual {v0}, Landroid/net/LocalServerSocket;->close()V
    :try_end_1a
    .catchall {:try_start_1a .. :try_end_1a} :catchall_e

    goto :goto_12

    :catchall_e
    move-exception v0

    :try_start_1b
    invoke-virtual {p0, v0}, Ljava/lang/Throwable;->addSuppressed(Ljava/lang/Throwable;)V

    :goto_12
    throw p0
    :try_end_1b
    .catch Ljava/io/IOException; {:try_start_1b .. :try_end_1b} :catch_5
    .catch Ljava/lang/RuntimeException; {:try_start_1b .. :try_end_1b} :catch_4

    :catch_4
    move-exception p0

    goto :goto_13

    :catch_5
    move-exception p0

    :goto_13
    move-object v0, v7

    goto :goto_16

    :cond_c
    if-lez v6, :cond_10

    if-eqz v2, :cond_d

    .line 236
    :try_start_1c
    invoke-static {v6}, Lcom/android/helper/device/DesktopConnection;->connectNet(I)Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    move-result-object p0
    :try_end_1c
    .catch Ljava/io/IOException; {:try_start_1c .. :try_end_1c} :catch_b
    .catch Ljava/lang/RuntimeException; {:try_start_1c .. :try_end_1c} :catch_a

    move-object v2, p0

    goto :goto_14

    :cond_d
    move-object v2, v7

    :goto_14
    if-eqz v3, :cond_e

    .line 237
    :try_start_1d
    invoke-static {v6}, Lcom/android/helper/device/DesktopConnection;->connectNet(I)Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    move-result-object p0
    :try_end_1d
    .catch Ljava/io/IOException; {:try_start_1d .. :try_end_1d} :catch_7
    .catch Ljava/lang/RuntimeException; {:try_start_1d .. :try_end_1d} :catch_6

    move-object v3, p0

    goto :goto_17

    :catch_6
    move-exception p0

    goto :goto_15

    :catch_7
    move-exception p0

    :goto_15
    move-object v0, v7

    move-object v1, v0

    move-object v3, v1

    :goto_16
    move-object v7, v2

    goto :goto_1e

    :cond_e
    move-object v3, v7

    :goto_17
    if-eqz v4, :cond_f

    .line 238
    :try_start_1e
    invoke-static {v6}, Lcom/android/helper/device/DesktopConnection;->connectNet(I)Lcom/android/helper/device/DesktopConnection$NetSocketWrapper;

    move-result-object p0
    :try_end_1e
    .catch Ljava/io/IOException; {:try_start_1e .. :try_end_1e} :catch_9
    .catch Ljava/lang/RuntimeException; {:try_start_1e .. :try_end_1e} :catch_8

    :goto_18
    move-object v8, v7

    move-object v7, p0

    move-object p0, v8

    goto :goto_1c

    :catch_8
    move-exception p0

    goto :goto_19

    :catch_9
    move-exception p0

    :goto_19
    move-object v0, v7

    move-object v1, v0

    goto :goto_16

    :cond_f
    move-object p0, v7

    goto :goto_1c

    .line 240
    :cond_10
    :try_start_1f
    invoke-static {v0}, Lcom/android/helper/device/DesktopConnection;->getSocketName(I)Ljava/lang/String;

    move-result-object p0

    if-eqz v2, :cond_11

    .line 241
    invoke-static {p0}, Lcom/android/helper/device/DesktopConnection;->connectLocal(Ljava/lang/String;)Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    move-result-object v0
    :try_end_1f
    .catch Ljava/io/IOException; {:try_start_1f .. :try_end_1f} :catch_b
    .catch Ljava/lang/RuntimeException; {:try_start_1f .. :try_end_1f} :catch_a

    move-object v2, v0

    goto :goto_1a

    :cond_11
    move-object v2, v7

    :goto_1a
    if-eqz v3, :cond_12

    .line 242
    :try_start_20
    invoke-static {p0}, Lcom/android/helper/device/DesktopConnection;->connectLocal(Ljava/lang/String;)Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    move-result-object v0
    :try_end_20
    .catch Ljava/io/IOException; {:try_start_20 .. :try_end_20} :catch_7
    .catch Ljava/lang/RuntimeException; {:try_start_20 .. :try_end_20} :catch_6

    move-object v3, v0

    goto :goto_1b

    :cond_12
    move-object v3, v7

    :goto_1b
    if-eqz v4, :cond_f

    .line 243
    :try_start_21
    invoke-static {p0}, Lcom/android/helper/device/DesktopConnection;->connectLocal(Ljava/lang/String;)Lcom/android/helper/device/DesktopConnection$LocalSocketWrapper;

    move-result-object p0
    :try_end_21
    .catch Ljava/io/IOException; {:try_start_21 .. :try_end_21} :catch_9
    .catch Ljava/lang/RuntimeException; {:try_start_21 .. :try_end_21} :catch_8

    goto :goto_18

    .line 254
    :goto_1c
    new-instance v0, Lcom/android/helper/device/DesktopConnection;

    invoke-direct {v0, v2, v3, v7, p0}, Lcom/android/helper/device/DesktopConnection;-><init>(Lcom/android/helper/device/DesktopConnection$SocketWrapper;Lcom/android/helper/device/DesktopConnection$SocketWrapper;Lcom/android/helper/device/DesktopConnection$SocketWrapper;Lcom/android/helper/device/DesktopConnection$SocketWrapper;)V

    return-object v0

    :catch_a
    move-exception p0

    goto :goto_1d

    :catch_b
    move-exception p0

    :goto_1d
    move-object v0, v7

    move-object v1, v0

    move-object v3, v1

    :goto_1e
    if-eqz v7, :cond_13

    .line 247
    invoke-interface {v7}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    :cond_13
    if-eqz v3, :cond_14

    .line 248
    invoke-interface {v3}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    :cond_14
    if-eqz v1, :cond_15

    .line 249
    invoke-interface {v1}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    :cond_15
    if-eqz v0, :cond_16

    .line 250
    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    .line 251
    :cond_16
    throw p0
.end method


# virtual methods
.method public close()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 271
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->videoSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_0

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    .line 272
    :cond_0
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->audioSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_1

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    .line 273
    :cond_1
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->controlSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_2

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    .line 274
    :cond_2
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->touchSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_3

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->close()V

    :cond_3
    return-void
.end method

.method public getAudioFd()Ljava/io/FileDescriptor;
    .locals 1

    .line 287
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->audioFd:Ljava/io/FileDescriptor;

    return-object v0
.end method

.method public getControlChannel()Lcom/android/helper/control/ControlChannel;
    .locals 1

    .line 288
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->controlChannel:Lcom/android/helper/control/ControlChannel;

    return-object v0
.end method

.method public getTouchChannel()Lcom/android/helper/control/ControlChannel;
    .locals 1

    .line 289
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->touchChannel:Lcom/android/helper/control/ControlChannel;

    return-object v0
.end method

.method public getVideoFd()Ljava/io/FileDescriptor;
    .locals 1

    .line 286
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->videoFd:Ljava/io/FileDescriptor;

    return-object v0
.end method

.method public sendDeviceMeta(Ljava/lang/String;)V
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    const/16 v0, 0x40

    .line 278
    new-array v1, v0, [B

    .line 279
    sget-object v2, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-virtual {p1, v2}, Ljava/lang/String;->getBytes(Ljava/nio/charset/Charset;)[B

    move-result-object p1

    const/16 v2, 0x3f

    .line 280
    invoke-static {p1, v2}, Lcom/android/helper/util/StringUtils;->getUtf8TruncationIndex([BI)I

    move-result v2

    const/4 v3, 0x0

    .line 281
    invoke-static {p1, v3, v1, v3, v2}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    .line 282
    invoke-direct {p0}, Lcom/android/helper/device/DesktopConnection;->getFirstSocket()Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    move-result-object p1

    invoke-interface {p1}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->getFileDescriptor()Ljava/io/FileDescriptor;

    move-result-object p1

    .line 283
    invoke-static {p1, v1, v3, v0}, Lcom/android/helper/util/IO;->writeFully(Ljava/io/FileDescriptor;[BII)V

    return-void
.end method

.method public shutdown()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 264
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->videoSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_0

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownInput()V

    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->videoSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownOutput()V

    .line 265
    :cond_0
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->audioSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_1

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownInput()V

    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->audioSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownOutput()V

    .line 266
    :cond_1
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->controlSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_2

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownInput()V

    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->controlSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownOutput()V

    .line 267
    :cond_2
    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->touchSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    if-eqz v0, :cond_3

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownInput()V

    iget-object v0, p0, Lcom/android/helper/device/DesktopConnection;->touchSocket:Lcom/android/helper/device/DesktopConnection$SocketWrapper;

    invoke-interface {v0}, Lcom/android/helper/device/DesktopConnection$SocketWrapper;->shutdownOutput()V

    :cond_3
    return-void
.end method
