from ursina import *
from ursina import curve

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)
y_dir = lambda y: -1 if y < 0 else(1 if y > 0 else -1)

class Player(Entity):
    def __init__(self, position, speed = 5, jump_height = 14):
        super().__init__(
            model = "cube", 
            position = position,
            scale = (1.3, 1, 1.3), 
            visible_self = False,
            rotation_y = -270
        )

        # Camera
        mouse.locked = True
        camera.parent = self
        camera.position = (0, 2, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 100

        # Player values
        self.speed = speed
        self.jump_count = 0
        self.jump_height = jump_height
        self.jumping = False
        self.can_move = True
        self.grounded = False

        # Velocity
        self.velocity = (0, -10, 0)
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]

        # Movement
        self.movementX = 0
        self.movementZ = 0

        self.mouse_sensitivity = 50

        self.terrain = None

    def jump(self):
        self.jumping = True
        self.velocity_y = self.jump_height
        self.jump_count += 1

    def update(self):
        movementY = self.velocity_y / 75
        self.velocity_y = clamp(self.velocity_y, -70, 100)

        direction = (0, sign(movementY), 0)

        # Main raycast for collision
        y_ray = raycast(origin = self.world_position, direction = (0, y_dir(self.velocity_y), 0), traverse_target = self.terrain, ignore = [self, ])
            
        if y_ray.distance <= self.scale_y * 1.5 + abs(movementY):
            if not self.grounded:
                self.velocity_y = 0
                self.grounded = True

            # Check if hitting a wall or steep slope
            if y_dir(self.velocity_y) == -1:
                if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                    # Set the y value to the ground's y value
                    if not held_keys["space"]:
                        self.y = y_ray.world_point.y + 1.4
                    self.jump_count = 0
                    self.jumping = False
        else:
            self.velocity_y -= 40 * time.dt
            self.grounded = False
            self.jump_count = 1

            self.y += movementY * 50 * time.dt

        movement = 10 if y_ray.distance < 5 else 5

        if held_keys["w"]:
            self.velocity_z += movement * time.dt
        else:
            self.velocity_z = lerp(self.velocity_z, 0 if y_ray.distance < 5 else 1, time.dt * 3)
        if held_keys["a"]:
            self.velocity_x += movement * time.dt
        else:
            self.velocity_x = lerp(self.velocity_x, 0 if y_ray.distance < 5 else 1, time.dt * 3)
        if held_keys["s"]:
            self.velocity_z -= movement * time.dt
        else:
            self.velocity_z = lerp(self.velocity_z, 0 if y_ray.distance < 5 else 1, time.dt * 3)
        if held_keys["d"]:
            self.velocity_x -= movement * time.dt
        else:
            self.velocity_x = lerp(self.velocity_x, 0 if y_ray.distance < 5 else -1, time.dt * 3)

        # Movement
        if y_ray.distance <= 5:
            self.movementX = (self.forward[0] * self.velocity_z + 
                self.left[0] * self.velocity_x + 
                self.back[0] * -self.velocity_z + 
                self.right[0] * -self.velocity_x) * self.speed * time.dt

            self.movementZ = (self.forward[2] * self.velocity_z + 
                self.left[2] * self.velocity_x + 
                self.back[2] * -self.velocity_z + 
                self.right[2] * -self.velocity_x) * self.speed * time.dt
        else:
            air_movementX = 0.5 if self.movementX < 0.5 and self.movementX > -0.5 else 0.2
            air_movementZ = 0.5 if self.movementZ < 0.5 and self.movementZ > -0.5 else 0.2

            self.movementX += (self.forward[0] * held_keys["w"] * air_movementX + 
                self.left[0] * held_keys["a"] * air_movementX + 
                self.back[0] * held_keys["s"] * air_movementX + 
                self.right[0] * held_keys["d"] * air_movementX) / 2 * time.dt

            self.movementZ += (self.forward[2] * held_keys["w"] * air_movementZ + 
                self.left[2] * held_keys["a"] * air_movementZ + 
                self.back[2] * held_keys["s"] * air_movementZ + 
                self.right[2] * held_keys["d"] * air_movementZ) / 2 * time.dt

        # Collision Detection
        if self.movementX != 0:
            direction = (sign(self.movementX), 0, 0)
            x_ray = raycast(origin = self.world_position, direction = direction, traverse_target = self.terrain, ignore = [self, ])

            if x_ray.distance > self.scale_x / 2 + abs(self.movementX):
                self.x += self.movementX

        if self.movementZ != 0:
            direction = (0, 0, sign(self.movementZ))
            z_ray = raycast(origin = self.world_position, direction = direction, traverse_target = self.terrain, ignore = [self, ])

            if z_ray.distance > self.scale_z / 2 + abs(self.movementZ):
                self.z += self.movementZ

        # Camera
        camera.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity
        camera.rotation_x = min(max(-90, camera.rotation_x), 90)

    def input(self, key):
        if key == "space":
            if self.jump_count < 1:
                self.jump()