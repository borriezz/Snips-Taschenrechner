#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes, MqttOptions
import toml
import random

MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None

snips_config = toml.load('/etc/snips.toml')
if 'mqtt' in snips_config['snips-common'].keys():
    MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
if 'mqtt_username' in snips_config['snips-common'].keys():
    MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
if 'mqtt_password' in snips_config['snips-common'].keys():
    MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']

def action_wrapper(hermes, intent_message):
    item = intent_message.slots.item_random.first().value
    if item == 'coin' or item == 'kopf ' or item == 'münze ':
        coin_random = random.randrange(0, 1)
        if coin_random == 0:
            result_sentence = "Es ist ein Kopf."
        else:
            result_sentence = "Es ist eine Zahl."
    elif item == 'dice' or item == 'würfel ':
        dice_random = random.randrange(1, 6)
        result_sentence = "Ich habe eine {number} gewürfelt.".format(number=dice_random)
    elif item == 'number' or item == 'zahl ':
        number_random = random.randrange(0, 1000)
        result_sentence = "Die {number} habe ich gerade zufällig gewählt.".format(number=number_random)
    # TODO: random number from range
    else:
        result_sentence = "Diese Funktion ist noch nicht verfügbar."
    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents("domi:getZufall", action_wrapper).start()