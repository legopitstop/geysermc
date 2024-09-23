from geysermc import GeyserMC


def test_gamertag_batch():
    api = GeyserMC()
    print(api.get_gamertag_batch(2535429120293563))
