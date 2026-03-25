import pygame 
import math 
from core .settings import GRID_SIZE ,ORANGE ,WHITE 


class Tower :
    """Alapozó Tower osztály - az összes tower ebből származik."""

    _images_cache :dict [str ,pygame .Surface ]={}

    TOWER_IMAGES ={
    "arc":"assets/images/arc_tower.png",
    "shock":"assets/images/shock_tower.png",
    "slow":"assets/images/slow_tower.png",
    }

    @classmethod 
    def load_images (cls )->None :
        """Előbetölti az összes tower képet."""
        for name ,path in cls .TOWER_IMAGES .items ():
            try :
                img =pygame .image .load (path )
                img =pygame .transform .scale (img ,(GRID_SIZE -8 ,GRID_SIZE -8 ))
                cls ._images_cache [name ]=img 
            except Exception as e :
                print (f"Hiba a {path } betöltésekor: {e }")

    def __init__ (self ,gx :int ,gy :int )->None :
        """Alapozó konstruktor - felülírható leszármazottakban."""
        self .gx :int =gx 
        self .gy :int =gy 
        self .image_type :str =self ._get_image_type ()


        self .size :int =2 


        self .max_hp :int =150 
        self .hp :int =self .max_hp 


        self .range :float =3.0 
        self .damage :int =10 
        self .fire_speed :int =1000 
        self .name :str ="Torony"

        self .last_shot :int =0 


        self .level :int =1 
        self .max_level :int =5 
        self .base_damage :int =self .damage 
        self .base_range :float =self .range 
        self .base_fire_speed :int =self .fire_speed 

    def _get_image_type (self )->str :
        """Visszaadja a tower típusát - felülírható leszármazottakban."""
        return "arc"

    def _get_pixel_center (self )->tuple [int ,int ]:
        """Kiszámolja a tower közepének pixel koordinátáit."""

        px =self .gx *GRID_SIZE +(self .size *GRID_SIZE )//2 
        py =self .gy *GRID_SIZE +(self .size *GRID_SIZE )//2 
        return px ,py 

    def find_target (self ,enemies :list )->None :
        """Megkeresi a legközelebbi ellenséget a hatótávon belül."""
        now =pygame .time .get_ticks ()
        if now -self .last_shot <self .fire_speed :
            return 

        tower_center =self ._get_pixel_center ()

        for enemy in enemies :

            dx =enemy .x -tower_center [0 ]
            dy =enemy .y -tower_center [1 ]
            distance =math .sqrt (dx **2 +dy **2 )

            if distance <=self .range *GRID_SIZE :
                self .shoot (enemy ,now )
                break 

    def shoot (self ,target ,now :int )->None :
        """Sebzi az ellenséget. Felülírható leszármazottakban."""
        target .hp -=self .damage 
        self .last_shot =now 
        print (f"{self .name } ({self .gx }, {self .gy }) eltalálta az ellenséget! Sebzés: {self .damage }")

    def take_damage (self ,damage :int )->bool :
        """Sebzi a tornyot. Visszatér True-val, ha a tower megsemmisült."""
        self .hp -=damage 
        if self .hp <0 :
            self .hp =0 

        print (f"{self .name } ({self .gx }, {self .gy }) sérült: -{damage } HP, hátralévő: {self .hp }")
        return self .hp ==0 

    def _draw_fallback_tower (self ,surface :pygame .Surface ,px :int ,py :int ,img_width :int ,img_height :int ,offset_x :int ,offset_y :int )->None :
        """Fallback rajzolás, ha a kép nincs betöltve."""
        rect =(px ,py ,img_width ,img_height )
        pygame .draw .rect (surface ,ORANGE ,rect ,border_radius =6 )

        center_x =self .gx *GRID_SIZE +(self .size *GRID_SIZE )//2 +offset_x 
        center_y =self .gy *GRID_SIZE +(self .size *GRID_SIZE )//2 +offset_y 
        pygame .draw .circle (surface ,WHITE ,(center_x ,center_y ),GRID_SIZE //5 )

    def _draw_hp_bar (self ,surface :pygame .Surface ,px :int ,py :int ,img_width :int ,img_height :int )->None :
        """Rajzol egy HP sávot a tower felett."""
        bar_width =img_width 
        bar_height =5 
        hp_ratio =self .hp /self .max_hp if self .max_hp >0 else 0 
        bar_x =px 
        bar_y =py -bar_height -2 

        pygame .draw .rect (surface ,(255 ,0 ,0 ),(bar_x ,bar_y ,bar_width ,bar_height ))
        pygame .draw .rect (surface ,(0 ,255 ,0 ),(bar_x ,bar_y ,bar_width *hp_ratio ,bar_height ))

    def draw (self ,surface :pygame .Surface ,offset_x :int =0 ,offset_y :int =0 )->None :
        """Kirajzolja a tower képét és a HP-sávot."""
        px =self .gx *GRID_SIZE +4 +offset_x 
        py =self .gy *GRID_SIZE +4 +offset_y 

        img_width =self .size *GRID_SIZE -8 
        img_height =self .size *GRID_SIZE -8 

        if self .image_type in self ._images_cache :
            img =self ._images_cache [self .image_type ]
            img =pygame .transform .scale (img ,(img_width ,img_height ))
            surface .blit (img ,(px ,py ))
        else :
            self ._draw_fallback_tower (surface ,px ,py ,img_width ,img_height ,offset_x ,offset_y )


        self ._draw_hp_bar (surface ,px ,py ,img_width ,img_height )

    def upgrade (self )->bool :
        """Fejleszti a tornyot: növeli a sebzést, hatótávot és lövési sebességet. Max 5 szint."""
        if self .level >=self .max_level :
            return False 

        self .level +=1 

        self .damage =int (self .base_damage *(1 +0.2 *(self .level -1 )))

        self .range =self .base_range *(1 +0.15 *(self .level -1 ))

        self .fire_speed =int (self .base_fire_speed *(1 -0.1 *(self .level -1 )))
        print (f"{self .name } ({self .gx }, {self .gy }) fejlesztve: Level {self .level }/{self .max_level }")
        print (f"  Sebzés: {self .damage }, Hatótáv: {self .range :.1f}, Lövési sebesség: {self .fire_speed }ms")
        return True 

    def get_upgrade_cost (self )->int :
        """Visszaadja a következő fejlesztés költségét."""
        if self .level >=self .max_level :
            return 0 


        return 25 *self .level 
