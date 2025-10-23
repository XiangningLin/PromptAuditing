#!/bin/bash

# Prompt Auditing Framework - Start Script

echo "🚀 Starting Prompt Auditing Framework..."
echo ""

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY environment variable not set"
    echo "Please set it using:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if required files exist
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found"
    exit 1
fi

if [ ! -f "standards.json" ]; then
    echo "❌ Error: standards.json not found"
    exit 1
fi

# Check if dependencies are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✅ Starting Flask server..."
echo "🌐 Open your browser and navigate to: http://localhost:5002"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py

