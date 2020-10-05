from pprint import pprint

from LentaRu import LentaRu
from MailRu import MailRu

print('parsing lenta.ru')
parserLenta = LentaRu()
parserLenta.connect()
pprint(parserLenta.parse())

print('parsing mail.ru')
parserMailRu = MailRu()
parserMailRu.connect()
pprint(parserMailRu.parse())




