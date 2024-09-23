from geysermc import GeyserMC

api = GeyserMC()

res = api.get_recent_uploads()
for i in res:
    print(i)
