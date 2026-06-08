from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_time_interval

from datetime import timedelta


BLUE_HC = 0.11
BLUE_HP = 0.15

WHITE_HC = 0.13
WHITE_HP = 0.18

RED_HC = 0.16
RED_HP = 0.72


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
):
    async_add_entities([OctopusTempoSensor(hass)], True)


class OctopusTempoSensor(SensorEntity):

    _attr_name = "Octopus Tempo Tarif Actuel"
    _attr_unique_id = "octopus_tempo_tarif_actuel"
    _attr_native_unit_of_measurement = "€/kWh"

    def __init__(self, hass):
        self.hass = hass
        self._state = None

    @property
    def native_value(self):
        return self._state

    async def async_update(self):

        couleur = self.hass.states.get(
            "sensor.tarif_tempo_couleur_aujourd_hui"
        )

        hc = self.hass.states.get(
            "binary_sensor.linky_hc_active"
        )

        if not couleur or not hc:
            self._state = None
            return

        couleur = couleur.state.lower()
        hc_active = hc.state == "on"

        if couleur == "bleu":
            self._state = BLUE_HC if hc_active else BLUE_HP

        elif couleur == "blanc":
            self._state = WHITE_HC if hc_active else WHITE_HP

        elif couleur == "rouge":
            self._state = RED_HC if hc_active else RED_HP

        else:
            self._state = None
