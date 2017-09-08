#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
from pyA20.gpio import connector
import config
import time

token = config.bot_token
allow_users = config.allow_users.split(',')
bot = telebot.TeleBot(token)
bot.config['api_key'] = token

print 'init gpio'
gpio.init()

pin_out = port.PA7 #gpio21
pin_in = port.PA8 #gpio22

gpio.setcfg(pin_out, gpio.OUTPUT)
gpio.setcfg(pin_in, gpio.INPUT)
sleep(0.1)

gpio.pullup(pin_in, gpio.PULLDOWN)
sleep(0.1)

gpio.output(pin_out, 1)
n = True
start = time.clock()
stop = 0
try:
    while True:
        #читаем еденицы
        if n:
            state = gpio.input(pin_in)
            n = state == 1
        # если проскочил 0 значит шум, сбрасываем время
        if not n:
            start = time.clock()
            n = True
        stop = time.clock()
        # если в течение 0.2 секунд были только 1 значит кнопка нажата
        if stop - start > 0.2:
            print 'bell'
            n = False
            for b in allow_users:
                bot.send_message(b, u'В дверь звонят!')
            sleep(1)
except KeyboardInterrupt:
    gpio.output(pin_out, gpio.LOW)
    print '\n exit'

