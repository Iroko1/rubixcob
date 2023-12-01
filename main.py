#!/usr/bin/env pybricks-micropython
import random
from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile, Font
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait




#variables
moveset = ["F","F'","F2",
           "R","R'","R2",
           "U","U'","U2",
           "D","D'","D2",
           "L","L'","L2",
           "B","B'","B2"]

restrict = {"B" : ["R","U","L","D"], 
            "L" : ["B","U","F","D"],
            "D" : ["R","B","L","F"],
            "R" : ["U","B","D","F"],
            "U" : ["F","R","B","L"],
            "F" : ["U","R","D","L"]}












#Objects
eve = EV3Brick()
sc = eve.screen
bt = eve.buttons.pressed()
try:
    
    arm = Motor(Port.B,Direction.CLOCKWISE,[12,12])
    base = Motor(Port.A,Direction.COUNTERCLOCKWISE,[12,36])
except:
    eve.screen.clear()
    eve.screen.set_font(Font("Terminal",6,False,True))
    sc.print("Arm Cable -> B\nBase Cable -> A\n Press Center to Continue")
    while True:
        if len(eve.buttons.pressed()) > 0:
            if (eve.buttons.pressed()[-1] == Button.CENTER):
                sc.clear()
                arm = Motor(Port.B,Direction.CLOCKWISE,[12,12])
                base = Motor(Port.A,Direction.COUNTERCLOCKWISE,[12,36])
                break
        else:
            wait(200)
            continue
    
#functions

#easier angle target function use. To shorten function len
def rotate(motor, speed, direction, then=Stop.HOLD, wait=True, reset=False):
    motor.run_target(speed,direction,then,wait)
    if reset:
        motor.reset_angle(0)



#splits the text at specific widths
def wrap(txt,width):
    if not(width >= len(txt)):
        ls = []
        while True:
            if len(txt) > 0:
                ls.append(txt[:width].strip())
                txt = txt[width:]
            else:
                break
    return ls
    

def lsprint(ls):
    for i in ls:
        sc.print(i)
    
def lastid(ls,item):
    ls.reverse()
    for i in range(len(ls)):
        if ls[i][0] == item:
            ls.reverse()
            return True, (i+1)*-1
    ls.reverse()
    return False, 0
    
    
# makes a scramble list (robot instructions)
def scramble(num):
    scramblelist = []
    
    for i in range(num):
        while True:
            move = random.choice(moveset)
            if  len(scramblelist) == 0:
                if move != "D" and move != "D2" and move != "D'":
                    scramblelist.append(move)
                continue
            if move[0] != scramblelist[-1][0]:
                _, index = lastid(scramblelist,move[0])
                stop = False
                if _ :
                    for i in scramblelist[index+1:]:
                        for n in restrict[move[0]]:
                            if i[0] == n:
                                stop = True
                                break
                        if stop:
                            scramblelist.append(move)
                            break
                else:
                    scramblelist.append(move)
                break
    return scramblelist

"""
   ['B',
'L','D','R','U',
    'F']
"""

def y(ls, times = 1, prime = False):
    for i in range(times):
        if prime:
            ls[0], ls[3], ls[5], ls[1] = ls[3], ls[5], ls[1], ls[0]
        else:
            ls[3], ls[5], ls[1], ls[0] = ls[0], ls[3], ls[5], ls[1]
    return ls

def z(ls, times = 1):
    for i in range(times):
        ls[2], ls[1], ls[4], ls[3] = ls[3], ls[2], ls[1], ls[4]
    return ls

rotations = {   '1' : ['y', 'z'],
                '2' : ['y2', 'z'],
                '4' : ['z'],
                '5' : ['z2'],
                '6' : ["y'", 'z']}

cube = [    'B',
        'L','D','R','U',
            'F']

motorrotations = {  'z' : 'f',  
                    'y' : 'r',   
                    'n' : 'br'} 
"""
z -> n always

n/y -> z                n or y will go into z
    if n :              if it is n to z
        up = False      it will alrealy be down
    elif y :            if y into z
        up = True       it will already be up

______________________________________________________

y -> z always
n -> y always

n -> y:
    up = True           arm will always go up for a y move
y -> z:
    up = True           arm will always be left in the up posistion

_______________________________________________________

z -> n always
n -> y/z:
    if y:
        up = True       arm will always go up for a y move
    if z:
        up = False      arm will always be down after a n move

"""
def f(up,times):
    if up:
        arm.run_until_stalled(100,Stop.HOLD)
        arm.reset_angle(0)
    else:
        arm.reset_angle(-70)
    for a in range(times):
        rotate(arm, 200, -80)
        rotate(arm, 2100, -150)
        rotate(arm, 2100, -45)
    rotate(arm,50,-70)
    return
def r(times,prime):
    arm.run_until_stalled(100,Stop.HOLD)
    arm.reset_angle(0)
    if prime:
        x = -1
    else:
        x = 1
    for v in range(times):
        rotate(base, 160, 95*x,Stop.HOLD)
        rotate(base, 160, 90*x,Stop.HOLD)
        base.reset_angle(0)
    return
def n(up,times,prime):
    if up:
        arm.run_until_stalled(100,Stop.HOLD)
        arm.reset_angle(0)
        rotate(arm,100,-70)
    else:
        arm.reset_angle(-70)
    if prime:
        x = 1
    else:
        x = -1
    for m in range(times):
        rotate(base,160,100*x,Stop.HOLD)
        rotate(base,160,90*x,Stop.HOLD)
        base.reset_angle(0)
    return
# Compile the scramble to turns and flips
def comp(ls):
    c = cube.copy()
    lsn = []
    def rttcb(index, ls, cube, face):
        for x in rotations[str(index)]:
            if len(x) > 1 :
                if x[1] == '2' :
                    cube = locals()[x[0]](cube,2)
                    ls.append(x)
                    continue
                elif x[1] == "'" :
                    cube = locals()[x[0]](cube,1,True)
                    ls.append(x)
                    continue
            else:
                cube = locals()[x](cube)
                ls.append(x)
                continue
        ls.append(face)
        return cube, ls
                
            
    for n in range(len(ls)):
        i = c.index(ls[n][0])+1
        if i == 3:
            lsn.append(ls[n])
            continue
        c , lsn = rttcb(i, lsn, c, ls[n])

            
            
    return lsn

# interpret the compiled scramble to "machine code" for the motors
def interpret(ls):
    lsn = []
    move = None
    up = True
    times = 1
    prime = False
    for x in range(len(ls)):
        item = []
        if ls[x][0] == 'z':
            move = f
        elif ls[x][0] == 'y':
            move = r
            up = True
        else:
            move = n
            up = False
        #print(len(ls[x]))
        if len(ls[x]) > 1:
            #print(ls[x][1])
            if ls[x][1] == '2':
                times = 2
                prime = False
            elif ls[x][1] == "'":
                
                times = 1
                prime = True
        else:
            times = 1
            prime = False
        if move == f:
            lsn.append([move,up,times])
        elif move == r:
            lsn.append([move,times,prime])
        else:
            lsn.append([move,up,times,prime])          
    return lsn


'''
#print(interpret(comp(txt)), comp(txt), txt)
up = True

txt = scramble(5)
for x in interpret(comp(txt)):
    if x[0] == f or x[0] == r:
        x[0](x[1],x[2])
    else:
        x[0](x[1],x[2],x[3])
'''


# 1. Make a random scramble depending on which side you put it on for your color scheme 
#       make restriction list to check against
# 2. graphical screen
# 3. settings for different scrambles
# 4. timer with touch sensor
# 5. graphs for times
#       plus times for each scramble, how long it takes it to scramble it
# 6. host a webpage for app version for control over it
# 7. be able to controll it from phone


# Write your program here.

#Define Positions
# Arm up: o*
# Arm down: -33*
# Arm back (to flip): -145*


eve.screen.clear()
eve.screen.set_font(Font("Terminal",6,False,True))
sc.print("Make New Scramble?")

while True:
    
    if len(eve.buttons.pressed()) > 0:
        if (eve.buttons.pressed()[-1] == Button.CENTER):
            sc.clear()
            txt = ' '.join(scramble(20))
            lsprint(wrap(txt,22))
            print(txt)
            for x in interpret(comp(scramble(20))):
                if x[0] == f or x[0] == r:
                    x[0](x[1],x[2])
                else:
                    x[0](x[1],x[2],x[3])
            arm.run_until_stalled(100,Stop.HOLD)
            sc.print("Make New Scramble?")
    else:
        wait(200)
        continue





"""
arm.run_target(50, -30)
arm.run_target(150, -145)
arm.run_target(200, -33)
arm.run_target(50,0)



rotate(base, 100,270)
"""





"""
z - flip
y - rotate
2 - twice
' - counterclockwise

cube =      ['B',
            'L','D','R','U',
            'F']

1 - y, z    ['L',
            'D','B','U','F',
            'R']
            
2 - y2, z   ['F',
            'D','L','U','R',
            'B']
             
4 - z       ['B',
            'D','R','U','L',
            'F']
            
5 - z2      ['B',
            'R','U','L','D',
            'F']
            
6 - y', z   ['R',
            'D','F','U','B',
            'L']




"""