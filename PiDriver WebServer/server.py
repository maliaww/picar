from flask import Flask
from flask import (
    jsonify,
    render_template,
    request,
    Response
)
import picamera
import RPi.GPIO as GPIO
import time
import io

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

forward =21
back = 26 
speed = 19

left = 20
right = 16
amplitude = 12

GPIO.setup(forward, GPIO.OUT)
GPIO.setup(back, GPIO.OUT)
GPIO.setup(speed, GPIO.OUT)

GPIO.setup(right, GPIO.OUT)
GPIO.setup(left, GPIO.OUT)
GPIO.setup(amplitude, GPIO.OUT)

# Set up PWM pins for motor control
pi_pwm1 = GPIO.PWM(speed, 100)
pi_pwm1.start(100)

pi_pwm2 = GPIO.PWM(amplitude, 100)
pi_pwm2.start(100)

# Create Flask app
app = Flask(__name__)

# Set up route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Set up route for processing incoming data from joystick
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # Get JSON data from request
    num = (data[list(data.keys())[0]])  # Extract number value from JSON data
    value = (data[list(data.keys())[1]])  # Extract value from JSON data
    global last  # Declare last variable as a global variable to track previous motor direction

    # If joystick is pushed to the left or right
    if value < 1 and num == 1:
        if (value < -0.3 or value > 0.3):
            
            # If joystick is pushed to the left
            if value < 0:
                GPIO.output(right, GPIO.LOW)  # Turn right motor off
                GPIO.output(left, GPIO.HIGH)  # Turn left motor on

            # If joystick is pushed to the right
            if value > 0.14:
                GPIO.output(right, GPIO.HIGH)  # Turn right motor on
                GPIO.output(left, GPIO.LOW)  # Turn left motor off

        # If joystick is centered
        else:
            GPIO.output(right, GPIO.LOW)  # Turn right motor off
            GPIO.output(left, GPIO.LOW)  # Turn left motor off

                
    # If joystick is pushed forward
    if num == 8 and value > 0:
        last = "forward"  # Update last variable to track previous motor direction
        speed = value  * 100  # Convert joystick value to duty cycle percentage for motor control
        pi_pwm1.ChangeDutyCycle(speed)  # Set motor speed using PWM
        GPIO.output(forward, GPIO.HIGH)  # Turn forward motor on
        GPIO.output(back, GPIO.LOW)  # Turn backward motor off

    # If joystick is released
    if num == 8 and value ==0:
        GPIO.output(forward, GPIO.LOW)  # Turn forward motor off
 
    # If joystick is pushed backward
    if num == 7 and value > 0:
        last = "back"  # Update last variable to track previous motor direction
        speed = value * 100  # Convert joystick value to duty cycle percentage for motor control
        pi_pwm1.ChangeDutyCycle(speed) # Set the speed of the motor using PWM
        GPIO.output(forward, GPIO.LOW) # Turn forward motor off
        GPIO.output(back, GPIO.HIGH) # Turn back motor on

    # If joystick is in neutral position
    if num == 7 and value == 0:
        GPIO.output(back, GPIO.LOW) # Turn back motor off
         
    # If joystick is pushed forward
    if num == 7 and value < 0:
        last = "forward" # Update last variable to track previous motor direction
        speed = abs(value) * 100 # Convert joystick value to speed percentage
        pi_pwm1.ChangeDutyCycle(speed) # Set the speed of the motor using PWM
        GPIO.output(back, GPIO.LOW) # Turn back motor off
        GPIO.output(forward, GPIO.HIGH) # Turn forward motor on

# If joystick is pushed left or right
    if num == 6:
        if last == "forward": # If the last direction was forward
            pi_pwm1.ChangeDutyCycle(100) # Set the speed to maximum
            GPIO.output(forward, GPIO.LOW) # Turn forward motor off
            GPIO.output(back, GPIO.HIGH) # Turn back motor on
            time.sleep(0.5) # Wait for 0.5 seconds
            GPIO.output(back, GPIO.LOW) # Turn back motor off
        if last == "back": # If the last direction was back
            pi_pwm1.ChangeDutyCycle(100) # Set the speed to maximum
            GPIO.output(back, GPIO.LOW) # Turn back motor off
            GPIO.output(forward, GPIO.HIGH) # Turn forward motor on
            time.sleep(0.5) # Wait for 0.5 seconds
            GPIO.output(forward, GPIO.LOW) # Turn forward motor off
    return jsonify(message='Success', stickdata=data)

def gen():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 24
        camera.rotation = 180
        # Set the video format to be JPEG
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            stream.seek(0)
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n\r\n')
        stream.seek(0)
        stream.truncate()

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
mimetype='multipart/x-mixed-replace; boundary=frame')

if name == 'main':
    app.run(debug=True, port=8080, host='raspberrypi.local')