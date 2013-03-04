#!/usr/bin/env python

import subprocess

class Device:
  def __init__(self, id):
    self.id = id
    self.name = subprocess.check_output(('xinput','--list','--name-only',id)).strip()
    
  def __str__(self):
    return self.id+':\t'+self.name
    
  def getProps(self):
    props = subprocess.check_output(('xinput','--list-props',self.id))
    ret = {}
    for p in props.splitlines():
      if ':' in p:
        key,val = p.split(':',1)
        if '(' in key:
          name,pid = key.rsplit('(',1)
          if ')' in pid:
            pid = pid.split(')')[0]
            prop = {'id':pid, 'name':name.strip()}
            if ',' in val:
              vals = []
              for v in val.split(','):
                vals.append(v.strip())
              prop['value'] = vals
            else:
              prop['value'] = val.strip()
            ret[int(pid)]=prop
    return ret          

  def findProp(self, prop_name):
    props = self.getProps()
    for p in props.itervalues():
      if p['name'] == prop_name:
        return p      

  def setProp(self, prop_name, *vals):
    subprocess.check_call(('xinput','set-prop',self.id,prop_name)+vals)
      

  def isEnabled(self):
    e = self.findProp('Device Enabled')
    if e['value'] == '1':
      return True
    return False
    
  def enable(self, enable_flag=True):
    if enable_flag:
      subprocess.check_call(('xinput','--enable',self.id))
    else:
      subprocess.check_call(('xinput','--disable',self.id))

        
class XInput:
  def __init__(self):
    self.devices = {}
    ids = subprocess.check_output(('xinput','--list','--id-only'))
    for id in ids.split():
      self.devices[int(id)] = Device(id)
      
  def __str__(self):
    ret = []
    for k in sorted(self.devices.iterkeys()):
      ret.append(str(self.devices[k]))
    return '\n'.join(ret)
    
  def find(self, name_part):
    ret = []
    for d in self.devices.itervalues():
      if name_part in d.name:
        ret.append(d)
    return ret
    
if __name__ == '__main__':
  x = XInput()
  print x
  atmel = x.find('Atmel')[0]
  print str(atmel)
  print atmel.findProp('Device Enabled')
  if atmel.isEnabled():
    print 'disabling'
    atmel.enable(False)
  else:
    print 'enabling'
    atmel.enable()
    
