# Voice Assistant Agent (with Telegram)

Create an AI-powered voice assistant that listens to voice messages on Telegram and responds intelligently.

## 📋 Overview

This workflow creates a Telegram bot that can receive voice messages, transcribe them using OpenAI Whisper, process them with GPT, and send back text responses. Perfect for hands-free interactions or accessibility needs.

## 🎯 Use Case

**Problem**: Users want to interact with AI assistants using voice without typing.

**Solution**: This voice agent:
- Receives voice messages via Telegram
- Transcribes speech to text using Whisper
- Processes requests with GPT AI
- Maintains conversation context
- Responds with intelligent text answers

## ⚙️ How It Works

1. **Telegram Trigger**: Listens for incoming messages
2. **Audio Check**: Detects if message contains voice audio
3. **Fetch Audio**: Downloads voice file from Telegram
4. **Transcription**: Converts speech to text using Whisper
5. **AI Processing**: GPT analyzes the transcription
6. **Memory**: Remembers last 10 messages for context
7. **Response**: Sends text reply back to Telegram

## 🔧 Setup Instructions

### Prerequisites

- Telegram account
- OpenAI API key ([Get one](https://platform.openai.com/api-keys))
- n8n instance with publicly accessible webhook URL
- Your Telegram User ID ([Find it](https://t.me/userinfobot))

### Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow prompts to name your bot
4. Copy the **Bot Token** (looks like `123456:ABC-DEF...`)
5. Save this token for later

### Step 2: Get Your Telegram User ID

1. Search for **@userinfobot** in Telegram
2. Start a chat
3. Copy your **User ID** (numeric value)
4. You'll use this to restrict bot access to only you

### Step 3: Import Workflow to n8n

1. Open your n8n instance
2. Click **Workflows** → **Import**
3. Copy contents of `voice-agent.json`
4. Paste and click **Import**

### Step 4: Configure Telegram Credentials

#### For Telegram Trigger Node:
1. Click **Telegram Message Trigger** node
2. Click **Create New Credential**
3. Choose **Telegram API**
4. Paste your Bot Token
5. Save credential

#### For Get a File Node:
1. Click **Get a file** node
2. Select the same Telegram credential
3. Save

#### For Reply Node:
1. Click **Reply in Telegram** node
2. Select the same Telegram credential
3. Save

### Step 5: Set Your User ID

1. Click **Telegram Message Trigger** node
2. Find **Additional Fields** → **User IDs**
3. Replace `YOUR_USER_ID` with your actual User ID
4. This restricts bot access to only you

### Step 6: Configure OpenAI Credentials

#### For Transcription:
1. Click the **Transcribe Voice** node (OpenAI Whisper)
2. Create new OpenAI credential
3. Enter your OpenAI API key
4. Save

#### For AI Agent:
1. Click **AI Agent** node
2. Navigate to **Model** sub-node
3. Select the same OpenAI credential
4. Choose your preferred model (gpt-4o recommended)

### Step 7: Configure Webhook

1. Save the workflow
2. **Activate** the workflow (toggle switch)
3. n8n will generate a webhook URL
4. Copy the webhook URL from the Telegram Trigger node

### Step 8: Set Telegram Webhook

1. Open this URL in your browser (replace with your values):
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>
```

2. You should see: `{"ok":true,"result":true}`

### Step 9: Test the Bot

1. Open Telegram and find your bot
2. Send `/start` command
3. **Send a voice message** (hold mic button)
4. Wait for transcription and AI response
5. Bot will reply with text

## 📊 Configuration Options

### AI Model Selection

Default: GPT-4o

To change:
1. Click **Model** node
2. Select different model:
   - `gpt-4o` - Most capable (higher cost)
   - `gpt-4o-mini` - Faster, cheaper
   - `gpt-3.5-turbo` - Budget option

### Memory Window

Default: 10 messages

To adjust:
1. Click **Memory** node
2. Change **Context Window Length**
3. Higher = more context (more expensive)

### Authorized Users

To allow multiple users:
1. Click **Telegram Message Trigger**
2. In **User IDs** field, add comma-separated IDs:
   ```
   123456789,987654321,555555555
   ```

## 🎓 Difficulty Level

**Advanced** 🔴

- Requires webhook setup and public n8n URL
- Multiple API integrations
- Telegram bot configuration
- Audio file processing

## 💡 Tips & Best Practices

1. **Test Text First**: Send text messages before voice to verify bot works
2. **Clear Audio**: Speak clearly and minimize background noise
3. **Short Messages**: Keep voice messages under 1 minute
4. **Monitor Costs**: Whisper charges per minute of audio
5. **Secure Your Bot**: Only share bot username with authorized users

## 🚨 Troubleshooting

### Bot Doesn't Respond

- Verify workflow is activated (green toggle)
- Check webhook is properly set
- Confirm your User ID is correct
- Review execution logs in n8n

### Voice Not Transcribed

- Ensure OpenAI credentials are valid
- Check API key has Whisper access
- Verify audio file downloads successfully
- Review n8n execution logs for errors

### Poor Transcription Quality

- Speak more clearly and slowly
- Reduce background noise
- Check microphone quality
- Try shorter voice messages

### Webhook Errors

- n8n must be publicly accessible
- Check firewall/security group settings
- Verify webhook URL is HTTPS (required by Telegram)
- Re-set webhook if n8n URL changes

## 💰 Cost Estimate

Per voice message:
- **Whisper Transcription**: ~$0.006/minute
- **GPT Response**: $0.002-0.06 (model-dependent)
- **Telegram**: Free
- **n8n**: Free (Community) or $20/month

**Example**: 100 voice messages/day (30 sec each) = ~$9-30/month

## 🔒 Security Considerations

- Bot token is sensitive - never share publicly
- User ID restriction prevents unauthorized access
- Voice messages processed by OpenAI (review privacy policy)
- No voice data stored in n8n after processing
- Use HTTPS for all webhook communications

## 📈 Advanced Features to Add

Consider extending this workflow:
- Text-to-speech responses (send voice back)
- Multi-language support
- Integration with knowledge bases
- Custom commands and triggers
- Voice analytics and logging

## 🔧 Customization Ideas

### Custom System Prompt
Edit the AI agent's instructions:
```
You are a helpful voice assistant.
Be concise in responses since users are using voice.
Ask clarifying questions if needed.
```

### Add Commands
Handle special commands like:
- `/help` - Show available features
- `/reset` - Clear conversation memory
- `/settings` - Configure preferences

### Connect to Services
Integrate with:
- Calendar (schedule via voice)
- Email (voice-to-email)
- Notes (voice dictation)
- Tasks (voice task creation)

## 🤝 Need Help?

- [Telegram Bot Documentation](https://core.telegram.org/bots)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [n8n Community](https://community.n8n.io)

---

**Workflow File**: `voice-agent.json`
**Category**: Customer Service → Chat Automation
**Version**: 1.0.0
**Last Updated**: November 19, 2025
