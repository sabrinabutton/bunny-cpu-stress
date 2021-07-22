import pygame
from random import seed
from random import randint
from pygame.locals import *

seed(1)
screen_width = 1500
screen_height = 750  
scale = 50
matrix_width = int(screen_width / scale)
matrix_height = int(screen_height / scale)

objects = []
plants = []
_display_surf = None
size =screen_width, screen_height

def load(path):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (scale , scale ))
    return image

pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE| pygame.DOUBLEBUF)
font = pygame.font.Font('freesansbold.ttf', 12)


bunnym_img = load('./graphics/bunnym.png')
bunnyf_img = load('./graphics/bunnyf.png')
grass_img = load('./graphics/grass.png')
plant_img = load('./graphics/plant.png')
water_img = load('./graphics/water.png')

class Game: 
    def __init__(self):
        self.matrix = []
        for i in range(matrix_height):
            line = []
            for j in range(matrix_width):
                line.append(0)
            self.matrix.append(line)    

class Genetics:
    def __init__(self, f, m):
        if f!=None and m!=None:
            self.speed = (f.genetics.speed + m.genetics.speed)/2 + randint(-1,5)
            self.hunger_thresh = (f.genetics.hunger_thresh + m.genetics.hunger_thresh)/2 + randint(-10,10)
            self.vision = (f.genetics.hunger_thresh + m.genetics.hunger_thresh)/2 + randint(-1,1)
            self.births = (f.genetics.births + m.genetics.births)/2 + randint(0,1)
        else:
            self.speed = 1
            self.hunger_thresh = -200
            self.births = 1
            self.vision = 30
        
class River:
    def __init__(self):
        self.image = water_img
        self.pos = self.image.get_rect().move(randint(0,matrix_width),randint(0,matrix_height))
        self.tiles = []
       
    def generate(self):
        for i in range(80):
            self.pos = self.pos.move(randint(-1,1), randint(-1,1) )
            self.tiles.append(self.pos)
        print(self.tiles)    
            
    def render(self):
        for tile in self.tiles:
            _display_surf.blit(self.image, (scale*tile.x, scale*tile.y))

class Turf:
    def __init__(self, x, y):
        self.image = grass_img
        self.pos = (x,y)

class Bunny:
    def __init__(self, f, m):
        self.alive = True
        self.sex = randint(0,1)
        
        self.genetics = Genetics(f,m)
        jhb
        if self.sex is 0:
            self.image = bunnyf_img
        elif self.sex is 1:
            self.image = bunnym_img

        self.pos = self.image.get_rect().move(randint(0,matrix_width),randint(0,matrix_height))

        self.hunger_sat = 0
        self.thirst_sat = 0 
        self.reproduction_sat = 0
    
    def render(self):    
        _display_surf.blit(self.image, (scale*self.pos.x, scale*self.pos.y))
    
    def on_turn(self):
        if(self.alive):
            self.hunger_sat -=10
          
            self.pick_task()
            if(self.hunger_sat <= self.genetics.hunger_thresh):
                self.die()
                
            self.render()
    
    def find_mate(self):
         #this funtion creates hellworld do not use
        queue = [((self.pos.x,self.pos.y), [])]
        visited = []
        
        for i in range(int(self.genetics.vision)):
            node, path = queue.pop(0)
            path.append(node)
            visited.append(node)  
            
            for f in objects:
                if f.sex != self.sex and node == (f.pos.x, f.pos.y):
                    return path
        
            if (node[0] + 1,node[1]) not in visited:
                queue.append(((node[0]+ 1,node[1]), path[:]))

            if (node[0] - 1,node[1]) not in visited:
                queue.append(((node[0]- 1,node[1]), path[:]))

            if (node[0],node[1] +1) not in visited:
                queue.append(((node[0],node[1] +1), path[:]))

            if (node[0],node[1]-1) not in visited:
                queue.append(((node[0],node[1]-1), path[:]))

        return False    
    
    def find_food(self):
        #this funtion creates hellworld do not use
        queue = [((self.pos.x,self.pos.y), [])]
        visited = []
        
        for i in range(int(self.genetics.vision)):
            node, path = queue.pop(0)
            path.append(node)

            visited.append(node)  
            
            for f in plants:
                if node == f.pos:
                    return path
        
            if (node[0] + 1,node[1]) not in visited:
                queue.append(((node[0]+ 1,node[1]), path[:]))

            if (node[0] - 1,node[1]) not in visited:
                queue.append(((node[0]- 1,node[1]), path[:]))

            if (node[0],node[1] +1) not in visited:
                queue.append(((node[0],node[1] +1), path[:]))

            if (node[0],node[1]-1) not in visited:
                queue.append(((node[0],node[1]-1), path[:]))

        return False          

            
    def pick_task(self): 
        if (self.hunger_sat < 100):
            food_path = self.find_food()
            if(food_path):
                if(len(food_path) >1):
                    self.pos = self.image.get_rect().move(food_path[1])
            else:
                self.move()    
            for f in plants:
                if f.pos == (self.pos.x,self.pos.y):
                    self.eat(f)                
           
        else:
            mate_path = self.find_mate()
            if(mate_path):
                if(len(mate_path) >1):
                    self.pos = self.image.get_rect().move(mate_path[1])
            else:
                self.move()
            for f in objects:
                if f.sex!= self.sex and ((f.pos.x, f.pos.y) == (self.pos.x,self.pos.y)):
                #have female bunny call reproduce
                    if(self.sex == 0):
                        newBunny(self, f)
    
    def drink(self):
        pass
    
    def eat(self, plant):
        self.hunger_sat += plant.calories
        plant.alive = False
    
    def die(self):    
        self.alive = False
    
    def move(self):
        x = int(self.genetics.speed)
        self.pos = self.pos.move(randint(-x,x), randint(-x,x) )
        if self.pos.x >= matrix_width:
                self.pos.x = matrix_width-1
        if self.pos.x <= 0:
                self.pos.x =1
        if self.pos.y >= matrix_height:
                self.pos.y = matrix_height-1
        if self.pos.y <= 0:
                self.pos.y = 1

class Plant: 
    def __init__(self):
        self.alive = True
        self.image = plant_img
        self.calories = 500
        self.pos = (randint(0,matrix_width),randint(0,matrix_height))
    def render(self):
        _display_surf.blit(self.image, (scale*self.pos[0], scale*self.pos[1]))
    
    def on_turn(self):
        if(self.alive):
            self.render()

def newBunny(f, m): 
    for i in range(int(f.genetics.births)):
        o = Bunny(f,m)
        objects.append(o)   
               
game = Game()                




for x in range(2):
    p = Plant()
    #game.matrix[p.pos[0]][p.pos[1]] = "p"
    #game.matrix[tile.pos.x][tile.pos.y] = "w"

for x in range(15):                    #create 10 objects</i>s
     o = Bunny(None,None)
     
     objects.append(o)
     
river = River()   
river.generate()
  
while(1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
    if(randint(0,10) > 7):
        p = Plant()
        plants.append(p)
            
    for x in range(matrix_width):
        for y in range(matrix_height):
            _display_surf.blit(grass_img, (x*scale,y*scale) )
           
    for i,p in enumerate(plants):
        p.on_turn()  
        if(p.alive==False):
            plants.remove(p)
                     
    for i,p in enumerate(objects):
        p.on_turn()
        if(p.alive==False):
            objects.remove(p) 
            
    river.render()        
    
    text = font.render('BunnySim, Sabrina Button 2021', True, (255, 255, 255), (0, 0, 0))

    _text_surf = text
    _text_surf.set_alpha(127)
    
    _display_surf.blit(_text_surf, (0,0))
    
    text = font.render('Bunnies: ' + str(len(objects)), True, (255, 255, 255), (0, 0, 0))

    _text_surf = text
    _text_surf.set_alpha(127)
    
    _display_surf.blit(_text_surf, (0,12))
    
    text = font.render((str(int(pygame.time.get_ticks() / 1000)) + " seconds"), True, (255, 255, 255), (0, 0, 0))

    _text_surf = text
    _text_surf.set_alpha(127)
    
    _display_surf.blit(_text_surf, (0,24))
         
    pygame.display.update()
    pygame.time.delay(500)
        

