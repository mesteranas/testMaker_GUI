# this file for maniging questions like deleting and adding
from abc import abstractmethod,ABC, ABCMeta
import guiTools
from . import jsonControl
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class CombinedMeta(type(qt.QDialog), ABCMeta):
    pass
class QuestionManiger(qt.QDialog,ABC,metaclass=CombinedMeta):
    def __init__(self,p):
        super().__init__(p)
        """
        a ABC class for maniging questions and categories
        """
        self.showFullScreen()
        self.setWindowTitle(_("question manager"))
        self.data=jsonControl.get()
        self.layout=qt.QVBoxLayout(self)
        self.listBox=qt.QListWidget()
        self.listBox.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.listBox.customContextMenuRequested.connect(self.onContextMenu)
        self.layout.addWidget(self.listBox)
        self.add=qt.QPushButton(_("Add"))
        self.add.clicked.connect(self.onAdd)
        self.layout.addWidget(self.add)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
    @abstractmethod
    def onAdd(self):
        """
        a ABC method makes you to add question or category
        """
    def onContextMenu(self):
        menu=qt.QMenu(self)
        menu.setAccessibleName(_("actions"))
        menu.setFocus()
        deleteAction=qt1.QAction(_("delete"),self)
        deleteAction.triggered.connect(self.onDelete)
        menu.addAction(deleteAction)
        menu.setDefaultAction(deleteAction)
        menu.exec()
    @abstractmethod
    def onDelete(self):
        """
        a method to delete question or category
        """
class CategoryManiger(QuestionManiger):
    def __init__(self, p):
        super().__init__(p)
        self.listBox.addItems(self.data.keys())
        self.open=qt.QPushButton(_("open questions"))
        self.open.clicked.connect(lambda:manageQuestions(self,self.listBox.currentItem().text()))
        self.layout.addWidget(self.open)
        self.exec()
    def onAdd(self):
        name,ok=qt.QInputDialog.getText(self,_("new category"),_("category name"))
        if ok and name:
            self.data[name]={}
            self.listBox.addItem(name)
            jsonControl.save(self.data)
    def onDelete(self):
        try:
            del(self.data[self.listBox.currentItem().text()])
            self.listBox.takeItem(self.listBox.currentRow())
            jsonControl.save(self.data)
            guiTools.speak(_("deleted"))
        except:
            guiTools.speak(_("error"))
class manageQuestions(QuestionManiger):
    def __init__(self,p,category:str):
        super().__init__(p)
        self.category=category
        self.listBox.addItems(self.data[category])
        self.exec()
    def onAdd(self):
        dlg=AddQuestion(self,self.category,self.data)
        if dlg.exec()==dlg.DialogCode.Accepted:
            self.data=dlg.data
            self.listBox.clear()
            self.listBox.addItems(self.data[self.category])
    def onDelete(self):
        try:
            del(self.data[self.category][self.listBox.currentItem().text()])
            self.listBox.takeItem(self.listBox.currentRow())
            jsonControl.save(self.data)
            guiTools.speak(_("deleted"))
        except:
            guiTools.speak(_("error"))
class AddQuestion(qt.QDialog):
    def __init__(self,p,category:str,data:dict):
        super().__init__(p)
        self.category=category
        self.data=data
        layout=qt.QVBoxLayout(self)
        self.question=qt.QLineEdit()
        layout.addWidget(qt.QLabel(_("question")))
        layout.addWidget(self.question)
        self.type=qt.QComboBox()
        self.type.addItems([_("choose"),_("complete")])
        self.type.currentIndexChanged.connect(self.onQuestionTypeChanged)
        layout.addWidget(qt.QLabel(_("question type")))
        layout.addWidget(self.type)
        self.answer=qt.QLineEdit()
        layout.addWidget(qt.QLabel(_("answer")))
        layout.addWidget(self.answer)
        self.falseAnsers=qt.QLineEdit()
        layout.addWidget(qt.QLabel(_("other answers")))
        layout.addWidget(self.falseAnsers)
        self.add=qt.QPushButton(_("add"))
        self.add.clicked.connect(self.onAdd)
        layout.addWidget(self.add)
    def onQuestionTypeChanged(self,index):
        if index==0:
            self.falseAnsers.setDisabled(False)
        else:
            self.falseAnsers.setDisabled(True)
    def onAdd(self):
        self.data[self.category][self.question.text()]={"answer":self.answer.text(),"type":self.type.currentIndex(),"otherAnswers":self.falseAnsers.text()}
        jsonControl.save(self.data)
        self.accept()