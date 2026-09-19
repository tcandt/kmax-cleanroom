.class Lcom/android/helper/FakeContext$2$1;
.super Ljava/lang/Object;
.source "FakeContext.java"

# interfaces
.implements Landroid/content/SharedPreferences$Editor;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/android/helper/FakeContext$2;->edit()Landroid/content/SharedPreferences$Editor;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/android/helper/FakeContext$2;


# direct methods
.method constructor <init>(Lcom/android/helper/FakeContext$2;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010
        }
        names = {
            null
        }
    .end annotation

    .line 130
    iput-object p1, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public apply()V
    .locals 0

    return-void
.end method

.method public clear()Landroid/content/SharedPreferences$Editor;
    .locals 1

    .line 138
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-interface {v0}, Ljava/util/Map;->clear()V

    return-object p0
.end method

.method public commit()Z
    .locals 1

    const/4 v0, 0x1

    return v0
.end method

.method public putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    .locals 1

    .line 136
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-static {p2}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object p2

    invoke-interface {v0, p1, p2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    return-object p0
.end method

.method public putFloat(Ljava/lang/String;F)Landroid/content/SharedPreferences$Editor;
    .locals 1

    .line 135
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-static {p2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object p2

    invoke-interface {v0, p1, p2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    return-object p0
.end method

.method public putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;
    .locals 1

    .line 133
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-static {p2}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object p2

    invoke-interface {v0, p1, p2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    return-object p0
.end method

.method public putLong(Ljava/lang/String;J)Landroid/content/SharedPreferences$Editor;
    .locals 1

    .line 134
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-static {p2, p3}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;

    move-result-object p2

    invoke-interface {v0, p1, p2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    return-object p0
.end method

.method public putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    .locals 1

    if-eqz p2, :cond_0

    .line 131
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-interface {v0, p1, p2}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    :cond_0
    return-object p0
.end method

.method public putStringSet(Ljava/lang/String;Ljava/util/Set;)Landroid/content/SharedPreferences$Editor;
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "Ljava/util/Set<",
            "Ljava/lang/String;",
            ">;)",
            "Landroid/content/SharedPreferences$Editor;"
        }
    .end annotation

    return-object p0
.end method

.method public remove(Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    .locals 1

    .line 137
    iget-object v0, p0, Lcom/android/helper/FakeContext$2$1;->this$1:Lcom/android/helper/FakeContext$2;

    invoke-static {v0}, Lcom/android/helper/FakeContext$2;->access$000(Lcom/android/helper/FakeContext$2;)Ljava/util/Map;

    move-result-object v0

    invoke-interface {v0, p1}, Ljava/util/Map;->remove(Ljava/lang/Object;)Ljava/lang/Object;

    return-object p0
.end method
