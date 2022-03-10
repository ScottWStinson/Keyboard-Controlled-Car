import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

import time, sys, os, curses

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096
right_max = 320
left_max = 480
steer = 400
fwdmax = 450
revmax = 350
inc = 1
incs = 5
go = 400
stop = 400
ch0 = 0
ch1 = 1

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

screen = curses.initscr()
curses.noecho()
curses.cbreak()

screen.keypad(True)

on = True

while on:
    char = screen.getch()

    if char == ord('q'):
        pwm.set_pwm(ch0, 0, stop)
        print(" \r", ch0, ' ', stop)
        go = stop
        on = False
        time.sleep(0.05)

    elif char == ord('b'):
        pwm.set_pwm(ch0, 0, fwdmax)
        print(" \r", ch0, ' ', fwdmax)
        time.sleep(2)
        pwm.set_pwm(ch0, 0, revmax)
        print(" \r", ch0, ' ', revmax)
        time.sleep(2)
        pwm.set_pwm(ch1, 0, steer)
        print(" \r", ch1, ' ', steer)

    elif char == ord('z'):
        go, steer = stop, stop

    elif char == curses.KEY_UP:
        if go >= fwdmax:
            go = go
        elif go < fwdmax:
            go += inc
    elif char == curses.KEY_DOWN:
        if go <= revmax:
            go = revmax
        elif go > revmax and go > stop:
            go -= inc
        elif go > revmax and go < stop:
            go -= inc
        elif go == stop:
            pwm.set_pwm(ch0, 0, go)
            print(" \r", ch0, ' ', go)
            time.sleep(0.05)
            go -= inc
            pwm.set_pwm(ch0, 0, go)
            print(" \r", ch0, ' ', go)
            time.sleep(0.05)
            pwm.set_pwm(ch0, 0, stop)
            print(" \r", ch0, ' ', stop)
            time.sleep(0.05)
            pwm.set_pwm(ch0, 0, go)
            print(" \r", ch0, ' ', go)

    elif char == curses.KEY_LEFT:
        if steer == left_max:
            steer = steer
            time.sleep(0.1)
        if steer < left_max:
            steer += incs

    elif char == curses.KEY_RIGHT:
        if steer == right_max:
            steer = steer
            time.sleep(0.1)
        if steer > right_max:
            steer -= incs

    pwm.set_pwm(ch0, 0, go)
    print(" \r", ch0, ' ', go, ch1, ' ', steer)
    pwm.set_pwm(ch1, 0, steer)

curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
