import os
import urllib.request
import json
from pyrogram import Client, filters
from pyrogram.types import Message

# Get the API key and URL from environment variables
API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")

# Initialize the Pyrogram client
bot = Client(
    "instagram_downloader_bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

# Define the command handler
@bot.on_message(filters.command("ig", prefixes="."))
async def instagram(client: Client, message: Message):
    # Get the URL from the message text
    url = message.text.split(" ")[1]

    # Check if the URL is valid
    if not url.startswith("https://www.instagram.com"):
        await message.reply_text("Please provide a valid Instagram URL.")
        return

    # Make the API request to Xteam API
    api_request_url = f"{API_URL}?url={url}&APIKEY={API_KEY}"
    try:
        with urllib.request.urlopen(api_request_url) as response:
            response_json = response.read()
    except Exception as e:
        await message.reply_text("Error: " + str(e))
        return

    # Parse the API response
    response_dict = json.loads(response_json)
    if not response_dict.get("status", False):
        await message.reply_text("The URL you provided is invalid.")
        return

    # Download the image/video
    media_url = response_dict["result"]["data"][0]["data"]
    file_extension = "." + response_dict["result"]["data"][0]["type"]
    file_name = "instagram" + file_extension
    urllib.request.urlretrieve(media_url, file_name)

    # Send the image/video
    caption = (
        f'<b>Username:</b> {response_dict["result"]["username"]}\n'
        f'<b>Link:</b> https://instagram.com/{response_dict["result"]["username"]}\n'
        f'<b>Caption:</b> {response_dict["result"]["caption"]}'
    )
    if file_extension == ".mp4":
        await message.reply_video(video=file_name, caption=caption, parse_mode="HTML")
    else:
        await message.reply_photo(photo=file_name, caption=caption, parse_mode="HTML")

    # Delete the downloaded file
    os.remove(file_name)

# Start the bot
bot.run()
