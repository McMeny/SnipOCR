import discord
from discord.ext import commands
import sqlite3
from googletrans import Translator

bot = commands.Bot(command_prefix = '?')

con = sqlite3.connect('lang_store.db')
cur = con.cursor()

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game('type ?change_to to set up the language you want to translate to!'))
    print('Translate bot is online!')

@bot.command()
async def change_to(ctx, text):
    authorized = []
    member = str(ctx.author)
    member = member.split('#')
    table_name = str(member[0])
    authorized.append(table_name)
    if table_name == 'flashcards_test':
        authorized.remove('flashcards_test')
    else:
        pass
    auth = authorized[0]
    create_table = f'''CREATE TABLE IF NOT EXISTS
    {auth}(id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT, Language TEXT);'''
    cur.execute(create_table)
    lang = str(text)
    user = f'{ctx.author}'
    cur.execute(f'INSERT INTO {auth} VALUES (NULL, ?, ?)', (user, lang))
    con.commit()
    #-------------------------------------------------------------------
    translator = Translator()
    detect = translator.detect(lang).lang
    cur.execute(f'SELECT Language FROM {table_name} ORDER BY id DESC')
    row = cur.fetchone()
    row = list(row)
    language = row[0]
    try:
        final_txt = translator.translate('Finished! To try another language, please use the ``?change_to`` command again. To do translations, type out ``T:``, then your message afterwards.\nFor example: ``T: How are you?``', src = detect, dest = language)
        await ctx.send(embed = discord.Embed(title = 'Finished!', description = final_txt.text, color = discord.Color.blue()))
    except Exception:
        await ctx.send(embed = discord.Embed(title = 'Error!', description = 'Error, unsupported language!', color = discord.Color.red()))

@bot.command()
async def languages(ctx):
    await ctx.send(embed = discord.Embed(title = 'Supported languages', description = '``Afrikaans: af\nAlbanian:	sq\nAmharic:	am\nArabic:	ar\nArmenian:	hy\nAzerbaijani:	az\nBasque:	eu\nBelarusian:	be\nBengali:	bn\nBosnian:	bs\nBulgarian:	bg\nCatalan:	ca\nCebuano:	ceb\nChinese (Simplified):	zh-CN or zh\nChinese (Traditional):	zh-TW\nCorsican:	co\nCroatian:	hr\nCzech:	cs\nDanish:	da\nDutch:	nl\nEnglish:	en\nEsperanto:	eo\nEstonian:	et\nFinnish:	fi\nFrench:	fr\nFrisian:	fy\nGalician:	gl\nGeorgian:	ka\nGerman:	de\nGreek:	el\nGujarati:	gu\nHaitianCreole:	ht\nHausa:'	'ha\nHawaiian:	haw\nHebrew:	he or iw\nHindi:	hi\nHmong:	hmn\nHungarian:	hu\nIcelandic:	is\nIgbo	ig\nIndonesian:	id\nIrish:	ga\nItalian:	it\nJapanese:	ja\nJavanese:	jv\nKannada:	kn\nKazakh:	kk\nKhmer:	km\nKinyarwanda:	rw\nKorean:	ko\nKurdish:	ku\nKyrgyz:	ky\nLao:	lo\nLatvian:	lv\nLithuanian:	lt\nLuxembourgish:	lb\nMacedonian:	mk\nMalagasy:	mg\nMalay:	ms\nMalayalam:	ml\nMaltese:	mt\nMaori:	mi\nMarathi:	mr\nMongolian:	mn\nMyanmar (Burmese):	my\nNepali:	ne\nNorwegian:'	'no\nNyanja (Chichewa):	ny\nOdia (Oriya):	or\nPashto:	ps\nPersian:	fa\nPolish:	pl\nPortuguese (Portugal\n Brazil):	pt\nPunjabi:	pa\nRomanian:	ro\nRussian:	ru\nSamoan:	sm\nScots Gaelic:	gd\nSerbian:	sr\n'
    'Sesotho:	st\nShona:	sn\nSindhi:	sd\nSinhala (Sinhalese):	si\nSlovak:	sk\nSlovenian:	sl\nSomali:	so\nSpanish:	es\nSundanese:	su\nSwahili:	sw\nSwedish:	sv\nTagalog (Filipino):	tl\nTajik:	tg\nTamil:	ta\nTatar:	tt\nTelugu:	te\nThai:	th\nTurkish:	tr\nTurkmen:	tk\nUkrainian:	uk\nUrdu:	ur\nUyghur:	ug\nUzbek:	uz\nVietnamese:	vi\nWelsh:	cy\nXhosa:	xh\nYiddish:	yi\nYoruba:	yo\nZulu:	zu``', color = discord.Color.blue()))

@bot.listen('on_message')
async def translation(message):
    if message.content.startswith('T:'):
        authorized = []
        member = str(message.author)
        member = member.split('#')
        table_name = str(member[0])
        authorized.append(table_name)
        if table_name == 'translator':
            authorized = None
        else:
            pass
        txt = str(message.content)
        txt = txt.split(':')
        primary_txt = txt[1]
        translator = Translator()
        detect = translator.detect(primary_txt).lang
        if authorized is not None:
            cur.execute(f'SELECT Language FROM {table_name} ORDER BY id DESC')
            row = cur.fetchone()
            row = list(row)
            print(row)
            language = row[0]
            print(language)
            final_txt = translator.translate(primary_txt, src = detect, dest = language)
            ctx = await bot.get_context(message)
            await ctx.send(final_txt.text)

bot.run('ODk5NjgyMzg1OTU4OTYxMjAz.YW2UhA.7KqXJzyMeLv34s_UZ4CHqZPPmZ8')
