import pygame
import numpy as np
from PIL import Image


# ggs to chatgpt for generating this shit
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_PINK = (255, 182, 193)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 139)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
TURQUOISE = (64, 224, 208)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
VIOLET = (238, 130, 238)
BEIGE = (245, 245, 220)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
INDIGO = (75, 0, 130)
LAVENDER = (230, 230, 250)
SALMON = (250, 128, 114)
CORAL = (255, 127, 80)
MINT = (189, 252, 201)
SKY_BLUE = (135, 206, 235)
CHOCOLATE = (210, 105, 30)
# guify

def get_table_color_from_image(image: str):
    """
    :param image: path to image
    """
    img = Image.open(image).convert("RGB")
    arr = np.array(img)

    if arr.shape[0] <= 16 and arr.shape[1] <= 16:
        return [tuple(map(int, pixel)) for pixel in arr.reshape(-1, 3)]
    return None

class TableGUI:
    def __init__(self,
                 app_name: str,
                 table_size: int,
                 screen_size: int,
                 background_color: tuple = BLACK,
                 audio_channels_amount: int = 10,
                 screens: int = 1,
                 debug: bool = False
        ):
        # initiation
        pygame.init()
        pygame.mixer.init()
        # audio helping
        self.audio_channels_amount = audio_channels_amount
        pygame.mixer.set_num_channels(audio_channels_amount)
        # window setting
        self.NAME = app_name
        self.SCREEN_SIZE = screen_size
        # find screen size
        scale_x = self.SCREEN_SIZE / table_size
        scale_y = self.SCREEN_SIZE / table_size
        # defines the space between pixels
        self.number = min(scale_x, scale_y)
        # table creator
        def return_table():
            return [
                [background_color for x in range(table_size)] for y in range(table_size)
            ]
        # window code
        # screen code
        self.all_screens = []
        for number in range(screens):
            self.all_screens.append(return_table())

        self.WINDOW = pygame.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        pygame.display.set_caption(self.NAME)
        # debug activator
        self.debug = debug

    def draw_screen(self, screen):
        """
        screen: the selected screen you want to draw
        """
        # uses self.number to determine the screen as a grid
        first_for_y = 0
        for table in self.all_screens[screen]:
            second_for_x = 0
            for number in table:
                pygame.draw.rect(self.WINDOW, (number[0], number[1], number[2]),
                [second_for_x, first_for_y, self.number, self.number], 0) # [x, y, width, height]
                second_for_x += self.number
                if self.debug:
                    print(f"Information: ({first_for_y}, {second_for_x}, {number})")
            first_for_y += self.number

        pygame.display.update()

    # detect collision
    def check_coordinate_for_object(self, expected: tuple, coordinate: tuple, screen: int):
        """
        expected: (x, y) ex: (8, 10)
        coordinate = (x, y)
        screen: the selected screen you want to draw
        """
        if expected == self.all_screens[screen][coordinate[1]][coordinate[0]]:
            if self.debug:
                print("Information: ")
                print(f"Data in {coordinate}: {self.all_screens[coordinate[1]][coordinate[0]]}")
            return True
        return False

    def render_image(self, image_path, screen: int):
        """
        image_path: path to image
        screen: the selected screen you want to draw
        """
        color = get_table_color_from_image(image_path)
        i = 0
        coordenadas = []
        for y in range(16):
            for x in range(16):
                coordenadas.append((x, y))
        for coordenda in coordenadas:
            if self.debug:
                print(f"Color: {color[i]}")
                print(f"Coordenada: {coordenda}")
            self.draw(color[i], coordenda, screen)
            i += 1


    #####
    #
    # Music Code
    #
    #####

    def play_music(self, audio_music: str, channel: int):
        """
        audio_music: path to file (ex: 'audio/audio.mp3')
        channel: int. ex: 1
        """
        if self.debug:
            print("Information: ")
            print(f"Channel: {channel}, File given: {audio_music}")
        pygame.mixer.Channel(channel).play(pygame.mixer.Sound(audio_music))

    def stop_music(self, channel: int):
        """
        channel: int. ex: 1
        """
        if self.debug:
            print("Information: ")
            print(f"Channel: {channel}")
        pygame.mixer.Channel(channel).stop()

    def set_volume(self, channel: int, volume: float):
        """
        channel: int. ex: 1
        volume: float. (0 - 1) ex: 0.7
        """
        if self.debug:
            print("Information: ")
            print(f"Channel: {channel}, Volume: {volume}")
        pygame.mixer.Channel(channel).set_volume(volume)

    #####
    #
    # Music Code
    #
    #####

    def draw(self, color: tuple, coordinates: tuple, screen: int):
        """
        color: color. ex: (255, 0, 0)
        coordinates: (x, y) ex: (8, 10)
        screen: the selected screen you want to draw
        """
        self.all_screens[screen][coordinates[1]][coordinates[0]] = color
        if self.debug:
            print(f"Color given: {color}")
            print(f"Coordinates given: {coordinates}")

    def loop_code(self, screen: int):
        """
        screen: the selected screen you want to draw
        Returns the key pressed by the user:
        - up arrow: 'up'
        - w key: 'w'
        """

        for event in pygame.event.get():
            self.draw_screen(screen)
            if self.debug:
                print("Finished drawing screen.")

            if event.type == pygame.QUIT:
                if self.debug:
                    print("Quitting game...")
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if self.debug:
                    print(key)
                return key
        if self.debug:
            print("Finished drawing screen. Again")
        self.draw_screen(screen)

        return None  # No key was pressed this frame

    def batch_draw(self, all_coordinates: list, color: tuple, screen: int):
        """
        color: color. ex: (255, 0, 0)
        coordinates: [(x, y), (x, y)]. ex: [(0, 1), (0, 1)]
        screen: the selected screen you want to draw
        """
        for coordinate in all_coordinates:
            self.all_screens[screen][coordinate[1]][coordinate[0]] = color
        if self.debug:
            print(f"Color given: {color}")
            print(f"Every coordinate: {all_coordinates}")
