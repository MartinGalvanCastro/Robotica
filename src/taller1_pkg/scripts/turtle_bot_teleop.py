#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import rospy
import rostopic
import traceback
from geometry_msgs.msg import Twist
from pynput.keyboard import Key, Listener

msgLin = 0.0
msgAng = 0.0
acc = []
acabo = False
guardar = False
recoFile=""

def teleop(vLin, vAng):
    global msgLin
    global msgAng
    global recoFile
    global guardar
    pub = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size=5)
    rospy.init_node('turtle_bot_teleop')
    rate = rospy.Rate(10)

    res1 = input("Desea guardar el recorrido del robot? [Y/N]: ")
    if res1 == 'y' or res1 == 'Y':
        guardar = True
        recoFile = input("Nombre del archivo que desea guardar (sin .txt): ") + ".txt"

    listener = Listener(on_press = actVel, on_release = parar)
    listener.start()

    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = msgLin*vLin
        msg.angular.z = msgAng*vAng
        pub.publish(msg)
        rate.sleep()
        if(acabo):
            rospy.on_shutdown(Hook)
            listener.stop()

def Hook():
    print("apagar")

def actVel(key):
    global msgLin
    global msgAng
    global acabo
    acc.append(key)

    if key == Key.up:
        msgLin = 1

    elif key == Key.down:
        msgLin = -1

    elif key == Key.left:
        msgAng = 1

    elif key == Key.right:
        msgAng = -1

    if key == Key.esc:
        acabo = True
        return False

def parar(key):
    global msgLin
    global msgAng
    msgLin = 0.0
    msgAng = 0.0

if __name__ == '__main__':
    try:
        vLin = float(input('Introduzca la velocidad lineal deseada (Máximo: 70cm/s): '))
        vAng = float(input('Introduzca la velocidad angular deseada (Máximo: 180°/s): '))
        teleop(vLin, vAng)
    except rospy.ROSInterruptException:
        track = traceback.format_exc()
        print(track)
    finally:
        if guardar:
            f = open(recoFile, "w")
            for k in acc:
                f.write("{}\n".format(k))
            f.close()
        