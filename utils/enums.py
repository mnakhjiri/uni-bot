from enum import Enum


class AdminSessionStates(Enum):
    WAITING_TO_SEND_ALERT = "adminWaitingAlert"

    def __get__(self, instance, owner):
        return str(self.value)
