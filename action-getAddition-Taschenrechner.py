#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes, MqttOptions
import toml


USERNAME_INTENTS = "domi"
MQTT_BROKER_ADDRESS = "192.168.180.20:1883"
MQTT_USERNAME = "mqttIO"
MQTT_PASSWORD = "Heli0s25"


def user_intent(intentname):
    return USERNAME_INTENTS + ":" + intentname

def action_wrapper(hermes, intent_message):
    first = int(intent_message.slots.firstTerm.first().value)
    second = int(intent_message.slots.secondTerm.first().value)
    calc = first + second
    if str(calc)[-2:] == ".0":
        calc = int(calc)
    result_sentence = "{} plus {} ergibt {} .".format(first, second, calc)

    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']

    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents("domi:getAddition", action_wrapper).start()