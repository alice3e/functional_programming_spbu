docker build -t chat-server .
docker run -p 8080:8080 -d --name chat-server-container chat-server
