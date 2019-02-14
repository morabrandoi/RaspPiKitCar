################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
# MUST USE PYTHON 2
import math
import requests
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:
            if hand.is_left:
                break

            handType = "Right hand"
            # we dont need z
            x = hand.palm_position[0]
            y = hand.palm_position[1]
            x = max(-1.0, min(x / 200, 1.0))
            y = max(-1.0, min((y-250) / 150, 1.0))
            print(x,y)
            left_speed, right_speed = map_to_left_right(x, y)
            POST_to_car(left_speed, right_speed)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

# expects Range (-1,1), Domain (-1,1)
def clip_angles_to_circle(x, y):
    radius = math.hypot(x, y)
    if radius >= 1:
        radius = 1
    angle = math.atan2(y, x)
    return (radius, angle)

def map_to_left_right(hand_x, hand_y):
    radius, theta = clip_angles_to_circle(hand_x, hand_y)

    x = radius * math.cos(theta)
    y = radius * math.sin(theta)

    u = (x * math.cos(-1 * math.pi / 4)) - (y * math.sin(-1 * math.pi / 4))
    v = (y * math.cos(-1 * math.pi / 4)) + (x * math.sin(-1 * math.pi / 4))

    u2 = u * u
    v2 = v * v
    twosqrt2 = 2.0 * math.sqrt(2.0)
    subtermx = 2.0 + u2 - v2
    subtermy = 2.0 - u2 + v2
    termx1 = subtermx + u * twosqrt2
    termx2 = subtermx - u * twosqrt2
    termy1 = subtermy + v * twosqrt2
    termy2 = subtermy - v * twosqrt2

    epsilon = 0.0001
    if abs(termx2) < epsilon:
        termx2 = 0.0
    if abs(termy2) < epsilon:
        termy2 = 0.0
    if abs(termx1) < epsilon:
        termx1 = 0.0
    if abs(termy1) < epsilon:
        termy1 = 0.0

    left_motor_speed = 0.5 * math.sqrt(termx1) - 0.5 * math.sqrt(termx2)
    right_motor_speed = 0.5 * math.sqrt(termy1) - 0.5 * math.sqrt(termy2)
    # both speeds are in range (-1,1) at this point

    return (left_motor_speed, right_motor_speed)


def POST_to_car(left, right):
    r = requests.post("http://192.168.4.1:80", data={'left': left, 'right': right})

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        r = requests.post("http://192.168.4.1:80", data={'left': 0, 'right': 0})
        pass
    finally:
        # Remove the sample listener when done
        r = requests.post("http://192.168.4.1:80", data={'left': 0, 'right': 0})
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
