color_code = {
    0: (242, 227, 213),
    2: (248, 246, 226),
    4: (250, 246, 241),
    8: (235, 254, 40),
    16: (244, 239, 90),
    32: (253, 228, 59),
    64: (255, 201, 12),
    128: (204, 147, 146),
    256: (171, 116, 91),
    512: (135, 35, 50),
    1024: (80, 59, 57),
    2048: (255, 215, 0)
}

class Grid():
    def __init__(self,number,pos,rect,size):
        self.number = number
        self.pos =pos
        self.rect = rect
        self.size = size
        self.BGcolor = color_code[number]

    def change_number(self,newNumber):

        self.number = newNumber
        self.BGcolor = color_code[newNumber]