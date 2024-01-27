from bot.bot import DiscordBot


def test_discord_bot(discord_bot: DiscordBot) -> None:
    bot = discord_bot
    assert bot is not None


async def test_discord_bot_update_active_threads(discord_bot: DiscordBot) -> None:
    bot = discord_bot
    await bot.update_active_threads()
    assert bot.active_threads is not None


async def test_discord_bot_on_ready(discord_bot: DiscordBot) -> None:
    bot = discord_bot
    await bot.on_ready()
    assert bot.client.user is not None


async def test_discord_bot_on_message(discord_bot: DiscordBot) -> None:
    bot = discord_bot
    await bot.on_message()
    assert True


async def test_discord_bot_process_feedback(discord_bot: DiscordBot) -> None:
    bot = discord_bot
    await bot.process_feedback()
    assert True


async def test_discord_bot_send_alert(discord_bot: DiscordBot) -> None:
    bot = discord_bot
    await bot.send_alert()
    assert True
