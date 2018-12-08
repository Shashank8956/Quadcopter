# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.                            

import socket                   #importing socket library for udp communication
import os                       #importing os library so as to communicate with the system
import time                     #importing time library to make Rpi wait because its too impatient

os.system ("sudo pigpiod")      #Launching GPIO library
time.sleep(1)

import pigpio                   #importing GPIO library

ESC1=4                          #Connect the ESC1 in this GPIO4 pin
ESC2=17                         #Connect the ESC2 in this GPIO17 pin
ESC3=27                         #Connect the ESC3 in this GPIO27 pin
ESC4=22                         #Connect the ESC4 in this GPIO22 pin

UDP_IP = "192.168.43.133"       #udp socket ip
UDP_PORT = 5005                 #udp socket port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)
pi.set_servo_pulsewidth(ESC3, 0)
pi.set_servo_pulsewidth(ESC4, 0) 

max_value = 2000
min_value = 1000

print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")

def manual_drive(): #function to program your ESC if required
    print ("You have selected manual option so give a value between 0 and you max value") 
    while True:
        inp = input()
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
            pi.set_servo_pulsewidth(ESC1,inp)
            pi.set_servo_pulsewidth(ESC2,inp)
            pi.set_servo_pulsewidth(ESC3,inp)
            pi.set_servo_pulsewidth(ESC4,inp)
                
def calibrate():   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0) 
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC1, max_value)
        pi.set_servo_pulsewidth(ESC2, max_value)
        pi.set_servo_pulsewidth(ESC3, max_value)
        pi.set_servo_pulsewidth(ESC4, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)
            print ("Special tone")
            time.sleep(7)
            print ("Wait....")
            time.sleep(5)
            print ("Im working on it.....")
            pi.set_servo_pulsewidth(ESC1, 0)
            pi.set_servo_pulsewidth(ESC2, 0)
            pi.set_servo_pulsewidth(ESC3, 0)
            pi.set_servo_pulsewidth(ESC4, 0) 
            time.sleep(2)
            print ("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)
            time.sleep(1)
            control() # Switching to control
            
def control(): 
    speed1 = 1200    # change your speed if you want to.... it should be between 700 - 2000
    speed2 = 1200
    print ("Controls - a to decrease speed by 10 || d to increase speed by 10 \n OR \n q to decrease speed by 100 || e to increase speed by 100")
    while True:
        pi.set_servo_pulsewidth(ESC1, speed1)
        pi.set_servo_pulsewidth(ESC2, speed2)
        pi.set_servo_pulsewidth(ESC3, speed2)
        pi.set_servo_pulsewidth(ESC4, speed1)
        
        data,_ = sock.recvfrom(1024) # buffer size is 1024 bytes
        
        if data == b'q':
            speed1 -= 10    # decrementing the speed Anticlockwise
            print("Anticlockwise")
            print ("AC speed = %d" % speed1)
            print ("CW speed = %d" % speed2)
        elif data == b'e':    
            speed1 += 10    # incrementing the speed Anticlockwise
            print("Anticlockwise")
            print ("AC speed = %d" % speed1)
            print ("CW speed = %d" % speed2)
        elif data == b'd':
            speed2 += 10     # incrementing the speed Clockwise
            print("Clockwise")
            print ("AC speed = %d" % speed1)
            print ("CW speed = %d" % speed2)
        elif data == b'a':
            speed2 -= 10     # decrementing the speed Clockwise
            print("Clockwise")
            print ("AC speed = %d" % speed1)
            print ("CW speed = %d" % speed2)
        elif data == b'z':
            speed1 -= 10
            speed2 -= 10     # decrementing the speed Both
            print("Both")
            print ("AC speed = %d" % speed1)
            print ("CW speed = %d" % speed2)
        elif data == b'c':
            speed1 += 10
            speed2 += 10     # incrementing the speed Both
            print("Both")
            print ("AC speed = %d" % speed1)
            print ("CW speed = %d" % speed2)
        elif data == b'x':
            stop()          #going for the stop function
            break
        elif data == b'manual':
            manual_drive()
            break
        elif data == b'arm':
            arm()
            break	
        else:
            print ("Invalid Input!!")
            
def arm(): #This is the arming procedure of an ESC 
    print ("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC1, 0)
        pi.set_servo_pulsewidth(ESC2, 0)
        pi.set_servo_pulsewidth(ESC3, 0)
        pi.set_servo_pulsewidth(ESC4, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, max_value)
        pi.set_servo_pulsewidth(ESC2, max_value)
        pi.set_servo_pulsewidth(ESC3, max_value)
        pi.set_servo_pulsewidth(ESC4, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC1, min_value)
        pi.set_servo_pulsewidth(ESC2, min_value)
        pi.set_servo_pulsewidth(ESC3, min_value)
        pi.set_servo_pulsewidth(ESC4, min_value)
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)
    pi.stop()


while True:
    print("Waiting for message from sender...")
    data,_ = sock.recvfrom(1024) # buffer size is 1024 bytes
    if data == b'manual':
        manual_drive()
        break
    elif data == b'calibrate':
        calibrate()
        break
    elif data == b'arm':
        arm()
        break
    elif data == b'control':
        control()
        break
    elif data == b'stop':
        stop()
        break
    else :
        print("Invalid input!!")
        continue


