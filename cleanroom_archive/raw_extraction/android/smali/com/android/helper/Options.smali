.class public Lcom/android/helper/Options;
.super Ljava/lang/Object;
.source "Options.java"


# static fields
.field static final synthetic $assertionsDisabled:Z


# instance fields
.field private angle:F

.field private audio:Z

.field private audioBitRate:I

.field private audioCodec:Lcom/android/helper/audio/AudioCodec;

.field private audioCodecOptions:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;"
        }
    .end annotation
.end field

.field private audioDup:Z

.field private audioEncoder:Ljava/lang/String;

.field private audioSocket:Ljava/lang/String;

.field private audioSource:Lcom/android/helper/audio/AudioSource;

.field private cameraAspectRatio:Lcom/android/helper/video/CameraAspectRatio;

.field private cameraFacing:Lcom/android/helper/video/CameraFacing;

.field private cameraFps:I

.field private cameraHighSpeed:Z

.field private cameraId:Ljava/lang/String;

.field private cameraSize:Lcom/android/helper/device/Size;

.field private cameraZoom:F

.field private captureOrientation:Lcom/android/helper/device/Orientation;

.field private captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

.field private cleanup:Z

.field private clipboardAutosync:Z

.field private control:Z

.field private controlSocket:Ljava/lang/String;

.field private crop:Landroid/graphics/Rect;

.field private displayId:I

.field private displayImePolicy:I

.field private downsizeOnError:Z

.field private listApps:Z

.field private listCameraSizes:Z

.field private listCameras:Z

.field private listDisplays:Z

.field private listEncoders:Z

.field private logLevel:Lcom/android/helper/util/Ln$Level;

.field private maxFps:F

.field private maxSize:I

.field private newDisplay:Lcom/android/helper/device/NewDisplay;

.field private port:I

.field private powerOffScreenOnClose:Z

.field private powerOn:Z

.field private scid:I

.field private screenOffTimeout:I

.field private sendCodecMeta:Z

.field private sendDeviceMeta:Z

.field private sendDummyByte:Z

.field private sendFrameMeta:Z

.field private showTouches:Z

.field private stayAwake:Z

.field private touchSocket:Ljava/lang/String;

.field private tunnelForward:Z

.field private vdDestroyContent:Z

.field private vdSystemDecorations:Z

.field private video:Z

.field private videoBitRate:I

.field private videoCodec:Lcom/android/helper/video/VideoCodec;

.field private videoCodecOptions:Ljava/util/List;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;"
        }
    .end annotation
.end field

.field private videoEncoder:Ljava/lang/String;

.field private videoSocket:Ljava/lang/String;

.field private videoSource:Lcom/android/helper/video/VideoSource;


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>()V
    .locals 3

    .line 23
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 25
    sget-object v0, Lcom/android/helper/util/Ln$Level;->DEBUG:Lcom/android/helper/util/Ln$Level;

    iput-object v0, p0, Lcom/android/helper/Options;->logLevel:Lcom/android/helper/util/Ln$Level;

    const/4 v0, -0x1

    .line 26
    iput v0, p0, Lcom/android/helper/Options;->scid:I

    const/4 v1, 0x1

    .line 27
    iput-boolean v1, p0, Lcom/android/helper/Options;->video:Z

    .line 28
    iput-boolean v1, p0, Lcom/android/helper/Options;->audio:Z

    .line 30
    sget-object v2, Lcom/android/helper/video/VideoCodec;->H264:Lcom/android/helper/video/VideoCodec;

    iput-object v2, p0, Lcom/android/helper/Options;->videoCodec:Lcom/android/helper/video/VideoCodec;

    .line 31
    sget-object v2, Lcom/android/helper/audio/AudioCodec;->OPUS:Lcom/android/helper/audio/AudioCodec;

    iput-object v2, p0, Lcom/android/helper/Options;->audioCodec:Lcom/android/helper/audio/AudioCodec;

    .line 32
    sget-object v2, Lcom/android/helper/video/VideoSource;->DISPLAY:Lcom/android/helper/video/VideoSource;

    iput-object v2, p0, Lcom/android/helper/Options;->videoSource:Lcom/android/helper/video/VideoSource;

    .line 33
    sget-object v2, Lcom/android/helper/audio/AudioSource;->OUTPUT:Lcom/android/helper/audio/AudioSource;

    iput-object v2, p0, Lcom/android/helper/Options;->audioSource:Lcom/android/helper/audio/AudioSource;

    const v2, 0x7a1200

    .line 35
    iput v2, p0, Lcom/android/helper/Options;->videoBitRate:I

    const v2, 0x1f400

    .line 36
    iput v2, p0, Lcom/android/helper/Options;->audioBitRate:I

    .line 41
    iput-boolean v1, p0, Lcom/android/helper/Options;->control:Z

    const/4 v2, 0x0

    .line 49
    iput v2, p0, Lcom/android/helper/Options;->cameraZoom:F

    .line 52
    iput v0, p0, Lcom/android/helper/Options;->screenOffTimeout:I

    .line 53
    iput v0, p0, Lcom/android/helper/Options;->displayImePolicy:I

    .line 60
    iput-boolean v1, p0, Lcom/android/helper/Options;->clipboardAutosync:Z

    .line 61
    iput-boolean v1, p0, Lcom/android/helper/Options;->downsizeOnError:Z

    .line 62
    iput-boolean v1, p0, Lcom/android/helper/Options;->cleanup:Z

    .line 63
    iput-boolean v1, p0, Lcom/android/helper/Options;->powerOn:Z

    .line 66
    iput-boolean v1, p0, Lcom/android/helper/Options;->vdDestroyContent:Z

    .line 67
    iput-boolean v1, p0, Lcom/android/helper/Options;->vdSystemDecorations:Z

    .line 69
    sget-object v0, Lcom/android/helper/device/Orientation$Lock;->Unlocked:Lcom/android/helper/device/Orientation$Lock;

    iput-object v0, p0, Lcom/android/helper/Options;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    .line 70
    sget-object v0, Lcom/android/helper/device/Orientation;->Orient0:Lcom/android/helper/device/Orientation;

    iput-object v0, p0, Lcom/android/helper/Options;->captureOrientation:Lcom/android/helper/device/Orientation;

    .line 79
    iput-boolean v1, p0, Lcom/android/helper/Options;->sendDeviceMeta:Z

    .line 80
    iput-boolean v1, p0, Lcom/android/helper/Options;->sendFrameMeta:Z

    .line 81
    iput-boolean v1, p0, Lcom/android/helper/Options;->sendDummyByte:Z

    .line 82
    iput-boolean v1, p0, Lcom/android/helper/Options;->sendCodecMeta:Z

    const/4 v0, 0x0

    .line 83
    iput v0, p0, Lcom/android/helper/Options;->port:I

    .line 84
    const-string v0, "cloudphone_video"

    iput-object v0, p0, Lcom/android/helper/Options;->videoSocket:Ljava/lang/String;

    .line 85
    const-string v0, "cloudphone_audio"

    iput-object v0, p0, Lcom/android/helper/Options;->audioSocket:Ljava/lang/String;

    .line 86
    const-string v0, "cloudphone_control"

    iput-object v0, p0, Lcom/android/helper/Options;->controlSocket:Ljava/lang/String;

    .line 87
    const-string v0, "cloudphone_touch"

    iput-object v0, p0, Lcom/android/helper/Options;->touchSocket:Ljava/lang/String;

    return-void
.end method

.method public static varargs parse([Ljava/lang/String;)Lcom/android/helper/Options;
    .locals 7

    .line 323
    new-instance v0, Lcom/android/helper/Options;

    invoke-direct {v0}, Lcom/android/helper/Options;-><init>()V

    .line 326
    const-string v1, "CP_STEAL_MODE"

    invoke-static {v1}, Ljava/lang/System;->getenv(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, -0x1

    if-nez v1, :cond_4

    array-length v1, p0

    if-nez v1, :cond_0

    goto :goto_1

    .line 331
    :cond_0
    array-length v1, p0

    const/4 v3, 0x1

    if-lt v1, v3, :cond_3

    const/4 v1, 0x0

    .line 335
    aget-object v4, p0, v1

    .line 336
    const-string v5, "3.3.4-2af7ccc1"

    invoke-virtual {v4, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_2

    .line 341
    :goto_0
    array-length v4, p0

    if-ge v3, v4, :cond_5

    .line 342
    aget-object v4, p0, v3

    const/16 v5, 0x3d

    .line 343
    invoke-virtual {v4, v5}, Ljava/lang/String;->indexOf(I)I

    move-result v5

    if-eq v5, v2, :cond_1

    .line 347
    invoke-virtual {v4, v1, v5}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v6

    add-int/lit8 v5, v5, 0x1

    .line 348
    invoke-virtual {v4, v5}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v4

    .line 349
    invoke-virtual {v0, v6, v4}, Lcom/android/helper/Options;->setOption(Ljava/lang/String;Ljava/lang/String;)V

    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    .line 345
    :cond_1
    new-instance p0, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Invalid key=value pair: \""

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "\""

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 337
    :cond_2
    new-instance p0, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "The server version (3.3.4-2af7ccc1) does not match the client ("

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, ")"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 332
    :cond_3
    new-instance p0, Ljava/lang/IllegalArgumentException;

    const-string v0, "Missing client version"

    invoke-direct {p0, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 352
    :cond_4
    :goto_1
    invoke-direct {v0}, Lcom/android/helper/Options;->readFromEnvironment()V

    .line 355
    :cond_5
    iget-object p0, v0, Lcom/android/helper/Options;->newDisplay:Lcom/android/helper/device/NewDisplay;

    if-eqz p0, :cond_6

    .line 357
    iput v2, v0, Lcom/android/helper/Options;->displayId:I

    :cond_6
    return-object v0
.end method

.method private static parseCameraAspectRatio(Ljava/lang/String;)Lcom/android/helper/video/CameraAspectRatio;
    .locals 3

    .line 655
    const-string v0, "sensor"

    invoke-virtual {v0, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 656
    invoke-static {}, Lcom/android/helper/video/CameraAspectRatio;->sensorAspectRatio()Lcom/android/helper/video/CameraAspectRatio;

    move-result-object p0

    return-object p0

    .line 659
    :cond_0
    const-string v0, ":"

    invoke-virtual {p0, v0}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object p0

    .line 660
    array-length v0, p0

    const/4 v1, 0x2

    const/4 v2, 0x0

    if-ne v0, v1, :cond_1

    .line 661
    aget-object v0, p0, v2

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    const/4 v1, 0x1

    .line 662
    aget-object p0, p0, v1

    invoke-static {p0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p0

    .line 663
    invoke-static {v0, p0}, Lcom/android/helper/video/CameraAspectRatio;->fromFraction(II)Lcom/android/helper/video/CameraAspectRatio;

    move-result-object p0

    return-object p0

    .line 666
    :cond_1
    aget-object p0, p0, v2

    invoke-static {p0}, Ljava/lang/Float;->parseFloat(Ljava/lang/String;)F

    move-result p0

    .line 667
    invoke-static {p0}, Lcom/android/helper/video/CameraAspectRatio;->fromFloat(F)Lcom/android/helper/video/CameraAspectRatio;

    move-result-object p0

    return-object p0
.end method

.method private static parseCaptureOrientation(Ljava/lang/String;)Landroid/util/Pair;
    .locals 2
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            ")",
            "Landroid/util/Pair<",
            "Lcom/android/helper/device/Orientation$Lock;",
            "Lcom/android/helper/device/Orientation;",
            ">;"
        }
    .end annotation

    .line 711
    invoke-virtual {p0}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_2

    const/4 v0, 0x0

    .line 716
    invoke-virtual {p0, v0}, Ljava/lang/String;->charAt(I)C

    move-result v0

    const/16 v1, 0x40

    if-ne v0, v1, :cond_1

    const/4 v0, 0x1

    .line 718
    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object p0

    .line 719
    invoke-virtual {p0}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 721
    sget-object p0, Lcom/android/helper/device/Orientation$Lock;->LockedInitial:Lcom/android/helper/device/Orientation$Lock;

    sget-object v0, Lcom/android/helper/device/Orientation;->Orient0:Lcom/android/helper/device/Orientation;

    invoke-static {p0, v0}, Landroid/util/Pair;->create(Ljava/lang/Object;Ljava/lang/Object;)Landroid/util/Pair;

    move-result-object p0

    return-object p0

    .line 723
    :cond_0
    sget-object v0, Lcom/android/helper/device/Orientation$Lock;->LockedValue:Lcom/android/helper/device/Orientation$Lock;

    goto :goto_0

    .line 725
    :cond_1
    sget-object v0, Lcom/android/helper/device/Orientation$Lock;->Unlocked:Lcom/android/helper/device/Orientation$Lock;

    .line 728
    :goto_0
    invoke-static {p0}, Lcom/android/helper/device/Orientation;->getByName(Ljava/lang/String;)Lcom/android/helper/device/Orientation;

    move-result-object p0

    invoke-static {v0, p0}, Landroid/util/Pair;->create(Ljava/lang/Object;Ljava/lang/Object;)Landroid/util/Pair;

    move-result-object p0

    return-object p0

    .line 712
    :cond_2
    new-instance p0, Ljava/lang/IllegalArgumentException;

    const-string v0, "Empty capture orientation string"

    invoke-direct {p0, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method private static parseCrop(Ljava/lang/String;)Landroid/graphics/Rect;
    .locals 5

    .line 623
    const-string v0, ":"

    invoke-virtual {p0, v0}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v1

    .line 624
    array-length v2, v1

    const/4 v3, 0x4

    if-ne v2, v3, :cond_2

    const/4 p0, 0x0

    .line 627
    aget-object p0, v1, p0

    invoke-static {p0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p0

    const/4 v2, 0x1

    .line 628
    aget-object v2, v1, v2

    invoke-static {v2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v2

    if-lez p0, :cond_1

    if-lez v2, :cond_1

    const/4 v3, 0x2

    .line 632
    aget-object v3, v1, v3

    invoke-static {v3}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v3

    const/4 v4, 0x3

    .line 633
    aget-object v1, v1, v4

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    if-ltz v3, :cond_0

    if-ltz v1, :cond_0

    .line 637
    new-instance v0, Landroid/graphics/Rect;

    add-int/2addr p0, v3

    add-int/2addr v2, v1

    invoke-direct {v0, v3, v1, p0, v2}, Landroid/graphics/Rect;-><init>(IIII)V

    return-object v0

    .line 635
    :cond_0
    new-instance p0, Ljava/lang/IllegalArgumentException;

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v4, "Invalid crop offset: "

    invoke-direct {v2, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0

    .line 630
    :cond_1
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v3, "Invalid crop size: "

    invoke-direct {v1, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string p0, "x"

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 625
    :cond_2
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Crop must contains 4 values separated by colons: \""

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, "\""

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private static parseDisplayImePolicy(Ljava/lang/String;)I
    .locals 5

    .line 732
    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    move-result v0

    const/4 v1, 0x2

    const/4 v2, 0x1

    const/4 v3, 0x0

    const/4 v4, -0x1

    sparse-switch v0, :sswitch_data_0

    goto :goto_0

    :sswitch_0
    const-string v0, "fallback"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v4, 0x2

    goto :goto_0

    :sswitch_1
    const-string v0, "local"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    goto :goto_0

    :cond_1
    const/4 v4, 0x1

    goto :goto_0

    :sswitch_2
    const-string v0, "hide"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2

    goto :goto_0

    :cond_2
    const/4 v4, 0x0

    :goto_0
    packed-switch v4, :pswitch_data_0

    .line 740
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid display IME policy: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0

    :pswitch_0
    return v2

    :pswitch_1
    return v3

    :pswitch_2
    return v1

    nop

    :sswitch_data_0
    .sparse-switch
        0x30dd42 -> :sswitch_2
        0x625df6b -> :sswitch_1
        0x2d5fa6e2 -> :sswitch_0
    .end sparse-switch

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_2
        :pswitch_1
        :pswitch_0
    .end packed-switch
.end method

.method private static parseFloat(Ljava/lang/String;Ljava/lang/String;)F
    .locals 3

    .line 672
    :try_start_0
    invoke-static {p1}, Ljava/lang/Float;->parseFloat(Ljava/lang/String;)F

    move-result p0
    :try_end_0
    .catch Ljava/lang/NumberFormatException; {:try_start_0 .. :try_end_0} :catch_0

    return p0

    .line 674
    :catch_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid float value for "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, ": \""

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, "\""

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private static parseNewDisplay(Ljava/lang/String;)Lcom/android/helper/device/NewDisplay;
    .locals 4

    .line 684
    invoke-virtual {p0}, Ljava/lang/String;->isEmpty()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 685
    new-instance p0, Lcom/android/helper/device/NewDisplay;

    invoke-direct {p0}, Lcom/android/helper/device/NewDisplay;-><init>()V

    return-object p0

    .line 688
    :cond_0
    const-string v0, "/"

    invoke-virtual {p0, v0}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object p0

    const/4 v0, 0x0

    .line 691
    aget-object v1, p0, v0

    invoke-virtual {v1}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    if-nez v1, :cond_1

    .line 692
    aget-object v1, p0, v0

    invoke-static {v1}, Lcom/android/helper/Options;->parseSize(Ljava/lang/String;)Lcom/android/helper/device/Size;

    move-result-object v1

    goto :goto_0

    :cond_1
    const/4 v1, 0x0

    .line 698
    :goto_0
    array-length v2, p0

    const/4 v3, 0x2

    if-lt v2, v3, :cond_3

    const/4 v0, 0x1

    .line 699
    aget-object v2, p0, v0

    invoke-static {v2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v2

    if-lez v2, :cond_2

    move v0, v2

    goto :goto_1

    .line 701
    :cond_2
    new-instance v1, Ljava/lang/IllegalArgumentException;

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Invalid non-positive dpi: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    aget-object p0, p0, v0

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v1, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v1

    .line 707
    :cond_3
    :goto_1
    new-instance p0, Lcom/android/helper/device/NewDisplay;

    invoke-direct {p0, v1, v0}, Lcom/android/helper/device/NewDisplay;-><init>(Lcom/android/helper/device/Size;I)V

    return-object p0
.end method

.method private static parseSize(Ljava/lang/String;)Lcom/android/helper/device/Size;
    .locals 4

    .line 642
    const-string v0, "x"

    invoke-virtual {p0, v0}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    .line 643
    array-length v1, v0

    const/4 v2, 0x2

    const-string v3, "\""

    if-ne v1, v2, :cond_1

    const/4 v1, 0x0

    .line 646
    aget-object v1, v0, v1

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v1

    const/4 v2, 0x1

    .line 647
    aget-object v0, v0, v2

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    if-lez v1, :cond_0

    if-lez v0, :cond_0

    .line 651
    new-instance p0, Lcom/android/helper/device/Size;

    invoke-direct {p0, v1, v0}, Lcom/android/helper/device/Size;-><init>(II)V

    return-object p0

    .line 649
    :cond_0
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid non-positive size dimension: \""

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 644
    :cond_1
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid size format (expected <width>x<height>): \""

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0
.end method

.method private readFromEnvironment()V
    .locals 59

    .line 594
    const-string v57, "control_socket"

    const-string v58, "touch_socket"

    const-string v2, "scid"

    const-string v3, "log_level"

    const-string v4, "video"

    const-string v5, "audio"

    const-string v6, "video_codec"

    const-string v7, "audio_codec"

    const-string v8, "video_source"

    const-string v9, "audio_source"

    const-string v10, "audio_dup"

    const-string v11, "max_size"

    const-string v12, "video_bit_rate"

    const-string v13, "audio_bit_rate"

    const-string v14, "max_fps"

    const-string v15, "angle"

    const-string v16, "tunnel_forward"

    const-string v17, "crop"

    const-string v18, "control"

    const-string v19, "display_id"

    const-string v20, "show_touches"

    const-string v21, "stay_awake"

    const-string v22, "screen_off_timeout"

    const-string v23, "video_codec_options"

    const-string v24, "audio_codec_options"

    const-string v25, "video_encoder"

    const-string v26, "audio_encoder"

    const-string v27, "power_off_on_close"

    const-string v28, "clipboard_autosync"

    const-string v29, "downsize_on_error"

    const-string v30, "cleanup"

    const-string v31, "power_on"

    const-string v32, "list_encoders"

    const-string v33, "list_displays"

    const-string v34, "list_cameras"

    const-string v35, "list_camera_sizes"

    const-string v36, "list_apps"

    const-string v37, "camera_id"

    const-string v38, "camera_size"

    const-string v39, "camera_facing"

    const-string v40, "camera_ar"

    const-string v41, "camera_fps"

    const-string v42, "camera_high_speed"

    const-string v43, "camera_zoom"

    const-string v44, "new_display"

    const-string v45, "vd_destroy_content"

    const-string v46, "vd_system_decorations"

    const-string v47, "capture_orientation"

    const-string v48, "display_ime_policy"

    const-string v49, "send_device_meta"

    const-string v50, "send_frame_meta"

    const-string v51, "send_dummy_byte"

    const-string v52, "send_codec_meta"

    const-string v53, "raw_stream"

    const-string v54, "port"

    const-string v55, "video_socket"

    const-string v56, "audio_socket"

    filled-new-array/range {v2 .. v58}, [Ljava/lang/String;

    move-result-object v1

    const/4 v0, 0x0

    const/4 v2, 0x0

    :goto_0
    const/16 v0, 0x39

    if-ge v2, v0, :cond_1

    .line 608
    aget-object v0, v1, v2

    .line 609
    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "CP_"

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    sget-object v4, Ljava/util/Locale;->ENGLISH:Ljava/util/Locale;

    invoke-virtual {v0, v4}, Ljava/lang/String;->toUpperCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    .line 610
    invoke-static {v3}, Ljava/lang/System;->getenv(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    if-eqz v4, :cond_0

    move-object/from16 v5, p0

    .line 613
    :try_start_0
    invoke-virtual {v5, v0, v4}, Lcom/android/helper/Options;->setOption(Ljava/lang/String;Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_1

    :catch_0
    move-exception v0

    .line 615
    new-instance v6, Ljava/lang/StringBuilder;

    const-string v7, "Failed to parse env variable "

    invoke-direct {v6, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v6, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v3, "="

    invoke-virtual {v6, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v3, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    goto :goto_1

    :cond_0
    move-object/from16 v5, p0

    :goto_1
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_1
    move-object/from16 v5, p0

    return-void
.end method


# virtual methods
.method public getAngle()F
    .locals 1

    .line 142
    iget v0, p0, Lcom/android/helper/Options;->angle:F

    return v0
.end method

.method public getAudio()Z
    .locals 1

    .line 102
    iget-boolean v0, p0, Lcom/android/helper/Options;->audio:Z

    return v0
.end method

.method public getAudioBitRate()I
    .locals 1

    .line 134
    iget v0, p0, Lcom/android/helper/Options;->audioBitRate:I

    return v0
.end method

.method public getAudioCodec()Lcom/android/helper/audio/AudioCodec;
    .locals 1

    .line 114
    iget-object v0, p0, Lcom/android/helper/Options;->audioCodec:Lcom/android/helper/audio/AudioCodec;

    return-object v0
.end method

.method public getAudioCodecOptions()Ljava/util/List;
    .locals 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;"
        }
    .end annotation

    .line 210
    iget-object v0, p0, Lcom/android/helper/Options;->audioCodecOptions:Ljava/util/List;

    return-object v0
.end method

.method public getAudioDup()Z
    .locals 1

    .line 126
    iget-boolean v0, p0, Lcom/android/helper/Options;->audioDup:Z

    return v0
.end method

.method public getAudioEncoder()Ljava/lang/String;
    .locals 1

    .line 218
    iget-object v0, p0, Lcom/android/helper/Options;->audioEncoder:Ljava/lang/String;

    return-object v0
.end method

.method public getAudioSocket()Ljava/lang/String;
    .locals 1

    .line 310
    iget-object v0, p0, Lcom/android/helper/Options;->audioSocket:Ljava/lang/String;

    return-object v0
.end method

.method public getAudioSource()Lcom/android/helper/audio/AudioSource;
    .locals 1

    .line 122
    iget-object v0, p0, Lcom/android/helper/Options;->audioSource:Lcom/android/helper/audio/AudioSource;

    return-object v0
.end method

.method public getCameraAspectRatio()Lcom/android/helper/video/CameraAspectRatio;
    .locals 1

    .line 174
    iget-object v0, p0, Lcom/android/helper/Options;->cameraAspectRatio:Lcom/android/helper/video/CameraAspectRatio;

    return-object v0
.end method

.method public getCameraFacing()Lcom/android/helper/video/CameraFacing;
    .locals 1

    .line 170
    iget-object v0, p0, Lcom/android/helper/Options;->cameraFacing:Lcom/android/helper/video/CameraFacing;

    return-object v0
.end method

.method public getCameraFps()I
    .locals 1

    .line 178
    iget v0, p0, Lcom/android/helper/Options;->cameraFps:I

    return v0
.end method

.method public getCameraHighSpeed()Z
    .locals 1

    .line 182
    iget-boolean v0, p0, Lcom/android/helper/Options;->cameraHighSpeed:Z

    return v0
.end method

.method public getCameraId()Ljava/lang/String;
    .locals 1

    .line 162
    iget-object v0, p0, Lcom/android/helper/Options;->cameraId:Ljava/lang/String;

    return-object v0
.end method

.method public getCameraSize()Lcom/android/helper/device/Size;
    .locals 1

    .line 166
    iget-object v0, p0, Lcom/android/helper/Options;->cameraSize:Lcom/android/helper/device/Size;

    return-object v0
.end method

.method public getCameraZoom()F
    .locals 1

    .line 186
    iget v0, p0, Lcom/android/helper/Options;->cameraZoom:F

    return v0
.end method

.method public getCaptureOrientation()Lcom/android/helper/device/Orientation;
    .locals 1

    .line 246
    iget-object v0, p0, Lcom/android/helper/Options;->captureOrientation:Lcom/android/helper/device/Orientation;

    return-object v0
.end method

.method public getCaptureOrientationLock()Lcom/android/helper/device/Orientation$Lock;
    .locals 1

    .line 250
    iget-object v0, p0, Lcom/android/helper/Options;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    return-object v0
.end method

.method public getCleanup()Z
    .locals 1

    .line 234
    iget-boolean v0, p0, Lcom/android/helper/Options;->cleanup:Z

    return v0
.end method

.method public getClipboardAutosync()Z
    .locals 1

    .line 226
    iget-boolean v0, p0, Lcom/android/helper/Options;->clipboardAutosync:Z

    return v0
.end method

.method public getControl()Z
    .locals 1

    .line 154
    iget-boolean v0, p0, Lcom/android/helper/Options;->control:Z

    return v0
.end method

.method public getControlSocket()Ljava/lang/String;
    .locals 1

    .line 314
    iget-object v0, p0, Lcom/android/helper/Options;->controlSocket:Ljava/lang/String;

    return-object v0
.end method

.method public getCrop()Landroid/graphics/Rect;
    .locals 1

    .line 150
    iget-object v0, p0, Lcom/android/helper/Options;->crop:Landroid/graphics/Rect;

    return-object v0
.end method

.method public getDisplayId()I
    .locals 1

    .line 158
    iget v0, p0, Lcom/android/helper/Options;->displayId:I

    return v0
.end method

.method public getDisplayImePolicy()I
    .locals 1

    .line 202
    iget v0, p0, Lcom/android/helper/Options;->displayImePolicy:I

    return v0
.end method

.method public getDownsizeOnError()Z
    .locals 1

    .line 230
    iget-boolean v0, p0, Lcom/android/helper/Options;->downsizeOnError:Z

    return v0
.end method

.method public getList()Z
    .locals 1

    .line 262
    iget-boolean v0, p0, Lcom/android/helper/Options;->listEncoders:Z

    if-nez v0, :cond_1

    iget-boolean v0, p0, Lcom/android/helper/Options;->listDisplays:Z

    if-nez v0, :cond_1

    iget-boolean v0, p0, Lcom/android/helper/Options;->listCameras:Z

    if-nez v0, :cond_1

    iget-boolean v0, p0, Lcom/android/helper/Options;->listCameraSizes:Z

    if-nez v0, :cond_1

    iget-boolean v0, p0, Lcom/android/helper/Options;->listApps:Z

    if-eqz v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v0, 0x0

    return v0

    :cond_1
    :goto_0
    const/4 v0, 0x1

    return v0
.end method

.method public getListApps()Z
    .locals 1

    .line 282
    iget-boolean v0, p0, Lcom/android/helper/Options;->listApps:Z

    return v0
.end method

.method public getListCameraSizes()Z
    .locals 1

    .line 278
    iget-boolean v0, p0, Lcom/android/helper/Options;->listCameraSizes:Z

    return v0
.end method

.method public getListCameras()Z
    .locals 1

    .line 274
    iget-boolean v0, p0, Lcom/android/helper/Options;->listCameras:Z

    return v0
.end method

.method public getListDisplays()Z
    .locals 1

    .line 270
    iget-boolean v0, p0, Lcom/android/helper/Options;->listDisplays:Z

    return v0
.end method

.method public getListEncoders()Z
    .locals 1

    .line 266
    iget-boolean v0, p0, Lcom/android/helper/Options;->listEncoders:Z

    return v0
.end method

.method public getLogLevel()Lcom/android/helper/util/Ln$Level;
    .locals 1

    .line 90
    iget-object v0, p0, Lcom/android/helper/Options;->logLevel:Lcom/android/helper/util/Ln$Level;

    return-object v0
.end method

.method public getMaxFps()F
    .locals 1

    .line 138
    iget v0, p0, Lcom/android/helper/Options;->maxFps:F

    return v0
.end method

.method public getMaxSize()I
    .locals 1

    .line 106
    iget v0, p0, Lcom/android/helper/Options;->maxSize:I

    return v0
.end method

.method public getNewDisplay()Lcom/android/helper/device/NewDisplay;
    .locals 1

    .line 242
    iget-object v0, p0, Lcom/android/helper/Options;->newDisplay:Lcom/android/helper/device/NewDisplay;

    return-object v0
.end method

.method public getPort()I
    .locals 1

    .line 302
    iget v0, p0, Lcom/android/helper/Options;->port:I

    return v0
.end method

.method public getPowerOffScreenOnClose()Z
    .locals 1

    .line 222
    iget-boolean v0, p0, Lcom/android/helper/Options;->powerOffScreenOnClose:Z

    return v0
.end method

.method public getPowerOn()Z
    .locals 1

    .line 238
    iget-boolean v0, p0, Lcom/android/helper/Options;->powerOn:Z

    return v0
.end method

.method public getScid()I
    .locals 1

    .line 94
    iget v0, p0, Lcom/android/helper/Options;->scid:I

    return v0
.end method

.method public getScreenOffTimeout()I
    .locals 1

    .line 198
    iget v0, p0, Lcom/android/helper/Options;->screenOffTimeout:I

    return v0
.end method

.method public getSendCodecMeta()Z
    .locals 1

    .line 298
    iget-boolean v0, p0, Lcom/android/helper/Options;->sendCodecMeta:Z

    return v0
.end method

.method public getSendDeviceMeta()Z
    .locals 1

    .line 286
    iget-boolean v0, p0, Lcom/android/helper/Options;->sendDeviceMeta:Z

    return v0
.end method

.method public getSendDummyByte()Z
    .locals 1

    .line 294
    iget-boolean v0, p0, Lcom/android/helper/Options;->sendDummyByte:Z

    return v0
.end method

.method public getSendFrameMeta()Z
    .locals 1

    .line 290
    iget-boolean v0, p0, Lcom/android/helper/Options;->sendFrameMeta:Z

    return v0
.end method

.method public getShowTouches()Z
    .locals 1

    .line 190
    iget-boolean v0, p0, Lcom/android/helper/Options;->showTouches:Z

    return v0
.end method

.method public getStayAwake()Z
    .locals 1

    .line 194
    iget-boolean v0, p0, Lcom/android/helper/Options;->stayAwake:Z

    return v0
.end method

.method public getTouchSocket()Ljava/lang/String;
    .locals 1

    .line 318
    iget-object v0, p0, Lcom/android/helper/Options;->touchSocket:Ljava/lang/String;

    return-object v0
.end method

.method public getVDDestroyContent()Z
    .locals 1

    .line 254
    iget-boolean v0, p0, Lcom/android/helper/Options;->vdDestroyContent:Z

    return v0
.end method

.method public getVDSystemDecorations()Z
    .locals 1

    .line 258
    iget-boolean v0, p0, Lcom/android/helper/Options;->vdSystemDecorations:Z

    return v0
.end method

.method public getVideo()Z
    .locals 1

    .line 98
    iget-boolean v0, p0, Lcom/android/helper/Options;->video:Z

    return v0
.end method

.method public getVideoBitRate()I
    .locals 1

    .line 130
    iget v0, p0, Lcom/android/helper/Options;->videoBitRate:I

    return v0
.end method

.method public getVideoCodec()Lcom/android/helper/video/VideoCodec;
    .locals 1

    .line 110
    iget-object v0, p0, Lcom/android/helper/Options;->videoCodec:Lcom/android/helper/video/VideoCodec;

    return-object v0
.end method

.method public getVideoCodecOptions()Ljava/util/List;
    .locals 1
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lcom/android/helper/util/CodecOption;",
            ">;"
        }
    .end annotation

    .line 206
    iget-object v0, p0, Lcom/android/helper/Options;->videoCodecOptions:Ljava/util/List;

    return-object v0
.end method

.method public getVideoEncoder()Ljava/lang/String;
    .locals 1

    .line 214
    iget-object v0, p0, Lcom/android/helper/Options;->videoEncoder:Ljava/lang/String;

    return-object v0
.end method

.method public getVideoSocket()Ljava/lang/String;
    .locals 1

    .line 306
    iget-object v0, p0, Lcom/android/helper/Options;->videoSocket:Ljava/lang/String;

    return-object v0
.end method

.method public getVideoSource()Lcom/android/helper/video/VideoSource;
    .locals 1

    .line 118
    iget-object v0, p0, Lcom/android/helper/Options;->videoSource:Lcom/android/helper/video/VideoSource;

    return-object v0
.end method

.method public isTunnelForward()Z
    .locals 1

    .line 146
    iget-boolean v0, p0, Lcom/android/helper/Options;->tunnelForward:Z

    return v0
.end method

.method public setOption(Ljava/lang/String;Ljava/lang/String;)V
    .locals 7

    .line 364
    invoke-virtual {p1}, Ljava/lang/String;->hashCode()I

    invoke-virtual {p1}, Ljava/lang/String;->hashCode()I

    move-result v0

    const-string v1, "max_fps"

    const-string v2, "angle"

    const/16 v3, 0x10

    const/4 v4, 0x0

    const/4 v5, -0x1

    sparse-switch v0, :sswitch_data_0

    :goto_0
    const/4 v0, -0x1

    goto/16 :goto_1

    :sswitch_0
    const-string v0, "send_device_meta"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    goto :goto_0

    :cond_0
    const/16 v0, 0x38

    goto/16 :goto_1

    :sswitch_1
    const-string v0, "camera_zoom"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    goto :goto_0

    :cond_1
    const/16 v0, 0x37

    goto/16 :goto_1

    :sswitch_2
    const-string v0, "camera_size"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2

    goto :goto_0

    :cond_2
    const/16 v0, 0x36

    goto/16 :goto_1

    :sswitch_3
    const-string v0, "list_displays"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_3

    goto :goto_0

    :cond_3
    const/16 v0, 0x35

    goto/16 :goto_1

    :sswitch_4
    const-string v0, "video_codec_options"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_4

    goto :goto_0

    :cond_4
    const/16 v0, 0x34

    goto/16 :goto_1

    :sswitch_5
    const-string v0, "camera_high_speed"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_5

    goto :goto_0

    :cond_5
    const/16 v0, 0x33

    goto/16 :goto_1

    :sswitch_6
    const-string v0, "video_codec"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_6

    goto :goto_0

    :cond_6
    const/16 v0, 0x32

    goto/16 :goto_1

    :sswitch_7
    const-string v0, "audio_codec_options"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_7

    goto :goto_0

    :cond_7
    const/16 v0, 0x31

    goto/16 :goto_1

    :sswitch_8
    const-string v0, "control"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_8

    goto :goto_0

    :cond_8
    const/16 v0, 0x30

    goto/16 :goto_1

    :sswitch_9
    const-string v0, "downsize_on_error"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_9

    goto/16 :goto_0

    :cond_9
    const/16 v0, 0x2f

    goto/16 :goto_1

    :sswitch_a
    const-string v0, "new_display"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_a

    goto/16 :goto_0

    :cond_a
    const/16 v0, 0x2e

    goto/16 :goto_1

    :sswitch_b
    const-string v0, "power_on"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_b

    goto/16 :goto_0

    :cond_b
    const/16 v0, 0x2d

    goto/16 :goto_1

    :sswitch_c
    const-string v0, "cleanup"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_c

    goto/16 :goto_0

    :cond_c
    const/16 v0, 0x2c

    goto/16 :goto_1

    :sswitch_d
    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_d

    goto/16 :goto_0

    :cond_d
    const/16 v0, 0x2b

    goto/16 :goto_1

    :sswitch_e
    const-string v0, "audio_codec"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_e

    goto/16 :goto_0

    :cond_e
    const/16 v0, 0x2a

    goto/16 :goto_1

    :sswitch_f
    const-string v0, "send_frame_meta"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_f

    goto/16 :goto_0

    :cond_f
    const/16 v0, 0x29

    goto/16 :goto_1

    :sswitch_10
    const-string v0, "send_codec_meta"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_10

    goto/16 :goto_0

    :cond_10
    const/16 v0, 0x28

    goto/16 :goto_1

    :sswitch_11
    const-string v0, "video_encoder"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_11

    goto/16 :goto_0

    :cond_11
    const/16 v0, 0x27

    goto/16 :goto_1

    :sswitch_12
    const-string v0, "max_size"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_12

    goto/16 :goto_0

    :cond_12
    const/16 v0, 0x26

    goto/16 :goto_1

    :sswitch_13
    const-string v0, "show_touches"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_13

    goto/16 :goto_0

    :cond_13
    const/16 v0, 0x25

    goto/16 :goto_1

    :sswitch_14
    const-string v0, "screen_off_timeout"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_14

    goto/16 :goto_0

    :cond_14
    const/16 v0, 0x24

    goto/16 :goto_1

    :sswitch_15
    const-string v0, "audio_dup"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_15

    goto/16 :goto_0

    :cond_15
    const/16 v0, 0x23

    goto/16 :goto_1

    :sswitch_16
    const-string v0, "video"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_16

    goto/16 :goto_0

    :cond_16
    const/16 v0, 0x22

    goto/16 :goto_1

    :sswitch_17
    const-string v0, "audio"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_17

    goto/16 :goto_0

    :cond_17
    const/16 v0, 0x21

    goto/16 :goto_1

    :sswitch_18
    invoke-virtual {p1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_18

    goto/16 :goto_0

    :cond_18
    const/16 v0, 0x20

    goto/16 :goto_1

    :sswitch_19
    const-string v0, "scid"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_19

    goto/16 :goto_0

    :cond_19
    const/16 v0, 0x1f

    goto/16 :goto_1

    :sswitch_1a
    const-string v0, "port"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1a

    goto/16 :goto_0

    :cond_1a
    const/16 v0, 0x1e

    goto/16 :goto_1

    :sswitch_1b
    const-string v0, "crop"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1b

    goto/16 :goto_0

    :cond_1b
    const/16 v0, 0x1d

    goto/16 :goto_1

    :sswitch_1c
    const-string v0, "video_source"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1c

    goto/16 :goto_0

    :cond_1c
    const/16 v0, 0x1c

    goto/16 :goto_1

    :sswitch_1d
    const-string v0, "video_socket"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1d

    goto/16 :goto_0

    :cond_1d
    const/16 v0, 0x1b

    goto/16 :goto_1

    :sswitch_1e
    const-string v0, "send_dummy_byte"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1e

    goto/16 :goto_0

    :cond_1e
    const/16 v0, 0x1a

    goto/16 :goto_1

    :sswitch_1f
    const-string v0, "tunnel_forward"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1f

    goto/16 :goto_0

    :cond_1f
    const/16 v0, 0x19

    goto/16 :goto_1

    :sswitch_20
    const-string v0, "stay_awake"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_20

    goto/16 :goto_0

    :cond_20
    const/16 v0, 0x18

    goto/16 :goto_1

    :sswitch_21
    const-string v0, "camera_id"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_21

    goto/16 :goto_0

    :cond_21
    const/16 v0, 0x17

    goto/16 :goto_1

    :sswitch_22
    const-string v0, "camera_ar"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_22

    goto/16 :goto_0

    :cond_22
    const/16 v0, 0x16

    goto/16 :goto_1

    :sswitch_23
    const-string v0, "list_cameras"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_23

    goto/16 :goto_0

    :cond_23
    const/16 v0, 0x15

    goto/16 :goto_1

    :sswitch_24
    const-string v0, "video_bit_rate"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_24

    goto/16 :goto_0

    :cond_24
    const/16 v0, 0x14

    goto/16 :goto_1

    :sswitch_25
    const-string v0, "audio_bit_rate"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_25

    goto/16 :goto_0

    :cond_25
    const/16 v0, 0x13

    goto/16 :goto_1

    :sswitch_26
    const-string v0, "control_socket"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_26

    goto/16 :goto_0

    :cond_26
    const/16 v0, 0x12

    goto/16 :goto_1

    :sswitch_27
    const-string v0, "power_off_on_close"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_27

    goto/16 :goto_0

    :cond_27
    const/16 v0, 0x11

    goto/16 :goto_1

    :sswitch_28
    const-string v0, "display_id"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_28

    goto/16 :goto_0

    :cond_28
    const/16 v0, 0x10

    goto/16 :goto_1

    :sswitch_29
    const-string v0, "capture_orientation"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_29

    goto/16 :goto_0

    :cond_29
    const/16 v0, 0xf

    goto/16 :goto_1

    :sswitch_2a
    const-string v0, "list_encoders"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2a

    goto/16 :goto_0

    :cond_2a
    const/16 v0, 0xe

    goto/16 :goto_1

    :sswitch_2b
    const-string v0, "display_ime_policy"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2b

    goto/16 :goto_0

    :cond_2b
    const/16 v0, 0xd

    goto/16 :goto_1

    :sswitch_2c
    const-string v0, "clipboard_autosync"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2c

    goto/16 :goto_0

    :cond_2c
    const/16 v0, 0xc

    goto/16 :goto_1

    :sswitch_2d
    const-string v0, "vd_system_decorations"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2d

    goto/16 :goto_0

    :cond_2d
    const/16 v0, 0xb

    goto/16 :goto_1

    :sswitch_2e
    const-string v0, "vd_destroy_content"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2e

    goto/16 :goto_0

    :cond_2e
    const/16 v0, 0xa

    goto/16 :goto_1

    :sswitch_2f
    const-string v0, "list_apps"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2f

    goto/16 :goto_0

    :cond_2f
    const/16 v0, 0x9

    goto/16 :goto_1

    :sswitch_30
    const-string v0, "audio_encoder"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_30

    goto/16 :goto_0

    :cond_30
    const/16 v0, 0x8

    goto/16 :goto_1

    :sswitch_31
    const-string v0, "raw_stream"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_31

    goto/16 :goto_0

    :cond_31
    const/4 v0, 0x7

    goto :goto_1

    :sswitch_32
    const-string v0, "audio_source"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_32

    goto/16 :goto_0

    :cond_32
    const/4 v0, 0x6

    goto :goto_1

    :sswitch_33
    const-string v0, "audio_socket"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_33

    goto/16 :goto_0

    :cond_33
    const/4 v0, 0x5

    goto :goto_1

    :sswitch_34
    const-string v0, "touch_socket"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_34

    goto/16 :goto_0

    :cond_34
    const/4 v0, 0x4

    goto :goto_1

    :sswitch_35
    const-string v0, "camera_facing"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_35

    goto/16 :goto_0

    :cond_35
    const/4 v0, 0x3

    goto :goto_1

    :sswitch_36
    const-string v0, "list_camera_sizes"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_36

    goto/16 :goto_0

    :cond_36
    const/4 v0, 0x2

    goto :goto_1

    :sswitch_37
    const-string v0, "log_level"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_37

    goto/16 :goto_0

    :cond_37
    const/4 v0, 0x1

    goto :goto_1

    :sswitch_38
    const-string v0, "camera_fps"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_38

    goto/16 :goto_0

    :cond_38
    const/4 v0, 0x0

    .line 588
    :goto_1
    const-string v6, " not supported"

    packed-switch v0, :pswitch_data_0

    new-instance p2, Ljava/lang/StringBuilder;

    const-string v0, "Unknown server option: "

    invoke-direct {p2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    .line 552
    :pswitch_0
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->sendDeviceMeta:Z

    return-void

    .line 530
    :pswitch_1
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 531
    invoke-static {p2}, Ljava/lang/Float;->parseFloat(Ljava/lang/String;)F

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->cameraZoom:F

    return-void

    .line 505
    :pswitch_2
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 506
    invoke-static {p2}, Lcom/android/helper/Options;->parseSize(Ljava/lang/String;)Lcom/android/helper/device/Size;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->cameraSize:Lcom/android/helper/device/Size;

    return-void

    .line 488
    :pswitch_3
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->listDisplays:Z

    return-void

    .line 454
    :pswitch_4
    invoke-static {p2}, Lcom/android/helper/util/CodecOption;->parse(Ljava/lang/String;)Ljava/util/List;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->videoCodecOptions:Ljava/util/List;

    return-void

    .line 527
    :pswitch_5
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->cameraHighSpeed:Z

    return-void

    .line 382
    :pswitch_6
    invoke-static {p2}, Lcom/android/helper/video/VideoCodec;->findByName(Ljava/lang/String;)Lcom/android/helper/video/VideoCodec;

    move-result-object p1

    if-eqz p1, :cond_39

    .line 386
    iput-object p1, p0, Lcom/android/helper/Options;->videoCodec:Lcom/android/helper/video/VideoCodec;

    return-void

    .line 384
    :cond_39
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Video codec "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 457
    :pswitch_7
    invoke-static {p2}, Lcom/android/helper/util/CodecOption;->parse(Ljava/lang/String;)Ljava/util/List;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->audioCodecOptions:Ljava/util/List;

    return-void

    .line 436
    :pswitch_8
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->control:Z

    return-void

    .line 476
    :pswitch_9
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->downsizeOnError:Z

    return-void

    .line 535
    :pswitch_a
    invoke-static {p2}, Lcom/android/helper/Options;->parseNewDisplay(Ljava/lang/String;)Lcom/android/helper/device/NewDisplay;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->newDisplay:Lcom/android/helper/device/NewDisplay;

    return-void

    .line 482
    :pswitch_b
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->powerOn:Z

    return-void

    .line 479
    :pswitch_c
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->cleanup:Z

    return-void

    .line 422
    :pswitch_d
    invoke-static {v1, p2}, Lcom/android/helper/Options;->parseFloat(Ljava/lang/String;Ljava/lang/String;)F

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->maxFps:F

    return-void

    .line 389
    :pswitch_e
    invoke-static {p2}, Lcom/android/helper/audio/AudioCodec;->findByName(Ljava/lang/String;)Lcom/android/helper/audio/AudioCodec;

    move-result-object p1

    if-eqz p1, :cond_3a

    .line 393
    iput-object p1, p0, Lcom/android/helper/Options;->audioCodec:Lcom/android/helper/audio/AudioCodec;

    return-void

    .line 391
    :cond_3a
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Audio codec "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 555
    :pswitch_f
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->sendFrameMeta:Z

    return-void

    .line 561
    :pswitch_10
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->sendCodecMeta:Z

    return-void

    .line 460
    :pswitch_11
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 461
    iput-object p2, p0, Lcom/android/helper/Options;->videoEncoder:Ljava/lang/String;

    return-void

    .line 413
    :pswitch_12
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    and-int/lit8 p1, p1, -0x8

    iput p1, p0, Lcom/android/helper/Options;->maxSize:I

    return-void

    .line 442
    :pswitch_13
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->showTouches:Z

    return-void

    .line 448
    :pswitch_14
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->screenOffTimeout:I

    if-lt p1, v5, :cond_3b

    goto/16 :goto_2

    .line 450
    :cond_3b
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance p2, Ljava/lang/StringBuilder;

    const-string v0, "Invalid screen off timeout: "

    invoke-direct {p2, v0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v0, p0, Lcom/android/helper/Options;->screenOffTimeout:I

    invoke-virtual {p2, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {p2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 410
    :pswitch_15
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->audioDup:Z

    return-void

    .line 376
    :pswitch_16
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->video:Z

    return-void

    .line 379
    :pswitch_17
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->audio:Z

    return-void

    .line 425
    :pswitch_18
    invoke-static {v2, p2}, Lcom/android/helper/Options;->parseFloat(Ljava/lang/String;Ljava/lang/String;)F

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->angle:F

    return-void

    .line 366
    :pswitch_19
    invoke-static {p2, v3}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;I)I

    move-result p1

    if-lt p1, v5, :cond_3c

    .line 370
    iput p1, p0, Lcom/android/helper/Options;->scid:I

    return-void

    .line 368
    :cond_3c
    new-instance p2, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "scid may not be negative (except -1 for \'none\'): "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p2, p1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p2

    .line 573
    :pswitch_1a
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->port:I

    return-void

    .line 431
    :pswitch_1b
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 432
    invoke-static {p2}, Lcom/android/helper/Options;->parseCrop(Ljava/lang/String;)Landroid/graphics/Rect;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->crop:Landroid/graphics/Rect;

    return-void

    .line 396
    :pswitch_1c
    invoke-static {p2}, Lcom/android/helper/video/VideoSource;->findByName(Ljava/lang/String;)Lcom/android/helper/video/VideoSource;

    move-result-object p1

    if-eqz p1, :cond_3d

    .line 400
    iput-object p1, p0, Lcom/android/helper/Options;->videoSource:Lcom/android/helper/video/VideoSource;

    return-void

    .line 398
    :cond_3d
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Video source "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 576
    :pswitch_1d
    iput-object p2, p0, Lcom/android/helper/Options;->videoSocket:Ljava/lang/String;

    return-void

    .line 558
    :pswitch_1e
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->sendDummyByte:Z

    return-void

    .line 428
    :pswitch_1f
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->tunnelForward:Z

    return-void

    .line 445
    :pswitch_20
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->stayAwake:Z

    return-void

    .line 500
    :pswitch_21
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 501
    iput-object p2, p0, Lcom/android/helper/Options;->cameraId:Ljava/lang/String;

    return-void

    .line 519
    :pswitch_22
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 520
    invoke-static {p2}, Lcom/android/helper/Options;->parseCameraAspectRatio(Ljava/lang/String;)Lcom/android/helper/video/CameraAspectRatio;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->cameraAspectRatio:Lcom/android/helper/video/CameraAspectRatio;

    return-void

    .line 491
    :pswitch_23
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->listCameras:Z

    return-void

    .line 416
    :pswitch_24
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->videoBitRate:I

    return-void

    .line 419
    :pswitch_25
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->audioBitRate:I

    return-void

    .line 582
    :pswitch_26
    iput-object p2, p0, Lcom/android/helper/Options;->controlSocket:Ljava/lang/String;

    return-void

    .line 470
    :pswitch_27
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->powerOffScreenOnClose:Z

    return-void

    .line 439
    :pswitch_28
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->displayId:I

    return-void

    .line 544
    :pswitch_29
    invoke-static {p2}, Lcom/android/helper/Options;->parseCaptureOrientation(Ljava/lang/String;)Landroid/util/Pair;

    move-result-object p1

    .line 545
    iget-object p2, p1, Landroid/util/Pair;->first:Ljava/lang/Object;

    check-cast p2, Lcom/android/helper/device/Orientation$Lock;

    iput-object p2, p0, Lcom/android/helper/Options;->captureOrientationLock:Lcom/android/helper/device/Orientation$Lock;

    .line 546
    iget-object p1, p1, Landroid/util/Pair;->second:Ljava/lang/Object;

    check-cast p1, Lcom/android/helper/device/Orientation;

    iput-object p1, p0, Lcom/android/helper/Options;->captureOrientation:Lcom/android/helper/device/Orientation;

    return-void

    .line 485
    :pswitch_2a
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->listEncoders:Z

    return-void

    .line 549
    :pswitch_2b
    invoke-static {p2}, Lcom/android/helper/Options;->parseDisplayImePolicy(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->displayImePolicy:I

    return-void

    .line 473
    :pswitch_2c
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->clipboardAutosync:Z

    return-void

    .line 541
    :pswitch_2d
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->vdSystemDecorations:Z

    return-void

    .line 538
    :pswitch_2e
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->vdDestroyContent:Z

    return-void

    .line 497
    :pswitch_2f
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->listApps:Z

    return-void

    .line 465
    :pswitch_30
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 466
    iput-object p2, p0, Lcom/android/helper/Options;->audioEncoder:Ljava/lang/String;

    return-void

    .line 564
    :pswitch_31
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    if-eqz p1, :cond_40

    .line 566
    iput-boolean v4, p0, Lcom/android/helper/Options;->sendDeviceMeta:Z

    .line 567
    iput-boolean v4, p0, Lcom/android/helper/Options;->sendFrameMeta:Z

    .line 568
    iput-boolean v4, p0, Lcom/android/helper/Options;->sendDummyByte:Z

    .line 569
    iput-boolean v4, p0, Lcom/android/helper/Options;->sendCodecMeta:Z

    return-void

    .line 403
    :pswitch_32
    invoke-static {p2}, Lcom/android/helper/audio/AudioSource;->findByName(Ljava/lang/String;)Lcom/android/helper/audio/AudioSource;

    move-result-object p1

    if-eqz p1, :cond_3e

    .line 407
    iput-object p1, p0, Lcom/android/helper/Options;->audioSource:Lcom/android/helper/audio/AudioSource;

    return-void

    .line 405
    :cond_3e
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Audio source "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    .line 579
    :pswitch_33
    iput-object p2, p0, Lcom/android/helper/Options;->audioSocket:Ljava/lang/String;

    return-void

    .line 585
    :pswitch_34
    iput-object p2, p0, Lcom/android/helper/Options;->touchSocket:Ljava/lang/String;

    return-void

    .line 510
    :pswitch_35
    invoke-virtual {p2}, Ljava/lang/String;->isEmpty()Z

    move-result p1

    if-nez p1, :cond_40

    .line 511
    invoke-static {p2}, Lcom/android/helper/video/CameraFacing;->findByName(Ljava/lang/String;)Lcom/android/helper/video/CameraFacing;

    move-result-object p1

    if-eqz p1, :cond_3f

    .line 515
    iput-object p1, p0, Lcom/android/helper/Options;->cameraFacing:Lcom/android/helper/video/CameraFacing;

    return-void

    .line 513
    :cond_3f
    new-instance p1, Ljava/lang/IllegalArgumentException;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "Camera facing "

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p2

    invoke-direct {p1, p2}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_40
    :goto_2
    return-void

    .line 494
    :pswitch_36
    invoke-static {p2}, Ljava/lang/Boolean;->parseBoolean(Ljava/lang/String;)Z

    move-result p1

    iput-boolean p1, p0, Lcom/android/helper/Options;->listCameraSizes:Z

    return-void

    .line 373
    :pswitch_37
    sget-object p1, Ljava/util/Locale;->ENGLISH:Ljava/util/Locale;

    invoke-virtual {p2, p1}, Ljava/lang/String;->toUpperCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln$Level;->valueOf(Ljava/lang/String;)Lcom/android/helper/util/Ln$Level;

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/Options;->logLevel:Lcom/android/helper/util/Ln$Level;

    return-void

    .line 524
    :pswitch_38
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result p1

    iput p1, p0, Lcom/android/helper/Options;->cameraFps:I

    return-void

    :sswitch_data_0
    .sparse-switch
        -0x77e99b31 -> :sswitch_38
        -0x779ee137 -> :sswitch_37
        -0x5e0e3f07 -> :sswitch_36
        -0x5adbd9cc -> :sswitch_35
        -0x58dd978d -> :sswitch_34
        -0x55ce5c04 -> :sswitch_33
        -0x55c6135c -> :sswitch_32
        -0x536c6889 -> :sswitch_31
        -0x4a476e4d -> :sswitch_30
        -0x48fe7a8d -> :sswitch_2f
        -0x4265d65d -> :sswitch_2e
        -0x3f07731c -> :sswitch_2d
        -0x3d563aad -> :sswitch_2c
        -0x39cf70f3 -> :sswitch_2b
        -0x39748ea8 -> :sswitch_2a
        -0x368f9da9 -> :sswitch_29
        -0x36827648 -> :sswitch_28
        -0x2fa3329e -> :sswitch_27
        -0x251d9b6b -> :sswitch_26
        -0x22a1d0e5 -> :sswitch_25
        -0x1d275fea -> :sswitch_24
        -0x15f284b3 -> :sswitch_23
        -0x14626075 -> :sswitch_22
        -0x14625f8b -> :sswitch_21
        -0xf3103e1 -> :sswitch_20
        -0xaf91e12 -> :sswitch_1f
        -0x29d40aa -> :sswitch_1e
        -0x5e849 -> :sswitch_1d
        0x2605f -> :sswitch_1c
        0x2eba90 -> :sswitch_1b
        0x349881 -> :sswitch_1a
        0x35c76b -> :sswitch_19
        0x58a78d3 -> :sswitch_18
        0x58d9bd6 -> :sswitch_17
        0x6b0147b -> :sswitch_16
        0xb3c7616 -> :sswitch_15
        0xf689f3e -> :sswitch_14
        0x12494ceb -> :sswitch_13
        0x1852b1fc -> :sswitch_12
        0x18fe9558 -> :sswitch_11
        0x1bdc5da5 -> :sswitch_10
        0x287e02ae -> :sswitch_f
        0x2de6566d -> :sswitch_e
        0x32550f8e -> :sswitch_d
        0x331156a4 -> :sswitch_c
        0x332c8f59 -> :sswitch_b
        0x3742c923 -> :sswitch_a
        0x386ad4c4 -> :sswitch_9
        0x38b7655d -> :sswitch_8
        0x4869c6cc -> :sswitch_7
        0x51b2ff52 -> :sswitch_6
        0x6a1798c4 -> :sswitch_5
        0x6a45bab1 -> :sswitch_4
        0x718a5272 -> :sswitch_3
        0x7abc04db -> :sswitch_2
        0x7abf48ad -> :sswitch_1
        0x7f855817 -> :sswitch_0
    .end sparse-switch

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_38
        :pswitch_37
        :pswitch_36
        :pswitch_35
        :pswitch_34
        :pswitch_33
        :pswitch_32
        :pswitch_31
        :pswitch_30
        :pswitch_2f
        :pswitch_2e
        :pswitch_2d
        :pswitch_2c
        :pswitch_2b
        :pswitch_2a
        :pswitch_29
        :pswitch_28
        :pswitch_27
        :pswitch_26
        :pswitch_25
        :pswitch_24
        :pswitch_23
        :pswitch_22
        :pswitch_21
        :pswitch_20
        :pswitch_1f
        :pswitch_1e
        :pswitch_1d
        :pswitch_1c
        :pswitch_1b
        :pswitch_1a
        :pswitch_19
        :pswitch_18
        :pswitch_17
        :pswitch_16
        :pswitch_15
        :pswitch_14
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
