import discord
from feedback import create_thread
from datetime import datetime

async def send_embedded_message(channel:discord.channel, info:dict):
    """
    Sends an embedded message to a Discord channel based on the provided information.
    """
    
    # Determine embbeded color
    type = info["severity"]
    
    if type == "WARNING":
        embedded_color =  0xF31CC8
    elif type == "ERROR":
        embedded_color = discord.Color.red()
    else: 
        embedded_color = 0x25F533 # INFO
    
    # create an Embed obj
    embed = discord.Embed(
        title = info["severity"],
        description = info["message"],
        color = embedded_color
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
            adjustment_mess += f"- CPU has to be increased {cpu}.\n" if cpu > 0 else f"- CPU has to be decreased {cpu}.\n"
        if memory != 0:
            adjustment_mess += f"- Memory has to be increased {memory}M.\n" if memory > 0 else f"- Memory has to be decreased {memory}M.\n"
        if instance:
            adjustment_mess += f"- Instance has to be increased {instance}.\n" if instance > 0 else f"- Instance has to be decreased {instance}.\n"
            
        embed.add_field(
            name = "Adjustment",
            value = adjustment_mess,
            inline = False
        )
    # Send the message
    message = await channel.send(embed=embed)

    # Create a discussion thread
    await create_thread(message)
