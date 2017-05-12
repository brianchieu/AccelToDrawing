# AccelToDrawing

> Accelerometer readings are calibrated, filtered, and converted to measurements of displacement in order to visualize the
movement of the accelerometer onto an Android app.  The main technical challenge of the project involved correctly mapping the
actual movement of the pen to the displacement that is read from the accelerometer.  The readings were calibrated by isolating
the acceleration due to gravity from the movement of the pen.  The readings were filtered to readjust the gravity vector and
prevent the position readings from drifting.  These readings were converted to displacement by using a double integral. 
Ultimately, the actual movement of the pen is not accurately mapped from the readings of the accelerometer, but the device
does provide adequate measurements of direction with some of the actual displacement from the pen.

The code base present in this repository can be classified broadly into two:
- An android application, code for which is present under the android directory.
- A server application running on the Intel Edison, code for which is present under the src directory.

### Android Application:

On the client side, an Android app was developed to visualize the position data from the server. The app first tries to open a
Bluetooth RFCOMM socket with the Edison. If the Edison is not listening, it will continuously reattempt to establish a
connection. Once the connection is established, it sends a data get request to get the position data from the Edison. The
received data is parsed and translated to pixel coordinates, where a line is drawn between the previous position and the new
position. This new position is updated for the next set of received data, and the app view is updated accordingly. Once the
view is updated, the app continues the process again beginning from the data get request to the Edison. If the clear button is
pressed at any point, the view is cleared and the drawing begins from its initial position once again.

### Intel Edison:

Two Python scripts are used to handle requests via Bluetooth from the client, and to track the current location of the
accelerometer. The Bluetooth handler is provided in the *SPP_loopback.py* module. This script runs instructions to initialize
the accelerometer and other settings, and then goes into the process. It begins by listening for a Bluetooth connection
request from the Android device. Once the request is heard and the connection is established, it begins to continuously listen
for data requests from the mobile device. Once the request is received, the script reads the data from the queue which
contains the most recent acceleration data and pushes it to the device. Once the data is transmitted to the device, it
continues to listen for further requests.

The acceleration and location tracking script is present in the *accelerometer_data.py* module. This script continuously runs
in a separate thread from the Bluetooth handler. The raw acceleration data is retrieved and filtered continuously over a 0.2
sec interval. The acceleration readings are summed and averaged over that interval, and the displacement and velocity are
calculated based on this average acceleration. The current position and previous velocity are stored, and the position value
is appended to a queue which the handler is able to access. This process repeats from this point.

There are three helper modules used to perform the desired functionality on the server side. 

- *get_accel.py* - This module contains the get_acceleration helper method that reads the raw acceleration and returns
 processed acceleration.
```    
    get_acceleration
    
    This method reads raw acceleration from the accelerometer, removes the noise and effect of gravity
    to provide with the final processed values.
    
    Input:
    myAccel - an object handler to the adxl345 accelerometer
    args - list()
    
    Output:
    x,y,z   - list()
    p_accel - list()


```
