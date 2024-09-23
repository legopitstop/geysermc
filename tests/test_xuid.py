from geysermc import GeyserMC


def test_xuid():
    api = GeyserMC()

    print(api.get_xuid("notch"))
