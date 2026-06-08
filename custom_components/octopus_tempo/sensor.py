from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "octopus_tempo"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    async_add_entities(
        [
            OctopusTempoCurrentPriceSensor(hass, entry),
            OctopusTempoColorSensor(hass),
            OctopusTempoTomorrowColorSensor(hass),
        ],
        True,
    )


class OctopusTempoCurrentPriceSensor(SensorEntity):

    _attr_name = "Octopus Tempo Tarif Actuel"
    _attr_unique_id = "octopus_tempo_tarif_actuel"
    _attr_native_unit_of_measurement = "€/kWh"

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._state = None

    @property
    def native_value(self):
        return self._state

    async def async_update(self):

        couleur_entity = self.hass.states.get(
            "sensor.tarif_edf_tempo_9kva_tarif_tempo_couleur_aujourd_hui"
        )

        hc_entity = self.hass.states.get(
            "binary_sensor.linky_06526193900327_heures_creuses_actives"
        )

        if not couleur_entity or not hc_entity:
            self._state = None
            return

        couleur = couleur_entity.state.lower()
        hc_active = hc_entity.state == "on"

        data = self.entry.data

        if couleur == "bleu":
            self._state = (
                data["blue_hc"] if hc_active else data["blue_hp"]
            )

        elif couleur == "blanc":
            self._state = (
                data["white_hc"] if hc_active else data["white_hp"]
            )

        elif couleur == "rouge":
            self._state = (
                data["red_hc"] if hc_active else data["red_hp"]
            )

        else:
            self._state = None


class OctopusTempoColorSensor(SensorEntity):

    _attr_name = "Octopus Tempo Couleur"
    _attr_unique_id = "octopus_tempo_couleur"

    def __init__(self, hass):
        self.hass = hass
        self._state = None

    @property
    def native_value(self):
        return self._state

    async def async_update(self):

        couleur_entity = self.hass.states.get(
            "sensor.tarif_edf_tempo_9kva_tarif_tempo_couleur_aujourd_hui"
        )

        if couleur_entity:
            self._state = couleur_entity.state
        else:
            self._state = None

class OctopusTempoTomorrowColorSensor(SensorEntity):

    _attr_name = "Octopus Tempo Couleur Demain"
    _attr_unique_id = "octopus_tempo_couleur_demain"

    def __init__(self, hass):
        self.hass = hass
        self._state = None

    @property
    def native_value(self):
        return self._state

    async def async_update(self):

        couleur_entity = self.hass.states.get(
            "sensor.tarif_edf_tempo_9kva_tarif_tempo_couleur_demain"
        )

        if couleur_entity:
            self._state = couleur_entity.state
        else:
            self._state = None
