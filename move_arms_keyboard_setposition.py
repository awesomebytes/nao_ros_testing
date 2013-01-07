#! /usr/bin/env python

# move arms with keyboard in X,Y axis

from __future__ import division
import sys
import time
from naoqi import ALProxy
import motion

import Tkinter as tk # for capturing keyboard


def moveEffector(effector):
  global motionProxy
  global postureProxy
  global x_
  global y_
  global z_
  global wx_
  global wy_
  global wz_

  positionChange = [x_, y_, z_, wx_, wy_, wz_]
  print "NewPos: " + str(positionChange)
  effectorName     = effector
  space            = motion.FRAME_ROBOT
  fractionMaxSpeed = 0.8
  axisMask       = 63

  motionProxy.post.setPosition(effectorName, space, positionChange, fractionMaxSpeed, axisMask)


def mouse_wheelCallback(event):
  global motionProxy
  global postureProxy
  global x_
  global y_
  global z_
  global wx_
  global wy_
  global wz_

  print "Pressed mouse: " + str(event.num)
  # respond to Linux or Windows wheel event
  if event.num == 5 or event.delta == -120: # scroll down
    print "mousewheel scroll down"
    z_ = z_ - 0.02
    moveEffector("RArm")
  if event.num == 4 or event.delta == 120: # scroll up
    print "mousewheel scroll up"
    z_ = z_ + 0.02
    moveEffector("RArm")
  if event.num == 9: # lateral front mouse key
    wy_ = wy_ + 3.14/16
    moveEffector("Torso")
  if event.num == 8: # lateral back key
    wy_ = wy_ - 3.14/16
    moveEffector("Torso")

  if event.num == 6: # to the left scroll button
    wx_ = wx_ + 3.14/16
    moveEffector("Torso")
  if event.num == 7: # to the right scroll button
    wx_ = wx_ - 3.14/16
    moveEffector("Torso")


def keyCallback(event):
  global motionProxy
  global postureProxy
  global x_
  global y_
  global z_
  global wx_
  global wy_
  global wz_


  if event.keysym == 'Escape': # Exit if we press Esc, sit the robot
    postureProxy.goToPosture("Sit", 0.5)
    root.destroy()

  if event.char == event.keysym: # normal number and letter characters
    print( 'Normal Key %r' % event.char )
  elif len(event.char) == 1: # charcters like []/.,><#$ also Return and ctrl/key
    print( 'Punctuation Key %r (%r)' % (event.keysym, event.char) )
  else: # f1 to f12, shift keys, caps lock, Home, End, Delete ...
    print( 'Special Key %r' % event.keysym )
    if event.keysym == 'Up':
      x_ = x_ + 0.02
    elif event.keysym == 'Down':
      x_ = x_ - 0.02
    elif event.keysym == 'Left':
      y_ = y_ + 0.02
    elif event.keysym == 'Right':
      y_ = y_ - 0.02

    positionChange = [x_, y_, z_, wx_, wy_, wz_]
    print "NewPos: " + str(positionChange)
    #print "Move RArm 1"
    effectorName     = "RArm"
    space            = motion.FRAME_ROBOT
    fractionMaxSpeed = 0.8
    axisMask         = 7
    motionProxy.post.setPosition(effectorName, space, positionChange, fractionMaxSpeed, axisMask)



#robotIP = "169.254.232.52"
robotIP = "127.0.0.1"
PORT = 9559
global motionProxy
global postureProxy
global x_
global y_
global z_
global wx_
global wy_
global wz_

x_ = y_ = z_ = wx_ = wy_ = wz_ = 0.0
try:
  motionProxy = ALProxy("ALMotion", robotIP, PORT)
except Exception,e:
  print "Could not create proxy to ALMotion"
  print "Error was: ",e
  sys.exit(1)

try:
  postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
except Exception, e:
  print "Could not create proxy to ALRobotPosture"
  print "Error was: ", e

postureProxy.goToPosture("StandInit", 0.5)




root = tk.Tk()
print( "Press a key (Escape key to exit):" )
root.bind('<KeyPress>', keyCallback)
# with Windows OS
root.bind("<MouseWheel>", mouse_wheelCallback)
# with Linux OS
root.bind("<ButtonPress>", mouse_wheelCallback)

print "Press Up/Down arrow keys to Move in X"
print "Press Left/Right to move in Y"
print "Use mousewheel scroll up/down to move in Z (over the window)"


root.mainloop()