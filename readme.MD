# Telegram to Supabase Webhook Server 🚀

A lightweight Flask server that listens to incoming Telegram messages from a **group** or **channel**, processes them, and stores them into a **Supabase** database.

Perfect for use cases like:
- Newsflash banners for websites
- Message archives
- Auto-publishing pipelines

---

## 📐 Architecture Overview

    Telegram Group/Channel ➔ Flask Webhook ➔ Supabase DB ➔ (Client-side fetch)

- The Telegram bot posts a message.
- Telegram forwards the message to your Flask server via webhook.
- Flask server processes and saves it into Supabase.
- Your frontend fetches the latest messages from Supabase to display live.

---

## 🚀 Setup Guide

### 1. Create Supabase Table

Create a table in Supabase named `news` (or any name you prefer) with the following columns:

    +--------------+-------------------+-------------------------------+
    | Column       | Type              | Description                   |
    +--------------+-------------------+-------------------------------+
    | id           | UUID (Primary Key) | Unique ID (default random)     |
    | text         | Text               | The message text              |
    | fetched      | Boolean            | Whether the message was fetched (default false) |
    | created_at   | Timestamp          | When it was inserted (default now) |
    +--------------+-------------------+-------------------------------+

---

### 2. Create a Telegram Bot

- Talk to [@BotFather](https://t.me/botfather).
- Create a new bot and save the bot token.
- Add the bot to your **group or channel**.
- Promote the bot to **Admin** with "Post Messages" permission if working with a channel.
- Note the **chat ID** of the group/channel.

---

### 3. Set Up Your Environment Variables

Example `.env` file:

    SUPABASE_URL=Your Supabase project URL
    SUPABASE_API_KEY=Supabase API
    SUPABASE_TABLE=Table name
    ALLOWED_CHAT_ID=Chat ID (use -100 prefix if it's a channel)
    DEBUGGING_JSON=True/False (to print out JSON)
---

### 4. Running Locally

1. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the Flask server:
    ```bash
    python app.py
    ```
3. Expose your localhost to the internet with ngrok:
    ```bash
    ngrok http 5000
   ```
   
4. Set the Telegram webhook:
    ```bash
    curl -X POST "https://api.telegram.org/bot<YOUR-BOT-TOKEN>/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"https://your-ngrok-url/webhook\"}"
    ```

---

### 5. Deploying to Render (or other cloud platforms)

- Create a new **Web Service** on Render.
- Connect your GitHub repo containing this project.
- Set the required environment variables in the Render dashboard.
- Set the Telegram webhook to your Render URL:
    ```bash
    https://api.telegram.org/bot<YOUR-BOT-TOKEN>/setWebhook?url=https://your-render-app.onrender.com/webhook
    ```
✅ The server is now live and accepting Telegram webhooks!

---

## 📦 Features

- Handles **group messages** and **channel posts**.
- Ignores system events like `my_chat_member`, `chat_member`, etc.
- Saves clean text messages into Supabase automatically.
- Logs incoming webhooks for debugging.
- Fully flushes logs.

---

## 🛡 Security Notes

- This version currently soft-accepts any POST and validates based on `chat_id`.
- For higher security, consider:
  - Validating user `from` fields.
- Supabase service key should not be exposed to users (backend only).

---

## 📄 License

This project is licensed under the MIT License.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

See the full [LICENSE](LICENSE) file for more details.
