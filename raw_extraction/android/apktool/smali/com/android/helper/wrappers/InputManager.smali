.class public final Lcom/android/helper/wrappers/InputManager;
.super Ljava/lang/Object;
.source "InputManager.java"


# static fields
.field public static final INJECT_INPUT_EVENT_MODE_ASYNC:I = 0x0

.field public static final INJECT_INPUT_EVENT_MODE_WAIT_FOR_FINISH:I = 0x2

.field public static final INJECT_INPUT_EVENT_MODE_WAIT_FOR_RESULT:I = 0x1

.field private static addUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

.field private static injectInputEventMethod:Ljava/lang/reflect/Method;

.field private static removeUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

.field private static setActionButtonMethod:Ljava/lang/reflect/Method;

.field private static setDisplayIdMethod:Ljava/lang/reflect/Method;


# instance fields
.field private lastPermissionLogDate:J

.field private final manager:Landroid/hardware/input/InputManager;


# direct methods
.method private constructor <init>(Landroid/hardware/input/InputManager;)V
    .locals 0

    .line 37
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 38
    iput-object p1, p0, Lcom/android/helper/wrappers/InputManager;->manager:Landroid/hardware/input/InputManager;

    return-void
.end method

.method static create()Lcom/android/helper/wrappers/InputManager;
    .locals 2

    .line 32
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v0

    const-string v1, "input"

    .line 33
    invoke-virtual {v0, v1}, Lcom/android/helper/FakeContext;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/hardware/input/InputManager;

    .line 34
    new-instance v1, Lcom/android/helper/wrappers/InputManager;

    invoke-direct {v1, v0}, Lcom/android/helper/wrappers/InputManager;-><init>(Landroid/hardware/input/InputManager;)V

    return-object v1
.end method

.method private static getAddUniqueIdAssociationByPortMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 112
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->addUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 113
    const-class v0, Landroid/hardware/input/InputManager;

    const/4 v1, 0x2

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Ljava/lang/String;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "addUniqueIdAssociationByPort"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/InputManager;->addUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

    .line 116
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->addUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getInjectInputEventMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 42
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->injectInputEventMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 43
    const-class v0, Landroid/hardware/input/InputManager;

    const/4 v1, 0x2

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Landroid/view/InputEvent;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x1

    aput-object v2, v1, v3

    const-string v2, "injectInputEvent"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/InputManager;->injectInputEventMethod:Ljava/lang/reflect/Method;

    .line 45
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->injectInputEventMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getRemoveUniqueIdAssociationByPortMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 130
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->removeUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 131
    const-class v0, Landroid/hardware/input/InputManager;

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    const-class v2, Ljava/lang/String;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "removeUniqueIdAssociationByPort"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/InputManager;->removeUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

    .line 134
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->removeUniqueIdAssociationByPortMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getSetActionButtonMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 94
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->setActionButtonMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 95
    const-class v0, Landroid/view/MotionEvent;

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "setActionButton"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/InputManager;->setActionButtonMethod:Ljava/lang/reflect/Method;

    .line 97
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->setActionButtonMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getSetDisplayIdMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 76
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->setDisplayIdMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 77
    const-class v0, Landroid/view/InputEvent;

    const/4 v1, 0x1

    new-array v1, v1, [Ljava/lang/Class;

    sget-object v2, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v3, 0x0

    aput-object v2, v1, v3

    const-string v2, "setDisplayId"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    sput-object v0, Lcom/android/helper/wrappers/InputManager;->setDisplayIdMethod:Ljava/lang/reflect/Method;

    .line 79
    :cond_0
    sget-object v0, Lcom/android/helper/wrappers/InputManager;->setDisplayIdMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method public static setActionButton(Landroid/view/MotionEvent;I)Z
    .locals 4

    const/4 v0, 0x0

    .line 102
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/InputManager;->getSetActionButtonMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 103
    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    const/4 v2, 0x1

    new-array v3, v2, [Ljava/lang/Object;

    aput-object p1, v3, v0

    invoke-virtual {v1, p0, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return v2

    :catch_0
    move-exception p0

    .line 106
    const-string p1, "Cannot set action button on MotionEvent"

    invoke-static {p1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method

.method public static setDisplayId(Landroid/view/InputEvent;I)Z
    .locals 4

    const/4 v0, 0x0

    .line 84
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/InputManager;->getSetDisplayIdMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 85
    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    const/4 v2, 0x1

    new-array v3, v2, [Ljava/lang/Object;

    aput-object p1, v3, v0

    invoke-virtual {v1, p0, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return v2

    :catch_0
    move-exception p0

    .line 88
    const-string p1, "Cannot associate a display id to the input event"

    invoke-static {p1, p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method


# virtual methods
.method public addUniqueIdAssociationByPort(Ljava/lang/String;Ljava/lang/String;)V
    .locals 4

    .line 122
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/InputManager;->getAddUniqueIdAssociationByPortMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 123
    iget-object v1, p0, Lcom/android/helper/wrappers/InputManager;->manager:Landroid/hardware/input/InputManager;

    const/4 v2, 0x2

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    const/4 p1, 0x1

    aput-object p2, v2, p1

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 125
    const-string p2, "Cannot add unique id association by port"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public injectInputEvent(Landroid/view/InputEvent;I)Z
    .locals 7

    const/4 v0, 0x0

    .line 50
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/InputManager;->getInjectInputEventMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 51
    iget-object v2, p0, Lcom/android/helper/wrappers/InputManager;->manager:Landroid/hardware/input/InputManager;

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p2

    const/4 v3, 0x2

    new-array v3, v3, [Ljava/lang/Object;

    aput-object p1, v3, v0

    const/4 p1, 0x1

    aput-object p2, v3, p1

    invoke-virtual {v1, v2, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Boolean;

    invoke-virtual {p1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result p1
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return p1

    :catch_0
    move-exception p1

    .line 53
    instance-of p2, p1, Ljava/lang/reflect/InvocationTargetException;

    if-eqz p2, :cond_1

    .line 54
    invoke-virtual {p1}, Ljava/lang/ReflectiveOperationException;->getCause()Ljava/lang/Throwable;

    move-result-object p2

    .line 55
    instance-of p2, p2, Ljava/lang/SecurityException;

    if-eqz p2, :cond_1

    .line 56
    invoke-virtual {p1}, Ljava/lang/ReflectiveOperationException;->getCause()Ljava/lang/Throwable;

    move-result-object p2

    invoke-virtual {p2}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object p2

    if-eqz p2, :cond_1

    .line 57
    const-string v1, "INJECT_EVENTS permission"

    invoke-virtual {p2, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v1

    if-eqz v1, :cond_1

    .line 59
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v1

    .line 60
    iget-wide v3, p0, Lcom/android/helper/wrappers/InputManager;->lastPermissionLogDate:J

    const-wide/16 v5, 0xbb8

    sub-long v5, v1, v5

    cmp-long p1, v3, v5

    if-gtz p1, :cond_0

    .line 61
    invoke-static {p2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 62
    const-string p1, "Make sure you have enabled \"USB debugging (Security Settings)\" and then rebooted your device."

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 63
    iput-wide v1, p0, Lcom/android/helper/wrappers/InputManager;->lastPermissionLogDate:J

    :cond_0
    return v0

    .line 70
    :cond_1
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method

.method public removeUniqueIdAssociationByPort(Ljava/lang/String;)V
    .locals 4

    .line 140
    :try_start_0
    invoke-static {}, Lcom/android/helper/wrappers/InputManager;->getRemoveUniqueIdAssociationByPortMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 141
    iget-object v1, p0, Lcom/android/helper/wrappers/InputManager;->manager:Landroid/hardware/input/InputManager;

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 143
    const-string v0, "Cannot remove unique id association by port"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method
