package com.android.helper;

import android.content.AttributionSource;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraConstrainedHighSpeedCaptureSession;
import android.hardware.camera2.params.OutputConfiguration;
import android.hardware.camera2.params.SessionConfiguration;
import android.media.AudioRecord;
import android.view.Surface;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;

/* JADX INFO: compiled from: D8$$SyntheticClass */
/* JADX INFO: loaded from: classes.dex */
public final /* synthetic */ class FakeContext$$ExternalSyntheticApiModelOutline0 {
    public static /* synthetic */ AttributionSource.Builder m(int i) {
        return new AttributionSource.Builder(i);
    }

    public static /* bridge */ /* synthetic */ CameraConstrainedHighSpeedCaptureSession m(Object obj) {
        return (CameraConstrainedHighSpeedCaptureSession) obj;
    }

    public static /* synthetic */ OutputConfiguration m(Surface surface) {
        return new OutputConfiguration(surface);
    }

    public static /* synthetic */ SessionConfiguration m(int i, List list, Executor executor, CameraCaptureSession.StateCallback stateCallback) {
        return new SessionConfiguration(i, list, executor, stateCallback);
    }

    public static /* synthetic */ AudioRecord.Builder m() {
        return new AudioRecord.Builder();
    }

    public static /* bridge */ /* synthetic */ Class m() {
        return AttributionSource.class;
    }

    public static /* synthetic */ CompletableFuture m() {
        return new CompletableFuture();
    }

    public static /* synthetic */ void m() {
    }
}
