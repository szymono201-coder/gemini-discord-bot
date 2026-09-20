import os
import discord
from discord.ext import commands
from google import genai

# Grab tokens securely from the cloud host environment
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini Client
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize Discord Bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in successfully as {bot.user}")

@bot.command(name="ai")
async def ask_gemini(ctx, *, prompt: str):
    """Triggers when a user types !ai [prompt]"""
    async with ctx.typing():
        try:
            # Generate content using the recommended general model
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            answer = response.text
            if len(answer) > 2000:
                answer = answer[:1990] + "..."

            await ctx.reply(answer)

        except Exception as e:
            await ctx.reply("Sorry, I ran into an error generating that response.")
            print(f"Error: {e}")

bot.run(DISCORD_TOKEN)
