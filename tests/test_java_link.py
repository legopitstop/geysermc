from geysermc import GeyserMC


def test_java_link():
    api = GeyserMC()
    print(api.get_java_link("3bbc39f8717b40ecaa1b69aaaa5811cb"))
