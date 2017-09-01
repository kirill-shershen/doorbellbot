#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
from pyA20.gpio import connector
import config


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
try:
    while True:
        state1 = gpio.input(pin_in)
        sleep(0.3)
        state2 = gpio.input(pin_in)
        if state1 == 1 and state1 == state2:
            for b in allow_users:
                bot.send_message(b, u'В дверь звонят!')
            sleep(1)
except KeyboardInterrupt:
    gpio.output(pin_out, gpio.LOW)
    print '\n exit'

