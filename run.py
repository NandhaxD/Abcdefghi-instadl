import pyrogram
from Instagram import InstaAPI

app = pyrogram.Client(...)
Instagram = InstaAPI()

@app.on_inline_query(group=0)
async def iginline(c,q):
  query = q.query
  if not (query and len(query.split(" ")) > 1 and query.split(" ")[0] == "!ig" and Instagram.exists(query.split(" ")[1])):
    return
  mediaid = query.split(" ")[1].split("/")
  res = pyrogram.types.InlineQueryResultPhoto(title="Download Instagram Video",photo_url="https://telegra.ph/file/2dbf6974c6bdc02be3f15.jpg",caption = f"Download Now : <a href={query.split(' ')[1]}>Insta Video</a>",reply_markup=pyrogram.types.InlineKeyboardMarkup([[pyrogram.types.InlineKeyboardButton(text="Download ⬇️", callback_data=f"igdownload:{mediaid[-2]}/{mediaid[-1]}")]]))
  if Instagram.is_valid_instagram_story_url(query.split(" ")[1]):
   mediaid = Instagram.filter_instagram_story_url(query.split(" ")[1]).split("/")
   res = pyrogram.types.InlineQueryResultPhoto(title="Download Instagram Video",photo_url="https://telegra.ph/file/2dbf6974c6bdc02be3f15.jpg",caption = f"Download Now : <a href={query.split(' ')[1]}>Insta Video</a>",reply_markup=pyrogram.types.InlineKeyboardMarkup([[pyrogram.types.InlineKeyboardButton(text="Download ⬇️", callback_data=f"igdownload:{mediaid[-3]}/{mediaid[-2]}/{mediaid[-1]}")]]))
  await q.answer([res],cache_time=10)


@app.on_callback_query(pyrogram.filters.regex(pattern=r"igdownload"))
async def song_commad_private(client, query):
    url = f"https://www.instagram.com/{query.data.split(':')[-1]}"
    mystic = await app.edit_inline_text(inline_message_id=query.inline_message_id,text="Wait processing your query..") 
    try:
      vidurl,picurl,name,typee = Instagram.info(url)
      instalink = f"https://www.instagram.com/{name}/"
      await app.edit_inline_text(inline_message_id=query.inline_message_id,text=f"<b>Downloading!</>\n\nInstagram media from  {name} \n\nUsage: <code>@mnrobot !ig url</code>")
      name,res = Instagram.instadl(url)
      await app.edit_inline_text(inline_message_id=query.inline_message_id,text=f"<b>Uploading!</>\n\nInstagram media from  {name} \n\nUsage: <code>@mnrobot !ig url</code>")
      if typee in [1,8]:
       with open(res, "rb") as photo_file:
         photo = io.BytesIO(photo_file.read())
       photo.name = "photo.jpg"
       await app.edit_inline_media(inline_message_id=query.inline_message_id,media= pyrogram.types.InputMediaPhoto(media=photo,caption=f"Instagram photo from <a href={instalink}> {name} </a>\n\nUsage: <code>@mnrobot !ig url</code>"))
      if typee == 2:
       await app.edit_inline_media(inline_message_id=query.inline_message_id,media= pyrogram.types.InputMediaVideo(media=res,caption=f"Instagram video from <a href={instalink}> {name} </a>\n\nUsage: <code>@mnrobot !ig url</code>"))
    except Exception as e:
      mystic = await app.edit_inline_text(inline_message_id=query.inline_message_id,text=f"Error: {e}")


@app.on_message(pyrogram.filters.command("insta"))
async def song_commad_private(client, message):
    await message.delete()
    if len(message.text.split(" ")) == 1:
     return await message.reply("Usage: /insta [Instagram URL]")
    url = message.text.split(" ")[1]
    if url:
        if not Instagram.exists(url):
            return await message.reply_text("Invalid Instagram url")
    mystic = await message.reply_text("Wait processing your query...")
    try:
      vidurl,picurl,name,typee = Instagram.info(url)
      instalink = f"https://www.instagram.com/{name}/"
      await mystic.edit(f"<b>Downloading!</>\n\nInstagram media from  {name} \n\nUsage: /insta [Instagram URL]")
      name,res = Instagram.instadl(url)
      await mystic.edit(f"<b>Uploading!</>\n\nInstagram media from  {name} \n\nUsage: /insta [Instagram URL]")
      await app.send_chat_action(
            chat_id=message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )
      if typee in [1,8]:
       await message.reply_document(res, caption=f"Instagram photo from <a href={instalink}> {name} </a>\n\nUsage: /insta [Instagram URL]")
      if typee == 2:
       await message.reply_video(res, caption=f"Instagram video from <a href={instalink}> {name} </a>\n\nUsage: /insta [Instagram URL]")
      await mystic.delete()
    except Exception as e:
      await message.reply(f"Error: {e}")
      await mystic.delete()

app.run()

