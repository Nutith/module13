from os import getenv
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ]
    ],
    resize_keyboard=True
)

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.message_handler(text='Информация')
async def info_message(message):
    await message.answer('Бот выполняет расчет каллорий на основе предоставленных данных')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {calories:.2f}')
    await UserState.callback.answer()
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f'10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    UserState.callback = call


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
