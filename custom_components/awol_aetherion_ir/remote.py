"""Remote platform for AWOL Vision Aetherion Max IR integration.

Exposes a remote entity with navigation and app-launch commands for use
with dashboards and automations that call remote.send_command.
"""

from __future__ import annotations

from homeassistant.components.remote import RemoteEntity, RemoteEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INFRARED_ENTITY_ID
from .entity import AetherionIrEntity
from .ir_codes import AetherionCode

PARALLEL_UPDATES = 1

_COMMAND_MAP: dict[str, AetherionCode] = {
    "power": AetherionCode.POWER,
    "ai": AetherionCode.AI,
    "mute": AetherionCode.MUTE,
    "input_source": AetherionCode.INPUT_SOURCE,
    "profile": AetherionCode.PROFILE,
    "google_assistant": AetherionCode.GOOGLE_ASSISTANT,
    "settings": AetherionCode.SETTINGS,
    "up": AetherionCode.UP,
    "down": AetherionCode.DOWN,
    "left": AetherionCode.LEFT,
    "right": AetherionCode.RIGHT,
    "ok": AetherionCode.OK,
    "back": AetherionCode.BACK,
    "home": AetherionCode.HOME,
    "live_guide": AetherionCode.LIVE_GUIDE,
    "live_tv": AetherionCode.LIVE_TV,
    "menu": AetherionCode.MENU,
    "volume_up": AetherionCode.VOLUME_UP,
    "volume_down": AetherionCode.VOLUME_DOWN,
    "youtube": AetherionCode.YOUTUBE,
    "netflix": AetherionCode.NETFLIX,
    "prime_video": AetherionCode.PRIME_VIDEO,
    "disney_plus": AetherionCode.DISNEY_PLUS,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up AWOL Aetherion remote from config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    async_add_entities([AetherionRemote(entry, infrared_entity_id)])


class AetherionRemote(AetherionIrEntity, RemoteEntity):
    """AWOL Aetherion Max remote entity for IR commands."""

    _attr_name = "Remote"
    _attr_supported_features = RemoteEntityFeature.ACTIVITY
    _attr_activity_list = list(_COMMAND_MAP.keys())

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        super().__init__(entry, infrared_entity_id, unique_id_suffix="remote")
        self._attr_is_on = True

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on."""
        await self._send_command(AetherionCode.POWER)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off."""
        await self._send_command(AetherionCode.POWER)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_send_command(self, command: list[str], **kwargs) -> None:
        """Send IR commands by name."""
        for cmd in command:
            code = _COMMAND_MAP.get(cmd.lower())
            if code is not None:
                await self._send_command(code)
