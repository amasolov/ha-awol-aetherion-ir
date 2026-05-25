"""Media player platform for AWOL Vision Aetherion Max IR integration."""

from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INFRARED_ENTITY_ID
from .entity import AetherionIrEntity
from .ir_codes import AetherionCode

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up AWOL Aetherion media player from config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    async_add_entities([AetherionMediaPlayer(entry, infrared_entity_id)])


class AetherionMediaPlayer(AetherionIrEntity, MediaPlayerEntity):
    """AWOL Vision Aetherion Max projector controlled via IR."""

    _attr_name = None
    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.TV
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )
    _attr_source_list = ["HDMI 1", "HDMI 2", "HDMI 3"]

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        super().__init__(entry, infrared_entity_id, unique_id_suffix="media_player")
        self._attr_state = MediaPlayerState.ON
        self._attr_is_volume_muted = False

    async def async_turn_on(self) -> None:
        """Turn on the projector."""
        await self._send_command(AetherionCode.POWER)

    async def async_turn_off(self) -> None:
        """Turn off the projector."""
        await self._send_command(AetherionCode.POWER)

    async def async_volume_up(self) -> None:
        """Volume up."""
        await self._send_command(AetherionCode.VOLUME_UP)

    async def async_volume_down(self) -> None:
        """Volume down."""
        await self._send_command(AetherionCode.VOLUME_DOWN)

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute/unmute (toggle)."""
        await self._send_command(AetherionCode.MUTE)
        self._attr_is_volume_muted = not self._attr_is_volume_muted
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        """Cycle source input."""
        await self._send_command(AetherionCode.INPUT_SOURCE)
        self._attr_source = source
        self.async_write_ha_state()
