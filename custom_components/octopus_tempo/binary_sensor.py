from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    async_add_entities(
        [
            OctopusTempoRedHPSensor(hass),
        ],
        True,
    )


class OctopusTempoRedHPSensor(BinarySensorEntity):

    _attr_name = "Octopus Tempo Rouge HP"
    _attr_unique_id = "octopus_tempo_rouge_hp"

    def __init__(self, hass):
        self.hass = hass
        self._attr_is_on = False

    async def async_update(self):

        couleur_entity = self.hass.states.get(
            "sensor.tarif_edf_tempo_9kva_tarif_tempo_couleur_aujourd_hui"
        )

        hc_entity = self.hass.states.get(
            "binary_sensor.linky_06526193900327_heures_creuses_actives"
        )

        if not couleur_entity or not hc_entity:
            self._attr_is_on = False
            return

        couleur = couleur_entity.state.lower()
        hc_active = hc_entity.state == "on"

        self._attr_is_on = (
            couleur == "rouge" and not hc_active
        )
