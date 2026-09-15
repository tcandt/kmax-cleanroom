.class public final Lcom/android/helper/FakeContext;
.super Landroid/content/ContextWrapper;
.source "FakeContext.java"


# static fields
.field private static final INSTANCE:Lcom/android/helper/FakeContext;

.field public static final PACKAGE_NAME:Ljava/lang/String; = "com.android.shell"

.field public static final ROOT_UID:I


# instance fields
.field private final contentResolver:Landroid/content/ContentResolver;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .line 22
    new-instance v0, Lcom/android/helper/FakeContext;

    invoke-direct {v0}, Lcom/android/helper/FakeContext;-><init>()V

    sput-object v0, Lcom/android/helper/FakeContext;->INSTANCE:Lcom/android/helper/FakeContext;

    return-void
.end method

.method private constructor <init>()V
    .locals 1

    .line 61
    invoke-static {}, Lcom/android/helper/Workarounds;->getSystemContext()Landroid/content/Context;

    move-result-object v0

    invoke-direct {p0, v0}, Landroid/content/ContextWrapper;-><init>(Landroid/content/Context;)V

    .line 28
    new-instance v0, Lcom/android/helper/FakeContext$1;

    invoke-direct {v0, p0, p0}, Lcom/android/helper/FakeContext$1;-><init>(Lcom/android/helper/FakeContext;Landroid/content/Context;)V

    iput-object v0, p0, Lcom/android/helper/FakeContext;->contentResolver:Landroid/content/ContentResolver;

    return-void
.end method

.method public static get()Lcom/android/helper/FakeContext;
    .locals 1

    .line 25
    sget-object v0, Lcom/android/helper/FakeContext;->INSTANCE:Lcom/android/helper/FakeContext;

    return-object v0
.end method


# virtual methods
.method public createPackageContext(Ljava/lang/String;I)Landroid/content/Context;
    .locals 0

    return-object p0
.end method

.method public getApplicationContext()Landroid/content/Context;
    .locals 0

    return-object p0
.end method

.method public getAttributionSource()Landroid/content/AttributionSource;
    .locals 2

    const/16 v0, 0x7d0

    .line 163
    invoke-static {v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(I)Landroid/content/AttributionSource$Builder;

    move-result-object v0

    .line 164
    const-string v1, "com.android.shell"

    invoke-static {v0, v1}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/content/AttributionSource$Builder;Ljava/lang/String;)Landroid/content/AttributionSource$Builder;

    .line 165
    invoke-static {v0}, Lcom/android/helper/FakeContext$$ExternalSyntheticApiModelOutline0;->m(Landroid/content/AttributionSource$Builder;)Landroid/content/AttributionSource;

    move-result-object v0

    return-object v0
.end method

.method public getCacheDir()Ljava/io/File;
    .locals 2

    .line 78
    new-instance v0, Ljava/io/File;

    const-string v1, "/data/local/tmp/scrcpy_cache"

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 79
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    :cond_0
    return-object v0
.end method

.method public getContentResolver()Landroid/content/ContentResolver;
    .locals 1

    .line 186
    iget-object v0, p0, Lcom/android/helper/FakeContext;->contentResolver:Landroid/content/ContentResolver;

    return-object v0
.end method

.method public getDataDir()Ljava/io/File;
    .locals 2

    .line 66
    new-instance v0, Ljava/io/File;

    const-string v1, "/data/local/tmp"

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    return-object v0
.end method

.method public getDatabasePath(Ljava/lang/String;)Ljava/io/File;
    .locals 2

    .line 85
    new-instance v0, Ljava/io/File;

    const-string v1, "/data/local/tmp/scrcpy_db"

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 86
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    .line 87
    :cond_0
    new-instance v1, Ljava/io/File;

    invoke-direct {v1, v0, p1}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    return-object v1
.end method

.method public getDeviceId()I
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public getDir(Ljava/lang/String;I)Ljava/io/File;
    .locals 2

    .line 102
    new-instance p2, Ljava/io/File;

    new-instance v0, Ljava/lang/StringBuilder;

    const-string v1, "/data/local/tmp/scrcpy_"

    invoke-direct {v0, v1}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {p2, p1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 103
    invoke-virtual {p2}, Ljava/io/File;->exists()Z

    move-result p1

    if-nez p1, :cond_0

    invoke-virtual {p2}, Ljava/io/File;->mkdirs()Z

    :cond_0
    return-object p2
.end method

.method public getFilesDir()Ljava/io/File;
    .locals 2

    .line 71
    new-instance v0, Ljava/io/File;

    const-string v1, "/data/local/tmp/scrcpy_files"

    invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 72
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    :cond_0
    return-object v0
.end method

.method public getOpPackageName()Ljava/lang/String;
    .locals 1

    .line 157
    const-string v0, "com.android.shell"

    return-object v0
.end method

.method public getPackageName()Ljava/lang/String;
    .locals 1

    .line 152
    const-string v0, "com.android.shell"

    return-object v0
.end method

.method public getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    .locals 0

    .line 109
    new-instance p1, Lcom/android/helper/FakeContext$2;

    invoke-direct {p1, p0}, Lcom/android/helper/FakeContext$2;-><init>(Lcom/android/helper/FakeContext;)V

    return-object p1
.end method

.method public getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    .locals 4

    .line 192
    invoke-super {p0, p1}, Landroid/content/ContextWrapper;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    if-nez v0, :cond_0

    const/4 p1, 0x0

    return-object p1

    .line 201
    :cond_0
    const-string v1, "clipboard"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    const-string v2, "power"

    if-nez v1, :cond_2

    const-string v1, "semclipboard"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_2

    const-string v1, "activity"

    invoke-virtual {v1, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_2

    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_1

    goto :goto_0

    :cond_1
    return-object v0

    .line 203
    :cond_2
    :goto_0
    :try_start_0
    invoke-virtual {v0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v1

    const-string v3, "mContext"

    invoke-virtual {v1, v3}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;

    move-result-object v1

    const/4 v3, 0x1

    .line 204
    invoke-virtual {v1, v3}, Ljava/lang/reflect/Field;->setAccessible(Z)V

    .line 205
    invoke-virtual {v1, v0, p0}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V
    :try_end_0
    .catch Ljava/lang/ReflectiveOperationException; {:try_start_0 .. :try_end_0} :catch_0

    return-object v0

    :catch_0
    move-exception v1

    .line 207
    invoke-virtual {v2, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result p1

    if-eqz p1, :cond_3

    .line 208
    new-instance p1, Ljava/lang/StringBuilder;

    const-string v2, "Could not inject FakeContext to PowerManager: "

    invoke-direct {p1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/lang/ReflectiveOperationException;->getMessage()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1}, Lcom/android/helper/util/Ln;->w(Ljava/lang/String;)V

    return-object v0

    .line 210
    :cond_3
    new-instance p1, Ljava/lang/RuntimeException;

    invoke-direct {p1, v1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/Throwable;)V

    throw p1
.end method

.method public openOrCreateDatabase(Ljava/lang/String;ILandroid/database/sqlite/SQLiteDatabase$CursorFactory;)Landroid/database/sqlite/SQLiteDatabase;
    .locals 0

    .line 92
    invoke-virtual {p0, p1}, Lcom/android/helper/FakeContext;->getDatabasePath(Ljava/lang/String;)Ljava/io/File;

    move-result-object p1

    invoke-static {p1, p3}, Landroid/database/sqlite/SQLiteDatabase;->openOrCreateDatabase(Ljava/io/File;Landroid/database/sqlite/SQLiteDatabase$CursorFactory;)Landroid/database/sqlite/SQLiteDatabase;

    move-result-object p1

    return-object p1
.end method

.method public openOrCreateDatabase(Ljava/lang/String;ILandroid/database/sqlite/SQLiteDatabase$CursorFactory;Landroid/database/DatabaseErrorHandler;)Landroid/database/sqlite/SQLiteDatabase;
    .locals 0

    .line 97
    invoke-virtual {p0, p1}, Lcom/android/helper/FakeContext;->getDatabasePath(Ljava/lang/String;)Ljava/io/File;

    move-result-object p1

    invoke-virtual {p1}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object p1

    invoke-static {p1, p3, p4}, Landroid/database/sqlite/SQLiteDatabase;->openOrCreateDatabase(Ljava/lang/String;Landroid/database/sqlite/SQLiteDatabase$CursorFactory;Landroid/database/DatabaseErrorHandler;)Landroid/database/sqlite/SQLiteDatabase;

    move-result-object p1

    return-object p1
.end method
