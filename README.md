# AWOL Vision Aetherion Max Infrared for Home Assistant

[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Control an **AWOL Vision Aetherion Max** (Google TV projector) over infrared
using Home Assistant's native [infrared entity platform](https://www.home-assistant.io/integrations/infrared/) (HA 2026.4+).

The integration sends raw IR commands through any configured infrared emitter,
giving you a **media player** entity, a **remote** entity, and **17 button**
entities for every key on the stock AWOL remote.

## Requirements

| Requirement | Version |
|---|---|
| Home Assistant | 2026.4 or later |
| Infrared emitter | Any entity on the `infrared` platform |

Your emitter device must expose an `infrared` entity in Home Assistant
(e.g. ESPHome IR proxy, Broadlink RM Max custom integration).

## Installation

### HACS (recommended)

1. Open **HACS &rarr; Integrations &rarr; ⋮ &rarr; Custom repositories**
2. Add `https://github.com/amasolov/ha-awol-aetherion-ir` as an **Integration**
3. Search for **AWOL Vision Aetherion Max Infrared** and click **Download**
4. Restart Home Assistant

### Manual

Copy `custom_components/awol_aetherion_ir/` into your Home Assistant
`config/custom_components/` directory and restart.

## Setup

1. Go to **Settings &rarr; Devices & Services &rarr; Add Integration**
2. Search for **AWOL Vision Aetherion Max Infrared**
3. Select the infrared emitter entity that can reach your projector
4. Done — a device with media player, remote, and button entities appears

## Entities

### Media Player

| Feature | Action |
|---|---|
| Turn on / off | Sends power toggle |
| Volume up / down | Sends volume IR commands |
| Mute | Toggles mute |
| Select source | Cycles HDMI input |

### Remote

Supports `remote.send_command` with any of the following command names:

`power`, `ai`, `mute`, `input_source`, `profile`, `google_assistant`,
`settings`, `up`, `down`, `left`, `right`, `ok`, `back`, `home`,
`live_guide`, `live_tv`, `menu`, `volume_up`, `volume_down`,
`youtube`, `netflix`, `prime_video`, `disney_plus`

### Buttons

| Button | Remote key |
|---|---|
| Power | Power toggle |
| AI | AI picture mode |
| Mute | Mute toggle |
| Input Source | HDMI input cycle |
| Profile | User profile |
| Google Assistant | Voice assistant |
| Settings | Settings menu |
| OK | Confirm/Select |
| Back | Navigate back |
| Home | Home screen |
| Live Guide | TV guide |
| Live TV | Live TV |
| Menu | Options menu |
| YouTube | Launch YouTube |
| Netflix | Launch Netflix |
| Prime Video | Launch Prime Video |
| Disney+ | Launch Disney+ |

## IR Codes

Codes were learned from the stock AWOL Vision Aetherion Max remote using a
Broadlink RM Max. They are stored as base64-encoded Broadlink IR packets and
converted to raw microsecond timings at runtime.

## License

MIT
