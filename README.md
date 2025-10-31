---
title: career-chat-bot
app_file: app.py
sdk: gradio
sdk_version: 5.49.1
---
# Career Chat Bot

A personalized AI chatbot that represents you professionally, encouraging detailed questions about your experience and skills while collecting contact information from interested users.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

**For Local Development:**
1. Copy `env_template.txt` to `.env`
2. Fill in your actual API keys:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PUSHOVER_USER`: Your Pushover user ID (for notifications)
   - `PUSHOVER_TOKEN`: Your Pushover app token

**For Hugging Face Spaces Deployment:**
1. Go to your Space settings → Secrets and variables → Secrets
2. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PUSHOVER_USER`: Your Pushover user ID (for notifications)
   - `PUSHOVER_TOKEN`: Your Pushover app token

### 3. Required Files
The following files must be present in the `me/` directory:

**Currently Present:**
- `B. Colby Hood Resume.pdf` ✅
- `Interview Prep.pdf` ✅ 
- `Psychological_Profile_Bryant_Colby_Hood.pdf` ✅

**Missing Files (need to be added):**
- `linkedin.pdf` - Your LinkedIn profile exported as PDF
- `summary.txt` - A text summary of your background and experience

### 4. Run the Application
```bash
python app.py
```

The chatbot will launch in your browser and will:
- Actively encourage users to ask detailed questions about your experience and skills
- Steer interested users toward providing contact information
- Send you push notifications when users share their contact details
- Record questions it cannot answer for your review

## Features
- Professional AI representation of your background
- Automatic contact information collection
- Push notifications for new leads
- Knowledge gap tracking for continuous improvement
