import geysermc
import mojang

api = mojang.API()

xuid = geysermc.get_xuid('legopitstop')
uuid = api.get_uuid('legopitstop')
print(xuid, uuid)
print(geysermc.verify_online_link(bedrock=xuid, java=uuid))
