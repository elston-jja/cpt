#!/usr/bin/python2
'''
Main file of Spark Night game
@author: Elston Almeida and Lance Pereira
@date: June 17, 2016
@course: ICS3U1
'''

# SOURCES

# blurSurf function
# http://www.akeric.com/blog/?p=720

# level making and other functions
# http://pygame.org

# Wizard sprite
# http://vignette3.wikia.nocookie.net/scribblenauts/images/f/fc/Wizard_Male.png/revision/latest?cb=20130215182314

# Player sprite
# http://piq.codeus.net/static/media/userpics/piq_244306_100x100.png

# WoodSprite
# http://www.thewallpapers.org/photo/34665/Wood-003.jpg

import pygame
from math import *
from map_list import maps
#from ImagesAndSounds import *
global done

class Player(pygame.sprite.Sprite):

    '''
    Class creates player objects that are used later for enemies
    and the main player
    '''

    def __init__(self, PlayerWidth, PlayerHeight):
        pygame.sprite.Sprite.__init__(self)
        # Width and height of image
        self.width = PlayerWidth
        self.height = PlayerHeight
        # Creates images (CREATE TWO, one for reference later)
        self.imageMaster = pygame.Surface([self.width, self.height], pygame.FULLSCREEN)
        self.image = self.imageMaster
        # Fills the image with white
        self.image.fill(white)
        # Makes transparent background
        # YOU NEED THIS FOR IT TO ROTATE
        self.image.set_colorkey(white)
        # Get rect frame of image
        self.rect = self.image.get_rect()
        # angle to face mouse
        self.rect.x = 150
        self.rect.y = 150
        # Just placeholder
        self.angle = 0
        self.vely = 2
        self.velx = 2
        #Movement placeholder positions
        self.mouseMovePos = 0
        self.movedy = 0
        self.movedx = 0
        #movement placeholder velocities
        self.xvelocity = 0
        self.yvelocity = 0
        self.remainderxvelocity = 0
        self.remainderyvelocity = 0
        #Timer placeholder for how many seconds movement takes
        self.moveTimer = 0
        #Timer placeholder for how many seconds movement
        #takes the finer movement
        self.remainderMoveTimer = 2
        #Tracer values for all velocities
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        #Dont know what this guy does, but probabley sets
        #what the moveTimr can do
        self.moveFactor = 40
        self.map_number = 0
        #Boolean value that determines if a wall was hit
        self.wallCollision = pygame.sprite.spritecollide(self, wall_list, False)
        self.obstacle = wall_list

        #Adds pickachu image
        self.imageMasterSprite = pygame.image.load("ImagesAndSounds/pickachu.png").convert()
        self.imageMasterSprite = pygame.transform.rotate(self.imageMasterSprite, 90)
        self.imageMasterSprite = pygame.transform.scale(self.imageMasterSprite, (35,35))
        self.imageSprite = self.imageMasterSprite
        self.imageSprite.set_colorkey(white)

    def get_pos(self):
        '''
        Gets the position and angle of the mouse, and adjusts the
        players angle that they are viewing
        '''
        # Get mouse cords while game running
        self.pos = pygame.mouse.get_pos()

        # Get change in X and y dy/dy
        self.dy = self.pos[1] - self.rect.centery
        self.dx = self.pos[0] - self.rect.centerx

        # Get angle from mouse and player
        self.mouse_angle = atan2(- self.dy, self.dx)

        # Var for move function
        self.mouse_angle = degrees(self.mouse_angle)
        #Possibley does nothing
        self.angle_move = self.mouse_angle

        # Sets angle value in class
        self.angle = self.mouse_angle
        if self.angle < 0:
            self.angle += 360

    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the
        #difference in x was 80, this would divide that by say 40 and get 2,
        # so each update would add 2 to posx
        self.wallCollision = pygame.sprite.spritecollide(self, self.obstacle, False)

        #Gets position of mouse and finds difference in x and y cords of
        #both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the
        #character moves
        self.xvelocity = self.movedx / self.moveFactor
        self.yvelocity = self.movedy / self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders
        #that are left, and these values store them so they can be
        # added in between big velocity movements
        self.remainderxvelocity = (self.movedx % self.moveFactor) /\
        (self.moveFactor / self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times to
        #update player pos before it reaches destination
        self.moveTimer = self.moveFactor

    def changeVelocityAfterCollision(self):
        '''
        Sets the velocities of players to ad absolute of 1 after a collision
        '''
        #All of the name velocities that we need to use in the next few
        #commands for string insertion
        velocities = [
            'xvelocity', 'yvelocity', 'remainderxvelocity', 'remainderyvelocity'
            ]

        #Each loop changes a velocity after a collision only if the
        #velocity is not the same as it was before
        for values in velocities:
            #All these variables are strings that will be executed as commands
            velocity = 'velocity = self.%s' % values
            currentTrace = 'currentTrace = self.trace%s' % values
            traceAssign = 'self.trace%s = self.%s' % (values, values)
            changeVelocity = ('self.%s = -1*self.%s/abs(self.%s)') %\
             (values, values, values)
            #assigns variable currentTrace a trace velocity
            #(previous velocity) value
            exec(currentTrace)
            #Assigns velocity the current velocity value
            exec(velocity)
            if abs(velocity) > 0 and currentTrace != velocity:
                #Changes the velocity to an absolute 1
                exec(changeVelocity)
                #sets the trace to current
                exec(traceAssign)

    def moveUpdate(self):
        '''
        Changes the x and y position of the player
        '''
        #Checks to see if the move timer is over
        if self.moveTimer > 0:
            #lets the remainder update every 2 loops
            if self.moveTimer % 2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            #Updates position eith velocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity
            #Checks to see if a collision occured after the move
            self.wallCollision = pygame.sprite.spritecollide(
                self, wall_list, False
            )
            self.exit_level = pygame.sprite.spritecollide(
                self, exit_list, False
            )
            #If collision was at exit block, loads new map
            if self.exit_level:
                self.map_number += 1
                self.map_number = self.map_number
                change_map("map" + str(self.map_number))
            #if not exit block, but normal wall cancel last movement
            elif self.wallCollision:
                if self.moveTimer % 2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                #and set velocity to opposite direction equal to 1
                self.changeVelocityAfterCollision()

            self.moveTimer -= 1

    def attack_Q(self):
        '''
        Creates the Q electricity ball attack, and projects
        it to wherever the mouse was
        '''
        orb = ElectricityOrb()
        attack_sprites_list.add(orb)
        all_sprites_list.add(orb)

    def attack_W(self):
        '''
        Calls the field of effect attack based on the loation of the player
        '''
        area_of_effect = FieldofEffect()
        attack_sprites_list.add(area_of_effect)
        all_sprites_list.add(area_of_effect)

    def update(self):
        '''
        Updates all of the movement attributes of the player
        each loop of the main loop
        '''

        #Movement Update
        self.moveUpdate()
        # Gets mouse position
        self.get_pos()
        # Gets the old center point
        self.centerpoint = self.rect.center
        # Rotate sprite
        self.image = pygame.transform.rotate(self.imageMaster, self.angle)
        self.imageSprite = pygame.transform.rotate(self.imageMasterSprite, self.angle)
        # Get rectangle frame
        self.rect = self.image.get_rect()
        # Sets the new image to the old center point
        # Makes sure the sprite does not go flying to oblivion
        self.rect.center = self.centerpoint

        screen.blit(self.imageSprite, (self.rect.x, self.rect.y))


class Enemy(Player):

    def __init__(self,spawnx,spawny):
        '''
        Explenations of attributes in Player Class
        '''
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, 30, 30)
        self.rect.x = spawnx
        self.rect.y = spawny
        self.health = 3
        self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
        self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
        self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, False)
        self.imageMasterSprite = pygame.image.load("ImagesAndSounds/Wizard_Male.png").convert()
        self.imageMasterSprite = pygame.transform.scale(self.imageMasterSprite, (30,30))
        self.imageMasterSprite = pygame.transform.rotate(self.imageMasterSprite, 180)
        self.imageSprite = self.imageMasterSprite
        self.imageSprite.set_colorkey(white)
        self.isBoss = False

    def move(self):
        '''
        Updates the velocities of the enemy by, checking where the player is and drawing hypotonus to it
        '''
        #determines how many increment to move the object by, say the
        #difference in x was 80, this would divide that by say 40 and get 2,
        # so each update would add 2 to posx
        self.wallCollision = pygame.sprite.spritecollide(self, self.obstacle, False)

        #Gets position of mouse and finds difference in x and y cords of
        #both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = player.rect.centerx - self.rect.center[0]
        self.movedy = player.rect.centery - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the
        #character moves
        self.xvelocity = self.movedx / self.moveFactor
        self.yvelocity = self.movedy / self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders
        #that are left, and these values store them so they can be
        # added in between big velocity movements
        self.remainderxvelocity = (self.movedx % self.moveFactor) /\
        (self.moveFactor / self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times to
        #update player pos before it reaches destination
        self.moveTimer = self.moveFactor

    def moveUpdate(self):
        '''
        Changes the x and y position of the enemy
        '''
        #Checks to see if the move timer is over
        if self.moveTimer > 0:
            #lets the remainder update every 2 loops
            if self.moveTimer % 2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            #Updates position eith velocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity
            #Checks to see if a collision occured after the move
            self.wallCollision = pygame.sprite.spritecollide(
                self, wall_list, False
            )
            enemy_list.remove(self)
            self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
            self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, True)
            self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
            #print self.player_collide
            #If collision was at exit block, loads new map

            if self.wallCollision or self.enemey_collide:
                if self.moveTimer % 2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                #and set velocity to opposite direction equal to 1
                self.changeVelocityAfterCollision()

            if self.attack_collide:
                self.health -= 1

            if self.player_collide and not self.isBoss:
                #print 'What up my boi'
                overlay.lives -= 1
                all_sprites_list.remove(self)
            else:
                enemy_list.add(self)

            self.moveTimer -= 1

    def update(self):
        self.move()

        if self.health <= 0:
            all_sprites_list.remove(self)

        Player.update(self)

class BossEnemy(Enemy):

    def __init__(self,spawnx,spawny):
        '''
        Explanation of attributes in Parent class
        '''
        Player.__init__(self,spawnx,spawny)
        self.health = 300
        #self.image = ""
        self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
        self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
        self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, False)
        self.imageMasterSprite = pygame.image.load("ImagesAndSounds/pickachu.png").convert()
        self.imageMasterSprite = pygame.transform.scale(self.imageMasterSprite, (80,80))
        #self.imageMasterSprite = pygame.transform.rotate(self.imageMasterSprite, 180)
        self.imageSprite = self.imageMasterSprite
        self.imageSprite.set_colorkey(white)
        self.isBoss = True

    def get_pos(self):
        #Done to overide the rotation of boss, as boss rotations make it too dangerous
        pass

    def attack_Q(self):
        '''
        Creates the Q electricity ball attack, and projects
        it to wherever the mouse was
        '''
        orb = ElectricityOrb(True)
        attack_sprites_list.add(orb)
        all_sprites_list.add(orb)

    def update(self):
        self.angle_move = 0
        self.attack_Q()
        Player.update(self)

class ElectricityOrb(Player):

    def __init__(self, isBoss = False):
        '''
        attributes explained in Player class
        '''
        pygame.sprite.Sprite.__init__(self)
        # Width and height of image
        self.width = 30
        self.height = 30
        # Creates images (CREATE TWO, one for reference later)
        self.imageMaster = pygame.Surface([self.width, self.height])
        self.image = self.imageMaster
        # Fills the image with white
        #self.image.fill(white)
        self.image.fill(bg)
        # Makes transparent background
        # YOU NEED THIS FOR IT TO ROTATE
        self.image.set_colorkey(bg)
        #self.image.set_colorkey(red)
        # Get rect frame of image
        self.rect = self.image.get_rect()
        # angle to face mouse
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        # Just placeholder
        self.angle = 0
        self.vely = 2
        self.velx = 2
        #Movement placeholder positions
        self.mouseMovePos = 0
        self.movedy = 0
        self.movedx = 0
        #movement placeholder velocities
        self.xvelocity = 0
        self.yvelocity = 0
        self.remainderxvelocity = 0
        self.remainderyvelocity = 0
        #Timer placeholder for how many seconds movement takes
        self.moveTimer = 0

        #Timer placeholder for how many seconds movement takes the
        # finer movement
        self.remainderMoveTimer = 2
        #Tracer values for all velocities
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        #Dont know what this guy does, but probabley sets what
        # the moveTimr can do
        self.moveFactor = 40
        #Boolean value that determines if a wall was hit
        self.wallCollision = pygame.sprite.spritecollide(self, wall_list, False)
        self.orb_image = pygame.image.load("ImagesAndSounds/better_orb.png").convert()
        self.orbExplision_image = pygame.image.load("ImagesAndSounds/orb_explosion_large.png").convert()
        self.orb_image.set_colorkey(bg)
        self.orbExplision_image.set_colorkey(bg)
        self.obstacle = wall_list
        #Determines which image to load for the orb
        self.exploded = False
        self.isBoss = isBoss
        self.move()

    """def move(self):
            Player.move(self)"""

    def get_pos(self):
        #Stops rotation of orbs, as it messes with collisions
        pass

    def moveUpdate(self):
        '''
        Keeps the electrriy ball moving to where the player clicked it to until collision
        '''
        #Checks to see if the move timer is over
        if self.moveTimer > 0:
            #lets the remainder update every 2 loops
            if self.moveTimer%2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            #Updates position eith velocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity
            #Checks to see if a collision occured after the move
            if self.wallCollision and self.moveTimer == 14:
                isDoubleCollision = True
            else:
                isDoubleCollision = False
            self.wallCollision = pygame.sprite.spritecollide(self,wall_list,False)
            self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
            self.wallCollisionTrace = None
            #self.enemy_collision = pygame.sprite.spritecollide(self,enemy_list,False)
            #If collision was at exit block, loads new map


            if (self.exit_level or self.wallCollision and not isDoubleCollision): #or self.enemy_collision:
                self.moveTimer = 15
                self.exploded = True
                #print "it's colliding"
                self.changeVelocityAfterCollision()
            if self.moveTimer <= 10:
                self.exploded = True
            self.moveTimer -= 1
            #print 'Its subtracting'
        else:
            all_sprites_list.remove(self)

    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the difference
        #in x was 80, this would divide that by say 40 and get 2,
        #so each update would add 2 to posx

        #Gets position of mouse and finds difference in x and y cords
        #of both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        # Divides difference of points by factor that determines
        # how fast the character moves
        self.xvelocity = self.movedx / self.moveFactor
        self.yvelocity = self.movedy / self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders
        # that are left, and these values store them so they can be added
        # in between big velocity movements
        self.remainderxvelocity = (self.movedx % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times
        # to update player pos before it reaches destination
        self.moveTimer = self.moveFactor + 40

    def update(self):
        #Movement Update
        self.moveUpdate()
        # Gets mouse position
        self.get_pos()
        # Gets the old center point
        self.centerpoint = self.rect.center
        # Rotate sprite
        #self.image = pygame.transform.rotate(self.imageMaster, self.angle)
        # Get rectangle frame
        self.rect = self.image.get_rect()
        # Sets the new image to the old center point
        # Makes sure the sprite does not go flying to oblivion
        self.rect.center = self.centerpoint

        if self.exploded:
            self.orbDrawImage = self.orbExplision_image
            #print 'Allah Akbar'
        else:
            self.orbDrawImage = self.orb_image

        screen.blit(self.orbDrawImage, (self.rect.x, self.rect.y))


class FieldofEffect(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        # Initial width, height, and field size
        self.height = 2
        self.width = 2
        self.field_level = 2
        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        # Number of times to loop animation
        self.loop_animation = 1

    def draw(self):
        '''
        Draw radiating circles as attack for player
        '''
        # Increase Field level
        self.field_level += 2

        # Draw Surface
        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        #self.image.fill(red)

        # set center points to player
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery

        # draw circle
        pygame.draw.circle(screen,red,player.rect.center,self.field_level,1)

        # When circle radius(field size) is max, reset the field size
        # reset the width and the height of the image and count to 1 less loop
        if self.field_level > 80:
            self.field_level = 2
            self.loop_animation -= 1
            self.width = 2
            self.height = 2
        # When increase the width and the height by 4 (of surface)
        self.width += 4
        self.height += 4

        # Makes sure the object is removed durring a level change or
        # removes an enemy when hit
        self.check_collisions()

        # When done looping, remove itself from the drawn classes
        if self.loop_animation < 0:
            attack_sprites_list.remove(self)
            all_sprites_list.remove(self)

    def check_collisions(self):
        '''
        Removes the attack, when a new level has been loaded
        '''
        self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
        if self.exit_level:
            all_sprites_list.remove(self)
            attack_sprites_list.remove(self)

    def update(self):
        self.draw()


class Level:
    '''
    Checks the level and display it accoringly
    '''
    def __init__(self,level):
        # State the initial level number
        # Value not needed except for verbosity
        self.level = level
        # Default x y starting block cordinates
        self.x = 0
        self.y = 0
        # Creates object called "list of maps" and I can call all maps
        # From the lists in the maps_list file
        list_of_maps = maps()
        # Get the level from maps_list and load it into the interpreter
        # Change the current level to the list varible in the maps_list file
        exec_var = "self.current_level = list_of_maps." + str(self.level)
        exec (exec_var)
        # Get the lines/rows from each variable in the list
        self.make_level()

    def make_level(self):

        for line_row in self.current_level:
            # Check each character in the row
            for char in line_row:
                # if the character is a 'w' then add a wall block (30,30)
                if char == "w":
                    wall = Wall(self.x,self.y,grey)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                # If the character is an 'e' then add an wall block
                # That when collided can cause to exit
                # As it is added to the exitdoor list (change var is need be)
                if char == "e":
                    exit_ = Wall(self.x,self.y,red)
                    wall_list.add(exit_)
                    exit_list.add(exit_)
                    all_sprites_list.add(exit_)
                elif char == "P":
                    player.rect.x = self.x
                    player.rect.y = self.y
                elif char == "E":
                    enemy = Enemy(self.x,self.y)
                    enemy_list.add(enemy)
                    all_sprites_list.add(enemy)
                    # When drawing each block
                    # (Character in row)
                    # Move 30px to the right
                elif char == "B":
                    boss_enemy = BossEnemy(self.x,self.y)
                    enemy_list.add(boss_enemy)
                    all_sprites_list.add(boss_enemy)
                self.x+= 30
                # When moving down to next row change the Y by 30
                # Reset th X
            self.y+=30
            self.x = 0

class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y,color):

        # Base sprite class with collisions
        pygame.sprite.Sprite.__init__(self)
        # Create the width and height of surface
        self.image = pygame.Surface([30,30])
        self.rect = self.image.get_rect()
        self.color = color
        # Set the colors
        self.image.fill(color)
        self.image.set_colorkey(color)
        # Check to see what color and draw
        # an image accordingly
        self.checkBlockSprite()
        # Set the image to be drawn at given x and y cords
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def checkBlockSprite(self):
        '''
        Checks to see what was the color code of the block
        this enables the program to know what type of block to draw
        using different color codes
        '''
        if self.color == grey:
            self.block = pygame.image.load("ImagesAndSounds/wall.png").convert()
            self.block = pygame.transform.scale(self.block,(30,30))
        else:
            self.block = pygame.image.load("ImagesAndSounds/exit.png").convert_alpha()
            self.block = pygame.transform.scale(self.block,(30,30))

    def update(self):
        screen.blit(self.block,(self.x,self.y))

class Overlay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Declare base amount of lives
        self.mouseflip = False
        self.lives = 3
        # Initialize fonts
        pygame.font.init()
        # Create fontattributes in namespace
        self.font = pygame.font.SysFont("Calibri",20)
        self.options_type = pygame.font.SysFont("Calibri", 50)
        self.pause_type = pygame.font.SysFont("Calibri",80)
        # Display lives_text
        self.live_text = self.font.render("Lives: ",True,bg)
        # Surface created
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        # Set the image of the heart
        self.hearts = pygame.image.load("ImagesAndSounds/heart.png").convert_alpha()
        self.hearts = pygame.transform.scale(self.hearts,(30,30))
        self.isPaused = False


    def update(self):
        '''
        Draw the amount of lives left
        '''
        screen.blit(self.live_text, (40,40))
        if self.lives == 3:
            #Draws three hearts
            screen.blit(self.hearts,(40, 60))
            screen.blit(self.hearts,(80, 60))
            screen.blit(self.hearts,(120, 60))
        if self.lives == 2:
            #Draws 2
            screen.blit(self.hearts,(40, 60))
            screen.blit(self.hearts,(80, 60))
        if self.lives == 1:
            #Please use your brain
            screen.blit(self.hearts,(40, 60))
        if self.lives == 0:
            # resets all values and starts from the beginning
            restart()

    def main_menu(self):
        '''
        Creates a menu loop inside game, and helps to keep events
        '''
        # Text to display
        self.screen_text = ("Press ESC to resume")
        self.music_toggle = ('Press "u" to toggle music')
        self.mouse_toggle = ('Press "y" to toggle mouse action flip')
        self.fullscreen_toggle = ('Press "i" to toggle fullscreen')
        self.quitswitch = ('Press "c" to quit ')
        # render all the types of text | has AA and color: black
        self.pause_render = self.pause_type.render(self.screen_text,True,bg)
        self.options_render = self.options_type.render(self.music_toggle, True, bg)
        self.mouse_render = self.options_type.render(self.mouse_toggle,True,bg)
        self.fullscreen_render = self.options_type.render(self.fullscreen_toggle,True,bg)
        self.quitswitch_render = self.options_type.render(self.quitswitch,True,bg)
        # Take new image when paused and load to be used
        pygame.image.save(screen,"ImagesAndSounds/current_bg.jpg")
        frame = pygame.image.load("ImagesAndSounds/current_bg.jpg")
        # Run nested loop for menu events, waiting for esc key to unlock
        inMenu = True
        while inMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global done
                    done = True
                    inMenu = False
                elif event.type == pygame.KEYDOWN:
                    # Unpause
                    if event.key == pygame.K_ESCAPE:
                        inMenu = False
                    # Toggle music
                    elif event.key == pygame.K_u:
                        self.isPaused = not self.isPaused
                        if self.isPaused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                            self.isPaused = False
                    # Toggle mouse flip from 2 to 0
                    elif event.key == pygame.K_y:
                        self.mouseflip = not self.mouseflip
                    # Toggle fullscreen
                    elif event.key == pygame.K_i:
                        flags=screen.get_flags()
                        if screen.get_flags() & pygame.FULLSCREEN:
                            pygame.display.set_mode([1440,870], pygame.RESIZABLE)
                        else:
                            pygame.display.set_mode([1440,870], pygame.FULLSCREEN)
                    elif event.key == pygame.K_c:
                        inMenu = False
                        done = True

            self.pause_type = pygame.font.SysFont("Calibri",80)
            self.pause_render = self.pause_type.render(self.screen_text,True,bg)
            self.options_type = pygame.font.SysFont("Calibri", 50)
            self.options_render = self.options_type.render(self.music_toggle, True, bg)
            # Draw blurred background and font on top

            screen.blit(self.blurSurf(frame,15),(0,0))
            screen.blit(self.pause_render, (450,90))
            screen.blit(self.options_render, (530, 300))
            screen.blit(self.mouse_render, (450, 400))
            screen.blit(self.fullscreen_render,(500,500))
            screen.blit(self.quitswitch_render,(590,600))
            clock.tick(60)
            pygame.display.flip()

    def intro_screen(self):
        '''
        Creates intro screen -NOT IMPLEMENTED
        '''
        try:
         intro_graphic = False
         intro = True
         while intro :
             for event.type in pygame.event_get():
                 if event.key == pygame.K_RETURN:
                     pass
                 if event.key == pygame.K_ESC:
                     pass
                 if event.key == pygame.QUIT:
                     pygame.quit()
        except:
            raise NotImplemented("Not done")


    def blurSurf(self,surface, amount):
        """
        Method used for blurring the background (Look at Source)
        -> look at source: http://www.akeric.com/blog/?p=720
        """
        #Takes screenshot of screen
        scale = 1.0/float(amount)
        surface_size = surface.get_size()
        scale_size = (int(surface_size[0]*scale), int(surface_size[1]*scale))
        #Transforms it and add blurring effect
        surface_soft1 = pygame.transform.smoothscale(surface, scale_size)
        surface_soft_final = pygame.transform.smoothscale(surface_soft1, surface_size)
        return surface_soft_final


def change_map(map_name):
    '''
    Builds new map when exit encountred, and creates new walls
    '''
    all_sprites_list.empty()
    wall_list.empty()
    exit_list.empty()
    attack_sprites_list.empty()
    #exit_doors_list.empty()
    Level(map_name)
    all_sprites_list.add(player, overlay, all_sprites_list)
    wall_list.add(wall_list)

# HARD RESET, worst way to reset.
def restart():
    #exit_doors_list,
    global lives_left, all_sprites_list,wall_list,exit_list,player_list,overlay,enemy_list,player,draw_map
    lives_left = 3
    # Create sprite group
    all_sprites_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    exit_list = pygame.sprite.Group()
    #exit_doors_list = pygame.sprite.Group()
    attack_sprites_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()
    overlay = Overlay()
    enemy_list = pygame.sprite.Group()

    player = Player(playerWidth, playerHeight)
    #enemy = Enemy(1200,600)

    #Draws level
    draw_map = Level("map1")


    # Adds player to sprites list
    all_sprites_list.add(player,overlay)
    player_list.add(player)
    wall_list.add(wall_list)
    obstacles_for_attacks = wall_list


# COLORS
bg = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (211,211,211)
white = (255,255,255)
blue = (0,0,255)
yellow = (255,255,0)
purple = (128,0,128)

width = 1440
height = 870


pygame.init()

# Screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Sparknight 2: The Sparkening")


# Create sprite group
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
exit_list = pygame.sprite.Group()
attack_sprites_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
overlay = Overlay()
enemy_list = pygame.sprite.Group()


playerWidth = 30
playerHeight = 30
#Move player Position###
#Defines borders which player should not be able to pass
playerWidthBorder = playerWidth / 2 + 5 + 30
playerHeightBorder = playerHeight / 2 + 5 + 30
player = Player(playerWidth, playerHeight)
#enemy = Enemy(1200,600)

#Draws level
draw_map = Level("map1")

# Adds player to sprites list

all_sprites_list.add(player)
player_list.add(player)
all_sprites_list.add(overlay)
wall_list.add(wall_list)


obstacles_for_attacks = wall_list




#Music file for background Music
pygame.mixer.music.load('ImagesAndSounds/MerryChristmasMr_Lawrence.mp3')
# Game time for clock functions
clock = pygame.time.Clock()

# Fill background (Makes cicle, when loop screen.fill is commented)
#screen.fill(bg)

background = pygame.image.load("ImagesAndSounds/background.jpg").convert()
background = pygame.transform.scale(background,(1440,900))
pygame.mixer.music.play(-1, 0.0)
# LOOP
if __name__ == "__main__":
    done = False
else:
    done = True
    # Set the background
    screen.blit(background,(0,0))
    # Call update function of sprites
    all_sprites_list.update()
    # Draw all sprites on screen
    all_sprites_list.draw(screen)
    # Set tick rate to 60
    clock.tick(60)
    # Redraw screen
    pygame.display.flip()

#Main game loop, handles all events, runs till user quits
while not done:
            # Quit pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = pygame.mouse.get_pressed()
            elif event.type == pygame.MOUSEBUTTONUP:
                if overlay.mouseflip:
                    if button_pressed[0]:
                        player.move()
                else:
                    if button_pressed[2]:
                        player.move()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.attack_Q()
                elif event.key == pygame.K_w:
                    player.attack_W()
                elif event.key == pygame.K_c:
                    done = True
                elif event.key == pygame.K_ESCAPE:
                    overlay.main_menu()
                elif event.key == pygame.K_m:
                    player.map_number = 5
                    change_map('map5')

        # Set the background
        screen.blit(background,(0,0))
        # Call update function of sprites
        all_sprites_list.update()
        # Draw all sprites on screen
        all_sprites_list.draw(screen)
        # Set tick rate to 60
        clock.tick(60)
        # Redraw screen
        pygame.display.flip()

# Quit if loop is exited and stop music
pygame.mixer.music.stop()
pygame.quit()
