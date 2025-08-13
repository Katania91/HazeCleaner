import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QProgressBar, QCheckBox, QComboBox, QFrame, QWidget, QDialog, QSizePolicy
)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import threading
from cleaner import clean_fivem

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

LOCALE_PATH = resource_path("localization")
ASSETS_PATH = resource_path("assets")

def load_locale(lang):
    with open(os.path.join(LOCALE_PATH, f"{lang}.json"), encoding="utf-8") as f:
        return json.load(f)

class SAboutWindow(QDialog):
    def __init__(self, locale, icon_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(locale["about_title"])
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(400, 320)
        self.setStyleSheet("""
            QDialog {
                background: rgba(35, 39, 46, 0.98);
                border-radius: 18px;
            }
            QLabel, QPushButton {
                color: #fff;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                background: transparent;
            }
            QLabel#aboutLogo {
                margin-bottom: 12px;
            }
            QLabel#aboutFooter {
                color: #888;
                font-size: 11px;
                background: transparent;
            }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo = QLabel()
        logo.setObjectName("aboutLogo")
        pixmap = QPixmap(icon_path).scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignHCenter)

        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        author = QLabel('Autore: <a href="https://github.com/Katania91" style="color:#00c6fb;text-decoration:none;">Katania91</a>')
        author.setTextFormat(Qt.TextFormat.RichText)
        author.setOpenExternalLinks(True)
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(author)

        discord = QLabel('Discord: @Katania91')
        discord.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(discord)

        version = QLabel('Versione: v1.0')
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(version)

        layout.addLayout(info_layout)

        # Spazio
        layout.addSpacing(10)

        links_layout = QHBoxLayout()
        links_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        website = QLabel(f'<a href="https://hazeroleplay.com">{locale["website"]}</a>')
        website.setOpenExternalLinks(True)
        website.setStyleSheet("color: #00c6fb; font-weight: bold; background: transparent;")
        discord_link = QLabel(f'<a href="https://discord.hazeroleplay.com">{locale["discord"]}</a>')
        discord_link.setOpenExternalLinks(True)
        discord_link.setStyleSheet("color: #7289da; font-weight: bold; background: transparent;")
        links_layout.addWidget(website)
        links_layout.addSpacing(16)
        links_layout.addWidget(discord_link)
        layout.addLayout(links_layout)

        layout.addStretch()

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        copyright_label = QLabel("© 2025 ! KΛTΛПIΛ")
        copyright_label.setObjectName("aboutFooter")
        footer_layout.addWidget(copyright_label)
        layout.addLayout(footer_layout)

        self.setLayout(layout)

class HazeCleanerGUI(QWidget):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    enable_start_btn_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.lang = "it"
        self.locale = load_locale(self.lang)
        self.icon_path = os.path.join(ASSETS_PATH, "icona.png")
        self.setWindowTitle(self.locale["title"])
        self.setWindowIcon(QIcon(self.icon_path))
        self.resize(700, 520)
        self.setMinimumWidth(540)
        self.setWindowOpacity(0.97)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #23272ecc, stop:1 #181a20cc);
                color: #fff;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                font-size: 15px;
            }
            QFrame#Header, QFrame#Footer {
                background: rgba(40, 44, 52, 0.92);
                border-radius: 16px;
            }
            QPushButton, QComboBox {
                background: #23272e;
                border: none;
                border-radius: 10px;
                padding: 10px 22px;
                color: #fff;
                font-size: 15px;
            }
            QPushButton:hover, QComboBox:hover {
                background: #005bea;
                color: #fff;
            }
            QPushButton#mainBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00c6fb, stop:1 #005bea);
                color: #fff;
                font-weight: bold;
                font-size: 17px;
                border-radius: 14px;
                padding: 14px 0;
            }
            QPushButton#mainBtn:hover {
                background: #005bea;
            }
            QTextEdit {
                background: #181a20;
                border-radius: 10px;
                color: #fff;
                font-family: 'Fira Mono', 'Consolas', monospace;
                font-size: 14px;
                padding: 8px;
            }
            QProgressBar {
                background: #23272e;
                border-radius: 10px;
                text-align: center;
                color: #fff;
                height: 26px;
                font-size: 15px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00c6fb, stop:1 #005bea);
                border-radius: 10px;
            }
            QCheckBox {
                padding: 6px;
                font-size: 15px;
            }
            QLabel {
                color: #fff;
                background: transparent;
            }
            QLabel#footerLink {
                color: #00c6fb;
                font-weight: bold;
                background: transparent;
            }
            QLabel#footerLink:hover {
                color: #fff;
                text-decoration: underline;
                background: transparent;
            }
        """)
        self.log_signal.connect(self._append_log)
        self.progress_signal.connect(self._set_progress)
        self.enable_start_btn_signal.connect(self.start_btn_set_enabled)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(22, 22, 22, 22)

        header = QFrame()
        header.setObjectName("Header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 10, 16, 10)

        logo = QLabel()
        pixmap = QPixmap(self.icon_path).scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        header_layout.addWidget(logo)

        self.title_label = QLabel(self.locale["title"])
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-left: 10px; background: transparent;")
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        lang_combo = QComboBox()
        lang_combo.addItem(QIcon(os.path.join(ASSETS_PATH, "it.png")), "Italiano", "it")
        lang_combo.addItem(QIcon(os.path.join(ASSETS_PATH, "en.png")), "English", "en")
        lang_combo.setCurrentIndex(0 if self.lang == "it" else 1)
        lang_combo.setMinimumWidth(110)
        lang_combo.setMaximumWidth(140)
        lang_combo.setStyleSheet("""
            QComboBox {
                background: #23272e;
                color: #fff;
                border-radius: 8px;
                padding: 2px 8px;
                font-size: 14px;
                min-width: 80px;
            }
            QComboBox QAbstractItemView {
                background: #23272e;
                color: #fff;
                selection-background-color: #005bea;
                border-radius: 8px;
            }
        """)
        lang_combo.currentIndexChanged.connect(self.change_language)
        header_layout.addWidget(lang_combo)

        help_btn = QPushButton("?")
        help_btn.setFixedSize(32, 32)
        help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        help_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        help_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #fff;
                font-weight: bold;
                font-size: 18px;
                border: 2px solid #fff;
                border-radius: 16px;
                margin-left: 8px;
                padding: 0px;
            }
            QPushButton:hover {
                background: rgba(0, 198, 251, 0.18);
                color: #00c6fb;
                border: 2px solid #00c6fb;
            }
        """)
        help_btn.clicked.connect(self.show_about)
        header_layout.addWidget(help_btn)

        header.setLayout(header_layout)
        main_layout.addWidget(header)

        main_layout.addSpacing(8)
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(140)
        main_layout.addWidget(self.log_box)

    self.progress = QProgressBar()
    self.progress.setValue(0)
    main_layout.addWidget(self.progress)

    self.keybind_checkbox = QCheckBox(self.locale["delete_keybind"])
    main_layout.addWidget(self.keybind_checkbox)

    self.start_btn = QPushButton(self.locale["start_clean"])
    self.start_btn.setObjectName("mainBtn")
    self.start_btn.clicked.connect(self.start_cleaning)
    main_layout.addWidget(self.start_btn)

    main_layout.addStretch()

    footer = QFrame()
    footer.setObjectName("Footer")
    footer_layout = QHBoxLayout()
    footer_layout.setContentsMargins(16, 10, 16, 10)
    icon_label = QLabel()
    pixmap_footer = QPixmap(self.icon_path).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    icon_label.setPixmap(pixmap_footer)
    footer_layout.addWidget(icon_label)
    footer_text = QLabel("Sviluppato da ! KΛTΛПIΛ per Haze RP")
    footer_layout.addWidget(footer_text)
    footer_layout.addStretch()
    website = QLabel(f'<a href="https://hazeroleplay.com">{self.locale["website"]}</a>')
    website.setObjectName("footerLink")
    website.setOpenExternalLinks(True)
    footer_layout.addWidget(website)
    discord = QLabel(f'<a href="https://discord.hazeroleplay.com">{self.locale["discord"]}</a>')
    discord.setObjectName("footerLink")
    discord.setOpenExternalLinks(True)
    footer_layout.addWidget(discord)
    footer.setLayout(footer_layout)
    main_layout.addWidget(footer)

    def _append_log(self, msg):
        self.log_box.append(msg)

    def _set_progress(self, val):
        self.progress.setValue(val)

    def start_btn_set_enabled(self, enabled):
        self.start_btn.setEnabled(enabled)

    def change_language(self, idx):
        lang = self.sender().itemData(idx)
        self.lang = lang
        self.locale = load_locale(lang)
        self.refresh_ui()

    def refresh_ui(self):
        self.setWindowTitle(self.locale["title"])
        self.title_label.setText(self.locale["title"])
        self.keybind_checkbox.setText(self.locale["delete_keybind"])
        self.start_btn.setText(self.locale["start_clean"])

    def show_about(self):
        about = SAboutWindow(self.locale, self.icon_path, self)
        about.exec()

    def start_cleaning(self):
        self.enable_start_btn_signal.emit(False)
        self.progress_signal.emit(0)
        self.log_signal.emit(self.locale["log_start"])
        self.log_box.clear()
        delete_keybind = self.keybind_checkbox.isChecked()

        def log_callback(msg):
            self.log_signal.emit(msg)

        def progress_callback(val):
            self.progress_signal.emit(val)

        def cleaning_task():
            clean_fivem(
                log_callback=log_callback,
                progress_callback=progress_callback,
                delete_keybind=delete_keybind,
                locale=self.locale
            )
            self.log_signal.emit(self.locale["log_done"])
            self.progress_signal.emit(100)
            self.enable_start_btn_signal.emit(True)

    threading.Thread(target=cleaning_task, daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HazeCleanerGUI()
    window.show()
    sys.exit(app.exec())