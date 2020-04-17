#!/usr/bin/env python

import Tkinter
import xinput
import randr

class App(Tkinter.Frame):
  def __init__(self, master=None):
    Tkinter.Frame.__init__(self, master)
    self.pack()
    
    master.title('ATIV Control')
    
    x = xinput.XInput()
    self.touch = x.find('Atmel')[0]
    for w in x.find('Wacom'):
      if 'stylus' in w.name:
        self.stylus = w
      elif 'eraser' in w.name:
        self.eraser = w
    
    self.TOUCH = Tkinter.Button(self)
    self.updateTouchLabel()
    self.TOUCH['command'] = self.toggleTouch
    self.TOUCH.pack({'side':'top'})
    
    r = randr.RandR()
    self.output = r.find('eDP-1')

    
    self.NORMAL = Tkinter.Button(self)
    self.NORMAL['text']='Normal'
    self.NORMAL['command'] = self.rotateNormal
    self.NORMAL.pack({'side':'top'})

    self.LEFT = Tkinter.Button(self)
    self.LEFT['text']='Left'
    self.LEFT['command'] = self.rotateLeft
    self.LEFT.pack({'side':'left'})

    self.RIGHT = Tkinter.Button(self)
    self.RIGHT['text']='Right'
    self.RIGHT['command'] = self.rotateRight
    self.RIGHT.pack({'side':'right'})

    self.INVERTED = Tkinter.Button(self)
    self.INVERTED['text']='Inverted'
    self.INVERTED['command'] = self.rotateInverted
    self.INVERTED.pack({'side':'bottom'})
    
  def updateTouchLabel(self):
    if self.touch.isEnabled():
      label = 'Touch (enabled)'
    else:
      label = 'Touch (disabled)'
    self.TOUCH['text']=label

  def toggleTouch(self):
    if self.touch.isEnabled():
      self.touch.enable(False)
    else:
      self.touch.enable(True)
    self.updateTouchLabel()

  def rotateNormal(self):
    self.output.rotate('normal')
    self.stylus.setProp('Wacom Rotation','0')
    self.eraser.setProp('Wacom Rotation','0')
    self.touch.setProp('Evdev Axis Inversion','0','0')
    self.touch.setProp('Evdev Axes Swap','0')

  def rotateInverted(self):
    self.output.rotate('inverted')
    self.stylus.setProp('Wacom Rotation','3')
    self.eraser.setProp('Wacom Rotation','3')
    self.touch.setProp('Evdev Axis Inversion','1','1')
    self.touch.setProp('Evdev Axes Swap','0')
    
  def rotateLeft(self):
    self.output.rotate('left')
    self.stylus.setProp('Wacom Rotation','2')
    self.eraser.setProp('Wacom Rotation','2')
    self.touch.setProp('Evdev Axis Inversion','1','0')
    self.touch.setProp('Evdev Axes Swap','1')

  def rotateRight(self):
    self.output.rotate('right')
    self.stylus.setProp('Wacom Rotation','1')
    self.eraser.setProp('Wacom Rotation','1')
    self.touch.setProp('Evdev Axis Inversion','0','1')
    self.touch.setProp('Evdev Axes Swap','1')
  
root = Tkinter.Tk()
app = App(master=root)
app.mainloop()
#root.destroy()

