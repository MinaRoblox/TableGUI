import engine

image_path = "8_8_weird.png"

game = engine.TableGUI("image test", 32, 600, background_color = engine.RED, debug=True)
screen = 0
game.render_image(image_path, 8, (16, 6), (0, 0, 0), screen)

while True:
    k = game.loop_code(screen)
    if k == False:
        break
