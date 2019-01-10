import itertools
import math
from archer import Archer, ArcherUser
class Arena:
    def __init__(self):
        self.keyDict = {}
        self.archers = []
        self.arrows = []
        
    def add_archer(self, archer):
        self.archers.append(archer)
    def get_archers(self):
        return self.archers
    def get_arrows(self):
        return self.arrows
    
    def populate_keyDict(self):
        for cchar in itertools.chain.from_iterable([list(archer.get_control_chars()) for archer in self.archers]): self.keyDict[cchar] = False

    def update(self):
        self.update_arrows()
        self.check_collisions()
        return self.update_archers()
        

    def update_archers(self):
        users = 0
        for archer in self.archers: 
            arr = None
            if isinstance(archer, ArcherUser):
                users += 1
                arr = archer.update(self.keyDict)
            else:
                arr = archer.update(self.archers)
            if arr is not None:
                self.arrows.append(arr)
            if archer.health <= 0:
                self.archers.remove(archer)
        return users
                
    def update_arrows(self):
        for arrow in self.arrows:
            act = arrow.update()
            if not act:
                self.arrows.remove(arrow)
                
    def check_collisions(self):
        for arrow in self.arrows:
            for archer in self.archers:
                if self.check_overlap(arrow, archer) and arrow.shooter is not archer:
                    archer.damage(10)
                    self.arrows.remove(arrow)

                    
    def check_overlap(self, arrow, archer):
        if self.distance(arrow.pos, archer.pos) < archer.size:
            return True
        return False
    def distance(self, pos_a, pos_b):
        delta_x = pos_a.x - pos_b.x
        delta_y = pos_a.y - pos_b.y
        return math.sqrt(delta_x *delta_x + delta_y * delta_y)
