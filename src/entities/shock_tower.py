from entities .tower import Tower 


class ShockTower (Tower ):
    """Sokk Torony - kis sebzés, gyors lövés."""

    def __init__ (self ,gx :int ,gy :int )->None :
        super ().__init__ (gx ,gy )
        self .damage =5 
        self .fire_speed =500 
        self .range =2.5 
        self .name ="Sokk Torony"

        self .base_damage =self .damage 
        self .base_range =self .range 
        self .base_fire_speed =self .fire_speed 

    def _get_image_type (self )->str :
        return "shock"
