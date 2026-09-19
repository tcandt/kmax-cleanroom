.class public final Lcom/android/helper/wrappers/ContentProvider;
.super Ljava/lang/Object;
.source "ContentProvider.java"

# interfaces
.implements Ljava/io/Closeable;


# static fields
.field private static final CALL_METHOD_GET_GLOBAL:Ljava/lang/String; = "GET_global"

.field private static final CALL_METHOD_GET_SECURE:Ljava/lang/String; = "GET_secure"

.field private static final CALL_METHOD_GET_SYSTEM:Ljava/lang/String; = "GET_system"

.field private static final CALL_METHOD_PUT_GLOBAL:Ljava/lang/String; = "PUT_global"

.field private static final CALL_METHOD_PUT_SECURE:Ljava/lang/String; = "PUT_secure"

.field private static final CALL_METHOD_PUT_SYSTEM:Ljava/lang/String; = "PUT_system"

.field private static final CALL_METHOD_USER_KEY:Ljava/lang/String; = "_user"

.field private static final NAME_VALUE_TABLE_VALUE:Ljava/lang/String; = "value"

.field public static final TABLE_GLOBAL:Ljava/lang/String; = "global"

.field public static final TABLE_SECURE:Ljava/lang/String; = "secure"

.field public static final TABLE_SYSTEM:Ljava/lang/String; = "system"


# instance fields
.field private callMethod:Ljava/lang/reflect/Method;

.field private callMethodVersion:I

.field private final manager:Lcom/android/helper/wrappers/ActivityManager;

.field private final name:Ljava/lang/String;

.field private final provider:Ljava/lang/Object;

.field private final token:Landroid/os/IBinder;


# direct methods
.method constructor <init>(Lcom/android/helper/wrappers/ActivityManager;Ljava/lang/Object;Ljava/lang/String;Landroid/os/IBinder;)V
    .locals 0

    .line 45
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 46
    iput-object p1, p0, Lcom/android/helper/wrappers/ContentProvider;->manager:Lcom/android/helper/wrappers/ActivityManager;

    .line 47
    iput-object p2, p0, Lcom/android/helper/wrappers/ContentProvider;->provider:Ljava/lang/Object;

    .line 48
    iput-object p3, p0, Lcom/android/helper/wrappers/ContentProvider;->name:Ljava/lang/String;

    .line 49
    iput-object p4, p0, Lcom/android/helper/wrappers/ContentProvider;->token:Landroid/os/IBinder;

    return-void
.end method

.method private call(Ljava/lang/String;Ljava/lang/String;Landroid/os/Bundle;)Landroid/os/Bundle;
    .locals 10
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/ReflectiveOperationException;
        }
    .end annotation

    .line 80
    :try_start_0
    invoke-direct {p0}, Lcom/android/helper/wrappers/ContentProvider;->getCallMethod()Ljava/lang/reflect/Method;

    move-result-object v0

    .line 83
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    const/16 v2, 0x1f

    const-string v3, "settings"

    const/4 v4, 0x5

    const/4 v5, 0x3

    const/4 v6, 0x0

    const/4 v7, 0x4

    const/4 v8, 0x2

    const/4 v9, 0x1

    if-lt v1, v2, :cond_0

    :try_start_1
    iget v1, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethodVersion:I

    if-nez v1, :cond_0

    .line 84
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v1

    invoke-virtual {v1}, Lcom/android/helper/FakeContext;->getAttributionSource()Landroid/content/AttributionSource;

    move-result-object v1

    new-array v2, v4, [Ljava/lang/Object;

    aput-object v1, v2, v6

    aput-object v3, v2, v9

    aput-object p1, v2, v8

    aput-object p2, v2, v5

    aput-object p3, v2, v7

    goto :goto_1

    .line 86
    :cond_0
    iget v1, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethodVersion:I
    :try_end_1
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_1 .. :try_end_1} :catch_0

    const-string v2, "com.android.shell"

    if-eq v1, v9, :cond_2

    if-eq v1, v8, :cond_1

    .line 94
    :try_start_2
    new-array v1, v7, [Ljava/lang/Object;

    aput-object v2, v1, v6

    aput-object p1, v1, v9

    aput-object p2, v1, v8

    aput-object p3, v1, v5

    :goto_0
    move-object v2, v1

    goto :goto_1

    .line 91
    :cond_1
    new-array v1, v4, [Ljava/lang/Object;

    aput-object v2, v1, v6

    aput-object v3, v1, v9

    aput-object p1, v1, v8

    aput-object p2, v1, v5

    aput-object p3, v1, v7

    goto :goto_0

    :cond_2
    const/4 v1, 0x6

    .line 88
    new-array v1, v1, [Ljava/lang/Object;

    aput-object v2, v1, v6

    const/4 v2, 0x0

    aput-object v2, v1, v9

    aput-object v3, v1, v8

    aput-object p1, v1, v5

    aput-object p2, v1, v7

    aput-object p3, v1, v4

    goto :goto_0

    .line 98
    :goto_1
    iget-object p1, p0, Lcom/android/helper/wrappers/ContentProvider;->provider:Ljava/lang/Object;

    invoke-virtual {v0, p1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/os/Bundle;
    :try_end_2
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_2 .. :try_end_2} :catch_0

    return-object p1

    :catch_0
    move-exception p1

    .line 100
    const-string p2, "Could not invoke method"

    invoke-static {p2, p1}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;Ljava/lang/Throwable;)V

    .line 101
    throw p1
.end method

.method private getCallMethod()Ljava/lang/reflect/Method;
    .locals 10
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/NoSuchMethodException;
        }
    .end annotation

    .line 54
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethod:Ljava/lang/reflect/Method;

    if-nez v0, :cond_1

    .line 55
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v1, 0x1f

    const/4 v2, 0x5

    const/4 v3, 0x4

    const-string v4, "call"

    const/4 v5, 0x3

    const/4 v6, 0x2

    const/4 v7, 0x1

    const/4 v8, 0x0

    if-lt v0, v1, :cond_0

    .line 56
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->provider:Ljava/lang/Object;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    invoke-static {}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m()Ljava/lang/Class;

    move-result-object v1

    new-array v2, v2, [Ljava/lang/Class;

    aput-object v1, v2, v8

    const-class v1, Ljava/lang/String;

    aput-object v1, v2, v7

    aput-object v1, v2, v6

    aput-object v1, v2, v5

    const-class v1, Landroid/os/Bundle;

    aput-object v1, v2, v3

    invoke-virtual {v0, v4, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethod:Ljava/lang/reflect/Method;

    .line 57
    iput v8, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethodVersion:I

    goto :goto_0

    .line 61
    :cond_0
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->provider:Ljava/lang/Object;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    const/4 v1, 0x6

    new-array v1, v1, [Ljava/lang/Class;

    const-class v9, Ljava/lang/String;

    aput-object v9, v1, v8

    aput-object v9, v1, v7

    aput-object v9, v1, v6

    aput-object v9, v1, v5

    aput-object v9, v1, v3

    const-class v9, Landroid/os/Bundle;

    aput-object v9, v1, v2

    .line 62
    invoke-virtual {v0, v4, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethod:Ljava/lang/reflect/Method;

    .line 63
    iput v7, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethodVersion:I
    :try_end_0
    .catch Ljava/lang/NoSuchMethodException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 66
    :catch_0
    :try_start_1
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->provider:Ljava/lang/Object;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v1, v2, [Ljava/lang/Class;

    const-class v2, Ljava/lang/String;

    aput-object v2, v1, v8

    aput-object v2, v1, v7

    aput-object v2, v1, v6

    aput-object v2, v1, v5

    const-class v2, Landroid/os/Bundle;

    aput-object v2, v1, v3

    invoke-virtual {v0, v4, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethod:Ljava/lang/reflect/Method;

    .line 67
    iput v6, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethodVersion:I
    :try_end_1
    .catch Ljava/lang/NoSuchMethodException; {:try_start_1 .. :try_end_1} :catch_1

    goto :goto_0

    .line 69
    :catch_1
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->provider:Ljava/lang/Object;

    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0

    new-array v1, v3, [Ljava/lang/Class;

    const-class v2, Ljava/lang/String;

    aput-object v2, v1, v8

    aput-object v2, v1, v7

    aput-object v2, v1, v6

    const-class v2, Landroid/os/Bundle;

    aput-object v2, v1, v5

    invoke-virtual {v0, v4, v1}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethod:Ljava/lang/reflect/Method;

    .line 70
    iput v5, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethodVersion:I

    .line 75
    :cond_1
    :goto_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->callMethod:Ljava/lang/reflect/Method;

    return-object v0
.end method

.method private static getGetMethod(Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    .line 110
    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    move-result v0

    const/4 v1, -0x1

    sparse-switch v0, :sswitch_data_0

    goto :goto_0

    :sswitch_0
    const-string v0, "system"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v1, 0x2

    goto :goto_0

    :sswitch_1
    const-string v0, "secure"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    goto :goto_0

    :cond_1
    const/4 v1, 0x1

    goto :goto_0

    :sswitch_2
    const-string v0, "global"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2

    goto :goto_0

    :cond_2
    const/4 v1, 0x0

    :goto_0
    packed-switch v1, :pswitch_data_0

    .line 118
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid table: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 114
    :pswitch_0
    const-string p0, "GET_system"

    return-object p0

    .line 112
    :pswitch_1
    const-string p0, "GET_secure"

    return-object p0

    .line 116
    :pswitch_2
    const-string p0, "GET_global"

    return-object p0

    :sswitch_data_0
    .sparse-switch
        -0x4a16fc5d -> :sswitch_2
        -0x3604a489 -> :sswitch_1
        -0x34e38dd1 -> :sswitch_0
    .end sparse-switch

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_2
        :pswitch_1
        :pswitch_0
    .end packed-switch
.end method

.method private static getPutMethod(Ljava/lang/String;)Ljava/lang/String;
    .locals 3

    .line 123
    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    move-result v0

    const/4 v1, -0x1

    sparse-switch v0, :sswitch_data_0

    goto :goto_0

    :sswitch_0
    const-string v0, "system"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_0

    goto :goto_0

    :cond_0
    const/4 v1, 0x2

    goto :goto_0

    :sswitch_1
    const-string v0, "secure"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_1

    goto :goto_0

    :cond_1
    const/4 v1, 0x1

    goto :goto_0

    :sswitch_2
    const-string v0, "global"

    invoke-virtual {p0, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_2

    goto :goto_0

    :cond_2
    const/4 v1, 0x0

    :goto_0
    packed-switch v1, :pswitch_data_0

    .line 131
    new-instance v0, Ljava/lang/IllegalArgumentException;

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Invalid table: "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v0, p0}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 127
    :pswitch_0
    const-string p0, "PUT_system"

    return-object p0

    .line 125
    :pswitch_1
    const-string p0, "PUT_secure"

    return-object p0

    .line 129
    :pswitch_2
    const-string p0, "PUT_global"

    return-object p0

    :sswitch_data_0
    .sparse-switch
        -0x4a16fc5d -> :sswitch_2
        -0x3604a489 -> :sswitch_1
        -0x34e38dd1 -> :sswitch_0
    .end sparse-switch

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_2
        :pswitch_1
        :pswitch_0
    .end packed-switch
.end method


# virtual methods
.method public close()V
    .locals 3

    .line 106
    iget-object v0, p0, Lcom/android/helper/wrappers/ContentProvider;->manager:Lcom/android/helper/wrappers/ActivityManager;

    iget-object v1, p0, Lcom/android/helper/wrappers/ContentProvider;->name:Ljava/lang/String;

    iget-object v2, p0, Lcom/android/helper/wrappers/ContentProvider;->token:Landroid/os/IBinder;

    invoke-virtual {v0, v1, v2}, Lcom/android/helper/wrappers/ActivityManager;->removeContentProviderExternal(Ljava/lang/String;Landroid/os/IBinder;)V

    return-void
.end method

.method public getValue(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 7
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/util/SettingsException;
        }
    .end annotation

    .line 136
    invoke-static {p1}, Lcom/android/helper/wrappers/ContentProvider;->getGetMethod(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 137
    new-instance v1, Landroid/os/Bundle;

    invoke-direct {v1}, Landroid/os/Bundle;-><init>()V

    .line 138
    const-string v2, "_user"

    const/4 v3, 0x0

    invoke-virtual {v1, v2, v3}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 140
    :try_start_0
    invoke-direct {p0, v0, p2, v1}, Lcom/android/helper/wrappers/ContentProvider;->call(Ljava/lang/String;Ljava/lang/String;Landroid/os/Bundle;)Landroid/os/Bundle;

    move-result-object v0

    if-nez v0, :cond_0

    const/4 p1, 0x0

    return-object p1

    .line 144
    :cond_0
    const-string v1, "value"

    invoke-virtual {v0, v1}, Landroid/os/Bundle;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-object p1

    :catch_0
    move-exception v0

    move-object v6, v0

    .line 146
    new-instance v1, Lcom/android/helper/util/SettingsException;

    const-string v3, "get"

    const/4 v5, 0x0

    move-object v2, p1

    move-object v4, p2

    invoke-direct/range {v1 .. v6}, Lcom/android/helper/util/SettingsException;-><init>(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)V

    throw v1
.end method

.method public putValue(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 9
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/util/SettingsException;
        }
    .end annotation

    .line 152
    invoke-static {p1}, Lcom/android/helper/wrappers/ContentProvider;->getPutMethod(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 153
    new-instance v1, Landroid/os/Bundle;

    invoke-direct {v1}, Landroid/os/Bundle;-><init>()V

    .line 154
    const-string v2, "_user"

    const/4 v3, 0x0

    invoke-virtual {v1, v2, v3}, Landroid/os/Bundle;->putInt(Ljava/lang/String;I)V

    .line 155
    const-string v2, "value"

    invoke-virtual {v1, v2, p3}, Landroid/os/Bundle;->putString(Ljava/lang/String;Ljava/lang/String;)V

    .line 157
    :try_start_0
    invoke-direct {p0, v0, p2, v1}, Lcom/android/helper/wrappers/ContentProvider;->call(Ljava/lang/String;Ljava/lang/String;Landroid/os/Bundle;)Landroid/os/Bundle;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    return-void

    :catch_0
    move-exception v0

    move-object v8, v0

    .line 159
    new-instance v3, Lcom/android/helper/util/SettingsException;

    const-string v5, "put"

    move-object v4, p1

    move-object v6, p2

    move-object v7, p3

    invoke-direct/range {v3 .. v8}, Lcom/android/helper/util/SettingsException;-><init>(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)V

    throw v3
.end method
