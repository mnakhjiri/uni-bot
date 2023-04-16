from enum import Enum


class AdminSessionStates(Enum):
    WAITING_TO_SEND_ALERT = "adminWaitingAlert"
    WAITING_TO_SEND_TEST_ALERT = "adminWaitingTestAlert"

    def __get__(self, instance, owner):
        return str(self.value)
