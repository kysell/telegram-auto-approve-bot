#!/bin/bash

echo "🤖 Installing Telegram Auto-Approve Bot"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create configuration files
echo "⚙️ Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env.example - please edit .env with your data"
fi

echo "🎉 Installation completed!"
echo "📝 Don't forget to fill in the .env file:"
echo "   - API_ID and API_HASH from my.telegram.org"
echo "   - CHANNEL_ID (your channel ID)"
echo ""
echo "🚀 Run: python -m src.bot"
echo "🐳 Or: docker-compose up -d"