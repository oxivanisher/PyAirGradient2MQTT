# Airgradient firmware MQTT support
Since version 3.1 of the [official airgradient firmware](https://github.com/airgradienthq/arduino), MQTT is now supported.

# PyAirGradient2MQTT

This script will pull the data trough the AirGradient API and publishes it to MQTT
[as it was a sensor](https://www.airgradient.com/support/kb-mqtt-conf/). This was a temporaray used script and **IS NO LONGER MAINTAINED**.

## Example docker-compose.yml
If you want to run it with docker compose, here is a example. Please remember to create a `config/config.yml` file.

```yaml
---
version: "3"
services:
  airgradient2mqtt:
    container_name: airgradient2mqtt
    restart: unless-stopped
    image: ghcr.io/oxivanisher/pyairgradient2mqtt:main
    volumes:
      - ./config:/app/config:ro
```
