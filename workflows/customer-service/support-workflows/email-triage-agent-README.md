# Email Triage Agent (with Gmail)

Automatically organize your Gmail inbox with AI-powered email categorization and labeling.

## 📋 Overview

This workflow uses an AI agent to read incoming emails and automatically apply appropriate Gmail labels based on the email's content, sender, and context. Perfect for support teams or anyone managing high email volumes.

## 🎯 Use Case

**Problem**: Manually sorting through hundreds of emails daily is time-consuming and inconsistent.

**Solution**: This AI agent automatically:
- Monitors your Gmail for new unread emails
- Analyzes email content, subject, and sender
- Applies relevant labels from your Gmail account
- Keeps your inbox organized 24/7

## ⚙️ How It Works

1. **Email Trigger**: Polls Gmail every minute for new unread emails
2. **AI Analysis**: LangChain AI agent analyzes email content
3. **Label Selection**: Agent chooses 1-3 most relevant labels
4. **Auto-Label**: Applies selected labels to the email in Gmail

## 🔧 Setup Instructions

### Prerequisites

- Gmail account
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- n8n instance (self-hosted or cloud)
- Basic understanding of Gmail labels

### Step 1: Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API for your project
4. Create OAuth 2.0 credentials
5. Download the credentials JSON file

### Step 2: Create Gmail Labels

1. Open Gmail
2. Create labels you want the agent to use (e.g., "Urgent", "Customer Support", "Sales", "Billing")
3. Note the label names

### Step 3: Import Workflow to n8n

1. Open your n8n instance
2. Click **Workflows** → **Import**
3. Copy the contents of `email-triage-agent.json`
4. Paste into the import dialog
5. Click **Import**

### Step 4: Configure Credentials

#### Gmail Credentials:
1. Click on **New Email Trigger** node
2. Select **Create New Credential**
3. Choose **Gmail OAuth2 API**
4. Upload your OAuth credentials
5. Authorize access to your Gmail account

#### OpenAI Credentials:
1. Click on **Email Classification Agent** node
2. Click on **Model** sub-node
3. Select **Create New Credential**
4. Enter your OpenAI API key

### Step 5: Customize the Agent (Optional)

Edit the system message in the **Email Classification Agent** node to:
- Define specific categorization rules
- Set priority guidelines
- Add custom instructions

### Step 6: Test the Workflow

1. Click **Test Workflow** in n8n
2. Send yourself a test email
3. Wait up to 1 minute for the agent to process it
4. Check if labels were applied correctly

### Step 7: Activate

1. Click **Active** toggle to enable the workflow
2. The agent will now automatically process new emails

## 📊 Configuration Options

### Email Polling Frequency

Default: Every 1 minute

To change:
1. Click **New Email Trigger** node
2. Modify **Poll Times** → **Mode**
3. Options: Every minute, Every 5 minutes, Every hour, Custom

### Label Selection Rules

Customize the agent's behavior by editing the system message:

```
You are an email categorization assistant...

### Instructions:
- Apply priority labels for urgent requests
- Use "Customer Support" for help requests
- Use "Sales" for product inquiries
- Use "Billing" for payment-related emails
```

## 🎓 Difficulty Level

**Intermediate** 🟡

- Requires API setup for Gmail and OpenAI
- Basic understanding of OAuth authentication
- Familiarity with Gmail labels

## 💡 Tips & Best Practices

1. **Start Simple**: Begin with 3-5 main labels, expand later
2. **Test Thoroughly**: Process test emails before going live
3. **Monitor Initial Results**: Check first 20-30 emails for accuracy
4. **Refine System Message**: Adjust instructions based on results
5. **Rate Limits**: Be aware of OpenAI API rate limits and costs

## 🚨 Troubleshooting

### Workflow Not Triggering

- Check Gmail OAuth credentials are valid
- Verify workflow is activated (toggle is green)
- Ensure polling frequency is set correctly

### Labels Not Applied

- Verify labels exist in your Gmail account
- Check OpenAI API key is valid and has credits
- Review workflow execution logs for errors

### Incorrect Categorization

- Update the system message with more specific instructions
- Add examples of good categorizations
- Consider using a more powerful OpenAI model (e.g., GPT-4)

## 💰 Cost Estimate

- **n8n**: Free (Community) or $20/month (Starter)
- **OpenAI API**: ~$0.002-0.06 per email (depending on model)
- **Gmail API**: Free (up to 1 billion requests/day)

**Example**: Processing 500 emails/day with GPT-3.5-turbo ≈ $1-3/month

## 🔒 Security & Privacy

- OAuth credentials stored securely in n8n
- Email content processed by OpenAI (review their privacy policy)
- No email content stored permanently in n8n
- Only label metadata sent back to Gmail

## 📈 Next Steps

Once running smoothly, consider:
- Adding more labels for finer categorization
- Creating follow-up workflows (e.g., auto-reply to urgent emails)
- Integrating with ticketing systems
- Adding sentiment analysis

## 🤝 Need Help?

- [n8n Community Forum](https://community.n8n.io)
- [n8n Documentation](https://docs.n8n.io)
- [OpenAI API Docs](https://platform.openai.com/docs)

---

**Workflow File**: `email-triage-agent.json`
**Category**: Customer Service → Support Workflows
**Version**: 1.0.0
**Last Updated**: November 19, 2025
