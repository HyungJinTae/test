import sys
from common.QtWidgets_Functions import *
from controller.SYS_Singleton import TheSys
from controller.HMI_Singleton import TheHmi
from controller.SCU import SCU


class TaskOS:
    def __init__(self):
        self.scu = SCU()
        self.evse = self.scu.evse

        self.task50_count = 0
        self.task1ms = QTimer()
        QTimer_Init(self.task1ms, 1, self.Task1ms)
        self.task50ms = QTimer()
        QTimer_Init(self.task50ms, 50, self.Task50ms)

    def Init(self):
        TheHmi.Init(self.evse, TheSys.dev, TheSys.sbms)
        self.scu.Init()

    def Task1ms(self):
        TheSys.Response_Infy()
        self.evse.RecvDataProcess()

    def Task50ms(self):
        self.scu.Task50ms()
        self.scu.SendDebugMessage()

        # task based on 50ms
        self.task50_count += 1
        task100 = int(self.task50_count % 2)
        task200 = int(self.task50_count % 4)
        task1000 = int(self.task50_count % 20)
        if task100 == 0:
            self.Task100ms()
        if task200 == 0:
            self.Task200ms()
        if task1000 == 0:
            self.Task1sec()

    def Task100ms(self):
        TheHmi.SendMonData100ms_count_InDCtestMode()
        TheHmi.SendMonData100ms_count()
        TheSys.DemandTask100ms_CEG()

    def Task200ms(self):
        self.scu.Task200ms()

    def Task1sec(self):
        self.scu.Task1000ms()
        TheHmi.CheckAlive()


if __name__ == "__main__":
    try:
        logger.info("Start..")
        logger.debug("Start..")
        app = QApplication(sys.argv)
        tos = TaskOS()
        tos.Init()
        app.exec_()
    except Exception as e:
        logger.error(f"e->{e}")