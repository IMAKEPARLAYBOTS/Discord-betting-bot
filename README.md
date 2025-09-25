# Discord Betting Bot

A modular Discord bot using discord.py with a ticket system for sports betting analysis on PrizePicks (extendable to Underdog, Sleeper, etc.).

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Install Tesseract OCR: On Ubuntu: `sudo apt install tesseract-ocr`; on Windows/Mac: Download from official site.
3. Fill in `config.py` with your tokens and IDs.
4. Run the bot: `python main.py`
5. For Replit: Upload all files, set up secrets for tokens, and configure UptimeRobot to ping `https://your-replit-app.repl.co/` every 5 mins.

## Commands
- `!ticket`: Creates a private ticket channel.
- `!parlay`: In ticket channel, attach a PrizePicks lineup image for analysis.

## Extending
Add modules in `main.py` for other platforms by creating new analysis functions.

## Notes
- This is a skeleton; implement placeholders for full functionality.
- Ensure OpenAI API usage complies with terms.
