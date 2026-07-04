from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from src.keyboards import keyboard_main, inline

router = Router()

users = {}

class Register(StatesGroup):
    name = State()
    age = State()
    confirm = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
        await message.answer(
                f"Привет {message.from_user.first_name}! показывает приветствие и кнопку ", reply_markup=keyboard_main)

         

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start\n'
        '/help\n'
        '/profile'
    )

@router.message(Command('profile'))
async def cmd_profile(message: Message):
    user_id = message.from_user.id
    
    if user_id in users:
        user = users[user_id]
        await message.answer(
                f'твой профиль:\n'
                f"Имя: {user['name']}\n"
                f"Возраст: {user['age']}"
        )
    else:
        await message.answer(
            "ты не зареган, есть ли хош зарегайся",
            reply_markup=keyboard_main
        )



@router.message(F.text =='ты не зареган, есть ли хош зарегайся')
async def register_start(message: Message, state: FSMContext):
    await message.answer(" ваше имя: ")
    await state.set_state(Register.name)


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(" ваш возраст:")
    await state.set_state(Register.age)


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(" нужна цифра")
        return
    await state.update_data(age=message.text)
    data = await state.get_data()

    user_id = message.from_user.id

    users[user_id] = {
        "name": data["name"],
        "age": message.text
    }#slovarik



    await message.answer(
        f"Регистрация завершена!\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {message.text}"
        f'подтверждаете?',
        reply_markup=inline
    )
    await state.set_state(Register.confirm)
    
@router.callback_query(Register.confirm,F.data == "Da" )
async def confirm_register(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    users[user_id] = {
        "name": data["name"],
        "age": data["age"]
    }

    await state.clear()

    await callback.answer()
    await callback.message.answer("Регистрация завершена!")


@router.callback_query(Register.confirm, F.data == "e51an")
async def restart_register(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer()
    await callback.message.answer("Хорошо, начнем заново. Введите ваше имя:")

    await state.set_state(Register.name)