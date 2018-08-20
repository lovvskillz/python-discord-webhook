from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

url = "https://discordapp.com/api/webhooks/481039345244045312/7dyFoOcdbJcAUfscBp58fCWnNJxdb0JmlSuIoCU_iI_yuQgVsJ0avST2sbg7fHv-BwDD"
webhook = DiscordWebhook(url=url)

embed = DiscordEmbed()
embed.title = "Embed Title"
embed.description = "Your Embed Description"
embed.color = 242424
embed.set_author(name='Author Name', url='https://github.com/lovvskillz', icon_url='https://avatars0.githubusercontent.com/u/14542790')
embed.set_footer(text='Embed Footer Text')
embed.set_timestamp()
embed.add_embed_field(name='Field 1', value='Lorem ipsum')
embed.add_embed_field(name='Field 2', value='dolor sit')
embed.add_embed_field(name='Field 3', value='amet consetetur')
embed.add_embed_field(name='Field 4', value='sadipscing elitr')

# create embed object for webhook
embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

# add embed object to webhook
webhook.add_embed(embed)

# webhook.add_embed(embed)
with open("C:/Users/vadim/Pictures/gitti.jpg", "rb") as f:
    pass
    # webhook.add_file(file=f.read(), filename='example.jpg')
webhook.execute()
