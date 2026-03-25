import math 
import pygame 
from entities .enemy import Enemy 
from entities .tower import Tower 


class BossEnemy (Enemy ):
    """Nagyobb, erősebb ellenség, aki a tornyokat is megtámadja."""

    def __init__ (self ,path :list [tuple [int ,int ]],wave :int =1 ):

        hp =396 +wave *30 
        speed =0.8 
        radius =22 
        color =(150 ,0 ,150 )

        super ().__init__ (path ,speed ,hp ,radius ,color )

        self .wave =wave 
        self .attack_range =60 
        self .attack_damage =25 +wave *5 
        self .attack_cooldown =1200 
        self .last_attack =0 

    def update (self ,towers :list [Tower ]|None =None ):

        super ().update ()


        if towers :
            self ._attack_nearest_tower (towers )

    def get_reward (self ):
        """Boss jutalma: HP alapú + wave szorzó"""


        return self .max_hp //3 +2 +(self .wave *10 )

    def _attack_nearest_tower (self ,towers :list [Tower ])->None :
        now =pygame .time .get_ticks ()
        if now -self .last_attack <self .attack_cooldown :
            return 

        closest_tower =None 
        closest_dist =float ("inf")

        for tower in towers :
            tx ,ty =tower ._get_pixel_center ()
            dist =math .hypot (self .x -tx ,self .y -ty )
            if dist <closest_dist :
                closest_dist =dist 
                closest_tower =tower 

        if closest_tower and closest_dist <=self .attack_range :
            destroyed =closest_tower .take_damage (self .attack_damage )
            self .last_attack =now 
            if destroyed :
                print ("Boss elpusztította a tornyot!")

    def draw_shape (self ,surface ,offset_x =0 ,offset_y =0 ):

        pygame .draw .circle (surface ,self .color ,(int (self .x +offset_x ),int (self .y +offset_y )),self .radius )
        pygame .draw .circle (surface ,(255 ,255 ,0 ),(int (self .x +offset_x ),int (self .y +offset_y )),self .radius ,3 )
