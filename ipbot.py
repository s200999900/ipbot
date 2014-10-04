#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'svelic'

import ConfigParser
import urllib2
import smtplib
from email.MIMEText import MIMEText

def main():
    config = ConfigParser.ConfigParser()
    config.read('ipbot.conf')

    ########Считываем параметры#################
    email= (config.get('account', 'email'))
    password=(config.get('account', 'password'))
    smtp_server= (config.get('account', 'smtp_server'))
    smtp_port= (config.get('account', 'smtp_port'))
    ############################################

    print ("Runned with next parameters: ")
    print ("Email:\t\t\t%s" % email )
    print ("Password:\t\t%s" % password )
    print ("Smtp server:\t" + smtp_server + ":" + smtp_port)
    print ("-" * 40)

    ################Получаем IP##################
    strURL='http://api.wipmania.com/'
    f = urllib2.urlopen(urllib2.Request(strURL))
    response = f.read()
    ipget= response.split("<br>")
    f.close()
    #############################################

    print ("Our external ip: " + ipget[1] + " => " + ipget[0])

    #########Отправка email-а####################
    # текст письма
    text = """
    Привет!
    Мой текущий IP: %s
    """ % ipget[1]
    # заголовок письма
    subj = 'My external IP'

    # формирование сообщения
    msg = MIMEText(text, "", "utf-8")
    msg['Subject'] = subj
    msg['From'] = email
    msg['To'] = email

    # отправка
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(email, password)
    s.sendmail(email, email, msg.as_string())
    s.quit()


if __name__ == "__main__":
    main()