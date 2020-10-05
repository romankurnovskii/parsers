from pprint import pprint

from MvideoHits import MvideoHits

mvideo = MvideoHits()
mvideo.start()
hits = mvideo.getProducts()

pprint(hits)