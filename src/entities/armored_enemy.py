import pygame 
from entities .enemy import Enemy 


LIGHT_BLUE =(100 ,149 ,237 )

class ArmoredEnemy (Enemy ):
    def __init__ (self ,path ):

        super ().__init__ (path ,speed =2.0 ,hp =21 ,radius =17 ,color =LIGHT_BLUE )

    def get_reward (self ):
        """Páncélzott ellenség jutalma: HP // 2 + 2 = 11 pénz (kiegyenlítéshez)"""
        return self .max_hp //2 +2 

    def draw_shape (self ,surface ,offset_x =0 ,offset_y =0 ):

        points =[
        (self .x +offset_x ,self .y -self .radius -5 +offset_y ),
        (self .x +self .radius +5 +offset_x ,self .y +self .radius +offset_y ),
        (self .x -self .radius -5 +offset_x ,self .y +self .radius +offset_y )
        ]
        pygame .draw .polygon (surface ,self .color ,points )
