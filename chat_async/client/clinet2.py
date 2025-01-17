import asyncio

async def handle_server(reader):
    """Функция для получения входящих сообщений от сервера."""
    while True:
        try:
            # Тайм-аут, чтобы избежать блокировки при отсутствии данных
            data = await asyncio.wait_for(reader.readline(), timeout=0.5)
            if data:
                print(f"Received from server -> {data.decode().strip()}")
        except asyncio.TimeoutError:
            # Периодическая проверка в случае отсутствия данных
            continue
        except asyncio.IncompleteReadError:
            print("Server closed the connection.")
            break
        except Exception as e:
            print(f"Error in handle_server: {e}")
            break

async def handle_user_input(writer, name):
    """Асинхронная функция для обработки пользовательского ввода."""
    while True:
        # Асинхронное получение пользовательского ввода
        message = await asyncio.to_thread(input, f"{name}> ")
        if message.lower() == "quit":
            writer.write("quit\n".encode())  # Команда выхода
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            print("Disconnected from the chat server.")
            break
        # Отправляем сообщение на сервер
        writer.write((message + "\n").encode())
        await writer.drain()

async def main():
    """Основная логика клиента."""
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    print("Connected to chat server. Type your name to join the chat.")
    name = input("Enter your name: ")
    room_number = input("Enter your room number: ")

    # Отправляем имя и номер комнаты на сервер
    writer.write((name + "\n").encode())
    writer.write((room_number + "\n").encode())
    await writer.drain()

    # Запускаем задачу для получения сообщений от сервера
    receive_task = asyncio.create_task(handle_server(reader))
    # Запускаем задачу для получения пользовательского ввода
    input_task = asyncio.create_task(handle_user_input(writer, name))

    await asyncio.gather(receive_task, input_task)  # Ожидаем завершения обеих задач

if __name__ == "__main__":
    asyncio.run(main())
