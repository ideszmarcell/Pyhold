import pygame 
from core .settings import (
BLUE ,
GRID_SIZE ,
BLACK ,
DARK_GRAY ,
GREEN ,
WHITE ,
MAZE ,
SCREEN_WIDTH ,
SCREEN_HEIGHT ,
)
from entities .tower import Tower 
from entities .arc_tower import ArcTower 
from entities .shock_tower import ShockTower 
from entities .slow_tower import SlowTower 




class Map :
    _base_cover_img :pygame .Surface |None =None 
    _path_img :pygame .Surface |None =None 
    _wall_img :pygame .Surface |None =None 
    _tower_base_img :pygame .Surface |None =None 

    def __init__ (self )->None :
        self .cols :int =len (MAZE [0 ])
        self .rows :int =len (MAZE )
        self .data :list [list [int ]]=[row [:]for row in MAZE ]
        self .tower_images :dict [tuple [int ,int ],str ]={}
        self .towers :list [Tower ]=[]
        self .map_width =self .cols *GRID_SIZE 
        self .map_height =self .rows *GRID_SIZE 
        self .offset_x =(SCREEN_WIDTH -self .map_width )//2 
        self .offset_y =(SCREEN_HEIGHT -self .map_height )//2 
        if Map ._base_cover_img is None :
            try :
                img =pygame .image .load ("assets/images/base_cover.png").convert_alpha ()
                Map ._base_cover_img =pygame .transform .scale (
                img ,(GRID_SIZE ,GRID_SIZE )
                )
            except Exception as e :
                print (f"Hiba a base_cover.png betöltésekor: {e }")

        self .base_cover_img =Map ._base_cover_img 

        if Map ._tower_base_img is None :
            try :
                img =pygame .image .load ("assets/images/tower_base.png").convert_alpha ()
                Map ._tower_base_img =pygame .transform .scale (
                img ,(GRID_SIZE ,GRID_SIZE )
                )
            except Exception as e :
                print (f"Hiba a tower_base.png betöltésekor: {e }")

        self .tower_base_img =Map ._tower_base_img 

        if Map ._path_img is None :
            try :
                img =pygame .image .load ("assets/images/path.jpg").convert ()
                Map ._path_img =pygame .transform .scale (img ,(GRID_SIZE ,GRID_SIZE ))
            except Exception as e :
                print (f"Hiba a path.jpg betöltésekor: {e }")

        self .path_img =Map ._path_img 

        if Map ._wall_img is None :
            try :
                img =pygame .image .load ("assets/images/wall.jpg").convert ()
                img =pygame .transform .flip (img ,False ,True )
                Map ._wall_img =pygame .transform .scale (img ,(GRID_SIZE ,GRID_SIZE ))
            except Exception as e :
                print (f"Hiba a wall.jpg betöltésekor: {e }")

        self .wall_img =Map ._wall_img 

    def calculate_coords (self ,pos :tuple [int ,int ])->tuple [int ,int ]:
        x ,y =pos 
        x -=self .offset_x 
        y -=self .offset_y 
        return x //GRID_SIZE ,y //GRID_SIZE 

    def _get_tower_block_top_left (self ,r :int ,c :int )->tuple [int ,int ]|None :
        """
        Megtalálja a 2x2 tower blokk bal felső sarkát.
        Ha a cella tower (2), visszatér a blokk bal felső koordinátájával, egyébként None-t ad vissza.
        """
        if (
        not (0 <=r <self .rows and 0 <=c <self .cols )
        or self .data [r ][c ]!=2 
        ):
            return None 

        top_r ,top_c =r ,c 

        if r >0 and c >0 and self .data [r -1 ][c -1 ]==2 :
            top_r ,top_c =r -1 ,c -1 
        elif r >0 and c +1 <self .cols and self .data [r -1 ][c ]==2 :
            top_r ,top_c =r -1 ,c 
        elif c >0 and r +1 <self .rows and self .data [r ][c -1 ]==2 :
            top_r ,top_c =r ,c -1 

        return (top_r ,top_c )

    def get_tower_image (self ,r :int ,c :int )->str |None :
        """Visszaadja a tower képét egy adott cellához. Ha nincs kiválasztva, None-t ad vissza."""
        tower_block =self ._get_tower_block_top_left (r ,c )
        if tower_block is None :
            return None 
        return self .tower_images .get (tower_block ,None )

    def set_tower_image (self ,r :int ,c :int ,image_type :str )->bool :
        """Beállítja a tower képét egy adott cellához és létrehozza az objektumot."""
        tower_block =self ._get_tower_block_top_left (r ,c )
        if tower_block is None :
            return False 


        self .tower_images [tower_block ]=image_type 



        tower =None 
        for t in self .towers :
            if t .gx ==tower_block [1 ]and t .gy ==tower_block [0 ]:
                tower =t 
                break 


        if tower is None :

            if image_type =="arc":
                tower =ArcTower (tower_block [1 ],tower_block [0 ])
            elif image_type =="shock":
                tower =ShockTower (tower_block [1 ],tower_block [0 ])
            elif image_type =="slow":
                tower =SlowTower (tower_block [1 ],tower_block [0 ])
            else :
                tower =ArcTower (tower_block [1 ],tower_block [0 ])

            self .towers .append (tower )
        else :

            self .towers .remove (tower )
            if image_type =="arc":
                tower =ArcTower (tower_block [1 ],tower_block [0 ])
            elif image_type =="shock":
                tower =ShockTower (tower_block [1 ],tower_block [0 ])
            elif image_type =="slow":
                tower =SlowTower (tower_block [1 ],tower_block [0 ])
            else :
                tower =ArcTower (tower_block [1 ],tower_block [0 ])

            self .towers .append (tower )

        return True 

    def remove_tower (self ,tower :Tower )->None :
        """Eltávolítja a tornyot a pályáról (map + tower lista + képállapot)."""
        for dr in range (tower .size ):
            for dc in range (tower .size ):
                r =tower .gy +dr 
                c =tower .gx +dc 
                if (
                0 <=r <self .rows 
                and 0 <=c <self .cols 
                ):
                    self .data [r ][c ]=2 

        if tower in self .towers :
            self .towers .remove (tower )

        self .tower_images .pop ((tower .gy ,tower .gx ),None )

    def modify_cell (self ,pos :tuple [int ,int ])->None :
        gx ,gy =self .calculate_coords (pos )
        if 0 <=gy <self .rows and 0 <=gx <self .cols :
            self .data [gy ][gx ]=1 if self .data [gy ][gx ]==0 else 0 

    def affect_tower_block (self ,pos :tuple [int ,int ])->bool :
        """Hatást gyakorol az összekapcsolt toronyblokkra.

        Ha van olyan tower objektum a listában, amelynek bal felső koordinátája
        egyezik a blokkéval, azt is eltávolítjuk.
        """
        gx ,gy =self .calculate_coords (pos )

        if (
        not (0 <=gy <self .rows and 0 <=gx <self .cols )
        or self .data [gy ][gx ]!=2 
        ):
            return False 

        top_r ,top_c =gy ,gx 
        if gy >0 and gx >0 and self .data [gy -1 ][gx -1 ]==2 :
            top_r ,top_c =gy -1 ,gx -1 
        elif gy >0 and gx +1 <self .cols and self .data [gy -1 ][gx ]==2 :
            top_r ,top_c =gy -1 ,gx 
        elif gx >0 and gy +1 <self .rows and self .data [gy ][gx -1 ]==2 :
            top_r ,top_c =gy ,gx -1 

        for tower in list (self .towers ):
            if tower .gx ==top_c and tower .gy ==top_r :
                self .remove_tower (tower )
                return True 

        for dr in range (2 ):
            for dc in range (2 ):
                nr ,nc =top_r +dr ,top_c +dc 
                if (
                0 <=nr <self .rows 
                and 0 <=nc <self .cols 
                and self .data [nr ][nc ]==2 
                ):
                    self .data [nr ][nc ]=0 

        return True 

    def _draw_lines (self ,surface :pygame .Surface )->None :
        for x in range (0 ,self .cols *GRID_SIZE +1 ,GRID_SIZE ):
            pygame .draw .line (
            surface ,
            DARK_GRAY ,
            (x +self .offset_x ,self .offset_y ),
            (x +self .offset_x ,self .rows *GRID_SIZE +self .offset_y ),
            )
        for y in range (0 ,self .rows *GRID_SIZE +1 ,GRID_SIZE ):
            pygame .draw .line (
            surface ,
            DARK_GRAY ,
            (self .offset_x ,y +self .offset_y ),
            (self .cols *GRID_SIZE +self .offset_x ,y +self .offset_y ),
            )

    def _draw_buildings (self ,surface :pygame .Surface )->None :
        drawn_towers :set [tuple [int ,int ]]=set ()

        for r in range (self .rows ):
            for c in range (self .cols ):
                if (r ,c )in drawn_towers :
                    continue 

                color =None 
                width =GRID_SIZE 
                height =GRID_SIZE 

                if self .data [r ][c ]==1 :
                    color =BLACK 
                elif self .data [r ][c ]==2 :
                    if (
                    r +1 <self .rows 
                    and c +1 <self .cols 
                    and self .data [r ][c +1 ]==2 
                    and self .data [r +1 ][c ]==2 
                    and self .data [r +1 ][c +1 ]==2 
                    ):
                        width =GRID_SIZE *2 
                        height =GRID_SIZE *2 
                        drawn_towers .add ((r ,c ))
                        drawn_towers .add ((r ,c +1 ))
                        drawn_towers .add ((r +1 ,c ))
                        drawn_towers .add ((r +1 ,c +1 ))

                        self ._draw_tower_with_image (surface ,c ,r ,width ,height )
                        continue 
                    else :
                        if self .tower_base_img is not None :
                            surface .blit (
                            self .tower_base_img ,
                            (
                            c *GRID_SIZE +self .offset_x ,
                            r *GRID_SIZE +self .offset_y ,
                            ),
                            )
                        continue 
                elif self .data [r ][c ]==3 :
                    color =BLUE 
                elif self .data [r ][c ]==6 :
                    color =WHITE 
                elif self .data [r ][c ]==5 :
                    color =(255 ,50 ,50 )
                elif self .data [r ][c ]==0 :
                    color =DARK_GRAY 
                else :
                    color =(255 ,0 ,255 )

                if color :
                    rect =pygame .Rect (
                    c *GRID_SIZE +self .offset_x ,
                    r *GRID_SIZE +self .offset_y ,
                    width ,
                    height ,
                    )
                    pygame .draw .rect (surface ,color ,rect )

                    rect =(
                    c *GRID_SIZE +1 +self .offset_x ,
                    r *GRID_SIZE +1 +self .offset_y ,
                    width -2 ,
                    height -2 ,
                    )
                    pygame .draw .rect (surface ,color ,rect )

                    if self .data [r ][c ]==5 and self .base_cover_img is not None :
                        surface .blit (
                        self .base_cover_img ,
                        (
                        c *GRID_SIZE +self .offset_x ,
                        r *GRID_SIZE +self .offset_y ,
                        ),
                        )

                    if self .data [r ][c ]==0 and self .path_img is not None :
                        surface .blit (
                        self .path_img ,
                        (
                        c *GRID_SIZE +self .offset_x ,
                        r *GRID_SIZE +self .offset_y ,
                        ),
                        )

                    if self .data [r ][c ]==3 and self .wall_img is not None :
                        surface .blit (
                        self .wall_img ,
                        (
                        c *GRID_SIZE +self .offset_x ,
                        r *GRID_SIZE +self .offset_y ,
                        ),
                        )

    def _draw_tower_with_image (
    self ,surface :pygame .Surface ,c :int ,r :int ,width :int ,height :int 
    )->None :

        if self .tower_base_img is not None :

            tower_base_scaled =pygame .transform .scale (self .tower_base_img ,(width ,height ))
            surface .blit (
            tower_base_scaled ,
            (
            c *GRID_SIZE +self .offset_x ,
            r *GRID_SIZE +self .offset_y ,
            ),
            )


        image_type =self .get_tower_image (r ,c )


        if image_type is not None and image_type in Tower ._images_cache :
            try :

                img =Tower ._images_cache [image_type ]
                scaled_img =pygame .transform .scale (img ,(width -8 ,height -8 ))
                surface .blit (
                scaled_img ,
                (
                c *GRID_SIZE +4 +self .offset_x ,
                r *GRID_SIZE +4 +self .offset_y ,
                ),
                )
            except Exception as e :
                print (f"Hiba a tower képének rajzolásánál: {e }")

    def _draw_tower_default (
    self ,surface :pygame .Surface ,c :int ,r :int ,width :int ,height :int 
    )->None :

        if self .tower_base_img is not None :
            tower_base_scaled =pygame .transform .scale (self .tower_base_img ,(width ,height ))
            surface .blit (
            tower_base_scaled ,
            (
            c *GRID_SIZE +self .offset_x ,
            r *GRID_SIZE +self .offset_y ,
            ),
            )
        else :
            rect =pygame .Rect (
            c *GRID_SIZE +self .offset_x ,
            r *GRID_SIZE +self .offset_y ,
            width ,
            height ,
            )
            pygame .draw .rect (surface ,GREEN ,rect )

            rect_inner =(
            c *GRID_SIZE +1 +self .offset_x ,
            r *GRID_SIZE +1 +self .offset_y ,
            width -2 ,
            height -2 ,
            )
            pygame .draw .rect (surface ,GREEN ,rect_inner )

    def draw (self ,surface :pygame .Surface )->None :
        surface .fill (BLACK )
        self ._draw_buildings (surface )

    def extract_path (self )->list [tuple [int ,int ]]:
        """Kikeresi a pixel-alapú útvonalat a 6-ostól az 5-ösig, figyelve a kereszteződésekre."""
        start :tuple [int ,int ]|None =None 
        end :tuple [int ,int ]|None =None 

        for r in range (self .rows ):
            for c in range (self .cols ):
                if self .data [r ][c ]==6 :
                    start =(r ,c )
                elif self .data [r ][c ]==5 :
                    end =(r ,c )

        if not start or not end :
            return []

        path_coords :list [tuple [int ,int ]]=[start ]
        current :tuple [int ,int ]=start 
        directions :list [tuple [int ,int ]]=[
        (-1 ,0 ),
        (1 ,0 ),
        (0 ,-1 ),
        (0 ,1 ),
        ]
        current_direction =None 

        for dr ,dc in directions :
            nr ,nc =start [0 ]+dr ,start [1 ]+dc 
            if 0 <=nr <self .rows and 0 <=nc <self .cols :
                if self .data [nr ][nc ]in [0 ,5 ]:
                    current_direction =(dr ,dc )
                    break 

        if not current_direction :
            return []

        safety_lock =0 
        while current !=end and safety_lock <1000 :
            safety_lock +=1 
            dr ,dc =current_direction 
            next_r ,next_c =current [0 ]+dr ,current [1 ]+dc 

            if (
            0 <=next_r <self .rows 
            and 0 <=next_c <self .cols 
            and self .data [next_r ][next_c ]in [0 ,5 ]
            ):
                current =(next_r ,next_c )
                path_coords .append (current )
            else :
                found =False 
                for new_dr ,new_dc in directions :
                    if new_dr ==-dr and new_dc ==-dc :
                        continue 

                    nr ,nc =current [0 ]+new_dr ,current [1 ]+new_dc 
                    if 0 <=nr <self .rows and 0 <=nc <self .cols :
                        if self .data [nr ][nc ]in [0 ,5 ]:
                            current_direction =(new_dr ,new_dc )
                            current =(nr ,nc )
                            path_coords .append (current )
                            found =True 
                            break 

                if not found :
                    break 

        pixel_path :list [tuple [int ,int ]]=[]
        for r ,c in path_coords :
            px =c *GRID_SIZE +(GRID_SIZE //2 )
            py =r *GRID_SIZE +(GRID_SIZE //2 )
            pixel_path .append ((px ,py ))

        return pixel_path 
