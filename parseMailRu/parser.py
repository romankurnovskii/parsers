from parseMailRu.MailRu import MailRu

mailru = MailRu()
mailru.start(countEmails=30)
mailru.getEmails()
