from geysermc import GeyserMC
import pytest


@pytest.mark.parametrize(
    "project",
    [
        ("floodgate"),
        ("geyser"),
        ("erosion"),
        ("geyserconnect"),
        ("geyseroptionalpack"),
        ("hydraulic"),
        ("geyserpreview"),
        ("thirdpartycosmetics"),
        ("hurricane"),
    ],
)
def test_version(project):
    api = GeyserMC()

    print(api.get_version(project))
