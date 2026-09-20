import os
import threading
import discord
from discord.ext import commands
from google import genai
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- Mini serwer WWW dla platformy Render ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Web server started on port {port}")
    server.serve_forever()

# Uruchomienie serwera WWW w osobnym wątku, żeby nie blokował bota
threading.Thread(target=run_web_server, daemon=True).start()
# ---------------------------------------------

# Pobieranie kluczy
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Inicjalizacja Gemini
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Inicjalizacja Discorda
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in successfully as {bot.user}")

@bot.command(name="ai")
async def ask_gemini(ctx, *, prompt: str):
    async with ctx.typing():
        try:
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
