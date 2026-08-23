from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.crypto import sha1_upper, analyze_password
from services.pwned import check_password_pwned, PwnedCheckError
from services.xposed import check_email_xposed, XposedCheckError
from utils.validators import validate_password, validate_email

router = Router()

class CheckInformation(StatesGroup):
    choosing_information = State()
    entering_password = State()
    entering_email = State()

class PasswordCB(CallbackData, prefix="password"):
    pass

class EmailCB(CallbackData, prefix="email"):
    pass

def build_choice_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Пароль", callback_data=PasswordCB().pack())
    builder.button(text="Почту", callback_data=EmailCB().pack())

    return builder.as_markup()

@router.message(Command("check"))
async def check(message: types.Message, state: FSMContext):
    data = {
        "password": "",
        "email": ""
    }
    await state.set_data(data)
    await state.set_state(CheckInformation.choosing_information)
    await message.answer("Что вы хотите проверить?", reply_markup=build_choice_keyboard())

@router.callback_query(PasswordCB.filter())
async def on_password(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CheckInformation.entering_password)
    if callback.message is not None and isinstance(callback.message, types.Message):
        await callback.message.answer("Введите пароль, который вы хотите проверить:")
    await callback.answer()

@router.callback_query(EmailCB.filter())
async def on_email(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CheckInformation.entering_email)
    if callback.message is not None and isinstance(callback.message, types.Message):
        await callback.message.answer("Введите почту, который вы хотите проверить:")
    await callback.answer()

@router.message(CheckInformation.entering_password)
async def on_entering_password(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer("Пришли пароль текстом, пожалуйста.")
        return

    is_valid, error = validate_password(message.text.strip())
    if error:
        await message.answer(error)
        return

    password = message.text.strip()

    data = await state.get_data()
    data["password"] = password
    await state.set_data(data)
    await state.clear()

    hashed = sha1_upper(password)
    # Удаляем сообщение с паролем из чата
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    try:
        count = check_password_pwned(hashed)
    except PwnedCheckError as exc:
        await message.answer(f"{exc}")
        return

    hard = analyze_password(password)

    if count > 0:
        await message.answer(
            f"Результат проверки пароля\n\n"
            f"Пароль найден в утечках!\n"
            f"Встречается <b>{count}</b> раз(а).\n\n"
            f"Рекомендуем сменить пароль!\n\n"
            f"Сложность вашего пароля: {hard.get("level")}",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"Результат проверки пароля\n\n"
            f"Пароль не найден в утечках.\n"
            f"Можешь использовать его спокойно.\n\n"
            f"Сложность вашего пароля: {hard.get("level")}",
            parse_mode="HTML"
        )

@router.message(CheckInformation.entering_email)
async def on_entering_email(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer("Пришли почту текстом, пожалуйста.")
        return

    is_valid, error = validate_email(message.text.strip())
    if error:
        await message.answer(error)
        return

    email = message.text.strip()

    data = await state.get_data()
    data["email"] = email
    await state.set_data(data)
    await state.clear()

    try:
        breaches = check_email_xposed(email)
    except XposedCheckError as exc:
        await message.answer(f"{exc}")
        return

    if len(breaches) == 0:
        await message.answer(
            f"Результат проверки почты\n\n"
            f"Почта не найдена в утечках\n\n"
            f"*проверено по открытой базе XposedOrNot, которая может не содержать все известные утечки",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"Результат проверки почты\n\n"
            f"Почта найдена в утечках!\n"
            f"Встречается <b>{len(breaches)}</b> раз(а).\n\n"
            f"Вот откуда были утечки:\n{breaches}",
            parse_mode="HTML"
        )