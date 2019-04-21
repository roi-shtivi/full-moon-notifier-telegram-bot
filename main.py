import os
import datetime

from telegram.ext import Updater, CommandHandler
import telegram.error

import jobs_pickle
import subscribers_db

s_db = subscribers_db.SubscribersDatabase()
full_moon_times = [datetime.datetime.now() + datetime.timedelta(0, 10),
                   datetime.datetime.now() + datetime.timedelta(0, 20),
                   ]


def start(update, context):
    chat_id = context.message.chat_id
    update.send_message(chat_id=chat_id, text="Welcome")
    s_db.insert(chat_id)


def broadcast(bot, job):
    time = job.context['time']
    for chat_id in s_db.get_all_subscribers():
        try:
            bot.send_message(chat_id=chat_id,
                             text="Raise your head to the sky and watch the full moon. "
                                  "The exact time is {}".format(time))
        except telegram.error.Unauthorized:
            s_db.delete(chat_id)


def set_jobs(job_queue):
    with open('full_moon_times.txt') as f:
        for str_time in [line.rstrip('\n') for line in f]:
            time = datetime.datetime.strptime(str_time, '%Y %b  %d %H:%M  %a')
            job = job_queue.run_once(broadcast, time, context={'time': time})
            job.name = str_time


def main():
    updater = Updater(os.environ['full_moon_notifier_bot_api_token'])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    jq = updater.job_queue

    # Periodically save jobs
    jq.run_repeating(jobs_pickle.save_jobs_job, datetime.timedelta(minutes=10))

    try:
        jobs_pickle.load_jobs(jq)

    except FileNotFoundError:
        # First run
        set_jobs(jq)

    updater.start_polling()
    updater.idle()

    # Run again after bot has been properly shut down
    jobs_pickle.save_jobs(jq)


if __name__ == '__main__':
    main()
