#!/usr/bin/env python

import subprocess

class Output:
  def __init__(self, screen_num,line):
    self.screen_number = screen_num
    self.name, self.status = line.split(None,2)[0:2]
    
  def addMode(self, line):
    pass
    
  def __str__(self):
    return self.name+': '+self.status

  def rotate(self,direction):
    subprocess.check_call(('xrandr','--screen',self.screen_number,'--output',self.name,'--rotate', direction))

class Screen:
  def __init__(self, number):
    self.number = number
    self.outputs = {}
    out = subprocess.check_output(('xrandr',))
    current_output = None
    for line in out.splitlines():
      if not line.startswith('Screen '):
        if not line.startswith(' '):
          current_output = Output(self.number,line)
          self.outputs[current_output.name] = current_output
        else:
          current_output.addMode(line)

  def __str__(self):
    ret = ['Screen '+self.number]
    for o in self.outputs:
      ret.append(str(self.outputs[o]))
    return '\n'.join(ret)
    
  def find(self,out_name):
    if out_name in self.outputs:
      return self.outputs[out_name]

class RandR:
  def __init__(self):
    self.screens = []
    out = subprocess.check_output(('xrandr',))
    for line in out.splitlines():
      if line.startswith('Screen '):
        if ':' in line:
          num = line.split(':',1)[0].rsplit(' ',1)[1]
          self.screens.append(Screen(num))
          
  def __str__(self):
    ret = []
    for s in self.screens:
      ret.append(str(s))
    return '\n'.join(ret)

  def find(self, out_name, screen=None):
    if screen is not None:
      return self.screens[screen].find(out_name)
    for s in self.screens:
      ret = s.find(out_name)
      if ret is not None:
        return ret

          
if __name__ == '__main__':
  r = RandR()
  print r
  import sys
  if len(sys.argv) > 1:
    edp1 = r.find('eDP1')
    edp1.rotate(sys.argv[1])

