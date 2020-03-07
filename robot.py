from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules

from commands.intel import get_intel_screenshot
from commands.help import get_documents
from logger import getLogger
from chromedriver import ChromeDriver
from settings import TOKEN


# message reply function
def get_message(bot, update):
    if str(update.message.text).startswith('/'):
        update.message.reply_text("지원하지 않는 명령어입니다.")
    else:
        update.message.reply_text("답장 기능이 제공되지 않습니다.")


# commands
def intel_command(bot, update):
    get_intel_screenshot(robot, bot, update)


def help_command(bot, update):
    get_documents(robot, bot, update)


def not_supported_command(bot, update):
    update.message.reply_text("준비중인 기능입니다.")


# main logic
def run():
    updater = Updater(TOKEN)

    intel_handler = CommandHandler('intel', intel_command)
    updater.dispatcher.add_handler(intel_handler)

    help_handler = CommandHandler('help', help_command)
    updater.dispatcher.add_handler(help_handler)

    link_handler = CommandHandler('link', not_supported_command)
    updater.dispatcher.add_handler(link_handler)

    subscribe_handler = CommandHandler('subscribe', not_supported_command)
    updater.dispatcher.add_handler(subscribe_handler)

    message_handler = MessageHandler(Filters.text, get_message)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling(timeout=1)
    updater.idle()


class Robot(object):
    def __init__(self):
        self.logger = getLogger()
        self.chrome = ChromeDriver(self)


if '__main__' == __name__:
    print('Initialize Robot Start...')
    robot = Robot()
    try:
        run()
        robot.logger.info('Initialize Robot Complete...')
    except KeyboardInterrupt as e:
        robot.logger.info('Honey Shutdown By User.')
    finally:
        robot.logger.info('Honey Shutdown.')
