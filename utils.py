def get_filename_media(message):
    if message.video:
        try:
            filename = message.video.file_name
        except:
            filename = message.video.file_id
    elif message.sticker:
        try:
            filename = message.sticker.file_name
        except:
            filename = message.sticker.file_id
    elif message.photo:
        try:
            filename = message.photo.file_name
        except:
            filename = message.photo.file_id
    elif message.audio:
        try:
            filename = message.audio.file_name
        except:
            filename = message.audio.file_id
    elif message.document:
        try:
            filename = message.document.file_name
        except:
            filename = message.document.file_id
    elif message.voice:
        try:
            filename = message.voice.file_name
        except:
            filename = message.voice.file_id
    return filename