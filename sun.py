from panda3d.core import DirectionalLight
from ursina import Entity

class SunLight(Entity):
    def __init__(self, direction, resolution, player):
        super().__init__()

        self.player = player
        self.resolution = resolution

        self.dlight = DirectionalLight("sun")
        self.dlight.setShadowCaster(True, self.resolution, self.resolution)

        lens = self.dlight.getLens()
        lens.setNearFar(-160, 400)
        lens.setFilmSize((200, 200))

        self.dlnp = render.attachNewNode(self.dlight)
        self.dlnp.lookAt(direction)
        render.setLight(self.dlnp)

    def update(self):
        self.dlnp.setPos(self.player.world_position)

    def update_resolution(self):
        self.dlight.setShadowCaster(True, self.resolution, self.resolution)