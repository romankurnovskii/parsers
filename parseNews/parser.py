from pprint import pprint
from parseNews.LentaRu import LentaRu
from parseNews.MailRu import MailRu

parserLenta = LentaRu()
parserLenta.connect()

pprint(parserLenta.parse())


parserMailRu = MailRu()
parserMailRu.connect()

pprint(parserMailRu.parse())




