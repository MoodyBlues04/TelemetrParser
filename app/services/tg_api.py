from subprocess import check_output
from django.conf import settings

class TgApi:
    def is_channel_inactive(self, channel_tag: str) -> bool:
        print(settings.BASE_DIR)
        output = check_output(["python", settings.BASE_DIR.__str__() + "/telemetr_api.py", channel_tag])
        print(output)
        return bool(int(output))
