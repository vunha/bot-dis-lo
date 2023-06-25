import discord
from discord.ext import commands,tasks
from tabulate import tabulate
import json
import requests
import traceback
import os.path
import urllib3
import re
import asyncio
import datetime
import youtube_dl
from pytube import YouTube
from googletrans import Translator
from gtts import gTTS
urllib3.disable_warnings()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

players_file = "players.json" 
# Địa chỉ IP và cổng của máy chủ FiveM
server_ip = '103.249.70.30'
server_port = '30120'
def is_allowed_channel():
    async def predicate(ctx):
        allowed_channel_ids = [id các kênh dis cách nhau dấu ,]  # Thêm các ID kênh vào danh sách này
        return ctx.channel.id in allowed_channel_ids

    return commands.check(predicate)
async def update_players_data():
    while True:
        try:
            # Tạo URL để gửi yêu cầu GET đến API của máy chủ
            url = f'http://{server_ip}:{server_port}/players.json'

            # Gửi yêu cầu GET đến máy chủ (không xác minh chứng chỉ SSL)
            response = requests.get(url, verify=False)

            # Kiểm tra mã trạng thái của phản hồi và xử lý dữ liệu
            if response.status_code == 200:
                data = response.json()

                # Lưu dữ liệu vào tệp JSON
                with open(players_file, 'w' ,encoding='utf-8') as file:
                    json.dump(data, file,ensure_ascii=False)
                print("Dữ liệu đã được cập nhật thành công trong tệp players.json.")
            else:
                print("Yêu cầu không thành công. Mã trạng thái:", response.status_code)
        except Exception as e:
            traceback.print_exc()

        await asyncio.sleep(10)  # Chờ 10 giây trước khi cập nhật lại dữ liệu

@bot.event
async def on_ready():
    print(f"Vô rồi nè bot : {bot.user}")
    live_status.start()
    # Tải dữ liệu và cập nhật lại mỗi 10 giây
    bot.loop.create_task(update_players_data())

       
@bot.command()
@is_allowed_channel()  # Kiểm tra kênh trước khi thực hiện lệnh
async def ping(ctx):
    await ctx.send('pong!')
@bot.command()
async def chat(ctx, *, message):
    await ctx.message.delete()  # Xóa tin nhắn của bạn

    # Gửi phản hồi
    await ctx.send(f"{message}")
@bot.command()
@is_allowed_channel()
async def ffa(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("No players found. Please use the `!update` command to fetch player information.")
        return

    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    player_info = []
    ffa_count = 0  # Số lượng người có từ khóa "FFA"
    player_count = 0  # Số thứ tự người chơi

    for player in players:
        player_name = player['name']
        if 'FFA' in player_name or 'ffa' in player_name:
            player_count += 1
            player_id = player['id']
            player_ping = player['ping']
            id_string = f"[ID: {player_id}]"
            formatted_name = f"{player_count}.\t{id_string}\t|\t{player_name}"

            if len(player_name) > 30:
                player_name = player_name[:30] + '...'

            player_info.append(formatted_name)

            if 'ffa' in player_name.lower():
                ffa_count += 1

    if player_info:
        embed = discord.Embed(title="FFA", description=f"Tổng Có: {player_count} người chơi FFA", color=0x00FF00)

        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("No players with 'FFA' found.")


@bot.command()
@is_allowed_channel()
async def tt(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("không có dữ liệu")
        return

    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    tt_count = 0  # Số lượng người có từ khóa "Titans"
    player_count = 0  # Số thứ tự người chơi
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    for player in players:
        player_name = player['name']
        if 'TiTans' in player_name or 'titans' in player_name:
            player_count += 1
            player_id = player['id']
            player_ping = player['ping']
            id_string = f"[ID: {player_id}]"
            formatted_name = f"{player_count}.\t{id_string}\t|\t{player_name}"

            if len(player_name) > 30:
                player_name = player_name[:30] + '...'

            player_info.append(formatted_name)

            if 'titans' in player_name.lower():
                tt_count += 1

    if player_info:
        embed = discord.Embed(title="Kí Sinh Trùng", description=f"Tổng Có: {player_count} người chơi Titans", color=0x00FF00)

        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("không có titan.")


@bot.command()
@is_allowed_channel()
async def prd(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("No players found. Please use the `!update` command to fetch player information.")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    prd_count = 0  # Số lượng người có từ khóa "Paradise"
    player_count = 0  # Số thứ tự người chơi

    for player in players:
        player_name = player['name']
        if 'Paradise' in player_name or 'paradise' in player_name:
            player_count += 1
            player_id = player['id']
            player_ping = player['ping']
            id_string = f"[ID: {player_id}]"
            formatted_name = f"{player_count}.\t{id_string}\t|\t{player_name}"

            if len(player_name) > 30:
                player_name = player_name[:30] + '...'

            player_info.append(formatted_name)

            if 'paradise' in player_name.lower():
                prd_count += 1

    if player_info:
        embed = discord.Embed(title="Para Đần", description=f"Tổng Có: {prd_count} thằng Paradise Đần", color=0x00FF00)

        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Para Dan deo ai on ca")

@bot.command()
@is_allowed_channel()
async def whale(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("Lỗi file")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    whale_count = 0  # Số lượng người có từ khóa "Whale" hoặc "WL"
    player_count = 0  # Số thứ tự người chơi

    for player in players:
        player_name = player['name']
        if 'Whale |' in player_name or 'whale' in player_name or 'WL |' in player_name or 'wl' in player_name:
            player_count += 1
            player_id = player['id']
            player_ping = player['ping']
            id_string = f"[ID: {player_id}]"
            formatted_name = f"{player_count}.\t{id_string}\t|\t{player_name}"

            if len(player_name) > 30:
                player_name = player_name[:30] + '...'

            player_info.append(formatted_name)

            if 'whale' in player_name.lower() or 'wl' in player_name.lower():
                whale_count += 1

    if player_info:
        embed = discord.Embed(title="Danh sách Whale/WL", description=f"Tổng số: {whale_count} người", color=0x00FF00)

        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Không có ai chơi Whale/WL")

@bot.command()
@is_allowed_channel()
async def bb(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("No players found. Please use the `!update` command to fetch player information.")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    categories = {
        "CA + QY": ['CA', 'QY'],
        "Paradise": ['Paradise'],
        "LangBăm": ['LangBăm'],
        "Titans": ['Titans'],
        "NewChamp": ['NewChamp'],
        "AL-Qaeda": ['AL-Qaeda'],
        "SSO": ['SSO'],
        "Người Nước Ngoài" : ['Người Nước Ngoài'],
        "Ocean" : ['Ocean'],
        "Victory" :['Victory'],
        "Loser" : ['Loser'],
        "The Triads" : ['The Triads'],
        "Inferno" : ['Inferno'],
        "BlackHole" : ['BlackHole'],
        "Justice" : ['Justice']
    }

    # Sắp xếp danh mục theo số lượng người chơi từ nhiều đến ít
    sorted_categories = sorted(categories.items(), key=lambda x: -len([p for p in players if any(k.lower() in p['name'].lower() for k in x[1])]))

    lines = []
    for category, keywords in sorted_categories:
        count = 0
        for player in players:
            player_name = player['name']
            for keyword in keywords:
                if keyword.lower() in player_name.lower():
                    count += 1
                    break
        if count > 0:
            line = f"- Số Lượng **{category}**: {count}"  # Đặt chữ đậm cho phần tử category
            lines.append(line)
            lines.append("-----------------------------")

    result = "\n".join(lines)

    embed = discord.Embed(title="Thống kê người chơi", color=0x00FF00)

    embed.description = result
    embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
    await ctx.send(embed=embed)


@bot.command()
@is_allowed_channel()
async def sso(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("Lỗi file")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    sso_count = 0  # Số lượng người có từ khóa "SSO"
    player_count = 0  # Số thứ tự người chơi

    for player in players:
        player_name = player['name']
        if 'SSO' in player_name or 'sso' in player_name:
            player_count += 1
            player_id = player['id']
            player_ping = player['ping']
            id_string = f"[ID: {player_id}]"
            formatted_name = f"{player_count}.\t{id_string}\t|\t{player_name}"

            if len(player_name) > 30:
                player_name = player_name[:30] + '...'

            player_info.append(formatted_name)

            if 'sso' in player_name.lower():
                sso_count += 1

    if player_info:
        embed = discord.Embed(title="Danh sách SSO", description=f"Tổng số: {sso_count} người", color=0x00FF00)

        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Không có ai chơi SSO")
        
@bot.command()
@is_allowed_channel()
async def ca(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("lỗi file")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    ca_keywords = ['CA', 'QLCA', 'PGDCA', 'S.W.A.T', 'GDCA']
    ca_players = []
    player_count = 0

    for player in players:
        player_name = player['name']
        for keyword in ca_keywords:
            if keyword.lower() in player_name.lower():
                player_count += 1
                player_id = player['id']
                id_string = f"[{player_count}] \t [ID: {player_id}]\t"
                formatted_name = f"{id_string}\t|\t{player_name}"
                player_info.append(formatted_name)
                ca_players.append(player_name)
                break

    ca_count = len(ca_players)

    if player_info:
        embed = discord.Embed(title=f"Danh sách CA :\n Tổng số CA : {ca_count}", color=0x00FF00)
        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("deo co ca.")

@bot.command()
@is_allowed_channel()
async def caqy(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("lỗi file")
        return

    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    player_info = []
    caqy_keywords = ['CA', 'QLCA', 'PGDCA', 'S.W.A.T', 'GDCA', 'Quân Y', 'QLMED', 'PGDBS', 'GDBS']
    caqy_players = []
    player_count = 0

    for player in players:
        player_name = player['name']
        for keyword in caqy_keywords:
            if keyword.lower() in player_name.lower():
                player_count += 1
                player_id = player['id']
                id_string = f"[{player_count}] \t [ID: {player_id}]\t"
                formatted_name = f"{id_string}\t|\t{player_name}"
                player_info.append(formatted_name)
                caqy_players.append(player_name)
                break

    caqy_count = len(caqy_players)

    if player_info:
        embed = discord.Embed(title=f"Danh sách CA, QY :\n Tổng số CA, QY : {caqy_count}", color=0x00FF00)
        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Méo có ai")

@bot.command()
@is_allowed_channel()
async def ch(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("lỗi file")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    ch_keywords = ['CH |', 'GSCH |', 'PGDCH |', 'GDCH |']
    ch_players = []
    player_count = 0

    for player in players:
        player_name = player['name']
        for keyword in ch_keywords:
            if keyword.lower() in player_name.lower():
                player_count += 1
                player_id = player['id']
                id_string = f"[{player_count}] \t [ID: {player_id}]\t"
                formatted_name = f"{id_string}\t\t|\t\t{player_name}"
                player_info.append(formatted_name)
                ch_players.append(player_name)
                break

    ch_count = len(ch_players)

    if player_info:
        embed = discord.Embed(title=f"Danh sách CH \n Tổng số: {ch_count}", color=0x00FF00)
        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Không có ai")
        
@bot.command()
@is_allowed_channel()
async def med(ctx):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("Lỗi file")
        return
    current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
    footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"
    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    player_info = []
    med_keywords = ["MED |", "QLMED |", "PGDBS |", "GDBS |", "Quân Y |"]
    med_players = []
    player_count = 0

    for player in players:
        player_name = player['name']
        for keyword in med_keywords:
            if keyword.lower() in player_name.lower():
                player_count += 1
                player_id = player['id']
                id_string = f"[{player_count}] \t [ID: {player_id}]\t"
                formatted_name = f"{id_string}\t\t|\t\t{player_name}"
                player_info.append(formatted_name)
                med_players.append(player_name)
                break

    med_count = len(med_players)

    if player_info:
        embed = discord.Embed(title=f"Danh sách MED \n Tổng số: {med_count}", color=0x00FF00)
        value = '\n'.join(player_info)
        embed.add_field(name='\u200B', value=value, inline=False)
        embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Không có ai")
        
def count_players(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    total_players = sum(len(item['identifiers']) for item in data)
    return total_players
## Live Status
async def live_status(seconds=75):
    player_count = count_players("players.json")  # Thay thế get_player_count() bằng hàm để lấy số lượng người chơi
    activity = discord.Activity(type=discord.ActivityType.watching, name=f' Đang Chơi ACE :{player_count}/550')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)
def count_players(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    id_count = sum('id' in item for item in data)
    return id_count
@tasks.loop(seconds=50)
async def live_status(seconds=75):
    player_count = count_players('players.json')
    status = f'ACE: {player_count}/550'
    activity = discord.Activity(type=discord.ActivityType.playing, name=status)
    await bot.change_presence(activity=activity)
    await asyncio.sleep(seconds)


def convert_to_steam_id_64(steam_id_hex):
    steam_id_dec = int(steam_id_hex[6:], 16)
    steam_id_64 = steam_id_dec + 76561197960265728
    return str(steam_id_64)


#check idngười dùng
@bot.command()
@is_allowed_channel()
async def id(ctx, player_id):
    # Kiểm tra nếu tệp tin không tồn tại
    if not is_players_file_exist():
        await ctx.send("No players found. Please use the `!update` command to fetch player information.")
        return

    with open(players_file, 'r', encoding='utf-8') as file:
        players = json.load(file)

    # Tìm kiếm người chơi với ID khớp
    player_found = False
    for player_info in players:
        if str(player_info['id']) == player_id:
            player_found = True
            player_name = player_info['name']
            server_id = player_info.get('id', '')
            ping = player_info.get('ping', '')
            identifiers = player_info.get('identifiers', [])
            discord_username = player_info.get('discord', '')

            steam_id = None
            discord_id = None
            for identifier in identifiers:
                if identifier.startswith('steam:'):
                    steam_id = identifier.split(':')[1]
                elif identifier.startswith('discord:'):
                    discord_id = identifier.split(':')[1]

            steam_id_64 = convert_to_steam_id_64(steam_id) if steam_id else None
            steam_link = f"https://steamcommunity.com/profiles/{steam_id_64}" if steam_id_64 else "N/A"

            discord_mention = f"<@!{discord_id}>" if discord_id else "N/A"

            discord_user = await bot.fetch_user(int(discord_id)) if discord_id else None
            discord_username = discord_user.name if discord_user else "N/A"
            discord_discriminator = discord_user.discriminator if discord_user else "N/A"

            current_time = datetime.datetime.now().strftime("%H:%M")  # Lấy thời gian hiện tại
            footer_text = f"\tHi hi của tui đó hahaha . Ti Mê  :  {current_time}"

            # Tạo một Embed mới
            embed = discord.Embed(title="Thông tin người chơi", color=0x00FF00)
            embed.add_field(name='Tên Ingame:', value=player_name, inline=False)
            embed.add_field(name='Server ID:', value=server_id, inline=True)
            embed.add_field(name='Ping:', value=ping, inline=True)
            embed.add_field(name='Danh Tính:', value=f"Link Steam: {steam_link}\n\nDiscord: {discord_mention}\n\nTên Dis: {discord_username}#{discord_discriminator}", inline=False)
            embed.set_footer(text=footer_text)  # Thêm dòng chữ dưới cùng của Embed

            await ctx.send(embed=embed)
            break

    if not player_found:
        await ctx.send(f"Đéo thằng nào id : {player_id}")



# Tạo một từ điển để lưu số lượng người từng phòng
room_counts = {}

room_counts = {}  # Tạo từ điển để lưu thông tin số lượng người từng phòng

@bot.command()
async def keoroom(ctx):
    # Lấy thông tin về phòng hiện tại mà người dùng đang ngồi
    current_channel = ctx.author.voice.channel
    
    # Lấy danh sách các phòng voice trong server
    voice_channels = ctx.guild.voice_channels
    
    # Duyệt qua danh sách phòng voice và chuyển thành viên từ các phòng khác về phòng hiện tại
    for voice_channel in voice_channels:
        if voice_channel != current_channel:
            members = voice_channel.members
            for member in members:
                await member.move_to(current_channel)
                # Cập nhật thông tin số lượng người từng phòng
                if voice_channel.name in room_counts:
                    room_counts[voice_channel.name] += 1
                else:
                    room_counts[voice_channel.name] = 1
    
    # Gửi thông báo với số lượng người từng phòng (loại bỏ phòng người gửi lệnh đang ngồi)
    message = "Đã kéo người từ các phòng:\n"
    for room, count in room_counts.items():
        if room != current_channel.name:
            message += f"- {room}: {count} người\n"
    
    await ctx.send(message)

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Bạn phải tham gia một kênh thoại trước.")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(voice_channel)
    else:
        voice_client = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def play_song(file):
        voice_client.play(discord.FFmpegPCMAudio(file))

    def download_song(url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            file = f"{info['title']}.mp3"
            ydl.download([url])
            return file

    file = await asyncio.to_thread(download_song, url)
    await asyncio.to_thread(play_song, file)

@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()

@bot.command()
async def noi(ctx, *, message):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    tts = gTTS(message, lang='vi')  # Tạo âm thanh từ văn bản
    tts.save('tts.mp3')  # Lưu âm thanh thành tệp tts.mp3

    voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="tts.mp3"))
    await asyncio.sleep(5)  # Chờ cho đủ thời gian để bot nói
    await voice_client.disconnect()
def is_players_file_exist():
    return os.path.exists(players_file)
bot.run("token bot ")
