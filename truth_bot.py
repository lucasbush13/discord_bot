import os
import requests
import json
import discord
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from PIL import Image 
from io import BytesIO

discord_secret = os.environ['discord_key']
bg_secret = os.environ['bg_key']

client = discord.Client()
client = commands.Bot(command_prefix = '!')

def remove_bg(url,api_key):
  response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    data={
        'image_url': url,
        'size': 'auto'
    },
    headers={'X-Api-Key': api_key},
  ) 
  if response.status_code == requests.codes.ok:
    return response
  else:
      print('Error:', response.status_code, response.text)
  
def resize_image(filepath):
  base_width = 300
  img = Image.open(filepath)
  wpercent = (basewidth/float(img.size[0]))
  hsize = int((float(img.size[1])*float(wpercent)))
  img = img.resize((basewidth,hsize), Image.ANTIALIAS)
  os.remove(filepath)
  img.save(filepath)

@client.event
async def on_ready():
  print('bot logged in as {}..... ready'.format(client.user.display_name))

@client.command()
async def bg(image):
  attachment_url = str(image.message.attachments[0].url)
  api_key = os.getenv('bg_key')
  response = remove_bg(attachment_url, api_key)
  file_location = '/home/runner/LatestLightsalmonParser/'
  file_name = 'no-bg.png'
  with open(file_name, 'wb') as out:
    out.write(response.content)
  
  embed = discord.Embed()
  embed.set_image(url = 'attachment://no-bg.png')

  file = discord.File(file_location + file_name, filename=file_name)
  await image.send(file=file, embed=embed)

  # resize = resize_image(str(file_location + file_name))

client.run(os.getenv('discord_key'))
