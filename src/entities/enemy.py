import math 
import pygame 

RED =(255 ,0 ,0 )
GREEN =(0 ,255 ,0 )
PURPLE =(128 ,0 ,128 )
YELLOW =(255 ,255 ,0 )

class Enemy :
    """Ez az általános ellenség osztály, minden ellenség ebből fog származni"""
    def __init__ (self ,path ,speed ,hp ,radius ,color ):
        self .path =path 
        self .path_index =0 
        self .x ,self .y =self .path [0 ]

        self .speed =speed 
        self .base_speed =speed 
        self .max_hp =int (hp *1.5 )
        self .hp =int (hp *1.5 )
        self .radius =radius 
        self .color =color 

        self .reached_end =False 
        self .reward_given =False 


        self .slow_effect =0 
        self .slow_duration =0 
        self .slow_start =0 

    def update (self ):

        current_time =pygame .time .get_ticks ()
        if self .slow_start >0 and current_time -self .slow_start <self .slow_duration :

            current_speed =self .base_speed *(1 -self .slow_effect /100 )
        else :

            current_speed =self .base_speed 
            self .slow_effect =0 

        if self .path_index <len (self .path )-1 :
            target_x ,target_y =self .path [self .path_index +1 ]
            dx =target_x -self .x 
            dy =target_y -self .y 
            distance =math .hypot (dx ,dy )

            if distance <current_speed :
                self .path_index +=1 
                self .x ,self .y =target_x ,target_y 
            else :
                self .x +=(dx /distance )*current_speed 
                self .y +=(dy /distance )*current_speed 
        else :
            self .reached_end =True 

    def draw_shape (self ,surface ,offset_x =0 ,offset_y =0 ):
        """Alapértelmezett alakzat: egy kör. Ezt fogják felülírni a speciális ellenségek."""
        pygame .draw .circle (surface ,self .color ,(int (self .x +offset_x ),int (self .y +offset_y )),self .radius )

    def draw (self ,surface ,offset_x =0 ,offset_y =0 ):
        self .draw_shape (surface ,offset_x ,offset_y )

        hp_bar_width =30 
        hp_bar_height =5 
        hp_ratio =self .hp /self .max_hp 

        pygame .draw .rect (surface ,RED ,(self .x -hp_bar_width /2 +offset_x ,self .y -self .radius -12 +offset_y ,hp_bar_width ,hp_bar_height ))
        if self .hp >0 :
            pygame .draw .rect (surface ,GREEN ,(self .x -hp_bar_width /2 +offset_x ,self .y -self .radius -12 +offset_y ,hp_bar_width *hp_ratio ,hp_bar_height ))

    def get_reward (self ):
        """Alapértelmezett jutalmazási érték (HP alapján)"""
        return max (1 ,self .max_hp //5 )