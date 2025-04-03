import telebot
import requests
import jsons
from Class_ModelResponse import ModelResponse

# Замените 'YOUR_BOT_TOKEN' на ваш токен от BotFather
API_TOKEN = '7674142884:AAHEVFm8kjMqIVGJzcRN1FfGb0yb5JNJs08'
bot = telebot.TeleBot(API_TOKEN)

# Хранилище контекста для каждого пользователя
user_contexts = {}

# Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет, друг мой любопытный!\n"
        "Меня зовут Лосяш, я радостью поговорю с тобой и отвечу на вопросы, используй эти команды:\n"
        "/start - вывод всех доступных команд\n"
        "/model - выводит название используемой языковой модели.\n"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['model'])
def send_model_name(message):
    # Отправляем запрос к LM Studio для получения информации о модели
    response = requests.get('http://localhost:1234/v1/models')

    if response.status_code == 200:
        model_info = response.json()
        model_name = model_info['data'][0]['id']
        bot.reply_to(message, f"Используемая модель: {model_name}")
    else:
        bot.reply_to(message, 'Не удалось получить информацию о модели.')


@bot.message_handler(commands=['clear'])
def clear_context(message):
    user_id = message.from_user.id
    if user_id in user_contexts:
        del user_contexts[user_id]
    bot.reply_to(message, "Контекст успешно очищен!")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_query = message.text
    
    # Инициализация контекста при первом сообщении
    if user_id not in user_contexts:
        user_contexts[user_id] = []
    
    # Добавляем новый запрос пользователя в контекст
    user_contexts[user_id].append({"role": "user", "content": user_query})
    
    # Формируем запрос с полной историей диалога
    request = {
        "messages": user_contexts[user_id]
    }
    
    response = requests.post(
        'http://localhost:1234/v1/chat/completions',
        json=request
    )

    if response.status_code == 200:
        model_response: ModelResponse = jsons.loads(response.text, ModelResponse)
        assistant_response = model_response.choices[0].message.content
        
        # Добавляем ответ ассистента в контекст
        user_contexts[user_id].append({
            "role": "assistant",
            "content": assistant_response
        })
        
        bot.reply_to(message, assistant_response)
    else:
        bot.reply_to(message, 'Произошла ошибка при обращении к модели.')

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)