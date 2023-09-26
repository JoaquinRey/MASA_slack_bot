# Synnax Slack Bot

The Synnax Slack Bot is intended to listen to changes in the data and metadata, and execute tools such as automated analysis scripts.

## TODO:
- Send file directly from request rather than downloading and then deleting
- Create command that returns a specified test and respective graph
- Dockerize the bot

## Instructions

### Docker
- `docker build -t synnax_bot .`
- `docker run -p 3000:3000 synnax_bot`

## Testing

### Macbook
- `sudo sh get_loopback.sh` - Gets the loopback address of the device
- `sudo sh test_file_send.sh {loopback address} {file path}` - Sends an image to the bot for it to post
- `sudo sh test_request.sh {loopback address}` - Sends a sample test payload to the bot
