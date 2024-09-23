from geysermc import GeyserMC


def test_all_stats():
    api = GeyserMC()
    api.get_all_stats()
