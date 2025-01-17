import asyncio

EMOJI_LIST = {
    "4chan-emoticon": "( ͡° ͜ʖ ͡°)",
    "angry-birds": "( ఠൠఠ )ﾉ",
    "angry-face": "(╬ ಠ益ಠ)",
    "angry-troll": "ヽ༼ ಠ益ಠ ༽ﾉ",
    "at-what-cost": "ლ(ಠ益ಠლ)",
    "barf": "(´ж｀ς)",
    "basking-in-glory": "ヽ(´ー｀)ノ",
    "boxing": "ლ(•́•́ლ)",
    "breakdown": "ಥ﹏ಥ",
    "careless": "◔_◔",
    "cheers": "( ^_^)o自自o(^_^ )",
    "chicken": "ʚ(•｀",
    "confused-scratch": "(⊙.☉)7",
    "confused": "¿ⓧ_ⓧﮌ",
    "crazy": "ミ●﹏☉ミ",
    "cry-face": "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "crying-face": "ಥ_ಥ",
    "cry-troll": "༼ ༎ຶ ෴ ༎ຶ༽",
    "cute-bear": "ʕ•ᴥ•ʔ",
    "cute-face-with-big-eyes": "(｡◕‿◕｡)",
    "dab": "ヽ( •_)ᕗ",
    "dance": "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "dancing": "┌(ㆆ㉨ㆆ)ʃ",
    "dear-god-why": "щ(ﾟДﾟщ)",
    "devious-smile": "ಠ‿ಠ",
    "disagree": "٩◔̯◔۶",
    "discombobulated": "⊙﹏⊙",
    "dislike": "( ಠ ʖ̯ ಠ)",
    "double-Flip": "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    "do-you-even-lift-bro?": "ᕦ(ò_óˇ)ᕤ",
    "emo-dance": "ヾ(-_- )ゞ",
    "excited": "☜(⌒▽⌒)☞",
    "exorcism": "ح(•̀ж•́)ง †",
    "eye-roll": "⥀.⥀",
    "feel-perky": "(`･ω･´)",
    "fido": "V•ᴥ•V",
    "fight": "(ง̀-́)ง",
    "fisticuffs": "ლ(｀ー´ლ)",
    "flexing": "ᕙ(⇀‸↼‶)ᕗ",
    "flip-friend": "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "fly-away": "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "flying": "ح˚௰˚づ",
    "fuck-it": "t(-_-t)",
    "fuck-off": "(° ͜ʖ͡°)╭∩╮",
    "GTFO-Bear": "ʕ •`ᴥ•´ʔ",
    "happy-face": "ヽ(´▽`)/",
    "happy-hug": "\\(ᵔᵕᵔ)/",
    "hitchhiking": "(งツ)ว",
    "hugger": "(づ￣ ³￣)づ",
    "im-a-hugger": "(⊃｡•́‿•̀｡)⊃",
    "injured": "(҂◡_◡)",
    "innocent-face": "ʘ‿ʘ",
    "japanese-lion-face": "°‿‿°",
    "judgemental": "{ಠʖಠ}",
    "judging": "( ఠ ͟ʖ ఠ)",
    "kirby": "⊂(◉‿◉)つ",
    "kissing": "( ˘ ³˘)♥",
    "kitty-emote": "ᵒᴥᵒ#",
    "listening-to-headphones": "◖ᵔᴥᵔ◗ ♪ ♫",
    "looking-down": "(._.)",
    "love": "♥‿♥",
    "meh": "¯\\(°_o)/¯",
    "meow": "ฅ^•ﻌ•^ฅ",
    "no-support": "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "opera": "ヾ(´〇`)ﾉ♪♪♪",
    "peepers": "ಠಠ",
    "pointing": "(☞ﾟヮﾟ)☞",
    "pretty-eyes": "ఠ_ఠ",
    "put-the-table-back": "┬─┬﻿ ノ( ゜-゜ノ)",
    "questionable": "(Ծ‸ Ծ)",
    "reddit-disapproval-face": "ಠ_ಠ",
    "resting-my-eyes": "ᴖ̮ ̮ᴖ",
    "robot": "{•̃_•̃}",
    "running": "ε=ε=ε=┌(;*´Д`)ﾉ",
    "sad-and-confused": "¯\\_(⊙︿⊙)_/¯",
    "sad-and-crying": "(ᵟຶ︵ ᵟຶ)",
    "sad-face": "(ಥ⌣ಥ)",
    "satisfied": "(◠﹏◠)",
    "seal": "(ᵔᴥᵔ)",
    "shark-face": "( ˇ෴ˇ )",
    "shrug-face": "¯\\_(ツ)_/¯",
    "shy": "(๑•́ ₃ •̀๑)",
    "sleepy": "눈_눈",
    "smiley-toast": "ʕʘ̅͜ʘ̅ʔ",
    "squinting-bear": "ʕᵔᴥᵔʔ",
    "staring": "٩(๏_๏)۶",
    "stranger-danger": "(づ｡◕‿‿◕｡)づ",
    "strut": "ᕕ( ᐛ )ᕗ",
    "stunna-shades": "(っ▀¯▀)つ",
    "surprised": "(　ﾟДﾟ)",
    "table-flip": "(╯°□°)╯︵ ┻━┻",
    "taking-a-dump": "(⩾﹏⩽)",
    "tgif": "“ヽ(´▽｀)ノ”",
    "things-that-cant-be-unseen": "♨_♨",
    "tidy-up": "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "tired": "( ͡ಠ ʖ̯ ͡ಠ)",
    "touchy-feely": "ԅ(≖‿≖ԅ)",
    "tripping-out": "q(❂‿❂)p",
    "trolling": "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "wave-dance": "~(^-^)~",
    "whistling": "(っ•́｡•́)♪♬",
    "winnie-the-pooh": "ʕ •́؈•̀)",
    "winning": "(•̀ᴗ•́)و ̑̑",
    "wizard": "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "worried": "(`･_･`)",
    "yum": "(っ˘ڡ˘ς)",
    "zombie": "[¬º-°]¬",
    "zoned": "(⊙_◎)"
}


class ChatServer:
    def __init__(self):
        # Храним клиентов в формате: {адрес: (номер_комнаты, writer, имя)}
        self.clients = dict()  # Все подключенные клиенты
        # Храним информацию о комнатах
        self.rooms = dict()  # {room_number: [client1, client2, ...]}

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        addr_str = f"{addr[0]}:{addr[1]}"
        print(f"Client {addr_str} connected", flush=True)

        name = None
        room_number = None

        try:
            # Регистрация клиента
            await writer.drain()
            name = (await reader.readline()).decode().strip()
            if not name:
                raise ValueError("Name cannot be empty.")

            await writer.drain()
            room_number = (await reader.readline()).decode().strip()
            if not room_number.isdigit():
                raise ValueError("Room number must be a valid integer.")
            room_number = int(room_number)

            print(f"Client {addr_str} joined room {room_number}! His name is {name}", flush=True)
        except Exception as e:
            print(f"Error during registration: {e}", flush=True)
            writer.write("Error during registration. Please try again.\n".encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        try:
            # Добавляем клиента в списки
            self.clients[addr_str] = (room_number, writer, name)
            if room_number not in self.rooms:
                self.rooms[room_number] = []
            self.rooms[room_number].append(name)
            await self.broadcast(f"{name} has joined the room!", room_number)

            # Основной цикл обработки сообщений
            while True:
                data = await reader.readline()
                message = data.decode().strip()

                if not message:  # Клиент разорвал соединение
                    break

                if message.lower() == "/quit":
                    await self.broadcast(f"{name} has left the room.", room_number)
                    break

                elif message.lower() == "/help":
                    await self.send_help(writer)
                elif message.lower() == "/listrooms":
                    await self.list_rooms(writer)
                else:
                    message = self.replace_emojis(message)
                    await self.broadcast(f"{name}: {message}", room_number)
        except Exception as e:
            print(f"Error handling messages for {addr_str}: {e}", flush=True)
        finally:
            # Отключение клиента
            print(f"Client {addr_str} disconnected", flush=True)
            if addr_str in self.clients:
                del self.clients[addr_str]
            if room_number in self.rooms and name in self.rooms[room_number]:
                self.rooms[room_number].remove(name)
                if not self.rooms[room_number]:  # Удаляем комнату, если она пустая
                    del self.rooms[room_number]
            writer.close()
            await writer.wait_closed()


    async def send_help(self, writer):
        """Отправка инструкции пользователю."""
        help_text = (
            "Welcome to the chat server! Here are some commands you can use:\n"
            "/help - Show this help message\n"
            "/listrooms - List all rooms and the users inside\n"
            "/quit - Exit the chat\n"
        )
        writer.write(help_text.encode())
        await writer.drain()

    async def list_rooms(self, writer):
        """Отправка списка всех комнат и пользователей в них."""
        message = "List of rooms:\n"
        for room_number, users in self.rooms.items():
            message += f"Room {room_number}: {', '.join(users)}\n"
        
        if not message.strip():
            message = "No rooms available.\n"
        
        writer.write(message.encode())
        await writer.drain()
        

    async def broadcast(self, message, room_number):
        """Отправка сообщения всем клиентам в указанной комнате."""
        print(f"Broadcasting message in room {room_number}: {message}", flush=True)
        for addr, (client_room, client_writer, client_name) in self.clients.items():
            if client_room == room_number:
                try:
                    print(f"Sending to {client_name} in room {room_number}", flush=True)
                    client_writer.write((message + "\n").encode())
                    await client_writer.drain()
                except Exception as e:
                    print(f"Error broadcasting to {addr}: {e}", flush=True)


    def replace_emojis(self, message):
        """Заменяет команды эмодзи в сообщении на символы эмодзи из списка EMOJI_LIST."""
        words = message.split()
        new_message = []

        for word in words:
            if word.startswith("/"):
                # Если слово это команда эмодзи, заменяем на эмодзи
                emoji = EMOJI_LIST.get(word[1:], None)  # Убираем слэш и ищем в списке
                if emoji:
                    new_message.append(emoji)
                else:
                    new_message.append(word)  # Если эмодзи не найдено, оставляем слово
            else:
                new_message.append(word)

        return " ".join(new_message)

    async def main(self):
        server = await asyncio.start_server(self.handle_client, '0.0.0.0', 8080)
        print('Server started and listening on 0.0.0.0:8080', flush=True)
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    print('Server starting...', flush=True)
    chat_server = ChatServer()
    asyncio.run(chat_server.main())