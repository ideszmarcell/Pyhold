import pygame 
from entities .enemy import Enemy ,YELLOW 

class FastEnemy (Enemy ):
    def __init__ (self ,path ):

        super ().__init__ (path ,speed =5.0 ,hp =11 ,radius =12 ,color =YELLOW )

    def get_reward (self ):
        """Gyors ellenség jutalma: HP // 2 + 2 = 7 pénz (kiegyenlítéshez)"""
        return self .max_hp //2 +2 

    def draw_shape (self ,surface ,offset_x =0 ,offset_y =0 ):

        points =[
        (self .x +offset_x ,self .y -self .radius -5 +offset_y ),
        (self .x +self .radius +offset_x ,self .y +offset_y ),
        (self .x +offset_x ,self .y +self .radius +5 +offset_y ),
        (self .x -self .radius +offset_x ,self .y +offset_y )
        ]
        pygame .draw .polygon (surface ,self .color ,points )