from geysermc import GeyserMC

api = GeyserMC()

xuid = api.get_xuid("legopitstop")
skin = api.get_skin(xuid)
image = api.get_raw_texture(skin.texture_id)
image.show()
