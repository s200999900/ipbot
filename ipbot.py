#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'svelic'

import os
import ConfigParser
import urllib2
import smtplib
from email.MIMEText import MIMEText


def main():

    configfile = 'ipbot.conf'
    config = ConfigParser.ConfigParser()

    if os.path.isfile(configfile) :
        config.read(configfile)
    else:
        config.add_section('account')
        config.set('account', 'email', 'email@server')
        config.set('account', 'password', 'PaSSword')
        config.set('account', 'smtp_server', 'smtp.gmail.com')
        config.set('account', 'smtp_port', '587')
        with open(configfile, 'w') as configfile:    # save config
            config.write(configfile)

        print("Please edit ipbot.conf file! ")
        return 0

    ########Считываем параметры#################
    email= (config.get('account', 'email'))
    password=(config.get('account', 'password'))
    smtp_server= (config.get('account', 'smtp_server'))
    smtp_port= (config.get('account', 'smtp_port'))
    try:
        old_ip= (config.get('ip', 'ip'))
    except ConfigParser.NoSectionError:
        # Create non-existent section
        config.add_section('ip')
        old_ip = ''
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
    new_ip= response.split("<br>")
    new_ip = new_ip[0]
    f.close()
    if old_ip == new_ip:
        return 0

    try:
        config.set('ip', 'ip', new_ip)
    except ConfigParser.NoSectionError:
        # Create non-existent section
        config.add_section('ip')
    else:
        with open(configfile, 'w') as configfile:    # save config
            config.write(configfile)
    #############################################

    print ("Our external ip: " + new_ip)

    #########Отправка email-а####################
    # текст письма
    text = """
    Привет!
    Мой текущий IP: %s

    -------------
    Br, IpBot
    """ % new_ip
    # заголовок письма
    subj = 'My external IP'

    # формирование сообщения
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = subj
    msg['From'] = email
    msg['To'] = email

    print("Email sending: ")
    print("From:\t\t" + msg['From'])
    print("To:\t\t" + msg['To'] )
    print("Subject:\t" + msg['Subject'])
    print("Text: \n " + text)

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