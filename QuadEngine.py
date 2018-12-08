# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.                            

import socket                   #importing socket library for udp communication
import os                       #importing os library so as to communicate with the system
import time                     #importing time library to make Rpi wait because its too impatient
import pigpio                   #importing GPIO library
import Transceiver              #Custom Transmitter and Receiver Module

class QuadEngine:
    
    def __init__(self):
        self.ESC1 =  4                         #Connect the ESC1 in this GPIO4 pin
        self.ESC2 = 17                         #Connect the ESC2 in this GPIO17 pin
        self.ESC3 = 27                         #Connect the ESC3 in this GPIO27 pin
        self.ESC4 = 22                         #Connect the ESC4 in this GPIO22 pin

        self.pi = pigpio.pi()
        setESCValue(0)

        self.max_value = 2000
        self.min_value = 1000

        self.tr = Transceiver()

        os.system ("sudo pigpiod")      #Launching GPIO library
        time.sleep(1)


    #UDP_IP = "192.168.43.133"       #udp socket ip
    #UDP_PORT = 5005                 #udp socket port

    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.bind((UDP_IP, UDP_PORT))

    def drive(self):
        print ("Select an option from below:")
        print ("1. Calibrate\n 2. Manual\n 3. Control\n 4. Arm\n 5. Stop\n")
        while True:
            print("Waiting for message from sender...")
            choice = tr.receive() # buffer size is 1024 bytes
            if choice == 'manual':
                manual_drive()
                break
            elif choice == 'calibrate':
                calibrate()
                break
            elif choice == 'arm':
                arm()
                break
            elif choice == 'control':
                control()
                break
            elif choice == 'stop':
                stop()
                break
            else :
                print("Invalid input!!")
                continue

    def manual_drive(self): #function to program your ESC if required
        print ("You have selected manual option so give a value between 0 and you max value") 
        while True:
            inp = tr.receive()
            if inp == "stop":
                stop()
                break
            elif inp == "control":
                control()
                break
            elif inp == "arm":
                arm()
                break	
            else:
                self.pi.set_servo_pulsewidth(self.ESC1,inp)
                self.pi.set_servo_pulsewidth(self.ESC2,inp)
                self.pi.set_servo_pulsewidth(self.ESC3,inp)
                self.pi.set_servo_pulsewidth(self.ESC4,inp)
                    
    def calibrate(self):   #This is the auto calibration procedure of a normal ESC
        setESCValue(0)
        while True:
            print("Disconnect the battery and press Enter")
            inp = tr.receive()
            if inp == '':
                print("Setting Max value!")
                setESCValue(self.max_value)
                print("Connect the battery NOW (Falling tone and then short beep) then press Enter")
                inp = input()
                if inp == '':            
                    setESCValue(self.min_value)
                    print ("Special tone")
                    time.sleep(7)
                    print ("Wait....")
                    time.sleep(5)
                    print ("Im working on it.....")
                    setESCValue(0)
                    time.sleep(2)
                    print ("Arming ESC now...")
                    setESCValue(self.min_value)
                    time.sleep(1)
                    control() # Switching to control
                
    def control(self): 
        speed = 1060    # change your speed if you want to.... it should be between 700 - 2000
        print ("Controls - a to decrease speed by 10 || d to increase speed by 10 \n OR \n q to decrease speed by 100 || e to increase speed by 100")
        while True:
            self.pi.set_servo_pulsewidth(self.ESC1, speed)
            self.pi.set_servo_pulsewidth(self.ESC2, speed)
            self.pi.set_servo_pulsewidth(self.ESC3, speed)
            self.pi.set_servo_pulsewidth(self.ESC4, speed)
            
            inp = tr.receive() # buffer size is 1024 bytes
            
            if inp == 'q':
                speed -= 10    # decrementing the speed like hell
                print ("speed = %d" % speed)
            elif inp == 'e':    
                speed += 10    # incrementing the speed like hell
                print ("speed = %d" % speed)
            elif inp == 'd':
                speed += 1     # incrementing the speed 
                print ("speed = %d" % speed)
            elif inp == 'a':
                speed -= 1     # decrementing the speed
                print ("speed = %d" % speed)
            elif inp == 'x':
                stop()          #going for the stop function
                break
            elif inp == b'manual':
                manual_drive()
                break
            elif data == b'arm':
                arm()
                break	
            else:
                print ("Invalid Input!!")
                
    def arm(self): #This is the arming procedure of an ESC 
        print ("Connect the battery and press Enter")
        inp = input()    
        if inp == '':
            setESCValue(0)
            time.sleep(1)
            setESCValue(self.max_value)
            time.sleep(1)
            setESCValue(self.min_value)
            time.sleep(1)
            control() 
            
    def stop(self): #This will stop every action your Pi is performing for ESC ofcourse.
        setESCValue(0)
        self.pi.stop()

    def setESCValue(self, value):
        self.pi.set_servo_pulsewidth(self.ESC1, value)
        self.pi.set_servo_pulsewidth(self.ESC2, value)
        self.pi.set_servo_pulsewidth(self.ESC3, value)
        self.pi.set_servo_pulsewidth(self.ESC4, value)


###########################################Driver Code############################################
qd = QuadEngine()
qd.drive()