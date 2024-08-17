from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QFormLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
from threading import Thread
import sys
import blumscript

class WorkerSignals(QObject):
    update_status = pyqtSignal(str)

class TokenInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите токен")
        self.setFixedSize(300, 150)
        
        # Layout
        layout = QVBoxLayout()
        
        # Title label
        self.titleLabel = QLabel("Введите Bearer токен:")
        self.titleLabel.setStyleSheet("color: #333333; font-family: 'Arial'; font-size: 16px;")
        layout.addWidget(self.titleLabel)

        # Token input field
        self.tokenInput = QLineEdit()
        self.tokenInput.setPlaceholderText("Введите токен...")
        self.tokenInput.setStyleSheet("background-color: rgb(240, 240, 240);"
                                      "color: #333333;"
                                      "border: 1px solid #cccccc;"
                                      "border-radius: 5px;"
                                      "padding: 10px;")
        layout.addWidget(self.tokenInput)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.okButton = QPushButton("ОК")
        self.cancelButton = QPushButton("Отмена")
        self.buttonBox.addButton(self.okButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton, QtWidgets.QDialogButtonBox.RejectRole)
        
        # Style buttons
        self.okButton.setStyleSheet("background-color: rgb(129, 129, 129);"
                                    "color: white;"
                                    "font-family: 'Arial';"
                                    "font-size: 14px;"
                                    "font-weight: bold;"
                                    "border-radius: 5px; padding: 5px; border: none;"
                                    "margin-right: 10px;")
        self.cancelButton.setStyleSheet("background-color: rgb(129, 129, 129);"
                                        "color: white;"
                                        "font-family: 'Arial';"
                                        "font-size: 14px;"
                                        "font-weight: bold;"
                                        "border-radius: 5px; padding: 5px; border: none;")
        self.buttonBox.setStyleSheet("QDialogButtonBox {"
                                     "border: none;"
                                     "}")
        
        # Connect signals
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        
        layout.addWidget(self.buttonBox)
        
        # Set layout
        self.setLayout(layout)

    def getToken(self):
        return self.tokenInput.text()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 400)
        MainWindow.setMinimumSize(QtCore.QSize(400, 400))
        MainWindow.setMaximumSize(QtCore.QSize(400, 400))

        # Set simple gray background
        MainWindow.setStyleSheet("background-color: rgb(240, 240, 240);")

        # Set window icon
        MainWindow.setWindowIcon(QtGui.QIcon("images/icon.ico"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title Label
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(60, 20, 280, 50))
        self.titleLabel.setStyleSheet("QLabel {"
                                      "color: black;"
                                      "font-family: 'Arial';"
                                      "font-size: 22px;"
                                      "font-weight: bold;"
                                      "}")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")

        # Subtitle Label
        self.subtitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.subtitleLabel.setGeometry(QtCore.QRect(150, 70, 100, 20))
        self.subtitleLabel.setStyleSheet("QLabel {"
                                         "color: black;"
                                         "font-family: 'Arial';"
                                         "font-size: 12px;"
                                         "}")
        self.subtitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitleLabel.setObjectName("subtitleLabel")

        # Status Text Area
        self.statusText = QtWidgets.QTextEdit(self.centralwidget)
        self.statusText.setGeometry(QtCore.QRect(50, 120, 300, 200))
        self.statusText.setStyleSheet("QTextEdit {"
                                      "background-color: rgb(255, 255, 255);"
                                      "color: black;"
                                      "font-family: 'Arial';"
                                      "font-size: 14px;"
                                      "border-radius: 10px;"
                                      "padding: 10px;"
                                      "}")
        self.statusText.setReadOnly(True)
        self.statusText.setObjectName("statusText")

        # Start Button
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(140, 340, 120, 41))
        self.StartButton.setStyleSheet("QPushButton {"
                                       "background-color: rgb(129, 129, 129);"
                                       "color: white;"
                                       "font-family: 'Arial';"
                                       "font-size: 16px;"
                                       "font-weight: bold;"
                                       "border-radius: 10px; padding: 10px; border: none;"
                                       "} QPushButton:hover {"
                                       "background-color: rgb(100, 100, 100);"
                                       "} QPushButton:pressed {"
                                       "background-color: rgb(80, 80, 80);"
                                       "}")
        self.StartButton.setObjectName("StartButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Button connection
        self.StartButton.clicked.connect(self.toggle_start)

        # Internal state
        self.is_running = False
        self.thread = None

        # Worker signals
        self.worker_signals = WorkerSignals()
        self.worker_signals.update_status.connect(self.update_status)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BlumAuto by FLUX"))
        self.titleLabel.setText(_translate("MainWindow", "Авто кликер BLUM"))
        self.subtitleLabel.setText(_translate("MainWindow", "by FLUX"))
        self.StartButton.setText(_translate("MainWindow", "Старт"))

    def toggle_start(self):
        if not self.is_running:
            # Show custom token input dialog
            dialog = TokenInputDialog(self.centralwidget)
            if dialog.exec_() == QDialog.Accepted:
                token = dialog.getToken()
                if token:
                    self.is_running = True
                    self.StartButton.setText("Стоп")
                    # Start the script in a separate thread
                    self.thread = Thread(target=self.run_script, args=(token,))
                    self.thread.start()
        else:
            self.is_running = False
            self.StartButton.setText("Старт")
            self.statusText.append("Остановлено.")

    def run_script(self, token):
        try:
            blumscript.main(token, self.worker_signals.update_status.emit)
        except Exception as e:
            self.worker_signals.update_status.emit(f"Ошибка: {str(e)}")
        finally:
            self.is_running = False
            self.worker_signals.update_status.emit("Завершено")
            self.StartButton.setText("Старт")

    def update_status(self, message):
        self.statusText.append(message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
