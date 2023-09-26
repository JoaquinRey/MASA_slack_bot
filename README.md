# Synnax Slack Bot

The Synnax Slack Bot is intended to listen to changes in the data and metadata, and execute tools such as automated analysis scripts.

## TODO:
- Send file directly from request rather than downloading and then deleting
- Create command that returns a specified test and respective graph
- Dockerize the bot

## Instructions:

### Docker file
- `docker build -t synnax_bot .`
- `docker run -p 3000:3000 synnax_bot`

## Testing :

### Macbook

Make sure you are in the Tests directory, and then run `sudo sh {file_name}.sh {loopback address}`
<br>ex: `sudo sh test_request.sh "127.0.0.1"`
<br>note: You can obtain the loopback address by running `sudo sh get_loopback.sh`
