import sys

import pygame

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Get screen resolution
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WIDTH, HEIGHT = 800, 600

# Define the margin based on resolution
MARGIN_TOP = HEIGHT // 20
MARGIN_SIDE = WIDTH // 40
FONT_SIZE = HEIGHT // 25

# Define the button size based on resolution
BUTTON_WIDTH = WIDTH // 10
BUTTON_HEIGHT = HEIGHT // 20
BUTTON_MARGIN_TOP = HEIGHT // 100
BUTTON_MARGIN_RIGHT = WIDTH // 100

# Define the page number size based on resolution
PAGE_NUM_MARGIN_BOTTOM = HEIGHT // 40
PAGE_NUM_HORIZONTAL_OFFSET = WIDTH // 40

# Define the text box dimensions based on resolution
TEXT_BOX_WIDTH = WIDTH // 2 - 2 * MARGIN_SIDE
TEXT_BOX_HEIGHT = HEIGHT - 2 * MARGIN_TOP

# Define the size of the interaction button
CLOSE_BUTTON = pygame.Rect(WIDTH - 2 * BUTTON_WIDTH - BUTTON_MARGIN_RIGHT, BUTTON_MARGIN_TOP, BUTTON_WIDTH,
                           BUTTON_HEIGHT)
SAVE_BUTTON = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_MARGIN_RIGHT, BUTTON_MARGIN_TOP, BUTTON_WIDTH, BUTTON_HEIGHT)
NEXT_PAGE_BUTTON = pygame.Rect(WIDTH - BUTTON_MARGIN_RIGHT - BUTTON_WIDTH, HEIGHT - BUTTON_MARGIN_TOP - BUTTON_HEIGHT,
                               BUTTON_WIDTH, BUTTON_HEIGHT)

# Define the sample text for the left page
sample_text = """Once upon a time in a faraway land where wonders and magic were everyday occurrences, there lived a brave hero who embarked on a quest to save the kingdom from a fearsome dragon."""

# Define screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Children\'s Book')
clock = pygame.time.Clock()

# Define fonts
font = pygame.font.Font(None, FONT_SIZE)


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
                if CLOSE_BUTTON.collidepoint(x, y):
                    running = False

                # Check save button
                elif SAVE_BUTTON.collidepoint(x, y):
                    # Implement save functionality here
                    print("Saved!")

                # Check next page button
                elif NEXT_PAGE_BUTTON.collidepoint(x, y):
                    if page_number < 100:
                        page_number += 1

        # Drawing
        screen.fill(WHITE)

        # Draw close button
        pygame.draw.rect(screen, BLACK, (
            WIDTH - 2 * BUTTON_WIDTH - BUTTON_MARGIN_RIGHT, BUTTON_MARGIN_TOP, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        draw_text(screen, "Exit", (
            WIDTH - 2 * BUTTON_WIDTH - BUTTON_MARGIN_RIGHT + BUTTON_WIDTH // 4, BUTTON_MARGIN_TOP + BUTTON_HEIGHT // 4),
                  font)

        # Draw save button
        pygame.draw.rect(screen, BLACK,
                         (WIDTH - BUTTON_WIDTH - BUTTON_MARGIN_RIGHT, BUTTON_MARGIN_TOP, BUTTON_WIDTH, BUTTON_HEIGHT),
                         2)
        draw_text(screen, "Save", (
            WIDTH - BUTTON_WIDTH - BUTTON_MARGIN_RIGHT + BUTTON_WIDTH // 4, BUTTON_MARGIN_TOP + BUTTON_HEIGHT // 4),
                  font)

        # Draw next page button
        pygame.draw.rect(screen, BLACK, (
            WIDTH - BUTTON_MARGIN_RIGHT - BUTTON_WIDTH, HEIGHT - BUTTON_MARGIN_TOP - BUTTON_HEIGHT, BUTTON_WIDTH,
            BUTTON_HEIGHT), 2)
        symbol = ">"
        symbol_width, symbol_height = font.size(symbol)
        draw_text(screen, symbol,
                  (WIDTH - BUTTON_MARGIN_RIGHT - BUTTON_WIDTH + (BUTTON_WIDTH - symbol_width) // 2,
                   HEIGHT - BUTTON_MARGIN_TOP - BUTTON_HEIGHT + (BUTTON_HEIGHT - symbol_height) // 2), font)

        # Display page numbers for both pages
        left_page_center = WIDTH / 4
        right_page_center = 3 * WIDTH / 4
        bottom_align = HEIGHT - PAGE_NUM_MARGIN_BOTTOM

        draw_text(screen, f"{page_number * 2 - 1}", (left_page_center - PAGE_NUM_HORIZONTAL_OFFSET, bottom_align),
                  font)  # Left page
        draw_text(screen, f"{page_number * 2}", (right_page_center - PAGE_NUM_HORIZONTAL_OFFSET, bottom_align),
                  font)  # Right page

        # Draw the vertical line separating the two pages
        pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

        # Define the decision rectangle
        DEC_HEIGHT = MARGIN_TOP + HEIGHT - 7 * MARGIN_TOP + 10
        dec_rect = pygame.Rect(MARGIN_SIDE, DEC_HEIGHT, WIDTH // 2 - 2 * MARGIN_SIDE, HEIGHT - DEC_HEIGHT - MARGIN_TOP)
        pygame.draw.rect(screen, GREY, dec_rect, border_radius=10)

        # Define the text rectangle
        text_rect = pygame.Rect(MARGIN_SIDE, MARGIN_TOP, WIDTH // 2 - 2 * MARGIN_SIDE, HEIGHT - 7 * MARGIN_TOP)

        # Wrapping the text
        wrapped_text = wrap_text(sample_text, font, text_rect.width - 20)  # 20 for some padding

        # Draw the text inside the box
        pygame.draw.rect(screen, GREY, text_rect,
                         border_radius=10)  # Draw a background for the text box with rounded corners
        draw_multiline_text(screen, wrapped_text, (MARGIN_SIDE + 10, MARGIN_TOP + 10), font)

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
