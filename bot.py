import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app import load_tokens, enc, make_request, send_multiple_requests, daily_limit


BOT_TOKEN = "9081337217:AAHwnXlM27_4ss8I4E9UeY69pOfO3EAGj1o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Free Fire Auto-Like Bot mein aapka swagat hai!**\n\n"
        "Use karne ka tarika:\n"
        "`/like <UID> <REGION>`\n"
        "Example: `/like 13338991906 IND`",
        parse_mode="Markdown"
    )

async def like_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ Kripya UID aur Region dono dein!\nExample: `/like 13338991906 IND`", parse_mode="Markdown")
        return

    uid = args[0]
    region = args[1].upper()

    await update.message.reply_text(f"🔍 UID **{uid}** ({region}) par likes bheje ja rahe hain, thoda intezaar karein...", parse_mode="Markdown")

    try:
        tokens = load_tokens(region)
        if not tokens:
            await update.message.reply_text("❌ Is region ke liye tokens load nahi ho paaye.")
            return
            
        token = tokens[0]['token']
        encrypted_uid = enc(uid)
        if encrypted_uid is None:
            await update.message.reply_text("❌ UID encryption fail ho gaya.")
            return
        
        before = make_request(encrypted_uid, region, token)
        if before is None:
            await update.message.reply_text("❌ Initial player info fetch karne mein error aaya.")
            return
        before_like = before.AccountInfo.Likes

        if region == "IND":
            url = "https://client.ind.freefiremobile.com/LikeProfile"
        elif region in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/LikeProfile"
        else:
            url = "https://clientbp.ggpolarbear.com/LikeProfile"

            
        await send_multiple_requests(uid, region, url)

        
        