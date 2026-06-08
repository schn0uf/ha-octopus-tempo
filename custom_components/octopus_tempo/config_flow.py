import voluptuous as vol

from homeassistant import config_entries

DOMAIN = "octopus_tempo"


class OctopusTempoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:

            return self.async_create_entry(
                title="Octopus Tempo",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required("blue_hc", default=0.11): float,
                vol.Required("blue_hp", default=0.15): float,

                vol.Required("white_hc", default=0.13): float,
                vol.Required("white_hp", default=0.18): float,

                vol.Required("red_hc", default=0.16): float,
                vol.Required("red_hp", default=0.72): float,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
