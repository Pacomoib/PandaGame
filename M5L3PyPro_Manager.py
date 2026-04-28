import pickle


class Mapmanager():
    def __init__(self):
        self.model = 'block'      # archivo del cubo: block.egg
        self.texture = 'block.png'
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]
        self.startNew()

    def startNew(self):
        """Crea la base para un nuevo mapa."""
        self.land = render.attachNewNode("Land")

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        return self.colors[-1]

    def addBlock(self, position):
        """Crea un bloque en la posición indicada."""
        block = loader.loadModel(self.model)
        block.setTexture(loader.loadTexture(self.texture))
        block.setPos(position)
        block.setColor(self.getColor(int(position[2])))
        block.setTag("at", str(tuple(int(v) for v in position)))
        block.reparentTo(self.land)
        return block

    def clear(self):
        """Restablece el mapa."""
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        """Crea un mapa desde un archivo de texto y devuelve sus dimensiones."""
        self.clear()
        x = y = 0
        with open(filename) as file:
            y = 0
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                x = 0
                for z in line.split():
                    for z0 in range(int(z) + 1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(tuple(int(v) for v in pos)))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        return len(blocks) == 0

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 0
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = (x, y, z - 1)
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        """Guarda todos los bloques a un archivo binario."""
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        """Carga el mapa desde un archivo binario."""
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for _ in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
