import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QTabWidget,
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QListWidget, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class BrowserTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)
        self.browser.urlChanged.connect(self.update_url)

    def update_url(self, q):
        self.parent.update_url(q.toString())

class MercuryBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mercury Browser: Tabbed, Bookmarked & Brainy")
        self.setGeometry(100, 100, 1400, 900)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.back_btn = QAction("←", self)
        self.back_btn.triggered.connect(lambda: self.current_browser().back())
        self.navbar.addAction(self.back_btn)

        self.forward_btn = QAction("→", self)
        self.forward_btn.triggered.connect(lambda: self.current_browser().forward())
        self.navbar.addAction(self.forward_btn)

        self.reload_btn = QAction("⟳", self)
        self.reload_btn.triggered.connect(lambda: self.current_browser().reload())
        self.navbar.addAction(self.reload_btn)

        self.navbar.addWidget(self.url_bar)

        self.new_tab_btn = QAction("+", self)
        self.new_tab_btn.triggered.connect(self.add_new_tab)
        self.navbar.addAction(self.new_tab_btn)

        self.bookmarks = QListWidget()
        self.bookmarks.setMaximumWidth(200)
        self.bookmarks.itemClicked.connect(self.load_bookmark)

        self.ai_prompt = QLineEdit()
        self.ai_prompt.setPlaceholderText("Ask AI (e.g., 'go to YouTube')")
        self.ai_prompt.returnPressed.connect(self.ai_navigate)

        ai_btn = QPushButton("🧠")
        ai_btn.clicked.connect(self.ai_navigate)

        ai_bar = QHBoxLayout()
        ai_bar.addWidget(self.ai_prompt)
        ai_bar.addWidget(ai_btn)

        side_panel = QVBoxLayout()
        side_panel.addWidget(QLabel("📑 Bookmarks"))
        side_panel.addWidget(self.bookmarks)
        side_panel.addLayout(ai_bar)

        container = QWidget()
        layout = QHBoxLayout()
        layout.addLayout(side_panel)
        layout.addWidget(self.tabs)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_new_tab()

    def current_browser(self):
        current_tab = self.tabs.currentWidget()
        return current_tab.browser

    def add_new_tab(self):
        tab = BrowserTab(self)
        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)
        tab.browser.loadFinished.connect(lambda _: self.tabs.setTabText(i, tab.browser.page().title()))

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def update_url(self, url):
        self.url_bar.setText(url)
        if url not in [self.bookmarks.item(i).text() for i in range(self.bookmarks.count())]:
            self.bookmarks.addItem(url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def load_bookmark(self, item):
        self.current_browser().setUrl(QUrl(item.text()))

def ai_navigate(self):
    prompt = self.ai_prompt.text().strip()
    if not prompt:
        return

    try:
        response = requests.post(
            "https://text.pollinations.ai/prompt/",
            json={"prompt": prompt}
        )
        if response.status_code == 200:
            result = response.json().get("text", "Sorry, I got nothing.")
        else:
            result = f"Error: {response.status_code}"

    except Exception as e:
        result = f"Exception: {str(e)}"

    QMessageBox.information(self, "AI Response", result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MercuryBrowser()
    window.show()
    sys.exit(app.exec_())
