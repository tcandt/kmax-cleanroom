.class public final Lcom/android/helper/wrappers/WindowManager;
.super Ljava/lang/Object;
.source "WindowManager.java"


# static fields
.field public static final DISPLAY_IME_POLICY_FALLBACK_DISPLAY:I = 0x1

.field public static final DISPLAY_IME_POLICY_HIDE:I = 0x2

.field public static final DISPLAY_IME_POLICY_LOCAL:I


# instance fields
.field private freezeDisplayRotationMethod:Ljava/lang/reflect/Method;

.field private freezeDisplayRotationMethodVersion:I

.field private getDisplayImePolicyMethod:Ljava/lang/reflect/Method;

.field private getRotationMethod:Ljava/lang/reflect/Method;

.field private isDisplayRotationFrozenMethod:Ljava/lang/reflect/Method;

.field private isDisplayRotationFrozenMethodVersion:I

.field private final manager:Landroid/os/IInterface;

.field private setDisplayImePolicyMethod:Ljava/lang/reflect/Method;

.field private thawDisplayRotationMethod:Ljava/lang/reflect/Method;

.field private thawDisplayRotationMethodVersion:I


# direct methods
.method private constructor <init>(Landroid/os/IInterface;)V
    .locals 0

    .line 41
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 42
    iput-object p1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    return-void
.end method

.method static create()Lcom/android/helper/wrappers/WindowManager;
    .locals 2

    .line 37
    const-string v0, "window"

    const-string v1, "android.view.IWindowManager"

    invoke-static {v0, v1}, Lcom/android/helper/wrappers/ServiceManager;->getService(Ljava/lang/String;Ljava/lang/String;)Landroid/os/IInterface;

    move-result-object v0

    .line 38
    new-instance v1, Lcom/android/helper/wrappers/WindowManager;

    invoke-direct {v1, v0}, Lcom/android/helper/wrappers/WindowManager;-><init>(Landroid/os/IInterface;)V

    return-object v1
.end method

.method private getFreezeDisplayRotationMethod()Ljava/lang/reflect/Method;
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 61
    const-string v0, "freezeDisplayRotation"

    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethod:Ljava/lang/reflect/Method;

    if-nez v1, :cond_0

    const/4 v1, 0x2

    const/4 v2, 0x0

    const/4 v3, 0x1

    .line 65
    :try_start_0
    iget-object v4, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    const/4 v5, 0x3

    new-array v5, v5, [Ljava/lang/Class;

    sget-object v6, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v6, v5, v2

    aput-object v6, v5, v3

    const-class v6, Ljava/lang/String;

    aput-object v6, v5, v1

    invoke-virtual {v4, v0, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    iput-object v4, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethod:Ljava/lang/reflect/Method;

    .line 66
    iput v2, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethodVersion:I
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 71
    :catch_0
    :try_start_1
    iget-object v4, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    new-array v5, v1, [Ljava/lang/Class;

    sget-object v6, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v6, v5, v2

    aput-object v6, v5, v3

    invoke-virtual {v4, v0, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethod:Ljava/lang/reflect/Method;

    .line 72
    iput v3, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethodVersion:I
    :try_end_1
    .catch Ljava/lang/NoSuchMethodException; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_0

    .line 74
    :catch_1
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v3, v3, [Ljava/lang/Class;

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v4, v3, v2

    const-string v2, "freezeRotation"

    invoke-virtual {v0, v2, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethod:Ljava/lang/reflect/Method;

    .line 75
    iput v1, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethodVersion:I

    .line 79
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getGetDisplayImePolicyMethod()Ljava/lang/reflect/Method;
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 215
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_1

    .line 216
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1f

    const/4 v2, 0x0

    const/4 v3, 0x1

    if-lt v0, v1, :cond_0

    .line 217
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v1, v3, [Ljava/lang/Class;

    sget-object v3, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v3, v1, v2

    const-string v2, "getDisplayImePolicy"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    goto :goto_0

    .line 219
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v1, v3, [Ljava/lang/Class;

    sget-object v3, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v3, v1, v2

    const-string v2, "shouldShowIme"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    .line 222
    :cond_1
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getGetRotationMethod()Ljava/lang/reflect/Method;
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 46
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getRotationMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    .line 47
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x0

    .line 51
    :try_start_0
    const-string v2, "getDefaultDisplayRotation"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v2

    iput-object v2, p0, Lcom/android/helper/wrappers/WindowManager;->getRotationMethod:Ljava/lang/reflect/Method;
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 54
    :catch_0
    const-string v2, "getRotation"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getRotationMethod:Ljava/lang/reflect/Method;

    .line 57
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->getRotationMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getIsDisplayRotationFrozenMethod()Ljava/lang/reflect/Method;
    .locals 6
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 83
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_0

    const/4 v0, 0x1

    .line 87
    :try_start_0
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const-string v2, "isDisplayRotationFrozen"

    new-array v3, v0, [Ljava/lang/Class;

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    invoke-virtual {v1, v2, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethod:Ljava/lang/reflect/Method;

    .line 88
    iput v5, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethodVersion:I
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 90
    :catch_0
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const-string v2, "isRotationFrozen"

    const/4 v3, 0x0

    invoke-virtual {v1, v2, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethod:Ljava/lang/reflect/Method;

    .line 91
    iput v0, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethodVersion:I

    .line 94
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getSetDisplayImePolicyMethod()Ljava/lang/reflect/Method;
    .locals 5
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 242
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_1

    .line 243
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1f

    const/4 v2, 0x1

    const/4 v3, 0x0

    const/4 v4, 0x2

    if-lt v0, v1, :cond_0

    .line 244
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v1, v4, [Ljava/lang/Class;

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v4, v1, v3

    aput-object v4, v1, v2

    const-string v2, "setDisplayImePolicy"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    goto :goto_0

    .line 246
    :cond_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v1, v4, [Ljava/lang/Class;

    sget-object v4, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v4, v1, v3

    sget-object v3, Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;

    aput-object v3, v1, v2

    const-string v2, "setShouldShowIme"

    invoke-virtual {v0, v2, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    .line 249
    :cond_1
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->setDisplayImePolicyMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private getThawDisplayRotationMethod()Ljava/lang/reflect/Method;
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 98
    const-string v0, "thawDisplayRotation"

    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethod:Ljava/lang/reflect/Method;

    if-nez v1, :cond_0

    const/4 v1, 0x2

    const/4 v2, 0x1

    const/4 v3, 0x0

    .line 102
    :try_start_0
    iget-object v4, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    new-array v5, v1, [Ljava/lang/Class;

    sget-object v6, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v6, v5, v3

    const-class v6, Ljava/lang/String;

    aput-object v6, v5, v2

    invoke-virtual {v4, v0, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v4

    iput-object v4, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethod:Ljava/lang/reflect/Method;

    .line 103
    iput v3, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethodVersion:I
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 108
    :catch_0
    :try_start_1
    iget-object v4, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v4}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    new-array v5, v2, [Ljava/lang/Class;

    sget-object v6, Ljava/lang/Integer;->TYPE:Ljava/lang/Class;

    aput-object v6, v5, v3

    invoke-virtual {v4, v0, v5}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethod:Ljava/lang/reflect/Method;

    .line 109
    iput v2, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethodVersion:I
    :try_end_1
    .catch Ljava/lang/NoSuchMethodException; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_0

    .line 111
    :catch_1
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const-string v2, "thawRotation"

    const/4 v3, 0x0

    invoke-virtual {v0, v2, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethod:Ljava/lang/reflect/Method;

    .line 112
    iput v1, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethodVersion:I

    .line 116
    :cond_0
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method


# virtual methods
.method public freezeRotation(II)V
    .locals 6

    .line 131
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/WindowManager;->getFreezeDisplayRotationMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 132
    iget v1, p0, Lcom/android/helper/wrappers/WindowManager;->freezeDisplayRotationMethodVersion:I

    const/4 v2, 0x2

    const/4 v3, 0x0

    const/4 v4, 0x1

    if-eqz v1, :cond_2

    if-eq v1, v4, :cond_1

    if-eqz p1, :cond_0

    .line 141
    const-string p1, "Secondary display rotation not supported on this device"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return-void

    .line 144
    :cond_0
    iget-object p1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p2

    new-array v1, v4, [Ljava/lang/Object;

    aput-object p2, v1, v3

    invoke-virtual {v0, p1, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 137
    :cond_1
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p2

    new-array v2, v2, [Ljava/lang/Object;

    aput-object p1, v2, v3

    aput-object p2, v2, v4

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 134
    :cond_2
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p2

    const/4 v5, 0x3

    new-array v5, v5, [Ljava/lang/Object;

    aput-object p1, v5, v3

    aput-object p2, v5, v4

    const-string p1, "scrcpy#freezeRotation"

    aput-object p1, v5, v2

    invoke-virtual {v0, v1, v5}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 148
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public getDisplayImePolicy(I)I
    .locals 5

    .line 228
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/WindowManager;->getGetDisplayImePolicyMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 229
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1f

    const/4 v3, 0x0

    const/4 v4, 0x1

    if-lt v1, v2, :cond_0

    .line 230
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    new-array v2, v4, [Ljava/lang/Object;

    aput-object p1, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Integer;

    invoke-virtual {p1}, Ljava/lang/Integer;->intValue()I

    move-result p1

    return p1

    .line 232
    :cond_0
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    new-array v2, v4, [Ljava/lang/Object;

    aput-object p1, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Boolean;

    invoke-virtual {p1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result p1
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    xor-int/2addr p1, v4

    return p1

    :catch_0
    move-exception p1

    .line 235
    const-string v0, "Could not invoke method"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    const/4 p1, -0x1

    return p1
.end method

.method public getRotation()I
    .locals 3

    .line 121
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/WindowManager;->getGetRotationMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 122
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/Integer;

    invoke-virtual {v0}, Ljava/lang/Integer;->intValue()I

    move-result v0
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return v0

    :catch_0
    move-exception v0

    .line 124
    const-string v1, "Could not invoke method"

    invoke-static {v1, v0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    const/4 v0, 0x0

    return v0
.end method

.method public isRotationFrozen(I)Z
    .locals 4

    const/4 v0, 0x0

    .line 154
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/WindowManager;->getIsDisplayRotationFrozenMethod()Ljava/lang/reflect/Method;

    move-result-object v1

    .line 155
    iget v2, p0, Lcom/android/helper/wrappers/WindowManager;->isDisplayRotationFrozenMethodVersion:I

    if-eqz v2, :cond_1

    if-eqz p1, :cond_0

    .line 160
    const-string p1, "Secondary display rotation not supported on this device"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return v0

    .line 163
    :cond_0
    iget-object p1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    const/4 v2, 0x0

    invoke-virtual {v1, p1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Boolean;

    invoke-virtual {p1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result p1

    return p1

    .line 157
    :cond_1
    iget-object v2, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    const/4 v3, 0x1

    new-array v3, v3, [Ljava/lang/Object;

    aput-object p1, v3, v0

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

    .line 166
    const-string v1, "Could not invoke method"

    invoke-static {v1, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return v0
.end method

.method public registerDisplayWindowListener(Landroid/view/IDisplayWindowListener;)[I
    .locals 6

    .line 197
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const-string v1, "registerDisplayWindowListener"

    const/4 v2, 0x1

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Landroid/view/IDisplayWindowListener;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    new-array v2, v2, [Ljava/lang/Object;

    aput-object p1, v2, v5

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, [I
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-object p1

    :catch_0
    move-exception p1

    .line 199
    const-string v0, "Could not register display window listener"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    const/4 p1, 0x0

    return-object p1
.end method

.method public setDisplayImePolicy(II)V
    .locals 6

    .line 255
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/WindowManager;->getSetDisplayImePolicyMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 256
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1f

    const/4 v3, 0x1

    const/4 v4, 0x0

    const/4 v5, 0x2

    if-lt v1, v2, :cond_0

    .line 257
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p2

    new-array v2, v5, [Ljava/lang/Object;

    aput-object p1, v2, v4

    aput-object p2, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    :cond_0
    if-eq p2, v5, :cond_2

    .line 259
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    if-nez p2, :cond_1

    const/4 p2, 0x1

    goto :goto_0

    :cond_1
    const/4 p2, 0x0

    :goto_0
    invoke-static {p2}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object p2

    new-array v2, v5, [Ljava/lang/Object;

    aput-object p1, v2, v4

    aput-object p2, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 261
    :cond_2
    const-string p1, "DISPLAY_IME_POLICY_HIDE is not supported before Android 12"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 264
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public thawRotation(I)V
    .locals 5

    .line 173
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/WindowManager;->getThawDisplayRotationMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 174
    iget v1, p0, Lcom/android/helper/wrappers/WindowManager;->thawDisplayRotationMethodVersion:I

    const/4 v2, 0x0

    const/4 v3, 0x1

    if-eqz v1, :cond_2

    if-eq v1, v3, :cond_1

    if-eqz p1, :cond_0

    .line 183
    const-string p1, "Secondary display rotation not supported on this device"

    invoke-static {p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return-void

    .line 186
    :cond_0
    iget-object p1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    const/4 v1, 0x0

    invoke-virtual {v0, p1, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 179
    :cond_1
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    new-array v3, v3, [Ljava/lang/Object;

    aput-object p1, v3, v2

    invoke-virtual {v0, v1, v3}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    return-void

    .line 176
    :cond_2
    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p1

    const/4 v4, 0x2

    new-array v4, v4, [Ljava/lang/Object;

    aput-object p1, v4, v2

    const-string p1, "scrcpy#thawRotation"

    aput-object p1, v4, v3

    invoke-virtual {v0, v1, v4}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 190
    const-string v0, "Could not invoke method"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public unregisterDisplayWindowListener(Landroid/view/IDisplayWindowListener;)V
    .locals 6

    .line 207
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const-string v1, "unregisterDisplayWindowListener"

    const/4 v2, 0x1

    new-array v3, v2, [Ljava/lang/Class;

    const-class v4, Landroid/view/IDisplayWindowListener;

    const/4 v5, 0x0

    aput-object v4, v3, v5

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iget-object v1, p0, Lcom/android/helper/wrappers/WindowManager;->manager:Landroid/os/IInterface;

    new-array v2, v2, [Ljava/lang/Object;

    aput-object p1, v2, v5

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception p1

    .line 209
    const-string v0, "Could not unregister display window listener"

    invoke-static {v0, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method
