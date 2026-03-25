from entities .tower import Tower 


class SlowTower (Tower ):
    """Lassító Torony - közepes sebzés, lassító effekt."""

    def __init__ (self ,gx :int ,gy :int )->None :
        super ().__init__ (gx ,gy )
        self .damage =10 
        self .fire_speed =800 
        self .range =3.0 
        self .name ="Lassító Torony"

        self .base_damage =self .damage 
        self .base_range =self .range 
        self .base_fire_speed =self .fire_speed 

    def _get_image_type (self )->str :
        return "slow"

    def shoot (self ,target ,now :int )->None :
        """Sebzi az ellenséget és alkalmazz lassító effektet."""
        super ().shoot (target ,now )

        target .slow_effect =40 
        target .slow_duration =2000 
        target .slow_start =now 
