#L-Code: The first firmware for Lego 3D printer architectures
#The latest version is version 1.7.3

#package imports
import time, force_sensor, motor
from hub import light_matrix, port

#Port A: X
#Port B: Y
#Port C and D: Z
#Port E: E
#Port F: BLS
#motor max speed: 135rpm (810deg/sec)
#each rotation of E: 36.7566mm (circumference of wheel)
#e constant is 9.79416 (degrees per millimeter using a 12t lego double bevel wheel)
#efeed will be taken in millimeters and millimeters per second

#G00: move in XY
#G01: move in Z
#G02: move independent Z motor
#G07: extruder movement
#G15: motor calibration
#G27: independent axis \homing
#G28: home all axes using force sensor
#G29: 3x3 auto leveling
#G34: Z axis alignment

#variable globalization

global xpos
global ypos
global zposC
global zposD
global iniz
global iniz2

#variable definitions

xpos=0
ypos=0
zposC=0
zposD=0
xlength=2100
ylength=2100
iniz=0
iniz2=0
motoron=0
etemp=20
ettemp=20
btemp=20
bttemp=20
flist=["PLA", "PETG", "ABS", "ASA", "PC", "PA", "TPU"]
tlist=[205, 250, 235, 245, 270, 285, 225]
tlist2=[60, 75, 105, 105, 110, 75, 45]
absolute=0

#function definitions

def convert(ttc):
  m=0
  h=0
  while ttc>=60:
    if ttc>=60:
      m+=1
      ttc-=60
      continue
    if m>=60:
      h+=1
      m-=60
      continue
  s=ttc
  s=round(s,2)
  if s<10:
    s="0"+str(s)
  if m<10:
    m="0"+str(m)
  if h<10:
    h="0"+str(h)
  ct=str(h)+":"+str(m)+":"+str(s)
  return(ct)

def probe():
  global motoron
  if motoron==1:
    while force_sensor.force(port.F)<=80:
      G01(-2, 20, 0, 0)
      time.sleep(0.2)
  else:
    print("Motors disabled")

def probe1():
  global iniz2, motoron
  if motoron==1:
    iniz2=0
    while force_sensor.force(port.F)<=80:
      G01(-2, 20, 0, 0)
      iniz2+=2
      time.sleep(0.2)
  else:
    print("Motors disabled")

def measure():
  probe1()
  G01(iniz2, 20, 0, 0)

def G00(x, y, feed, length, efeed):
  global xpos, ypos, zposC, zposD, motoron, absolute
  if motoron==1:
    if absolute==0:
      if x>0:
        motor.run_for_degrees(port.A, x, feed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.A, x, -feed)
        G07(length, efeed)
      if y>0:
        motor.run_for_degrees(port.B, y, feed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.B, y, -feed)
        G07(length, efeed)
      xpos+=x
      ypos+=y
    else:
      xn=x-xpos
      yn=y-ypos
      if xn>0:
        motor.run_for_degrees(port.A, xn, feed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.A, xn, -feed)
        G07(length, efeed)
      if yn>0:
        motor.run_for_degrees(port.B, yn, feed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.B, yn, -feed)
        G07(length, efeed)
      xpos+=xn
      ypos+=yn
    print("G00 X",x,"Y",y,"F",feed,"EF",efeed,"E",length)
    print("New Position: X",xpos,"Y",ypos,"ZC",zposC,"ZD",zposD)
    light_matrix.write("G00")
  else:
    print("Motors disabled")

def G01(z, feed, length, efeed):
  global xpos, ypos, zposC, zposD, motoron, absolute
  if motoron==1:
    if absolute==0:
      if z>0:
        motor.run_for_degrees(port.C, z, -feed)
        motor.run_for_degrees(port.D, z, feed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.C, z, feed)
        motor.run_for_degrees(port.D, z, -feed)
        G07(length, efeed)
      zposC+=z
      zposD+=z
    else:
      zn=z-zposC
      znn=z-zposD
      if z>0:
        motor.run_for_degrees(port.C, zn, -feed)
        motor.run_for_degrees(port.D, znn, feed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.C, zn, feed)
        motor.run_for_degrees(port.D, znn, -feed)
        G07(length, efeed)
      zposC+=zn
      zposD+=znn
    print("G01 Z",z,"F",feed,"EF" ,efeed,"E",length)
    print("New Position: X",xpos,"Y",ypos,"ZC",zposC,"ZD",zposD)
    light_matrix.write("G01")
  else:
    print("Motors disabled")

def G02(z, feed, motorn):
  global xpos, ypos, zposC, zposD, motoron, absolute
  if motoron==1:
    if motorn=="C":
      if absolute==0:
        if z>0:
          motor.run_for_degrees(port.C, z, -feed)
        else:
          motor.run_for_degrees(port.C, z, feed)
        zposC+=z
      else:
        zn=z-zposC
        if z>0:
          motor.run_for_degrees(port.C, zn, -feed)
        else:
          motor.run_for_degrees(port.C, zn, feed)
        zposC+=zn
      print("G02 Z",z,"F",feed,"M",motor)
      print("New Position: X",xpos,"Y",ypos,"ZC",zposC,"ZD",zposD)
      light_matrix.write("G02")
    elif motorn=="D":
      if absolute==0:
        if z>0:
          motor.run_for_degrees(port.D, z, -feed)
        else:
          motor.run_for_degrees(port.D, z, feed)
        zposD+=z
      else:
        zn=z-zposD
        if z>0:
          motor.run_for_degrees(port.D, zn, -feed)
        else:
          motor.run_for_degrees(port.D, zn, feed)
        zposD+=zn
      print("G02 Z",z,"F",feed,"M",motor)
      print("New Position: X",xpos,"Y",ypos,"ZC",zposC,"ZD",zposD)
      light_matrix.write("G02")
    else:
      print("Invalid Z motor")
  else:
    print("Motors disabled")

def G07(length, feed):
  global motoron, ftype, flist, tlist, etemp, btemp
  if ftype in flist:
    findex=flist.index(ftype)
    if etemp>=tlist[findex]-10:
      if etemp<=tlist[findex]+10:
        if btemp>=tlist2[findex]-10:
          if btemp<=tlist2[findex]+10:
            if motoron==1:
              nfeed=feed*9.79416
              nlength=length*9.79416
              if length>0:
                motor.run_for_degrees(port.E, nlength, nfeed)
              else:
                motor.run_for_degrees(port.E, nlength, -nfeed)
              print("G07 E",length,"F",feed)
              light_matrix.write("G07")
            else:
              print("Motors disabled")
          else:
            print("Bed temperature too high")
        else:
          print("Bed temperature too low")
      else:
        print("Extruder temperature too high")
    else:
      print("Extruder temperature too low")
  else:
    print("Unknown filament type")

def G15(tests, speed):
  i=0
  while i<tests:
    G00(xlength, 0, speed*8.1, 0, 0)
    G00(0, ylength, speed*8.1, 0, 0)
    G00(-xlength, 0, speed*8.1, 0, 0)
    G00(0, -ylength, speed*8.1, 0, 0)
    i+=1
    print(tests-i, "tests remaining")
  print("G15 T", tests, "S", speed*8.1)
  light_matrix.write("G15")

def G27(axis):
  global xpos, ypos, zposC, zposD
  if axis=="X":
    G00(-xlength, 0, 60, 0, 0)
    xpos=0
  elif axis=="Y":
    G00(0, -ylength, 60, 0, 0)
    ypos=0
  elif axis=="Z":
    probe()
    zposC=0
    zposD=0
    G01(90,60, 0, 0)
  else:
    print("Invalid axis to home")
  print("G27 A",axis)
  light_matrix.write("G27")

def G28():
  global xpos, ypos, zposC, zposD
  print("Homing all axes")
  G00(-xlength, -ylength, 180, 0, 0)
  time.sleep(6.2)
  print("Finding Z zero")
  probe()
  zposC=0
  zposD=0
  G01(90, 60, 0, 0)
  print("Homing Complete!")
  light_matrix.write("Homing Complete!")
  light_matrix.clear()
  xpos=0
  ypos=0
  print("G28")
  light_matrix.write("G28")

def G29(tests):
  G28()
  i=0
  rows=[]
  while i<tests*tests:
    rows.append(0)
    i+=1
  i=0
  i2=0
  while i2<tests:
    while i<tests:
      measure()
      rows[i]=iniz2
      G00(xlength/(tests-1), 0, 50, 0, 0)
      i+=1
    G00(-xlength, ylength/(tests-1), 80, 0, 0)
    i2+=1
  G00(-xlength, -ylength, 100, 0, 0)
  print("G29 R1:",rows)
  light_matrix.write("G29")

def G34(tests):
  iniz2=0
  G28()
  i=0
  if tests>=1:
    while i<tests:
      time.sleep(2)
      iniz=0
      iniz2=0
      motor.reset_relative_position(port.C,0)
      motor.reset_relative_position(port.D,0)
      print("Calculating Motor C Z zero")
      probe()
      iniz=motor.relative_position(port.C)
      G01(100, 90, 0, 0)
      time.sleep(1.3)
      G00(xlength, 0, 360, 0, 0)
      time.sleep(3.35)
      print("Calculating Motor D Z zero")
      probe1()
      if iniz2 != 100:
        if iniz-iniz2>0:
          G02(iniz-iniz2, 20, "D")
        elif iniz-iniz2<0:
          G02(iniz-iniz2, -20, "D")
      print("G34 CZA",zposC,"CZB",zposD)
      print("Motor D offset by",iniz-iniz)
      print("(positive value means lower than expected)")
      i+=1
      G00(-xlength, 0, 360, 0, 0)
      time.sleep(3.35)
      print("Completed Z aligning.",(tests-i),"tests remaining")
    print("G34 T",tests)
    light_matrix.write("G34")
  else:
    print("Invalid number of tests")

def M02(timet):
  time.sleep(timet)
  print("M02 T",timet)
  light_matrix.write("M02")

def M17():
  global motoron
  motoron=1
  print("M17")
  light_matrix.write("M17")

def M18():
  global motoron
  motoron=0
  print("M18")
  light_matrix.write("M18")

def M30(seq):
  start=time.time()
  if seq==1:
    G28()
    G34(3)
    G29(4)
  #elif...
  end=time.time()
  print("M30",seq)
  print("Sequence",seq,"completed in",convert(end-start),"seconds")
  light_matrix.write("M30")
  light_matrix.write("Done")

def M103(temp):
  global ettemp, etemp
  ettemp=temp
  print("M103 T",temp)
  light_matrix.write("M103")
  if ettemp<etemp:
    while etemp>ettemp:
      etemp-=1
      time.sleep(1)
      print("Current Extruder Temp:",etemp,"/",ettemp,"degrees")
  elif ettemp>etemp:
    while ettemp>etemp:
      etemp+=1
      time.sleep(0.4)
      print("Current Extruder Temp:",etemp,"/",ettemp,"degrees")

def M105(temp):
  global bttemp, btemp
  bttemp=temp
  print("M105 T",temp)
  light_matrix.write("M105")
  if bttemp<btemp:
    while btemp>bttemp:
      btemp-=1
      time.sleep(1)
      print("Current Extruder Temp:",btemp,"/",bttemp,"degrees")
  elif bttemp>btemp:
    while bttemp>btemp:
      btemp+=1
      time.sleep(0.4)
      print("Current Extruder Temp:",btemp,"/",bttemp,"degrees")

def M271(type):
  global ftype
  ftype=type
  print("M271 T",type)
  light_matrix.write("M271")

def M278(diam):
  global fdim
  fdim=diam
  print("M278 D",diam)
  light_matrix("M278")

def M502():
  global xpos, ypos, zposC, zposD, xlength, ylength, iniz, iniz2, motoron
  global etemp, btemp, ettemp, bttemp, ftype, fdim, absolute
  xpos=0
  ypos=0
  zposC=0
  zposD=0
  xlength=1080
  ylength=1080
  iniz=0
  iniz2=0
  motoron=0
  etemp=20
  ettemp=20
  btemp=20
  bttemp=20
  ftype="PLA"
  fdim=1.75
  absolute=0

# == commands below ==
