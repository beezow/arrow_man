import itertools
import math
from arena import Arena
from archer import ArcherUser, ArcherCPU

#takes two parametric equations in lambda form and generates a list of waypoints as PVectors
def gen_waypoints(x, y, t_interval, t_step):
    path = []
    for t in range(t_interval[0], t_interval[1], t_step):
        print(t)
        path.append(PVector(x(t), y(t)))
    return path

x = lambda t: 400.0*math.cos(t/200.0)+960.0
y = lambda t: 300.0*math.sin(t/200.0)+540.0
arena = None
path = gen_waypoints(x, y, (0,1257), 1)

def populate():
    global arena
    p1 = ArcherUser(speed=1, shoot_freq=800, size=100, color=(255,255,0), pos=PVector(100,100), arrow_speed=10)
    p2 = ArcherCPU(path, speed=1, shoot_freq=1000, size=75, color=(255,0,255), accuracy=2, arrow_speed=10)
    arena = Arena()
    arena.add_archer(p1)
    arena.add_archer(p2)

    arena.populate_keyDict()


def setup():
    fullScreen() #size(980, 540)

    populate()
    colorMode(RGB, 255, 255, 255)
    frameRate(144)
    noStroke()
    background(0)
    
    
def draw():
    #print(frameRate)
    background(0)
    if arena.update() == 0:
        populate()

    
def keyPressed():
    arena.keyDict[key] = True
    
def keyReleased():
    arena.keyDict[key] = False
    
