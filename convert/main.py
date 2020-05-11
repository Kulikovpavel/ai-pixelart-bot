from io import BytesIO
import cv2
import os
import numpy as np
from pyxelate import Pyxelate
import telegram


bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])


def continue_processing(update):
    text = update.message.text

    chat_id = update.message.chat.id
    if not update.message.photo:
        return
    file_id = update.message.photo[-1].file_id
    image_str = bot.get_file(file_id).download_as_bytearray()
    nparr = np.frombuffer(image_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height, width, _ = img_np.shape
    try:
        factor, backscale, colors = text.split(":")
        factor = int(factor)
        backscale = int(backscale)
        colors = int(colors)
    except:
        factor = max(1, max(height, width) // 320)
        backscale = 1
        colors = 8

    dither = True

    bot.sendMessage(chat_id=chat_id, text="got it, working... (up to 4 min)")

    p = Pyxelate(height // factor, width // factor, colors, dither)
    img_small = p.convert(img_np)  # convert an image with these settings
    if backscale > 1:
        img_small = cv2.resize(
            img_small, (img_small.shape[1] * backscale, img_small.shape[0] * backscale)
        )
    img_back_bytes = cv2.imencode(".jpg", img_small)[1].tostring()
    bot.send_photo(chat_id=chat_id, photo=BytesIO(img_back_bytes))


def convert(request):
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    try:
        continue_processing(update)
    except Exception as e:
        bot.sendMessage(chat_id=chat_id, text=str(e))
    return "ok"
