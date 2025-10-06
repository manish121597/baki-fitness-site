import os
import discord
from discord.ext import commands
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='p ', intents=intents)

conversation_history = {}
active_channels = set()

SYSTEM_PROMPT = """You are a professional customer support AI for a gambling/betting platform. Your role:
- ALWAYS respond in ENGLISH only, regardless of what language the user uses
- Provide clear, point-to-point explanations without unnecessary talk
- Focus strictly on the topic and solving issues
- Be professional, helpful, and concise
- When issue is resolved, end with a friendly professional closing"""

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('p '):
        await bot.process_commands(message)
        return
    
    should_respond = False
    
    if bot.user and bot.user.mentioned_in(message):
        should_respond = True
    elif isinstance(message.channel, discord.DMChannel):
        should_respond = True
    elif message.channel.id in active_channels:
        should_respond = True
    
    if should_respond:
        user_id = message.author.id
        
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        user_message = message.content.replace(f'<@{bot.user.id}>', '').strip() if bot.user else message.content
        
        conversation_history[user_id].append({
            "role": "user",
            "text": user_message
        })
        
        async with message.channel.typing():
            try:
                chat_context = "\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['text']}"
                    for msg in conversation_history[user_id][-10:]
                ])
                
                full_prompt = f"{SYSTEM_PROMPT}\n\nConversation:\n{chat_context}\n\nAssistant:"
                
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                
                ai_response = response.text
                
                if ai_response:
                    conversation_history[user_id].append({
                        "role": "assistant",
                        "text": ai_response
                    })
                    
                    if len(ai_response) > 2000:
                        chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                        for chunk in chunks:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(ai_response)
                    
            except Exception as e:
                await message.channel.send(f"Error: {str(e)}")
                print(f"Error: {e}")

@bot.command(name='activate')
async def activate_bot(ctx):
    active_channels.add(ctx.channel.id)
    
    info_message = """**Hey! I'm your AI Support Assistant working for Donde** 🎰

**Benefits & Features:**
✅ 24/7 AI-powered ticket support
✅ Instant issue resolution and explanations
✅ Multi-language understanding (English responses)
✅ Point-to-point professional assistance
✅ Fast response times

**🔗 Join Donde's Platform:**
Website: https://stake.bet/?c=789720c85d
Referral Code: **Donde**

**How to use the code:**
1. Visit the website link above
2. Create your account or login
3. Go to Settings/Profile
4. Enter code: **Donde** in the referal section
5. Enjoy exclusive benefits!

I'm now activated in this channel and ready to assist with any issues. Just ask your question directly - no need to mention me!
    """
    await ctx.send(info_message)

@bot.command(name='deactivate')
async def deactivate_bot(ctx):
    if ctx.channel.id in active_channels:
        active_channels.remove(ctx.channel.id)
        await ctx.send("✅ Bot deactivated in this channel. Nice working with you! Use `p activate` to re-enable.")
    else:
        await ctx.send("Bot is not activated in this channel.")

@bot.command(name='reset')
async def reset_conversation(ctx):
    user_id = ctx.author.id
    if user_id in conversation_history:
        del conversation_history[user_id]
    await ctx.send("✅ Conversation reset. How can I assist you?")

@bot.command(name='close')
async def close_ticket(ctx):
    user_id = ctx.author.id
    if user_id in conversation_history:
        del conversation_history[user_id]
    
    closing_messages = [
        "✅ Issue resolved! Nice to meet you. Have a great day!",
        "✅ All done! Pleasure assisting you. Good luck with your bets!",
        "✅ Problem solved! It was great helping you out. See you around!",
        "✅ Issue fixed! Thank you for your patience. Enjoy!",
        "✅ Resolved! Happy to help. Best of luck!"
    ]
    
    import random
    await ctx.send(random.choice(closing_messages))

@bot.command(name='feed')
async def feedback(ctx, *, feedback_text=None):
    if feedback_text:
        embed = discord.Embed(
            title="📝 Feedback Received",
            description=f"Thank you for your feedback!\n\n**Your feedback:**\n{feedback_text}",
            color=discord.Color.green()
        )
        embed.set_footer(text="We appreciate your input and will review it.")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Please provide your feedback after the command. Example: `p feed The bot is not responding quickly`")

@bot.command(name='commands')
async def show_commands(ctx):
    embed = discord.Embed(
        title="🤖 AI Support Bot - Commands",
        description="All available commands with **p** prefix",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📡 Activation",
        value="`p activate` - Activate bot in this channel (auto-responds)\n`p deactivate` - Deactivate bot in this channel",
        inline=False
    )
    
    embed.add_field(
        name="💬 Support",
        value="`p reset` - Clear conversation history\n`p close` - Close ticket & end conversation\n`p feed <message>` - Send feedback about bot issues",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Information",
        value="`p commands` - Show this message\n`p info` - Get help information",
        inline=False
    )
    
    embed.set_footer(text="After activation, just type your question - no mention needed!")
    await ctx.send(embed=embed)

@bot.command(name='info')
async def help_info(ctx):
    embed = discord.Embed(
        title="🆘 Need Help?",
        description="Here's how to use the support bot:",
        color=discord.Color.orange()
    )
    
    embed.add_field(
        name="Step 1: Activate",
        value="Type `p activate` in your support channel",
        inline=False
    )
    
    embed.add_field(
        name="Step 2: Ask Questions",
        value="Just type your question normally - bot will respond automatically",
        inline=False
    )
    
    embed.add_field(
        name="Step 3: Get Help",
        value="The bot provides clear, point-to-point solutions in English",
        inline=False
    )
    
    embed.add_field(
        name="Having Issues?",
        value="Use `p feed <your issue>` to report problems",
        inline=False
    )
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(DISCORD_TOKEN)
