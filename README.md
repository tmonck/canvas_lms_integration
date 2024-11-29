# Integration Blueprint

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Integration to integrate with [canvas_lms_integration][canvas_lms_integration]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from blueprint API.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `canvas_lms`.
1. Download _all_ the files from the `custom_components/canvas_lms/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[canvas_lms_integration]: https://github.com/tmonck/canvas_lms_integration
[buymecoffee]: https://www.buymeacoffee.com/tmonck
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/tmonck/canvas_lms_integration.svg?style=for-the-badge
[commits]: https://github.com/tmonck/canvas_lms_integration/commits/main
[license-shield]: https://img.shields.io/github/license/tmonck/canvas_lms_integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Tom%20Monck%20%40tmonck-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/tmonck/canvas_lms_integration.svg?style=for-the-badge
[releases]: https://github.com/tmonck/canvas_lms_integration/releases
