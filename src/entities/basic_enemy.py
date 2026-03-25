from entities .enemy import Enemy ,RED 

class BasicEnemy (Enemy ):
    def __init__ (self ,path ):

        super ().__init__ (path ,speed =3 ,hp =28 ,radius =15 ,color =RED )

    def get_reward (self ):
        """Alapellenség jutalma: HP // 2 + 2 = 14 pénz (kiegyenlítéshez)"""
        return self .max_hp //2 +2 