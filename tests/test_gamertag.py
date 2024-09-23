from geysermc import GeyserMC


def test_gamertag():
    api = GeyserMC()
    print(api.get_gamertag(2535453759792258))
