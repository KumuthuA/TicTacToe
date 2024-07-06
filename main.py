import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        self.WINDOW_WIDTH = 720
        self.SQUARE_WIDTH = self.WINDOW_WIDTH // 3
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_WIDTH))

        self.title_font = pygame.font.Font(pygame.font.match_font("arialblack"), 70)
        self.button_font = pygame.font.Font(pygame.font.match_font("arialblack"), 40)

        self.button_bg_colour = pygame.Color("#5A7FB1")
        self.cicle_font_colour = pygame.Color("#5AC3F3")
        self.cross_font_colour = pygame.Color("#F56361")

        self.BG_IMAGE = self.load_image("images/background.jpg", (self.WINDOW_WIDTH, self.WINDOW_WIDTH))
        self.GRID = self.load_image("images/grid.png", (self.WINDOW_WIDTH, self.WINDOW_WIDTH))
        self.CROSS = self.load_image("images/cross.png", (self.SQUARE_WIDTH, self.SQUARE_WIDTH))
        self.CIRCLE = self.load_image("images/circle.png", (self.SQUARE_WIDTH, self.SQUARE_WIDTH))

        self.win_sound = pygame.mixer.Sound('sounds/tadaa.mp3')
        self.draw_sound = pygame.mixer.Sound('sounds/draw.mp3')
        self.play_win_sound = None
        self.play_draw_sound = None

        #game variables
        self.BOARD = [[None, None, None], [None, None, None], [None, None, None]]
        self.PLAYER_1 = 0
        self.PLAYER_2 = 1
        self.PLAYER = self.PLAYER_1

        self.clock = pygame.time.Clock()
        self.running = True
        self.starting_screen = True

    def load_image(self, path, resolution):
        return pygame.transform.scale(pygame.image.load(path), resolution)

    def play(self, curr_player):
        curr_position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            row, col = curr_position[0] // self.SQUARE_WIDTH, curr_position[1] // self.SQUARE_WIDTH
            if self.BOARD[col][row] is None:
                self.BOARD[col][row] = 0 if curr_player == 0 else 1
                self.PLAYER = 1 - self.PLAYER
                print(self.BOARD)

    def display_icons(self):
        for i in range(3):
            for j in range(3):
                icon = self.BOARD[i][j]
                if icon is not None:
                    self.screen.blit(self.CIRCLE if icon == 0 else self.CROSS, (j * self.SQUARE_WIDTH, i * self.SQUARE_WIDTH))

    def has_equal_icons(self, icons, curr_player):
        """Check if all icons in a row, column or diagonal are the same"""
        return all(icon == curr_player for icon in icons)

    def is_winner(self, curr_player):
        """Check if the a player has won"""
        return any(self.has_equal_icons(self.BOARD[i], curr_player) for i in range(3)) or \
               any(self.has_equal_icons([self.BOARD[i][j] for i in range(3)], curr_player) for j in range(3)) or \
               self.has_equal_icons([self.BOARD[i][i] for i in range(3)], curr_player) or \
               self.has_equal_icons([self.BOARD[i][2-i] for i in range(3)], curr_player)

    def has_winner(self):
        """Check if there is a winner"""
        if self.is_winner(self.PLAYER_1):
            self.text = "Player 1 WON!"
            return True
        if self.is_winner(self.PLAYER_2):
            self.text = "Player 2 WON!"
            return True
        return False

    def has_drawn(self):
        """Check for a draw."""
        if all(self.BOARD[i][j] is not None for i in range(3) for j in range(3)):
            self.text = "It's a DRAW!"
            return True
        return False

    def create_button(self, text, colour, pos):
        """Create a button on the screen"""
        button = self.button_font.render(text, True, "white")
        button_rect = button.get_rect(center=pos)
        pygame.draw.rect(self.screen, colour, button_rect.inflate(20, 20))
        self.screen.blit(button, button_rect)
        return button_rect

    def create_title_text(self, text, colour, pos, hasBgcolour = False):
        """Create text on the screen"""
        if hasBgcolour:
            title = self.title_font.render(text, True, colour)
            title_rect = title.get_rect(center=pos)
            pygame.draw.rect(self.screen, "white", title_rect.inflate(10, 10))
            pygame.draw.rect(self.screen, "black", title_rect.inflate(10, 10), 5)
        else: 
            title = self.button_font.render(text, True, colour)
            title_rect = title.get_rect(center=pos)
        self.screen.blit(title, title_rect)
        return 

    def wait_for_button_click(self, *button_rects):
        """Wait for a click event."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in button_rects:
                        if rect.collidepoint(event.pos):
                            if rect == button_rects[0]:
                                self.reset_game()
                            else:
                                self.running = False
                            return
                        
    def display_starting_screen(self):
        """Display the starting screen with game title, player definition and play button."""
        self.screen.blit(self.BG_IMAGE, (0, 0))

        title = self.title_font.render("TicTacToe", True, "black")
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 4))
        self.screen.blit(title, title_rect)

        self.create_title_text("Player 1: Circle",  self.cicle_font_colour , (self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2 - 50))
        self.create_title_text("Player 2: Cross",  self.cross_font_colour , (self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2))

        play_button_rect = self.create_button("Play", self.button_bg_colour, (self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2 + 100))

        pygame.display.flip()
        self.wait_for_button_click(play_button_rect)


    def display_end_screen(self):
        """Display the end screen with game result and options to play again or quit."""
        self.create_title_text(self.text, self.cicle_font_colour if self.text == "Player 1 WON!" else self.cross_font_colour , (self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2 - 100), True)

        play_again_button_rect = self.create_button("Play Again", "blue", (self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2 + 50))
        quit_button_rect = self.create_button("Quit", "red", (self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2 + 150))

        pygame.display.flip()
        self.wait_for_button_click(play_again_button_rect, quit_button_rect)

    def reset_game(self):
        """Reset the game"""
        self.BOARD = [[None, None, None], [None, None, None], [None, None, None]]
        self.PLAYER = self.PLAYER_1
        self.play_win_sound = None
        self.play_draw_sound = None

    def run(self):
        self.display_starting_screen()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.BG_IMAGE, (0, 0))
            self.screen.blit(self.GRID, (0, 0))

            pygame.event.wait()

            if not self.has_winner():
                self.display_icons()
                if self.has_drawn():
                    if self.play_draw_sound is None:
                        self.play_draw_sound = 1
                    self.display_end_screen()
                else:
                    self.play(self.PLAYER)    
            else:
                self.display_icons()
                if self.play_win_sound is None:
                    self.play_win_sound = 1
                self.display_end_screen()

            if self.play_win_sound:
                self.win_sound.play()
                self.play_win_sound = 0
            
            if self.play_draw_sound:
                self.draw_sound.play()
                self.play_draw_sound = 0

            pygame.display.flip()
            self.clock.tick

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()