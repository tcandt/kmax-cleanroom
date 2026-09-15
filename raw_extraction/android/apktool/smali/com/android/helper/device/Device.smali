.class public final Lcom/android/helper/device/Device;
.super Ljava/lang/Object;
.source "Device.java"


# static fields
.field static final synthetic $assertionsDisabled:Z = false

.field public static final DISPLAY_ID_NONE:I = -0x1

.field public static final INJECT_MODE_ASYNC:I = 0x0

.field public static final INJECT_MODE_WAIT_FOR_FINISH:I = 0x2

.field public static final INJECT_MODE_WAIT_FOR_RESULT:I = 0x1

.field public static final POWER_MODE_NORMAL:I = 0x2

.field public static final POWER_MODE_OFF:I = 0x0

.field private static final USE_ANDROID_15_DISPLAY_POWER:Z = false


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method private constructor <init>()V
    .locals 0

    .line 47
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static collapsePanels()V
    .locals 1

    .line 98
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getStatusBarManager()Lcom/android/helper/wrappers/StatusBarManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/wrappers/StatusBarManager;->collapsePanels()V

    return-void
.end method

.method public static expandNotificationPanel()V
    .locals 1

    .line 90
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getStatusBarManager()Lcom/android/helper/wrappers/StatusBarManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/wrappers/StatusBarManager;->expandNotificationsPanel()V

    return-void
.end method

.method public static expandSettingsPanel()V
    .locals 1

    .line 94
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getStatusBarManager()Lcom/android/helper/wrappers/StatusBarManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/wrappers/StatusBarManager;->expandSettingsPanel()V

    return-void
.end method

.method public static findByName(Ljava/lang/String;)Ljava/util/List;
    .locals 7
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            ")",
            "Ljava/util/List<",
            "Lcom/android/helper/device/DeviceApp;",
            ">;"
        }
    .end annotation

    .line 276
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 277
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    move-result-object v1

    invoke-virtual {p0, v1}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object p0

    .line 279
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v1

    invoke-virtual {v1}, Lcom/android/helper/FakeContext;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v1

    .line 280
    invoke-static {v1}, Lcom/android/helper/device/Device;->getLaunchableApps(Landroid/content/pm/PackageManager;)Ljava/util/List;

    move-result-object v2

    invoke-interface {v2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v2

    :cond_0
    :goto_0
    invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z

    move-result v3

    if-eqz v3, :cond_2

    invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Landroid/content/pm/ApplicationInfo;

    .line 281
    invoke-virtual {v1, v3}, Landroid/content/pm/PackageManager;->getApplicationLabel(Landroid/content/pm/ApplicationInfo;)Ljava/lang/CharSequence;

    move-result-object v4

    invoke-interface {v4}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;

    move-result-object v4

    .line 282
    invoke-static {}, Ljava/util/Locale;->getDefault()Ljava/util/Locale;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v5, p0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v5

    if-eqz v5, :cond_0

    .line 283
    iget v5, v3, Landroid/content/pm/ApplicationInfo;->flags:I

    const/4 v6, 0x1

    and-int/2addr v5, v6

    if-eqz v5, :cond_1

    goto :goto_1

    :cond_1
    const/4 v6, 0x0

    .line 284
    :goto_1
    new-instance v5, Lcom/android/helper/device/DeviceApp;

    iget-object v3, v3, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    invoke-direct {v5, v3, v4, v6}, Lcom/android/helper/device/DeviceApp;-><init>(Ljava/lang/String;Ljava/lang/String;Z)V

    invoke-interface {v0, v5}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    goto :goto_0

    :cond_2
    return-object v0
.end method

.method public static findByPackageName(Ljava/lang/String;)Lcom/android/helper/device/DeviceApp;
    .locals 4

    .line 263
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/FakeContext;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v0

    const/16 v1, 0x80

    .line 265
    invoke-virtual {v0, v1}, Landroid/content/pm/PackageManager;->getInstalledApplications(I)Ljava/util/List;

    move-result-object v1

    invoke-interface {v1}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v1

    :cond_0
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    move-result v2

    if-eqz v2, :cond_1

    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Landroid/content/pm/ApplicationInfo;

    .line 266
    iget-object v3, v2, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    invoke-virtual {p0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_0

    .line 267
    invoke-static {v0, v2}, Lcom/android/helper/device/Device;->toApp(Landroid/content/pm/PackageManager;Landroid/content/pm/ApplicationInfo;)Lcom/android/helper/device/DeviceApp;

    move-result-object p0

    return-object p0

    :cond_1
    const/4 p0, 0x0

    return-object p0
.end method

.method public static getClipboardText()Ljava/lang/String;
    .locals 2

    .line 102
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getClipboardManager()Lcom/android/helper/wrappers/ClipboardManager;

    move-result-object v0

    const/4 v1, 0x0

    if-nez v0, :cond_0

    return-object v1

    .line 106
    :cond_0
    invoke-virtual {v0}, Lcom/android/helper/wrappers/ClipboardManager;->getText()Ljava/lang/CharSequence;

    move-result-object v0

    if-nez v0, :cond_1

    return-object v1

    .line 110
    :cond_1
    invoke-interface {v0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private static getCurrentRotation(I)I
    .locals 1

    if-nez p0, :cond_0

    .line 217
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object p0

    invoke-virtual {p0}, Lcom/android/helper/wrappers/WindowManager;->getRotation()I

    move-result p0

    return p0

    .line 220
    :cond_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getDisplayManager()Lcom/android/helper/wrappers/DisplayManager;

    move-result-object v0

    invoke-virtual {v0, p0}, Lcom/android/helper/wrappers/DisplayManager;->getDisplayInfo(I)Lcom/android/helper/device/DisplayInfo;

    move-result-object p0

    .line 221
    invoke-virtual {p0}, Lcom/android/helper/device/DisplayInfo;->getRotation()I

    move-result p0

    return p0
.end method

.method public static getDeviceName()Ljava/lang/String;
    .locals 1

    .line 52
    sget-object v0, Landroid/os/Build;->MODEL:Ljava/lang/String;

    return-object v0
.end method

.method public static getLaunchIntent(Landroid/content/pm/PackageManager;Ljava/lang/String;)Landroid/content/Intent;
    .locals 1

    .line 247
    invoke-virtual {p0, p1}, Landroid/content/pm/PackageManager;->getLaunchIntentForPackage(Ljava/lang/String;)Landroid/content/Intent;

    move-result-object v0

    if-eqz v0, :cond_0

    return-object v0

    .line 252
    :cond_0
    invoke-virtual {p0, p1}, Landroid/content/pm/PackageManager;->getLeanbackLaunchIntentForPackage(Ljava/lang/String;)Landroid/content/Intent;

    move-result-object p0

    return-object p0
.end method

.method private static getLaunchableApps(Landroid/content/pm/PackageManager;)Ljava/util/List;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/content/pm/PackageManager;",
            ")",
            "Ljava/util/List<",
            "Landroid/content/pm/ApplicationInfo;",
            ">;"
        }
    .end annotation

    .line 236
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    const/16 v1, 0x80

    .line 237
    invoke-virtual {p0, v1}, Landroid/content/pm/PackageManager;->getInstalledApplications(I)Ljava/util/List;

    move-result-object v1

    invoke-interface {v1}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v1

    :cond_0
    :goto_0
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z

    move-result v2

    if-eqz v2, :cond_1

    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v2

    check-cast v2, Landroid/content/pm/ApplicationInfo;

    .line 238
    iget-boolean v3, v2, Landroid/content/pm/ApplicationInfo;->enabled:Z

    if-eqz v3, :cond_0

    iget-object v3, v2, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    invoke-static {p0, v3}, Lcom/android/helper/device/Device;->getLaunchIntent(Landroid/content/pm/PackageManager;Ljava/lang/String;)Landroid/content/Intent;

    move-result-object v3

    if-eqz v3, :cond_0

    .line 239
    invoke-interface {v0, v2}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    goto :goto_0

    :cond_1
    return-object v0
.end method

.method public static injectEvent(Landroid/view/InputEvent;II)Z
    .locals 1

    .line 61
    invoke-static {p1}, Lcom/android/helper/device/Device;->supportsInputEvents(I)Z

    move-result v0

    if-eqz v0, :cond_1

    if-eqz p1, :cond_0

    .line 65
    invoke-static {p0, p1}, Lcom/android/helper/wrappers/InputManager;->setDisplayId(Landroid/view/InputEvent;I)Z

    move-result p1

    if-nez p1, :cond_0

    const/4 p0, 0x0

    return p0

    .line 69
    :cond_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getInputManager()Lcom/android/helper/wrappers/InputManager;

    move-result-object p1

    invoke-virtual {p1, p0, p2}, Lcom/android/helper/wrappers/InputManager;->injectInputEvent(Landroid/view/InputEvent;I)Z

    move-result p0

    return p0

    .line 62
    :cond_1
    new-instance p0, Ljava/lang/AssertionError;

    const-string p1, "Could not inject input event if !supportsInputEvents()"

    invoke-direct {p0, p1}, Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V

    throw p0
.end method

.method public static injectKeyEvent(IIIIII)Z
    .locals 13

    .line 73
    invoke-static {}, Landroid/os/SystemClock;->uptimeMillis()J

    move-result-wide v1

    .line 74
    new-instance v0, Landroid/view/KeyEvent;

    const/4 v11, 0x0

    const/16 v12, 0x101

    const/4 v9, -0x1

    const/4 v10, 0x0

    move-wide v3, v1

    move v5, p0

    move v6, p1

    move v7, p2

    move/from16 v8, p3

    invoke-direct/range {v0 .. v12}, Landroid/view/KeyEvent;-><init>(JJIIIIIIII)V

    move/from16 p0, p4

    move/from16 p1, p5

    .line 76
    invoke-static {v0, p0, p1}, Lcom/android/helper/device/Device;->injectEvent(Landroid/view/InputEvent;II)Z

    move-result p0

    return p0
.end method

.method public static isScreenOn(I)Z
    .locals 1

    .line 86
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getPowerManager()Lcom/android/helper/wrappers/PowerManager;

    move-result-object v0

    invoke-virtual {v0, p0}, Lcom/android/helper/wrappers/PowerManager;->isScreenOn(I)Z

    move-result p0

    return p0
.end method

.method public static listApps()Ljava/util/List;
    .locals 4
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()",
            "Ljava/util/List<",
            "Lcom/android/helper/device/DeviceApp;",
            ">;"
        }
    .end annotation

    .line 225
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    .line 226
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v1

    invoke-virtual {v1}, Lcom/android/helper/FakeContext;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v1

    .line 227
    invoke-static {v1}, Lcom/android/helper/device/Device;->getLaunchableApps(Landroid/content/pm/PackageManager;)Ljava/util/List;

    move-result-object v2

    invoke-interface {v2}, Ljava/util/List;->iterator()Ljava/util/Iterator;

    move-result-object v2

    :goto_0
    invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z

    move-result v3

    if-eqz v3, :cond_0

    invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Landroid/content/pm/ApplicationInfo;

    .line 228
    invoke-static {v1, v3}, Lcom/android/helper/device/Device;->toApp(Landroid/content/pm/PackageManager;Landroid/content/pm/ApplicationInfo;)Lcom/android/helper/device/DeviceApp;

    move-result-object v3

    invoke-interface {v0, v3}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    goto :goto_0

    :cond_0
    return-object v0
.end method

.method public static powerOffScreen(I)Z
    .locals 2

    .line 184
    invoke-static {p0}, Lcom/android/helper/device/Device;->isScreenOn(I)Z

    move-result v0

    if-nez v0, :cond_0

    const/4 p0, 0x1

    return p0

    :cond_0
    const/16 v0, 0x1a

    const/4 v1, 0x0

    .line 187
    invoke-static {v0, p0, v1}, Lcom/android/helper/device/Device;->pressReleaseKeycode(III)Z

    move-result p0

    return p0
.end method

.method public static pressReleaseKeycode(III)Z
    .locals 6

    const/4 v2, 0x0

    const/4 v3, 0x0

    const/4 v0, 0x0

    move v1, p0

    move v4, p1

    move v5, p2

    .line 80
    invoke-static/range {v0 .. v5}, Lcom/android/helper/device/Device;->injectKeyEvent(IIIIII)Z

    move-result p0

    if-eqz p0, :cond_0

    const/4 v2, 0x0

    const/4 v3, 0x0

    const/4 v0, 0x1

    .line 81
    invoke-static/range {v0 .. v5}, Lcom/android/helper/device/Device;->injectKeyEvent(IIIIII)Z

    move-result p0

    if-eqz p0, :cond_0

    const/4 p0, 0x1

    return p0

    :cond_0
    const/4 p0, 0x0

    return p0
.end method

.method public static rotateDevice(I)V
    .locals 5

    .line 196
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getWindowManager()Lcom/android/helper/wrappers/WindowManager;

    move-result-object v0

    .line 198
    invoke-virtual {v0, p0}, Lcom/android/helper/wrappers/WindowManager;->isRotationFrozen(I)Z

    move-result v1

    .line 200
    invoke-static {p0}, Lcom/android/helper/device/Device;->getCurrentRotation(I)I

    move-result v2

    and-int/lit8 v2, v2, 0x1

    xor-int/lit8 v2, v2, 0x1

    if-nez v2, :cond_0

    .line 202
    const-string v3, "portrait"

    goto :goto_0

    :cond_0
    const-string v3, "landscape"

    .line 204
    :goto_0
    const-string v4, "Device rotation requested: "

    invoke-virtual {v4, v3}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    invoke-static {v3}, Lcom/android/helper/util/Ln;->i(Ljava/lang/String;)V

    .line 205
    invoke-virtual {v0, p0, v2}, Lcom/android/helper/wrappers/WindowManager;->freezeRotation(II)V

    if-nez v1, :cond_1

    .line 209
    invoke-virtual {v0, p0}, Lcom/android/helper/wrappers/WindowManager;->thawRotation(I)V

    :cond_1
    return-void
.end method

.method public static setClipboardText(Ljava/lang/String;)Z
    .locals 3

    .line 114
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getClipboardManager()Lcom/android/helper/wrappers/ClipboardManager;

    move-result-object v0

    const/4 v1, 0x0

    if-nez v0, :cond_0

    return v1

    .line 119
    :cond_0
    invoke-static {}, Lcom/android/helper/device/Device;->getClipboardText()Ljava/lang/String;

    move-result-object v2

    if-eqz v2, :cond_1

    .line 120
    invoke-virtual {v2, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_1

    return v1

    .line 128
    :cond_1
    invoke-virtual {v0, p0}, Lcom/android/helper/wrappers/ClipboardManager;->setText(Ljava/lang/CharSequence;)Z

    move-result p0

    return p0
.end method

.method public static setDisplayPower(IZ)Z
    .locals 6

    .line 138
    sget p0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v0, 0x1d

    const/4 v1, 0x1

    const/4 v2, 0x0

    if-lt p0, v0, :cond_0

    const/4 p0, 0x1

    goto :goto_0

    :cond_0
    const/4 p0, 0x0

    :goto_0
    const/16 v0, 0x22

    if-eqz p0, :cond_1

    .line 140
    sget v3, Landroid/os/Build$VERSION;->SDK_INT:I

    if-lt v3, v0, :cond_1

    sget-object v3, Landroid/os/Build;->BRAND:Ljava/lang/String;

    const-string v4, "honor"

    .line 142
    invoke-virtual {v3, v4}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z

    move-result v3

    if-eqz v3, :cond_1

    .line 143
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->hasGetBuildInDisplayMethod()Z

    move-result v3

    if-eqz v3, :cond_1

    const/4 p0, 0x0

    :cond_1
    if-eqz p1, :cond_2

    const/4 p1, 0x2

    goto :goto_1

    :cond_2
    const/4 p1, 0x0

    :goto_1
    if-eqz p0, :cond_8

    .line 153
    sget p0, Landroid/os/Build$VERSION;->SDK_INT:I

    if-lt p0, v0, :cond_3

    .line 154
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->hasGetPhysicalDisplayIdsMethod()Z

    move-result p0

    if-nez p0, :cond_3

    const/4 p0, 0x1

    goto :goto_2

    :cond_3
    const/4 p0, 0x0

    :goto_2
    if-eqz p0, :cond_4

    .line 157
    invoke-static {}, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayIds()[J

    move-result-object v0

    goto :goto_3

    :cond_4
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayIds()[J

    move-result-object v0

    :goto_3
    if-nez v0, :cond_5

    .line 159
    const-string p0, "Could not get physical display ids"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return v2

    .line 164
    :cond_5
    array-length v3, v0

    :goto_4
    if-ge v2, v3, :cond_7

    aget-wide v4, v0, v2

    if-eqz p0, :cond_6

    .line 165
    invoke-static {v4, v5}, Lcom/android/helper/wrappers/DisplayControl;->getPhysicalDisplayToken(J)Landroid/os/IBinder;

    move-result-object v4

    goto :goto_5

    .line 166
    :cond_6
    invoke-static {v4, v5}, Lcom/android/helper/wrappers/SurfaceControl;->getPhysicalDisplayToken(J)Landroid/os/IBinder;

    move-result-object v4

    .line 167
    :goto_5
    invoke-static {v4, p1}, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayPowerMode(Landroid/os/IBinder;I)Z

    move-result v4

    and-int/2addr v1, v4

    add-int/lit8 v2, v2, 0x1

    goto :goto_4

    :cond_7
    return v1

    .line 173
    :cond_8
    invoke-static {}, Lcom/android/helper/wrappers/SurfaceControl;->getBuiltInDisplay()Landroid/os/IBinder;

    move-result-object p0

    if-nez p0, :cond_9

    .line 175
    const-string p0, "Could not get built-in display"

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return v2

    .line 178
    :cond_9
    invoke-static {p0, p1}, Lcom/android/helper/wrappers/SurfaceControl;->setDisplayPowerMode(Landroid/os/IBinder;I)Z

    move-result p0

    return p0
.end method

.method public static startApp(Ljava/lang/String;IZ)V
    .locals 3

    .line 292
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v0

    invoke-virtual {v0}, Lcom/android/helper/FakeContext;->getPackageManager()Landroid/content/pm/PackageManager;

    move-result-object v0

    .line 294
    invoke-static {v0, p0}, Lcom/android/helper/device/Device;->getLaunchIntent(Landroid/content/pm/PackageManager;Ljava/lang/String;)Landroid/content/Intent;

    move-result-object v0

    if-nez v0, :cond_0

    .line 296
    new-instance p1, Ljava/lang/StringBuilder;

    const-string p2, "Cannot create launch intent for app "

    invoke-direct {p1, p2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    :cond_0
    const/high16 v1, 0x10000000

    .line 300
    invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;

    .line 303
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1a

    if-lt v1, v2, :cond_1

    .line 304
    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Landroid/app/ActivityOptions;

    move-result-object v1

    .line 305
    invoke-static {v1, p1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/app/ActivityOptions;I)Landroid/app/ActivityOptions;

    .line 306
    invoke-virtual {v1}, Landroid/app/ActivityOptions;->toBundle()Landroid/os/Bundle;

    move-result-object p1

    goto :goto_0

    :cond_1
    const/4 p1, 0x0

    .line 309
    :goto_0
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object v1

    if-eqz p2, :cond_2

    .line 311
    invoke-virtual {v1, p0}, Lcom/android/helper/wrappers/ActivityManager;->forceStopPackage(Ljava/lang/String;)V

    .line 313
    :cond_2
    invoke-virtual {v1, v0, p1}, Lcom/android/helper/wrappers/ActivityManager;->startActivity(Landroid/content/Intent;Landroid/os/Bundle;)I

    return-void
.end method

.method public static supportsInputEvents(I)Z
    .locals 1

    if-eqz p0, :cond_1

    .line 57
    sget p0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v0, 0x1d

    if-lt p0, v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 p0, 0x0

    return p0

    :cond_1
    :goto_0
    const/4 p0, 0x1

    return p0
.end method

.method private static toApp(Landroid/content/pm/PackageManager;Landroid/content/pm/ApplicationInfo;)Lcom/android/helper/device/DeviceApp;
    .locals 2

    .line 256
    invoke-virtual {p0, p1}, Landroid/content/pm/PackageManager;->getApplicationLabel(Landroid/content/pm/ApplicationInfo;)Ljava/lang/CharSequence;

    move-result-object p0

    invoke-interface {p0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;

    move-result-object p0

    .line 257
    iget v0, p1, Landroid/content/pm/ApplicationInfo;->flags:I

    const/4 v1, 0x1

    and-int/2addr v0, v1

    if-eqz v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v1, 0x0

    .line 258
    :goto_0
    new-instance v0, Lcom/android/helper/device/DeviceApp;

    iget-object p1, p1, Landroid/content/pm/ApplicationInfo;->packageName:Ljava/lang/String;

    invoke-direct {v0, p1, p0, v1}, Lcom/android/helper/device/DeviceApp;-><init>(Ljava/lang/String;Ljava/lang/String;Z)V

    return-object v0
.end method
