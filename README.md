# Zorg-Bot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

Zorg-Bot is a multi purpose Discord bot. It is under very early development and is **not ready for production**.

## Self-Hosting

### ⚠️ **Reminder**

You may self host this bot on your own hardware **as long as you follow the [AGPL-3.0](https://github.com/joqwer/Zorg-Bot/blob/main/LICENSE)**.

### Instructions

1. Place your discord token in a `.env` file. Here is what it should look like.

```
DISCORD_TOKEN=Your-Token-Here!
```

2. Install dependencies by using `pipenv install`.

3. You should be done! This bot does not currently require intents.

## Activities

Have a cool idea for an activity to add to the bot? Here is how you can contribute your own. It should meet the following criteria:

1. It Follows [Discord's Community Guidelines](https://discord.com/guidelines)
2. It is original and unique
3. It is not terribly long

To contribute a new activity status, [Fork](https://github.com/joqwer/Zorg-Bot/fork) the repository. Then, edit `static/activities.json` with the following format.

```json
[
    ...
    {
        "status": "Playing", // Can be Playing, Listening to or Watching
        "message": "some games" // The message to display
    }, // Don't forget the comma!
]
```

This example will make the bot's status display `Playing some games`

Then, Open a [pull request](https://github.com/joqwer/Zorg-Bot/pulls) under the tag "Activity".

If your PR is merged, the bot will have a chance to randomly pick your status every hour.
