# this file for making tests
import random
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class MakeTests(qt.QDialog):
    def __init__(self,p,data:dict,count:int):
        super().__init__(p)
        self.showFullScreen()
        self.setWindowTitle(_("make tests"))
        layout=qt.QVBoxLayout(self)
        self.true=0
        self.false=0
        self.count=count
        self.done=0
        self.trueAnswer=""
        self.type=0
        self.data=data
        self.question=guiTools.QReadOnlyTextEdit()
        layout.addWidget(qt.QLabel(_("question")))
        layout.addWidget(self.question)
        self.choose=qt.QComboBox()
        layout.addWidget(self.choose)
        self.complete=qt.QLineEdit()
        layout.addWidget(self.complete)
        self.submit=qt.QPushButton(_("submit"))
        self.submit.clicked.connect(self.onSubmit)
        layout.addWidget(self.submit)
        self.onNext()
    def onSubmit(self):
        if self.type==0:
            check=self.trueAnswer==self.choose.currentText()
        else:
            check=self.trueAnswer==self.complete.text()
        if check:
            guiTools.playSoundEffect("data/sounds/1.wav")
            self.true+=1
        else:
            guiTools.playSoundEffect("data/sounds/2.wav")
            self.false+=1
            qt.QMessageBox.warning(self,_("error"),_("your answer is false the true one is ") + self.trueAnswer)
        self.done+=1
        if self.done==self.count:
            qt.QMessageBox.information(self,("congratulation"),_("you finished the test and you got ") + str(self.true) + _("from") + str(self.count))
            self.close()
        else:
            self.onNext()
    def onNext(self):
        self.choose.setDisabled(True)
        self.complete.setDisabled(True)
        result=random.choice(list(self.data.keys()))
        question=self.data[result]
        self.question.setText(result)
        self.trueAnswer=question["answer"]
        self.type=question["type"]
        if self.type==0:
            self.choose.setDisabled(False)
            self.choose.clear()
            otherAnswers=question["otherAnswers"].split(",")
            otherAnswers.append(self.trueAnswer)
            self.choose.addItems(random.sample(otherAnswers,len(otherAnswers)))
        else:
            self.complete.setDisabled(False)
        self.question.setFocus()