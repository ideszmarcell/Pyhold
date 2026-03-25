from entities .tower import Tower 


class ArcTower (Tower ):
    """Íj Torony - nagy sebzés, lassú lövés."""

    def __init__ (self ,gx :int ,gy :int )->None :
        super ().__init__ (gx ,gy )
        self .damage =16 
        self .fire_speed =1500 
        self .range =3.0 
        self .name ="Íj Torony"

        self .base_damage =self .damage 
        self .base_range =self .range 
        self .base_fire_speed =self .fire_speed 

    def _get_image_type (self )->str :
        return "arc"
