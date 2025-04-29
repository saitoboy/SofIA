from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.ext import CommandHandler

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Olá, {update.effective_user.first_name}!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Olá, eu sou a Sofia, inteligência virtual da Houer!\n"
        "No que posso ajudar? "
    )

def run_telegram_bot(token: str, rag_chain):
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        question = update.message.text
        answer = rag_chain.invoke({"input": question}).get("answer", "Sem resposta.")
        await update.message.reply_text(answer)

    app_telegram = ApplicationBuilder().token(token).build()
    app_telegram.add_handler(CommandHandler("hello", hello))
    app_telegram.add_handler(CommandHandler("start", start))  # <- Adicionamos o /start aqui
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_telegram.run_polling()
