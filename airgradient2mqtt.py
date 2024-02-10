#!/usr/bin/env python3

import logging
import time
import os

import yaml
import requests
import paho.mqtt.client as mqtt

log_level = logging.INFO
if os.getenv('DEBUG', False):
  log_level = logging.DEBUG

logging.basicConfig(
  format='%(asctime)s %(levelname)-7s %(message)s',
  datefmt='%Y-%d-%m %H:%M:%S',
  level=log_level
)


class AirGradient2MQTT:

    def __init__(self):

        config_file = os.path.join("config", "config.yml")
        with open(config_file) as file:
            logging.debug("Loading config from %s" % config_file)
            self.config = yaml.load(file, Loader=yaml.FullLoader)

        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_connect = self.mqtt_on_connect
        # self.mqtt_client.on_message = self.mqtt_on_message
        self.last_run = 0.0

    def fetch_sensor_data(self, location_id):
        logging.info("Fetching data for location_id %s" % location_id)
        url = f"https://api.airgradient.com/public/api/v1/locations/{location_id}/measures/current?token={self.config['airgradient']['token']}"
        try:
            r = requests.get(url, timeout=3)
            logging.debug("Got data for location_id %s: %s" % (location_id, r.json()))
            return r.text
        except requests.exceptions.Timeout:
            logging.warning("Timeout of 3 seconds reached. Will retry later.")
            return False
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request error encountered {e}")
            return False

    def mqtt_on_connect(self, client, userdata, flags, rc, properties):
        logging.info("MQTT: Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # topic = "%s/set/#" % self.mqtt_base_topic
        # logging.info("MQTT: Subscribing to %s" % topic)
        # client.subscribe(topic)

    def run(self):
        logging.debug("Setting up MQTT client (user %s, password %s)" % (self.config['mqtt']['user'], self.config['mqtt']['password']))
        self.mqtt_client.username_pw_set(self.config['mqtt']['user'], self.config['mqtt']['password'])

        while True:
            logging.info("Waiting for MQTT server...")

            connected = False
            while not connected:
                try:
                    logging.debug("Connecting to MQTT server %s:%s" % (self.config['mqtt']['server'], self.config['mqtt']['port']))
                    self.mqtt_client.connect(self.config['mqtt']['server'], int(self.config['mqtt']['port']), 60)
                    connected = True
                    logging.info("Connection to MQTT successful")
                except ConnectionRefusedError:
                    time.sleep(1)

            try:
                while True:
                    if self.last_run + float(self.config['airgradient']['fetch_every']) < time.time():
                        logging.info("Starting to work")

                        for sensor in self.config['sensors']:
                            sensor_data = self.fetch_sensor_data(sensor['location_id'])
                            if sensor_data:
                                self.mqtt_client.publish(f"{self.config['mqtt']['base_topic'].removesuffix("/")}/{sensor['serial']}", sensor_data)

                        logging.debug("Sleeping for %s seconds..." % self.config['airgradient']['fetch_every'])
                        self.last_run = time.time()

                        return_value = self.mqtt_client.loop()
                        if return_value:
                            logging.error("MQTT client loop returned <%s>. Restarting..." % return_value)
                            break
                    else:
                        time.sleep(0.1)
            finally:
                self.mqtt_client.disconnect()
                connected = False


if __name__ == "__main__":
    a2m = AirGradient2MQTT()
    a2m.run()
