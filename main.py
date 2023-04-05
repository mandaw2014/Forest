from ursina import *
from direct.stdpy import thread

from player import Player
from tree import Tree
from sun import SunLight

Text.default_resolution = Text.size * 1080

if sys.platform != "darwin":
    window.fullscreen = True
else:
    window.size = window.fullscreen_size
    window.position = Vec2(
        int((window.screen_resolution[0] - window.fullscreen_size[0]) / 2),
        int((window.screen_resolution[1] - window.fullscreen_size[1]) / 2)
    )

app = Ursina()
window.borderless = False
window.cog_button.disable()
window.exit_button.disable()

# Starting new thread for assets

def load_assets():
    models_to_load = [
        "tree.obj", "rocks.obj", "grass.obj", "boulders.obj", "ground.obj", "tent.obj"
    ]

    textures_to_load = [
        "ground.png", "tent.png", "trees.png", "rocks.png", "grass.png", "boulders.png"
    ]

    for i, m in enumerate(models_to_load):
        load_model(m)

    for i, t in enumerate(textures_to_load):
        load_texture(t)

try:
    thread.start_new_thread(function = load_assets, args = "")
except Exception as e:
    print("error starting thread", e)

scene.fog_density = 0.008
scene.fog_color = color.hex("ffd666")

player = Player((0, 50, 10))

terrain = Entity(model = "ground.obj", texture = "ground.png", collider = "mesh", scale = 5)
player.terrain = terrain

trees = []

tent = Entity(model = "tent.obj", texture = "tent", collider = "mesh", parent = terrain)
rocks = Entity(model = "rocks.obj", texture = "rocks", scale = 5)
grass = Entity(model = "grass.obj", texture = "grass", scale = 5)
boulders = Entity(model = "boulders.obj", texture = "boulder", scale = 5)

for i in range(0, 400):
    tree = Tree(tent)
    trees.append(tree)

# Lighting + shadows
sun = SunLight(direction = (-0.7, -0.9, 0.5), resolution = 3072, player = player)
ambient = AmbientLight(color = Vec4(0.5, 0.55, 0.66, 0) * 1.3)

render.setShaderAuto()

sky = Entity(model = "sphere", double_sided = True, scale = 3000, texture = "sky_default")

def update():
    for tree in trees:
        if distance(player, tree) < 400:
            tree.enabled = True
        else:
            tree.enabled = False

def input(key):
    if key == "g":
        player.position = (0, 50, 10)

app.run()