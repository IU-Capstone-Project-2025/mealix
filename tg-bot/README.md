## Telegram bot

### Usage
1. Create .env file in root directory. It should contain:
```
BOT_TOKEN=<YOUR TOKEN>
```
2. Edit links in application.properties:
```
backend.host=<YOUR BACKEND HOST>
bot.miniapp.host=<YOUR MINIAPP HOST>
```
3. Run docker
4. Run command:
```
docker compose up --build -d
```