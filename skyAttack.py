#Import modules
import shelve
import pygame,random,sys
from pygame.locals import *
pygame.init()

#intialising variables for ease

window_height=600 
window_width=500

blue  = (0,0,255)
black = (0,0,0)

white = (255,255,255)

fps = 25
level = 0
addnewblockrate = 30

# class road

global canvas

List1 = [window_width/2 +50,window_width/2,window_width/2 -50]

# class block1

class block1:                                       #fire balls 
    
    blockspeed = 25
      
    def __init__(self):
        self.image  = load_image('fireball.png')
        self.image = pygame.transform.scale(self.image,(40,40))
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = random.choice(List1)
        self.image_rect.top = 50
        self.imagerect = pygame.Rect(self.image_rect.centerx,self.image_rect.top, 40, 40)
        
    def update(self):
        self.image_rect.top += self.blockspeed

          
            
############# class plane
        
class plane:
    global moveright ,moveleft
    speed =30
    
    def __init__(self):
        self.image = pygame.image.load("B-24j.png")
        self.image = pygame.transform.scale(self.image, (100,100))
        self.image_rect = self.image.get_rect()
        self.image_rect.bottom = 550
        self.image_rect.centerx = window_width/2
        self.score =0 
        
    def update(self):
        
        if (moveleft and self.image_rect.left>window_width/2 - 120):
            self.image_rect.left -= self.speed
            self.score +=1
                        
        if (moveright and self.image_rect.right<window_width/2 + 120):
            self.image_rect.right += self.speed
            self.score += 1
                       
        
def terminate():        #to end the program
    pygame.quit()
    sys.exit()

def waitforkey():
    while True :                                        #to wait for user to start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     #to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_SPACE:  # to wait until press space
                    return

def drawtext(text, font, surface, x, y):        #to display text on the screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)
            
def load_image(imagename):
    return pygame.image.load(imagename)

def flamehitcar(audirect,blocklist):
    for f in blocklist:
        if audirect.colliderect(f.image_rect):
            return True
             
#main code start here
mainClock = pygame.time.Clock()

canvas = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Sky-Attack')

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

startimage = load_image("start.png")
startimage = pygame.transform.scale(startimage, (300,200))
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2
canvas.blit(startimage,startimagerect)

endimage = load_image("game-over.png")
endimage = pygame.transform.scale(endimage, (300,200))
endimagerect = endimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

drawtext('sky-fly', font, canvas,(window_width/3), (window_height/3))
pygame.display.update()

##waiting for user response
waitforkey()  

#setting background  
background = pygame.image.load("darkness.png")
background = pygame.transform.scale(background,(500,600)).convert()
# to fit according to the screen size
background_rect= background.get_rect()
background_rect.centerx = window_width/2
background_rect.centery = window_height/2

#start the main game

topscore =0

while True:  

    background_rect.centery = window_height/2
    block_list1 = []
    audi = plane()
    moveright = moveleft = False
    blockaddcounter = 0

    while True:     #the main game loop
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                
                if event.key == K_LEFT:
                    moveright = False
                    moveleft = True
                    
                if event.key == K_RIGHT:
                    moveright = True
                    moveleft = False
                    
            if event.type == KEYUP:

                if event.key == K_LEFT:
                    moveleft = False
                    
                if event.key == K_RIGHT:
                    moveright = False
                    
                if event.key == K_ESCAPE:
                    terminate()

        d = shelve.open('topscore.txt')
        topscore = d['topscore']
        
        background_rect.bottom += 10                         #to scroll the background
        if background_rect.top == window_height/2:
             background_rect.centery = window_height/2
             canvas.blit(background, background_rect)
             pygame.display.update()
            
            
        blockaddcounter += 1
        
        if blockaddcounter == addnewblockrate:
            blockaddcounter = 0
            newblock1 = block1()
            block_list1.append(newblock1)
            
        for f in block_list1:
              block1.update(f)

        audi.update()

        canvas.fill(black)
        canvas.blit(background, background_rect)
        drawtext('Score : %s | Top score : %s' %(audi.score, topscore), scorefont, canvas,150,50)
                
        for f in block_list1:
            canvas.blit(f.image,f.image_rect)
            
        if flamehitcar(audi.image_rect,block_list1):
            if topscore < audi.score:
                topscore = audi.score
                d = shelve.open('topscore.txt') # here you will save the score variable
                d['topscore'] = topscore           # thats all, now it is saved on disk.
                d.close()
            break

        canvas.blit(audi.image,audi.image_rect)    
        pygame.display.update()
        mainClock.tick(fps)
        
    canvas.blit(endimage,endimagerect)
    pygame.display.update()
    waitforkey()
