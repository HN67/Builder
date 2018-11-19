# Config file for game "Circular"

class game:

    caption = "Circular"

    mapSize = 450
    height = 450

    interfaceWidth = 150

    width = mapSize + interfaceWidth
    
    fps = 60

    tileNum = 15
    
    tileSize = int(height/tileNum)

class color:

    white = (255, 255, 255)
    black = (0, 0, 0)

    grey = (127, 127, 127)
    
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
