package com.robotcar.smart.views;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

import androidx.annotation.Nullable;

/**
 * Custom Joystick View pour contrôler le robot
 */
public class JoystickView extends View {

    private Paint circlePaint;
    private Paint knobPaint;
    private Paint directionPaint;

    private float centerX, centerY;
    private float baseRadius;
    private float knobRadius;
    private float knobX, knobY;

    private boolean isTouching = false;
    private JoystickListener listener;

    public interface JoystickListener {
        void onJoystickMoved(int angle, int strength);
        void onJoystickReleased();
    }

    public JoystickView(Context context) {
        super(context);
        init();
    }

    public JoystickView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        circlePaint = new Paint();
        circlePaint.setColor(Color.parseColor("#40FFFFFF"));
        circlePaint.setStyle(Paint.Style.FILL);
        circlePaint.setAntiAlias(true);

        knobPaint = new Paint();
        knobPaint.setColor(Color.parseColor("#FFC107"));
        knobPaint.setStyle(Paint.Style.FILL);
        knobPaint.setAntiAlias(true);

        directionPaint = new Paint();
        directionPaint.setColor(Color.parseColor("#60FFFFFF"));
        directionPaint.setStyle(Paint.Style.STROKE);
        directionPaint.setStrokeWidth(8f);
        directionPaint.setAntiAlias(true);
    }

    public void setJoystickListener(JoystickListener listener) {
        this.listener = listener;
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        centerX = w / 2f;
        centerY = h / 2f;
        baseRadius = Math.min(w, h) / 2f * 0.8f;
        knobRadius = baseRadius * 0.3f;
        resetKnob();
    }

    private void resetKnob() {
        knobX = centerX;
        knobY = centerY;
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        // Draw base circle
        canvas.drawCircle(centerX, centerY, baseRadius, circlePaint);

        // Draw direction indicators
        float indicatorLength = baseRadius * 0.3f;
        canvas.drawLine(centerX, centerY - indicatorLength,
                centerX, centerY - baseRadius * 0.8f, directionPaint);
        canvas.drawLine(centerX, centerY + indicatorLength,
                centerX, centerY + baseRadius * 0.8f, directionPaint);
        canvas.drawLine(centerX - indicatorLength, centerY,
                centerX - baseRadius * 0.8f, centerY, directionPaint);
        canvas.drawLine(centerX + indicatorLength, centerY,
                centerX + baseRadius * 0.8f, centerY, directionPaint);

        // Draw knob
        canvas.drawCircle(knobX, knobY, knobRadius, knobPaint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        float touchX = event.getX();
        float touchY = event.getY();

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
            case MotionEvent.ACTION_MOVE:
                isTouching = true;
                updateKnobPosition(touchX, touchY);
                break;

            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_CANCEL:
                isTouching = false;
                resetKnob();
                if (listener != null) {
                    listener.onJoystickReleased();
                }
                invalidate();
                break;
        }
        return true;
    }

    private void updateKnobPosition(float touchX, float touchY) {
        float dx = touchX - centerX;
        float dy = touchY - centerY;
        float distance = (float) Math.sqrt(dx * dx + dy * dy);

        // Constrain knob to base circle
        if (distance < baseRadius - knobRadius) {
            knobX = touchX;
            knobY = touchY;
        } else {
            float ratio = (baseRadius - knobRadius) / distance;
            knobX = centerX + dx * ratio;
            knobY = centerY + dy * ratio;
            distance = baseRadius - knobRadius;
        }

        // Calculate angle and strength
        int angle = (int) Math.toDegrees(Math.atan2(dx, -dy));
        if (angle < 0) {
            angle += 360;
        }
        // Convert to -180 to 180 range
        if (angle > 180) {
            angle -= 360;
        }

        int strength = (int) ((distance / (baseRadius - knobRadius)) * 100);

        if (listener != null) {
            listener.onJoystickMoved(angle, strength);
        }

        invalidate();
    }
}
