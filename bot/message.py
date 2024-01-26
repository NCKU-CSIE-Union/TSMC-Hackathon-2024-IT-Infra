from datetime import datetime

import discord


async def send_embedded_message(channel: discord.channel, info: dict):
    """
    Sends an embedded message to a Discord channel based on the provided information.
    """

    # Determine embbeded color
    type = info["severity"]

    if type == "WARNING":
        embedded_color = 0xF31CC8
    elif type == "ERROR":
        embedded_color = discord.Color.red()
    else:
        embedded_color = 0x25F533  # INFO

    # create an Embed obj
    embed = discord.Embed(
        title=info["severity"], description=info["message"], color=embedded_color
    )

    # Set the timestamp
    timestamp_format = "%Y-%m-%d %H:%M:%S%z"
    parsed_timestamp = datetime.strptime(info["timestamp"], timestamp_format)
    embed.timestamp = parsed_timestamp

    # Set the footer
    type = info["severity"]
    embed.set_footer(text=f"{type} Message by your system buddy")

    # Add a field if severity is "ERROR"
    if info["severity"] == "ERROR":
        cpu = info["cpu"]
        memory = info["memory"]
        instance = info["instance"]

        adjustment_mess = ""
        if cpu != 0:
            adjustment_mess += (
                f"- CPU has to be increased {cpu}.\n"
                if cpu > 0
                else f"- CPU has to be decreased {cpu}.\n"
            )
        if memory != 0:
            adjustment_mess += (
                f"- Memory has to be increased {memory}M.\n"
                if memory > 0
                else f"- Memory has to be decreased {memory}M.\n"
            )
        if instance != 0:
            adjustment_mess += (
                f"- Instance has to be increased {instance}.\n"
                if instance > 0
                else f"- Instance has to be decreased {instance}.\n"
            )

        embed.add_field(name="Adjustment", value=adjustment_mess, inline=False)
    # Send the message
    message = await channel.send(embed=embed)

    return message

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
