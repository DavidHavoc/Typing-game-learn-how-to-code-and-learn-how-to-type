import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QComboBox, QPushButton, 
                              QTextEdit, QFrame, QSplitter, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QSize
from PySide6.QtGui import QFont, QColor, QPalette, QTextCharFormat, QTextCursor

from code_generator import CodeGenerator

class CodeDisplayWidget(QTextEdit):
    """Widget for displaying code that needs to be typed."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 12))
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set a light background color for the code display
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("#f5f5f5"))
        self.setPalette(palette)
        
    def set_code(self, code):
        """Set the code to be displayed."""
        self.setPlainText(code)
        
    def highlight_current_position(self, position, correct=True):
        """Highlight the current position in the code."""
        cursor = self.textCursor()
        cursor.setPosition(position)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        
        # Create format for highlighting
        fmt = QTextCharFormat()
        if correct:
            fmt.setBackground(QColor("#c8e6c9"))  # Light green for correct
        else:
            fmt.setBackground(QColor("#ffcdd2"))  # Light red for incorrect
            
        # Apply highlighting
        cursor.mergeCharFormat(fmt)
        
    def clear_highlighting(self):
        """Clear all highlighting in the code display."""
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        
        # Reset format
        fmt = QTextCharFormat()
        cursor.mergeCharFormat(fmt)
        
    def scroll_to_position(self, position):
        """Scroll the view to ensure the position is visible."""
        cursor = self.textCursor()
        cursor.setPosition(position)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()


class TypingInputWidget(QTextEdit):
    """Widget for user typing input."""
    
    typing_progress = Signal(int, bool)  # Position, correct/incorrect
    typing_complete = Signal()  # Emitted when typing is complete
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Courier New", 12))
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set a white background for the typing area
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        self.setPalette(palette)
        
        self._target_code = ""
        self._current_position = 0
        self._error_count = 0
        self._total_keystrokes = 0
        
    def set_target_code(self, code):
        """Set the target code that user needs to type."""
        self.clear()
        self._target_code = code
        self._current_position = 0
        self._error_count = 0
        self._total_keystrokes = 0
        
    def keyPressEvent(self, event):
        """Handle key press events for typing."""
        # Ignore if no target code is set
        if not self._target_code:
            return
            
        # Special handling for Enter/Return key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Get the expected character at current position
            if self._current_position < len(self._target_code):
                # Check if the next expected character is a newline
                expected_char = self._target_code[self._current_position]
                
                # Increment total keystrokes
                self._total_keystrokes += 1
                
                # Check if the expected character is a newline
                is_correct = expected_char == '\n'
                
                if not is_correct:
                    self._error_count += 1
                
                # Emit signal for typing progress
                self.typing_progress.emit(self._current_position, is_correct)
                
                if is_correct:
                    self._current_position += 1
                    
                    # Insert a newline in the text edit
                    cursor = self.textCursor()
                    cursor.insertText('\n')
                    self.setTextCursor(cursor)
                    
                    # Check if typing is complete
                    if self._current_position >= len(self._target_code):
                        self.typing_complete.emit()
            
            # Consume the event
            event.accept()
            return
            
        # Check if the key is a character key
        if event.text() and not event.modifiers() & (Qt.ControlModifier | Qt.AltModifier):
            # Get the expected character at current position
            if self._current_position < len(self._target_code):
                expected_char = self._target_code[self._current_position]
                typed_char = event.text()
                
                # Increment total keystrokes
                self._total_keystrokes += 1
                
                # Check if the typed character matches the expected one
                is_correct = typed_char == expected_char
                
                if not is_correct:
                    self._error_count += 1
                
                # Emit signal for typing progress
                self.typing_progress.emit(self._current_position, is_correct)
                
                if is_correct:
                    self._current_position += 1
                    
                    # Auto-scroll the text edit to keep the cursor visible
                    cursor = self.textCursor()
                    cursor.insertText(typed_char)
                    self.setTextCursor(cursor)
                    
                    # Check if typing is complete
                    if self._current_position >= len(self._target_code):
                        self.typing_complete.emit()
            
            # Consume the event
            event.accept()
        else:
            # Allow special keys like Ctrl+C, etc.
            super().keyPressEvent(event)
            
    def get_progress_percentage(self):
        """Get the current typing progress as a percentage."""
        if not self._target_code:
            return 0
        return (self._current_position / len(self._target_code)) * 100
    
    def get_accuracy(self):
        """Get the typing accuracy as a percentage."""
        if self._total_keystrokes == 0:
            return 100.0
        return 100.0 - (self._error_count / self._total_keystrokes * 100.0)
    
    def get_wpm(self, elapsed_seconds):
        """Calculate words per minute (WPM)."""
        if elapsed_seconds == 0:
            return 0
        
        # Standard: 5 characters = 1 word
        words = self._current_position / 5
        minutes = elapsed_seconds / 60
        
        if minutes == 0:
            return 0
            
        return words / minutes


class TypingGameWindow(QMainWindow):
    """Main window for the typing game."""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Code Typing Practice")
        self.resize(1000, 700)
        
        # Initialize code generator
        self.code_generator = CodeGenerator()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create settings area
        settings_frame = QFrame()
        settings_frame.setFrameShape(QFrame.StyledPanel)
        settings_layout = QHBoxLayout(settings_frame)
        
        # Language selection
        language_label = QLabel("Programming Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "C++", "Java", "Rust", "JavaScript"])
        settings_layout.addWidget(language_label)
        settings_layout.addWidget(self.language_combo)
        
        # Timer selection
        timer_label = QLabel("Timer Duration:")
        self.timer_combo = QComboBox()
        self.timer_combo.addItems(["30 seconds", "1 minute", "2 minutes", "3 minutes"])
        settings_layout.addWidget(timer_label)
        settings_layout.addWidget(self.timer_combo)
        
        # Start button
        self.start_button = QPushButton("Start Game")
        settings_layout.addWidget(self.start_button)
        
        # Add settings to main layout
        main_layout.addWidget(settings_frame)
        
        # Create splitter for code display and typing input
        splitter = QSplitter(Qt.Vertical)
        
        # Code display area
        self.code_display = CodeDisplayWidget()
        splitter.addWidget(self.code_display)
        
        # Typing input area
        self.typing_input = TypingInputWidget()
        self.typing_input.setEnabled(False)  # Disabled until game starts
        splitter.addWidget(self.typing_input)
        
        # Set initial splitter sizes
        splitter.setSizes([400, 300])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Timer display
        self.timer_display = QLabel("Time: 00:00")
        self.timer_display.setAlignment(Qt.AlignCenter)
        self.timer_display.setFont(QFont("Arial", 14, QFont.Bold))
        main_layout.addWidget(self.timer_display)
        
        # Set up timer
        self.game_timer = QTimer()
        self.game_timer.setInterval(1000)  # 1 second interval
        self.remaining_seconds = 0
        self.elapsed_seconds = 0
        self.current_code = ""
        
        # Connect signals and slots
        self.start_button.clicked.connect(self.start_game)
        self.game_timer.timeout.connect(self.update_timer)
        self.typing_input.typing_progress.connect(self.update_typing_progress)
        self.typing_input.typing_complete.connect(self.handle_typing_complete)
        
    def start_game(self):
        """Start the typing game."""
        # Get selected language and timer duration
        language = self.language_combo.currentText().lower()
        timer_text = self.timer_combo.currentText()
        
        # Map language names to code generator format
        language_map = {
            "python": "py",
            "c++": "cpp",
            "java": "java",
            "rust": "rust",
            "javascript": "javascript"
        }
        language_code = language_map.get(language, "py")
        
        # Parse timer duration
        if "seconds" in timer_text:
            self.remaining_seconds = int(timer_text.split()[0])
        else:
            minutes = int(timer_text.split()[0])
            self.remaining_seconds = minutes * 60
            
        # Reset elapsed time
        self.elapsed_seconds = 0
            
        # Update timer display
        self.update_timer_display()
        
        # Get code from the code generator
        try:
            self.current_code = self.code_generator.generate_code(language_code)
            
            # Ensure code is within the desired length range
            lines = self.current_code.splitlines()
            if len(lines) > 200:
                # Truncate to about 200 lines
                self.current_code = "\n".join(lines[:200])
            elif len(lines) < 175:
                # If too short, use sample code
                self.current_code = self.code_generator._get_sample_code(language_code)
                
        except Exception as e:
            # If code generation fails, use sample code
            self.current_code = self.code_generator._get_sample_code(language_code)
            QMessageBox.warning(self, "Code Generation Warning", 
                               f"Could not generate code from API. Using sample code instead.\nError: {str(e)}")
        
        # Set code in display and typing input
        self.code_display.set_code(self.current_code)
        self.typing_input.set_target_code(self.current_code)
        
        # Reset progress bar
        self.progress_bar.setValue(0)
        
        # Enable typing input and start timer
        self.typing_input.setEnabled(True)
        self.typing_input.setFocus()
        self.game_timer.start()
        
        # Disable settings during game
        self.language_combo.setEnabled(False)
        self.timer_combo.setEnabled(False)
        self.start_button.setEnabled(False)
        
    def update_timer(self):
        """Update the game timer."""
        self.remaining_seconds -= 1
        self.elapsed_seconds += 1
        self.update_timer_display()
        
        # Check if time is up
        if self.remaining_seconds <= 0:
            self.end_game()
            
    def update_timer_display(self):
        """Update the timer display label."""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_display.setText(f"Time: {minutes:02d}:{seconds:02d}")
        
    def update_typing_progress(self, position, is_correct):
        """Update the typing progress."""
        # Highlight current position in code display
        self.code_display.highlight_current_position(position, is_correct)
        
        # Scroll code display to keep current position visible
        self.code_display.scroll_to_position(position)
        
        # Update progress bar
        progress = self.typing_input.get_progress_percentage()
        self.progress_bar.setValue(int(progress))
        
    def handle_typing_complete(self):
        """Handle completion of typing."""
        self.end_game(completed=True)
        
    def end_game(self, completed=False):
        """End the typing game."""
        # Stop the timer
        self.game_timer.stop()
        
        # Disable typing input
        self.typing_input.setEnabled(False)
        
        # Re-enable settings
        self.language_combo.setEnabled(True)
        self.timer_combo.setEnabled(True)
        self.start_button.setEnabled(True)
        
        # Calculate statistics
        accuracy = self.typing_input.get_accuracy()
        wpm = self.typing_input.get_wpm(self.elapsed_seconds)
        progress = self.typing_input.get_progress_percentage()
        
        # Show results
        if completed:
            message = f"Congratulations! You completed the typing exercise.\n\n"
        else:
            message = f"Time's up!\n\n"
            
        message += f"Accuracy: {accuracy:.1f}%\n"
        message += f"Speed: {wpm:.1f} WPM\n"
        message += f"Progress: {progress:.1f}%\n"
        
        QMessageBox.information(self, "Game Results", message)
        
        # Update the timer display
        if completed:
            self.timer_display.setText("Completed!")
        else:
            self.timer_display.setText("Time's Up!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingGameWindow()
    window.show()
    sys.exit(app.exec())
