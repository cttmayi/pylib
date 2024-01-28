import visdom
import numpy as np

vis = visdom.Visdom()

vis.text('Hello')

vis.image(np.ones((3,100,100)))