from geysermc import GeyserMC
import mojang

api1 = GeyserMC()
api2 = mojang.API()

xuid = api1.get_xuid("legopitstop")
uuid = api2.get_uuid("legopitstop")
print(xuid, uuid)
print(api1.verify_online_link(bedrock=xuid, java=uuid))
