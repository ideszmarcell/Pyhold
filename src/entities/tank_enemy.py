import pygame 
from entities .enemy import Enemy ,PURPLE 

class TankEnemy (Enemy ):
    def __init__ (self ,path ):

        super ().__init__ (path ,speed =1.5 ,hp =69 ,radius =20 ,color =PURPLE )

    def get_reward (self ):
        """Tank ellenség jutalma: HP // 2 + 10 = 44 pénz (erősebb HP-val)"""
        return self .max_hp //2 +10 

    def draw_shape (self ,surface ,offset_x =0 ,offset_y =0 ):

        rect =pygame .Rect (0 ,0 ,self .radius *2 ,self .radius *2 )
        rect .center =(int (self .x +offset_x ),int (self .y +offset_y ))
        pygame .draw .rect (surface ,self .color ,rect )