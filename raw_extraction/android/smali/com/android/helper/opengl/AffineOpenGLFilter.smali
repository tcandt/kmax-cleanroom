.class public Lcom/android/helper/opengl/AffineOpenGLFilter;
.super Ljava/lang/Object;
.source "AffineOpenGLFilter.java"

# interfaces
.implements Lcom/android/helper/opengl/OpenGLFilter;


# static fields
.field static final synthetic $assertionsDisabled:Z


# instance fields
.field private program:I

.field private texCoordsBuffer:Ljava/nio/FloatBuffer;

.field private texCoordsInLoc:I

.field private texLoc:I

.field private texMatrixLoc:I

.field private final userMatrix:[F

.field private userMatrixLoc:I

.field private vertexBuffer:Ljava/nio/FloatBuffer;

.field private vertexPosLoc:I


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>(Lcom/android/helper/util/AffineMatrix;)V
    .locals 0

    .line 24
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 25
    invoke-virtual {p1}, Lcom/android/helper/util/AffineMatrix;->to4x4()[F

    move-result-object p1

    iput-object p1, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->userMatrix:[F

    return-void
.end method


# virtual methods
.method public draw(I[F)V
    .locals 13

    .line 98
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    invoke-static {v0}, Landroid/opengl/GLES20;->glUseProgram(I)V

    .line 99
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 101
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->vertexPosLoc:I

    invoke-static {v0}, Landroid/opengl/GLES20;->glEnableVertexAttribArray(I)V

    .line 102
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 103
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texCoordsInLoc:I

    invoke-static {v0}, Landroid/opengl/GLES20;->glEnableVertexAttribArray(I)V

    .line 104
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 106
    iget v1, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->vertexPosLoc:I

    const/4 v5, 0x0

    iget-object v6, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->vertexBuffer:Ljava/nio/FloatBuffer;

    const/4 v2, 0x2

    const/16 v3, 0x1406

    const/4 v4, 0x0

    invoke-static/range {v1 .. v6}, Landroid/opengl/GLES20;->glVertexAttribPointer(IIIZILjava/nio/Buffer;)V

    .line 107
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 108
    iget v7, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texCoordsInLoc:I

    const/4 v11, 0x0

    iget-object v12, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texCoordsBuffer:Ljava/nio/FloatBuffer;

    const/4 v8, 0x2

    const/16 v9, 0x1406

    const/4 v10, 0x0

    invoke-static/range {v7 .. v12}, Landroid/opengl/GLES20;->glVertexAttribPointer(IIIZILjava/nio/Buffer;)V

    .line 109
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const v0, 0x84c0

    .line 111
    invoke-static {v0}, Landroid/opengl/GLES20;->glActiveTexture(I)V

    .line 112
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const v0, 0x8d65

    .line 113
    invoke-static {v0, p1}, Landroid/opengl/GLES20;->glBindTexture(II)V

    .line 114
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 115
    iget p1, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texLoc:I

    const/4 v0, 0x0

    invoke-static {p1, v0}, Landroid/opengl/GLES20;->glUniform1i(II)V

    .line 116
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 118
    iget p1, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texMatrixLoc:I

    const/4 v1, 0x1

    invoke-static {p1, v1, v0, p2, v0}, Landroid/opengl/GLES20;->glUniformMatrix4fv(IIZ[FI)V

    .line 119
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    .line 121
    iget p1, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->userMatrixLoc:I

    iget-object p2, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->userMatrix:[F

    invoke-static {p1, v1, v0, p2, v0}, Landroid/opengl/GLES20;->glUniformMatrix4fv(IIZ[FI)V

    .line 122
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const/16 p1, 0x4000

    .line 124
    invoke-static {p1}, Landroid/opengl/GLES20;->glClear(I)V

    .line 125
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    const/4 p1, 0x5

    const/4 p2, 0x4

    .line 126
    invoke-static {p1, v0, p2}, Landroid/opengl/GLES20;->glDrawArrays(III)V

    .line 127
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    return-void
.end method

.method public init()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Lcom/android/helper/opengl/OpenGLException;
        }
    .end annotation

    .line 31
    const-string v0, "#version 100\nattribute vec4 vertex_pos;\nattribute vec4 tex_coords_in;\nvarying vec2 tex_coords;\nuniform mat4 tex_matrix;\nuniform mat4 user_matrix;\nvoid main() {\n    gl_Position = vertex_pos;\n    tex_coords = (tex_matrix * user_matrix * tex_coords_in).xy;\n}"

    .line 43
    const-string v1, "#version 100\n#extension GL_OES_EGL_image_external : require\nprecision highp float;\nuniform samplerExternalOES tex;\nvarying vec2 tex_coords;\nvoid main() {\n    if (tex_coords.x >= 0.0 && tex_coords.x <= 1.0\n            && tex_coords.y >= 0.0 && tex_coords.y <= 1.0) {\n        gl_FragColor = texture2D(tex, tex_coords);\n    } else {\n        gl_FragColor = vec4(0.0);\n    }\n}"

    .line 57
    invoke-static {v0, v1}, Lcom/android/helper/opengl/GLUtils;->createProgram(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    if-eqz v0, :cond_0

    const/16 v0, 0x8

    .line 62
    new-array v1, v0, [F

    fill-array-data v1, :array_0

    .line 69
    new-array v0, v0, [F

    fill-array-data v0, :array_1

    .line 77
    invoke-static {v1}, Lcom/android/helper/opengl/GLUtils;->createFloatBuffer([F)Ljava/nio/FloatBuffer;

    move-result-object v1

    iput-object v1, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->vertexBuffer:Ljava/nio/FloatBuffer;

    .line 78
    invoke-static {v0}, Lcom/android/helper/opengl/GLUtils;->createFloatBuffer([F)Ljava/nio/FloatBuffer;

    move-result-object v0

    iput-object v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texCoordsBuffer:Ljava/nio/FloatBuffer;

    .line 80
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    const-string v1, "vertex_pos"

    invoke-static {v0, v1}, Landroid/opengl/GLES20;->glGetAttribLocation(ILjava/lang/String;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->vertexPosLoc:I

    .line 83
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    const-string v1, "tex_coords_in"

    invoke-static {v0, v1}, Landroid/opengl/GLES20;->glGetAttribLocation(ILjava/lang/String;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texCoordsInLoc:I

    .line 86
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    const-string v1, "tex"

    invoke-static {v0, v1}, Landroid/opengl/GLES20;->glGetUniformLocation(ILjava/lang/String;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texLoc:I

    .line 89
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    const-string v1, "tex_matrix"

    invoke-static {v0, v1}, Landroid/opengl/GLES20;->glGetUniformLocation(ILjava/lang/String;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->texMatrixLoc:I

    .line 92
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    const-string v1, "user_matrix"

    invoke-static {v0, v1}, Landroid/opengl/GLES20;->glGetUniformLocation(ILjava/lang/String;)I

    move-result v0

    iput v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->userMatrixLoc:I

    return-void

    .line 59
    :cond_0
    new-instance v0, Lcom/android/helper/opengl/OpenGLException;

    const-string v1, "Cannot create OpenGL program"

    invoke-direct {v0, v1}, Lcom/android/helper/opengl/OpenGLException;-><init>(Ljava/lang/String;)V

    throw v0

    nop

    :array_0
    .array-data 4
        -0x40800000    # -1.0f
        -0x40800000    # -1.0f
        0x3f800000    # 1.0f
        -0x40800000    # -1.0f
        -0x40800000    # -1.0f
        0x3f800000    # 1.0f
        0x3f800000    # 1.0f
        0x3f800000    # 1.0f
    .end array-data

    :array_1
    .array-data 4
        0x0
        0x0
        0x3f800000    # 1.0f
        0x0
        0x0
        0x3f800000    # 1.0f
        0x3f800000    # 1.0f
        0x3f800000    # 1.0f
    .end array-data
.end method

.method public release()V
    .locals 1

    .line 132
    iget v0, p0, Lcom/android/helper/opengl/AffineOpenGLFilter;->program:I

    invoke-static {v0}, Landroid/opengl/GLES20;->glDeleteProgram(I)V

    .line 133
    invoke-static {}, Lcom/android/helper/opengl/GLUtils;->checkGlError()V

    return-void
.end method
