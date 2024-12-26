import os
import time
import sqlite3
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from scraper import scrape_website, scrape_hackerone, scrape_bugcrowd
from ai_module import analyze_scraped_data, recommend_program, generate_report, extract_keywords, translate_text
from utils import fetch_rss
from db import init_db, update_points, get_leaderboard, set_user_pref, get_user_pref
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
BOT_TOKEN = os.getenv("7484460764:AAFOP5PDomeOy_H0oS9nNHBSbZOsC24nyzc")

# Initialize Database
init_db()

# Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Bug Bounty Finder Bot! Use /menu to see available options."
    )

# Scrape Command
def scrape(update: Update, context: CallbackContext):
    if context.args:
        url = context.args[0]
        try:
            data = scrape_website(url)
            update_points(update.effective_user.id, 10)
            update.message.reply_text(f"Scraped Data:\n{data[:500]}...")  # Limit output
        except Exception as e:
            update.message.reply_text(f"Error scraping the website: {e}")
    else:
        update.message.reply_text("Usage: /scrape <url>")

# AI-Powered Scraping
def scrape_ai(update: Update, context: CallbackContext):
    if context.args:
        url = context.args[0]
        try:
            data = scrape_website(url)
            analysis = analyze_scraped_data(data)
            update.message.reply_text(f"AI Analysis:\n{analysis}")
        except Exception as e:
            update.message.reply_text(f"Error: {e}")
    else:
        update.message.reply_text("Please provide a valid URL. Usage: /scrapeai <url>")

# Generate Report Command
def generate_report_cmd(update: Update, context: CallbackContext):
    if context.args:
        data = " ".join(context.args)
        try:
            report = generate_report(data)
            update.message.reply_text(f"Generated Report:\n{report}")
        except Exception as e:
            update.message.reply_text(f"Error generating report: {e}")
    else:
        update.message.reply_text("Please provide data to generate a report. Usage: /generatereport <data>")

# Extract Keywords Command
def extract_keywords_cmd(update: Update, context: CallbackContext):
    if context.args:
        data = " ".join(context.args)
        try:
            keywords = extract_keywords(data)
            update.message.reply_text(f"Extracted Keywords:\n{keywords}")
        except Exception as e:
            update.message.reply_text(f"Error extracting keywords: {e}")
    else:
        update.message.reply_text("Please provide data to extract keywords. Usage: /extractkeywords <data>")

# Translate Text Command
def translate_text_cmd(update: Update, context: CallbackContext):
    if len(context.args) >= 2:
        text = " ".join(context.args[:-1])
        target_language = context.args[-1]
        try:
            translation = translate_text(text, target_language)
            update.message.reply_text(f"Translated Text:\n{translation}")
        except Exception as e:
            update.message.reply_text(f"Error translating text: {e}")
    else:
        update.message.reply_text("Please provide text and target language. Usage: /translate <text> <target_language>")

# Leaderboard Command
def leaderboard(update: Update, context: CallbackContext):
    leaders = get_leaderboard()
    message = "\n".join([f"User: {user[0]} - Points: {user[1]}" for user in leaders])
    update.message.reply_text(message or "No leaderboard data available.")

# Recommend Command
def recommend(update: Update, context: CallbackContext):
    user_input = " ".join(context.args)
    if user_input:
        recommendation = recommend_program(user_input)
        update.message.reply_text(recommendation)
    else:
        update.message.reply_text("Usage: /recommend <keywords>")

# RSS Feed Command
def rss_feed(update: Update, context: CallbackContext):
    url = "https://www.hackerone.com/feeds/programs.rss"
    try:
        entries = fetch_rss(url)
        message = "\n\n".join([f"Title: {entry['title']}\nLink: {entry['link']}" for entry in entries[:5]])
        update.message.reply_text(f"Latest Bug Bounty Updates:\n{message}")
    except Exception as e:
        update.message.reply_text(f"Error fetching RSS feed: {e}")

# Interactive Menu
def interactive_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Scrape HackerOne", callback_data='scrape_h1')],
        [InlineKeyboardButton("Scrape Bugcrowd", callback_data='scrape_bc')],
        [InlineKeyboardButton("View Leaderboard", callback_data='leaderboard')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'scrape_h1':
        data = scrape_hackerone()
        query.edit_message_text(f"HackerOne Programs:\n{data}")
    elif query.data == 'scrape_bc':
        data = scrape_bugcrowd()
        query.edit_message_text(f"Bugcrowd Programs:\n{data}")
    elif query.data == 'leaderboard':
        leaders = get_leaderboard()
        message = "\n".join([f"User: {user[0]} - Points: {user[1]}" for user in leaders])
        query.edit_message_text(message or "No leaderboard data available.")

# Telegram Bot Setup
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("scrape", scrape))
dispatcher.add_handler(CommandHandler("scrapeai", scrape_ai))
dispatcher.add_handler(CommandHandler("generatereport", generate_report_cmd))
dispatcher.add_handler(CommandHandler("extractkeywords", extract_keywords_cmd))
dispatcher.add_handler(CommandHandler("translate", translate_text_cmd))
dispatcher.add_handler(CommandHandler("leaderboard", leaderboard))
dispatcher.add_handler(CommandHandler("recommend", recommend))
dispatcher.add_handler(CommandHandler("rss", rss_feed))
dispatcher.add_handler(CommandHandler("menu", interactive_menu))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

# Start Bot
updater.start_polling()
updater.idle()