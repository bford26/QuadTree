import math, random
import pygame, sys

from pygame.locals import *

class particle:

    def __init__(self,x,y,r=5):
        self.x = x
        self.y = y
        self.r = r
        self.highlight = False

    def move(self,mx,my):
        if mx == None and my == None:
            self.x += 2*random.random()-1
            self.y += 2*random.random()-1
        else:
            if mx > self.x:
                self.x += 1
            else:
                self.x -= 1

            if my > self.y:
                self.y += 1
            else:
                self.y -= 1

    def collide(self,others):

        self.highlight = False
        for o in others:
            if not self == o:
                d = math.sqrt((self.x-o.x)**2 + (self.y-o.y)**2)
                if d < o.r + self.r:
                    if o.x > self.x:
                        o.x += 2
                        p.x -= 2
                    else:
                        o.x -= 2
                        p.x += 2
                    if o.y > self.y:
                        o.y += 2
                        p.y -= 2
                    else:
                        o.y -= 2
                        p.y += 2

                    self.highlight = True


class Rect:

    def __init__(self, x, y, w, h):

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self,particle):
        return (particle.x>self.x and particle.x<=self.x+self.w and particle.y>self.y and particle.y<=self.y+self.h)


class Quadtree:

    def __init__(self, boundary, capacity=5):

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

        return (self.TR.insert(particle) or self.TL.insert(particle) or self.BR.insert(particle) or self.BL.insert(particle) )

    def branch(self):
        TR = Rect(self.boundary.x + self.boundary.w/2, self.boundary.y, self.boundary.w/2, self.boundary.h/2)
        TL = Rect(self.boundary.x, self.boundary.y, self.boundary.w/2, self.boundary.h/2)
        BR = Rect(self.boundary.x + self.boundary.w/2, self.boundary.y + self.boundary.h/2, self.boundary.w/2, self.boundary.h/2)
        BL = Rect(self.boundary.x, self.boundary.y + self.boundary.h/2, self.boundary.w/2, self.boundary.h/2)

        self.TR = Quadtree(TR,self.cap)
        self.TL = Quadtree(TL,self.cap)
        self.BR = Quadtree(BR,self.cap)
        self.BL = Quadtree(BL,self.cap)

        self.divided = True

    def getChildren(self):

        if self.divided:
            return [self.TR, self.TL, self.BR, self.BL]
        else:
            return False


def drawTree(qtree):

    x,y = qtree.boundary.x, qtree.boundary.y
    w,h = qtree.boundary.w, qtree.boundary.h
    pygame.draw.rect(screen, white, [math.floor(x),math.floor(y),w,h], 1)

    for p in qtree.particles:
        if p.highlight:
            pygame.draw.circle(screen, white, [round(p.x), round(p.y)], p.r)
        else:
            pygame.draw.circle(screen, grey, [round(p.x), round(p.y)], p.r)

    if qtree.divided:
        for quad in qtree.getChildren():
            drawTree(quad)

def Collided(qtree):

    if qtree.divided:
        for quad in qtree.getChildren():
            Collided(quad)
    else:
        for p in qtree.particles:
            p.collide(qtree.particles)


#===========================#

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
run = True

black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255
grey = 50,50,50

#===========================#


nparticles = 1000

xmin, xmax = 0, width
ymin, ymax = 0, height

bound = Rect(0,0,width,height)


# Create the particle dist.
particles = [ None for i in range(nparticles) ]
for i in range(nparticles):
    p = particle(random.randint(xmin,xmax), random.randint(ymin,ymax))
    particles[i] = p
    # qt.insert(p)


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                Mx,My = pygame.mouse.get_pos()
        else:
            Mx,My = None, None
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                run = False

    screen.fill(black)

    # Because the particles move every frame we have to overwrite the quadtree
    qt = Quadtree(bound, 6)
    for p in particles:
        qt.insert(p)

    #DRAW TREE AND PARTICLES
    drawTree(qt)

    pygame.display.flip()

    #MOVE PARTICLES
    for p in particles:
        p.move(Mx,My)

    # Check particles
    Collided(qt)

print("Game Over")
pygame.quit()
