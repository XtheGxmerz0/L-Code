#L-Code: The first firmware for Lego 3D printer architectures
#The latest version is version 2.0.7

#package imports
import time, random, force_sensor, motor
from colorama import Fore as color
from hub import light_matrix, port

#Port A: X
#Port B: Y
#Port C and D: Z
#Port E: E
#Port F: BLS
#motor max speed: 135rpm (810deg/sec)
#each rotation of E: 36.7566mm (circumference of wheel)
#e constant is 9.79416 (degrees per millimeter using a 12t lego double bevel wheel)
#all measurements will be taken in mm and mm/s

#G00: move in XY
#G01: move in Z
#G02: move independent Z motor
#G07: extruder movement
#G15: motor calibration
#G27: independent axis \homing
#G28: home all axes using force sensor
#G29: 3x3 auto leveling
#G34: Z axis alignment
#M02: wait
#M17: activate motors
#M18: deactivate motors
#M30: run custom sequence
#M84: color change
#M103: set extruder temp
#M105: set bed temp
#M271: set filament type
#M278: set filamnt diameter
#M355: deactivate coreXY mode
#M356: activate coreXY mode
#M502: reset parameters

#variable globalization

global xpos
global ypos
global zposC
global zposD
global iniz
global iniz2

#variable definitions

xpos = 0
ypos = 0
zposC = 0
zposD = 0
xlength = 2100
ylength = 2100
iniz = 0
iniz2 = 0
motoron = 0
etemp = 20
ettemp = 20
btemp = 20
bttemp = 20
flist = ["PLA", "PETG", "ABS", "ASA", "PC", "PA", "TPU"]
tlist = [205, 250, 235, 245, 270, 285, 225]
tlist2 = [60, 75, 105, 105, 110, 75, 45]
absolute = 0
corexy = 0
key = "INIT"
us = []
ps = []
signedin = 0


#function definitions
def signin():
  global signedin
  print(color.BLUE)
  u = input("Username: ")
  p = input("Password: ")
  if u in us:
    if ps[us.index(u)] == p:
      signedin = 1
      print(color.GREEN, "Access granted")
    else:
      print(color.RED, "Invalid Credentials")
  else:
    print(color.RED, "Invalid Credentials")


def signout():
  global signedin
  signedin = 0
  print(color.YELLOW, "Signing out...")
  time.sleep(2)


def genkey():
  global key
  key = random.randint(0, 1000000000)


def convert(ttc):
  m = 0
  h = 0
  while ttc >= 60:
    if ttc >= 60:
      m += 1
      ttc -= 60
      continue
    if m >= 60:
      h += 1
      m -= 60
      continue
  s = ttc
  s = round(s, 2)
  if s < 10:
    s = "0" + str(s)
  if m < 10:
    m = "0" + str(m)
  if h < 10:
    h = "0" + str(h)
  ct = str(h) + ":" + str(m) + ":" + str(s)
  return (ct)


def probe():
  global motoron
  if motoron == 1:
    while force_sensor.force(port.F) <= 80:
      G01(-2, 20, 0, 0)
      time.sleep(0.2)
  else:
    print(color.RED, "Motors disabled")


def probe1():
  global iniz2, motoron
  if motoron == 1:
    iniz2 = 0
    while force_sensor.force(port.F) <= 80:
      G01(-2, 20, 0, 0)
      iniz2 += 2
      time.sleep(0.2)
  else:
    print(color.RED, "Motors disabled")


def measure():
  probe1()
  G01(iniz2, 20, 0, 0)


def G00(x, y, feed, length, efeed):
  global xpos, ypos, zposC, zposD, motoron, absolute, corexy
  xs=9.79416*x
  ys=9.79416*y
  sfeed=9.79416*feed
  if motoron == 1:
    if absolute == 0:
      if corexy == 0:
        if xs > 0:
          motor.run_for_degrees(port.A, xs, sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.A, xs, -sfeed)
          G07(length, efeed)
        if ys > 0:
          motor.run_for_degrees(port.B, ys, sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.B, ys, -sfeed)
          G07(length, efeed)
      else:
        if xs > 0:
          motor.run_for_degrees(port.A, xs, -sfeed)
          motor.run_for_degrees(port.B, xs, -sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.A, xs, sfeed)
          motor.run_for_degrees(port.B, xs, sfeed)
          G07(length, efeed)
        if ys > 0:
          motor.run_for_degrees(port.A, ys, sfeed)
          motor.run_for_degrees(port.B, ys, -sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.A, ys, -sfeed)
          motor.run_for_degrees(port.B, ys, sfeed)
          G07(length, efeed)
      xpos += xs
      ypos += ys
    else:
      xn = xs - xpos
      yn = ys - ypos
      if corexy == 0:
        if xn > 0:
          motor.run_for_degrees(port.A, xn, sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.A, xn, -sfeed)
          G07(length, efeed)
        if yn > 0:
          motor.run_for_degrees(port.B, yn, sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.B, yn, -sfeed)
          G07(length, efeed)
      else:
        if xn > 0:
          motor.run_for_degrees(port.A, xn, -sfeed)
          motor.run_for_degrees(port.B, xn, -sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.A, xn, sfeed)
          motor.run_for_degrees(port.B, xn, sfeed)
          G07(length, efeed)
        if yn > 0:
          motor.run_for_degrees(port.A, yn, sfeed)
          motor.run_for_degrees(port.B, yn, -sfeed)
          G07(length, efeed)
        else:
          motor.run_for_degrees(port.A, yn, -sfeed)
          motor.run_for_degrees(port.B, yn, sfeed)
          G07(length, efeed)
      xpos += xn
      ypos += yn
    print(color.GREEN, "G00 X", x, "Y", y, "F", feed, "EF", efeed, "E", length)
    print(color.GREEN, "New Position: X", xpos, "Y", ypos, "ZC", zposC, "ZD", zposD)
    light_matrix.write("G00")
  else:
    print(color.RED, "Motors disabled")


def G01(z, feed, length, efeed):
  global xpos, ypos, zposC, zposD, motoron, absolute
  zs=9.79416*z
  sfeed=9.79416*feed
  if motoron == 1:
    if absolute == 0:
      if zs > 0:
        motor.run_for_degrees(port.C, zs, -sfeed)
        motor.run_for_degrees(port.D, zs, sfeed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.C, zs, sfeed)
        motor.run_for_degrees(port.D, zs, -sfeed)
        G07(length, efeed)
      zposC += zs
      zposD += zs
    else:
      zn = zs - zposC
      znn = zs - zposD
      if zs > 0:
        motor.run_for_degrees(port.C, zn, -sfeed)
        motor.run_for_degrees(port.D, znn, sfeed)
        G07(length, efeed)
      else:
        motor.run_for_degrees(port.C, zn, sfeed)
        motor.run_for_degrees(port.D, znn, -sfeed)
        G07(length, efeed)
      zposC += zn
      zposD += znn
    print(color.GREEN, "G01 Z", z, "F", feed, "EF", efeed, "E", length)
    print(color.GREEN, "New Position: X", xpos, "Y", ypos, "ZC", zposC, "ZD", zposD)
    light_matrix.write("G01")
  else:
    print(color.RED, "Motors disabled")


def G02(z, feed, motorn):
  global xpos, ypos, zposC, zposD, motoron, absolute
  zs=9.79416*z
  sfeed=9.79416*feed
  if motoron == 1:
    if motorn == "C":
      if absolute == 0:
        if zs > 0:
          motor.run_for_degrees(port.C, zs, -sfeed)
        else:
          motor.run_for_degrees(port.C, zs, sfeed)
        zposC += zs
      else:
        zn = zs - zposC
        if zs > 0:
          motor.run_for_degrees(port.C, zn, -sfeed)
        else:
          motor.run_for_degrees(port.C, zn, sfeed)
        zposC += zn
      print(color.GREEN, "G02 Z", z, "F", feed, "M", motor)
      print(color.GREEN, "New Position: X", xpos, "Y", ypos, "ZC", zposC, "ZD", zposD)
      light_matrix.write("G02")
    elif motorn == "D":
      if absolute == 0:
        if zs > 0:
          motor.run_for_degrees(port.D, zs, -sfeed)
        else:
          motor.run_for_degrees(port.D, zs, sfeed)
        zposD += zs
      else:
        zn = zs - zposD
        if zs > 0:
          motor.run_for_degrees(port.D, zn, -sfeed)
        else:
          motor.run_for_degrees(port.D, zn, sfeed)
        zposD += zn
      print(color.GREEN, "G02 Z", z, "F", feed, "M", motor)
      print(color.GREEN, "New Position: X", xpos, "Y", ypos, "ZC", zposC, "ZD", zposD)
      light_matrix.write("G02")
    else:
      print(color.RED, "Invalid Z motor")
  else:
    print(color.RED, "Motors disabled")


def G07(length, feed):
  global motoron, ftype, flist, tlist, etemp, btemp
  if ftype in flist:
    findex = flist.index(ftype)
    if etemp >= tlist[findex] - 10:
      if etemp <= tlist[findex] + 10:
        if btemp >= tlist2[findex] - 10:
          if btemp <= tlist2[findex] + 10:
            if motoron == 1:
              nfeed = feed * 9.79416
              nlength = length * 9.79416
              if length > 0:
                motor.run_for_degrees(port.E, nlength, nfeed)
              else:
                motor.run_for_degrees(port.E, nlength, -nfeed)
              print(color.GREEN, "G07 E", length, "F", feed)
              light_matrix.write("G07")
            else:
              print(color.RED, "Motors disabled")
          else:
            print(color.RED, "Bed temperature too high")
        else:
          print(color.RED, "Bed temperature too low")
      else:
        print(color.RED, "Extruder temperature too high")
    else:
      print(color.RED, "Extruder temperature too low")
  else:
    print(color.RED, "Unknown filament type")


def G15(tests, speed):
  i = 0
  while i < tests:
    G00(xlength, 0, speed * 8.1, 0, 0)
    G00(0, ylength, speed * 8.1, 0, 0)
    G00(-xlength, 0, speed * 8.1, 0, 0)
    G00(0, -ylength, speed * 8.1, 0, 0)
    i += 1
    print(color.YELLOW, tests - i, "tests remaining")
  print(color.GREEN, "G15 T", tests, "S", speed * 8.1)
  light_matrix.write("G15")


def G27(axis):
  global xpos, ypos, zposC, zposD
  if axis == "X":
    G00(-xlength, 0, 60, 0, 0)
    xpos = 0
  elif axis == "Y":
    G00(0, -ylength, 60, 0, 0)
    ypos = 0
  elif axis == "Z":
    probe()
    zposC = 0
    zposD = 0
    G01(90, 60, 0, 0)
  else:
    print(color.RED, "Invalid axis to home")
  print(color.GREEN, "G27 A", axis)
  light_matrix.write("G27")


def G28():
  global xpos, ypos, zposC, zposD
  print(color.YELLOW, "Homing all axes")
  G00(-xlength, -ylength, 180, 0, 0)
  time.sleep(6.2)
  print(color.YELLOW, "Finding Z zero")
  probe()
  zposC = 0
  zposD = 0
  G01(90, 60, 0, 0)
  print(color.GREEN, "Homing Complete!")
  light_matrix.write("Homing Complete!")
  xpos = 0
  ypos = 0
  print(color.GREEN, "G28")
  light_matrix.write("G28")


def G29(tests):
  G28()
  i = 0
  rows = []
  while i < tests * tests:
    rows.append(0)
    i += 1
  i = 0
  i2 = 0
  while i2 < tests:
    while i < tests:
      measure()
      rows[i] = iniz2
      G00(xlength / (tests - 1), 0, 50, 0, 0)
      i += 1
    G00(-xlength, ylength / (tests - 1), 80, 0, 0)
    i2 += 1
  G00(-xlength, -ylength, 100, 0, 0)
  print(color.GREEN, "G29 R1:", rows)
  light_matrix.write("G29")


def G34(tests):
  iniz2 = 0
  G28()
  i = 0
  if tests >= 1:
    while i < tests:
      time.sleep(2)
      iniz = 0
      iniz2 = 0
      motor.reset_relative_position(port.C, 0)
      motor.reset_relative_position(port.D, 0)
      print(color.YELLOW, "Calculating Motor C Z zero")
      probe()
      iniz = motor.relative_position(port.C)
      G01(100, 90, 0, 0)
      time.sleep(1.3)
      G00(xlength, 0, 360, 0, 0)
      time.sleep(3.35)
      print(color.YELLOW, "Calculating Motor D Z zero")
      probe1()
      if iniz2 != 100:
        if iniz - iniz2 > 0:
          G02(iniz - iniz2, 20, "D")
        elif iniz - iniz2 < 0:
          G02(iniz - iniz2, -20, "D")
      print(color.GREEN, "G34 CZA", zposC, "CZB", zposD)
      print(color.CYAN, "Motor D offset by", iniz - iniz)
      print(color.CYAN, "(positive value means lower than expected)")
      i += 1
      G00(-xlength, 0, 360, 0, 0)
      time.sleep(3.35)
      print(color.YELLOW, "Completed Z aligning.", (tests - i), "tests remaining")
    print(color.GREEN, "G34 T", tests)
    light_matrix.write("G34")
  else:
    print(color.RED, "Invalid number of tests")


def M02(timet):
  time.sleep(timet)
  print(color.GREEN, "M02 T", timet)
  light_matrix.write("M02")


def M17():
  global motoron
  motoron = 1
  print(color.GREEN, "M17")
  light_matrix.write("M17")


def M18():
  global motoron
  motoron = 0
  print(color.GREEN, "M18")
  light_matrix.write("M18")


def M30(seq):
  start = time.time()
  if seq == 1:
    G28()
    G34(3)
    G29(4)
  #elif...
  end = time.time()
  print(color.GREEN, "M30", seq)
  print(color.CYAN, "Sequence", seq, "completed in", convert(end - start), "seconds")
  light_matrix.write("M30")
  light_matrix.write("Done")


def M84():
  save = [xpos, ypos, (zposC + zposD) / 2]
  G28()
  G01(720, 0, 0, 0)
  print(color.YELLOW, "Initiating color change...")
  print(color.YELLOW, "Retracting filament")
  G07(-100, 10)
  print(color.BLUE)
  input("Press enter when new filament is inserted > ")
  print(color.YELLOW, "Purging filament...")
  G07(100, 10)
  purged = 100
  print(color.BLUE)
  more = input("Has previous filament been purged? (y/n) > ")
  while more.lower() != "y":
    G07(10, 10)
    purged += 10
    print(color.BLUE)
    more = input("Has previous filament been purged? (y/n) > ")
    continue
  print(color.BLUE)
  input("Press enter when filament blob has been removed > ")
  G28()
  G00(save[0], save[1], 100, 0, 0)
  G01(save[2], 100, 0, 0)
  print(color.GREEN, "M84, Purged" + str(purged) + "mm of filament")
  light_matrix.write("M84")


def M103(temp):
  global ettemp, etemp
  ettemp = temp
  print(color.GREEN"M103 T", temp)
  light_matrix.write("M103")
  if ettemp < etemp:
    while etemp > ettemp:
      etemp -= 1
      time.sleep(1)
      print(color.CYAN, "Current Extruder Temp:", etemp, "/", ettemp, "degrees")
  elif ettemp > etemp:
    while ettemp > etemp:
      etemp += 1
      time.sleep(0.4)
      print(color.CYAN, "Current Extruder Temp:", etemp, "/", ettemp, "degrees")


def M105(temp):
  global bttemp, btemp
  bttemp = temp
  print(color.GREEN, "M105 T", temp)
  light_matrix.write("M105")
  if bttemp < btemp:
    while btemp > bttemp:
      btemp -= 1
      time.sleep(1)
      print(color.CYAN, "Current Extruder Temp:", btemp, "/", bttemp, "degrees")
  elif bttemp > btemp:
    while bttemp > btemp:
      btemp += 1
      time.sleep(0.4)
      print(color.CYAN, "Current Extruder Temp:", btemp, "/", bttemp, "degrees")


def M271(type):
  global ftype
  ftype = type
  print(color.GREEN, "M271 T", type)
  light_matrix.write("M271")


def M278(diam):
  global fdim
  fdim = diam
  print(color.GREEN, "M278 D", diam)
  light_matrix.write("M278")


def M355():
  global corexy
  corexy = 0
  print(color.GREEN, "M355")
  light_matrix.write("M355")


def M356():
  global corexy
  corexy = 1
  print(color.GREEN, "M356")
  light_matrix.write("M356")


def M502():
  global xpos, ypos, zposC, zposD, xlength, ylength, iniz, iniz2, motoron
  global etemp, btemp, ettemp, bttemp, ftype, fdim, absolute, corexy
  xpos = 0
  ypos = 0
  zposC = 0
  zposD = 0
  xlength = 2100
  ylength = 2100
  iniz = 0
  iniz2 = 0
  motoron = 0
  etemp = 20
  ettemp = 20
  btemp = 20
  bttemp = 20
  ftype = "PLA"
  fdim = 1.75
  absolute = 0
  corexy = 0


#live interface code below
while True:
  print(color.BLUE)
  action = input("Next action: > ")
  if signedin == 1:
    if "RUN" in action:
      exec(action[action.rfind("RUN "):])
    elif action == "EXIT":
      print(color.RED)
      exit("Exiting program...")
    elif "SEQ" in action:
      exec("M30 (" + action[action.rfind("SEQ "):] + ")")
    elif action == "FRESET":
      print(color.YELLOW, "Resetting to factory default...")
      G28()
      M502()
    elif action == "SOUT":
      signout()
      signin()
    else:
      print(color.RED, "Invalid action to perform")
  else:
    print(color.MAGENTA, "Please sign in")
    signin()
