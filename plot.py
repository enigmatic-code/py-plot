#! python3
###############################################################################
#
# File:         plot.py
# RCS:          $Header: $
# Description:  A Simple Plotting Library Using Tk
# Author:       Jim Randell
# Created:      Sat Oct  6 10:33:02 2012
# Modified:     Sun Oct  5 13:13:27 2025 (Jim Randell) jim.randell@gmail.com
# Language:     Python
# Package:      N/A
# Status:       Experimental (Do Not Distribute)
#
# (C) Copyright 2012-2020, Jim Randell, all rights reserved.
#
###############################################################################
# -*- mode: Python; py-indent-offset: 2; -*-

"""
[[documentation to go here]]
"""

from __future__ import print_function

__author__ = "Jim Randell <jim.randell@gmail.com>"
__version__ = "2025-10-05"

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

# translate args to tk equivalents
T = {
  'fill': 'fill',
  'color': 'fill',
  'colour': 'fill',
  'width': 'width',
  'outline': 'outline',
  'stipple': 'stipple', # but Tk on macOS doesn't seem to support 'stipple'
  'cap': 'capstyle',
  'join': 'joinstyle',
  'arrow': 'arrow',
  'arrowshape': 'arrowshape',
  'dash': 'dash',
  'anchor': 'anchor',
  'font': 'font',
  'start': 'start',
  'extent': 'extent',
  'style': 'style',
  'angle': 'angle',
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
  arrowshape=<tuple> - arrow shape
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
    self.set_args(args, fill=None, width=1)

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


# mark a point
class Mark(Shape):
  """
  pixel size
  """

  def __init__(self, point, size, **args):
    self.point = point
    self.size = size
    self.set_args(args)

  def draw(self, canvas, x0=0, y0=0, xscale=1, yscale=1, xoffset=0, yoffset=0):
    (x, y) = self.point
    size = self.size
    (x, y) = (x0 + (x + xoffset) * xscale, y0 - (y + yoffset) * yscale)
    pts = (x - size, y - size, x + size, y + size)
    canvas.create_oval(*pts, **self.tkargs)


# draw an arc [provisional support]
class Arc(Shape):
  """
  Arc((x, y), r, squish=1, arg=value, ...)

  Draw an arc, centred at (x, y) of radius r.

  Using a squish value that isn't 1 will draw an ellipse.

  Useful args:
  width=<width> - pixel width of outline
  outline=<colour> - outline colour ('black', 'red', '#rrggbb', ...)
  fill=<color> - fill colour (None, 'black', 'red', '#rrggbb', ...)
  style=<pieslice|chord|arc>
  start=<degrees>
  extent=<degrees>
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
    canvas.create_arc(*pts, **self.tkargs)


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
  def __init__(self, width=600, height=600, xscale=1, yscale=1, xoffset=0, yoffset=0, verbose=0):
    # instead of this use: [[ port install tk +quartz ]] when installing tk via macports
    #if sys.platform == "darwin":
    #  # prefixes of Pythons with native Tk
    #  prefix = ["/usr/bin/python", "/usr/local/bin/python", "/Library/Frameworks", "/System/Library/Frameworks/"]
    #  if not any(sys.executable.startswith(p) for p in prefix):
    #    print("WARNING! using {exe}".format(exe=sys.executable))
    if verbose:
      print("Tk.TkVersion = {v}".format(v=Tk.TkVersion))
    self.width = width
    self.height = height
    self.objects = list()
    self.border = 20
    self.xscale = float(xscale)
    self.yscale = float(yscale)
    self.xoffset = xoffset
    self.yoffset = yoffset
    self.pan = 4.0
    # for animations
    self.frame_iter = None
    self.frame_fn = None
    self.frame_delay = None
    self.playing = 0

  # add an object to plot
  def add(self, x):
    self.objects.append(x)

  # remove all objects to plot
  def clear(self):
    del self.objects[:]

  # for animation
  def animate(self, frames, fn, delay):
    self.frame_iter = iter(frames)
    self.frame_fn = fn
    self.frame_delay = delay

  # do the next frame in an animation
  def next_frame(self, play=0):
    i = self.frame_iter
    if i is None: return
    try:
      t = next(i)
    except StopIteration:
      return

    self.clear()
    if self.frame_fn(t) and play: self.play_pause_handler()
    self.draw()

    # if play is set automatically trigger the following frame
    if play and self.playing:
      self.canvas.after(self.frame_delay, self.next_frame, 1)

    return t

  # display the objects
  def display(self):

    # create a window with a canvas in it
    master = Tk.Tk()

    self.canvas = canvas = Tk.Canvas(master, width=self.width, height=self.height, highlightthickness=0, background="white")
    canvas.pack(fill=Tk.BOTH, expand=1)

    # if we are animating draw the first frame
    if self.frame_fn: self.next_frame()

    # interaction
    canvas.bind('<Configure>', self.configure_handler)
    canvas.bind('<Button-1>', self.click_handler)
    canvas.bind('<B1-Motion>', self.drag_handler)
    canvas.bind('<ButtonRelease-1>', self.release_handler)
    canvas.bind('<KeyPress-minus>', self.zoom_minus)
    canvas.bind('<KeyPress-comma>', self.zoom_minus)
    canvas.bind('<KeyPress-plus>', self.zoom_plus)
    canvas.bind('<KeyPress-equal>', self.zoom_plus)
    canvas.bind('<KeyPress-period>', self.zoom_plus)
    canvas.bind('<KeyPress-X>', self.zoom_x_plus)
    canvas.bind('<KeyPress-x>', self.zoom_x_minus)
    canvas.bind('<KeyPress-Y>', self.zoom_y_plus)
    canvas.bind('<KeyPress-y>', self.zoom_y_minus)
    canvas.bind('<Double-Button-1>', self.double_click_handler)
    canvas.bind('<Double-Button-2>', self.double_click2_handler)
    canvas.bind('<KeyPress-Up>', self.pan_up_handler)
    canvas.bind('<KeyPress-Down>', self.pan_down_handler)
    canvas.bind('<KeyPress-Right>', self.pan_right_handler)
    canvas.bind('<KeyPress-Left>', self.pan_left_handler)

    # keyboard actions
    # Q, Esc = quit
    quit = lambda e: master.quit()
    canvas.bind('<KeyPress-Escape>', quit)
    canvas.bind('<KeyPress-q>', quit)
    # S = capture image to file (plot.png)
    canvas.bind('<KeyPress-s>', self.screencapture)
    # I = info
    canvas.bind('<KeyPress-i>', self.info_handler)

    # F = step forward a frame
    canvas.bind('<KeyPress-f>', self.frame_handler)
    canvas.bind('<KeyPress-space>', self.play_pause_handler)

    # H = help
    canvas.bind('<KeyPress-h>', self.help_handler)

    canvas.focus_set()
    Tk.mainloop()

  # draw the objects
  def draw(self):
    self.width = self.canvas.winfo_width()
    self.height = self.canvas.winfo_height()
    self.canvas.delete(Tk.ALL)
    for i in self.objects:
      i.draw(
        self.canvas, self.border, self.height - self.border,
        xscale=self.xscale, yscale=self.yscale,
        xoffset=self.xoffset, yoffset=self.yoffset
      )

  # handlers
  def help_handler(self, event=None):
    print('=' * 40)
    print("  click + drag = move")
    print("  +/= = zoom in")
    print("  -/, = zoom out")
    print("  double click left = zoom in")
    print("  double click right = zoom out")
    print("  X = zoom in x-dimension")
    print("  Y = zoom in y-dimension")
    print("  x = zoom out x-dimension")
    print("  y = zoom out y-dimension")
    print("  left/right/up/down = pan")
    print("  q/esc = quit")
    print("  s = screenshot (macOS only)")
    print("  i = print info")
    print("  space = play/pause (animation)")
    print("  f = single frame advance (animation)")
    print("  h = help (this message)")
    print('=' * 40)

  def configure_handler(self, event=None):
    if self.playing: self.play_pause_handler(event)
    self.draw()

  def click_handler(self, event=None):
    (self.move_x, self.move_y) = (event.x, event.y)
    (self.delta_x, self.delta_y) = (0, 0)

  def drag_handler(self, event=None):
    if self.playing: self.play_pause_handler(event)
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
    self.xoffset += (self.width - 2 * self.border) / (2 * self.xscale)
    self.yoffset += (self.height - 2 * self.border) / (2 * self.yscale)
    self.xscale /= 2.0
    self.yscale /= 2.0
    self.draw()

  def zoom_plus(self, event=None):
    self.xscale *= 2.0
    self.yscale *= 2.0
    self.xoffset -= (self.width - 2 * self.border) / (2 * self.xscale)
    self.yoffset -= (self.height - 2 * self.border) / (2 * self.yscale)
    self.draw()

  def zoom_x_minus(self, event=None):
    self.xoffset += (self.width - 2 * self.border) / (2 * self.xscale)
    self.xscale /= 2.0
    self.draw()

  def zoom_x_plus(self, event=None):
    self.xscale *= 2.0
    self.xoffset -= (self.width - 2 * self.border) / (2 * self.xscale)
    self.draw()

  def zoom_y_minus(self, event=None):
    self.yoffset += (self.height - 2 * self.border) / (2 * self.yscale)
    self.yscale /= 2.0
    self.draw()

  def zoom_y_plus(self, event=None):
    self.yscale *= 2.0
    self.yoffset -= (self.height - 2 * self.border) / (2 * self.yscale)
    self.draw()

  def pan_up_handler(self, event=None):
    self.yoffset += self.pan
    self.draw()

  def pan_down_handler(self, event=None):
    self.yoffset -= self.pan
    self.draw()

  def pan_right_handler(self, event=None):
    self.xoffset += self.pan
    self.draw()

  def pan_left_handler(self, event=None):
    self.xoffset -= self.pan
    self.draw()

  def double_click_handler(self, event=None, button=1):
    (x, y) = (event.x, event.y)
    # centre at <x>,<y>
    (dx, dy) = (0.5 * self.width - x, y - 0.5 * self.height)
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

  def info_handler(self, event):
    print("width={width}, height={height}, xscale={xscale}, yscale={yscale}, xoffset={xoffset}, yoffset={yoffset}".format(**self.__dict__))

  def screencapture(self, event=None):
    if sys.platform == 'darwin':
      # OS X
      import subprocess
      # -iw = interactive window mode (Esc to cancel)
      # -P = open in "Preview"
      subprocess.call(['screencapture', '-iw', '-P', 'plot.png'])

  def frame_handler(self, event):
    self.next_frame()

  def play_pause_handler(self, event=None):
    if self.playing:
      print("[paused]")
      self.playing = 0
    else:
      print("[running ...]")
      self.playing = 1
      self.next_frame(play=1)


  # shapes
  def line(self, *args, **kw): self.add(Line(*args, **kw))
  def polygon(self, *args, **kw): self.add(Polygon(*args, **kw))
  def circle(self, *args, **kw): self.add(Circle(*args, **kw))
  def mark(self, *args, **kw): self.add(Mark(*args, **kw))
  def arc(self, *args, **kw): self.add(Arc(*args, **kw))
  def label(self, *args, **kw): self.add(Label(*args, **kw))

  # draw a bunch of line segments
  def lines(self, segs, *args, **kw):
    for seg in segs:
      self.line(seg, *args, **kw)

  # graph axes
  def graph_axes(self, xaxis, yaxis, xlabels=None, ylabels=None, xtext=None, ytext=None, tick=0.2, xtick=None, ytick=None):
    (xaxis, yaxis) = map(list, (xaxis, yaxis))
    (xmin, xmax, ymin, ymax) = (xaxis[0], xaxis[-1], yaxis[0], yaxis[-1])
    (xscale, yscale) = (self.xscale, self.yscale)

    black = "black"
    widths = [1, 2]
    font=("Times New Roman", 18)

    # x-axis grid lines
    xt = (xaxis[1] - xaxis[0]) * (xtick or tick)
    for i in xaxis:
      self.line((i, ymin - xt, i, ymax), width=widths[i == 0], colour=black)

    # y-axis grid lines
    yt = (yaxis[1] - yaxis[0]) * (ytick or tick)
    for i in yaxis:
      self.line((xmin - yt, i, xmax, i), width=widths[i == 0], colour=black)

    # x-axis labels
    if xlabels:
      xlabels = list(xlabels)
      n = len(xlabels) - 1
      for (i, t) in enumerate(xlabels):
        x = (xmax - xmin) * i / n
        self.label((xmin + x, ymin - 10 / yscale), t, colour=black, anchor="n", font=font)

    # y-axis labels
    if ylabels:
      ylabels = list(ylabels)
      n = len(ylabels) - 1
      for (i, t) in enumerate(ylabels):
        y = (ymax - ymin) * i / n
        self.label((xmin - 10 / xscale, ymin + y), t, colour=black, anchor="e", font=font)

    # x-axis text (Unicode 0x2192 = \N{RIGHTWARD ARROW})
    if xtext and not(Tk.TkVersion < 8.6):
      self.label((xmin, ymin - 50 / yscale), xtext + u" \u2192", anchor="w", font=font)

    # y-axis text
    if ytext and not(Tk.TkVersion < 8.6):
      self.label((xmin - 50 / xscale, ymin), ytext + u" \u2192", anchor="w", angle=90, font=font)

  # plot a polyiamond grid using colours from cols
  def polyiamonds(self, grid, cols=dict()):
    (xf, yf) = (0.5, 0.75 ** 0.5)
    # plot the cells
    for ((x, y), i) in grid.items():
      kw = dict(outline="black", width=3, fill=cols.get(i, "white"))
      (y2, r) = divmod(y, 2)
      x += xf * y2
      if r == 0:
        # upward pointing
        self.polygon((x, y2 * yf, x + xf, (y2 + 1) * yf, x + 1, y2 * yf), **kw)
      else:
        # downward pointing
        y2 += 1
        self.polygon((x + 3 * xf, y2 * yf, x + xf, y2 * yf, x + 2 * xf, (y2 - 1) * yf), **kw)
