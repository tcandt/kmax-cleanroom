.class final Lcom/android/helper/control/Controller$DisplayData;
.super Ljava/lang/Object;
.source "Controller.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/android/helper/control/Controller;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x1a
    name = "DisplayData"
.end annotation


# instance fields
.field private final positionMapper:Lcom/android/helper/control/PositionMapper;

.field private final virtualDisplayId:I


# direct methods
.method private constructor <init>(ILcom/android/helper/control/PositionMapper;)V
    .locals 0

    .line 60
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 61
    iput p1, p0, Lcom/android/helper/control/Controller$DisplayData;->virtualDisplayId:I

    .line 62
    iput-object p2, p0, Lcom/android/helper/control/Controller$DisplayData;->positionMapper:Lcom/android/helper/control/PositionMapper;

    return-void
.end method

.method synthetic constructor <init>(ILcom/android/helper/control/PositionMapper;Lcom/android/helper/control/Controller$1;)V
    .locals 0

    .line 56
    invoke-direct {p0, p1, p2}, Lcom/android/helper/control/Controller$DisplayData;-><init>(ILcom/android/helper/control/PositionMapper;)V

    return-void
.end method

.method static synthetic access$100(Lcom/android/helper/control/Controller$DisplayData;)I
    .locals 0

    .line 56
    iget p0, p0, Lcom/android/helper/control/Controller$DisplayData;->virtualDisplayId:I

    return p0
.end method

.method static synthetic access$200(Lcom/android/helper/control/Controller$DisplayData;)Lcom/android/helper/control/PositionMapper;
    .locals 0

    .line 56
    iget-object p0, p0, Lcom/android/helper/control/Controller$DisplayData;->positionMapper:Lcom/android/helper/control/PositionMapper;

    return-object p0
.end method
