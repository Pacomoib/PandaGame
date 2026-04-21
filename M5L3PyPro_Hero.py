key_switch_camera = 'c' # la cámara está ligada al héroe o no
key_switch_mode = 'z' # puede atravesar obstáculos o no


key_forward = 'w' # avanzar (la dirección a la que apunta la cámara)
key_back = 's' # retroceder
key_left = 'a' # caminar a la izquierda (de lado a la cámara)
key_right = 'd' # caminar a la derecha
key_up = 'e' # subir
key_down = 'q' # bajar


key_turn_left = 'n' # girar la cámara a la derecha (y el mundo a la izquierda)
key_turn_right = 'm' # girar la cámara a la izquierda (y el mundo a la derecha)


class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True # modo para atravesar todo
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()


    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True


    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False




    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()


    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)


    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)


    def look_at(self, angle):
        '''devuelve las coordenadas a las que se desplaza el héroe en el punto (x, y)
        si caminan hacia un ángulo '''
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from


    def just_move(self, angle):
        '''se mueve a las coordenadas deseadas en cualquier caso'''
        pos = self.look_at(angle)
        self.hero.setPos(pos)


    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
  
    def check_dir(self,angle):
        '''devuelve cambios redondeados en las coordenadas X, Y
        correspondientes al movimiento hacia el ángulo.
        La coordenada Y disminuye si el héroe está mirando a un ángulo de 0 grados,
        y aumenta cuando está mirando a un ángulo de 180 grados.   
        La coordenada X aumenta si el héroe está mirando a un ángulo de 90 grados,
        y disminuye cuando está mirando a un ángulo de 270 grados.   
            ángulo de 0 grados (de 0 a 20)      ->        Y - 1
            ángulo de 45 grados (de 25 a 65)    -> X + 1, Y - 1
            ángulo de 90 grados (de 70 a 110) -> X + 1
            de 115 a 155 -> X + 1, Y + 1
            de 160 a 200 -> Y + 1
            205 a 245 -> X - 1, Y + 1
            de 250 a 290 -> X - 1
            de 290 a 335 -> X - 1, Y - 1
            de 340 -> Y - 1 '''
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)


    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)


    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)


    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)


    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)


        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)


        base.accept(key_switch_camera, self.changeView)
