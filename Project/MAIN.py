import pygame
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Set the margin for the text box
MARGIN_TOP = 100
MARGIN_SIDE = 50

# Define the sample text for the left page
sample_text = """Es war einmal in einem weit entfernten Land, 
in dem Wunder und Magie alltäglich waren. In diesem Land 
lebte ein mutiger Held, der sich auf eine Quest begab, um 
das Königreich vor einem schrecklichen Drachen zu retten."""

# Get screen resolution
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Define screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kinderbuch')
clock = pygame.time.Clock()

# Define fonts
font = pygame.font.Font(None, 36)

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        # Check width of the line with the new word
        line_width, _ = font.size(' '.join(current_line + [word]))
        if line_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))  # Add the last line
    return '\n'.join(lines)

def draw_multiline_text(surface, text, pos, font, color=BLACK):
    """Draw multiline text on a surface."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        text_surface = font.render(line.strip(), True, color)
        y_offset = i * font.get_height()
        surface.blit(text_surface, (pos[0], pos[1] + y_offset))

def draw_text(surf, text, pos, font, color=BLACK):
    """Helper function to render text on a surface."""
    text_surface = font.render(text, True, color)
    surf.blit(text_surface, pos)


def main():
    page_number = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check close button
                if WIDTH - 210 <= x <= WIDTH - 110 and 10 <= y <= 60:
                    running = False

                # Check save button
                elif WIDTH - 100 <= x <= WIDTH - 10 and 10 <= y <= 60:
                    # Implement save functionality here
                    print("Saved!")

                # Check next page button
                elif WIDTH - 60 <= x <= WIDTH - 10 and HEIGHT - 60 <= y <= HEIGHT - 10:
                    if page_number < 100:
                        page_number += 1

        # Drawing
        screen.fill(WHITE)

        # Draw close button
        pygame.draw.rect(screen, BLACK, (WIDTH - 210, 10, 100, 50), 2)
        draw_text(screen, "Exit", (WIDTH - 200, 15), font)

        # Draw save button
        pygame.draw.rect(screen, BLACK, (WIDTH - 100, 10, 90, 50), 2)
        draw_text(screen, "Save", (WIDTH - 90, 15), font)

        # Draw next page button
        pygame.draw.rect(screen, BLACK, (WIDTH - 60, HEIGHT - 60, 50, 50), 2)
        draw_text(screen, ">", (WIDTH - 50, HEIGHT - 55), font)

        # Display page numbers for both pages
        draw_text(screen, f"{page_number * 2 - 1}", (WIDTH / 4 - 70, HEIGHT - 50), font)  # Left page
        draw_text(screen, f"{page_number * 2}", (3 * WIDTH / 4 - 70, HEIGHT - 50), font)  # Right page

        # Draw the vertical line separating the two pages
        pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

        # Define the text rectangle first
        text_rect = pygame.Rect(MARGIN_SIDE, MARGIN_TOP, WIDTH // 2 - 2 * MARGIN_SIDE, HEIGHT - 2 * MARGIN_TOP)

        # Wrapping the text
        wrapped_text = wrap_text(sample_text, font, text_rect.width - 20)  # 20 for some padding

        # Draw the text inside the box
        pygame.draw.rect(screen, GREY, text_rect, border_radius=10)  # Draw a background for the text box with rounded corners
        draw_multiline_text(screen, wrapped_text, (MARGIN_SIDE + 10, MARGIN_TOP + 10), font)

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
