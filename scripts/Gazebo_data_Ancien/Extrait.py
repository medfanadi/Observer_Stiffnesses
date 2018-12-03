#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re





#inFile = open("Gazebo_Forces_V5.txt")
#outFile = open("result.txt", "w")
##buffer = []
##keepCurrentSet = True
#for line in inFile:
##    buffer.append(line)
#    if re.search("force:", line):
#        #---- starts a new data set
##        line = inFile.next()
#        outFile.write(line)
#        #now reset our state
##        buffer = []
#inFile.close()
#outFile.close()
#
#
#
#with open(r'result.txt', 'r') as infile, \
#     open(r'PLOT/Y_forces_V5', 'w') as outfile:
#    data = infile.read()
#    data = data.replace("[force: 0.0]", "")
#    data = data.replace("force: ", "\n")
#    data = data.replace("[", "")
#    data = data.replace("]", "")
#    data = data.replace(",", "")
#    outfile.write(data)
#    
    
    



 ###############################################################################
inFile = open("Gazebo_model_V8.txt")
outFile = open("result2.txt", "w")
#buffer = []
#keepCurrentSet = True
for line in inFile:
#    buffer.append(line)
    if re.search("z:", line):
        #---- starts a new data set
#        line = inFile.next()
        outFile.write(line)
        #now reset our state
#        buffer = []
inFile.close()
outFile.close()


with open(r'result2.txt', 'r') as infile, \
     open(r'PLOT/Vpsi_Gazebo_V8.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace("[linear:", "")
    data = data.replace("x: 0.0", "")
    data = data.replace("y: 0.0", "")
    #data = data.replace("z: 0.0", "")
    #data = data.replace("z: 0.0,", "")
    data = data.replace("linear:", "")
    data = data.replace("angular:", "")
    data = data.replace(",", "")
    data = data.replace("  y: ", "")
    data = data.replace("]", "")
    data = data.replace("]", "")
    data = data.replace("  z: ", "")
    outfile.write(data)


 ###############################################################################
inFile = open("Gazebo_model_V8.txt")
outFile = open("result3.txt", "w")
#buffer = []
#keepCurrentSet = True
for line in inFile:
#    buffer.append(line)
    if re.search("y:", line):
        #---- starts a new data set
#        line = inFile.next()
        outFile.write(line)
        #now reset our state
#        buffer = []
inFile.close()
outFile.close()


with open(r'result3.txt', 'r') as infile, \
     open(r'PLOT/Vy_Gazebo_V8.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace("[linear:", "")
    data = data.replace("x: 0.0", "")
    #data = data.replace("y: 0.0", "")
    data = data.replace("z: 0.0", "")
    data = data.replace("z: 0.0,", "")
    data = data.replace("linear:", "")
    data = data.replace("angular:", "")
    data = data.replace(",", "")
    data = data.replace("  y: ", "")
    data = data.replace("]", "")
    data = data.replace("]", "")
    data = data.replace("  x: ", "")
    outfile.write(data)
    


 ###############################################################################
inFile = open("Gazebo_model_V8.txt")
outFile = open("result4.txt", "w")
#buffer = []
#keepCurrentSet = True
for line in inFile:
#    buffer.append(line)
    if re.search("x:", line):
        #---- starts a new data set
#        line = inFile.next()
        outFile.write(line)
        #now reset our state
#        buffer = []
inFile.close()
outFile.close()


with open(r'result3.txt', 'r') as infile, \
     open(r'PLOT/Vx_Gazebo_V8.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace("  x: ", "")
    outfile.write(data)