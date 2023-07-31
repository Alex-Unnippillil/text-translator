import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon, QClipboard
from PyQt5.QtCore import Qt
from googletrans import LANGUAGES, Translator

class LanguageLearningBuddy(QWidget):
    def __init__(self):
        super().__init__()

        self.translations_history = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Translator App")
        self.setGeometry(100, 100, 500, 400)
        self.set_modern_palette()

        layout = QVBoxLayout()

        self.word_label = QLabel("Enter the text to translate:", self)
        self.word_input = QLineEdit(self)

        self.source_lang_label = QLabel("Select the source language:", self)
        self.source_lang_combo = QComboBox(self)
        self.source_lang_combo.addItems(sorted(LANGUAGES.values()))

        self.target_lang_label = QLabel("Select the target language:", self)
        self.target_lang_combo = QComboBox(self)
        self.target_lang_combo.addItems(sorted(LANGUAGES.values()))

        default_source_lang_index = list(LANGUAGES.keys()).index("en")
        default_target_lang_index = list(LANGUAGES.keys()).index("fr")
        self.source_lang_combo.setCurrentIndex(default_source_lang_index)
        self.target_lang_combo.setCurrentIndex(default_target_lang_index)

        self.translate_button = QPushButton("Translate", self)
        self.translate_button.clicked.connect(self.translate_word)
        self.translate_button.setStyleSheet("background-color: #00bfff; color: white; font-weight: bold;")

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setStyleSheet("background-color: #98fb98; color: black; font-weight: bold;")
      
        self.save_button = QPushButton("Save Translation", self)
        self.save_button.clicked.connect(self.save_translation)
        self.save_button.setStyleSheet("background-color: #ff8c00; color: white; font-weight: bold;")

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.history_label = QLabel("Translation History:", self)
        self.history_label.setAlignment(Qt.AlignCenter)
        self.history_text_edit = QTextEdit(self)
        self.history_text_edit.setReadOnly(True)

        layout.addWidget(self.word_label)
        layout.addWidget(self.word_input)

        layout.addWidget(self.source_lang_label)
        layout.addWidget(self.source_lang_combo)

        layout.addWidget(self.target_lang_label)
        layout.addWidget(self.target_lang_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.translate_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.result_label)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_text_edit)

        self.setLayout(layout)

    def set_modern_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(245, 245, 245))  
        palette.setColor(QPalette.Base, QColor(240, 240, 240)) 
        palette.setColor(QPalette.Button, QColor(0, 191, 255)) 
        palette.setColor(QPalette.ButtonText, Qt.white) 

        self.setPalette(palette)

    def translate_word(self):
        word = self.word_input.text().strip().lower()
        source_lang_index = self.source_lang_combo.currentIndex()
        target_lang_index = self.target_lang_combo.currentIndex()

        source_lang_code = list(LANGUAGES.keys())[source_lang_index]
        target_lang_code = list(LANGUAGES.keys())[target_lang_index]

        if not word or source_lang_code == target_lang_code:
            self.result_label.setText("Invalid input. Please check the word and languages.")
            self.result_label.setStyleSheet("color: red;")
            return

        translator = Translator()
        try:
            translation = translator.translate(word, src=source_lang_code, dest=target_lang_code)
            translated_text = translation.text
            self.result_label.setText(f"Translation: {translated_text}")
            self.result_label.setStyleSheet("color: green;")

            self.save_to_history(f"{word} [{source_lang_code}] => {translated_text} [{target_lang_code}]")
            self.update_history_text()

        except Exception as e:
            self.result_label.setText(str(e))
            self.result_label.setStyleSheet("color: red;")

    def copy_to_clipboard(self):
        translation = self.result_label.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(translation.replace("Translation: ", ""))

    def save_translation(self):
        translation = self.result_label.text().replace("Translation: ", "")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Translation", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, "w") as file:
                    file.write(translation)
                QMessageBox.information(self, "Success", "Translation saved successfully.", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save translation. {str(e)}", QMessageBox.Ok)


    def clear_fields(self):
        self.word_input.clear()
        self.source_lang_combo.setCurrentIndex(0)
        self.target_lang_combo.setCurrentIndex(0)
        self.result_label.clear()

    def save_to_history(self, translation):
        self.translations_history.append(translation)

    def update_history_text(self):
        self.history_text_edit.setPlainText("\n".join(self.translations_history))

def main():
    app = QApplication(sys.argv)

    icon_path = "translator_icon.png"
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    buddy = LanguageLearningBuddy()
    buddy.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
