#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:58:37 2020

@author: elenadisvidisdottir
"""

#Mayhem test movement from breakout istedenfor boids

#Import the predefined libraries used
from pygame import Vector2
import pygame
import random 
import numpy as np

#Define the size of the screen
SCREEN_X = 520
SCREEN_Y = 700
#Background filename image
BG_FNAME = "/Users/elenadisvidisdottir/Documents/3. aret/INF-1400/Mayhem_ASS3/Screenshot 2020-03-24 at 13.48.43.png"
JET_FNAME = "/Users/elenadisvidisdottir/Documents/3. aret/INF-1400/Mayhem_ASS3/jet.png"
JET2_FNAME = "/Users/elenadisvidisdottir/Documents/3. aret/INF-1400/Mayhem_ASS3/jet2.jpg"

pygame.init()

#Define the screen, backround image and object images
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
background_img = pygame.image.load(BG_FNAME)
jet_img = pygame.image.load(JET_FNAME)
sizejet = 40
jet_imgscaled = pygame.transform.scale(jet_img, (sizejet,sizejet))   #40x40x32
#for jet2
jet2_img = pygame.image.load(JET2_FNAME)
jet2_imgscaled = pygame.transform.scale(jet2_img, (sizejet,sizejet)) 


#Define some colors
blue = (173,216,230)
gray = (128,128,128)
white = (255,255,255)
peach = (255,200,180)
green = (0,255,0)
red = (255,0,0)
black= (0,0,0)



"""
Vil sette rotasjon på bullet og.
Vil sette opp alle funksjonen for jet2 og.

Vil sette opp funksjonen sånn at når en bullet colliderer med en jet forsvinner
 jetten av skjermen. Og det at når en bullet flyr ut av skjermen blir den deleted.

Da har eg fått ferdig gjørt alt av bevegelse av jetten :) 

Etter det kan eg begynne med å lage "world", men en landningsplass for bensinstasjon.
"""

jet_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()


#Parent class
class JetParent(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        #Want to have the posision and the image different for each jet!!
        self.pos = Vector2(random.randint(0,SCREEN_X),random.randint(0,SCREEN_Y/2)) #Vector2(SCREEN_X/2 + sizejet, SCREEN_Y/2 -sizejet) #
        self.image = jet_imgscaled
        
        #Important to define a original image since i will be rotating the self.img
        self.org_img = jet_imgscaled
        
        #Want movement along x and y axes!
        self.movement = Vector2(0,0)
        #self.vel = Vector2(4,4)
        #The gravitation force
        self.acc = Vector2(0,0.03)
        
        #Try rotation
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 
        self.angle = 0
        
    #Try the collision
    def collide(self, spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False):
            self.movement.y = -self.movement.y
            self.movement.x = -self.movement.x
        
    #Keep the jet on the screen
    def checkbounds(self):
        #The vector for the movement of the ball is the velocity multiplied by time passed
        #self.pos += self.vel
        
        #Same velocity but in opposite direction   
        #Keep the ball on the screen on the right hand side
        if self.pos.x > SCREEN_X - self.image.get_width()/2: 
            #self.vel.x = -abs(self.vel.x)
            self.movement = Vector2(0,0)
        #The left hand side of screen
        if self.pos.x < 0 + self.image.get_width()/2:       
            self.movement = Vector2(0,0)
        #The roof of the screen
        if self.pos.y < 0 + self.image.get_width()/2:       
            self.movement = Vector2(0,0)
        #The floor of the screen
        if self.pos.y > SCREEN_Y - self.image.get_width()/2:
            self.movement = Vector2(0,0)
            
    
    def rotation(self, angle):
        x, y = self.rect.center #Define the center of the original image
        self.image = pygame.transform.rotate(self.org_img, self.angle) #Rotate the original image
        self.angle += angle #1 % 360 #Define the angle , avoiding overlap
        #x, y = self.rect.center #Define the center of the original image
        self.rect = self.image.get_rect()  #The rectangle of the rotated image
        #har plusset på movement her??
        self.rect.center = (x, y)  #Set the center of the rotated image (rectangle), back to original center
    
    def moveup(self):
        #Angle is the rotation
        speed_down = 12
        direction = Vector2(0,-1).rotate(-self.angle) /speed_down
        #Define the movement to be in the direction of the jet
        self.movement += direction
        
    def shoot(self):
        bullet = Bullet(self.pos, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)
        print(all_sprites)
        print(bullets)
        
        
 
class Jet(JetParent):
    def __init__(self):
        #Call the parent class
        super().__init__()
                
                
        #Define the position and image of this jet
        self.pos = Vector2(SCREEN_X/2 + sizejet, SCREEN_Y/2 -sizejet)
        self.image = jet_imgscaled
        self.org_img = jet_imgscaled #Using the original image in the rotation function so I need that one here
    
    def update(self):
        #Give the jet movement by updating its position
        self.pos += self.movement
        self.rect.center = self.pos
        self.checkbounds()
        
        #Get pressed, control the jet here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.moveup()
        if keys[pygame.K_LEFT]:
            self.rotation(2)
        if keys[pygame.K_RIGHT]:
            self.rotation(-2)
    
        if not keys[pygame.K_UP]:
            self.movement += self.acc  #Ved dette får eg acceleration i y retning, dvs begge i positiv og negativ retning  
        
    def draw(self):
        screen.blit(self.image, self.rect) #Important to use self.rect here!
        


class Jet2(JetParent):
    def __init__(self):
        #Call the parent class
        super().__init__()
    
        #Define the position and image of this jet
        self.pos = Vector2(SCREEN_X/4 + sizejet, SCREEN_Y/4 -sizejet)
        self.image = jet2_imgscaled
        self.org_img = jet2_imgscaled #Using the original image in the rotation function so I need that one here
        
    def update(self):
        #Give the jet movement by updating its position
        self.pos += self.movement
        self.rect.center = self.pos
        self.checkbounds()
        
        #Get pressed, control the jet here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.moveup()
        if keys[pygame.K_a]:
            self.rotation(2)
        if keys[pygame.K_d]:
            self.rotation(-2)
        
        if not keys[pygame.K_w]:
            self.movement += self.acc  #Ved dette får eg acceleration i y retning, dvs begge i positiv og negativ retning
        
    def draw(self):
        screen.blit(self.image, self.rect) #Important to use self.rect here!



#Define a class for shooting
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):   #Have position and angle in the init, will be used to tell where the bullet should shoot from (that is from the polar of the jet)
        pygame.sprite.Sprite.__init__(self)
        
        
        self.pos = pos + Vector2(0,0)   #Kan prøve med (1,1) eller noe annet 
        self.rotation = angle
        
        self.image = pygame.Surface((10,20))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        #Right in front of the jet...  want to use from_polar
        self.maxVel = 10   #av skipet! an integer not a Vector2! Den er lengde av from polar vektoren...
        
        self.bullet_speed = Vector2(0,0)
        #from_polar is a Vector2 function takes in ((length, -angle))
        self.bullet_speed.from_polar((self.maxVel*2,-self.rotation-90))   #Do I have to input the vel of the jet here?
        print(self.bullet_speed)
        """
        #Try rotation
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 
        self.angle = 0
    
    def rotation(self, angle):
        x, y = self.rect.center #Define the center of the original image
        self.image = pygame.transform.rotate(self.org_img, self.angle) #Rotate the original image
        self.angle += angle #1 % 360 #Define the angle , avoiding overlap
        #x, y = self.rect.center #Define the center of the original image
        self.rect = self.image.get_rect()  #The rectangle of the rotated image
        #har plusset på movement her??
        self.rect.center = (x, y)  #Set the center of the rotated image (rectangle), back to original center
        """
    def update(self):
        self.rect.center = self.pos
        self.pos += self.bullet_speed
        
        #Try rotation
        
        
        
        
        #Want to update this so that if there is a collision between the bullet and a jet it is self.kill
        #And also if it leaves the screen self.kill
        
        if pygame.sprite.spritecollide(self, jet_group, True):
            self.kill()
        
    def draw(self):
        screen.blit(self.image, self.rect)
        
        #update and draw the bullet and than call it in the game class

class Game:
    def __init__(self):
        self.jet = Jet()
        self.jet2 = Jet2()
        #self.bullet = Bullet(self.jet.pos, self.jet.angle)
        
        all_sprites.add(self.jet)
        all_sprites.add(self.jet2)
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)
        
    def game_loop(self):
        #Want to run the code 30 times in a second
        #time_passed = self.clock.tick(30)
            
        #This is where the game is actually played
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                
                #Try the shooting 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jet.shoot()
            
            #Try the collision...
            for ajet in jet_group:
                jet_group.remove(ajet)  #Prevent it to collide with it self..
                ajet.collide(jet_group)
                jet_group.add(ajet)
            
            
            #Call out the background on the screen (window). Important to
            #do this first so that other objects are layed ontop of the background
            #self.screen.blit(background_img, (0,0))
            self.screen.fill(white)
            
            
            #Update the sprite groups
            all_sprites.draw(self.screen)
            all_sprites.update()


            
            pygame.display.update()
        

#Call the class and its functions to play the game
game = Game()
if __name__ == "__main__":
    breakout = Game()
    breakout.game_loop()
