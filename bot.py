# Name: Calvin Ip
# Date: 01/07/2023
# Version 1.1
# Description: A Discord bot that uses the Chinese Social Credit Meme as its basis

import discord
from discord.ext import commands
import responses
import bot_functions
import sys
import random

STARTING_CREDITS = 1000


async def send_message(message, user_message, is_private: bool) -> None:
    """
    Handle Responses and sends messages

    """
    try:
        # Handle Responses
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_bot():
    # To get the token. Put the bot's token in a "token.txt" file
    file = open("token.txt", "r")
    TOKEN = file.read().strip()

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='sc!', intents=intents)

    @bot.event
    async def on_ready() -> None:
        """
        The code in this even is executed when the bot is ready
        """
        print(f'{bot.user} is now running!')


    @bot.event
    async def on_message(message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        # Ignores its own message to prevent an infinite loop :(
        if message.author == bot.user:
            return

        # Grabs information on the message and its author
        username = message.author
        user_message = message.content
        user_id = message.author.id
        channel = message.channel

        # Debugging
        print(f'{username} said: "{user_message}" (Channel: {channel})')

        # Block of Code for Chatting
        # for private messaging
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        # send to the server
        else:
            await send_message(message, user_message, is_private=False)

        # Shutdown
        if user_message == '!shutdown':
            await message.channel.send("Shutting down!")
            sys.exit   
        
        # Needs this line for commands to work in conjunction with on_message
        await bot.process_commands(message)


    @bot.command()
    async def test(ctx, arg):
        """
        test command
        """
        await ctx.send(arg)

        # if bot_functions.has_role(ctx.message.author.roles, "Xi's Council") or ctx.message.author.guild_permissions.administrator:
        #     print("he has roles")
        # else:
        #     print("he does not have roles")


    @bot.command(aliases=['checkcredits', 'checkcredit', 'checkcred', 'checkcreds'])
    async def check_credits(ctx):
        """
        Returns the Social Credits of the user

        sc!checkcredits
        >>> <@{user_id}> You have <#user social creds> Social credits
        """
        user_id = ctx.message.author.id
        user_credit = bot_functions.get_credits(user_id)

        await ctx.message.channel.send(f"<@{user_id}> You have " + str(user_credit) + " Social Credits")
    

    @bot.command(aliases=['checkothers', 'checkother'])
    async def check_credits_other(ctx, member: commands.MemberConverter):
        """
        Returns the Social Credits of another user

        sc!checkothers <@userid>
        >>> <@{user_id}> Has <#user social creds> Social credits
        """
        user_id = member.id
        user_credit = bot_functions.get_credits(user_id)

        await ctx.message.channel.send(f"<@{user_id}> Has " + str(user_credit) + " Social Credits")

    
    @bot.command(aliases=['p'])
    async def praise(ctx):
        """
        Praise another user via a message reply and reward them with social credits
        """
        user_id = ctx.message.author.id
        
        if ctx.message.reference is None:
            await ctx.message.channel.send("Error! Praise another user by replying to a message and saying \"sc!praise\"")
        else:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            praised_id = message.author.id
            reward_creds = 5    # Can be changed as needed

            if user_id == praised_id:
                await ctx.message.channel.send("Why are you praising yourself?")
            else:
                new_credit = bot_functions.add_credits(praised_id, int(reward_creds)) 

                await ctx.message.channel.send(f"<@{praised_id}> gained " + str(reward_creds) + " credits! New: " + str(new_credit))


    @bot.command(aliases=['con', 'c'])
    async def condemn(ctx):
        """
        Condemn another user via a message reply and take away their social credits
        """
        user_id = ctx.message.author.id
        
        if ctx.message.reference is None:
            await ctx.message.channel.send("Error! Condemn another user by replying to a message and saying \"sc!condemn\"")
        else:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            praised_id = message.author.id
            sub_creds = 15    # Can be changed as needed

            if user_id == praised_id:
                await ctx.message.channel.send("Why are you condemning yourself?")
            else:
                new_credit = bot_functions.remove_credits(praised_id, int(sub_creds)) 

                await ctx.message.channel.send(f"<@{praised_id}> lost " + str(sub_creds) + " credits! New: " + str(new_credit))


    # Below are admin commands 
    # If the user does not have admin or the specified role, the will lose social credits
    @bot.command(aliases=['addcredit', 'addcredits', 'addcred', 'addcreds'])
    async def add_credits(ctx, member: commands.MemberConverter, num_creds):
        """
        Adds and returns the credit adjustment of a user

        sc!checkother <@userid> 
        >>> <@{user_id}> Has 1000 Social credits
        sc!addcredit <@userid> 10
        >>> <@{user_id}> gained credits! New: 1010
        """
        if bot_functions.has_role(ctx.message.author.roles, "Xi's Council") or ctx.message.author.guild_permissions.administrator:
            # User has either the role or admin privileges
            user_id = member.id
            new_credit = bot_functions.add_credits(user_id, int(num_creds)) 

            await ctx.message.channel.send(f"<@{user_id}> gained " + str(num_creds) + " credits! New: " + str(new_credit))

        else:
            # User does not have perms
            num_creds = random.randint(10,20)    # Values can be adjusted as needed
            citizen_id = ctx.message.author.id
            new_credit = bot_functions.remove_credits(citizen_id, int(num_creds))

            await ctx.message.channel.send(f"<@{citizen_id}> you should have not used an admin command. You lost " + str(num_creds) + " credits! New: " + str(new_credit))


    @bot.command(aliases=['subcredit', 'subcredits', 'subcred', 'subcreds'])
    async def subtract_credits(ctx, member: commands.MemberConverter, num_creds):
        """
        Subtracts and returns the credit adjustment of a user

        sc!checkother <@userid> 
        >>> <@{user_id}> Has 1000 Social credits
        sc!subcredit <@userid> 10
        >>> <@{user_id}> lost credits! New: 990
        """
        if bot_functions.has_role(ctx.message.author.roles, "Xi's Council") or ctx.message.author.guild_permissions.administrator:
            # User has either the role or admin privileges
            user_id = member.id
            new_credit = bot_functions.remove_credits(user_id, int(num_creds)) 

            await ctx.message.channel.send(f"<@{user_id}> lost " + str(num_creds) + " credits! New: " + str(new_credit))

        else:
            # User does not have perms
            num_creds = random.randint(10,20)    # Values can be adjusted as needed
            citizen_id = ctx.message.author.id
            new_credit = bot_functions.remove_credits(citizen_id, int(num_creds))

            await ctx.message.channel.send(f"<@{citizen_id}> you should have not used an admin command. You lost " + str(num_creds) + " credits! New: " + str(new_credit))

        
    @bot.command(aliases=['setcredit', 'setcredits', 'setcred', 'setcreds'])
    async def set_credits(ctx, member: commands.MemberConverter, num_creds):
        """
        Hard Sets and returns the credit adjustment of a user

        sc!checkother <@userid> 
        >>> <@{user_id}> Has 1000 Social credits
        sc!setcredit <@userid> 1500
        >>> <@{user_id}> credits are set! New: 1500
        """
        if bot_functions.has_role(ctx.message.author.roles, "Xi's Council") or ctx.message.author.guild_permissions.administrator:
            # User has either the role or admin privileges
            user_id = member.id
            new_credit = bot_functions.set_credits(user_id, int(num_creds)) 

            await ctx.message.channel.send(f"<@{user_id}> credits are set to: " + str(new_credit))

        else:
            # User does not have perms
            num_creds = random.randint(10,20)    # Values can be adjusted as needed
            citizen_id = ctx.message.author.id
            new_credit = bot_functions.remove_credits(citizen_id, int(num_creds))

            await ctx.message.channel.send(f"<@{citizen_id}> you should have not used an admin command. You lost " + str(num_creds) + " credits! New: " + str(new_credit))

    
    @bot.command(aliases=['reset'])
    async def reset_creds(ctx, member: commands.MemberConverter):
        """
        Resets the social credit to default value (of 1000) and returns the credit adjustment of a user.
        Prints differently depending if the user lost or gained credits

        sc!checkother <@userid> 
        >>> <@{user_id}> Has 5 Social credits
        sc!reset <@userid>
        >>> <@{user_id}> has been blessed by the great leader! New: 1000
        """
        if bot_functions.has_role(ctx.message.author.roles, "Xi's Council") or ctx.message.author.guild_permissions.administrator:
            # User has either the role or admin privileges
            user_id = member.id
            old_cred_amount = bot_functions.get_credits(user_id)
            new_credit = bot_functions.set_credits(user_id, STARTING_CREDITS) 

            # Prints differently depending if the target user lost or gained credits
            if old_cred_amount <= new_credit:
                await ctx.message.channel.send(f"<@{user_id}> has been blessed by the great leader! Social Credits reset to: " + str(new_credit))
            else:
                await ctx.message.channel.send(f"<@{user_id}> has been condemned by the great leader! Social Credits reset to: " + str(new_credit))

        else:
            # User does not have perms
            num_creds = random.randint(10,20)    # Values can be adjusted as needed
            citizen_id = ctx.message.author.id
            new_credit = bot_functions.remove_credits(citizen_id, int(num_creds))

            await ctx.message.channel.send(f"<@{citizen_id}> you should have not used an admin command. You lost " + str(num_creds) + " credits! New: " + str(new_credit))


    @bot.event
    async def on_command_error(ctx, error):
        """
        Error Handling
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.channel.send("I don't understand what you mean by \"" + str(ctx.message.content) + "\"")
            

    # Run the bot!!!!
    bot.run(TOKEN)
