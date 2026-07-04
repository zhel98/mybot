from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

keyboard_main= ReplyKeyboardMarkup(
    keyboard=(
        [KeyboardButton(text='ты не зареган, есть ли хош зарегайся')],
), resize_keyboard=True, input_field_placeholder="на кнопку нажми")

inline = InlineKeyboardMarkup(
    inline_keyboard=[
        
    [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_register"),
    InlineKeyboardButton(text="Начать заново", callback_data="restart_register")]
    
    ])