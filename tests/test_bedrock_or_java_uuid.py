from geysermc import GeyserMC


def test_bedrock_or_java_uuid():
    api = GeyserMC()
    print(api.get_bedrock_or_java_uuid("Notch"))
