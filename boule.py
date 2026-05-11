
class Boule:
    def __init__(self, x,y,couleur,vx,vy,masse):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vx = vx
        self.vy = vy
        self.masse = masse

    def deplacer(self,dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def resistance(self,r):
        self.vx *= -r
        self.vy *= -r

    def change_couleur(self):
        if self.couleur == "blue":
            self.couleur = "red"
        elif self.couleur == "red":
            self.couleur = "blue"
        elif self.couleur == "white":
            raise ValueError('La boule blanche ne peut pas changer de couleur')
        else :
            raise ValueError('Couleur non reconnue')

    def arret(self,seuil):
        v = (self.vx**2 + self.vy**2)**0.5
        if v < seuil:
            self.vx = 0
            self.vy = 0

    def distance_interboule(self,boule2):
        d = ((self.x - boule2.x)**2 + (self.y - boule2.y)**2)*0.5
        return d


