from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from ip_tools import get_ip_info, speed_test, ping_host, get_ip_type
from vpn_manager import add_vpn, get_vpn_list

WAIT_VPN_NAME = 1
WAIT_VPN_LINK = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to VPN Tools Bot!\n\n"
        "Available commands:\n"
        "/ip [IP] - Get IP info\n"
        "/speed - Speed test\n"
        "/ping [host] - Ping host\n"
        "/iptype [IP] - Get IP type\n"
        "/vpn - VPN manager\n"
        "/help - Show help"
    )

async def ip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ip [IP address]")
        return
    ip = context.args[0]
    result = get_ip_info(ip)
    await update.message.reply_text(result, parse_mode='Markdown')

async def speed_test_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Running speed test... (this may take a minute)")
    result = speed_test()
    await update.message.reply_text(result, parse_mode='Markdown')

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ping [host]")
        return
    host = context.args[0]
    result = ping_host(host)
    await update.message.reply_text(result, parse_mode='Markdown')

async def iptype_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /iptype [IP address]")
        return
    ip = context.args[0]
    result = get_ip_type(ip)
    await update.message.reply_text(result, parse_mode='Markdown')

async def vpn_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_vpn_list()
    await update.message.reply_text(
        f"{text}\n\n"
        "Options:\n"
        "/vpnadd - Add new VPN\n"
        "/vpnlist - Show all VPNs"
    )

async def vpn_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Enter VPN name:")
    return WAIT_VPN_NAME

async def vpn_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['vpn_name'] = update.message.text
    await update.message.reply_text("🔗 Enter VPN link:")
    return WAIT_VPN_LINK

async def vpn_add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vpn_link = update.message.text
    vpn_name = context.user_data['vpn_name']
    result = add_vpn(vpn_name, vpn_link)
    await update.message.reply_text(result)
    return ConversationHandler.END

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **VPN Tools Bot Help**\n\n"
        "/start - Start bot\n"
        "/ip [IP] - Get geolocation info\n"
        "/speed - Test internet speed\n"
        "/ping [host] - Ping host\n"
        "/iptype [IP] - Analyze IP type\n"
        "/vpn - VPN manager\n"
        "/vpnadd - Add VPN\n"
        "/vpnlist - Show VPNs\n"
        "/help - Show this help",
        parse_mode='Markdown'
    )

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ip", ip_info))
    app.add_handler(CommandHandler("speed", speed_test_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("iptype", iptype_cmd))
    app.add_handler(CommandHandler("vpn", vpn_menu))
    app.add_handler(CommandHandler("vpnlist", vpn_menu))
    
    vpn_add_handler = ConversationHandler(
        entry_points=[CommandHandler("vpnadd", vpn_add_start)],
        states={
            WAIT_VPN_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, vpn_add_name)],
            WAIT_VPN_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, vpn_add_link)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )
    
    app.add_handler(vpn_add_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
