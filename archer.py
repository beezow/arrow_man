import math
import copy

class Archer:
    def __init__(self, speed=1, size=75, color=(150,150,150), pos=PVector(100,100), arrow_speed=10):
        self.arrow_speed = arrow_speed
        self.size = size
        self.color = color
        self.health = 100
        self.pos = pos
        self.speed = speed  #PARAM HERE
        self.angle = 0;

    def draw(self, target):
        fill(self.color[0], self.color[1], self.color[2])
        with pushMatrix():
            translate(self.pos.x, self.pos.y)
            ellipse(0, 0, self.size, self.size)
            fill(0,0,0)
            text(self.health, 0, 0)
            fill(self.color[0], self.color[1], self.color[2])
            self.draw_bow(target)
                 
    def draw_bow(self, target):
        rectMode(CENTER)
        fill(255,255,255)
        with pushMatrix():
            rotate(self.get_angle(target)+PI/4)
            with pushMatrix():
                translate(0, -self.size/2)
                rect(self.size/16,0, self.size, self.size/8)
            with pushMatrix():
                translate(self.size/2, 0)
                rect(0,0, self.size/8,self.size)
    
    def shoot(self):
        arrow = Arrow(self.pos, self.get_angle(), self, self.arrow_speed)
        return arrow
        
    def setSpeed(self, speed):
        self.speed = speed
        
    def damage(self, damage):
        self.health -= damage
    
    def check_pos(self):
        border = self.size/2
        if self.pos.x < border: self.pos.x = border
        if self.pos.y < border: self.pos.y = border
        if self.pos.x > width - border: self.pos.x = width - border 
        if self.pos.y > height - border: self.pos.y = height - border
        
    def get_angle(self, target= None):
        if target:
            delta_x = self.pos.x - target.x
            delta_y = self.pos.y - target.y
            self.angle =  math.atan2(-delta_y,-delta_x)
        return self.angle
    def get_control_chars(self):
        return []


class ArcherCPU(Archer):
    def __init__(self, path, speed=1, shoot_freq=1000, size=75, color=(120,120,120), accuracy=2, arrow_speed=5):
        Archer.__init__(self,speed=speed, size=size, color=color, pos=path[0], arrow_speed=arrow_speed)
        self.shoot_freq = shoot_freq
        self.path = path
        self.index = 0
        self.direction = 1
        self.time = 0
        self.accuracy = accuracy
        

    def update(self, archers):
        ret = None
        self.move()
        target = PVector(mouseX, mouseY)
        for archer in archers:
            if isinstance(archer, ArcherUser):
                target = copy.copy(archer.pos)
        #add some unreliabality to cpu
        target.x = target.x + random(-self.size*self.accuracy, self.size*self.accuracy)
        target.y = target.y + random(-self.size*self.accuracy, self.size*self.accuracy)
        self.draw(target)
        
        if millis() - self.time > self.shoot_freq:
            ret = self.shoot()
            self.time = millis()
        return ret

        
    def move(self):
        delta_x = self.pos.x - self.path[self.index].x 
        delta_y = self.pos.y - self.path[self.index].y
        print(self.index)
        if abs(delta_x) < 1 and abs(delta_y) < 1:
            self.index += self.direction

            if self.index >= len(self.path) or self.index < 0:
                self.direction *= -1
                self.index += self.direction 

        theta = math.atan2(delta_y, delta_x)
        delta_y = math.sin(theta) * self.speed * -1
        delta_x = math.cos(theta) * self.speed * -1
        self.pos.x += delta_x
        self.pos.y += delta_y

        
class ArcherUser(Archer):
    CHAR_UP = 0;
    CHAR_DOWN = 2;
    CHAR_RIGHT = 3;
    CHAR_LEFT = 1;
    
    def __init__(self, speed=1, shoot_freq=1000, size=75, color=(120,0,120), pos=PVector(100,100), arrow_speed=10, control_chars=("w", "a", "s", "d", " ")):
        Archer.__init__(self, speed=speed, size=size, color=color, pos=pos, arrow_speed=arrow_speed)
        self.control_chars = control_chars
        self.shoot_state_last = False
        self.shoot_state = False
        self.time = 0
        self.shoot_freq = shoot_freq
               
    def update(self, keyDict):
        ret = None
        self.move(keyDict)
        self.draw(PVector(mouseX, mouseY))
        self.shoot_state = keyDict[" "]
        if self.shoot_state and not self.shoot_state_last and millis()-self.time > self.shoot_freq:
            ret = self.shoot()
            self.time = millis()
        self.shoot_state_last = self.shoot_state
        return ret
    
    def get_control_chars(self):
        return self.control_chars
    
    def move(self, keyDict): 
        if keyDict[self.control_chars[ArcherUser.CHAR_UP]]:
            #print(self.speed)
            self.pos.y -= self.speed
        elif keyDict[self.control_chars[ArcherUser.CHAR_DOWN]]:
            self.pos.y += self.speed
        if keyDict[self.control_chars[ArcherUser.CHAR_LEFT]]:
            self.pos.x -= self.speed
        elif keyDict[self.control_chars[ArcherUser.CHAR_RIGHT]]:
            self.pos.x += self.speed
        
        self.check_pos()
        
        
        
class Arrow:

    def __init__(self, pos, theta, shooter, speed):
        self.speed = speed  #PARAMS HERE
        self.length = shooter.size*1.8
        self.pos = copy.copy(pos)
        self.theta = theta
        self.vel = PVector()
        self.vel.x = math.cos(theta) * self.speed
        self.vel.y = math.sin(theta) * self.speed
        self.shooter = shooter
    def update(self):
        self.move()
        self.draw()
        return self.on_screen()
        
    def move(self):
        #print(self.theta)
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y  
        
    def draw(self):
        with pushMatrix():
            translate(self.pos.x, self.pos.y)
            rotate(self.theta)
            fill(255,0,0)
            rect(0,0, self.length, self.length*0.1)#PARAMS HERE
            
    def on_screen(self):
        border = -self.length
        if self.pos.x < border or self.pos.y < border or self.pos.x > width - border or self.pos.y > height - border: return False
        return True
        
