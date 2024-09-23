from geysermc import GeyserMC


def test_skin():
    api = GeyserMC()

    print(api.get_skin(2535429120293563))
