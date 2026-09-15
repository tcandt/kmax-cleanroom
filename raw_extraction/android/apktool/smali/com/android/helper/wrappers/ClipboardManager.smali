.class public final Lcom/android/helper/wrappers/ClipboardManager;
.super Ljava/lang/Object;
.source "ClipboardManager.java"


# instance fields
.field private final manager:Landroid/content/ClipboardManager;


# direct methods
.method private constructor <init>(Landroid/content/ClipboardManager;)V
    .locals 0

    .line 28
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 29
    iput-object p1, p0, Lcom/android/helper/wrappers/ClipboardManager;->manager:Landroid/content/ClipboardManager;

    return-void
.end method

.method static create()Lcom/android/helper/wrappers/ClipboardManager;
    .locals 3

    const/4 v0, 0x0

    .line 14
    :try_start_0
    invoke-static {}, Lcom/android/helper/FakeContext;->get()Lcom/android/helper/FakeContext;

    move-result-object v1

    const-string v2, "clipboard"

    invoke-virtual {v1, v2}, Lcom/android/helper/FakeContext;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/content/ClipboardManager;

    if-nez v1, :cond_0

    return-object v0

    .line 21
    :cond_0
    new-instance v2, Lcom/android/helper/wrappers/ClipboardManager;

    invoke-direct {v2, v1}, Lcom/android/helper/wrappers/ClipboardManager;-><init>(Landroid/content/ClipboardManager;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-object v2

    :catchall_0
    move-exception v1

    .line 23
    const-string v2, "create ClipboardManager"

    invoke-static {v2, v1}, Lcom/android/helper/wrappers/ClipboardManager;->logClipboardError(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method private static logClipboardError(Ljava/lang/String;Ljava/lang/Throwable;)V
    .locals 2

    .line 65
    invoke-virtual {p1}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;

    move-result-object v0

    .line 66
    instance-of p1, p1, Ljava/lang/SecurityException;

    const-string v1, "Could not "

    if-eqz p1, :cond_0

    invoke-static {}, Landroid/os/Process;->myUid()I

    move-result p1

    if-nez p1, :cond_0

    .line 67
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " (SecurityException). Since scrcpy-server is running as root (uid 0), please try running cloudphone-agent with the \'-root\' flag to drop privileges to shell (uid 2000). Detail: "

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void

    .line 69
    :cond_0
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, ": "

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-void
.end method


# virtual methods
.method public addPrimaryClipChangedListener(Landroid/content/ClipboardManager$OnPrimaryClipChangedListener;)V
    .locals 1

    .line 58
    :try_start_0
    iget-object v0, p0, Lcom/android/helper/wrappers/ClipboardManager;->manager:Landroid/content/ClipboardManager;

    invoke-virtual {v0, p1}, Landroid/content/ClipboardManager;->addPrimaryClipChangedListener(Landroid/content/ClipboardManager$OnPrimaryClipChangedListener;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    return-void

    :catchall_0
    move-exception p1

    .line 60
    const-string v0, "add primary clip changed listener"

    invoke-static {v0, p1}, Lcom/android/helper/wrappers/ClipboardManager;->logClipboardError(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-void
.end method

.method public getText()Ljava/lang/CharSequence;
    .locals 3

    const/4 v0, 0x0

    .line 34
    :try_start_0
    iget-object v1, p0, Lcom/android/helper/wrappers/ClipboardManager;->manager:Landroid/content/ClipboardManager;

    invoke-virtual {v1}, Landroid/content/ClipboardManager;->getPrimaryClip()Landroid/content/ClipData;

    move-result-object v1

    if-eqz v1, :cond_1

    .line 35
    invoke-virtual {v1}, Landroid/content/ClipData;->getItemCount()I

    move-result v2

    if-nez v2, :cond_0

    goto :goto_0

    :cond_0
    const/4 v2, 0x0

    .line 38
    invoke-virtual {v1, v2}, Landroid/content/ClipData;->getItemAt(I)Landroid/content/ClipData$Item;

    move-result-object v1

    invoke-virtual {v1}, Landroid/content/ClipData$Item;->getText()Ljava/lang/CharSequence;

    move-result-object v0
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :cond_1
    :goto_0
    return-object v0

    :catchall_0
    move-exception v1

    .line 40
    const-string v2, "get clipboard text"

    invoke-static {v2, v1}, Lcom/android/helper/wrappers/ClipboardManager;->logClipboardError(Ljava/lang/String;Ljava/lang/Throwable;)V

    return-object v0
.end method

.method public setText(Ljava/lang/CharSequence;)Z
    .locals 1

    const/4 v0, 0x0

    .line 47
    :try_start_0
    invoke-static {v0, p1}, Landroid/content/ClipData;->newPlainText(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Landroid/content/ClipData;

    move-result-object p1

    .line 48
    iget-object v0, p0, Lcom/android/helper/wrappers/ClipboardManager;->manager:Landroid/content/ClipboardManager;

    invoke-virtual {v0, p1}, Landroid/content/ClipboardManager;->setPrimaryClip(Landroid/content/ClipData;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    const/4 p1, 0x1

    return p1

    :catchall_0
    move-exception p1

    .line 51
    const-string v0, "set clipboard text"

    invoke-static {v0, p1}, Lcom/android/helper/wrappers/ClipboardManager;->logClipboardError(Ljava/lang/String;Ljava/lang/Throwable;)V

    const/4 p1, 0x0

    return p1
.end method
