import sqlite3
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Command

from keyboards import sexKeyboard, ageKeyboard, websiteKeyboard, sendingKeyboard, envelopeKeyboard, decorKeyboard, abroadKeyboard

from main import bot, dp
from config import chat_id

# async def send_hello(dp):
#     await bot.send_message(chat_id = chat_id, text='Hello')

# @dp.message_handler(Command('start'))
# async def ask_sex(message: Message):
#     await message.answer('Добрый день! Этот опрос посвящен определению интересов нашей аудитории с целью увеличения ассортимента нашего интернет магазина открыток. Пожалуйста, ответьте на 7 вопросов:', reply_markup=sexKeyboard)
#

# @dp.message_handler(Text(equals=['Женский', 'Мужской']))
# async def get_sex(message: Message):
#     await message.answer(f'Вы выбрали {message.text}', reply_markup=ReplyKeyboardRemove())


from aiogram.dispatcher import FSMContext

from states import States

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(user_id: int, sex: bool, age: int, website: bool, sending: int, envelope: bool, decor: int,
                 abroad: bool):
    cursor.execute(
        'INSERT INTO users (user_id, sex, age, website, sending, envelope, decor, abroad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (user_id, sex, age, website, sending, envelope, decor, abroad))
    conn.commit()

@dp.message_handler(Command('start'), state=None)
async def question1(message: Message):
    await message.answer('Добрый день! Этот опрос посвящен определению интересов нашей аудитории с целью увеличения ассортимента нашего интернет магазина открыток. Пожалуйста, ответьте на 7 вопросов:')

    await message.answer('Ваш пол?',  reply_markup=sexKeyboard)

    await States.questionSex.set()


@dp.message_handler(state=States.questionSex)
async def question(message: Message, state: FSMContext):
    sex = message.text
    await state.update_data(
        {
            'sex': sex
        }
    )
    await message.answer('Сколько вам лет?',  reply_markup=ageKeyboard)
    await States.next()

@dp.message_handler(state=States.questionAge)
async def question(message: Message, state: FSMContext):
    if(message.text == 'Меньше 18 лет'):
        age = 0
    else:
        age = 1

    await state.update_data(
        {
            'age': age
        }
    )
    await message.answer('Используете ли вы сайты для посткроссинга?', reply_markup=websiteKeyboard)
    # data = await state.get_data()
    # age = data.get('age')
    # sex = data.get('sex')
    await States.next()

@dp.message_handler(state=States.questionWebsite)
async def question(message: Message, state: FSMContext):
    website = message.text
    await state.update_data(
        {
            'website': website
        }
    )
    await message.answer('Как часто вы отправляете открытки?',  reply_markup=sendingKeyboard)
    await States.next()

@dp.message_handler(state=States.questionSending)
async def question(message: Message, state: FSMContext):
    sending = message.text
    await state.update_data(
        {
            'sending': sending
        }
    )
    await message.answer('Пользуетесь ли вы конвртами?',  reply_markup=envelopeKeyboard)
    await States.next()

@dp.message_handler(state=States.questionEnvelope)
async def question(message: Message, state: FSMContext):
    envelope = message.text
    await state.update_data(
        {
            'envelope': envelope
        }
    )
    await message.answer('Как вы оформляете почтовую открытку?',  reply_markup=decorKeyboard)
    await States.next()

@dp.message_handler(state=States.questionDecor)
async def question(message: Message, state: FSMContext):
    decor = message.text
    await state.update_data(
        {
            'decor': decor
        }
    )
    data = await state.get_data()
    sex = data.get('sex')
    age = data.get('age')
    website = data.get('website')
    sending = data.get('sending')
    envelope = data.get('envelope')
    # decor = data.get('decor')
    await message.answer(f'В результате проведения опроса из хз человек было выяснено, что целевая аудитория это: {sex}, {age}, которые {website}, отправляют открытки {sending} {envelope}, оформляют {decor}')

    await message.answer('Отправляете ли вы открытки в другие страны?',  reply_markup=abroadKeyboard)
    await message.answer('ну ок')
    db_table_val(user_id=message.from_user.id, sex='true', age=0, website='true', sending=1, envelope='true', decor=1, abroad='false')
    await States.next()


@dp.message_handler(state=States.questionEnding)
async def ending(message: Message, state: FSMContext):
    await message.answer('ada')
    abroad = message.text
    await state.update_data(
        {
            'abroad': abroad
        }
    )
    await message.answer(f'{message.text}')
    await state.finish()

    # await message.answer('Все!', reply_markup=ReplyKeyboardRemove())
    # data = await state.get_data()
    # sex = data.get('sex')
    # age = data.get('age')
    # website = data.get('website')
    # sending = data.get('sending')
    # envelope = data.get('envelope')
    # decor = data.get('decor')
    #
    # await message.answer(f'В результате проведения опроса из хз человек было выяснено, что целевая аудитория это: {sex}, {age}, которые {website}, отправляют открытки {sending} {envelope}, оформляют {decor} и {abroad}')
