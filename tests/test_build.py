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
def test_build(project):
    api = GeyserMC()
    print(api.get_build(project))
