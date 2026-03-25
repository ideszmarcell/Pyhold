
import pygame 
from core .settings import BLACK ,WHITE ,GREEN ,ORANGE ,MINER_COST ,TOWER_COST 

class Economy :
    def __init__ (self )->None :
        self .crystal :int =200 

        self .font :pygame .font .Font =pygame .font .SysFont ("Arial",24 ,bold =True )

    def purchase (self ,cost :int )->bool :
        """Levonja a pénzt, ha van elég. Visszatér True/False értékkel."""
        if self .crystal >=cost :
            self .crystal -=cost 
            return True 
        return False 

    def draw_ui (self ,surface :pygame .Surface ,current_building :int )->None :
        """Draw money and currently selected building."""

        building_name =f"Miner ({MINER_COST })"if current_building ==1 else f"Tower ({TOWER_COST })"
        building_color =GREEN if current_building ==1 else ORANGE 

        money_text =self .font .render (f"Crystal: {self .crystal }",True ,WHITE )
        building_text =self .font .render (f"Build [TAB]: {building_name }",True ,building_color )


        pygame .draw .rect (surface ,BLACK ,(5 ,5 ,250 ,70 ))
        surface .blit (money_text ,(10 ,10 ))
        surface .blit (building_text ,(10 ,40 ))