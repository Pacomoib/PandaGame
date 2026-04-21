class Mapmanager():
    def __init__(self):
        self.model = 'block' # el modelo del cubo está en el archivo block.egg
        # se utilizan las siguientes texturas:
        self.texture = 'block.png'         
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ] #rgba
        # crea el nodo principal del mapa:
        self.startNew()
        # self.addBlock((0,10, 0))


    def startNew(self):
        """crea la base para un nuevo mapa"""
        self.land = render.attachNewNode("Land") # el nodo al cual todos los bloques de mapa están vinculados


    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]


    def addBlock(self, position):
        # crear bloques de construcción
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)


    def clear(self):
        """restablece el mapa"""
        self.land.removeNode()
        self.startNew()


    def loadLand(self, filename):
        """crea un mapa de tierra desde un archivo de texto, devuelve sus dimensiones"""
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y