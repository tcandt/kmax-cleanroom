.class public final Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;
.super Ljava/lang/Object;
.source "DisplayManager.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/wrappers/DisplayManager;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x19
    name = "DisplayListenerHandle"
.end annotation


# instance fields
.field private final displayListenerProxy:Ljava/lang/Object;


# direct methods
.method private constructor <init>(Ljava/lang/Object;)V
    .locals 0

    .line 43
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 44
    iput-object p1, p0, Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;->displayListenerProxy:Ljava/lang/Object;

    return-void
.end method

.method synthetic constructor <init>(Ljava/lang/Object;Lcom/android/helper/wrappers/DisplayManager$1;)V
    .locals 0

    .line 41
    invoke-direct {p0, p1}, Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;-><init>(Ljava/lang/Object;)V

    return-void
.end method

.method static synthetic access$100(Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;)Ljava/lang/Object;
    .locals 0

    .line 41
    iget-object p0, p0, Lcom/android/helper/wrappers/DisplayManager$DisplayListenerHandle;->displayListenerProxy:Ljava/lang/Object;

    return-object p0
.end method
