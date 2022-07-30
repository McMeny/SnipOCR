import discord
from discord.ext import commands
import random
import asyncio
import sqlite3
import discord.utils
import csv
from difflib import SequenceMatcher
from datetime import date
import calendar

bot = commands.Bot(command_prefix = '!')

con = sqlite3.connect('q_a.db')
cur = con.cursor()

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle,
    activity = discord.Game('Say !startquiz to start a quiz!'))
    print('Bot flashcards_test is operational!')

@bot.command()
async def setup(ctx):
    await ctx.send(embed = discord.Embed(title = 'Bot set up', description = 'To set up the Flashcards bot, please manually give it administrative permissions, and from there the bot is ready to go! To create new quiz channels please use the command ``!startquiz`` and to give feedback use ``!feedback``.', color = discord.Color.blue()))

@bot.command()
async def importing(ctx):
    await ctx.send(embed = discord.Embed(title = 'Format for importing csv files', description = 'CSV files should be formatted like the following:\n ```Question,Answer\nHow old am I?,18 years old\nWhat is newtons second law?,Force is equal to the rate of change of momentum```\n**NOTE:** Question and answers must not contain commas, or else the quizzing will not work.', color = discord.Color.blue()))

@bot.command()
async def startquiz(ctx):
    role_srch = discord.utils.get(ctx.guild.roles, name = 'quiz permission')
    if role_srch == None:
        role = await ctx.guild.create_role(name = 'quiz permission', permissions = discord.Permissions.none())
#this is a coroutine; with the use of 'async', it can be executed and stopped at any time. Pause coroutines using 'await'
    #variables (int)
    count = 0
    count += 1
    score = 0
    #lists
    y_response = [ 'Lets go!',
    'Your killing it!',
    'Well done!',
    'Correct!',
    'Your great at this!',
    'Sheesh!',
    'Woah! Great answer!']
    #variables (str)
    #code
    cat_srch = discord.utils.get(ctx.guild.categories, name = 'Quizzes')
    if cat_srch == None:
        category = await ctx.guild.create_category(name = 'Quizzes')
        my_channel = await category.create_text_channel(name = f'Quiz {ctx.author}', overwrites = None, reason = None)
    else:
        new_channel_name = f'Quiz {ctx.author}'
        my_channel = await cat_srch.create_text_channel(new_channel_name)
    perms = my_channel.overwrites_for(ctx.guild.default_role)
    perms.attach_files = True
    await my_channel.set_permissions(ctx.guild.default_role, overwrite = perms)
    await ctx.send(f' Hello {ctx.author} A new channel called Quiz {ctx.author} was created for you!')
    await my_channel.send(embed = discord.Embed(title = 'Welcome to the quiz channel!', description = 'Here you will be able to put in questions and answers easily so you can ``quiz yourself on them for your revision.`` Please type ``y`` to continue, or ``n`` to stop the bot.', color = discord.Color.green()))
    try:
        message = await bot.wait_for('message', check = lambda message: message.author.id == ctx.author.id and message.channel.id == my_channel.id, timeout = 500)
    except asyncio.TimeoutError:
        await ctx.author.remove_roles(role_srch)
        await my_channel.delete()
        return
    if message.content.lower() not in ('y','n'):
        await my_channel.send(embed = discord.Embed(title = 'Error!', description = 'Text is unrecognizable, start your message with `y` or `n`!', color = discord.Color.orange()))
        message = await bot.wait_for('message', check = lambda message: message.author.id == ctx.author.id and message.channel.id == my_channel.id, timeout = None)
        if message.content.lower() in ('y'):
            pass
        if message.content.lower() in ('n'):
            await ctx.author.remove_roles(role_srch)
            await my_channel.delete()
    if message.content.lower() == 'n':
        await ctx.author.remove_roles(role_srch)
        await my_channel.delete()
    if message.content.lower() == 'y':
        await my_channel.send(embed = discord.Embed(title = 'Group or individual revision?', description = 'For a group session, type ``group``, for an individual session type ``myself``.', color = discord.Color.green()))
        message = await bot.wait_for('message', check = lambda message: message.author.id == ctx.author.id and message.channel.id == my_channel.id, timeout = None)
        if message.content.lower() not in ('group','myself'):
            await my_channel.send(embed = discord.Embed(title = 'Error!', description = 'Text is unrecognizable, start your message with ``group`` or ``myself``!', color = discord.Color.orange()))
            message = await bot.wait_for('message', check = lambda message: message.author.id == ctx.author.id and message.channel.id == my_channel.id, timeout = None)
        if message.content.lower() == 'group':
            reg_user = []
            rct_msg = await my_channel.send(embed = discord.Embed(title = 'React to emote', description = 'React to the emote to register.\n To register non-present users, start with ``reg:`` and put in their ID. When finished, type ``registration complete``.', color = discord.Color.green()))
            await rct_msg.add_reaction('👍')
            @bot.event
            async def on_raw_reaction_add(payload):
                message_id = rct_msg.id
                if message_id == payload.message_id:
                    member = payload.member
                    global guild
                    emoji = payload.emoji.name
                    if emoji == '👍':
                        member_id = member.id
                        member_id = str(member_id)
                        registered = reg_user.append(member_id)
                        await member.add_roles(role_srch)
                        reaction = await bot.wait_for('reaction_add', check = registered, timeout = None)
                        if '881081223533977630' in reg_user:
                            reg_user.remove('881081223533977630')
            message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
            if message.content.lower() == 'registration complete':
                everyone = my_channel.overwrites_for(ctx.guild.default_role)
                everyone.send_messages = False
                await my_channel.set_permissions(ctx.guild.default_role, overwrite = everyone)
                selected_role = discord.utils.get(ctx.guild.roles, name = 'quiz permission')
                role_overwrite = my_channel.overwrites_for(selected_role)
                role_overwrite.send_messages = True
                await my_channel.set_permissions(selected_role, overwrite = role_overwrite)
                await my_channel.send('All users registered!')
            if message.content.startswith('reg:'):
                while True:
                    m = message.content
                    reg = m.split()
                    reg = reg[1:]
                    reg = ' '.join(reg)
                    reg = str(reg)
                    print(reg)
                    reg_user.append(f'{reg}')
                    await my_channel.send('foriegn user registered')
                    message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                    if message.content.lower() == 'registration complete':
                        print(reg_user)
                        break
        if message.content.lower() == 'myself':
            reg_user = []
            reg_user.append(f'{message.author.id}')
            everyone = my_channel.overwrites_for(ctx.guild.default_role)
            everyone.send_messages = False
            await my_channel.set_permissions(ctx.guild.default_role, overwrite = everyone)
            selected_role = discord.utils.get(ctx.guild.roles, name = 'quiz permission')
            role_overwrite = my_channel.overwrites_for(selected_role)
            role_overwrite.send_messages = True
            await my_channel.set_permissions(selected_role, overwrite = role_overwrite)
            await ctx.author.add_roles(role_srch)
            print('most wont be able to speak anymore')
            pass
        print(reg_user)
        await my_channel.send(embed = discord.Embed(title = 'CSV import shortcut', description = 'Would you like to import a csv file?\n To import please start with ``import:`` and upload the ``.csv`` file as an attachment.\n', color = discord.Color.green()))
        message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
        if message.content.startswith('import:'):
            file_name = message.attachments[0].filename
            print(file_name)
            messageattachment = await message.attachments[0].read()
            if len(messageattachment) <= 0:
                await my_channel.send(embed = discord.Embed(title = 'Error', description = 'File is empty', color = discord.Color.orange()))
            for attachment in messageattachment:
                #filtering
                if file_name.endswith('.csv'):
                    ex_save = await message.attachments[0].save(file_name)
                    print('true')
                    await my_channel.purge()
                    await my_channel.send(embed = discord.Embed(title = 'Import successful!', description = 'The quiz is starting!', color = discord.Color.green()))
                    with open(file_name, 'r') as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        score = 0
                        _id = 0
                        for line in csv_reader:
                            _id += 1
                            print(line)
                            answer = str(line['Answer'])
                            rq = await my_channel.send(embed = discord.Embed(title = 'Quizzing..', description = line['Question'], color = discord.Color.green()))
                            message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                            user_msg = message.content
                            us = user_msg.casefold()
                            a = answer.casefold()
                            # lambda x ignores spaces, compares the user_msg variable with the arow variable and asseses its similarity
                            sq = SequenceMatcher(lambda x: x == ' ', us, a).ratio()
                            if sq < 0.6:
                                score += 0
                                await my_channel.send(embed = discord.Embed(title = 'Incorrect!', description = 'Answer: ' + str(answer), color = discord.Color.green()))
                            if sq >= 0.6:
                                score += 1
                                await my_channel.send(embed = discord.Embed(title = 'Correct!', description = f'{random.choice(y_response)}', color = discord.Color.green()))
                        s_response = [ f'Sheesh! You got: {score}/{_id}!',
                        f'Wow! Great job for getting {score}/{_id}!',
                        f'Im amazed! You got: {score}/{_id}!',
                        f'Sheesh! Your bare smart arent you? You got {score}/{_id}.']
                        if line not in csv_reader:
                            await my_channel.send(embed = discord.Embed(title = 'Your score is..', description = f'{random.choice(s_response)}', color = discord.Color.green()))
                            try:
                                await my_channel.send(embed = discord.Embed(title = 'You are done!', description = 'The quiz channel is now finished, you may now close the channel by typing ``n``.\n To re-quiz yourself, please open a new quiz channel and repeat the same process.', color = discord.Color.green()))
                                message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = 200)
                            except asyncio.TimeoutError:
                                await ctx.author.remove_roles(role_srch)
                                await my_channel.delete()
                                return
                            if message.content == 'n':
                                await ctx.author.remove_roles(role_srch)
                                await my_channel.delete()
                                return
                else:
                    await my_channel.send(embed = discord.Embed(title = 'ERROR', description = 'UNRECOGNIZED FILE DETECTED! REPORTING...', color = discord.Color.red()))
                    await ctx.author.remove_roles(role_srch)
                    cr_table = '''CREATE TABLE IF NOT EXISTS
                    flagged(id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT);'''
                    cur.execute(cr_table)
                    flagged_user = f'{message.author}'
                    cur.execute('INSERT INTO flagged VALUES (NULL, ?)', (flagged_user,))
                    con.commit()
                    print(f'USER {flagged_user} FLAGGED UP!')
                    message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                    return
        else:
            await my_channel.send(embed = discord.Embed(title = 'Entering questions and answers', description = '``Please enter your questions and answers that you want to revise.`` To enter a question, start with ``Q:``. To enter an answer for the question, start with ``A:``.', color = discord.Color.green()))
            message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
            while True:
                acount = 0
                qcount = 0
                anum = 0
                if message.content.startswith('Q:'):
                # to add the question
                    user_id = message.author.id
                    print(user_id)
                    qcount += 1
                    res = message.content
                    que = res.split()
                    global ques
                    ques = que[1:]
                    ques = ' '.join(ques)
                    tb_n = f'_{message.channel.id}'
                    command1 = f'''CREATE TABLE IF NOT EXISTS
                    {tb_n}(id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT NOT NULL, Question TEXT, Answer TEXT);'''
                    cur.execute(command1)
                    print(ques)
                    print(f'Question append {qcount}: success')
                    await my_channel.send(embed = discord.Embed(title = 'Entering the answer for your question', description = 'Now, please type in the answer for the question start with ``A:``', color = discord.Color.green()))
                    message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                else:
                    await my_channel.send(embed = discord.Embed(title = 'Error!', description = 'Text is unrecognizable, start your message with ``Q:`` to enter questions!\nstart your message with ``A:`` to enter answers!', color = discord.Color.orange()))
                    message = await bot.wait_for('message', check = lambda message: message.author.id == ctx.author.id and message.channel.id == my_channel.id, timeout = None)
                if message.content.startswith('A:'):
                # to add the answer to the question
                    tb_n = f'_{message.channel.id}'
                    acount += 1
                    resp = message.content
                    ans = resp.split()
                    answ = ans[1:]
                    answ = ' '.join(answ)
                    user = f'{message.author}'
                    cur.execute(f'INSERT INTO {tb_n} VALUES (NULL, ?, ?, ?)', (user, ques, answ))
                    con.commit()
                    print(answ)
                    print(f'Answer append {acount}: success')
                    await my_channel.send(embed = discord.Embed(title = 'Questions and Answers registered!', description = 'You may repeat this as many times as you like. If you are finished, please type ``done``.', color = discord.Color.green()))
                    message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                    print('SUCCESS!')
                if message.content.lower() == 'done':
                    await my_channel.purge()
                    cur.execute(f'SELECT Question, Answer FROM {tb_n} ORDER BY RANDOM() LIMIT 1;')
                    tb_n = f'_{message.channel.id}'
                    id = 0
                    score = 0
                    await my_channel.send(embed = discord.Embed(title = 'Starting..', description = 'The quiz is starting!', color = discord.Color.green()))
                    while True:
                        id += 1
                        cur.execute(f'SELECT Question, Answer FROM {tb_n} WHERE id = ?', (id,))
                        row = cur.fetchone()
                        try:
                            row = list(row)
                            print(row)
                            qrow = row[0]
                            print(qrow)
                            arow = row[1]
                            print(arow)
                            await my_channel.send(embed = discord.Embed(title = 'Quizzing..', description = f'Question {id}: ' + str(qrow), color = discord.Color.green()))
                        except:
                            # calculating actual total score
                            _id = id - 1
                            percentage = int(score/_id)
                            if percentage > 0:
                                s_response = [ f'Sheesh! You got: {score}/{_id}!',
                                f'Wow! Great job for getting {score}/{_id}!',
                                f'Im amazed! You got: {score}/{_id}!',
                                f'Sheesh! Your bare smart arent you? You got {score}/{_id}.']
                                await my_channel.send(embed = discord.Embed(title = 'Your score is..', description = f'{random.choice(s_response)}', color = discord.Color.green()))
                            if percentage == 0:
                                await my_channel.send(embed = discord.Embed(title = 'Your score is...', description = f'Your score is: {score}/{_id}', color = discord.Color.green()))
                            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            try:
                                await my_channel.send(embed = discord.Embed(title = 'You are done!', description = 'The quiz channel is now finished, you may now close the channel by typing ``n``, or if you would like to try again please type ``try again``.', color = discord.Color.green()))
                                message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = 200)
                            except asyncio.TimeoutError:
                                await ctx.author.remove_roles(role_srch)
                                await my_channel.delete()
                                return
                            if message.content.lower() == 'n':
                                await ctx.author.remove_roles(role_srch)
                                await my_channel.delete()
                            if message.content.lower() == 'try again':
                                await my_channel.purge()
                                #rebooting the quiz
                                await my_channel.send(embed = discord.Embed(title = 'Rebooting!', description = 'The Quiz is restarting!', color = discord.Color.green()))
                                tb_n = f'_{message.channel.id}'
                                id = 0
                                score = 0
                                while True:
                                    id += 1
                                    cur.execute(f'SELECT Question, Answer FROM {tb_n} WHERE id = ?', (id,))
                                    row = cur.fetchone()
                                    try:
                                        row = list(row)
                                        print('Re test:', row)
                                        qrow = row[0]
                                        print('Re test:', qrow)
                                        arow = row[1]
                                        print('Re test:', arow)
                                        await my_channel.send(embed = discord.Embed(title = 'Quizzing..', description = f'Question {id}: ' + str(qrow), color = discord.Color.green()))
                                        break
                                        message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                                    except:
                                        await my_channel.send('Error')
                                        message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                            else:
                                message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                        # end of except block
                        # verification of questions to check if they are right or wrong
                        message = await bot.wait_for('message', check = lambda message: str(message.author.id) in reg_user and message.channel.id == my_channel.id, timeout = None)
                        user_msg = message.content
                        us = user_msg.casefold()
                        a = arow.casefold()
                        # lambda x ignores spaces, compares the user_msg variable with the arow variable and asseses its similarity
                        sq = SequenceMatcher(lambda x: x == ' ', us, a).ratio()
                        if sq < 0.6:
                            score += 0
                            await my_channel.send(embed = discord.Embed(title = 'Incorrect!', description = 'Answer: ' + str(arow), color = discord.Color.green()))
                        if sq >= 0.6:
                            score += 1
                            await my_channel.send(embed = discord.Embed(title = 'Correct!', description = f'{random.choice(y_response)}', color = discord.Color.green()))

@bot.command()
async def setreminders(ctx):
    await ctx.send(embed = discord.Embed(title = 'Set up your revision schedule.', description = 'Welcome to the reminders feature, a tool to enhance your revision technique by using active recall. Would you like to continue?'))
    msgg = await bot.wait_for('message', check = None, timeout = None)
    if msgg.content == 'YES' or 'yes':
        global user
        user = f'{msgg.author}'
        command3 = f'''CREATE TABLE IF NOT EXISTS
        revision(user TEXT, start_at NOT NULL, end_at NOT NULL, study_days TEXT);'''
        cur.execute(command3)
        await ctx.send(embed = discord.Embed(title = 'Setting up a time schedule', description = 'At what time would you like to start studying?'))
        msgg = await bot.wait_for('message', check = None, timeout = None)
        start_time = msgg.content
        await ctx.send(embed = discord.Embed(title = 'Setting up a time schedule', description = 'At what time would you like to end studying?'))
        msgg = await bot.wait_for('message', check = None, timeout = None)
        end_time = msgg.content
        await ctx.send(embed = discord.Embed(title = 'Setting up a time schedule', description = 'What days do you want to study?'))
        msgg = await bot.wait_for('message', check = None, timeout = None)
        global study_days
        study_days = msgg.content.upper()
        cur.execute(f'INSERT INTO revision VALUES (?, ?, ?, ?)', (user, start_time, end_time, study_days))
        await ctx.send(embed = discord.Embed(title = 'Setting up a time schedule', description = 'Set!'))
        con.commit()
        con.close()

#@bot.event
#async def on_ready():
#    cur.execute(f'SELECT user, start_at, end_at from revision_table WHERE study_days = ?', (study_days,))
#    row = cur.fetchone()
#    print(row)
#    cur_date = date.today()
#    curr_date = calendar.day_name[cur_date.weekday()]
#    con.close()
#    print(curr_date)


@bot.command()
async def feedback(ctx):
    await ctx.send('To provide feedback, please start your response with ``F:``.')
    msg = await bot.wait_for('message', check = None, timeout = None)
    if msg.content.startswith('F:'):
        command4 = '''CREATE TABLE IF NOT EXISTS
        feedback(id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT, Feedback TEXT);'''
        cur.execute(command4)
        f = msg.content
        feed = f.split()
        fb = feed[1:]
        fb = ' '.join(fb)
        fb = str(fb)
        user1 = f'{msg.author}'
        cur.execute('INSERT INTO feedback VALUES (NULL, ?, ?)', (user1, fb))
        print(fb)
        con.commit()
        await ctx.send(' Your response has been recorded. Thank you for giving us feedback!')
        print('NOTICE: Feedback recieved!')

@bot.command()
async def inv(ctx):
    await ctx.channel.send('Heres an invite to the flashcards server! https://discord.gg/ahpb74rbD2')
    print(f'{ctx.author} used the invite link!')

bot.run('ODgxMDgxMjIzNTMzOTc3NjMw.GU-rGo.rlN04RFOp9IUXa266weZQTio8sNaHQ5xRC1lD0')
