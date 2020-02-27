#!/usr/bin/env python

import datetime
import optparse
import os
import dateutil.relativedelta
import slacker
from dotenv import load_dotenv
from slack_cleaner2 import *

load_dotenv(".envrc")


def main():
    parser = optparse.OptionParser("%prog " + "[OPTIONS]")

    parser.add_option("-l", "--log", action="store_true", dest="logfile", default=False,
                      help="Save the log to a log file.")
    parser.add_option("-d", "--dryrun", action="store_true", dest="dry_run", default=False,
                      help="Specify the dry run mode.")
    parser.add_option("-c", "--channel", action="store", type="string", dest="channel",
                      default=os.environ.get("SLACK_CHANNEL"),
                      help="Specify the channel. If you want a default setting, you can set the environment variable SLACK_CHANNEL in the .envrc file.")
    parser.add_option("-m", "--month", action="store", type="int", dest="month", default=1,
                      help="Specify the retention period(month).")
    (options, args) = parser.parse_args()
    if (options.logfile is None) & (options.dry_run is None):
        print
        print("You can also specify options.")
        parser.usage

    s = Slack(options.logfile, options.dry_run)

    s.clean_old(options)
    s.logger_message()


class Slack():
    # https://slack-cleaner2.readthedocs.io/en/latest/modules.html

    def __init__(self, logfile, dry_run):
        self.logfile = logfile
        self.dry_run = dry_run

    def clean_old(self, options):
        s = SlackCleaner(os.environ.get("SLACK_TOKEN"), sleep_for=0.5, log_to_file=self.logfile)

        # If gmail, that require parameter of the following because large contents.
        s.api.conversations.rate_limit_retries = 500
        s.api.conversations.timeout = 500
        s.api.conversations.count = 5000

        ## list of all kind of channels
        # print(s.conversations)

        ## list of all channels. However, non private channels and DM
        # print(s.channels)

        ## list of all private channels.
        # print(s.groups)

        ## list of DM.
        # print(s.ims)

        # How many months save messages?
        retention_period = options.month

        while True:
            try:
                if options.channel in str(s.groups):
                    for msg in s.msgs(filter(match(options.channel),
                                             s.groups)):  # Don't use before= and after=, because of if that private channel, invalid_cursor error for a limit over.
                        if msg.ts <= a_while_ago(months=retention_period):
                            print("Will delete ", msg.json)
                            self.delete(msg, options)
                else:
                    for msg in s.msgs(filter(match(options.channel),
                                             s.conversations),
                                      before=a_while_ago(months=retention_period)):
                        print("Will delete ", msg.json)
                        self.delete(msg, options)

            except slacker.Error as e:
                print(e)

            finally:
                print("Delete completed.")
                today = datetime.datetime.now()
                search_before_date = today + dateutil.relativedelta.relativedelta(months=-retention_period)
                search_after_date = search_before_date + dateutil.relativedelta.relativedelta(weeks=-2)
                print()
                print(f"\033[1;36mSearch \033[1;32m'in:#{options.channel} after:{search_after_date.date()}"
                      f" before:{search_before_date.date()}'"
                      "\033[1;36m in the Slack search form.\033[0m")
                break

    def delete(self, msg: iter, options: optparse.Values) -> None:
        if self.dry_run:
            print(f"Dry run finished: {msg.text}")
        else:
            msg.delete()
            print(f"The old message for the {options.channel} was deleted."
                  f"\033[1;34m Please make sure {options.channel}. \033[0m")

    def logger_message(self):
        if self.logfile:
            print("\033[1;34mYou can check log: ./slack-cleaner.YYYYMMDD-Hms.log\033[0m")
            print()
            print("\033[1;33mIf clean up, run: rm ./slack-cleaner.*.log\033[0m")


if __name__ == '__main__':
    main()
