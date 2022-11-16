from time import time
from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid,ChannelPrivate, ChatIdInvalid, ChatInvalid
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from pyrogram.methods.utilities.idle import idle
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid,InviteHashExpired,UsernameInvalid,UserAlreadyParticipant
#
from progress import progressddl,progressub
from utils import get_filename_media
from cfg import *

"""===============Initializing the Bot================="""
userbot = Client("userbot", API_ID, API_HASH,bot_token=BOT_TOKEN,session_string=SESSION)
bot = Client("locobot", API_ID, API_HASH,bot_token=BOT_TOKEN)



"""=======Command Start======="""
@bot.on_message(filters.command('start') & filters.private)
async def hello(client, message):
    enlace_directo = [
            [InlineKeyboardButton(
                '⚙️Soporte',
                url=f'https://t.me/Wachu985'
            ),
            InlineKeyboardButton(
                '💻GITHUB',
                url=f'https://github.com/Wachu985/'
            ),
            ],
            [
                InlineKeyboardButton(
                    '🖥Support Channel',
                    url=f'https://t.me/IDMDescarga'
                )
            ]       
        ]
    reply_botton = InlineKeyboardMarkup(enlace_directo)
    await bot.send_message(message.chat.id,'✉️**Bienvenido al Bot '+message.chat.first_name+'**'+'\n\n__📱Enviame el Enlace de Invitacion del Grupo o Canal y luego Enviame el Enlace del Archivo📱__\n **📲Use el Comando /help para ver la Guia Basica de Uso**',reply_markup=reply_botton)

"""=================Help Command for the BOT================="""
@bot.on_message(filters.command('help') & filters.private)
async def help(client, message):
    text = '**🚸Guia Básica de Uso:\n\n Pasos: 👇**\n\n'
    text += '**1️⃣- ** __Enviar el Enlace del Grupo o Canal para Unirse__\n\n'
    text += '**2️⃣- ** __Enviar el Enlace del Archivo Restringido__\n\n'
    text += '**3️⃣- ** __Espere a que el Bot le Envie su Archivo y a Disfrutar__\n\n' 
    text += '**📲Cualquier Problema Contactar con Soporte**'
    enlace_directo = [
            [InlineKeyboardButton(
                '⚙️Soporte',
                url=f'https://t.me/Wachu985'
            ),
            InlineKeyboardButton(
                '💻GITHUB',
                url=f'https://github.com/Wachu985/'
            ),
            ],
            [
                InlineKeyboardButton(
                    '🖥Support Channel',
                    url=f'https://t.me/IDMDescarga'
                )
            ]      
    ]
    reply_botton = InlineKeyboardMarkup(enlace_directo)
    await bot.send_message(message.chat.id,text,reply_markup=reply_botton)


"""=============Method that Receives the Link from the User=============="""
@bot.on_message(filters.private)
async def get_message(client,message):
    await get_mensage(client,message)
    


"""============Method to Get Message from Group or Channel Restricted and Upload to BOT=============="""
async def get_mensage(client, message):
    try:
        """===========Join to Channel or Group==========="""
        if len(message.text.split('/')) <= 4 and len(message.text.split('/')) > 2:
            msag = await client.send_message(message.chat.id,'**🕥Procesando...**')
            if 'https://t.me/+' in message.text:
                try:
                    await userbot.join_chat(message.text)
                    await client.send_message(message.chat.id, '**✅Unido al Canal**')
                except (UsernameInvalid,ChannelInvalid,InviteHashExpired,PeerIdInvalid):
                    await client.send_message(message.chat.id, '**⚠️Link Invalido Verifiquelo**')
                except UserAlreadyParticipant:
                    await client.send_message(message.chat.id, '**⚠️Ya Estas en el Canal**')

            else:
                try:
                    await userbot.join_chat(message.text.split('/')[-1])
                    await client.send_message(message.chat.id, '**✅Unido al Canal**')
                except (UsernameInvalid,ChannelInvalid,InviteHashExpired,PeerIdInvalid):
                    await client.send_message(message.chat.id, '**⚠️Link Invalido Verifiquelo**')
                except UserAlreadyParticipant:
                    await client.send_message(message.chat.id, '**⚠️Ya Estas en el Canal**')


        #============Download fron te Channel or Group and Upload to Telegram============
        elif 'https://t.me/c/' in  message.text:
            save = './downloads/'+message.chat.username+'/'
            msag = await client.send_message(message.chat.id,'**🕥Procesando...**')
            try:
                chat = '-100' + message.text.split('/')[-2]
                msg_id = message.text.split('/')[-1]
                msge = await userbot.get_messages(int(chat),int(msg_id))
                if msge.media:
                    msg = await client.edit_message_text(msag.chat.id,msag.id,'**📥Intentando Descargar....**')
                    start = time()
                    filename = get_filename_media(msge)
                    file = await userbot.download_media(
                        msge,
                        save,
                        progress=progressddl,
                        progress_args=(msg,bot,filename,start)
                    )
                    msg = await client.edit_message_text(msg.chat.id,msg.id,'**✅Descarga Correcta**')
                    start = time()
                    filename = file.split('/')[-1]
                    if str(file).split('.')[-1] in ['jpg','png','gif','webp','jpeg']:
                        msg = client.edit_message_text(msg.chat.id,msg.id,'**📤Subiendo a Telegram**')
                        await bot.send_photo(
                            message.chat.id,
                            file,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start)
                        )
                    elif str(file).split('.')[-1] in ['mp4','mpg','mkv','webp','avi','flv']:
                        msg = await client.edit_message_text(msg.chat.id,msg.id,'**📤Subiendo a Telegram**')
                        await bot.send_video(
                            message.chat.id,
                            file,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start)
                        )
                    else:
                        msg = await client.edit_message_text(msg.chat.id,msg.id,'**📤Subiendo a Telegram**')
                        await bot.send_document(
                            message.chat.id,
                            file,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start)
                        )
                elif not msge.media:
                    await client.send_message(
                        message.chat.id, msge.text.markdown
                    )
                msg = await client.edit_message_text(msg.chat.id,msg.id,'**✅Subido Correctamente**')
            except ChannelInvalid:
                await client.send_message(message.chat.id, '**Te Haz Unido al Canal❓**')

        #============Download fron te Channel or Group and Upload to Telegram============
        elif 'https://t.me/' in  message.text:
            save = './downloads/'+message.chat.username+'/'
            msag = await client.send_message(message.chat.id,'**🕥Procesando...**')
            try:
                chat =  message.text.split('/')[-2]
                msg_id =  message.text.split('/')[-1]
                msge = await userbot.get_messages(chat,int(msg_id))
                if msge.media:
                    msg = await client.edit_message_text(msag.chat.id,msag.id,'**📥Intentando Descargar....**')
                    start = time()
                    filename = get_filename_media(msge)
                    file = await userbot.download_media(
                        msge,
                        save,
                        progress=progressddl,
                        progress_args=(msg,bot,filename,start)
                    )
                    msg = await client.edit_message_text(msg.chat.id,msg.id,'**✅Descarga Correcta**')
                    start = time()
                    filename = file.split('/')[-1]
                    if str(file).split('.')[-1] in ['jpg','png','gif','webp','jpeg']:
                        msg = await client.edit_message_text(msg.chat.id,msg.id,'**📤Subiendo a Telegram**')
                        await bot.send_photo(
                            message.chat.id,
                            file,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start)
                        )
                    elif str(file).split('.')[-1] in ['mp4','mpg','mkv','webp','avi','flv']:
                        msg = await client.edit_message_text(msg.chat.id,msg.id,'**📤Subiendo a Telegram**')
                        await bot.send_video(
                            message.chat.id,
                            file,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start)
                        )
                    else:
                        msg = await client.edit_message_text(msg.chat.id,msg.id,'📤**Subiendo a Telegram**')
                        await bot.send_document(
                            message.chat.id,
                            file,
                            progress=progressub,
                            progress_args=(msg,bot,filename,start)
                        )
                elif not msge.media:
                    await client.send_message(message.chat.id, msge.text.markdown) 
                msg = await client.edit_message_text(msg.chat.id,msg.id,'**✅Subido Correctamente**')
            except ChannelInvalid:
                await client.send_message(message.chat.id, '**Te Haz Unido al Canal❓**')
    except Exception as ex:
        await client.send_message(message.chat.id, f'Error {ex}')
            

"""=============Method for Start Bot============="""
async def runbot():
    print('==============Starting Bot==============')
    await userbot.start()
    print('==============User Bot Started==============')
    await bot.start()
    print('==============Bot Started==============')
    
"""============Start the Bot============"""
if __name__ == '__main__':
    try:
        bot.loop.run_until_complete(runbot())
        idle()
    except:
        bot.loop.run_until_complete(runbot())
        idle()