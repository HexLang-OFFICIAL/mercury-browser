import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.webview = QWebEngineView()
        self.layout.addWidget(self.url_bar)
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)
        self.load_url('https://www.google.com')

    def load_url(self, url=None):
        if not url:
            url = self.url_bar.text()
        self.webview.setUrl(QUrl(url))

class MercuryBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mercury AI Browser")
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.new_tab()

    def new_tab(self):
        tab = BrowserTab()
        self.tabs.addTab(tab, "New Tab")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MercuryBrowser()
    browser.show()
    sys.exit(app.exec_())
