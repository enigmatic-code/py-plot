#!/usr/bin/env python -t
###############################################################################
#
# File:         plot.py
# RCS:          $Header: $
# Description:  A Simple Plotting Library Using Tk
# Author:       Jim Randell
# Created:      Sat Oct  6 10:33:02 2012
# Modified:     Wed Jan 20 11:56:36 2016 (Jim Randell) jim.randell@gmail.com
# Language:     Python
# Package:      N/A
# Status:       Experimental (Do Not Distribute)
#
# (C) Copyright 2012, Jim Randell, all rights reserved.
#
###############################################################################
# -*- mode: Python; py-indent-offset: 2; -*-

"""
[[documentation to go here]]
"""

from __future__ import print_function

__author__ = "Jim Randell <jim.randell@gmail.com>"
__version__ = "2014-04-14"

import sys

try:
  if sys.version_info[0] < 3:
    # Python 2
    import Tkinter as Tk
  else:
    # Python 3
    import tkinter as Tk
except ImportError:
  print('WARNING: Tk (tkinter) not found')

class Plot(object):
  """
  Plot(xscale=1, yscale=1, xoffset=0, yoffset=0)

  A plot object.

  You can interact with the plot window in the following ways:

  * click and drag to reposition the plot.
  * plus key (or equals key) to zoom in.
  * minus key to zoom out.
  * escape key (or Q) to quit.
  """

  # initialise the plot
  def __init__(self, xscale=1, yscale=1, xoffset=0, yoffset=0):
    self.objects = list()
    self.border = 20
    self.xscale = float(xscale)
    self.yscale = float(yscale)
    self.xoffset = xoffset
    self.yoffset = yoffset

  # add an object to plot
  def add(self, x):
    self.objects.append(x)

  # remove all objects to plot
  def clear(self):
    del self.objects[:]

  # display the objects
  def display(self):

    # create a window with a canvas in it
    master = Tk.Tk()

    self.canvas = canvas = Tk.Canvas(master, width=600, height=600, highlightthickness=0)
    canvas.pack(fill=Tk.BOTH, expand=1)

    # interaction
    canvas.bind('<Configure>', self.draw_handler)
    canvas.bind('<Button-1>', self.click_handler)
    canvas.bind('<B1-Motion>', self.drag_handler)
    canvas.bind('<ButtonRelease-1>', self.release_handler)
    canvas.bind('<KeyPress-minus>', self.zoom_minus)
    canvas.bind('<KeyPress-plus>', self.zoom_plus)
    canvas.bind('<KeyPress-equal>', self.zoom_plus)
    canvas.bind('<Double-Button-1>', self.double_click_handler)
    canvas.bind('<Double-Button-2>', self.double_click2_handler)

    # keyboard actions
    # Q, Esc = quit
    quit = lambda e: master.quit()
    canvas.bind('<KeyPress-Escape>', quit)
    canvas.bind('<KeyPress-q>', quit)
    # S = capture image to file (plot.png)
    canvas.bind('<KeyPress-s>', self.screencapture)

    canvas.focus_set()
    Tk.mainloop()

  # draw the objects
  def draw(self):
    self.canvas.delete(Tk.ALL)
    for i in self.objects:
      i.draw(self.canvas, self.border, self.canvas.winfo_height() - self.border,
             xscale=self.xscale, yscale=self.yscale,
             xoffset=self.xoffset, yoffset=self.yoffset)

  # handlers

  def draw_handler(self, event=None):
    self.draw()

  def click_handler(self, event=None):
    (self.move_x, self.move_y) = (event.x, event.y)
    (self.delta_x, self.delta_y) = (0, 0)

  def drag_handler(self, event=None):
    (x, y) = (event.x, event.y)
    (dx, dy) = (x - self.move_x, y - self.move_y)
    self.delta_x += dx
    self.delta_y += dy
    # move everything by (dx, dy)
    self.canvas.move('move', dx, dy)
    (self.move_x, self.move_y) = (x, y)

  def release_handler(self, event=None):
    self.xoffset += self.delta_x / self.xscale
    self.yoffset -= self.delta_y / self.yscale
    self.draw()

  def zoom_minus(self, event=None):
    self.xoffset += (self.canvas.winfo_width() - 2 * self.border) / (2 * self.xscale)
    self.yoffset += (self.canvas.winfo_height() - 2 * self.border) / (2 * self.yscale)
    self.xscale /= 2.0
    self.yscale /= 2.0
    self.draw()

  def zoom_plus(self, event=None):
    self.xscale *= 2.0
    self.yscale *= 2.0
    self.xoffset -= (self.canvas.winfo_width() - 2 * self.border) / (2 * self.xscale)
    self.yoffset -= (self.canvas.winfo_height() - 2 * self.border) / (2 * self.yscale)
    self.draw()

  def double_click_handler(self, event=None, button=1):
    (x, y) = (event.x, event.y)
    # centre at <x>,<y>
    (dx, dy) = (self.canvas.winfo_width() / 2 - x, y - self.canvas.winfo_height() / 2)
    self.xoffset += dx / self.xscale
    self.yoffset += dy / self.yscale
    if button == 1:
      self.zoom_plus()
    elif button == 2:
      self.zoom_minus()
    else:
      self.draw()

  def double_click2_handler(self, event):
    self.double_click_handler(event, 2)

  def screencapture(self, event=None):
    if sys.platform == 'darwin':
      # OS X
      import subprocess
      # -iw = interactive window mode (Esc to cancel)
      # -P = open in "Preview"
      subprocess.call(['screencapture', '-iw', '-P', 'plot.png'])

# translate args to tk equivalents
T = {
  'fill': 'fill',
  'color': 'fill',
  'colour': 'fill',
  'width': 'width',
  'outline': 'outline',
  'cap': 'capstyle',
  'join': 'joinstyle',
  'arrow': 'arrow',
  'dash': 'dash',
  'anchor': 'anchor',
}

# common defaults
D = {
  'fill': 'black',
  'width': 2,
  # and make shapes movable
  'tag': 'move',
}

class Shape(object):

  def __init__(self, **args):
    pass

  def set_args(self, args, **kw):
    tkargs = D.copy()
    for (k, v) in kw.items():
      tkargs[k] = v
    for (k, v) in args.items():
      if k in T:
        tkargs[T[k]] = v
    self.tkargs = tkargs
    

# draw a line
class Line(Shape):
  """
  Line((x0, y0, x1, y1, ...), arg=value, ...)

  Draw a poly-line.

  Useful args:
  width=<width> - pixel width of the line
  colour=<colour> - colour of line ('black', 'red', '#rrggbb', ...)
  cap=<cap> - cap style ('round', 'projecting', 'butt')
  join=<join> - join style ('round', 'bevel', 'miter')
  arrow=<arrow> - arrow style ('none', 'first', 'last', 'both')
  """

  def __init__(self, points, **args):
    self.pts = points
    self.set_args(args, arrow='none', joinstyle='round', capstyle='round')

  def draw(self, canvas, x0=0, y0=0, xscale=1, yscale=1, xoffset=0, yoffset=0):
    pts = []
    for i in range(0, len(self.pts), 2):
      (x, y) = self.pts[i:i+2]
      pts.extend((x0 + (x + xoffset) * xscale, y0 - (y + yoffset) * yscale))
    canvas.create_line(*pts, **self.tkargs)


# draw a polygon
class Polygon(Shape):
  """
  Polygon((x0, y0, x1, y1, ...), arg=value, ...)

  Draw a closed polygon.

  Useful args:
  squish=
  width=<wdith> - pixel width of outline
  outline=<colour> - outline colour ('black', 'red', '#rrggbb', ...)
  fill=<colour> - fill colour (None, 'black', 'red', '#rrggbb', ...)
  """

  def __init__(self, points, **args):
    self.pts = points
    self.set_args(args, fill=None)

  def draw(self, canvas, x0=0, y0=0, xscale=1.0, yscale=1.0, xoffset=0, yoffset=0):
    pts = []
    for i in range(0, len(self.pts), 2):
      (x, y) = self.pts[i:i+2]
      pts.extend((x0 + (x + xoffset) * xscale, y0 - (y + yoffset) * yscale))
    canvas.create_polygon(*pts, **self.tkargs)


# draw a circle
# NOTE: it appears very large circles may not be drawn accurately
class Circle(Shape):
  """
  Circle((x, y), r, squish=1, arg=value, ...)

  Draw a circle, centred at (x, y) of radius r.

  Using a squish value that isn't 1 will draw an ellipse.

  Useful args:
  width=<width> - pixel width of outline
  outline=<colour> - outline colour ('black', 'red', '#rrggbb', ...)
  fill=<color> - fill colour (None, 'black', 'red', '#rrggbb', ...)
  """

  def __init__(self, centre, radius, squish=1.0, **args):
    self.centre = centre
    self.radius = radius
    self.squish = squish # squish in the y direction
    self.set_args(args)

  def draw(self, canvas, x0=0, y0=0, xscale=1, yscale=1, xoffset=0, yoffset=0):
    (x1, y1, x2, y2) = (self.centre[0] - self.radius, self.centre[1] - self.radius * self.squish,
                        self.centre[0] + self.radius, self.centre[1] + self.radius * self.squish)
    pts = (x0 + (x1 + xoffset) * xscale, y0 - (y1 + yoffset) * yscale,
           x0 + (x2 + xoffset) * xscale, y0 - (y2 + yoffset) * yscale)
    canvas.create_oval(*pts, **self.tkargs)


# draw a text label
class Label(Shape):
  """
  Label((x, y), text, arg=value, ...)

  Draw a text label at (x, y).

  Useful args:
  anchor=<anchor> - text anchor position ('center', 'n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se')
  """

  def __init__(self, point, text, **args):
    self.point = point
    self.text = text
    self.set_args(args, width=None)

  def draw(self, canvas, x0=0, y0=0, xscale=1, yscale=1, xoffset=0, yoffset=0):
    (x, y) = self.point
    canvas.create_text(x0 + (x + xoffset) * xscale, y0 - (y + yoffset) * yscale, text=self.text, **self.tkargs)
