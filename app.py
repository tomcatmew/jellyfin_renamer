import sys
from PySide6.QtWidgets import QMessageBox,QApplication, QMainWindow
from PySide6.QtGui import QIcon
from ui_mainwindow import Ui_MainWindow
import os 
from enum import Enum

UI_PATH=os.path.join(os.path.dirname(__file__), 'resources/main.ui')
STYLE_PATH=os.path.join(os.path.dirname(__file__), 'resources/Ubuntu.qss')
ICON_PATH=os.path.join(os.path.dirname(__file__), 'resources/cat.png')

class Target(Enum):
    """Enumerators
    Args:
        Enum (_type_): parent class
    """
    MOVIE = 1
    SUBTITLE = 2

class MainWindow(QMainWindow):
    """The main window class of Pyside app, set up your signals, logic functions and store variables here

    Args:
        QMainWindow (_type_): parent class
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Jellyfin Movie Renamer")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.renameTarget = Target.MOVIE
        self.movieSuffix = ".mkv"
        self.workDirectory = ""
        self.movieList = []
        self.subtitleList = []
        self.ui.radioButton.setChecked(True)
        self.ui.radioButton.setToolTip("currently only support .mkv extension")
        self.ui.radioButton_2.setToolTip("currently only support .ass extension")
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setToolTip("Search the Movie or Subtitle files in directory")
        self.ui.pushButton.setToolTip("You need to Search the directory first")
        self.ConnectSignalsToSlot()

    def ConnectSignalsToSlot(self):
        """Initialize the signals
        """
        self.ui.pushButton.clicked.connect(self.ButtonApply)
        self.ui.pushButton_2.clicked.connect(self.ButtonSearch)
        self.ui.lineEdit.textChanged.connect(self.PathChanged)
        self.ui.radioButton.clicked.connect(self.RadioMovie)
        self.ui.radioButton_2.clicked.connect(self.RadioSub)

    def RadioMovie(self):
        self.renameTarget = Target.MOVIE
        self.ui.pushButton.setEnabled(False)

    def RadioSub(self):
        self.renameTarget = Target.SUBTITLE
        self.ui.pushButton.setEnabled(False)

    def PathChanged(self):
        self.workDirectory = self.ui.lineEdit.text()

    def ButtonApply(self):
        msg = "Rename the file names ?"
        ret = QMessageBox.information(self, "Confirm", msg, QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.Yes:
            try :
                self.Rename()
            except :
                print("Error Occured")
            else :
                msg = "Rename Completed"
                ret = QMessageBox.information(self, "Info", msg)
            self.ui.pushButton.setEnabled(False)
        elif ret == QMessageBox.No:
            pass

    def clearListWidget(self):
        self.movieList = []
        self.subtitleList = []
        self.ui.listWidget.clear()

    def ButtonSearch(self):
        """Search the directory
        """
        self.clearListWidget()

        path = self.workDirectory.replace("\\", "//")
        try :
            if self.renameTarget == Target.MOVIE :
                for file in os.listdir(path):
                    # if file.endswith(".mkv"):
                    if file.endswith(".mkv") or file.endswith(".mp4"):
                        self.movieList.append(file)
                self.movieList = sorted(self.movieList, key=lambda x: x[:])
                self.ui.listWidget.addItems(self.movieList)
                self.movieSuffix = self.movieList[0][-4:]
            else :
                for file in os.listdir(path):
                    if file.endswith(".ass"):
                    # if file.endswith(".ass") or file.endswith(".srt"):
                        self.subtitleList.append(file)
                self.subtitleList = sorted(self.subtitleList, key=lambda x: x[:])
                self.ui.listWidget.addItems(self.subtitleList)          
        except FileNotFoundError :
            msg = f"The system cannot find the path specified: {path}"
            ret = QMessageBox.information(self, "Error", msg)
        else :
            self.ui.pushButton.setEnabled(True)
        # self.listWidget.itemClicked.connect(self.clicked)

    def Rename(self):
        """rename the file iteratly
        """
        new_name = []
        season = self.ui.spinBox.value()

        if self.renameTarget == Target.MOVIE :
            for i in range(1,10):
                new_name.append(f"Episode S{season:02}E0" + str(i) + self.movieSuffix)
            for i in range(10,99):
                new_name.append(f"Episode S{season:02}E" + str(i) + self.movieSuffix)
            for i in range(len(self.movieList)) :
                os.rename(self.workDirectory + '//' + self.movieList[i], self.workDirectory + '//' + new_name[i])

        if self.renameTarget == Target.SUBTITLE :
            for i in range(1,10):
                new_name.append(f"Episode S{season:02}E0" + str(i) + ".ass")
            for i in range(10,99):
                new_name.append(f"Episode S{season:02}E" + str(i) + ".ass")
            for i in range(len(self.subtitleList)) :
                os.rename(self.workDirectory + '//' + self.subtitleList[i], self.workDirectory + '//' + new_name[i])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(STYLE_PATH, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())