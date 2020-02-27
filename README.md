# slack sweeper

You can delete old messages in the your slack group channel. The default for this deletion is over a month ago.

## Credential configuration

### Get the token

You will need to generate a Slack legacy user token to use slack-cleaner.
Generate a token here: https://api.slack.com/custom-integrations/legacy-tokens.

### Set into a dotenv file for the credential of above Slack token

```shell script
echo "export SLACK_TOKEN=xoxp-xxxxxxxxxx" > ./.envrc
```

## If you want a default channel setting

```shell script
echo "export SLACK_CHANNEL=xxxxxx" > ./.envrc
```

## Local execution

### Requirements

- Python 3.7 or later
- pip

### Install

```shell script
pip install -r requirements.txt
```

### Usage

```shell script
python ./sweeper.py [OPTIONS]
```

### Help

```shell script
 python ./sweeper.py [-h|--help]
```

## Run in a container

### UseCase

- e.g. Development for AWS ECS + Scheduled Tasks(cron)

### Install

```shell script
make
```

### Help

```shell script
make help
```

### Run

```shell script
$ vagrant ssh
vagrant@my-app:~/$ cd app
vagrant@my-app:~/$ docker build -t <name>:<tag> .
vagrant@my-app:~/app$ docker run -it --rm <name>:<tag> /root/sweeper.py -h
% ./sweeper.py -h
Usage: sweeper.py [OPTIONS]

Options:
  -h, --help            show this help message and exit
  -l, --log             Save the log to a log file.
  -d, --dryrun          Specify the dry run mode.
  -c CHANNEL, --channel=CHANNEL
                        Specify the channel. If you want a default setting,
                        you can set the environment variable SLACK_CHANNEL in
                        the .envrc file.
  -m MONTH, --month=MONTH
                        Specify the retention period(month).
```

If actually delete them, run the following command.

```shell scirpt
vagrant@my-app:~/app$ docker run -it --rm <name>:<tag>
```
  - Run by default.

or

```shell scirpt
vagrant@my-app:~/app$ docker run -it --rm <name>:<tag> /root/sweeper.py [-l|-c <CHANNEL>|-m <MONTH>]
```

### Ref.

- "Docker for Mac" is not used.
  - https://qiita.com/yuki_ycino/items/cb21cf91a39ddd61f484
