from aiogram import Router, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.crypto import analyze_password, build_alphabet, generate_password
from utils.validators import validate_password_length

router = Router()


class PasswordGen(StatesGroup):
    choosing_length = State()
    choosing_options = State()
    entering_custom_length = State()


class NextCB(CallbackData, prefix="next"):
    pass


class BackCB(CallbackData, prefix="back"):
    pass


class LengthCB(CallbackData, prefix="len"):
    value: int  # 8, 12, 16, 24, 32


class ToggleCB(CallbackData, prefix="toggle"):
    field: str


class GenerateCB(CallbackData, prefix="gen"):
    pass


def build_length_keyboard(data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for length in (8, 12, 16, 24, 32):
        mark = "✅" if data["length"] == length else ""
        builder.button(text=f"{mark}{length}", callback_data=LengthCB(value=length))
    builder.button(text="Своя длина ✏️", callback_data=LengthCB(value=0))
    builder.adjust(3, 3)
    builder.row(InlineKeyboardButton(text="Далее ➡️", callback_data=NextCB().pack()))
    return builder.as_markup()


def build_options_keyboard(data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=BackCB().pack()))

    def flag(name, label):
        mark = "✅" if data[name] else "⬜"
        builder.row(
            InlineKeyboardButton(
                text=f"{mark} {label}", callback_data=ToggleCB(field=name).pack()
            )
        )

    flag("use_letters", "буквы")
    flag("use_digits", "цифры")
    flag("use_symbols", "символы")
    flag("exclude_similar", "исключить похожие (Il1O0)")

    builder.row(
        InlineKeyboardButton(text="🔐 Сгенерировать", callback_data=GenerateCB().pack())
    )
    return builder.as_markup()


@router.message(Command("password"))
async def password(message: types.Message, state: FSMContext):
    data = {
        "length": 16,
        "use_letters": True,
        "use_digits": True,
        "use_symbols": True,
        "exclude_similar": False,
    }
    await state.set_data(data)
    await state.set_state(PasswordGen.choosing_length)
    await message.answer(
        "Выбери длину пароля:", reply_markup=build_length_keyboard(data)
    )


@router.callback_query(LengthCB.filter())
async def on_length(
    callback: types.CallbackQuery, callback_data: LengthCB, state: FSMContext
):
    if callback_data.value == 0:
        await state.set_state(PasswordGen.entering_custom_length)
        await callback.message.answer("Пришли число от 4 до 128.")
        await callback.answer()
        return

    data = await state.get_data()
    data["length"] = callback_data.value
    await state.set_data(data)
    await callback.message.edit_reply_markup(reply_markup=build_length_keyboard(data))
    await callback.answer()


@router.callback_query(NextCB.filter())
async def on_next(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(PasswordGen.choosing_options)
    await callback.message.edit_text(
        f"Длина: {data['length']}. Настрой параметры и нажми «Сгенерировать»:",
        reply_markup=build_options_keyboard(data),
    )
    await callback.answer()


@router.callback_query(BackCB.filter())
async def on_back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(PasswordGen.choosing_length)
    await callback.message.edit_text(
        "Выбери длину пароля:", reply_markup=build_length_keyboard(data)
    )
    await callback.answer()


@router.callback_query(ToggleCB.filter())
async def on_toggle(
    callback: types.CallbackQuery, callback_data: ToggleCB, state: FSMContext
):
    data = await state.get_data()
    data[callback_data.field] = not data[callback_data.field]

    if not (data["use_letters"] or data["use_digits"] or data["use_symbols"]):
        data[callback_data.field] = True  # не даём выключить всё разом
        await callback.answer(
            "Должен остаться хотя бы один тип символов", show_alert=True
        )
        return

    await state.set_data(data)
    await callback.message.edit_reply_markup(reply_markup=build_options_keyboard(data))
    await callback.answer()


@router.callback_query(GenerateCB.filter())
async def on_generate(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    alphabet = build_alphabet(
        data["use_letters"],
        data["use_digits"],
        data["use_symbols"],
        data["exclude_similar"],
    )
    pas = generate_password(data["length"], alphabet)
    hard = analyze_password(pas)

    await callback.message.edit_text(
        f"🔐 Сгенерирован пароль ({data['length']} символов):\n"
        f"`{pas}`\n"
        f"Сложность пароля: {hard.get('level')}",
        parse_mode="Markdown",
    )
    await callback.answer()


@router.message(PasswordGen.entering_custom_length)
async def on_custom_length(message: types.Message, state: FSMContext):
    length, error = validate_password_length(message.text.strip())
    if error:
        await message.answer(error)
        return

    data = await state.get_data()
    data["length"] = length
    await state.set_data(data)
    await state.set_state(PasswordGen.choosing_length)

    await message.answer("Длина обновлена:", reply_markup=build_options_keyboard(data))
