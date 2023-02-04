                await m.reply_photo(
                    photo="https://telegra.ph/file/18d25616d9883400af112.png",
                    caption=f"""
**▶ Now Meow userbot playing video {pos}
🏷️ Song name: [{songname}]
💡 Status: Playing
🎧 Request by: {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/18d25616d9883400af112.png",
                    caption=f"""
**▶ Now Meow userbot playing Video
🏷️ Song name: [{songname}]
💡 Status: Playing
🎧 Request by: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply(
                "** Please check you have typed the word correctly **"
            )
        else:
            await m.delete()
            huehue = await m.reply("** Your search terms did not match any entries **")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(
                    "**Please check your songs name**"
                )
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR âš ï¸** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{IMAGE_THUMBNAIL}",
                            caption=f"""
**▶ Now Meow userbot Playing video {pos}
🏷️ Song name : [{songname}]
💡 Status: Playing
🎧 Request by: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{IMAGE_THUMBNAIL}",
                                caption=f"""
**▶ Now Meow userbot playing video
🏷️ Song name: [{songname}]
💡 Status: Playing
🎧 Request by: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")

@Client.on_message(filters.me & filters.command(["playfrom"], prefixes=f"{HNDLR}"))
@Client.on_message(filters.user(SUDO_USERS) & filters.command(["playfrom"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**Playform:** \n\n`{HNDLR}playfrom [chat_id/username]` \n`{HNDLR}playfrom [chat_id/username]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"**✧ Duration {limit} playing {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_photo(
                        photo="https://telegra.ph/file/18d25616d9883400af112.png",
                        caption=f"""
**▶ Now Meow userbot playing {chat}
🏷️ Song name: [{songname}]
💡 Status: Playing
🎧 Request by: {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"âž• it's duration {lmt} sir\nâ€¢ click {HNDLR}playlist to add playlist**"
            )
        except Exception as e:
            await hmm.edit(f"**ERROR** \n`{e}`")


@Client.on_message(filters.me & filters.command(["playlist", "queue"], prefixes=f"{HNDLR}"))
@Client.on_message(filters.user(SUDO_USERS) & filters.command(["playlist", "queue"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**✧ Starting playing:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**✧ song playlist:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**â¯ songs:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**✧ Done...**")
