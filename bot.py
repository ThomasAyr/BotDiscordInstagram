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
    # Créer une instance d'Instaloader
    L = instaloader.Instaloader()

    # Charger le profil public Instagram
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


# Appliquer le patch pour permettre d'exécuter asyncio.run() dans Jupyter
nest_asyncio.apply()

TOKEN = ${{ secrets.TOCKEN_BOT_DISCORD_INSTAGRAM }}
CHANNEL_ID = 1201173528221864116 

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
    print(f'Logged in as {client.user}')
    
    # Obtenir le canal Discord où envoyer les messages
    channel = client.get_channel(CHANNEL_ID)

    while True:
        # Obtenir l'heure actuelle en UTC
        current_time = datetime.utcnow()  # Obtenir l'heure actuelle UTC
        next_run_time = current_time.replace(minute=5, second=0, microsecond=0) + timedelta(hours=1)

        print("Démarrage dans",(next_run_time - current_time).total_seconds())

        # Attendre jusqu'au prochain lancement
        await asyncio.sleep((next_run_time - current_time).total_seconds())

        print("Démarrage")

        # Récupérer les derniers posts Instagram
        username = 'cfa_ensup_lr'
        posts = get_latest_instagram_posts(username)

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

# Lancer le bot Discord
client.run(TOKEN)
