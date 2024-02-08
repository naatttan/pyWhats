import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QTextEdit, QPushButton,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
from client import Clients

class ChatInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyWhats')
        self.setWindowIcon(QIcon('logopyt.jpg'))  # Assurez-vous que l'icône existe
        self.setGeometry(100, 100, 1000, 600)  # Ajustez la taille selon vos besoins

        # Main layout configuration
        mainLayout = QHBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # Sidebar configuration
        sidebarLayout = QVBoxLayout()
        sidebarLayout.setContentsMargins(0, 0, 0, 0)
        sidebarLayout.setSpacing(0)
        sidebarWidget = QWidget()
        sidebarWidget.setFixedWidth(80)
        sidebarWidget.setStyleSheet("background-color: black;")

        # Sidebar buttons
        messagesButton = QPushButton()
        settingsButton = QPushButton()
        messagesButton.setIcon(QIcon('mssg.png'))  # Update with the correct path
        settingsButton.setIcon(QIcon('param.png'))  # Update with the correct path
        messagesButton.setIconSize(QSize(40, 40))
        settingsButton.setIconSize(QSize(40, 40))
        messagesButton.setStyleSheet("background-color: black; border: none;")
        settingsButton.setStyleSheet("background-color: black; border: none;")

        # Add buttons to sidebar layout
        sidebarLayout.addWidget(messagesButton, 1)
        sidebarLayout.addStretch(1)
        sidebarLayout.addWidget(settingsButton, 1)

        sidebarWidget.setLayout(sidebarLayout)
        mainLayout.addWidget(sidebarWidget)

        # Conversation list with header
        conversationLayout = QVBoxLayout()
        header = QLabel("Conversations")
        header.setStyleSheet("font-weight: bold; font-size: 16px; color: white; background-color: #333;")
        header.setFixedHeight(40)
        header.setAlignment(Qt.AlignCenter)  # Center align the header text
        conversationLayout.addWidget(header)

        self.conversationList = QListWidget()
        self.conversationList.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #2c3e50;
                font: 14px;
                border: none;
            }
            QListWidget::item {
                border-bottom: 1px solid #ecf0f1;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        conversationLayout.addWidget(self.conversationList)
        mainLayout.addLayout(conversationLayout, 3)

        # Chat area configuration
        chatLayout = QVBoxLayout()
        chatLayout.setContentsMargins(0, 0, 0, 0)
        chatLayout.setSpacing(0)

        # Chat history area
        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setStyleSheet("background-color: #ecf0f1; border-left: 1px solid grey; padding: 5px;")
        chatLayout.addWidget(self.chatHistory)

        # Message input area
        self.messageInput = QTextEdit()
        self.messageInput.setMaximumHeight(100)
        self.messageInput.setStyleSheet("background-color: white; border: 2px solid #3498db; border-radius: 10px; padding: 5px; color: black")
        chatLayout.addWidget(self.messageInput)

        # Send button
        sendButton = QPushButton("Send")
        sendButton.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font: bold 14px;
                margin-bottom: 5px;
            }
            QPushButton:pressed {
                background-color: #9b59b6;
            }
        """)
        sendButton.clicked.connect(self.sendMessage())
        chatLayout.addWidget(sendButton)

        mainLayout.addLayout(chatLayout, 5)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        
        self.show()

    def sendMessage(self):
        self.chatHistory.append(self.messageInput.toPlainText())
        
        self.messageInput.clear()
        self.messageInput.repaint()
        self.update()
        # Logic to send message
        # pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ChatInterface()
    # mainWin.show()
    sys.exit(app.exec_())
