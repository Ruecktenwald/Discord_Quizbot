import discord 
import requests
import json
import asyncio
import logging
logging.basicConfig(level=logging.INFO)

#figure it out - logging

client = discord.Client()
logging.info("Starting discord client")
logging.info("Starting Discord Client...")
answer = False

def get_question():
    qs = ''
    id = 1
    answer = 0
    response = requests.get("https://https://young-ocean-22684.herokuapp.com//api/random/")
    json_data = response.json()
    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
      qs += str(id) + ". " + item['answer'] + "\n"

      if item['is_correct']:
        answer = id

      id += 1

    return qs, answer

@client.event
async def on_message(message):
    global answer
    debug = dict(
        message = message.content,
        message_type = type(message.content),
        answer = answer,
        answer_type = type(answer)
      )
    logging.info(debug)

    if message.author == client.user:
      logging.info("message.author == client.user")
      return

    if message.content.startswith("$q"):
      logging.info("message.content.startswith('$q')")
      qs,answer = get_question()
      await message.channel.send(qs)

      def check(m):
        return m.author == message.author and m.content.isdigit()

      try:
        guess = await client.wait_for('message', check=check, timeout=5)
      except asyncio.TimeoutError:
        return await message.channel.send("Sorry you took too long.")

      if int(guess.content) == answer:
        await message.channel.send("You're right!")
      else:
        await message.channel.send("Oops. That's not correct.")



    # if message.content.isnumeric() and message.content == str(answer):
    #   # logging.info('answer', message.content)
    #   logging.info('You are correct!')
    # elif message.content.isnumeric():
    #   logging.info('Nope')
      

client.run('MTAwNTc3NTYzMzQ1ODE1MTQ0NQ.GLYlO5.sRLuya1p3UKEXjiB2u3hmw3SHO3gAv2f3YVlaA')
