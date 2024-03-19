from subprocess import check_output
from django.conf import settings


def is_channel_inactive(channel_tag: str) -> bool:
    output = check_output(["python", str(settings.BASE_DIR) + "/telemetr_api.py", channel_tag])
    return bool(int(output))
