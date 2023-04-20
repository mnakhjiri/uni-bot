from enum import Enum


class BaseEnum(Enum):
    def __get__(self, instance, owner):
        return str(self.value)


class AdminSessionStates(BaseEnum):
    WAITING_TO_SEND_ALERT = "adminWaitingAlert"
    WAITING_TO_SEND_TEST_ALERT = "adminWaitingTestAlert"


class UserSessionStates(BaseEnum):
    WAITING_TO_SEND_FEEDBACK = "userWaitingToSendFeedBack"
    WAITING_TO_SEND_SHOW_WORD = "WAITING_TO_SEND_SHOW_WORD"
    WAITING_TO_SEND_DONT_SHOW_WORD = "WAITING_TO_SEND_DONT_SHOW_WORD"


class UserActions(BaseEnum):
    ACTION = "userAction"
    ANSWER_POLL = "userAnswerPoll"
    CANCEL_SESSION = "cancelSession"
    START_BOT = "startBot"
