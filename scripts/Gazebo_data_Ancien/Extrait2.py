#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re





inFile = open("Gazebo_Forces_V8.txt")
outFile = open("result.txt", "w")
#buffer = []
#keepCurrentSet = True
for line in inFile:
#    buffer.append(line)
    if re.search("front_right_wheel", line):
        #---- starts a new data set
#        line = inFile.next()
        outFile.write(line)
        #now reset our state
#        buffer = []
inFile.close()
outFile.close()
#
#
#
with open(r'result.txt', 'r') as infile, \
     open(r'Fy2_front_left_V8.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace(', collision_1: "spido::front_right_wheel::front_right_wheel_collision"', "")
    data = data.replace("force: ", "\n")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace('collision_1: "spido::front_right_wheel::front_right_wheel_collision"', "")
    outfile.write(data)
    
    
with open("Fy2_front_left_V8.txt","r") as f, open("PLOT/Fy_rear_left_V8.txt","w") as outfile:
 for i in f.readlines():
       if not i.strip():
           continue
       if i:
           outfile.write(i)   


########################################"%%%%%%%%%%%%%%%%%%%%

inFile = open("Gazebo_Forces_V8.txt")
outFile = open("resultt.txt", "w")
#buffer = []
#keepCurrentSet = True
for line in inFile:
#    buffer.append(line)
    if re.search("rear_right_wheel", line):
        #---- starts a new data set
#        line = inFile.next()
        outFile.write(line)
        #now reset our state
#        buffer = []
inFile.close()
outFile.close()
#
#
#
with open(r'resultt.txt', 'r') as infile, \
     open(r'Fy3_front_left_V8.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace("force: -0.0,", "")
    data = data.replace("force: 0.0,", "")
    data = data.replace(', collision_1: "spido::front_left_wheel::front_left_wheel_collision"', "")
    data = data.replace('collision_1: "spido::rear_right_wheel::rear_right_wheel_collision"', "")
    data = data.replace("force: ", "\n")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace(",", "")
    data = data.replace('collision_1: "spido::front_left_wheel::front_left_wheel_collision"', "")
    outfile.write(data)
    
    
with open("Fy3_front_left_V8.txt","r") as f, open("PLOT/Fy_front_right_V8.txt","w") as outfile:
 for i in f.readlines():
       if not i.strip():
           continue
       if i:
           outfile.write(i) 