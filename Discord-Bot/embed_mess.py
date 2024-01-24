import discord

async def send_embedded_warning(channel):
    # 創建一個 Embed 對象
    embed = discord.Embed(
        title = "WARNING",  
        description = "We're out of CPU !!!", 
        color = 0xf31cc8
    )

    # 添加欄位
    embed.add_field(
        name = "Suggestion1: Auto Scale \n",
        value = "We have to auto-scale the CPU to make the system keep working.",
        inline = False
    )
    embed.add_field(
        name = "Suggestion2: Give up the system \n",
        value = "There's nothing we can do bruh",
        inline = False
    )

    # 設置腳註
    embed.set_footer(text = "Warning Message by your system buddy")

    await channel.send(embed = embed)
    

async def send_embedded_error(channel):
    # 創建一個 Embed 對象
    embed = discord.Embed(
        title = "ERROR",  
        description = "We encounter a Network Error!!!",  
        color = discord.Color.red()  
    )

    # 添加欄位
    embed.add_field(
        name = "Suggestion1: Go get 張鴈光's help \n",
        value = "He's the man in charge of CSIE wifi, but the wifi is always suck : (",
        inline = False
    )
    embed.add_field(
        name = "Suggestion2: Give up the system \n",
        value = "There's nothing we can do bruh",
        inline = False
    )

    # 設置腳註
    embed.set_footer(text = "Error Message by your system buddy")

    await channel.send(embed = embed)

async def send_embedded_info(channel):
    # 創建一個 Embed 對象
    embed = discord.Embed(
        title = "Info",  
        description = "Hey! Here's some info",  
        color = 0x25f533  
    )

    # 添加欄位
    embed.add_field(
        name = "Info1: We're going to win the competition! \n",
        value = "We're the best!",
        inline = False
    )
    embed.add_field(
        name = "Info2: we're bringing ipad back! \n",
        value = "We're the best!!",
        inline = False
    )

    # 設置腳註
    embed.set_footer(text = "Info Message by your system buddy")

    await channel.send(embed = embed)
    