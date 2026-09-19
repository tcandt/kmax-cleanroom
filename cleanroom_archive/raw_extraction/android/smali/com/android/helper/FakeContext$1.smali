.class Lcom/android/helper/FakeContext$1;
.super Landroid/content/ContentResolver;
.source "FakeContext.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/FakeContext;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/android/helper/FakeContext;


# direct methods
.method constructor <init>(Lcom/android/helper/FakeContext;Landroid/content/Context;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x0
        }
        names = {
            null,
            null
        }
    .end annotation

    .line 28
    iput-object p1, p0, Lcom/android/helper/FakeContext$1;->this$0:Lcom/android/helper/FakeContext;

    invoke-direct {p0, p2}, Landroid/content/ContentResolver;-><init>(Landroid/content/Context;)V

    return-void
.end method


# virtual methods
.method protected acquireProvider(Landroid/content/Context;Ljava/lang/String;)Landroid/content/IContentProvider;
    .locals 1

    .line 32
    invoke-static {}, Lcom/android/helper/wrappers/ServiceManager;->getActivityManager()Lcom/android/helper/wrappers/ActivityManager;

    move-result-object p1

    new-instance v0, Landroid/os/Binder;

    invoke-direct {v0}, Landroid/os/Binder;-><init>()V

    invoke-virtual {p1, p2, v0}, Lcom/android/helper/wrappers/ActivityManager;->getContentProviderExternal(Ljava/lang/String;Landroid/os/IBinder;)Landroid/content/IContentProvider;

    move-result-object p1

    return-object p1
.end method

.method protected acquireUnstableProvider(Landroid/content/Context;Ljava/lang/String;)Landroid/content/IContentProvider;
    .locals 0

    const/4 p1, 0x0

    return-object p1
.end method

.method public releaseProvider(Landroid/content/IContentProvider;)Z
    .locals 0

    const/4 p1, 0x0

    return p1
.end method

.method public releaseUnstableProvider(Landroid/content/IContentProvider;)Z
    .locals 0

    const/4 p1, 0x0

    return p1
.end method

.method public unstableProviderDied(Landroid/content/IContentProvider;)V
    .locals 0

    return-void
.end method
