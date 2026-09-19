package com.android.helper.device;

import android.net.LocalServerSocket;
import android.net.LocalSocket;
import android.net.LocalSocketAddress;
import android.os.ParcelFileDescriptor;
import com.android.helper.Options;
import com.android.helper.control.ControlChannel;
import com.android.helper.util.IO;
import com.android.helper.util.StringUtils;
import java.io.Closeable;
import java.io.FileDescriptor;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/* JADX INFO: loaded from: classes.dex */
public final class DesktopConnection implements Closeable {
    private static final int DEVICE_NAME_FIELD_LENGTH = 64;
    private static final String SOCKET_NAME_PREFIX = "scrcpy";
    private final FileDescriptor audioFd;
    private final SocketWrapper audioSocket;
    private final ControlChannel controlChannel;
    private final SocketWrapper controlSocket;
    private final ControlChannel touchChannel;
    private final SocketWrapper touchSocket;
    private final FileDescriptor videoFd;
    private final SocketWrapper videoSocket;

    private interface SocketWrapper extends Closeable {
        FileDescriptor getFileDescriptor();

        InputStream getInputStream() throws IOException;

        OutputStream getOutputStream() throws IOException;

        void shutdownInput() throws IOException;

        void shutdownOutput() throws IOException;
    }

    private static class LocalSocketWrapper implements SocketWrapper {
        private final LocalSocket socket;

        public LocalSocketWrapper(LocalSocket localSocket) {
            this.socket = localSocket;
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public FileDescriptor getFileDescriptor() {
            return this.socket.getFileDescriptor();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public InputStream getInputStream() throws IOException {
            return this.socket.getInputStream();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public OutputStream getOutputStream() throws IOException {
            return this.socket.getOutputStream();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public void shutdownInput() throws IOException {
            this.socket.shutdownInput();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public void shutdownOutput() throws IOException {
            this.socket.shutdownOutput();
        }

        @Override // java.io.Closeable, java.lang.AutoCloseable
        public void close() throws IOException {
            this.socket.close();
        }
    }

    private static class NetSocketWrapper implements SocketWrapper {
        private final ParcelFileDescriptor pfd;
        private final Socket socket;

        public NetSocketWrapper(Socket socket) {
            this.socket = socket;
            this.pfd = ParcelFileDescriptor.fromSocket(socket);
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public FileDescriptor getFileDescriptor() {
            return this.pfd.getFileDescriptor();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public InputStream getInputStream() throws IOException {
            return this.socket.getInputStream();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public OutputStream getOutputStream() throws IOException {
            return this.socket.getOutputStream();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public void shutdownInput() throws IOException {
            this.socket.shutdownInput();
        }

        @Override // com.android.helper.device.DesktopConnection.SocketWrapper
        public void shutdownOutput() throws IOException {
            this.socket.shutdownOutput();
        }

        @Override // java.io.Closeable, java.lang.AutoCloseable
        public void close() throws IOException {
            try {
                this.pfd.close();
            } finally {
                this.socket.close();
            }
        }
    }

    private DesktopConnection(SocketWrapper socketWrapper, SocketWrapper socketWrapper2, SocketWrapper socketWrapper3, SocketWrapper socketWrapper4) throws IOException {
        this.videoSocket = socketWrapper;
        this.audioSocket = socketWrapper2;
        this.controlSocket = socketWrapper3;
        this.touchSocket = socketWrapper4;
        this.videoFd = socketWrapper != null ? socketWrapper.getFileDescriptor() : null;
        this.audioFd = socketWrapper2 != null ? socketWrapper2.getFileDescriptor() : null;
        this.controlChannel = socketWrapper3 != null ? new ControlChannel(socketWrapper3.getInputStream(), socketWrapper3.getOutputStream()) : null;
        this.touchChannel = socketWrapper4 != null ? new ControlChannel(socketWrapper4.getInputStream(), socketWrapper4.getOutputStream()) : null;
    }

    private static LocalSocketWrapper connectLocal(String str) throws IOException {
        LocalSocket localSocket = new LocalSocket();
        localSocket.connect(new LocalSocketAddress(str));
        return new LocalSocketWrapper(localSocket);
    }

    private static NetSocketWrapper connectNet(int i) throws IOException {
        return new NetSocketWrapper(new Socket("127.0.0.1", i));
    }

    private static String getSocketName(int i) {
        if (i == -1) {
            return SOCKET_NAME_PREFIX;
        }
        return SOCKET_NAME_PREFIX + String.format("_%08x", Integer.valueOf(i));
    }

    /* JADX WARN: Code duplicated, block: B:132:0x0176 A[PHI: r2 r3
  0x0176: PHI (r2v6 java.lang.Object) = (r2v4 java.lang.Object), (r2v9 java.lang.Object) binds: [B:142:0x018e, B:125:0x0166] A[DONT_GENERATE, DONT_INLINE]
  0x0176: PHI (r3v8 java.lang.Object) = (r3v6 java.lang.Object), (r3v11 java.lang.Object) binds: [B:142:0x018e, B:125:0x0166] A[DONT_GENERATE, DONT_INLINE]] */
    /* JADX WARN: Code duplicated, block: B:152:0x01a3  */
    /* JADX WARN: Code duplicated, block: B:154:0x01a8  */
    /* JADX WARN: Code duplicated, block: B:156:0x01ad  */
    /* JADX WARN: Code duplicated, block: B:158:0x01b2  */
    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r1v1 */
    /* JADX WARN: Type inference failed for: r1v11, types: [com.android.helper.device.DesktopConnection$LocalSocketWrapper] */
    /* JADX WARN: Type inference failed for: r1v14 */
    /* JADX WARN: Type inference failed for: r1v16 */
    /* JADX WARN: Type inference failed for: r1v2 */
    /* JADX WARN: Type inference failed for: r1v24 */
    /* JADX WARN: Type inference failed for: r1v25 */
    /* JADX WARN: Type inference failed for: r1v26 */
    /* JADX WARN: Type inference failed for: r1v27 */
    /* JADX WARN: Type inference failed for: r1v3 */
    /* JADX WARN: Type inference failed for: r1v4, types: [com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r1v5 */
    /* JADX WARN: Type inference failed for: r1v6 */
    /* JADX WARN: Type inference failed for: r1v7 */
    /* JADX WARN: Type inference failed for: r1v8 */
    /* JADX WARN: Type inference failed for: r1v9 */
    /* JADX WARN: Type inference failed for: r2v0, types: [boolean] */
    /* JADX WARN: Type inference failed for: r2v1 */
    /* JADX WARN: Type inference failed for: r2v11, types: [com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r2v12 */
    /* JADX WARN: Type inference failed for: r2v13 */
    /* JADX WARN: Type inference failed for: r2v15 */
    /* JADX WARN: Type inference failed for: r2v16 */
    /* JADX WARN: Type inference failed for: r2v17, types: [com.android.helper.device.DesktopConnection$LocalSocketWrapper, com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r2v18 */
    /* JADX WARN: Type inference failed for: r2v19 */
    /* JADX WARN: Type inference failed for: r2v2 */
    /* JADX WARN: Type inference failed for: r2v20 */
    /* JADX WARN: Type inference failed for: r2v21 */
    /* JADX WARN: Type inference failed for: r2v22 */
    /* JADX WARN: Type inference failed for: r2v23 */
    /* JADX WARN: Type inference failed for: r2v24 */
    /* JADX WARN: Type inference failed for: r2v25 */
    /* JADX WARN: Type inference failed for: r2v26, types: [com.android.helper.device.DesktopConnection$NetSocketWrapper, com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r2v27 */
    /* JADX WARN: Type inference failed for: r2v28 */
    /* JADX WARN: Type inference failed for: r2v29 */
    /* JADX WARN: Type inference failed for: r2v30 */
    /* JADX WARN: Type inference failed for: r2v31 */
    /* JADX WARN: Type inference failed for: r2v32 */
    /* JADX WARN: Type inference failed for: r2v33 */
    /* JADX WARN: Type inference failed for: r2v34 */
    /* JADX WARN: Type inference failed for: r2v35 */
    /* JADX WARN: Type inference failed for: r2v36 */
    /* JADX WARN: Type inference failed for: r2v37 */
    /* JADX WARN: Type inference failed for: r2v38 */
    /* JADX WARN: Type inference failed for: r3v0, types: [boolean] */
    /* JADX WARN: Type inference failed for: r3v1 */
    /* JADX WARN: Type inference failed for: r3v13, types: [com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r3v14 */
    /* JADX WARN: Type inference failed for: r3v15 */
    /* JADX WARN: Type inference failed for: r3v19 */
    /* JADX WARN: Type inference failed for: r3v2 */
    /* JADX WARN: Type inference failed for: r3v20 */
    /* JADX WARN: Type inference failed for: r3v21 */
    /* JADX WARN: Type inference failed for: r3v22 */
    /* JADX WARN: Type inference failed for: r3v23 */
    /* JADX WARN: Type inference failed for: r3v24 */
    /* JADX WARN: Type inference failed for: r3v25 */
    /* JADX WARN: Type inference failed for: r3v26 */
    /* JADX WARN: Type inference failed for: r3v27 */
    /* JADX WARN: Type inference failed for: r3v28, types: [com.android.helper.device.DesktopConnection$NetSocketWrapper, com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r3v29 */
    /* JADX WARN: Type inference failed for: r3v3, types: [com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r3v30 */
    /* JADX WARN: Type inference failed for: r3v31 */
    /* JADX WARN: Type inference failed for: r3v32 */
    /* JADX WARN: Type inference failed for: r3v33 */
    /* JADX WARN: Type inference failed for: r3v34 */
    /* JADX WARN: Type inference failed for: r3v35 */
    /* JADX WARN: Type inference failed for: r3v36 */
    /* JADX WARN: Type inference failed for: r3v37 */
    /* JADX WARN: Type inference failed for: r3v38 */
    /* JADX WARN: Type inference failed for: r3v39 */
    /* JADX WARN: Type inference failed for: r3v4 */
    /* JADX WARN: Type inference failed for: r4v0, types: [boolean] */
    /* JADX WARN: Type inference failed for: r4v10 */
    /* JADX WARN: Type inference failed for: r4v11 */
    /* JADX WARN: Type inference failed for: r4v3 */
    /* JADX WARN: Type inference failed for: r4v4 */
    /* JADX WARN: Type inference failed for: r4v5 */
    /* JADX WARN: Type inference failed for: r4v6 */
    /* JADX WARN: Type inference failed for: r4v7 */
    /* JADX WARN: Type inference failed for: r4v8 */
    /* JADX WARN: Type inference failed for: r4v9, types: [com.android.helper.device.DesktopConnection$NetSocketWrapper, com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r7v0 */
    /* JADX WARN: Type inference failed for: r7v1, types: [com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r7v2 */
    /* JADX WARN: Type inference failed for: r7v3 */
    /* JADX WARN: Type inference failed for: r7v4, types: [com.android.helper.device.DesktopConnection$SocketWrapper] */
    /* JADX WARN: Type inference failed for: r7v6 */
    /* JADX WARN: Type inference failed for: r7v7 */
    /* JADX WARN: Type inference failed for: r7v8 */
    public static DesktopConnection open(Options options) throws Throwable {
        LocalSocketWrapper localSocketWrapper;
        ?? r1;
        ?? r3;
        ?? r2;
        ?? r4;
        ?? r5;
        Object objConnectLocal;
        Object objConnectLocal2;
        LocalSocketWrapper localSocketWrapper2;
        Object objConnectLocal3;
        Object obj;
        Object obj2;
        ?? r6;
        ?? r7;
        ?? localSocketWrapper3;
        ?? r8;
        int scid = options.getScid();
        boolean zIsTunnelForward = options.isTunnelForward();
        ?? video = options.getVideo();
        ?? audio = options.getAudio();
        ?? control = options.getControl();
        boolean sendDummyByte = options.getSendDummyByte();
        int port = options.getPort();
        ?? r9 = 0;
        ?? r10 = 0;
        try {
            try {
                try {
                    if (zIsTunnelForward) {
                        if (port > 0) {
                            ServerSocket serverSocket = new ServerSocket();
                            try {
                                try {
                                    serverSocket.setReuseAddress(true);
                                    serverSocket.bind(new InetSocketAddress(port));
                                    if (video != 0) {
                                        video = new NetSocketWrapper(serverSocket.accept());
                                        if (sendDummyByte) {
                                            try {
                                                video = video;
                                                video.getOutputStream().write(0);
                                                sendDummyByte = false;
                                                video = video;
                                            } catch (Throwable th) {
                                                th = th;
                                                audio = 0;
                                                video = video;
                                                control = audio;
                                                try {
                                                    serverSocket.close();
                                                } catch (Throwable th2) {
                                                    th.addSuppressed(th2);
                                                }
                                                throw th;
                                            }
                                        }
                                    } else {
                                        video = 0;
                                    }
                                    if (audio != 0) {
                                        audio = new NetSocketWrapper(serverSocket.accept());
                                        audio = audio;
                                        if (sendDummyByte) {
                                            try {
                                                audio.getOutputStream().write(0);
                                                sendDummyByte = false;
                                                audio = audio;
                                            } catch (Throwable th3) {
                                                th = th3;
                                                control = 0;
                                                serverSocket.close();
                                                throw th;
                                            }
                                        }
                                    } else {
                                        audio = 0;
                                    }
                                    if (control != 0) {
                                        control = new NetSocketWrapper(serverSocket.accept());
                                        if (sendDummyByte) {
                                            try {
                                                r8 = control;
                                                control.getOutputStream().write(0);
                                                r8 = control;
                                            } catch (Throwable th4) {
                                                th = th4;
                                                serverSocket.close();
                                                throw th;
                                            }
                                        }
                                    } else {
                                        r8 = 0;
                                    }
                                    r8 = control;
                                    serverSocket.close();
                                    localSocketWrapper2 = null;
                                    r10 = r8;
                                    r7 = video;
                                    r6 = audio;
                                } catch (Throwable th5) {
                                    th = th5;
                                    video = 0;
                                    audio = 0;
                                }
                            } catch (IOException | RuntimeException e) {
                                e = e;
                                localSocketWrapper3 = control;
                                localSocketWrapper = null;
                                r2 = localSocketWrapper3;
                                r5 = video;
                                r4 = audio;
                                r9 = r5;
                                r1 = r2;
                                r3 = r4;
                                if (r9 != 0) {
                                    r9.close();
                                }
                                if (r3 != 0) {
                                    r3.close();
                                }
                                if (r1 != 0) {
                                    r1.close();
                                }
                                if (localSocketWrapper != null) {
                                    localSocketWrapper.close();
                                }
                                throw e;
                            }
                        } else {
                            if (video != 0) {
                                LocalServerSocket localServerSocket = new LocalServerSocket(options.getVideoSocket());
                                try {
                                    video = new LocalSocketWrapper(localServerSocket.accept());
                                    if (sendDummyByte) {
                                        try {
                                            video.getOutputStream().write(0);
                                        } catch (Throwable th6) {
                                            th = th6;
                                            try {
                                                localServerSocket.close();
                                            } catch (Throwable th7) {
                                                th.addSuppressed(th7);
                                            }
                                            throw th;
                                        }
                                    }
                                    localServerSocket.close();
                                    video = video;
                                } catch (Throwable th8) {
                                    th = th8;
                                    video = 0;
                                }
                            } else {
                                video = 0;
                            }
                            if (audio != 0) {
                                LocalServerSocket localServerSocket2 = new LocalServerSocket(options.getAudioSocket());
                                try {
                                    LocalSocketWrapper localSocketWrapper4 = new LocalSocketWrapper(localServerSocket2.accept());
                                    if (sendDummyByte) {
                                        try {
                                            localSocketWrapper4.getOutputStream().write(0);
                                        } catch (Throwable th9) {
                                            th = th9;
                                            try {
                                                localServerSocket2.close();
                                            } catch (Throwable th10) {
                                                th.addSuppressed(th10);
                                            }
                                            throw th;
                                        }
                                    }
                                    localServerSocket2.close();
                                    audio = localSocketWrapper4;
                                } catch (Throwable th11) {
                                    th = th11;
                                }
                            } else {
                                audio = 0;
                            }
                            if (control != 0) {
                                LocalServerSocket localServerSocket3 = new LocalServerSocket(options.getControlSocket());
                                try {
                                    localSocketWrapper3 = new LocalSocketWrapper(localServerSocket3.accept());
                                    try {
                                        localServerSocket3.close();
                                        localSocketWrapper3 = localSocketWrapper3;
                                    } catch (IOException e2) {
                                        e = e2;
                                        localSocketWrapper = null;
                                        r2 = localSocketWrapper3;
                                        r5 = video;
                                        r4 = audio;
                                    } catch (RuntimeException e3) {
                                        e = e3;
                                        localSocketWrapper = null;
                                        r2 = localSocketWrapper3;
                                        r5 = video;
                                        r4 = audio;
                                    }
                                } catch (Throwable th12) {
                                    try {
                                        localServerSocket3.close();
                                    } catch (Throwable th13) {
                                        th12.addSuppressed(th13);
                                    }
                                    throw th12;
                                }
                            } else {
                                localSocketWrapper3 = 0;
                            }
                            LocalServerSocket localServerSocket4 = new LocalServerSocket(options.getTouchSocket());
                            try {
                                localSocketWrapper2 = new LocalSocketWrapper(localServerSocket4.accept());
                                try {
                                    localServerSocket4.close();
                                    r10 = localSocketWrapper3;
                                    r7 = video;
                                    r6 = audio;
                                } catch (IOException | RuntimeException e4) {
                                    localSocketWrapper = localSocketWrapper2;
                                    e = e4;
                                    r2 = localSocketWrapper3;
                                    r5 = video;
                                    r4 = audio;
                                }
                            } catch (Throwable th14) {
                                try {
                                    localServerSocket4.close();
                                } catch (Throwable th15) {
                                    th14.addSuppressed(th15);
                                }
                                throw th14;
                            }
                        }
                        r9 = r5;
                        r1 = r2;
                        r3 = r4;
                        if (r9 != 0) {
                            r9.close();
                        }
                        if (r3 != 0) {
                            r3.close();
                        }
                        if (r1 != 0) {
                            r1.close();
                        }
                        if (localSocketWrapper != null) {
                            localSocketWrapper.close();
                        }
                        throw e;
                    }
                    if (port > 0) {
                        objConnectLocal = video != 0 ? connectNet(port) : null;
                        objConnectLocal2 = audio != 0 ? connectNet(port) : null;
                        if (control != 0) {
                            obj2 = objConnectLocal;
                            obj = objConnectLocal2;
                            objConnectLocal3 = connectNet(port);
                            r10 = objConnectLocal3;
                            localSocketWrapper2 = null;
                            r7 = obj2;
                            r6 = obj;
                        } else {
                            localSocketWrapper2 = null;
                            r7 = objConnectLocal;
                            r6 = objConnectLocal2;
                        }
                    } else {
                        String socketName = getSocketName(scid);
                        objConnectLocal = video != 0 ? connectLocal(socketName) : null;
                        objConnectLocal2 = audio != 0 ? connectLocal(socketName) : null;
                        if (control != 0) {
                            obj2 = objConnectLocal;
                            obj = objConnectLocal2;
                            objConnectLocal3 = connectLocal(socketName);
                            r10 = objConnectLocal3;
                            localSocketWrapper2 = null;
                            r7 = obj2;
                            r6 = obj;
                        } else {
                            localSocketWrapper2 = null;
                            r7 = objConnectLocal;
                            r6 = objConnectLocal2;
                        }
                    }
                    return new DesktopConnection(r7, r6, r10, localSocketWrapper2);
                } catch (IOException | RuntimeException e5) {
                    e = e5;
                    localSocketWrapper = null;
                    r2 = 0;
                    r5 = video;
                    r4 = audio;
                }
            } catch (IOException | RuntimeException e6) {
                e = e6;
                localSocketWrapper = null;
                r2 = 0;
                r4 = 0;
                r5 = video;
            }
        } catch (IOException | RuntimeException e7) {
            e = e7;
            localSocketWrapper = null;
            r1 = 0;
            r3 = 0;
        }
    }

    private SocketWrapper getFirstSocket() {
        SocketWrapper socketWrapper = this.videoSocket;
        if (socketWrapper != null) {
            return socketWrapper;
        }
        SocketWrapper socketWrapper2 = this.audioSocket;
        return socketWrapper2 != null ? socketWrapper2 : this.controlSocket;
    }

    public void shutdown() throws IOException {
        SocketWrapper socketWrapper = this.videoSocket;
        if (socketWrapper != null) {
            socketWrapper.shutdownInput();
            this.videoSocket.shutdownOutput();
        }
        SocketWrapper socketWrapper2 = this.audioSocket;
        if (socketWrapper2 != null) {
            socketWrapper2.shutdownInput();
            this.audioSocket.shutdownOutput();
        }
        SocketWrapper socketWrapper3 = this.controlSocket;
        if (socketWrapper3 != null) {
            socketWrapper3.shutdownInput();
            this.controlSocket.shutdownOutput();
        }
        SocketWrapper socketWrapper4 = this.touchSocket;
        if (socketWrapper4 != null) {
            socketWrapper4.shutdownInput();
            this.touchSocket.shutdownOutput();
        }
    }

    @Override // java.io.Closeable, java.lang.AutoCloseable
    public void close() throws IOException {
        SocketWrapper socketWrapper = this.videoSocket;
        if (socketWrapper != null) {
            socketWrapper.close();
        }
        SocketWrapper socketWrapper2 = this.audioSocket;
        if (socketWrapper2 != null) {
            socketWrapper2.close();
        }
        SocketWrapper socketWrapper3 = this.controlSocket;
        if (socketWrapper3 != null) {
            socketWrapper3.close();
        }
        SocketWrapper socketWrapper4 = this.touchSocket;
        if (socketWrapper4 != null) {
            socketWrapper4.close();
        }
    }

    public void sendDeviceMeta(String str) throws IOException {
        byte[] bArr = new byte[DEVICE_NAME_FIELD_LENGTH];
        byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
        System.arraycopy(bytes, 0, bArr, 0, StringUtils.getUtf8TruncationIndex(bytes, 63));
        IO.writeFully(getFirstSocket().getFileDescriptor(), bArr, 0, DEVICE_NAME_FIELD_LENGTH);
    }

    public FileDescriptor getVideoFd() {
        return this.videoFd;
    }

    public FileDescriptor getAudioFd() {
        return this.audioFd;
    }

    public ControlChannel getControlChannel() {
        return this.controlChannel;
    }

    public ControlChannel getTouchChannel() {
        return this.touchChannel;
    }
}
