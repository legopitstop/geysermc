from geysermc import GeyserMC

api = GeyserMC()

with open('geyser-spigot.jar', 'wb') as fd:
    data = api.get_download('geyser', 'spigot')
    fd.write(data)