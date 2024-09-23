from geysermc import GeyserMC


def test_bedrock_link():
    api = GeyserMC()
    print(api.get_bedrock_link(2535429120293563))
