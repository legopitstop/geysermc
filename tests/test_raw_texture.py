from geysermc import GeyserMC


def test_raw_texture():
    api = GeyserMC()

    api.get_raw_texture(
        "3d8ada082aa912d5a122cc226fd307ea05856192a9a4f7c5a3caaf875774742e"
    )
