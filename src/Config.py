# Config file for game "Circular"

class game:

    caption = "Builder"

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
    lightGrey = (191, 191, 191)
    
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    brown = (80, 25, 0)
    lightBrown = (180, 100, 0)

class interface:

    imgXRatio = 0.5
    imgYRatio = 0.1
    imgBorder = 3
