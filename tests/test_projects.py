from geysermc import GeyserMC


def test_projects():
    api = GeyserMC()
    print(api.get_projects())
