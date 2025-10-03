# GTAPinguApp
An averagely useful bot for Discord.

# Setup Instructions (No Docker)

- Clone the repository and switch to the newly created directory:

    ```
    git clone https://github.com/uaimio/GTAPinguApp.git
    cd GTAPinguApp
    ```
- Create the virtual environment and activate it:

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- Install the dependencies listed in `requirements.txt` using pip:

    ```
    pip install -r requirements.txt
    ```
- Add the environment variables to the venv, specifically in `.venv/bin/activate`:

    ```
    # --- context
    export GTPTOKEN="YOUR_TOKEN"
    export PLS_STRING="YOUR_BASE64_ENCODED_PYTHON_CODE"
    ```
- Set execution permissions for the routine scripts:

    ```
    chmod 0644 planned_activities_local/garbage_collector.sh
    chmod 0644 planned_activities_local/planned_activities.sh
    ```
- Set up cron for the routine scripts:

    ```
    crontab planned_activities.sh
    ```
- Start the bot

    ```
    python bot.py & disown
    ```