"""Base entity for AWOL Vision Aetherion Max IR integration."""

from __future__ import annotations

import logging

from homeassistant.components.infrared import async_send_command
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN
from .ir_codes import AetherionCode, AetherionCommand

_LOGGER = logging.getLogger(__name__)


class AetherionIrEntity(Entity):
    """AWOL Vision Aetherion Max IR base entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        unique_id_suffix: str,
    ) -> None:
        self._infrared_entity_id = infrared_entity_id
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="AWOL Vision Aetherion Max",
            manufacturer="AWOL Vision",
            model="Aetherion Max",
        )

    async def async_added_to_hass(self) -> None:
        """Track infrared emitter availability."""
        await super().async_added_to_hass()

        @callback
        def _async_ir_state_changed(event: Event[EventStateChangedData]) -> None:
            new_state = event.data["new_state"]
            ir_available = (
                new_state is not None and new_state.state != STATE_UNAVAILABLE
            )
            if ir_available != self.available:
                self._attr_available = ir_available
                self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._infrared_entity_id], _async_ir_state_changed
            )
        )

        ir_state = self.hass.states.get(self._infrared_entity_id)
        self._attr_available = (
            ir_state is not None and ir_state.state != STATE_UNAVAILABLE
        )

    async def _send_command(self, code: AetherionCode) -> None:
        """Send an IR command through the selected emitter."""
        await async_send_command(
            self.hass,
            self._infrared_entity_id,
            AetherionCommand(code),
            context=self._context,
        )
