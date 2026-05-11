class Couleur:
    def __init__(self,color_name):
        self.list_color = ["white","blue","red"]
        if color_name in list(self.list_color):
            self.couleur = color_name
        else :
            raise ValueError('couleur non reconnue')

class Boule:
    def __init__(self, x,y,couleur,rayon,vx,vy,masse):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vx = vx
        self.vy = vy
        self.masse = masse
        self.rayon = rayon

    def deplacer(self,dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def resistance(self,r):
        self.vx *= -r
        self.vy *= -r

    def change_couleur(self,new_color):
        if self.couleur == "white":
            raise ValueError('La boule blanche ne peut pas changer de couleur')
        else :
            self.couleur = new_color

    def arret(self,seuil):
        v = (self.vx**2 + self.vy**2)**0.5
        if v < seuil:
            self.vx = 0
            self.vy = 0

    def distance_interboule(self,boule2):
        d = ((self.x - boule2.x)**2 + (self.y - boule2.y)**2)*0.5
        return d

    def collision(self,boule2):
        d = self.distance_interboule(boule2)
        return d <= self.rayon + boule2.rayon






