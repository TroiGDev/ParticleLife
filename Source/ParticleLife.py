import pygame
import random
import math

pygame.init()
screenWidth = 800
screenHeight = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Particle Life')

#fps display
clock = pygame.time.Clock()
def displayFPS(screen, font_size):
    font = pygame.font.SysFont(None, font_size)
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))  # White text
    screen.blit(fps_text, (10, 10))  # Top-left corner with slight padding

#-----------------------------------------------------------------------------------------------------------------------------------------

class Particle:
    def __init__(self, x, y, color):
        allParticles.append(self)

        self.pos = (x, y)
        self.vel = (0, 0)

        self.color = color
        self.radius = 4

    def drawShadow(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.pos[0], self.pos[1] + self.radius), self.radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def move(self, dTs):
        borderMargin = 20

        if self.pos[0] < borderMargin:
            self.pos = (screenWidth - borderMargin, self.pos[1])
        if self.pos[0] > screenWidth - borderMargin:
            self.pos = (borderMargin, self.pos[1])

        if self.pos[1] < borderMargin:
            self.pos = (self.pos[0], screenHeight - borderMargin)
        if self.pos[1] > screenHeight - borderMargin:
            self.pos = (self.pos[0], borderMargin)

        self.pos = (self.pos[0] + self.vel[0] * dTs, self.pos[1] + self.vel[1] * dTs)

def particleType(count, color):
    particles = []

    for i in range(count):
        newParticle = Particle(random.randint(0, screenWidth), random.randint(0, screenHeight), color)
        particles.append(newParticle)

    return particles

def rule(group1, group2, dTs, g, rMax, frictionFactor):
    for a in group1: 
        totalForceX = 0
        totalForceY = 0
        for b in group2:
            rX = b.pos[0] - a.pos[0]
            rY = b.pos[1] - a.pos[1]
            r = math.sqrt(rX*rX + rY*rY)
            if r > 0 and r < rMax:
                f = force(r/rMax, g)
                totalForceX += rX / r * f
                totalForceY += rY / r * f
        
        totalForceX *= rMax
        totalForceY *= rMax

        a.vel = (a.vel[0] * frictionFactor, a.vel[1] * frictionFactor)

        a.vel = (a.vel[0] + totalForceX * dTs, a.vel[1] + totalForceY * dTs)
        
def force(r, g):
    beta = 0.3

    if r < beta:
        return r / beta - 1
    elif beta < r and r < 1:
        return g * (1 - abs(2 * r - 1 - beta) / (1 - beta))
    else:
        return 0

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def drawGroupLines(types, groupRange):
    for type in types:
        for a in type:
            for b in type:
                if a != b:
                    v = (b.pos[0] - a.pos[0], b.pos[1] - a.pos[1])
                    dist = math.sqrt(v[0] * v[0] + v[1] * v[1])
                    if dist <= groupRange:
                        pygame.draw.aaline(screen, a.color, a.pos, b.pos)

#-----------------------------------------------------------------------------------------------------------------------------------------

#initialize particle types
allParticles = []
types = [particleType(50, (255, 0, 0)), particleType(50, (0, 255, 0)), particleType(50, (0, 0, 255)), particleType(50, (255, 0, 255)), particleType(50, (255, 255, 0)), particleType(50, (0, 255, 255))]

r = [random.randint(-1, 1) for i in range(len(types) ** 2)]

#get delta time initial ticks
prevT = pygame.time.get_ticks()

running = True
while running:

    #update delta time
    currT = pygame.time.get_ticks()
    dTms = currT - prevT
    dTs = dTms / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                r = [random.randint(-1, 1) for i in range(len(types) ** 2)]
        
    # Fill screen
    screen.fill((20, 20, 20))

    #rules
    c = 0
    for type in types:
        for otherType in types:
            rule(type, otherType, dTs * 2, r[c], 80, 0.99)
            c+=1

    #move all particles
    for particle in allParticles:
        particle.move(dTs)

    #draw all particles:
    for particle in allParticles:
        particle.drawShadow()

    for particle in allParticles:
        particle.draw()

    #draw line groups
    drawGroupLines(types, 20)

    # Update the display (buffer flip)
    displayFPS(screen, 25)
    pygame.display.flip()
    clock.tick(60)

    #update delta time
    prevT = currT

# Quit Pygame
pygame.quit()
