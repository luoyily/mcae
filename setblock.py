class Command:
    def __init__(self, tick, x, y, z, block, mode='replace'):
        self.tick = tick
        self.x = x
        self.y = y
        self.z = z
        self.block = block
        self.mode = mode

    def __str__(self):
        text = 'setblock %s %s %s %s %s' % (self.x, self.y, self.z, self.block, self.mode)
        return text
