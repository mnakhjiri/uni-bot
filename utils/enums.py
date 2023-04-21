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
    WAITING_TO_SEND_FOOD_DESC = "WAITING_TO_SEND_FOOD_DESC"
    WAITING_TO_SEND_FOOD_DESC_WITHOUT_USERNAME = "WAITING_TO_SEND_FOOD_DESC2"


class UserActions(BaseEnum):
    ACTION = "userAction"
    ANSWER_POLL = "userAnswerPoll"
    CANCEL_SESSION = "cancelSession"
    START_BOT = "startBot"
    SEND_POLL = "sendPoll"
    RESET_BLACKLIST = "resetBlacklist"
    SHOW_FILTERED_PANEL = "showFilteredPanel"
    SEND_FILTERED_WORDS = "SEND_FILTERED_WORDS"
    SHOW_WORD = "showWord"
    DONT_SHOW = "dontShow"
    SEND_SHEET = "sendSheet"
    SEND_FEEDBACK = "sendFeedback"
    SEND_ID = "sendId"
    SEND_EXAMS = "sendExams"
    SEND_HW = "sendHomework"
    FOOD = "food"
    SHOW_ALERTS = "SHOW_ALERTS"


class UserCustomConfigsEnum(Enum):
    DONT_SHOW_ALERTS = 0
