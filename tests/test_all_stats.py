from geysermc import GeyserMC, Statistics

api = GeyserMC()

assert isinstance(api.get_all_stats(), Statistics)
