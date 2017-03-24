# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    qwe.open()


class CustomSync(QDialog):
    def __init__(self, mv):
        super(CustomSync, self).__init__()
        self.__mv = mv
        self.layout = QVBoxLayout()
        self.decksComboBox = QComboBox()
        self.layout.addWidget(self.decksComboBox)
        self.syncButton = QPushButton("Sync")
        self.layout.addWidget(self.syncButton)
        self.syncButton.clicked.connect(self.syncButtonClicked)
        self.addButton = QPushButton("Add")
        self.layout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.currentModelLable = QLabel()
        self.layout.addWidget(self.currentModelLable)
        self.setLayout(self.layout)

    def open(self):
        self.decksComboBox.clear()
        self.decksComboBox.addItems(self.__mv.col.decks.allNames())
        QDialog.open(self)

    def syncButtonClicked(self):
        self.dataSource = {
            'keys': ['word', 'translate', 'score', 'img'],
            'keysMaps': {},
            'notes': [
                {'word': "lol", 'translate': 'ohlol', 'score': 123, 'img': 'lol.png'},
                {'word': "lol1", 'translate': 'ohlol2', 'score': 123, 'img': 'lol.png'},
                {'word': "lol2", 'translate': 'ohlol3', 'score': 123, 'img': 'lol.png'},
            ]
        }
        map = mw.col.models.fieldMap(mw.col.models.current())
        self.renderMapping(map)

    def addButtonClicked(self):
        for destNote in self.dataSource['notes']:
            newNote = self.createNote(destNote)
            self.saveNote(newNote)

    def createNote(self, destNote):
        note = mw.col.newNote()

        for index in range(len(note.fields)):
            if index in self.dataSource['keysMaps']:
                newFieldKey = self.dataSource['keysMaps'][index]
            else:
                continue
            if newFieldKey in destNote:
                note.fields[index] = destNote[newFieldKey]
        return note

    def saveNote(self, note):
        # self.layout.update()
        ret = note.dupeOrEmpty()
        if ret == 1:
            print "error"
            return
        elif ret == 2:
            print "duble"
            return
        cards = mw.col.addNote(note)
        if not cards:
            print "error"
            return
        mw.requireReset()


    def renderMapping(self, map):
        self.mapLayout = QVBoxLayout()
        for item in map:
            layout = QHBoxLayout()
            lable = QLabel(map[item][1]['name'])
            layout.addWidget(lable)
            combobox = QComboBox()
            combobox.id = map[item][0]
            combobox.addItem("")
            combobox.addItems(self.dataSource['keys'])
            combobox.currentIndexChanged.connect(self.onChange)
            layout.addWidget(combobox)
            self.mapLayout.addLayout(layout)
        self.layout.addLayout(self.mapLayout)


    def onChange(self, event):
        subject = self.sender()
        self.dataSource["keysMaps"][subject.id] = subject.currentText()
        print self.dataSource

# create a new menu item, "test"
action = QAction("test", mw)

# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)

# and add it to the tools menu
mw.form.menuTools.addAction(action)

button = QPushButton('Custom Sync')

button.clicked.connect(testFunction)

mw.mainLayout.addWidget(button)
qwe = CustomSync(mw)

