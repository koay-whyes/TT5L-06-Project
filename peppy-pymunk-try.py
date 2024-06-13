import pygame
import pymunk
import pymunk.pygame_util


pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10/10), (width, 20/10)],
        [(width/2, 10/10), (width, 20/10)],
        [(10/10, height/2), (20/10, height)],
        [(width - 10/10, height/2), (20/10, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.mass = 100000
        shape.elasticity = 0.4
        shape.friction = 0.8
        space.add(body, shape)

def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, height - 120), (40, 200), BROWN, 100],
        [(900, height - 120), (40, 200), BROWN, 100],
        [(750, height - 240), (340, 40), BROWN, 150]
    ]

    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=2)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

def create_swinging_ball(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 100)

    body = pymunk.Body()
    body.position = (300, 150)
    line = pymunk.Segment(body, (0, 0), (200, 0), 5)
    circle = pymunk.Circle(body, 40, (200, 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95
    circle.color = (128, 128, 128,0)
    line.color = (128, 128, 128,0)
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)


def run(screen, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)
    last_jump_time = 0
    jump_cooldown = 2  # 2 seconds
    
    # Create the body
    body_body = pymunk.Body(1, 1666)
    body_body.position = (100, 100)

    # Create the shape for the body
    body_shape = pymunk.Circle(body_body, 50)
    body_shape.elasticity = 0.2
    body_shape.friction = 0.1
    body_shape.color = (255,255,255,0)
    body_image = pygame.image.load("img/Peppy/Peppy_Fall_Frames/Peppy_Fall_Frame1.png")
    body_image = pygame.transform.scale(body_image, (100,100))

    # Add the body and shape to the space
    space.add(body_body, body_shape)

    create_boundaries(space, width, height)
    create_structure(space, width, height)
    create_swinging_ball(space)

    draw_options = pymunk.pygame_util.DrawOptions(screen)



    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        # Get the current key presses
        keys = pygame.key.get_pressed()

        # Move the body left and right
        if keys[pygame.K_a]:
            body_body.velocity = (-200, body_body.velocity.y)
        if keys[pygame.K_d]:
            body_body.velocity = (200, body_body.velocity.y)

        # Jump
        current_time = pygame.time.get_ticks() / 1000
        if keys[pygame.K_w] and abs(body_body.velocity.y) < 1 and current_time - last_jump_time > jump_cooldown:
            body_body.apply_impulse_at_local_point((0, 1000), (0, 0))
            last_jump_time = current_time

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the Pymunk shapes
        space.debug_draw(draw_options)
        image_x = body_body.position.x - body_image.get_width() / 2
        image_y = body_body.position.y - body_image.get_height() / 2
        screen.blit(body_image, (image_x, image_y))

        # Flip the screen
        pygame.display.flip()

        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(screen, WIDTH, HEIGHT)