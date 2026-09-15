.class public final Lcom/android/helper/control/ControlMessage;
.super Ljava/lang/Object;
.source "ControlMessage.java"


# static fields
.field public static final COPY_KEY_COPY:I = 0x1

.field public static final COPY_KEY_CUT:I = 0x2

.field public static final COPY_KEY_NONE:I = 0x0

.field public static final SEQUENCE_INVALID:J = 0x0L

.field public static final TYPE_BACK_OR_SCREEN_ON:I = 0x4

.field public static final TYPE_COLLAPSE_PANELS:I = 0x7

.field public static final TYPE_EXPAND_NOTIFICATION_PANEL:I = 0x5

.field public static final TYPE_EXPAND_SETTINGS_PANEL:I = 0x6

.field public static final TYPE_GET_CLIPBOARD:I = 0x8

.field public static final TYPE_INJECT_KEYCODE:I = 0x0

.field public static final TYPE_INJECT_SCROLL_EVENT:I = 0x3

.field public static final TYPE_INJECT_TEXT:I = 0x1

.field public static final TYPE_INJECT_TOUCH_EVENT:I = 0x2

.field public static final TYPE_OPEN_HARD_KEYBOARD_SETTINGS:I = 0xf

.field public static final TYPE_REQUEST_KEYFRAME:I = 0x12

.field public static final TYPE_RESET_VIDEO:I = 0x11

.field public static final TYPE_ROTATE_DEVICE:I = 0xb

.field public static final TYPE_SET_BITRATE:I = 0x13

.field public static final TYPE_SET_CLIPBOARD:I = 0x9

.field public static final TYPE_SET_DISPLAY_POWER:I = 0xa

.field public static final TYPE_START_APP:I = 0x10

.field public static final TYPE_UHID_CREATE:I = 0xc

.field public static final TYPE_UHID_DESTROY:I = 0xe

.field public static final TYPE_UHID_INPUT:I = 0xd


# instance fields
.field private action:I

.field private actionButton:I

.field private bitrate:I

.field private buttons:I

.field private copyKey:I

.field private data:[B

.field private hScroll:F

.field private id:I

.field private keycode:I

.field private metaState:I

.field private on:Z

.field private paste:Z

.field private pointerId:J

.field private position:Lcom/android/helper/device/Position;

.field private pressure:F

.field private productId:I

.field private repeat:I

.field private sequence:J

.field private text:Ljava/lang/String;

.field private type:I

.field private vScroll:F

.field private vendorId:I


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 60
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static createBackOrScreenOn(I)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 104
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/4 v1, 0x4

    .line 105
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 106
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->action:I

    return-object v0
.end method

.method public static createEmpty(I)Lcom/android/helper/control/ControlMessage;
    .locals 1

    .line 134
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    .line 135
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->type:I

    return-object v0
.end method

.method public static createGetClipboard(I)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 111
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0x8

    .line 112
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 113
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->copyKey:I

    return-object v0
.end method

.method public static createInjectKeycode(IIII)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 64
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/4 v1, 0x0

    .line 65
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 66
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->action:I

    .line 67
    iput p1, v0, Lcom/android/helper/control/ControlMessage;->keycode:I

    .line 68
    iput p2, v0, Lcom/android/helper/control/ControlMessage;->repeat:I

    .line 69
    iput p3, v0, Lcom/android/helper/control/ControlMessage;->metaState:I

    return-object v0
.end method

.method public static createInjectScrollEvent(Lcom/android/helper/device/Position;FFI)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 94
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/4 v1, 0x3

    .line 95
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 96
    iput-object p0, v0, Lcom/android/helper/control/ControlMessage;->position:Lcom/android/helper/device/Position;

    .line 97
    iput p1, v0, Lcom/android/helper/control/ControlMessage;->hScroll:F

    .line 98
    iput p2, v0, Lcom/android/helper/control/ControlMessage;->vScroll:F

    .line 99
    iput p3, v0, Lcom/android/helper/control/ControlMessage;->buttons:I

    return-object v0
.end method

.method public static createInjectText(Ljava/lang/String;)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 74
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/4 v1, 0x1

    .line 75
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 76
    iput-object p0, v0, Lcom/android/helper/control/ControlMessage;->text:Ljava/lang/String;

    return-object v0
.end method

.method public static createInjectTouchEvent(IJLcom/android/helper/device/Position;FII)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 82
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/4 v1, 0x2

    .line 83
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 84
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->action:I

    .line 85
    iput-wide p1, v0, Lcom/android/helper/control/ControlMessage;->pointerId:J

    .line 86
    iput p4, v0, Lcom/android/helper/control/ControlMessage;->pressure:F

    .line 87
    iput-object p3, v0, Lcom/android/helper/control/ControlMessage;->position:Lcom/android/helper/device/Position;

    .line 88
    iput p5, v0, Lcom/android/helper/control/ControlMessage;->actionButton:I

    .line 89
    iput p6, v0, Lcom/android/helper/control/ControlMessage;->buttons:I

    return-object v0
.end method

.method public static createSetBitrate(I)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 173
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0x13

    .line 174
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 175
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->bitrate:I

    return-object v0
.end method

.method public static createSetClipboard(JLjava/lang/String;Z)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 118
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0x9

    .line 119
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 120
    iput-wide p0, v0, Lcom/android/helper/control/ControlMessage;->sequence:J

    .line 121
    iput-object p2, v0, Lcom/android/helper/control/ControlMessage;->text:Ljava/lang/String;

    .line 122
    iput-boolean p3, v0, Lcom/android/helper/control/ControlMessage;->paste:Z

    return-object v0
.end method

.method public static createSetDisplayPower(Z)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 127
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0xa

    .line 128
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 129
    iput-boolean p0, v0, Lcom/android/helper/control/ControlMessage;->on:Z

    return-object v0
.end method

.method public static createStartApp(Ljava/lang/String;)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 166
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0x10

    .line 167
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 168
    iput-object p0, v0, Lcom/android/helper/control/ControlMessage;->text:Ljava/lang/String;

    return-object v0
.end method

.method public static createUhidCreate(IIILjava/lang/String;[B)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 140
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0xc

    .line 141
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 142
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->id:I

    .line 143
    iput p1, v0, Lcom/android/helper/control/ControlMessage;->vendorId:I

    .line 144
    iput p2, v0, Lcom/android/helper/control/ControlMessage;->productId:I

    .line 145
    iput-object p3, v0, Lcom/android/helper/control/ControlMessage;->text:Ljava/lang/String;

    .line 146
    iput-object p4, v0, Lcom/android/helper/control/ControlMessage;->data:[B

    return-object v0
.end method

.method public static createUhidDestroy(I)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 159
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0xe

    .line 160
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 161
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->id:I

    return-object v0
.end method

.method public static createUhidInput(I[B)Lcom/android/helper/control/ControlMessage;
    .locals 2

    .line 151
    new-instance v0, Lcom/android/helper/control/ControlMessage;

    invoke-direct {v0}, Lcom/android/helper/control/ControlMessage;-><init>()V

    const/16 v1, 0xd

    .line 152
    iput v1, v0, Lcom/android/helper/control/ControlMessage;->type:I

    .line 153
    iput p0, v0, Lcom/android/helper/control/ControlMessage;->id:I

    .line 154
    iput-object p1, v0, Lcom/android/helper/control/ControlMessage;->data:[B

    return-object v0
.end method


# virtual methods
.method public getAction()I
    .locals 1

    .line 192
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->action:I

    return v0
.end method

.method public getActionButton()I
    .locals 1

    .line 200
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->actionButton:I

    return v0
.end method

.method public getBitrate()I
    .locals 1

    .line 264
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->bitrate:I

    return v0
.end method

.method public getButtons()I
    .locals 1

    .line 204
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->buttons:I

    return v0
.end method

.method public getCopyKey()I
    .locals 1

    .line 228
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->copyKey:I

    return v0
.end method

.method public getData()[B
    .locals 1

    .line 248
    iget-object v0, p0, Lcom/android/helper/control/ControlMessage;->data:[B

    return-object v0
.end method

.method public getHScroll()F
    .locals 1

    .line 220
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->hScroll:F

    return v0
.end method

.method public getId()I
    .locals 1

    .line 244
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->id:I

    return v0
.end method

.method public getKeycode()I
    .locals 1

    .line 196
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->keycode:I

    return v0
.end method

.method public getMetaState()I
    .locals 1

    .line 188
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->metaState:I

    return v0
.end method

.method public getOn()Z
    .locals 1

    .line 252
    iget-boolean v0, p0, Lcom/android/helper/control/ControlMessage;->on:Z

    return v0
.end method

.method public getPaste()Z
    .locals 1

    .line 232
    iget-boolean v0, p0, Lcom/android/helper/control/ControlMessage;->paste:Z

    return v0
.end method

.method public getPointerId()J
    .locals 2

    .line 208
    iget-wide v0, p0, Lcom/android/helper/control/ControlMessage;->pointerId:J

    return-wide v0
.end method

.method public getPosition()Lcom/android/helper/device/Position;
    .locals 1

    .line 216
    iget-object v0, p0, Lcom/android/helper/control/ControlMessage;->position:Lcom/android/helper/device/Position;

    return-object v0
.end method

.method public getPressure()F
    .locals 1

    .line 212
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->pressure:F

    return v0
.end method

.method public getProductId()I
    .locals 1

    .line 260
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->productId:I

    return v0
.end method

.method public getRepeat()I
    .locals 1

    .line 236
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->repeat:I

    return v0
.end method

.method public getSequence()J
    .locals 2

    .line 240
    iget-wide v0, p0, Lcom/android/helper/control/ControlMessage;->sequence:J

    return-wide v0
.end method

.method public getText()Ljava/lang/String;
    .locals 1

    .line 184
    iget-object v0, p0, Lcom/android/helper/control/ControlMessage;->text:Ljava/lang/String;

    return-object v0
.end method

.method public getType()I
    .locals 1

    .line 180
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->type:I

    return v0
.end method

.method public getVScroll()F
    .locals 1

    .line 224
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->vScroll:F

    return v0
.end method

.method public getVendorId()I
    .locals 1

    .line 256
    iget v0, p0, Lcom/android/helper/control/ControlMessage;->vendorId:I

    return v0
.end method
