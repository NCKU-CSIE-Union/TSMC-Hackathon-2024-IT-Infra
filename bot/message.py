import discord
from feedback import create_thread
from datetime import datetime


async def send_embedded_message(channel,info:dict):
    # 創建一個 Embed 對象
    embed = discord.Embed(
        title = info["severity"],
        description=info["message"],
        color=0xF31CC8
    )
    
    # 設置 timestamp
    timestamp_format = "%a %b %d %Y %H:%M:%S"
    parsed_timestamp = datetime.strptime(info["timestamp"], timestamp_format)
    embed.timestamp = parsed_timestamp
    
    # 設置腳註
    embed.set_footer(text=f"{info["severity"]} Message by your system buddy")
    
    # 發送訊息
    message = await channel.send(embed=embed)

    # 創建討論串
    await create_thread(message)

    # 添加欄位
    # embed.add_field(
    #     name="Suggestion1: Auto Scale \n",
    #     value="Hi There! Have you receive my warning?",
    #     inline=False,
    # )
    # embed.add_field(
    #     name="Suggestion2: Give up the system \n",
    #     value="There's nothing we can do bruh",
    #     inline=False,
    # )



# async def send_embedded_error(channel):
#     # 創建一個 Embed 對象
#     embed = discord.Embed(
#         title="ERROR",
#         description="We encounter a Network Error!!!",
#         color=discord.Color.red(),
#     )

#     # 添加欄位
#     embed.add_field(
#         name="Suggestion1: Go get 張鴈光's help \n",
#         value="He's the man in charge of CSIE wifi, but the wifi is always suck : (",
#         inline=False,
#     )
#     embed.add_field(
#         name="Suggestion2: Give up the system \n",
#         value="There's nothing we can do bruh",
#         inline=False,
#     )

#     # 設置腳註
#     embed.set_footer(text="Error Message by your system buddy")

#     await channel.send(embed=embed)
    
#     # 創建討論串
#     await create_thread(message)


# async def send_embedded_info(channel):
#     # 創建一個 Embed 對象
#     embed = discord.Embed(
#         title="Info", description="Hey! Here's some info", color=0x25F533
#     )

#     # 添加欄位
#     embed.add_field(
#         name="Info1: We're going to win the competition! \n",
#         value="We're the best!",
#         inline=False,
#     )
#     embed.add_field(
#         name="Info2: we're bringing ipad back! \n",
#         value="We're the best!!",
#         inline=False,
#     )

#     # 設置腳註
#     embed.set_footer(text="Info Message by your system buddy")

#     await channel.send(embed=embed)
