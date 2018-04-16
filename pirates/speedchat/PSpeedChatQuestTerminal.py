from otp.speedchat.SCTerminal import *
from pirates.quest import QuestDB

PSpeedChatQuestMsgEvent = 'PSCQuestMsg'

def decodeSCQuestMsg(questId, msgType, taskNum):
    questdb = QuestDB.QuestDict[questId]
    if questdb is None:
        return
    if msgType == 0:
        return questdb.getSCSummaryText(taskNum)
    else:
        if msgType == 1:
            return questdb.getSCWhereIsText(taskNum)
        else:
            if msgType == 2:
                return questdb.getSCHowToText(taskNum)
            else:
                return
    return


def decodeSCQuestMsgInt(questInt, msgType, taskNum):
    qId = QuestDB.getQuestIdFromQuestInt(questInt)
    questDna = QuestDB.QuestDict[qId]
    if questDna is None:
        return
    if msgType == 0:
        return questDna.getSCSummaryText(taskNum)
    else:
        if msgType == 1:
            return questDna.getSCWhereIsText(taskNum)
        else:
            if msgType == 2:
                return questDna.getSCHowToText(taskNum)
            else:
                return
    return


class PSpeedChatQuestTerminal(SCTerminal):
    
    def __init__(self, msg, questInt, toNpcId, msgType, taskNum):
        SCTerminal.__init__(self)
        self.msg = msg
        self.questInt = questInt
        self.toNpcId = toNpcId
        self.msgType = msgType
        self.taskNum = taskNum

    def getDisplayText(self):
        return self.msg

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(PSpeedChatQuestMsgEvent), [
         self.questInt, self.toNpcId, self.msgType, self.taskNum])
