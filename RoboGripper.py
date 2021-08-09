import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

import time, sys, os, curses

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096
right_max = 320
left_max = 480
steer = 400
fwdmax = 650
revmax = 200
inc = 1
go = 400
stop = 400

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

screen = curses.initscr()
curses.noecho()
curses.cbreak()

screen.keypad(True)

on = True

openup = 125
closed = 675
claws = closed
while on:
    char = screen.getch()
    if char == ord('o'):
        claws = claws - 30
        if claws > openup:
            claws = claws
        if claws < openup:
            claws = openup
            
    elif char == ord('c'):
        claws = claws + 30
        if claws < closed:
            claws = claws
        if claws > closed:
            claws = closed
    elif char == ord('q'):
        pwm.set_pwm(0, 0, closed)
        pwm.set_pwm(1, 0, stop)
        go = stop
        on = False
        time.sleep(0.05)
        
    elif char == ord('b'):
        pwm.set_pwm(1, 0, fwdmax)
        time.sleep(2)
        pwm.set_pwm(1,0,revmax)
        time.sleep(2)
        pwm.set_pwm(2, 0, steer)
   
    elif char == ord('t'):
        pwm.set_pwm(1,0, go)
    
    elif char == curses.KEY_UP:
        if go == 400:
            time.sleep(0.2)
        if go < fwdmax:
            go = 407
    elif char == curses.KEY_DOWN:
        if go > revmax:
            go = stop
            pwm.set_pwm(1, 0, go)
            time.sleep(0.05)
            go = 393
            pwm.set_pwm(1, 0, go)
            time.sleep(0.05)
            pwm.set_pwm(1, 0, stop)
            time.sleep(0.05)
            pwm.set_pwm(1, 0, go)
    elif char == curses.KEY_LEFT:
        if steer == left_max:
            steer = steer
            time.sleep(0.1)
        if steer < left_max:
            steer = left_max
    
            
    elif char == curses.KEY_RIGHT:
        if steer == right_max:
            steer = steer
            time.sleep(0.1)
        if steer > right_max:
            steer = right_max
        
                
                
                    
   # pwm.set_pwm(0, 0, claws)
    pwm.set_pwm(1, 0, go)
    pwm.set_pwm(2, 0, steer)
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()


