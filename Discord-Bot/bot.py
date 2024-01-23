import discord
# 連結 Error_Notify
# 連接 Receive_Mess

# 權限設置
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    slash = await client.tree.sync()
    print("TSMC System Bot is Online!")
    print(f'Logged in as {client.user}')
    


    
client.run("MTE5OTI3MTYxMzM1OTczOTAxMA.GJN31L.rNSDr17bJ4cMPOsKeLd4jFdS45wZqVGcrDmo6k")