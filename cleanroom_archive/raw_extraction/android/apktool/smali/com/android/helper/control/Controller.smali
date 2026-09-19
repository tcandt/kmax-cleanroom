.class public Lcom/android/helper/control/Controller;
.super Ljava/lang/Object;
.source "Controller.java"

# interfaces
.implements Lcom/android/helper/AsyncProcessor;
.implements Lcom/android/helper/video/VirtualDisplayListener;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/android/helper/control/Controller$DisplayData;
    }
.end annotation


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field private static final DEFAULT_DEVICE_ID:I = 0x0

.field private static final EXECUTOR:Ljava/util/concurrent/ScheduledExecutorService;

.field private static final POINTER_ID_MOUSE:I = -0x1


# instance fields
.field private final charMap:Landroid/view/KeyCharacterMap;

.field private final cleanUp:Lcom/android/helper/CleanUp;

.field private final clipboardAutosync:Z

.field private final controlChannel:Lcom/android/helper/control/ControlChannel;

.field private final displayData:Ljava/util/concurrent/atomic/AtomicReference;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/concurrent/atomic/AtomicReference<",
            "Lcom/android/helper/control/Controller$DisplayData;",
            ">;"
        }
    .end annotation
.end field

.field private final displayDataAvailable:Ljava/lang/Object;

.field private final displayId:I

.field private final isSettingClipboard:Ljava/util/concurrent/atomic/AtomicBoolean;

.field private keepDisplayPowerOff:Z

.field private lastTouchDown:J

.field private final pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

.field private final pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

.field private final pointersState:Lcom/android/helper/control/PointersState;

.field private final powerOn:Z

.field private final sender:Lcom/android/helper/control/DeviceMessageSender;

.field private startAppExecutor:Ljava/util/concurrent/ExecutorService;

.field private final supportsInputEvents:Z

.field private surfaceCapture:Lcom/android/helper/video/SurfaceCapture;

.field private thread:Ljava/lang/Thread;

.field private uhidManager:Lcom/android/helper/control/UhidManager;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .line 71
    invoke-static {}, Ljava/util/concurrent/Executors;->newSingleThreadScheduledExecutor()Ljava/util/concurrent/ScheduledExecutorService;

    move-result-object v0

    sput-object v0, Lcom/android/helper/control/Controller;->EXECUTOR:Ljava/util/concurrent/ScheduledExecutorService;

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/control/ControlChannel;Lcom/android/helper/CleanUp;Lcom/android/helper/Options;)V
    .locals 2

    .line 103
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    const/4 v0, -0x1

    .line 86
    invoke-static {v0}, Landroid/view/KeyCharacterMap;->load(I)Landroid/view/KeyCharacterMap;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/control/Controller;->charMap:Landroid/view/KeyCharacterMap;

    .line 88
    new-instance v0, Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-direct {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;-><init>()V

    iput-object v0, p0, Lcom/android/helper/control/Controller;->isSettingClipboard:Ljava/util/concurrent/atomic/AtomicBoolean;

    .line 90
    new-instance v0, Ljava/util/concurrent/atomic/AtomicReference;

    invoke-direct {v0}, Ljava/util/concurrent/atomic/AtomicReference;-><init>()V

    iput-object v0, p0, Lcom/android/helper/control/Controller;->displayData:Ljava/util/concurrent/atomic/AtomicReference;

    .line 91
    new-instance v0, Ljava/lang/Object;

    invoke-direct {v0}, Ljava/lang/Object;-><init>()V

    iput-object v0, p0, Lcom/android/helper/control/Controller;->displayDataAvailable:Ljava/lang/Object;

    .line 94
    new-instance v0, Lcom/android/helper/control/PointersState;

    invoke-direct {v0}, Lcom/android/helper/control/PointersState;-><init>()V

    iput-object v0, p0, Lcom/android/helper/control/Controller;->pointersState:Lcom/android/helper/control/PointersState;

    const/16 v0, 0xa

    .line 95
    new-array v1, v0, [Landroid/view/MotionEvent$PointerProperties;

    iput-object v1, p0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    .line 96
    new-array v0, v0, [Landroid/view/MotionEvent$PointerCoords;

    iput-object v0, p0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    .line 104
    invoke-virtual {p3}, Lcom/android/helper/Options;->getDisplayId()I

    move-result v0

    iput v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    .line 105
    iput-object p1, p0, Lcom/android/helper/control/Controller;->controlChannel:Lcom/android/helper/control/ControlChannel;

    .line 106
    iput-object p2, p0, Lcom/android/helper/control/Controller;->cleanUp:Lcom/android/helper/CleanUp;

    .line 107
    invoke-virtual {p3}, Lcom/android/helper/Options;->getClipboardAutosync()Z

    move-result p2

    iput-boolean p2, p0, Lcom/android/helper/control/Controller;->clipboardAutosync:Z

    .line 108
    invoke-virtual {p3}, Lcom/android/helper/Options;->getPowerOn()Z

    move-result p3

    iput-boolean p3, p0, Lcom/android/helper/control/Controller;->powerOn:Z

    .line 109
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->initPointers()V

    .line 110
    new-instance p3, Lcom/android/helper/control/DeviceMessageSender;

    invoke-direct {p3, p1}, Lcom/android/helper/control/DeviceMessageSender;-><init>(Lcom/android/helper/control/ControlChannel;)V

    iput-object p3, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    .line 112
    invoke-static {v0}, Lcom/android/helper/device/Device;->supportsInputEvents(I)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-nez p1, :cond_0

    .line 114
    const-string p1, "Input events are not supported for secondary displays before Android 10"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    .line 118
    :cond_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getClipboardManager()Lcom/android/helper/wrappers/ClipboardManager;

    move-result-object p1

    if-eqz p2, :cond_2

    if-eqz p1, :cond_1

    .line 122
    new-instance p2, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda0;

    invoke-direct {p2, p0}, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda0;-><init>(Lcom/android/helper/control/Controller;)V

    invoke-virtual {p1, p2}, Lcom/android/helper/wrappers/ClipboardManager;->addPrimaryClipChangedListener(Landroid/content/ClipboardManager$OnPrimaryClipChangedListener;)V

    return-void

    .line 134
    :cond_1
    const-string p1, "No clipboard manager, copy-paste between device and computer will not work"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    :cond_2
    return-void
.end method

.method private control()V
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 204
    iget-boolean v0, p0, Lcom/android/helper/control/Controller;->powerOn:Z

    if-eqz v0, :cond_0

    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    if-nez v0, :cond_0

    invoke-static {v0}, Lcom/android/helper/device/Device;->isScreenOn(I)Z

    move-result v0

    if-nez v0, :cond_0

    .line 205
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v1, 0x0

    const/16 v2, 0xe0

    invoke-static {v2, v0, v1}, Lcom/android/helper/device/Device;->pressReleaseKeycode(III)Z

    const-wide/16 v0, 0x1f4

    .line 214
    invoke-static {v0, v1}, Landroid/os/SystemClock;->sleep(J)V

    :cond_0
    const/4 v0, 0x1

    .line 218
    :goto_0
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Thread;->isInterrupted()Z

    move-result v1

    if-nez v1, :cond_1

    if-eqz v0, :cond_1

    .line 219
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->handleEvent()Z

    move-result v0

    goto :goto_0

    :cond_1
    return-void
.end method

.method private getActionDisplayId()I
    .locals 2

    .line 636
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v1, -0x1

    if-eq v0, v1, :cond_0

    return v0

    .line 642
    :cond_0
    iget-object v0, p0, Lcom/android/helper/control/Controller;->displayData:Ljava/util/concurrent/atomic/AtomicReference;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicReference;->get()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/android/helper/control/Controller$DisplayData;

    if-nez v0, :cond_1

    const/4 v0, 0x0

    return v0

    .line 648
    :cond_1
    invoke-static {v0}, Lcom/android/helper/control/Controller$DisplayData;->access$100(Lcom/android/helper/control/Controller$DisplayData;)I

    move-result v0

    return v0
.end method

.method private getClipboard(I)V
    .locals 2

    if-eqz p1, :cond_1

    .line 582
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x18

    if-lt v0, v1, :cond_1

    iget-boolean v0, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v0, :cond_1

    const/4 v0, 0x1

    if-ne p1, v0, :cond_0

    const/16 v0, 0x116

    goto :goto_0

    :cond_0
    const/16 v0, 0x115

    :goto_0
    const/4 v1, 0x2

    .line 585
    invoke-direct {p0, v0, v1}, Lcom/android/helper/control/Controller;->pressReleaseKeycode(II)Z

    .line 591
    :cond_1
    iget-boolean v0, p0, Lcom/android/helper/control/Controller;->clipboardAutosync:Z

    if-eqz v0, :cond_2

    if-nez p1, :cond_3

    .line 592
    :cond_2
    invoke-static {}, Lcom/android/helper/device/Device;->getClipboardText()Ljava/lang/String;

    move-result-object p1

    if-eqz p1, :cond_3

    .line 594
    invoke-static {p1}, Lcom/android/helper/control/DeviceMessage;->createClipboard(Ljava/lang/String;)Lcom/android/helper/control/DeviceMessage;

    move-result-object p1

    .line 595
    iget-object v0, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {v0, p1}, Lcom/android/helper/control/DeviceMessageSender;->send(Lcom/android/helper/control/DeviceMessage;)V

    :cond_3
    return-void
.end method

.method private getEventPointAndDisplayId(Lcom/android/helper/device/Position;)Landroid/util/Pair;
    .locals 3
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Lcom/android/helper/device/Position;",
            ")",
            "Landroid/util/Pair<",
            "Lcom/android/helper/device/Point;",
            "Ljava/lang/Integer;",
            ">;"
        }
    .end annotation

    .line 388
    iget-object v0, p0, Lcom/android/helper/control/Controller;->displayData:Ljava/util/concurrent/atomic/AtomicReference;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicReference;->get()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lcom/android/helper/control/Controller$DisplayData;

    if-eqz v0, :cond_2

    .line 396
    invoke-static {v0}, Lcom/android/helper/control/Controller$DisplayData;->access$200(Lcom/android/helper/control/Controller$DisplayData;)Lcom/android/helper/control/PositionMapper;

    move-result-object v1

    invoke-virtual {v1, p1}, Lcom/android/helper/control/PositionMapper;->map(Lcom/android/helper/device/Position;)Lcom/android/helper/device/Point;

    move-result-object v1

    if-nez v1, :cond_1

    .line 398
    sget-object v1, Lcom/android/helper/util/Ln$Level;->VERBOSE:Lcom/android/helper/util/Ln$Level;

    invoke-static {v1}, Lcom/android/helper/util/Ln;->isEnabled(Lcom/android/helper/util/Ln$Level;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 399
    invoke-virtual {p1}, Lcom/android/helper/device/Position;->getScreenSize()Lcom/android/helper/device/Size;

    move-result-object p1

    .line 400
    invoke-static {v0}, Lcom/android/helper/control/Controller$DisplayData;->access$200(Lcom/android/helper/control/Controller$DisplayData;)Lcom/android/helper/control/PositionMapper;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/control/PositionMapper;->getVideoSize()Lcom/android/helper/device/Size;

    move-result-object v0

    .line 401
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Ignore positional event generated for size "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string p1, " (current size is "

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string p1, ")"

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->v(Ljava/lang/String;)V

    :cond_0
    const/4 p1, 0x0

    return-object p1

    .line 405
    :cond_1
    invoke-static {v0}, Lcom/android/helper/control/Controller$DisplayData;->access$100(Lcom/android/helper/control/Controller$DisplayData;)I

    move-result p1

    goto :goto_0

    .line 408
    :cond_2
    invoke-virtual {p1}, Lcom/android/helper/device/Position;->getPoint()Lcom/android/helper/device/Point;

    move-result-object v1

    .line 409
    iget p1, p0, Lcom/android/helper/control/Controller;->displayId:I

    .line 412
    :goto_0
    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    invoke-static {v1, p1}, Landroid/util/Pair;->create(Ljava/lang/Object;Ljava/lang/Object;)Landroid/util/Pair;

    move-result-object p1

    return-object p1
.end method

.method private getStartAppDisplayId()I
    .locals 4

    .line 704
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v1, -0x1

    if-eq v0, v1, :cond_0

    return v0

    :cond_0
    const-wide/16 v2, 0x3e8

    .line 711
    :try_start_0
    invoke-direct {p0, v2, v3}, Lcom/android/helper/control/Controller;->waitDisplayData(J)Lcom/android/helper/control/Controller$DisplayData;

    move-result-object v0

    if-eqz v0, :cond_1

    .line 713
    invoke-static {v0}, Lcom/android/helper/control/Controller$DisplayData;->access$100(Lcom/android/helper/control/Controller$DisplayData;)I

    move-result v0
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    return v0

    :catch_0
    :cond_1
    return v1
.end method

.method private getUhidManager()Lcom/android/helper/control/UhidManager;
    .locals 3

    .line 156
    iget-object v0, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    if-nez v0, :cond_2

    .line 157
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    .line 158
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x23

    if-lt v1, v2, :cond_0

    .line 159
    iget v1, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v2, -0x1

    if-ne v1, v2, :cond_0

    const-wide/16 v1, 0x3e8

    .line 164
    :try_start_0
    invoke-direct {p0, v1, v2}, Lcom/android/helper/control/Controller;->waitDisplayData(J)Lcom/android/helper/control/Controller$DisplayData;

    move-result-object v1

    if-eqz v1, :cond_0

    .line 166
    invoke-static {v1}, Lcom/android/helper/control/Controller$DisplayData;->access$100(Lcom/android/helper/control/Controller$DisplayData;)I

    move-result v0
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    nop

    :cond_0
    :goto_0
    if-lez v0, :cond_1

    .line 177
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v1

    invoke-virtual {v1, v0}, Lcom/android/helper/wrappers/DisplayManager;->getDisplayInfo(I)Lcom/android/helper/device/DisplayInfo;

    move-result-object v0

    if-eqz v0, :cond_1

    .line 179
    invoke-virtual {v0}, Lcom/android/helper/device/DisplayInfo;->getUniqueId()Ljava/lang/String;

    move-result-object v0

    goto :goto_1

    :cond_1
    const/4 v0, 0x0

    .line 182
    :goto_1
    new-instance v1, Lcom/android/helper/control/UhidManager;

    iget-object v2, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-direct {v1, v2, v0}, Lcom/android/helper/control/UhidManager;-><init>(Lcom/android/helper/control/DeviceMessageSender;Ljava/lang/String;)V

    iput-object v1, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    .line 185
    :cond_2
    iget-object v0, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    return-object v0
.end method

.method private handleEvent()Z
    .locals 10
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 261
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/control/Controller;->controlChannel:Lcom/android/helper/control/ControlChannel;

    invoke-virtual {v0}, Lcom/android/helper/control/ControlChannel;->recv()Lcom/android/helper/control/ControlMessage;

    move-result-object v0
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    .line 267
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getType()I

    move-result v1

    packed-switch v1, :pswitch_data_0

    :cond_0
    :goto_0
    move-object v2, p0

    goto/16 :goto_1

    .line 339
    :pswitch_0
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getBitrate()I

    move-result v0

    invoke-static {v0}, Lcom/android/helper/video/SurfaceEncoder;->setVideoBitrate(I)V

    goto :goto_0

    .line 335
    :pswitch_1
    const-string v0, "KeyframeTrace controller-request-keyframe"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 336
    invoke-static {}, Lcom/android/helper/video/SurfaceEncoder;->requestKeyFrame()V

    goto :goto_0

    .line 332
    :pswitch_2
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->resetVideo()V

    goto :goto_0

    .line 329
    :pswitch_3
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getText()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Lcom/android/helper/control/Controller;->startAppAsync(Ljava/lang/String;)V

    goto :goto_0

    .line 326
    :pswitch_4
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->openHardKeyboardSettings()V

    goto :goto_0

    .line 323
    :pswitch_5
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getUhidManager()Lcom/android/helper/control/UhidManager;

    move-result-object v1

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getId()I

    move-result v0

    invoke-virtual {v1, v0}, Lcom/android/helper/control/UhidManager;->close(I)V

    goto :goto_0

    .line 320
    :pswitch_6
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getUhidManager()Lcom/android/helper/control/UhidManager;

    move-result-object v1

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getId()I

    move-result v2

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getData()[B

    move-result-object v0

    invoke-virtual {v1, v2, v0}, Lcom/android/helper/control/UhidManager;->writeInput(I[B)V

    goto :goto_0

    .line 317
    :pswitch_7
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getUhidManager()Lcom/android/helper/control/UhidManager;

    move-result-object v3

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getId()I

    move-result v4

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getVendorId()I

    move-result v5

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getProductId()I

    move-result v6

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getText()Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getData()[B

    move-result-object v8

    invoke-virtual/range {v3 .. v8}, Lcom/android/helper/control/UhidManager;->open(IIILjava/lang/String;[B)V

    goto :goto_0

    .line 314
    :pswitch_8
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getActionDisplayId()I

    move-result v0

    invoke-static {v0}, Lcom/android/helper/device/Device;->rotateDevice(I)V

    goto :goto_0

    .line 309
    :pswitch_9
    iget-boolean v1, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v1, :cond_0

    .line 310
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getOn()Z

    move-result v0

    invoke-direct {p0, v0}, Lcom/android/helper/control/Controller;->setDisplayPower(Z)V

    goto :goto_0

    .line 306
    :pswitch_a
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getText()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getPaste()Z

    move-result v2

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getSequence()J

    move-result-wide v3

    invoke-direct {p0, v1, v2, v3, v4}, Lcom/android/helper/control/Controller;->setClipboard(Ljava/lang/String;ZJ)Z

    goto :goto_0

    .line 303
    :pswitch_b
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getCopyKey()I

    move-result v0

    invoke-direct {p0, v0}, Lcom/android/helper/control/Controller;->getClipboard(I)V

    goto/16 :goto_0

    .line 300
    :pswitch_c
    invoke-static {}, Lcom/android/helper/device/Device;->collapsePanels()V

    goto/16 :goto_0

    .line 297
    :pswitch_d
    invoke-static {}, Lcom/android/helper/device/Device;->expandSettingsPanel()V

    goto/16 :goto_0

    .line 294
    :pswitch_e
    invoke-static {}, Lcom/android/helper/device/Device;->expandNotificationPanel()V

    goto/16 :goto_0

    .line 289
    :pswitch_f
    iget-boolean v1, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v1, :cond_0

    .line 290
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getAction()I

    move-result v0

    invoke-direct {p0, v0}, Lcom/android/helper/control/Controller;->pressBackOrTurnScreenOn(I)Z

    goto/16 :goto_0

    .line 284
    :pswitch_10
    iget-boolean v1, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v1, :cond_0

    .line 285
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getPosition()Lcom/android/helper/device/Position;

    move-result-object v1

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getHScroll()F

    move-result v2

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getVScroll()F

    move-result v3

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getButtons()I

    move-result v0

    invoke-direct {p0, v1, v2, v3, v0}, Lcom/android/helper/control/Controller;->injectScroll(Lcom/android/helper/device/Position;FFI)Z

    goto/16 :goto_0

    .line 279
    :pswitch_11
    iget-boolean v1, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v1, :cond_0

    .line 280
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getAction()I

    move-result v3

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getPointerId()J

    move-result-wide v4

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getPosition()Lcom/android/helper/device/Position;

    move-result-object v6

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getPressure()F

    move-result v7

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getActionButton()I

    move-result v8

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getButtons()I

    move-result v9

    move-object v2, p0

    invoke-direct/range {v2 .. v9}, Lcom/android/helper/control/Controller;->injectTouch(IJLcom/android/helper/device/Position;FII)Z

    goto :goto_1

    :pswitch_12
    move-object v2, p0

    .line 274
    iget-boolean v1, v2, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v1, :cond_1

    .line 275
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getText()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Lcom/android/helper/control/Controller;->injectText(Ljava/lang/String;)I

    goto :goto_1

    :pswitch_13
    move-object v2, p0

    .line 269
    iget-boolean v1, v2, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz v1, :cond_1

    .line 270
    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getAction()I

    move-result v1

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getKeycode()I

    move-result v3

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getRepeat()I

    move-result v4

    invoke-virtual {v0}, Lcom/android/helper/control/ControlMessage;->getMetaState()I

    move-result v0

    invoke-direct {p0, v1, v3, v4, v0}, Lcom/android/helper/control/Controller;->injectKeycode(IIII)Z

    :cond_1
    :goto_1
    const/4 v0, 0x1

    return v0

    :catch_0
    move-object v2, p0

    const/4 v0, 0x0

    return v0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_13
        :pswitch_12
        :pswitch_11
        :pswitch_10
        :pswitch_f
        :pswitch_e
        :pswitch_d
        :pswitch_c
        :pswitch_b
        :pswitch_a
        :pswitch_9
        :pswitch_8
        :pswitch_7
        :pswitch_6
        :pswitch_5
        :pswitch_4
        :pswitch_3
        :pswitch_2
        :pswitch_1
        :pswitch_0
    .end packed-switch
.end method

.method private initPointers()V
    .locals 4

    const/4 v0, 0x0

    :goto_0
    const/16 v1, 0xa

    if-ge v0, v1, :cond_0

    .line 190
    new-instance v1, Landroid/view/MotionEvent$PointerProperties;

    invoke-direct {v1}, Landroid/view/MotionEvent$PointerProperties;-><init>()V

    const/4 v2, 0x1

    .line 191
    iput v2, v1, Landroid/view/MotionEvent$PointerProperties;->toolType:I

    .line 193
    new-instance v2, Landroid/view/MotionEvent$PointerCoords;

    invoke-direct {v2}, Landroid/view/MotionEvent$PointerCoords;-><init>()V

    const/4 v3, 0x0

    .line 194
    iput v3, v2, Landroid/view/MotionEvent$PointerCoords;->orientation:F

    .line 195
    iput v3, v2, Landroid/view/MotionEvent$PointerCoords;->size:F

    .line 197
    iget-object v3, p0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    aput-object v1, v3, v0

    .line 198
    iget-object v1, p0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    aput-object v2, v1, v0

    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_0
    return-void
.end method

.method private injectChar(C)Z
    .locals 6

    .line 357
    invoke-static {p1}, Lcom/android/helper/control/KeyComposition;->decompose(C)Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x1

    const/4 v2, 0x0

    if-eqz v0, :cond_0

    .line 358
    invoke-virtual {v0}, Ljava/lang/String;->toCharArray()[C

    move-result-object p1

    goto :goto_0

    :cond_0
    new-array v0, v1, [C

    aput-char p1, v0, v2

    move-object p1, v0

    .line 359
    :goto_0
    iget-object v0, p0, Lcom/android/helper/control/Controller;->charMap:Landroid/view/KeyCharacterMap;

    invoke-virtual {v0, p1}, Landroid/view/KeyCharacterMap;->getEvents([C)[Landroid/view/KeyEvent;

    move-result-object p1

    if-nez p1, :cond_1

    return v2

    .line 364
    :cond_1
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getActionDisplayId()I

    move-result v0

    .line 365
    array-length v3, p1

    const/4 v4, 0x0

    :goto_1
    if-ge v4, v3, :cond_3

    aget-object v5, p1, v4

    .line 366
    invoke-static {v5, v0, v2}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v5

    if-nez v5, :cond_2

    return v2

    :cond_2
    add-int/lit8 v4, v4, 0x1

    goto :goto_1

    :cond_3
    return v1
.end method

.method private injectKeyEvent(IIIII)Z
    .locals 6

    .line 628
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getActionDisplayId()I

    move-result v4

    move v0, p1

    move v1, p2

    move v2, p3

    move v3, p4

    move v5, p5

    invoke-static/range {v0 .. v5}, Lcom/android/helper/device/Device;->injectKeyEvent(IIIIII)Z

    move-result p1

    return p1
.end method

.method private injectKeycode(IIII)Z
    .locals 7

    .line 349
    iget-boolean v0, p0, Lcom/android/helper/control/Controller;->keepDisplayPowerOff:Z

    if-eqz v0, :cond_1

    const/4 v0, 0x1

    if-ne p1, v0, :cond_1

    const/16 v0, 0x1a

    if-eq p2, v0, :cond_0

    const/16 v0, 0xe0

    if-ne p2, v0, :cond_1

    .line 351
    :cond_0
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    invoke-static {v0}, Lcom/android/helper/control/Controller;->scheduleDisplayPowerOff(I)V

    :cond_1
    const/4 v6, 0x0

    move-object v1, p0

    move v2, p1

    move v3, p2

    move v4, p3

    move v5, p4

    .line 353
    invoke-direct/range {v1 .. v6}, Lcom/android/helper/control/Controller;->injectKeyEvent(IIIII)Z

    move-result p1

    return p1
.end method

.method private injectScroll(Lcom/android/helper/device/Position;FFI)Z
    .locals 18

    move-object/from16 v0, p0

    .line 527
    invoke-static {}, Landroid/os/SystemClock;->uptimeMillis()J

    move-result-wide v3

    .line 529
    invoke-direct/range {p0 .. p1}, Lcom/android/helper/control/Controller;->getEventPointAndDisplayId(Lcom/android/helper/device/Position;)Landroid/util/Pair;

    move-result-object v1

    const/4 v2, 0x0

    if-nez v1, :cond_0

    return v2

    .line 534
    :cond_0
    iget-object v5, v1, Landroid/util/Pair;->first:Ljava/lang/Object;

    check-cast v5, Lcom/android/helper/device/Point;

    .line 535
    iget-object v1, v1, Landroid/util/Pair;->second:Ljava/lang/Object;

    check-cast v1, Ljava/lang/Integer;

    invoke-virtual {v1}, Ljava/lang/Integer;->intValue()I

    move-result v1

    .line 537
    iget-object v6, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    aget-object v6, v6, v2

    .line 538
    iput v2, v6, Landroid/view/MotionEvent$PointerProperties;->id:I

    .line 540
    iget-object v6, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    aget-object v6, v6, v2

    .line 541
    invoke-virtual {v5}, Lcom/android/helper/device/Point;->getX()I

    move-result v7

    int-to-float v7, v7

    iput v7, v6, Landroid/view/MotionEvent$PointerCoords;->x:F

    .line 542
    invoke-virtual {v5}, Lcom/android/helper/device/Point;->getY()I

    move-result v5

    int-to-float v5, v5

    iput v5, v6, Landroid/view/MotionEvent$PointerCoords;->y:F

    const/16 v5, 0xa

    move/from16 v7, p2

    .line 543
    invoke-virtual {v6, v5, v7}, Landroid/view/MotionEvent$PointerCoords;->setAxisValue(IF)V

    const/16 v5, 0x9

    move/from16 v7, p3

    .line 544
    invoke-virtual {v6, v5, v7}, Landroid/view/MotionEvent$PointerCoords;->setAxisValue(IF)V

    move v5, v1

    const/4 v6, 0x0

    .line 546
    iget-wide v1, v0, Lcom/android/helper/control/Controller;->lastTouchDown:J

    iget-object v7, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    iget-object v8, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    const/16 v15, 0x2002

    const/16 v16, 0x0

    move v9, v5

    const/16 v5, 0x8

    const/4 v10, 0x0

    const/4 v6, 0x1

    move v11, v9

    const/4 v9, 0x0

    move v12, v11

    const/high16 v11, 0x3f800000    # 1.0f

    move v13, v12

    const/high16 v12, 0x3f800000    # 1.0f

    move v14, v13

    const/4 v13, 0x0

    move/from16 v17, v14

    const/4 v14, 0x0

    move/from16 v10, p4

    move/from16 v0, v17

    invoke-static/range {v1 .. v16}, Landroid/view/MotionEvent;->obtain(JJII[Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;IIFFIIII)Landroid/view/MotionEvent;

    move-result-object v1

    const/4 v6, 0x0

    .line 548
    invoke-static {v1, v0, v6}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v0

    return v0
.end method

.method private injectText(Ljava/lang/String;)I
    .locals 7

    .line 375
    invoke-virtual {p1}, Ljava/lang/String;->toCharArray()[C

    move-result-object p1

    array-length v0, p1

    const/4 v1, 0x0

    const/4 v2, 0x0

    const/4 v3, 0x0

    :goto_0
    if-ge v2, v0, :cond_1

    aget-char v4, p1, v2

    .line 376
    invoke-direct {p0, v4}, Lcom/android/helper/control/Controller;->injectChar(C)Z

    move-result v5

    if-nez v5, :cond_0

    .line 377
    new-instance v5, Ljava/lang/StringBuilder;

    const-string v6, "Could not inject char u+"

    invoke-direct {v5, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {v4}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v4

    const/4 v6, 0x1

    new-array v6, v6, [Ljava/lang/Object;

    aput-object v4, v6, v1

    const-string v4, "%04x"

    invoke-static {v4, v6}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    goto :goto_1

    :cond_0
    add-int/lit8 v3, v3, 0x1

    :goto_1
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_1
    return v3
.end method

.method private injectTouch(IJLcom/android/helper/device/Position;FII)Z
    .locals 21

    move-object/from16 v0, p0

    move/from16 v1, p1

    move-wide/from16 v2, p2

    move/from16 v4, p6

    .line 416
    invoke-static {}, Landroid/os/SystemClock;->uptimeMillis()J

    move-result-wide v7

    move-object/from16 v5, p4

    .line 418
    invoke-direct {v0, v5}, Lcom/android/helper/control/Controller;->getEventPointAndDisplayId(Lcom/android/helper/device/Position;)Landroid/util/Pair;

    move-result-object v5

    const/4 v6, 0x0

    if-nez v5, :cond_0

    return v6

    .line 423
    :cond_0
    iget-object v9, v5, Landroid/util/Pair;->first:Ljava/lang/Object;

    check-cast v9, Lcom/android/helper/device/Point;

    .line 424
    iget-object v5, v5, Landroid/util/Pair;->second:Ljava/lang/Object;

    check-cast v5, Ljava/lang/Integer;

    invoke-virtual {v5}, Ljava/lang/Integer;->intValue()I

    move-result v5

    .line 426
    iget-object v10, v0, Lcom/android/helper/control/Controller;->pointersState:Lcom/android/helper/control/PointersState;

    invoke-virtual {v10, v2, v3}, Lcom/android/helper/control/PointersState;->getPointerIndex(J)I

    move-result v10

    const/4 v11, -0x1

    if-ne v10, v11, :cond_1

    .line 428
    const-string v1, "Too many pointers for touch event"

    invoke-static {v1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return v6

    .line 431
    :cond_1
    iget-object v11, v0, Lcom/android/helper/control/Controller;->pointersState:Lcom/android/helper/control/PointersState;

    invoke-virtual {v11, v10}, Lcom/android/helper/control/PointersState;->get(I)Lcom/android/helper/control/Pointer;

    move-result-object v11

    .line 432
    invoke-virtual {v11, v9}, Lcom/android/helper/control/Pointer;->setPoint(Lcom/android/helper/device/Point;)V

    move/from16 v9, p5

    .line 433
    invoke-virtual {v11, v9}, Lcom/android/helper/control/Pointer;->setPressure(F)V

    or-int v9, v4, p7

    and-int/lit8 v9, v9, -0x2

    const/4 v12, 0x1

    if-eqz v9, :cond_2

    const/4 v9, 0x1

    goto :goto_0

    :cond_2
    const/4 v9, 0x0

    :goto_0
    const-wide/16 v13, -0x1

    const/16 v15, 0x2002

    cmp-long v16, v2, v13

    if-nez v16, :cond_5

    const/4 v2, 0x7

    if-eq v1, v2, :cond_3

    if-eqz v9, :cond_5

    .line 439
    :cond_3
    iget-object v2, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    aget-object v2, v2, v10

    const/4 v3, 0x3

    iput v3, v2, Landroid/view/MotionEvent$PointerProperties;->toolType:I

    if-nez p7, :cond_4

    const/4 v2, 0x1

    goto :goto_1

    :cond_4
    const/4 v2, 0x0

    .line 441
    :goto_1
    invoke-virtual {v11, v2}, Lcom/android/helper/control/Pointer;->setUp(Z)V

    move/from16 v14, p7

    const/16 v2, 0x2002

    goto :goto_3

    .line 444
    :cond_5
    iget-object v2, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    aget-object v2, v2, v10

    iput v12, v2, Landroid/view/MotionEvent$PointerProperties;->toolType:I

    if-ne v1, v12, :cond_6

    const/4 v2, 0x1

    goto :goto_2

    :cond_6
    const/4 v2, 0x0

    .line 448
    :goto_2
    invoke-virtual {v11, v2}, Lcom/android/helper/control/Pointer;->setUp(Z)V

    const/16 v2, 0x1002

    const/4 v14, 0x0

    .line 451
    :goto_3
    iget-object v3, v0, Lcom/android/helper/control/Controller;->pointersState:Lcom/android/helper/control/PointersState;

    iget-object v9, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    iget-object v11, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    invoke-virtual {v3, v9, v11}, Lcom/android/helper/control/PointersState;->update([Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;)I

    move-result v3

    if-ne v3, v12, :cond_7

    if-nez v1, :cond_9

    .line 454
    iput-wide v7, v0, Lcom/android/helper/control/Controller;->lastTouchDown:J

    goto :goto_4

    :cond_7
    if-ne v1, v12, :cond_8

    shl-int/lit8 v1, v10, 0x8

    or-int/lit8 v1, v1, 0x6

    goto :goto_4

    :cond_8
    if-nez v1, :cond_9

    shl-int/lit8 v1, v10, 0x8

    or-int/lit8 v1, v1, 0x5

    .line 473
    :cond_9
    :goto_4
    sget v9, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v10, 0x17

    if-lt v9, v10, :cond_14

    if-ne v2, v15, :cond_14

    if-nez v1, :cond_e

    if-ne v4, v14, :cond_a

    move v1, v5

    const/4 v9, 0x0

    .line 477
    iget-wide v5, v0, Lcom/android/helper/control/Controller;->lastTouchDown:J

    iget-object v11, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    const/4 v10, 0x1

    iget-object v12, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    const/16 v18, 0x0

    const/16 v20, 0x0

    const/4 v13, 0x0

    const/4 v9, 0x0

    const/4 v15, 0x0

    const/4 v13, 0x0

    const/16 v16, 0x0

    const/high16 v15, 0x3f800000    # 1.0f

    const/16 v17, 0x0

    const/high16 v16, 0x3f800000    # 1.0f

    const/16 v19, 0x0

    const/16 v17, 0x0

    move/from16 v19, v2

    move v10, v3

    const/4 v3, 0x1

    move v2, v1

    const/4 v1, 0x0

    invoke-static/range {v5 .. v20}, Landroid/view/MotionEvent;->obtain(JJII[Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;IIFFIIII)Landroid/view/MotionEvent;

    move-result-object v5

    .line 479
    invoke-static {v5, v2, v1}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v5

    if-nez v5, :cond_b

    return v1

    :cond_a
    move/from16 v19, v2

    move v10, v3

    move v2, v5

    const/4 v1, 0x0

    const/4 v3, 0x1

    .line 485
    :cond_b
    iget-wide v5, v0, Lcom/android/helper/control/Controller;->lastTouchDown:J

    iget-object v11, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    iget-object v12, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    const/16 v18, 0x0

    const/16 v20, 0x0

    const/16 v9, 0xb

    const/4 v13, 0x0

    const/high16 v15, 0x3f800000    # 1.0f

    const/high16 v16, 0x3f800000    # 1.0f

    const/16 v17, 0x0

    invoke-static/range {v5 .. v20}, Landroid/view/MotionEvent;->obtain(JJII[Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;IIFFIIII)Landroid/view/MotionEvent;

    move-result-object v5

    .line 487
    invoke-static {v5, v4}, Lcom/android/helper/wrappers/InputManager;->setActionButton(Landroid/view/MotionEvent;I)Z

    move-result v4

    if-nez v4, :cond_c

    return v1

    .line 490
    :cond_c
    invoke-static {v5, v2, v1}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v2

    if-nez v2, :cond_d

    return v1

    :cond_d
    return v3

    :cond_e
    move/from16 v19, v2

    move v10, v3

    move v2, v5

    const/4 v3, 0x1

    const/4 v9, 0x0

    if-ne v1, v3, :cond_13

    .line 499
    iget-wide v5, v0, Lcom/android/helper/control/Controller;->lastTouchDown:J

    iget-object v11, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    iget-object v12, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    const/16 v18, 0x0

    const/16 v20, 0x0

    const/4 v13, 0x0

    const/16 v9, 0xc

    const/4 v15, 0x0

    const/4 v13, 0x0

    const/16 v16, 0x0

    const/high16 v15, 0x3f800000    # 1.0f

    const/16 v17, 0x0

    const/high16 v16, 0x3f800000    # 1.0f

    const/4 v1, 0x0

    const/16 v17, 0x0

    invoke-static/range {v5 .. v20}, Landroid/view/MotionEvent;->obtain(JJII[Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;IIFFIIII)Landroid/view/MotionEvent;

    move-result-object v5

    .line 501
    invoke-static {v5, v4}, Lcom/android/helper/wrappers/InputManager;->setActionButton(Landroid/view/MotionEvent;I)Z

    move-result v4

    if-nez v4, :cond_f

    return v1

    .line 504
    :cond_f
    invoke-static {v5, v2, v1}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v4

    if-nez v4, :cond_10

    return v1

    :cond_10
    if-nez v14, :cond_11

    move v4, v2

    const/4 v9, 0x0

    .line 510
    iget-wide v1, v0, Lcom/android/helper/control/Controller;->lastTouchDown:J

    move v5, v4

    move-wide v3, v7

    const/4 v6, 0x1

    iget-object v7, v0, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    iget-object v8, v0, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    move v6, v10

    move v10, v14

    const/4 v11, 0x1

    const/4 v14, 0x0

    const/16 v16, 0x0

    move v12, v5

    const/4 v5, 0x1

    const/4 v13, 0x0

    const/4 v9, 0x0

    const/4 v15, 0x1

    const/high16 v11, 0x3f800000    # 1.0f

    move/from16 v17, v12

    const/high16 v12, 0x3f800000    # 1.0f

    const/16 v18, 0x0

    const/4 v13, 0x0

    move/from16 v0, v17

    move/from16 v15, v19

    const/16 v17, 0x1

    invoke-static/range {v1 .. v16}, Landroid/view/MotionEvent;->obtain(JJII[Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;IIFFIIII)Landroid/view/MotionEvent;

    move-result-object v1

    const/4 v2, 0x0

    .line 512
    invoke-static {v1, v0, v2}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v0

    if-nez v0, :cond_12

    return v2

    :cond_11
    const/16 v17, 0x1

    :cond_12
    return v17

    :cond_13
    move v0, v2

    move-object/from16 v3, p0

    move v5, v1

    goto :goto_5

    :cond_14
    move/from16 v19, v2

    move v10, v3

    move v0, v5

    move-object/from16 v3, p0

    move v5, v1

    const/4 v9, 0x0

    .line 521
    :goto_5
    iget-wide v1, v3, Lcom/android/helper/control/Controller;->lastTouchDown:J

    move-wide v11, v7

    iget-object v7, v3, Lcom/android/helper/control/Controller;->pointerProperties:[Landroid/view/MotionEvent$PointerProperties;

    iget-object v8, v3, Lcom/android/helper/control/Controller;->pointerCoords:[Landroid/view/MotionEvent$PointerCoords;

    move v6, v10

    move v10, v14

    const/4 v14, 0x0

    const/16 v16, 0x0

    const/4 v13, 0x0

    const/4 v9, 0x0

    move-wide v3, v11

    const/high16 v11, 0x3f800000    # 1.0f

    const/high16 v12, 0x3f800000    # 1.0f

    const/4 v15, 0x0

    const/4 v13, 0x0

    move/from16 v15, v19

    invoke-static/range {v1 .. v16}, Landroid/view/MotionEvent;->obtain(JJII[Landroid/view/MotionEvent$PointerProperties;[Landroid/view/MotionEvent$PointerCoords;IIFFIIII)Landroid/view/MotionEvent;

    move-result-object v1

    const/4 v9, 0x0

    .line 523
    invoke-static {v1, v0, v9}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result v0

    return v0
.end method

.method static synthetic lambda$scheduleDisplayPowerOff$2(I)V
    .locals 1

    .line 556
    const-string v0, "Forcing display off"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    const/4 v0, 0x0

    .line 557
    invoke-static {p0, v0}, Lcom/android/helper/device/Device;->setDisplayPower(IZ)Z

    return-void
.end method

.method private openHardKeyboardSettings()V
    .locals 2

    .line 623
    new-instance v0, Landroid/content/Intent;

    const-string v1, "android.settings.HARD_KEYBOARD_SETTINGS"

    invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    .line 624
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v1

    invoke-virtual {v1, v0}, Lcom/android/helper/wrappers/ActivityManager;->startActivity(Landroid/content/Intent;)I

    return-void
.end method

.method private pressBackOrTurnScreenOn(I)Z
    .locals 6

    .line 562
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v1, -0x1

    if-eq v0, v1, :cond_3

    invoke-static {v0}, Lcom/android/helper/device/Device;->isScreenOn(I)Z

    move-result v0

    if-eqz v0, :cond_0

    goto :goto_0

    :cond_0
    if-eqz p1, :cond_1

    const/4 p1, 0x1

    return p1

    .line 573
    :cond_1
    iget-boolean p1, p0, Lcom/android/helper/control/Controller;->keepDisplayPowerOff:Z

    if-eqz p1, :cond_2

    .line 575
    iget p1, p0, Lcom/android/helper/control/Controller;->displayId:I

    invoke-static {p1}, Lcom/android/helper/control/Controller;->scheduleDisplayPowerOff(I)V

    :cond_2
    const/16 p1, 0x1a

    const/4 v0, 0x0

    .line 577
    invoke-direct {p0, p1, v0}, Lcom/android/helper/control/Controller;->pressReleaseKeycode(II)Z

    move-result p1

    return p1

    :cond_3
    :goto_0
    const/4 v4, 0x0

    const/4 v5, 0x0

    const/4 v2, 0x4

    const/4 v3, 0x0

    move-object v0, p0

    move v1, p1

    .line 563
    invoke-direct/range {v0 .. v5}, Lcom/android/helper/control/Controller;->injectKeyEvent(IIIII)Z

    move-result p1

    return p1
.end method

.method private pressReleaseKeycode(II)Z
    .locals 1

    .line 632
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getActionDisplayId()I

    move-result v0

    invoke-static {p1, v0, p2}, Lcom/android/helper/device/Device;->pressReleaseKeycode(III)Z

    move-result p1

    return p1
.end method

.method private resetVideo()V
    .locals 1

    .line 759
    iget-object v0, p0, Lcom/android/helper/control/Controller;->surfaceCapture:Lcom/android/helper/video/SurfaceCapture;

    if-eqz v0, :cond_0

    .line 760
    const-string v0, "KeyframeTrace video-reset-request"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 761
    iget-object v0, p0, Lcom/android/helper/control/Controller;->surfaceCapture:Lcom/android/helper/video/SurfaceCapture;

    invoke-virtual {v0}, Lcom/android/helper/video/SurfaceCapture;->requestInvalidate()V

    return-void

    .line 763
    :cond_0
    const-string v0, "KeyframeTrace video-reset-skipped: no surface capture"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void
.end method

.method private static scheduleDisplayPowerOff(I)V
    .locals 4

    .line 555
    sget-object v0, Lcom/android/helper/control/Controller;->EXECUTOR:Ljava/util/concurrent/ScheduledExecutorService;

    new-instance v1, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda3;

    invoke-direct {v1, p0}, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda3;-><init>(I)V

    const-wide/16 v2, 0xc8

    sget-object p0, Ljava/util/concurrent/TimeUnit;->MILLISECONDS:Ljava/util/concurrent/TimeUnit;

    invoke-interface {v0, v1, v2, v3, p0}, Ljava/util/concurrent/ScheduledExecutorService;->schedule(Ljava/lang/Runnable;JLjava/util/concurrent/TimeUnit;)Ljava/util/concurrent/ScheduledFuture;

    return-void
.end method

.method private setClipboard(Ljava/lang/String;ZJ)Z
    .locals 2

    .line 601
    iget-object v0, p0, Lcom/android/helper/control/Controller;->isSettingClipboard:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    .line 602
    invoke-static {p1}, Lcom/android/helper/device/Device;->setClipboardText(Ljava/lang/String;)Z

    move-result p1

    .line 603
    iget-object v0, p0, Lcom/android/helper/control/Controller;->isSettingClipboard:Ljava/util/concurrent/atomic/AtomicBoolean;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->set(Z)V

    if-eqz p1, :cond_0

    .line 605
    const-string v0, "Device clipboard set"

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    :cond_0
    if-eqz p2, :cond_1

    .line 609
    sget p2, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v0, 0x18

    if-lt p2, v0, :cond_1

    iget-boolean p2, p0, Lcom/android/helper/control/Controller;->supportsInputEvents:Z

    if-eqz p2, :cond_1

    const/16 p2, 0x117

    .line 610
    invoke-direct {p0, p2, v1}, Lcom/android/helper/control/Controller;->pressReleaseKeycode(II)Z

    :cond_1
    const-wide/16 v0, 0x0

    cmp-long p2, p3, v0

    if-eqz p2, :cond_2

    .line 615
    invoke-static {p3, p4}, Lcom/android/helper/control/DeviceMessage;->createAckClipboard(J)Lcom/android/helper/control/DeviceMessage;

    move-result-object p2

    .line 616
    iget-object p3, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {p3, p2}, Lcom/android/helper/control/DeviceMessageSender;->send(Lcom/android/helper/control/DeviceMessage;)V

    :cond_2
    return p1
.end method

.method private setDisplayPower(Z)V
    .locals 4

    .line 745
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v1, 0x0

    const/4 v2, -0x1

    if-eq v0, v2, :cond_0

    goto :goto_0

    :cond_0
    const/4 v0, 0x0

    .line 746
    :goto_0
    invoke-static {v0, p1}, Lcom/android/helper/device/Device;->setDisplayPower(IZ)Z

    move-result v0

    if-eqz v0, :cond_3

    .line 749
    iget v0, p0, Lcom/android/helper/control/Controller;->displayId:I

    const/4 v3, 0x1

    if-eq v0, v2, :cond_1

    if-nez p1, :cond_1

    const/4 v1, 0x1

    :cond_1
    iput-boolean v1, p0, Lcom/android/helper/control/Controller;->keepDisplayPowerOff:Z

    if-eqz p1, :cond_2

    .line 750
    const-string v0, "on"

    goto :goto_1

    :cond_2
    const-string v0, "off"

    :goto_1
    const-string v1, "Device display turned "

    invoke-virtual {v1, v0}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 751
    iget-object v0, p0, Lcom/android/helper/control/Controller;->cleanUp:Lcom/android/helper/CleanUp;

    if-eqz v0, :cond_3

    xor-int/2addr p1, v3

    .line 753
    invoke-virtual {v0, p1}, Lcom/android/helper/CleanUp;->setRestoreDisplayPower(Z)V

    :cond_3
    return-void
.end method

.method private startApp(Ljava/lang/String;)V
    .locals 5

    .line 661
    const-string v0, "+"

    invoke-virtual {p1, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    const/4 v1, 0x1

    if-eqz v0, :cond_0

    .line 663
    invoke-virtual {p1, v1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p1

    .line 667
    :cond_0
    const-string v2, "?"

    invoke-virtual {p1, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v2

    .line 668
    const-string v3, "\""

    if-eqz v2, :cond_3

    .line 669
    invoke-virtual {p1, v1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p1

    .line 671
    const-string v2, "Processing Android apps... (this may take some time)"

    invoke-static {v2}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 672
    invoke-static {p1}, Lcom/android/helper/device/Device;->findByName(Ljava/lang/String;)Ljava/util/List;

    move-result-object v2

    .line 673
    invoke-interface {v2}, Ljava/util/List;->isEmpty()Z

    move-result v4

    if-eqz v4, :cond_1

    .line 674
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "No app found for name \""

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    .line 678
    :cond_1
    invoke-interface {v2}, Ljava/util/List;->size()I

    move-result v4

    if-le v4, v1, :cond_2

    .line 679
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "No unique app found for name \""

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p1, "\":"

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    .line 680
    invoke-static {p1, v2}, Lcom/android/helper/util/LogUtils;->buildAppListMessage(Ljava/lang/String;Ljava/util/List;)Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    :cond_2
    const/4 v1, 0x0

    .line 684
    invoke-interface {v2, v1}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lcom/android/helper/device/DeviceApp;

    goto :goto_0

    .line 686
    :cond_3
    invoke-static {p1}, Lcom/android/helper/device/Device;->findByPackageName(Ljava/lang/String;)Lcom/android/helper/device/DeviceApp;

    move-result-object v1

    if-nez v1, :cond_4

    .line 688
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "No app found for package \""

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    .line 693
    :cond_4
    :goto_0
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->getStartAppDisplayId()I

    move-result v2

    const/4 v4, -0x1

    if-ne v2, v4, :cond_5

    .line 695
    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "No known display id to start app \""

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return-void

    .line 699
    :cond_5
    new-instance p1, Ljava/lang/StringBuilder;

    const-string v3, "Starting app \""

    invoke-direct {p1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Lcom/android/helper/device/DeviceApp;->getName()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v3, "\" ["

    invoke-virtual {p1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Lcom/android/helper/device/DeviceApp;->getPackageName()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {p1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v3, "] on display "

    invoke-virtual {p1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v3, "..."

    invoke-virtual {p1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 700
    invoke-virtual {v1}, Lcom/android/helper/device/DeviceApp;->getPackageName()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1, v2, v0}, Lcom/android/helper/device/Device;->startApp(Ljava/lang/String;IZ)V

    return-void
.end method

.method private startAppAsync(Ljava/lang/String;)V
    .locals 2

    .line 652
    iget-object v0, p0, Lcom/android/helper/control/Controller;->startAppExecutor:Ljava/util/concurrent/ExecutorService;

    if-nez v0, :cond_0

    .line 653
    invoke-static {}, Ljava/util/concurrent/Executors;->newSingleThreadExecutor()Ljava/util/concurrent/ExecutorService;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/control/Controller;->startAppExecutor:Ljava/util/concurrent/ExecutorService;

    .line 657
    :cond_0
    iget-object v0, p0, Lcom/android/helper/control/Controller;->startAppExecutor:Ljava/util/concurrent/ExecutorService;

    new-instance v1, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda1;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda1;-><init>(Lcom/android/helper/control/Controller;Ljava/lang/String;)V

    invoke-interface {v0, v1}, Ljava/util/concurrent/ExecutorService;->submit(Ljava/lang/Runnable;)Ljava/util/concurrent/Future;

    return-void
.end method

.method private waitDisplayData(J)Lcom/android/helper/control/Controller$DisplayData;
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 724
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    add-long/2addr v0, p1

    .line 726
    iget-object p1, p0, Lcom/android/helper/control/Controller;->displayDataAvailable:Ljava/lang/Object;

    monitor-enter p1

    .line 727
    :try_start_0
    iget-object p2, p0, Lcom/android/helper/control/Controller;->displayData:Ljava/util/concurrent/atomic/AtomicReference;

    invoke-virtual {p2}, Ljava/util/concurrent/atomic/AtomicReference;->get()Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Lcom/android/helper/control/Controller$DisplayData;

    :goto_0
    if-nez p2, :cond_2

    .line 729
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v2

    sub-long v2, v0, v2

    const-wide/16 v4, 0x0

    cmp-long p2, v2, v4

    if-gez p2, :cond_0

    const/4 p2, 0x0

    .line 731
    monitor-exit p1

    return-object p2

    :cond_0
    if-lez p2, :cond_1

    .line 734
    iget-object p2, p0, Lcom/android/helper/control/Controller;->displayDataAvailable:Ljava/lang/Object;

    invoke-virtual {p2, v2, v3}, Ljava/lang/Object;->wait(J)V

    .line 736
    :cond_1
    iget-object p2, p0, Lcom/android/helper/control/Controller;->displayData:Ljava/util/concurrent/atomic/AtomicReference;

    invoke-virtual {p2}, Ljava/util/concurrent/atomic/AtomicReference;->get()Ljava/lang/Object;

    move-result-object p2

    check-cast p2, Lcom/android/helper/control/Controller$DisplayData;

    goto :goto_0

    .line 739
    :cond_2
    monitor-exit p1

    return-object p2

    :catchall_0
    move-exception p2

    .line 740
    monitor-exit p1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw p2
.end method


# virtual methods
.method public join()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/InterruptedException;
        }
    .end annotation

    .line 252
    iget-object v0, p0, Lcom/android/helper/control/Controller;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 253
    invoke-virtual {v0}, Ljava/lang/Thread;->join()V

    .line 255
    :cond_0
    iget-object v0, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {v0}, Lcom/android/helper/control/DeviceMessageSender;->join()V

    return-void
.end method

.method synthetic lambda$new$0$com-android-helper-control-Controller()V
    .locals 2

    .line 123
    iget-object v0, p0, Lcom/android/helper/control/Controller;->isSettingClipboard:Ljava/util/concurrent/atomic/AtomicBoolean;

    invoke-virtual {v0}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z

    move-result v0

    if-eqz v0, :cond_0

    goto :goto_0

    .line 127
    :cond_0
    invoke-static {}, Lcom/android/helper/device/Device;->getClipboardText()Ljava/lang/String;

    move-result-object v0

    if-eqz v0, :cond_1

    .line 129
    invoke-static {v0}, Lcom/android/helper/control/DeviceMessage;->createClipboard(Ljava/lang/String;)Lcom/android/helper/control/DeviceMessage;

    move-result-object v0

    .line 130
    iget-object v1, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {v1, v0}, Lcom/android/helper/control/DeviceMessageSender;->send(Lcom/android/helper/control/DeviceMessage;)V

    :cond_1
    :goto_0
    return-void
.end method

.method synthetic lambda$start$1$com-android-helper-control-Controller(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 4

    .line 227
    const-string v0, "Controller stopped"

    const/4 v1, 0x1

    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/control/Controller;->control()V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 231
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 232
    iget-object v0, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    if-eqz v0, :cond_0

    .line 233
    invoke-virtual {v0}, Lcom/android/helper/control/UhidManager;->closeAll()V

    .line 235
    :cond_0
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    return-void

    :catchall_0
    move-exception v2

    goto :goto_0

    :catch_0
    move-exception v2

    .line 229
    :try_start_1
    const-string v3, "Controller error"

    invoke-static {v3, v2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    .line 231
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 232
    iget-object v0, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    if-eqz v0, :cond_1

    .line 233
    iget-object v0, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    invoke-virtual {v0}, Lcom/android/helper/control/UhidManager;->closeAll()V

    .line 235
    :cond_1
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    return-void

    .line 231
    :goto_0
    invoke-static {v0}, Lcom/android/helper/util/Ln;->d(Ljava/lang/String;)V

    .line 232
    iget-object v0, p0, Lcom/android/helper/control/Controller;->uhidManager:Lcom/android/helper/control/UhidManager;

    if-eqz v0, :cond_2

    .line 233
    invoke-virtual {v0}, Lcom/android/helper/control/UhidManager;->closeAll()V

    .line 235
    :cond_2
    invoke-interface {p1, v1}, Lcom/android/helper/AsyncProcessor$TerminationListener;->onTerminated(Z)V

    .line 236
    throw v2
.end method

.method synthetic lambda$startAppAsync$3$com-android-helper-control-Controller(Ljava/lang/String;)V
    .locals 0

    .line 657
    invoke-direct {p0, p1}, Lcom/android/helper/control/Controller;->startApp(Ljava/lang/String;)V

    return-void
.end method

.method public onNewVirtualDisplay(ILcom/android/helper/control/PositionMapper;)V
    .locals 2

    .line 141
    new-instance v0, Lcom/android/helper/control/Controller$DisplayData;

    const/4 v1, 0x0

    invoke-direct {v0, p1, p2, v1}, Lcom/android/helper/control/Controller$DisplayData;-><init>(ILcom/android/helper/control/PositionMapper;Lcom/android/helper/control/Controller$1;)V

    .line 142
    iget-object p1, p0, Lcom/android/helper/control/Controller;->displayData:Ljava/util/concurrent/atomic/AtomicReference;

    invoke-virtual {p1, v0}, Ljava/util/concurrent/atomic/AtomicReference;->getAndSet(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Lcom/android/helper/control/Controller$DisplayData;

    if-nez p1, :cond_0

    .line 145
    iget-object p1, p0, Lcom/android/helper/control/Controller;->displayDataAvailable:Ljava/lang/Object;

    monitor-enter p1

    .line 146
    :try_start_0
    iget-object p2, p0, Lcom/android/helper/control/Controller;->displayDataAvailable:Ljava/lang/Object;

    invoke-virtual {p2}, Ljava/lang/Object;->notify()V

    .line 147
    monitor-exit p1

    return-void

    :catchall_0
    move-exception p2

    monitor-exit p1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw p2

    :cond_0
    return-void
.end method

.method public setSurfaceCapture(Lcom/android/helper/video/SurfaceCapture;)V
    .locals 0

    .line 152
    iput-object p1, p0, Lcom/android/helper/control/Controller;->surfaceCapture:Lcom/android/helper/video/SurfaceCapture;

    return-void
.end method

.method public start(Lcom/android/helper/AsyncProcessor$TerminationListener;)V
    .locals 2

    .line 225
    new-instance v0, Ljava/lang/Thread;

    new-instance v1, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda2;

    invoke-direct {v1, p0, p1}, Lcom/android/helper/control/Controller$$ExternalSyntheticLambda2;-><init>(Lcom/android/helper/control/Controller;Lcom/android/helper/AsyncProcessor$TerminationListener;)V

    const-string p1, "control-recv"

    invoke-direct {v0, v1, p1}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;Ljava/lang/String;)V

    iput-object v0, p0, Lcom/android/helper/control/Controller;->thread:Ljava/lang/Thread;

    .line 238
    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    .line 239
    iget-object p1, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {p1}, Lcom/android/helper/control/DeviceMessageSender;->start()V

    return-void
.end method

.method public stop()V
    .locals 1

    .line 244
    iget-object v0, p0, Lcom/android/helper/control/Controller;->thread:Ljava/lang/Thread;

    if-eqz v0, :cond_0

    .line 245
    invoke-virtual {v0}, Ljava/lang/Thread;->interrupt()V

    .line 247
    :cond_0
    iget-object v0, p0, Lcom/android/helper/control/Controller;->sender:Lcom/android/helper/control/DeviceMessageSender;

    invoke-virtual {v0}, Lcom/android/helper/control/DeviceMessageSender;->stop()V

    return-void
.end method
