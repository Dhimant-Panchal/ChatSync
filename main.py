import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import requests,urllib3

urllib3.disable_warnings()

load_dotenv()

token: str= os.getenv("DISCORD_TOKEN")
apilink: str=str(os.getenv("CLINK")) + "/v1/chat/completions"
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

headers = {
    "Content-Type": "application/json"
}

history = []

@client.event
async def on_ready():
    print("Bot is ready and running")

def getresponse(message: str)->str:
    history.append({"role": "user", "content": message})
    data = {
        "mode": "chat",
        "character": "HeliXAI",
        "messages": history
    }
    try:
        response = requests.post(apilink,headers=headers,json=data,verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except Exception as e:
        return "Some error occoured:\n" + str(e)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty because of an intent fault")
        return
    
    try:
        async with message.channel.typing():
            response: str = getresponse(user_message)
        await message.channel.send(response)
    except Exception as ex:
        try:
            await message.channel.send(ex)
            print(ex)
        except Exception as ex2:
            [print(ex2)]

@client.event
async def on_message(message: Message)->None:
    if message.author == client.user:
        return

    user_message: str = message.content
    await send_message(message,user_message)
    
client.run(token)