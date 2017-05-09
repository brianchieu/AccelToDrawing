package com.example.brian.e6765project;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.view.View;

/**
 * Created by Brian on 5/4/2017.
 */

public class SimpleDrawingView extends View {
    // setup initial color
    private final int paintColor = Color.BLACK;
    private Path path;
    // defines paint and canvas
    private Paint drawPaint;
    public int current_x = 270, current_y = 480;
    public int next_x = 270, next_y = 480;
    public boolean clear = false;
    public SimpleDrawingView(Context context, AttributeSet attrs) {
        super(context, attrs);
        setFocusable(true);
        setFocusableInTouchMode(true);
        setupPaint();
    }

    // Setup paint with color and stroke styles
    private void setupPaint() {
        drawPaint = new Paint();
        drawPaint.setColor(paintColor);
        drawPaint.setAntiAlias(true);
        drawPaint.setStrokeWidth(5);
        drawPaint.setStyle(Paint.Style.STROKE);
        drawPaint.setStrokeJoin(Paint.Join.ROUND);
        drawPaint.setStrokeCap(Paint.Cap.ROUND);

        path = new Path();
    }

    public void redraw(){
        invalidate();
    }

    public void clear(){
        clear = true;
        current_x = 270;
        current_y = 480;
        next_x = 270;
        next_y= 480;
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        if (clear) {
            clear = false;
            path.reset();
            canvas.drawColor(Color.WHITE);
        }
        else {
            path.moveTo(current_x, current_y);
            path.lineTo(next_x, next_y);
            current_x = next_x;
            current_y = next_y;
            canvas.drawPath(path, drawPaint);
        }
    }
}
