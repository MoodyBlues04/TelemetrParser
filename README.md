# TelemetrParser
Simple python app to autommaticly parse channels from telemetr.io and upload to google sheets.

# Installation
1. Install [venv](https://docs.python.org/3/library/venv.html)
2. Clone this repository
3. Create venv using ```python -m venv venv``` and activate by typing ```source venv/bin/activate```
4. After installation run ```python -m pip install -r requirements.txt``` to install all project dependencies to virtual environment
5. Execute ```cp .env.example .env``` and fill environmental variables.

# Usage
- Run ```python manage.py parse_telemetr ``` to parse data from telemetr.io to google sheet specified in ```.env```