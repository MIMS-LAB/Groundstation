import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    pygame.quit()
    sys.exit()

# Use the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick Name: {joystick.get_name()}")
print(f"Number of Axes: {joystick.get_numaxes()}")
print(f"Number of Buttons: {joystick.get_numbuttons()}")
print(f"Number of Hats: {joystick.get_numhats()}")

# Create a screen to keep the event loop running
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Joystick Test")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read axis values
    for i in range(joystick.get_numaxes()):
        axis = joystick.get_axis(i)
        print(f"Axis {i}: {axis:.2f}")

    # Read button values
    for i in range(joystick.get_numbuttons()):
        button = joystick.get_button(i)
        print(f"Button {i}: {'Pressed' if button else 'Released'}")

    # Read hat (D-pad) values
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        print(f"Hat {i}: {hat}")

    print("-" * 30)
    pygame.time.wait(500)  # Delay to make output readable

# Cleanup
pygame.quit()
