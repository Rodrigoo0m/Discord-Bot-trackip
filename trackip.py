import discord
import requests

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

active_channels = {}

@client.event
async def on_ready():
    print(f'Bot logado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?track'):
        if message.author.id in active_channels:
            await message.channel.send(f"{message.author.mention}, você já tem um canal ativo para Lookup de IP.")
            return

        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await message.guild.create_text_channel(f'trackip - {message.author.name}', overwrites=overwrites)
        active_channels[message.author.id] = channel.id
        await channel.send(f"{message.author.mention} Por favor, envie o IP que deseja rastrear.")

    elif message.channel.id in active_channels.values():
        try:
            ip_address = message.content.strip()
            ip_info = requests.get(f'http://ip-api.com/json/{ip_address}').json()
            if ip_info['status'] == 'success':
                response = (f"IP: {ip_info['query']}\n"
                            f"Cidade: {ip_info['city']}\n"
                            f"Região: {ip_info['regionName']}\n"
                            f"País: {ip_info['country']}\n"
                            f"Provedor: {ip_info['isp']}\n"
                            f"Latitude: {ip_info.get('lat', 'Em desenvolvimento!')}\n"
                            f"Longitude: {ip_info.get('lon', 'Em desenvolvimento!')}\n"
                           )
            else:
                response = "IP inválido ou erro na busca."
        except Exception as e:
            response = f"Erro ao processar o comando. Erro: {e}"

        await message.author.send(response)
        await message.channel.delete()
        del active_channels[message.author.id]

client.run('MTE4ODE5NTc0NzAwNzU2OTk1MQ.GahjEs.iFN56b-gnjEADgU5xu3ybFi3LMnAmO_TcPN8Nc')
