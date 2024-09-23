from geysermc import GeyserMC


def test_recent_uploads():
    api = GeyserMC()
    res = api.get_recent_uploads()
    for i in res:
        print(i)
