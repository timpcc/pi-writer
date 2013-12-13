import requests
import time
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(24, GPIO.OUT) # LED output
# connect switch on pin 25 to GND
#GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Input button to toggle status - pull up

import threading
import ctypes

class NetworkThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, timePeriod):
        super(NetworkThread, self).__init__()
        self._stop = threading.Event()
        self._waitPeriod = timePeriod
        self._active = True
        self._lastResult = False
        #GPIO.add_event_detect(25, GPIO_FALLING, callback=self.toggle, bouncetime=500)

    def toggle(self):
        # toggle the active status
        self._active = not self._active;

    def stop(self):
        print("Attempting to stop networking thread...")
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            if (self._active):
                # flash the pin
                #if GPIO.output(24) == True:
                    #GPIO.output(24, GPIO.LOW) # turn the LED off
                #    time.sleep(0.1)
                    #GPIO.output(24, GPIO.HIGH) # turn the LED on
                #else:
                    #GPIO.output(24, GPIO.HIGH) # turn the LED on
                #    time.sleep(0.1)
                    #GPIO.output(24, GPIO.LOW) # turn the LED off

                # check the status
                response = requests.get('http://google.com')
                if response.status_code == requests.codes.ok:
                    #GPIO.output(24, GPIO.LOW) # turn the LED off
                    #print("success")
                    # record this result
                    self._lastResult = True
                else:
                    # result was failure - turn the LED on
                    #GPIO.output(24, GPIO.HIGH)
                    self._lastResult = False
                    print("failure")
                time.sleep(self._waitPeriod)
        print("Network thread stopped")
        self._stop.clear()

    
