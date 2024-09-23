from geysermc import GeyserMC


def test_verify_online_link():
    api = GeyserMC()

    print(
        api.verify_online_link(
            bedrock=2535429120293563, java="3bbc39f8717b40ecaa1b69aaaa5811cb"
        )
    )
