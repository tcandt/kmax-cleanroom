.class public final Lcom/android/helper/opengl/GLUtils;
.super Ljava/lang/Object;
.source "GLUtils.java"


# static fields
.field private static final DEBUG:Z = false


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 17
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static checkGlError()V
    .locals 0

    return-void
.end method

.method public static createFloatBuffer([F)Ljava/nio/FloatBuffer;
    .locals 2

    .line 119
    array-length v0, p0

    mul-int/lit8 v0, v0, 0x4

    invoke-static {v0}, Ljava/nio/ByteBuffer;->allocateDirect(I)Ljava/nio/ByteBuffer;

    move-result-object v0

    invoke-static {}, Ljava/nio/ByteOrder;->nativeOrder()Ljava/nio/ByteOrder;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/nio/ByteBuffer;->order(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;

    move-result-object v0

    invoke-virtual {v0}, Ljava/nio/ByteBuffer;->asFloatBuffer()Ljava/nio/FloatBuffer;

    move-result-object v0

    .line 120
    invoke-virtual {v0, p0}, Ljava/nio/FloatBuffer;->put([F)Ljava/nio/FloatBuffer;

    const/4 p0, 0x0

    .line 121
    invoke-virtual {v0, p0}, Ljava/nio/FloatBuffer;->position(I)Ljava/nio/Buffer;

    return-object v0
.end method

.method public static createProgram(Ljava/lang/String;Ljava/lang/String;)I
    .locals 4

    const v0, 0x8b31

    .line 22
    invoke-static {v0, p0}, Lcom/android/helper/opengl/GLUtils;->createShader(ILjava/lang/String;)I

    move-result p0

    const/4 v0, 0x0

    if-nez p0, :cond_0

    return v0

    :cond_0
    const v1, 0x8b30

    .line 27
    invoke-static {v1, p1}, Lcom/android/helper/opengl/GLUtils;->createShader(ILjava/lang/String;)I

    move-result p1

    if-nez p1, :cond_1

    .line 29
    invoke-static {p0}, Landroid/opengl/GLES20;->glDeleteShader(I)V

    return v0

    .line 33
    :cond_1
    invoke-static {}, Landroid/opengl/GLES20;->glCreateProgram()I

    move-result v1

    if-nez v1, :cond_2

    .line 35
    invoke-static {p1}, Landroid/opengl/GLES20;->glDeleteShader(I)V

    .line 36
    invoke-static {p0}, Landroid/opengl/GLES20;->glDeleteShader(I)V

    return v0

    .line 40
    :cond_2
    invoke-static {v1, p0}, Landroid/opengl/GLES20;->glAttachShader(II)V

    .line 41
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 42
    invoke-static {v1, p1}, Landroid/opengl/GLES20;->glAttachShader(II)V

    .line 43
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 44
    invoke-static {v1}, Landroid/opengl/GLES20;->glLinkProgram(I)V

    .line 45
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const/4 v2, 0x1

    .line 47
    new-array v2, v2, [I

    const v3, 0x8b82

    .line 48
    invoke-static {v1, v3, v2, v0}, Landroid/opengl/GLES20;->glGetProgramiv(II[II)V

    .line 49
    aget v2, v2, v0

    if-nez v2, :cond_3

    .line 50
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Could not link program: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {v1}, Landroid/opengl/GLES20;->glGetProgramInfoLog(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 51
    invoke-static {v1}, Landroid/opengl/GLES20;->glDeleteProgram(I)V

    .line 52
    invoke-static {p1}, Landroid/opengl/GLES20;->glDeleteShader(I)V

    .line 53
    invoke-static {p0}, Landroid/opengl/GLES20;->glDeleteShader(I)V

    return v0

    :cond_3
    return v1
.end method

.method public static createShader(ILjava/lang/String;)I
    .locals 3

    .line 61
    invoke-static {p0}, Landroid/opengl/GLES20;->glCreateShader(I)I

    move-result v0

    const/4 v1, 0x0

    if-nez v0, :cond_0

    .line 63
    const-string p0, "Could not create shader"

    invoke-static {p0}, Lcom/android/helper/opengl/GLUtils;->getGlErrorMessage(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    return v1

    .line 67
    :cond_0
    invoke-static {v0, p1}, Landroid/opengl/GLES20;->glShaderSource(ILjava/lang/String;)V

    .line 68
    invoke-static {v0}, Landroid/opengl/GLES20;->glCompileShader(I)V

    const/4 p1, 0x1

    .line 70
    new-array p1, p1, [I

    const v2, 0x8b81

    .line 71
    invoke-static {v0, v2, p1, v1}, Landroid/opengl/GLES20;->glGetShaderiv(II[II)V

    .line 72
    aget p1, p1, v1

    if-nez p1, :cond_1

    .line 73
    new-instance p1, Ljava/lang/StringBuilder;

    const-string v2, "Could not compile "

    invoke-direct {p1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {p0}, Lcom/android/helper/opengl/GLUtils;->getShaderTypeString(I)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, ": "

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {v0}, Landroid/opengl/GLES20;->glGetShaderInfoLog(I)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {p1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-static {p0}, Lcom/android/helper/util/Ln;->e(Ljava/lang/String;)V

    .line 74
    invoke-static {v0}, Landroid/opengl/GLES20;->glDeleteShader(I)V

    return v1

    :cond_1
    return v0
.end method

.method public static getGlErrorMessage(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .line 105
    invoke-static {}, Landroid/opengl/GLES20;->glGetError()I

    move-result v0

    if-nez v0, :cond_0

    return-object p0

    .line 110
    :cond_0
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " ("

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-static {v0}, Lcom/android/helper/opengl/GLUtils;->toErrorString(I)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, ")"

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method

.method private static getShaderTypeString(I)Ljava/lang/String;
    .locals 0

    packed-switch p0, :pswitch_data_0

    .line 88
    const-string p0, "shader"

    return-object p0

    .line 84
    :pswitch_0
    const-string p0, "vertex shader"

    return-object p0

    .line 86
    :pswitch_1
    const-string p0, "fragment shader"

    return-object p0

    :pswitch_data_0
    .packed-switch 0x8b30
        :pswitch_1
        :pswitch_0
    .end packed-switch
.end method

.method private static toErrorString(I)Ljava/lang/String;
    .locals 3

    .line 114
    invoke-static {p0}, Landroid/opengl/GLU;->gluErrorString(I)Ljava/lang/String;

    move-result-object v0

    .line 115
    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "glError 0x"

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {p0}, Ljava/lang/Integer;->toHexString(I)Ljava/lang/String;

    move-result-object p0

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string p0, " "

    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method
