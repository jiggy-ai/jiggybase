
from enum import Enum

 
class ChatModelName(str, Enum):
    gpt3_5_turbo :str = "gpt-3-5-turbo"
    gpt4         :str = "gpt-4"

    def __str__(self):
        return str(self.value)    