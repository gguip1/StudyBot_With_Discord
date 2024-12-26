import discord
from datetime import timedelta

def create_study_embed(start_time, elapsed_seconds=0, username="Unknown"):
    """
    공부 시간 임베드를 생성하는 함수.
    
    :param start_time: 시작 시간 (datetime 객체)
    :param elapsed_seconds: 경과 시간 (초)
    :return: discord.Embed 객체
    """
    elapsed_time = str(timedelta(seconds=elapsed_seconds))
    embed = discord.Embed(
        title="🎓 공부 시간 측정 중!",
        description=f"{username} 님이 열심히 공부 중입니다. 아래에서 진행 상황을 확인하세요! 👇",
        color=discord.Color.blue(),
    )
    embed.add_field(name="⏳ 경과 시간", value=f"{elapsed_time}", inline=False)
    embed.add_field(name="📅 시작 시간", value=start_time.strftime("%Y-%m-%d %H:%M:%S (UTC)"), inline=False)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2907/2907277.png")
    embed.set_footer(
        text="공부를 멈추지 마세요! 🚀",
        icon_url="https://cdn-icons-png.flaticon.com/512/891/891399.png",
    )
    embed.set_author(
        name="Study Bot",
        icon_url="https://cdn-icons-png.flaticon.com/512/891/891399.png",
    )
    return embed
