import sys
import asyncio
import logging
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTextEdit
)
from PyQt5.QtCore import QTimer
from qasync import QEventLoop, asyncSlot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chat_client.log"),
        logging.StreamHandler(sys.stdout),
    ]
)


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Async Chat Client")
        self.setGeometry(100, 100, 600, 400)

        # GUI элементы
        self.layout = QVBoxLayout(self)

        self.label_status = QLabel("Status: Disconnected", self)
        self.layout.addWidget(self.label_status)

        self.name_field = QLineEdit(self)
        self.name_field.setPlaceholderText("Enter your name")
        self.layout.addWidget(self.name_field)

        self.room_field = QLineEdit(self)
        self.room_field.setPlaceholderText("Enter room number")
        self.layout.addWidget(self.room_field)

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)

        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)
        self.layout.addWidget(self.chat_log)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message here...")
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Подключение
        self.reader = None
        self.writer = None
        self.receive_task = None
        self.name = None
        self.room_number = None

    @asyncSlot()
    async def connect_to_server(self):
        if self.receive_task:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                self.log_message("Previous message receiving task cancelled.", level="info")
        
        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except Exception as e:
                self.log_message(f"Error closing previous connection: {e}", level="error")

        self.name = self.name_field.text().strip()
        self.room_number = self.room_field.text().strip()

        if not self.name or not self.room_number:
            self.log_message("Name and room number must be provided.", level="warning")
            return

        try:
            self.reader, self.writer = await asyncio.open_connection("localhost", 8080)
            self.update_status("Connected")
            self.log_message("Successfully connected to the server.")

            self.writer.write(f"{self.name}\n".encode())
            self.writer.write(f"{self.room_number}\n".encode())
            await self.writer.drain()

            response = await self.reader.readline()
            self.log_message(f"Server response: {response.decode().strip()}")

            self.receive_task = asyncio.create_task(self.receive_messages())
        except Exception as e:
            self.log_message(f"Error: {e}", level="error")
            self.update_status("Disconnected")
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()

    async def close_connection(self):
        """Корректно завершает соединение с сервером."""
        if self.receive_task and not self.receive_task.done():
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                self.log_message("Message receiving task cancelled.", level="info")

        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except Exception as e:
                self.log_message(f"Error while closing writer: {e}", level="error")


        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except Exception as e:
                self.log_message(f"Error while closing writer: {e}", level="error")


    async def receive_messages(self):
        try:
            while True:
                message = await self.reader.readline()
                if not message:
                    break
                self.log_message(message.decode().strip())
        except asyncio.CancelledError:
            self.log_message("Message receiving task was cancelled.", level="info")
        except Exception as e:
            self.log_message(f"Error receiving messages: {e}", level="error")
        finally:
            self.update_status("Disconnected")

    @asyncSlot()
    async def send_message(self):
        if not self.writer:
            self.log_message("Not connected to the server.", level="warning")
            return

        message = self.input_field.text().strip()
        if not message:
            return

        try:
            self.writer.write(f"{message}\n".encode())
            await self.writer.drain()
            self.input_field.clear()
            self.log_message(f"Message sent: {message}")
        except Exception as e:
            self.log_message(f"Error sending message: {e}", level="error")

    def log_message(self, message, level="info"):
        log_function = getattr(logging, level)
        log_function(message)

        def update():
            if self.chat_log:
                self.chat_log.append(message)

        QTimer.singleShot(0, update)

    def update_status(self, status):
        def update():
            if self.label_status:
                self.label_status.setText(f"Status: {status}")
        QTimer.singleShot(0, update)


async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    client = ChatClient()
    client.show()

    def handle_exit():
        """Обработчик выхода из приложения."""
        asyncio.create_task(client.close_connection())
        loop.stop()

    app.aboutToQuit.connect(handle_exit)

    with loop:
        loop.run_forever()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    client = ChatClient()
    client.show()

    with loop:
        loop.run_forever()
