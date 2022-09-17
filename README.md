# Lol JY Bot

A telegram bot just for fun among friends.

Created with [Telegram Bot API](https://core.telegram.org/bots/api).

Deployed on AWS Lambda, with [Lambda function URL](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html) as the trigger.

---

## Local setup

Use [Poetry](https://python-poetry.org/) for dependency management and virtual environment.

"bot.py" is the main file to run.

[Flask](https://flask.palletsprojects.com/) is used to set up a simple web application running on localhost with just the root route (eg. localhost:5000).

[ngrok](https://ngrok.com/) is used to obtain a temporary public URL that forwards HTTP requests to localhost. Run `.\ngrok http 5000` to forward traffic from the public URL to localhost:5000.

There are two ways of [getting updates](https://core.telegram.org/bots/api#getting-updates) from your Telegram bot. This is using webhooks.

After obtaining the public URL, inform Telegram server to send bot updates to that public URL by sending a HTTP GET request to `https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={PUBLIC_URL}`.

Once the above is done, you can start sending messages to your Telegram bot to test. Telegram will send updates (eg. messages) from your bot to the webhook (public) URL, which then forwards the request to your Flask app.

---

## Deploy on AWS Lambda

Create a new Lambda function on AWS. Use Lambda function URL as the trigger. This URL will replace the public URL used above in local.

Lambda function code mainly resides in "bot_lambda.py". It does not work if run locally.

No third party dependencies are required.

Code in "bot.py" will need to be tweaked to fit the Lambda function structure. Details about the HTTP request is stored in the "event" parameter. Play around with the function to understand how it works. Each request to the function URL, including "print()" statements, will be logged to AWS CloudWatch by default.

---

## Acknowledgement

Credits to [this guide](https://www.freecodecamp.org/news/how-to-build-a-server-less-telegram-bot-227f842f4706/) on freeCodeCamp for the idea of setting up a local webhook server.