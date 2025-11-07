# Telegram Auto-Approve Bot

🤖 Automatic approval of join requests for Telegram channels

## 🚀 Quick Start

### Method 1: Local Installation
```bash
# Clone repository
git clone https://github.com/yourusername/telegram-auto-approve-bot.git
cd telegram-auto-approve-bot

# Automatic installation
chmod +x scripts/install.sh
./scripts/install.sh

# Setup environment
cp .env.example .env
# Edit .env file with your data

# Run
python -m src.bot
Method 2: Docker
bash
# Setup environment file
cp .env.example .env

# Run with Docker
docker-compose up -d
⚙️ Configuration
Get API credentials from my.telegram.org

Fill in the .env file:

env
API_ID=12345678
API_HASH=your_api_hash_here
CHANNEL_ID=your_channel_id
🔧 Channel Setup
Add the bot as channel administrator

Grant permissions: "Add users"

Ensure the channel is private with join requests enabled

📦 Docker Commands
bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
🐛 Troubleshooting
Sessions are saved in the sessions/ folder

Logs available via docker-compose logs

Automatic restart on errors

📄 License