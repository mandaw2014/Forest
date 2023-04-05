from ursina import *

class Tree(Entity):
    def __init__(self, tent):
        super().__init__(
            model = "tree.obj",
            texture = "trees",
            scale = 5,
            position = (random.randint(-500, 500), 2, random.randint(-500, 500))
        )

        self.tent = tent

        if distance(self, tent) < 80:
            self.reset()

    def reset(self):
        self.position = (random.randint(-500, 500), 2, random.randint(-500, 500))
        if distance(self, self.tent) < 80:
            self.reset()