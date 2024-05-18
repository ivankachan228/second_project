# constants.py
import codecs

import requests


# main.py
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import InputFile
from aiogram.enums.dice_emoji import DiceEmoji
import re
import config
import utils
TOKEN = config.BOT_TOKEN
tag = ""
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Привет, {(message.from_user.full_name)}! Жмакай на кнопочки и всё поёмешь)")
@dp.message(Command('help'))
async def command_help_handler(message: types.Message):
    predicted_tag = utils.CheckerOfUser(message.from_user.full_name)
    if predicted_tag != " ":
        await message.reply(f"Вижу, ты тут уже был. Твой тег в нашей базе данных {predicted_tag}\n Если это не он, введи новый ")
        tag = predicted_tag
    await message.reply(
        "Это бот специально для таких же любиетелей бравлика, как и его создатель! "
        "Тут ты можешь узнать статистику своего аккаунта\n"
        "вот описание функций данного бота\n"
        "1)нажми /bs для старта\n"
        "2)нажми /numtroph для просмотра числа кубков на твоем аккаунте\n"
        "3)введи запрос вида /brawler_stat {ИМЯ_БРАВЛЕРА_КАПСОМ} (например, PAM или MORTIS или даже можно ELPRIMO) и узнай всю информацию об этом бойце")

@dp.message(Command('bs'))
async def command_help_handler(message: types.Message):
    """Handle the /bs command"""
    await message.reply("Напиши мне свой тег и я скажу число трофеев у тебя! (пиши без #)")


@dp.message(Command('numtroph'))
async def num_troph_handler(message: types.Message):
    """Handle the /numtroph command"""
    ans = utils.PrinterTroph()
    await message.reply(f"число трофеев у вас: {ans}")


@dp.message(Command('brawler_stat'))
async def brawler_stat_handler(message: types.Message):
    if (message.text == "/brawler_stat"):
        await message.reply("вы не ввели имя персонажа. я хочу видеть запрос вида /brawler_stat MORTIS")
    brawler_name = message.text.split()[1]
    if (brawler_name == ""):
        await message.reply("вы не ввели имя персонажа. я хочу видеть запрос вида /brawler_stat MORTIS")
    ans = utils.PrinterTrophOfBrawler(brawler_name)
    # photo_path = f'brawlers_photo/{brawler_name}.jpg'
    # photo_path = "brawlers_photo / PAM.webp"
    info_text = (
        f"Информация о {brawler_name}:\n"
        f"Максимум трофеев: {ans[4]}\n"
        f"Текущее число трофеев: {ans[3]}\n"
        f"Максимальный ранг бойца: {ans[2]}\n"
        f"Уровень силы бойца: {ans[1]}"
    )
    await message.reply(info_text)
@dp.message(Command('boost_of_trophies'))
async def boost_of_trophies(message: types.Message):
    answer = utils.PrinterBoosts()
    info_text = (
        f"Динамика твоих трофеев:\n"
        f"Прирост за эту неделю: {answer[0]}\n"
        f"Прирост за сезон: {answer[1]}\n"
    )
    await message.reply(info_text)
@dp.message(Command('full_info'))
async def full_info(message: types.Message):
    answer = utils.InfoPlayer()
    info_text = (
        f"Твоя статистика по режимам:\n"
        f"Победы в 3 на 3: {answer[0]}\n"
        f"Победы в одиночном столкновении: {answer[1]}\n"
        f"Победы в парном столкновении: {answer[2]}\n"
    )
    await message.reply(info_text)
@dp.message(Command('about_brawlers'))
async def about_brawlers(message: types.Message):
    answer = utils.Brawlers()
    info_text = (
        f"Общая статистика по бойцам:\n"
        f"Всего в игре бойцов на данный момент: {answer[1]}\n"
        f"У тебя бойцов: {answer[0]}\n"
        f"Процент покрытия бойцов: {answer[2]}%\n"
    )
    await message.reply(info_text)

@dp.message()
async def char_count_handler(message: types.Message) -> None:
    """Handle any other message"""
    input = message.text
    if re.search(r'\d', input) and len(input) == 9:
        predicted_tag = utils.CheckerOfUser(message.from_user.full_name)
        print(predicted_tag)
        if predicted_tag == " ":
            tag = input
            with codecs.open('database.txt', 'a', encoding='utf-8') as file:  # 'a' mode for appending
                file.write(tag + " ")  # Adding a newline after tag for readability
                file.write(message.from_user.full_name + "\n")  # Adding a newline after the full name for readability
            url = "https://brawlify.com/ru//stats/profile/"
            url += tag
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad status codes
            except requests.RequestException as e:
                await message.reply(f"Ошибка при загрузке страницы: {e}")
                return
            html = response.text
            with codecs.open('output.txt', 'w', encoding='utf-8') as file:
                file.write(html)
            await message.reply(f"1Отлично! Я запомнил твой тег. Далее можешь узнать информацию о своём профиле.")
        else:
            tag = input
            utils.RewriteTag(tag, message.from_user.full_name)
            with codecs.open('database.txt', 'a', encoding='utf-8') as file:  # 'a' mode for appending
                file.write(tag + " ")  # Adding a newline after tag for readability
                file.write(
                    message.from_user.full_name + "\n")  # Adding a newline after the full name for readability
            url = "https://brawlify.com/ru//stats/profile/"
            url += tag
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad status codes
            except requests.RequestException as e:
                await message.reply(f"Ошибка при загрузке страницы: {e}")
                return
            html = response.text
            with codecs.open('output.txt', 'w', encoding='utf-8') as file:
                file.write(html)
            await message.reply(f"Отлично! Перезаписал твой тег с {predicted_tag} на {tag}. Далее можешь узнать информацию о своём профиле.")
    else:
        await message.reply("Если ты вводил тег, то он не валиден. Он должен выглядеть как мой: YJRQ0Y8R9")


async def main() -> None:
    """Main function"""
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
