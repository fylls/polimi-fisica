# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:04:25 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, sin, cos, arrow, sphere, quad, text, cross, rate, mag, textures, vertex, pi, color

def vectorize(function):
    
    def inner(*args,**kwargs):
        vs = function(*args)
        sys = args[0]
        colors = [color.green,color.white,color.magenta,color.cyan]
        for index, v in enumerate(vs):
            if not inner.called: 
                inner.vector[index]=arrow(color=colors[index],shaftwidth=0.3,headwidth=1,headlength=1)               
            inner.vector[index].pos = sys.body.pos
            inner.vector[index].axis = v
        inner.called = True
        return vs
    inner.called = False
    inner.vector = {}
    return inner

class pendolum:
    
    g = -9.81
    
    def  __init__(self, mass, length, angle0):
        
        self.mass = mass
        self.length = length
        self.angle = angle0
        self.omega = 0
        # create mass
        body = sphere(radius = 1.2)
        body.pos = vector(length*sin(angle0), length*(1-cos(angle0)),0)
        body.color = color.orange
        self.body = body
        #create cord
        self.rope = arrow(pos = vector(0,length,0),
                          axis = body.pos, 
                          shaftwidth=0.15, headwidth=0.001, headlength = 0.001,
                          color = color.gray(0.7))
        self.rope.axis = self.body.pos - vector (0,length,0)  
        
    def set_velocity(self, dt):
        alpha = self.g * sin(self.angle) / self.length
        self.omega += alpha * dt
        
    def set_position(self, dt):
        self.angle += self.omega * dt
        self.body.pos = vector(self.length*sin(self.angle), self.length*(1-cos(self.angle)),0)
        self.rope.axis = self.body.pos - vector (0,self.length,0) 
    
    @vectorize
    def calculate_vectors(self):
        g = self.g
        origin = vector(0,self.length,0)
        r = self.body.pos-origin
        av = self.omega*vector(0,0,1)
        v = cross(av, r)   
        weight = g *vector(0,1,0) * self.mass
        tension = self.mass * (r/mag(r)*g*cos(self.angle) + cross(av,v)) 
        acceleration = (tension + weight) / self.mass

        return (v, weight,tension,acceleration)

LENGTH = 20
THETA = 30 * pi/180
MASS = 1
    
p = pendolum(MASS,LENGTH,THETA)

dt = 0.01    

scene.center = vector(0,LENGTH/2,0)
scene.waitfor('textures')

# draw ceiling
a = vertex( pos=vector(-LENGTH/2,LENGTH,-LENGTH/2), texpos=vector(0,0,0))
b = vertex( pos=vector(LENGTH/2,LENGTH,-LENGTH/2) , texpos=vector(1,0,0))
c = vertex( pos=vector(LENGTH/2,LENGTH,LENGTH/2)  , texpos=vector(1,1,0))
d = vertex( pos=vector(-LENGTH/2,LENGTH,LENGTH/2) , texpos=vector(0,1,0))
Q = quad( vs =[a,b,c,d], texture = textures.wood )
    
while True:
    rate(100)
    p.set_velocity(dt)
    p.set_position(dt)
    p.calculate_vectors()