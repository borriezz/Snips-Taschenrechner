#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes, MqttOptions
import toml

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
    first = int(intent_message.slots.firstTerm.first().value)
    second = int(intent_message.slots.secondTerm.first().value)
    if second != 0:
        calc = first / float(second)
        if str(calc)[-2:] == ".0":
            calc = int(calc)
        if "." in str(calc):
            calc_part1, calc_part2 = str(calc).split(".")
            result_sentence = "{0} geteilt durch {1} ergibt {2} komma {3} .".format(first, second,
                                                                                    calc_part1, calc_part2)
        else:
            result_sentence = "{} geteilt durch {} ergibt {} .".format(first, second, calc)
    else:
        result_sentence = "Ich kann leider nicht durch Null teilen."

    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("domi:getDivision", action_wrapper).start()