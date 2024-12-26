import discord
from discord.ext import commands, tasks

from utils.embed_utils import create_study_embed

import sqlite3

class VoiceUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("study_data.db")
        self.cursor = self.conn.cursor()
        self.active_sessions = {}
        self.update_embeds.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        server_id = member.guild.id
        
        self.cursor.execute("""
            SELECT channel_id
            FROM server_settings
            WHERE server_id = ?
        """, (server_id,))
        
        result = self.cursor.fetchone()

        if not result:
            return
        
        study_channel_id = result[0]

        if after.channel and after.channel.id == study_channel_id:
            
            if member.id in self.active_sessions:
                return
            
            embed = create_study_embed(discord.utils.utcnow(), username=member.display_name)
            
            message = await after.channel.send(embed=embed)
            
            self.active_sessions[member.id] = {
                "start_time": discord.utils.utcnow(),
                "message": message,
                "username": member.display_name
            }
            
            print(f"{member.name} joined the study channel.")

        elif before.channel and before.channel.id == study_channel_id:
            # 사용자가 공부 채널에서 나갔을 때
            if member.id in self.active_sessions:
                session = self.active_sessions.pop(member.id)

                # 최종 공부 시간 계산
                total_time = discord.utils.utcnow() - session["start_time"]
                elapsed_seconds = int(total_time.total_seconds())

                # 새 임베드 생성
                embed = create_study_embed(
                    start_time=session["start_time"],
                    elapsed_seconds=elapsed_seconds
                )
                embed.description = f"{member.display_name} 님의 공부가 종료되었습니다.\n총 공부 시간이 기록되었습니다."
                embed.color = discord.Color.red()  # 색상 변경: 종료 시 강조

                # 메시지 업데이트
                await session["message"].edit(embed=embed)

    
    @tasks.loop(seconds=1)  # 갱신 주기를 1초로 설정
    async def update_embeds(self):
        
        for user_id, session in list(self.active_sessions.items()):
            
            # 경과 시간 계산
            elapsed_time = (discord.utils.utcnow() - session["start_time"]).total_seconds()

            # 새 임베드 생성
            embed = create_study_embed(
                start_time=session["start_time"],
                elapsed_seconds=int(elapsed_time),
                username=session['username']
            )

            # 메시지 업데이트
            await session["message"].edit(embed=embed)
            
    @update_embeds.before_loop
    async def before_update_embeds(self):
        await self.bot.wait_until_ready() 

async def setup(bot):
    await bot.add_cog(VoiceUpdateEvent(bot))