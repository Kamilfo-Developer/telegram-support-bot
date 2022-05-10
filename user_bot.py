from config import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import User
from data_module import Admin, UserQuestions
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

logger = logging.getLogger()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    user = User.get_current()
    full_name = user.full_name
    username = user.username
    logger.info(f"{full_name} with username {username} sent start command")
    
    await message.reply(f"Доброго времени суток, {user.first_name}!\nЯ - бот Яндекса от помогаторов!\nЗдесь Вы можете задать вопрос помогаторам!\nЧтобы узнать подробнее про то, как пользоваться ботом введить команду /help)))")



@dp.message_handler(commands=["help"])
async def handle_help(message: types.Message):
    user = User.get_current()
    full_name = user.full_name
    username = user.username

    message_to_send = ""

    if Admin.check_if_admin(user.id):
        admin = Admin(user.id)
        
        message_to_send = f"Вы администратор.\n\n"
        
        message_to_send += f"Список команд: \n/getquestion - вы получете вопрос, чтобы на него ответить просто введите текст и он будет отправлен пользователю. Внимание! После отправки текста изменить его будет нельзя! Вы можете только заново ввести текст и он будет отправлен пользователю, ответ изменится, но старое сообщение также останется.\n/getmychatid - возвращает пользователю его уникальный chat_id. Доступна даже для пользователей.\n\nСтатистика:\nВсего неотвеченных вопросов: {UserQuestions.get_unanswered_questions_number()}\nИз них доступных для ответа (это значит, что на эти вопросы никто не отвечает на данный момент): {UserQuestions.get_unanswered_questions_number(True)}"
    
        await message.reply(message_to_send)
        return
    
    message_to_send = f"Если Вы хотите задать вопос, то просто отправьте мне текст вопроса)))\nНо помните, после отправки вопрос нельзя изменить(((\n\nВот список доступных команд:\n/gethelperanswers - Вы получите список заданных вопросов и ответы на них (если они есть, конечно же)"
    
    

@dp.message_handler(commands=["gethelperanswers"])
async def handle_gethelperanswers(message: types.Message):
    user = User.get_current()
    user_id = user.id
    username = f"@{user.username}"
    full_name = user.full_name
    
    user_questions = UserQuestions(user_id)
    
    questions = user_questions.get_questions_data()
    

    if Admin.check_if_admin(user_id):
        await message.reply(f"Ты администратор, ты и так уже знаешь ответы на все вопросы)))")
    
        return
    
    
    
    if len(questions) == 0:
        await message.reply("Похоже Вы пока не задавали вопросов(((", parse_mode="html")
        
        return
    
    
    message_to_send = "Вот все Ваши вопросы:\n\n"
    message_to_log = f"{user.full_name} with nickname {user.username} required all the asked questions. Their ids: "
    
    for question in questions:
        if question["answer_text"] == "":
            
            message_to_log += f"{question['question_id']} "
            
            message_to_send += f"Вопрос:\n{question['question_text']}\n\n<b>Ответа пока нет(((\nПопробуйте проверить информацию позже)))</b>\n\n"
            
            continue
        
        message_to_send += f"Вопрос:\n{question['question_text']}\n\nОтвет:\n{question['answer_text']}\n\nНа этот вопрос ответил: {question['answer_author']}\n\n"
        
    message_to_send += f"С профессионализмом на кончиках пальцев - команда помогаторов Яндекса :)))"
    
    
    logger.info(f"{full_name} with username {username} required answers successfully")
    
    await message.reply(message_to_send, parse_mode="html")



@dp.message_handler(commands=["getquestion"])
async def handle_get_question(message: types.Message):
    user = User.get_current()
    
    if not Admin.check_if_admin(user.id):
        await message.reply("ЭЭЭЙ! Вы не помогатор!!!! Сюда нельзя!!!!! ;((((")
        
        return
    
    admin = Admin(user.id)
    
    if admin.current_question_id:
        admin.uncover_current_question()
    
    question = admin.require_random_question()
    
    if question:
        message_to_send = "" 

        if question.author != "@None" and question.author != "None":
            message_to_send += f"{question.author} прислал вопрос:\n\n{question.question_text}"
        
        else:
            message_to_send += f"Человек без ника прислал вопрос\n\n{question.question_text}"
        
        logger.info(f"{user.full_name} with nickname {user.username} required a new question to answer. Its id: {question.question_id}")
        
        await message.reply(message_to_send)
        return
    
    logger.info(f"{user.full_name} with nickname {user.username} tried to require a new question to answer, but none of them are available")
    await message.reply("Похоже, вопросов больше нет...")



@dp.message_handler(commands=["getmychatid"])
async def handle_get_my_chat_id(message: types.Message):
    user = User.get_current()
    
    logger.info(f"{user.full_name} with nickname {user.username} tried to required the chat_id, it is {user.id}")
    await message.reply(user.id)
    
    
    
@dp.message_handler(commands=["gethelperanswer"])
async def handler_get_helper_answer(message: types.Message):
    user = User.get_current()
    logger.info(f"{user.full_name} with username {user.username} required command /gethelperanswer, but it doesn't work now")
    await message.reply("Эта команда устарела(((\n\nВведите /gethelperanswers, чтобы получить список заданных вопросов и ответы на них (если они уже есть, конечно) :)))")
    

@dp.message_handler(commands=["skip"])
async def handle_skip(message: types.Message):
    user = User.get_current()

    if Admin.check_if_admin(user.id):
        admin = Admin(user.id)
        if admin.current_question_id:
            admin.skip_current_question()
            await message.reply("Выделение снято, теперь на этот вопрос может ответить кто-нибудь другой")
            return

        await message.reply("У тебя и так уже нет выделенного вопроса!")


        

@dp.message_handler()
async def handle_text(message: types.Message):
    user = User.get_current()
    username = f"{user.username}"
    full_name = user.full_name
    
    text = message.text
    
    if text[0] == "/" and len(text.split(" ")) == 1:
        logger.info(f"{full_name} with username {username} entered a non-existent command. Input: {message.text}")
        await message.reply("Такой команды нет((((")
        return 
    
    if not Admin.check_if_admin(user.id):
        user_questions = UserQuestions(user.id)
        
        user_questions.add_question(question_text=text, author=username)
        
        
        
        message_to_send = "Ваш вопрос успешно добавлен! Теперь ждите, пока наши помогающие помогаторы Вам ответят ;)))"
        
        logger.info(f"{full_name} with username {username} sent a question")
        await message.reply(message_to_send)
        
        return
    
    admin = Admin(user.id)
    
    if admin.current_question_id:
        
        question = admin.answer_current_question(text)
        
        author_id = question.user_id
        
        message_to_send = f"Помогатор {question.answer_author} ответил Вам:\n\nВаш вопрос:\n\n{question.question_text}\n\nНаш ответ:\n\n{question.answer_text}"
        
        logger.info(f"User with nickname {question.author} got an answer from {question.answer_author}, question_id: {question.question_id}")
        await bot.send_message(author_id, message_to_send)
        return
    
    await message.reply("У тебя нет вопроса, введи команду /getquestion, чтобы его получить!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)