#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 's200999900'

import os
import sys
import ConfigParser
import logging
import urllib2
import smtplib
from email.MIMEText import MIMEText


def main():

    configfile = 'ipbot.conf'
    logfile = 'ipbot.log'

    config = ConfigParser.ConfigParser()
    logging.basicConfig(filename=logfile,
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    if os.path.isfile(configfile) :
        logging.debug('reading config file "%s" ' % configfile )
        config.read(configfile)
    else:
        config.add_section('account')
        config.set('account', 'email', 'email@server')
        config.set('account', 'password', 'PaSSword')
        config.set('account', 'smtp_server', 'mail_server')
        config.set('account', 'smtp_port', '25')
        config.set('account', 'logfile', 'ipbot.log')
        with open(configfile, 'w') as configfile:    # save config
            config.write(configfile)

        print('Default config file created. Please edit "ipbot.conf" file! ')
        sys.exit(0)

    ########Считываем параметры#################
    email = config.get('account', 'email')
    password = config.get('account', 'password')
    smtp_server = config.get('account', 'smtp_server')
    smtp_port = config.get('account', 'smtp_port')
    logfile = config.get('account', 'logfile')

    if email == 'email@server' and password == 'PaSSword' and smtp_server == 'mail_server':
        print('Please edit "ipbot.conf" file! ')
        sys.exit(1)

    try:
        old_ip = config.get('ip', 'ip')
        logging.debug('Old IP is: ' + old_ip)
    except ConfigParser.NoSectionError:
        logging.debug('Create ip section in config file')
        config.add_section('ip')
        old_ip = ''

    logging.debug('Use next parameters: ')
    logging.debug('Email: %s' % email )
    logging.debug('Password:XXXXXX' )
    logging.debug('Smtp server: ' + smtp_server + ':' + smtp_port)

    ################Получаем IP##################
    URL = 'http://api.wipmania.com/'
    f = urllib2.urlopen(urllib2.Request(URL))
    response = f.read()
    new_ip = response.split("<br>")
    logging.info('New IP is: ' + new_ip[0] + ' => ' + new_ip[1])
    new_ip = new_ip[0]
    f.close()

    if old_ip == new_ip:
        logging.debug('IP was not changed, exiting.')
        sys.exit(0)

    try:
        config.set('ip', 'ip', new_ip)
    except ConfigParser.NoSectionError:
        # Create non-existent section
        config.add_section('ip')
    else:
        with open(configfile, 'w') as configfile:    # save config
            config.write(configfile)
    #############################################

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
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = subj
    msg['From'] = email
    msg['To'] = email

    # отправка
    # try:
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    try:
        s.login(email, password)
    except smtplib.SMTPAuthenticationError:
        print('Incorrect login!')
        logging.error('Incorrect login!')
        sys.exit(1)

    s.sendmail(email, email, msg.as_string())
    logging.debug('email sended')
    s.quit()

if __name__ == "__main__":
    main()