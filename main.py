# atributos fantasma
class Fantasma:

    def __init__(self, estado, pos_x, pos_y, color):
        self.estado = estado
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.velocidad = {
            "rojo": 2,
            "celeste": 1,
            "rosado": 1,
            "naranja": 1,
        }[color]

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, pos_x):
        self._pos_x = pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, pos_y):
        self._pos_y = pos_y

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def velocidad(self):
        return self._velocidad

    @velocidad.setter
    def velocidad(self, velocidad):
        self._velocidad = velocidad