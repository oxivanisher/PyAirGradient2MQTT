# PyAirGradient2MQTT

Since the current AirGradient ONE does [not support MQTT](https://forum.airgradient.com/t/mqtt-on-air-gradient-one/1390)
(yet?), this script will pull the data trough the AirGradient API and publishes it to MQTT
[as it was a sensor](https://www.airgradient.com/support/kb-mqtt-conf/). The aim is to just simulate the behaviour that
will be implemented in the future.

## Example docker-compose.yml
If you want to run it with docker compose, here is a example. Please remember to create a `config/config.yml` file.

```yaml
---
version: "3"
services:
  pywishlist:
    container_name: airgradient2mqtt
    restart: unless-stopped
    image: ghcr.io/oxivanisher/pyairgradient2mqtt:main
    volumes:
      - ./config:/app/config:ro
```
