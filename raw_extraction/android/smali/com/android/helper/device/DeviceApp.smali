.class public final Lcom/android/helper/device/DeviceApp;
.super Ljava/lang/Object;
.source "DeviceApp.java"


# instance fields
.field private final name:Ljava/lang/String;

.field private final packageName:Ljava/lang/String;

.field private final system:Z


# direct methods
.method public constructor <init>(Ljava/lang/String;Ljava/lang/String;Z)V
    .locals 0

    .line 9
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 10
    iput-object p1, p0, Lcom/android/helper/device/DeviceApp;->packageName:Ljava/lang/String;

    .line 11
    iput-object p2, p0, Lcom/android/helper/device/DeviceApp;->name:Ljava/lang/String;

    .line 12
    iput-boolean p3, p0, Lcom/android/helper/device/DeviceApp;->system:Z

    return-void
.end method


# virtual methods
.method public getName()Ljava/lang/String;
    .locals 1

    .line 20
    iget-object v0, p0, Lcom/android/helper/device/DeviceApp;->name:Ljava/lang/String;

    return-object v0
.end method

.method public getPackageName()Ljava/lang/String;
    .locals 1

    .line 16
    iget-object v0, p0, Lcom/android/helper/device/DeviceApp;->packageName:Ljava/lang/String;

    return-object v0
.end method

.method public isSystem()Z
    .locals 1

    .line 24
    iget-boolean v0, p0, Lcom/android/helper/device/DeviceApp;->system:Z

    return v0
.end method
