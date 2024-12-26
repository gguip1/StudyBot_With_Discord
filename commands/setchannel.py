import discord
from discord import app_commands
from discord.ext import commands

import sqlite3

class SetChannelCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("study_data.db")
        self.cursor = self.conn.cursor()

    @app_commands.command(name="setchannel", description="채널을 설정합니다.")
    async def set_channel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        server_id = interaction.guild.id
        channel_id = channel.id
        
        self.cursor.execute("""
            INSERT INTO server_settings (server_id, channel_id)
            VALUES (?, ?)
            ON CONFLICT(server_id) DO UPDATE SET channel_id=excluded.channel_id
        """, (server_id, channel_id))
        self.conn.commit()
        
        # 슬래시 명령어 응답
        await interaction.response.send_message(f"채널이 {channel.mention}으로 설정될 예정입니다.")

async def setup(bot):
    await bot.add_cog(SetChannelCommand(bot))
