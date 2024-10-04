import instaloader
import discord
import asyncio
import nest_asyncio
import instaloader
from datetime import datetime, timedelta

def get_latest_instagram_posts(username):
    """
    Renvoie un json des 10 derniers posts d'instagram de username
    """
    L = instaloader.Instaloader()

    profile = instaloader.Profile.from_username(L.context, username)

    # Récupérer les derniers posts
    posts = []
    for post in profile.get_posts():
        # Récupérer l'URL du post, la date et la description
        post_info = {
            "urlpost": f"https://www.instagram.com/p/{post.shortcode}/",
            "urlphoto": post.url,
            "date": post.date_utc,  # Date de publication
            "description": post.caption  # Description du post
        }
        posts.append(post_info)

        if len(posts) >= 10:
            break
    return posts


nest_asyncio.apply()

TOKEN = os.getenv('TOCKEN_BOT_DISCORD_INSTAGRAM')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

@client.event
async def on_ready():
    """
    Fonction qui envoie un embed pour chaque post publié par cfa_ensup_lr dans les dernières 24 heures vers le salon CHANNEL_ID.
    """
    print(f'Logged in as {client.user}')

    CHANNEL_ID = 1201173528221864116 
    channel = client.get_channel(CHANNEL_ID)
    current_time = datetime.utcnow()

    # Récupérer les derniers posts Instagram
    posts = get_latest_instagram_posts('cfa_ensup_lr')

    # Envoyer les posts Instagram sur Discord
    for post in posts:
        if (current_time - post['date']).total_seconds() < 3600 and post["description"] is not None:
            titre =  post['description'].split('\n')[0].upper().strip("[]")

            embed = discord.Embed(
                title= titre,
                description= post['description'][len(post['description'].split('\n')[0]):],
                color=0x1E90FF,
                url=post['urlpost']
            )
            embed.set_image(url=post['urlphoto'])
            datet = post['date'].strftime("%d/%m/%Y %H:%M")
            embed.set_footer(text=f"cfa_ensup_lr | instagram.com • {datet}")

            await channel.send(embed=embed)
            
    await client.close() 

client.run(TOKEN)
