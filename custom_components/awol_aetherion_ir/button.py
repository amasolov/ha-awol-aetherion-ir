"""Button platform for AWOL Vision Aetherion Max IR integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_INFRARED_ENTITY_ID
from .entity import AetherionIrEntity
from .ir_codes import AetherionCode

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class AetherionButtonDescription(ButtonEntityDescription):
    """Describes an Aetherion IR button entity."""

    command_code: AetherionCode


BUTTON_DESCRIPTIONS: tuple[AetherionButtonDescription, ...] = (
    AetherionButtonDescription(
        key="power",
        name="Power",
        command_code=AetherionCode.POWER,
    ),
    AetherionButtonDescription(
        key="ai",
        name="AI",
        command_code=AetherionCode.AI,
    ),
    AetherionButtonDescription(
        key="mute",
        name="Mute",
        command_code=AetherionCode.MUTE,
    ),
    AetherionButtonDescription(
        key="input_source",
        name="Input Source",
        command_code=AetherionCode.INPUT_SOURCE,
    ),
    AetherionButtonDescription(
        key="profile",
        name="Profile",
        command_code=AetherionCode.PROFILE,
    ),
    AetherionButtonDescription(
        key="google_assistant",
        name="Google Assistant",
        command_code=AetherionCode.GOOGLE_ASSISTANT,
    ),
    AetherionButtonDescription(
        key="settings",
        name="Settings",
        command_code=AetherionCode.SETTINGS,
    ),
    AetherionButtonDescription(
        key="ok",
        name="OK",
        command_code=AetherionCode.OK,
    ),
    AetherionButtonDescription(
        key="back",
        name="Back",
        command_code=AetherionCode.BACK,
    ),
    AetherionButtonDescription(
        key="home",
        name="Home",
        command_code=AetherionCode.HOME,
    ),
    AetherionButtonDescription(
        key="live_guide",
        name="Live Guide",
        command_code=AetherionCode.LIVE_GUIDE,
    ),
    AetherionButtonDescription(
        key="live_tv",
        name="Live TV",
        command_code=AetherionCode.LIVE_TV,
    ),
    AetherionButtonDescription(
        key="menu",
        name="Menu",
        command_code=AetherionCode.MENU,
    ),
    AetherionButtonDescription(
        key="youtube",
        name="YouTube",
        command_code=AetherionCode.YOUTUBE,
    ),
    AetherionButtonDescription(
        key="netflix",
        name="Netflix",
        command_code=AetherionCode.NETFLIX,
    ),
    AetherionButtonDescription(
        key="prime_video",
        name="Prime Video",
        command_code=AetherionCode.PRIME_VIDEO,
    ),
    AetherionButtonDescription(
        key="disney_plus",
        name="Disney+",
        command_code=AetherionCode.DISNEY_PLUS,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up AWOL Aetherion IR buttons from config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    async_add_entities(
        AetherionButton(entry, infrared_entity_id, desc)
        for desc in BUTTON_DESCRIPTIONS
    )


class AetherionButton(AetherionIrEntity, ButtonEntity):
    """AWOL Aetherion IR button entity."""

    entity_description: AetherionButtonDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        description: AetherionButtonDescription,
    ) -> None:
        super().__init__(entry, infrared_entity_id, unique_id_suffix=description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button."""
        await self._send_command(self.entity_description.command_code)
