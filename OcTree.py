import math, random
import pygame, sys

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255

# ---------------------------------- #

class Point:

    def __init__(self,x,y,z,r=10):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

class RectPrism:

    def __init__(self,x,y,z,w,h,d):
        """Creates a boundary, at a given location using Cart. points and width height and depth parameters"""
        self.x = x
        self.y = y
        self.z = z

        self.w = w
        self.h = h
        self.d = d

    def contains(self, particle):
        """Checks if particle is in the boundary"""
        return ( particle.x>self.x-self.w and particle.x<=self.x+self.w and particle.y>self.y-self.h and particle.y<=self.y+self.h and particle.z>self.z-self.d and particle.z<=self.z+self.d)

class OcTree:

    def __init__(self,boundary, capacity):
        """ Has option to hold 8 sub OcTree children, will hold points within  """
        self.cap = capacity
        self.divided = False
        self.boundary = boundary
        self.particles = []

    def insert(self,particle):

        if not self.boundary.contains(particle):
            return False

        if len(self.particles) < self.cap:
            self.particles.append(particle)
            return True

        if not self.divided:
            self.branch()

        return (self.oct1.insert(particle) or self.oct2.insert(particle) or self.oct3.insert(particle) or self.oct4.insert(particle) or self.oct5.insert(particle) or self.oct6.insert(particle) or self.oct7.insert(particle) or self.oct8.insert(particle))

    def branch(self):


        """ This function creates the children for the current OcTree object """

        bnw = RectPrism(self.boundary.x - self.boundary.w/2, self.boundary.y - self.boundary.h/2, self.boundary.z + self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)
        bne = RectPrism(self.boundary.x + self.boundary.w/2, self.boundary.y - self.boundary.h/2, self.boundary.z + self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)
        bsw = RectPrism(self.boundary.x - self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.z + self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)
        bse = RectPrism(self.boundary.x + self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.z + self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)

        tnw = RectPrism(self.boundary.x - self.boundary.w/2, self.boundary.y - self.boundary.h/2, self.boundary.z - self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)
        tne = RectPrism(self.boundary.x + self.boundary.w/2, self.boundary.y - self.boundary.h/2, self.boundary.z - self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)
        tsw = RectPrism(self.boundary.x - self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.z - self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)
        tse = RectPrism(self.boundary.x + self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.z - self.boundary.d/2, self.boundary.w/2,self.boundary.h/2,self.boundary.d/2)

        self.oct1 = OcTree(bnw,self.cap)
        self.oct2 = OcTree(bne,self.cap)
        self.oct3 = OcTree(bsw,self.cap)
        self.oct4 = OcTree(bse,self.cap)

        self.oct5 = OcTree(tnw,self.cap)
        self.oct6 = OcTree(tne,self.cap)
        self.oct7 = OcTree(tsw,self.cap)
        self.oct8 = OcTree(tse,self.cap)

        self.divided = True

    def getChildren(self):
        if self.divided:
            return [self.oct1,self.oct2,self.oct3,self.oct4, self.oct5,self.oct6,self.oct7,self.oct8]
        else:
            return False


def drawtree(oct):

    if oct.divided:
        for oct_elem in oct.getChildren():
            drawtree(oct_elem)
    else:
        x,y,z = oct.boundary.x+500, oct.boundary.y+500, oct.boundary.z+500
        w,h,d = oct.boundary.w, oct.boundary.h, oct.boundary.d

        pygame.draw.rect(screen,white, [x,y, w,h], 1)

def drawparticles(oct):

    for p in oct.particles:
        pygame.draw.circle(screen,white, [p.x+500,p.y+500], p.r)

    if oct.divided:
        for oct_elem in oct.getChildren():
            for p in oct_elem.particles:
                pygame.draw.circle(screen,white, [p.x+500,p.y+500], p.r)

# Primary Boundaries
xmin, xmax = -500, 500
ymin, ymax = -500, 500
zmin, zmax = -500, 500

bound = RectPrism(xmin,ymin,zmin,1000,1000,1000)
oct = OcTree(bound,4)

npoints = 50
# Filling with points
for i in range(npoints):
    p = Point(random.randint(xmin,xmax), random.randint(ymin,ymax), random.randint(zmin,zmax))
    oct.insert(p)


# "game loop"
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Begin Drawing
    screen.fill(black)

    drawtree(oct)
    drawparticles(oct)

    pygame.display.flip()

pygame.quit()
