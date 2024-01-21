import tkinter, inspect
from tkinter import font, ttk
from Logger import Logger


class Ic:

    @staticmethod
    def __isValidIc(prefix:str, icNum:str) -> bool:

        if (len(prefix) > 2) or (len(prefix) == 0):
            logger.infoLog('Invalid IC prefix length')
            return False

        for p in prefix:
            if p.isnumeric():
                logger.infoLog('Invalid IC prefix')
                return False

        for n in icNum:
            if n.isalpha():
                logger.infoLog('Invalid IC Number')
                return False

        logger.infoLog('Valid IC')
        return True

    @staticmethod
    def __getIcPrefix(icNo:str) -> str:

        prefix = ''
        if icNo[0].isalpha(): prefix = prefix + icNo[0]
        if icNo[1].isalpha(): prefix = prefix + icNo[1]

        return prefix

    @staticmethod
    def __getIcNumber(icNo:str) -> str: return icNo[-6:]

    def getHkIcChkDigit(self, icNo:str):

        refStr = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if len(icNo) < 7 or len(icNo) > 8:
            logger.infoLog('Invalid IC length')
            return None

        prefix, icNum = self.__getIcPrefix(icNo), self.__getIcNumber(icNo)
        logger.infoLog(f'IcNo: {icNo}, prefix: {prefix}, icNum: {icNum}')

        if not self.__isValidIc(prefix,icNum): return None

        weight = len(prefix + icNum) + 1
        sum = 0

        for p in prefix:
            sum += ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(p.upper()) + 1) * weight
            weight -= 1

        for n in icNum:
            sum += int(n) * weight
            weight -= 1

        out = refStr[11 - (sum % 11)]
        logger.infoLog(f'chkDigit: {out}')

        return out


class Visa:

    @staticmethod
    def __isValidVisa(visaNo4:str, visaNo7:str, visaNo2:str):

        if not visaNo4.isalpha():
            logger.infoLog('Invalid Visa prefix')
            return False

        if not visaNo7.isnumeric():
            logger.infoLog('Invalid Visa Number')
            return False

        if not visaNo2.isnumeric():
            logger.infoLog('Invalid Visa Year')
            return False

        logger.infoLog('Valid Visa')
        return True

    @staticmethod
    def __getVisaPrefix(visaNo:str) -> str:
        return visaNo[:4]

    @staticmethod
    def __getVisaNumber(visaNo:str) -> str:
        return visaNo[4:-2]

    @staticmethod
    def __getVisaYear(visaNo:str) -> str:
        return visaNo[-2:]

    def getVisaChkDigit(self, visaNo:str):

        refStr = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        weight, sum = 14, 0

        if ' ' in visaNo: visaNo = visaNo.replace(' ', '')
        if '-' in visaNo: visaNo = visaNo.replace('-', '')

        if len(visaNo) != 13:
            logger.infoLog('Invalid Visa Length')
            return None

        prefix, number, year = self.__getVisaPrefix(visaNo), self.__getVisaNumber(visaNo), self.__getVisaYear(visaNo)
        logger.infoLog(f'visaNo: {visaNo}, prefix: {prefix}, number:{number}, year:{year}')

        if not self.__isValidVisa(prefix, number, year): return None

        visa = prefix.upper() + number + year
        logger.infoLog(f'visaNo: {visaNo}')

        for i in visa:
            sum += refStr.index(i) * weight
            weight -= 1

        out = refStr[17 - (sum % 17)]

        logger.infoLog(f'chkDigit: {out}')

        return out


class GUI:

    def closeWindows(self):
        self.app.destroy()

    def startNewWindows(self, title: str, width: int, height: int, isFixedSize: bool) -> tkinter.Tk:

        root = tkinter.Tk()
        root.title(title)
        root.wm_minsize(width, height)
        if isFixedSize: root.wm_maxsize(width, height)
        root.protocol('WM_DELETE_WINDOW', self.closeWindows)

        return root

    def __calBind(self,event):
        logger.infoLog(f'Return pressed')
        self.__calculate()

    def __calculate(self):

        logger.infoLog(f'start chk digit calculation')

        out = None
        logger.infoLog(f"TD Num: {self.td[1].get()}, TD Type: {self.__tdType.get()}")

        if 'ID' in self.__tdType.get():
            out = self.ic.getHkIcChkDigit(self.td[1].get())

        if 'Visa' in self.__tdType.get():
            out = self.visa.getVisaChkDigit(self.td[1].get())

        if out is None:
            msg = 'Invalid TD Num or TD Type'
            self.message[0]['text'] = msg
            logger.infoLog(msg)
        else:
            self.message[0]['text'] = f'Check Digit: {out}'

    def __clsBind(self, event):
        logger.infoLog(f'Ctrl+F12 pressed')
        self.__cls()

    def __cls(self):

        logger.infoLog(f'called clear function')

        self.td[1].delete(0, len(self.td[1].get()))
        self.__tdType.set(" ")
        self.message[0]['text'] = ""

    def main(self):

        self.app = self.startNewWindows('Check Digit Calculator', 300, 200, True)

        self.__tdType = tkinter.StringVar()
        supportedTd = ('Hong Kong ID Card', 'Visa')

        inputArea = tkinter.Frame(self.app, height=99)
        tdSubArea = tkinter.Frame(inputArea, height=49)
        typeSubArea = tkinter.Frame(inputArea, height=49)
        controlArea = tkinter.Frame(self.app, height=99)
        messageArea = tkinter.Frame(self.app, height=99)

        self.td = [tkinter.Label(tdSubArea, text="Td Num :"), tkinter.Entry(tdSubArea)]
        self.tdType = [
            tkinter.Label(typeSubArea, text="TD Type :"),
            tkinter.ttk.Combobox(typeSubArea, textvariable=self.__tdType, state="readonly")
        ]
        control = [
            tkinter.Button(controlArea, text="Calculate", command=self.__calculate),
            tkinter.Button(controlArea, text="Clear", command=self.__cls)
        ]
        self.message = [tkinter.Label(messageArea, width=350, height=2)]

        area = [inputArea, tdSubArea, typeSubArea, controlArea, messageArea]
        component = [self.td, self.tdType, control, self.message]

        self.app.bind('<Return>', self.__calBind)
        self.app.bind('<Control-F12>', self.__clsBind)

        for widget in area:
            widget.config(width=290, relief="ridge", bd=2)
            if widget in [inputArea, controlArea, messageArea]:
                widget.pack(side="top", pady=10)
                pass
            widget.pack(side="top")

        for element in component:
            for widget in element:

                if component.index(element) == 3:
                    widget.config(width=30, font=font.Font(size=10))
                    pass

                # for control
                if component.index(element) == 2:
                    widget.config(width=15)
                    pass

                if component.index(element) == 1:

                    if element.index(widget) == 0:
                        widget.config(width=10)

                    if element.index(widget) == 1:
                        widget['values'] = supportedTd
                        widget.config(width=20)
                    pass

                if component.index(element) == 0:

                    if element.index(widget) == 0:
                        widget.config(width=10)

                    if element.index(widget) == 1:
                        if element.index(widget) == 1: widget.config(width=20, font=font.Font(size=10))
                    pass

                widget.pack(side="left")

        self.app.mainloop()

    def __init__(self):

        logger.infoLog('Start GUI')

        self.ic, self.visa = Ic(), Visa()
        self.main()

        logger.infoLog('End GUI')


if "__main__" == __name__:

    logger = Logger()
    logger.__int__()
    GUI()
