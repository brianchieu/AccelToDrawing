package com.example.brian.e6765project;

import android.app.Activity;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import android.bluetooth.BluetoothSocket;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import android.os.Handler;
public class BluetoothActivity extends Activity {

    private static final String TAG = "BluetoothActivity";
    Button On,Off, Connect, Close;
    TextView Version, Count;
    BluetoothSocket Socket;
    BluetoothDevice Device = null;
    BluetoothAdapter Adapter;
    Set<BluetoothDevice> pairedDevices;
    Button clearButton;
    SimpleDrawingView drawView;

    OutputStream outStream = null;
    InputStream inStream = null;
    int x = 270;
    int y = 480;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bluetooth);
        drawView = (SimpleDrawingView) findViewById(R.id.simpleDrawingView1);
        clearButton = (Button) findViewById(R.id.ClearButton);
        clearButton.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                x = 270;
                y = 480;
                drawView.clear();
            }
        });
        /*On.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                try{
                    on(v);
                }
                catch (IOException e){
                    ;
                }
            }
        }); */



        Adapter = BluetoothAdapter.getDefaultAdapter();
        connect();

        final Handler h = new Handler();
        final int delay = 1000;
        h.postDelayed(new Runnable(){
            public void run(){
                //do something
                try {
                    float[] coords = {-1, -1};
                    coords = on();
                    if (coords[0] != -1 && coords[1] != -1) {
                        if( coords[0]*10 + 270 < 540 && coords[0]*10 + 270 > 0)
                            drawView.next_x = (int) (coords[0] * 10) + 270;
                        else if (coords[0]*10 + 270 >= 540)
                            drawView.next_x = 540;
                        else
                            drawView.next_x = 0;

                        if ( coords[1]*10 + 480 < 960 && coords[1]*10+480 > 0)
                            drawView.next_y = (int) (coords[1] * 10) + 480;
                        else if (coords[1]*10 +480 >= 960)
                            drawView.next_y = 960;
                        else
                            drawView.next_y = 0;

                        drawView.redraw();
                    }
                }
                catch (IOException e) {
                    ;
                }
                h.postDelayed(this, delay);
            }
        }, delay);
    }

    //    public void on(View view) throws IOException {
    public float[] on() throws IOException {
        String msg = "ON";
        float[] coords = {-1, -1};
        if (outStream == null) {
            Log.d(TAG, "You have to connect");
            return coords;
        }


        try {
            outStream.write(msg.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
        Log.d(TAG, "LED ON!");


        String c = read(); //Get count from Edison
        String[] numbers = c.split("\n")[0].split(",");
        try {
            coords[0] = Float.parseFloat(numbers[0]);
            coords[1] = Float.parseFloat(numbers[1]);
        }
        catch (Exception e){
            coords[0] = -1;
            coords[1] = -1;
        }
        Log.d("Read", c);
        return coords;
        //Count.setText("Count: " + c);
    }

    public void connect(){//View view){
        pairedDevices = Adapter.getBondedDevices();

        for(BluetoothDevice bt : pairedDevices) {
            if(bt.getName().equals("edison"))
                Device = bt;
        }
        Log.d(TAG, "Address: " + Device.getAddress());
        Log.d(TAG, "Name: "+Device.getName());
        while (true) {
            try {
                BluetoothSocket Socket = Device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805f9b34fb"));

                if (!Socket.isConnected()) {

                    Socket.connect();

                    outStream = Socket.getOutputStream();
                    inStream = Socket.getInputStream();

                    Log.d(TAG, "Connected");
                    break;
                }



                String v = read(); //Get version from Edison

            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    public void close(View view) {
        if (inStream != null) {
            try {inStream.close();} catch (Exception e) {}
            inStream = null;
        }

        if (outStream != null) {
            try {outStream.close();} catch (Exception e) {}
            outStream = null;
        }

        if (Socket != null) {
            try {Socket.close();} catch (Exception e) {}
            Socket = null;
        }
    }

    public String read() throws IOException {
        byte[] buffer = new byte[64];
        inStream.read(buffer);
        String s = new String(buffer);
        return s;
    }

}