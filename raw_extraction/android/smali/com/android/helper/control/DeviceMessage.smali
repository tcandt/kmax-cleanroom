.class public final Lcom/android/helper/control/DeviceMessage;
.super Ljava/lang/Object;
.source "DeviceMessage.java"


# static fields
.field public static final TYPE_ACK_CLIPBOARD:I = 0x1

.field public static final TYPE_CLIPBOARD:I = 0x0

.field public static final TYPE_UHID_OUTPUT:I = 0x2


# instance fields
.field private data:[B

.field private id:I

.field private sequence:J

.field private text:Ljava/lang/String;

.field private type:I


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 15
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static createAckClipboard(J)Lcom/android/helper/control/DeviceMessage;
    .locals 2

    .line 26
    new-instance v0, Lcom/android/helper/control/DeviceMessage;

    invoke-direct {v0}, Lcom/android/helper/control/DeviceMessage;-><init>()V

    const/4 v1, 0x1

    .line 27
    iput v1, v0, Lcom/android/helper/control/DeviceMessage;->type:I

    .line 28
    iput-wide p0, v0, Lcom/android/helper/control/DeviceMessage;->sequence:J

    return-object v0
.end method

.method public static createClipboard(Ljava/lang/String;)Lcom/android/helper/control/DeviceMessage;
    .locals 2

    .line 19
    new-instance v0, Lcom/android/helper/control/DeviceMessage;

    invoke-direct {v0}, Lcom/android/helper/control/DeviceMessage;-><init>()V

    const/4 v1, 0x0

    .line 20
    iput v1, v0, Lcom/android/helper/control/DeviceMessage;->type:I

    .line 21
    iput-object p0, v0, Lcom/android/helper/control/DeviceMessage;->text:Ljava/lang/String;

    return-object v0
.end method

.method public static createUhidOutput(I[B)Lcom/android/helper/control/DeviceMessage;
    .locals 2

    .line 33
    new-instance v0, Lcom/android/helper/control/DeviceMessage;

    invoke-direct {v0}, Lcom/android/helper/control/DeviceMessage;-><init>()V

    const/4 v1, 0x2

    .line 34
    iput v1, v0, Lcom/android/helper/control/DeviceMessage;->type:I

    .line 35
    iput p0, v0, Lcom/android/helper/control/DeviceMessage;->id:I

    .line 36
    iput-object p1, v0, Lcom/android/helper/control/DeviceMessage;->data:[B

    return-object v0
.end method


# virtual methods
.method public getData()[B
    .locals 1

    .line 57
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessage;->data:[B

    return-object v0
.end method

.method public getId()I
    .locals 1

    .line 53
    iget v0, p0, Lcom/android/helper/control/DeviceMessage;->id:I

    return v0
.end method

.method public getSequence()J
    .locals 2

    .line 49
    iget-wide v0, p0, Lcom/android/helper/control/DeviceMessage;->sequence:J

    return-wide v0
.end method

.method public getText()Ljava/lang/String;
    .locals 1

    .line 45
    iget-object v0, p0, Lcom/android/helper/control/DeviceMessage;->text:Ljava/lang/String;

    return-object v0
.end method

.method public getType()I
    .locals 1

    .line 41
    iget v0, p0, Lcom/android/helper/control/DeviceMessage;->type:I

    return v0
.end method
