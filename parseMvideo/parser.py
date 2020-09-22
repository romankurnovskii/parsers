from pprint import pprint
from parseMvideo.MvideoHits import MvideoHits

mvideo = MvideoHits()
mvideo.start()
hits = mvideo.getProducts()

pprint(hits)