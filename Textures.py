from PIL import Image

imgPLAYER   = "Player.png"
imgPLATFORM = "platform.png"
imgBLOCK    = "block.png"
imgFLAG     = "flag.png"
imgCOIN     = "coin.png"
imgSTART    = "start.png"

imgMAP = Image.open("map1.png", 'r')
imgMAP2 = Image.open("map2.png", 'r')
imgMAP3 = Image.open("map3.png", 'r')


LEVELS = {
    1: imgMAP,
    2: imgMAP2,
    3: imgMAP3,
}

