# Code Typing Practice Game

A typing game to help users improve their programming typing skills with support for multiple programming languages and customizable timer settings.

## Features

- **Multiple Programming Languages**: Practice typing in Python, C++, Java, Rust, and JavaScript
- **Customizable Timer**: Set practice sessions from 30 seconds to 3 minutes
- **Real-time Feedback**: Get immediate visual feedback on typing accuracy
- **Performance Metrics**: View your typing speed (WPM), accuracy, and progress
- **Code Generation**: Uses Hugging Face's DeepSeek-R1-0528 model to generate programming examples

## Requirements

- Python 3.6+
- PySide6
- huggingface_hub

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install pyside6 huggingface_hub
```

3. Set up your Hugging Face API token (optional for full functionality):
   - Create an account on [Hugging Face](https://huggingface.co/)
   - Generate an API token in your account settings
   - Set the token as an environment variable:
     ```bash
     export HF_TOKEN="your_token_here"
     ```
   - Note: The game will work without a token by using built-in sample code

## Usage

Run the game by executing:

```bash
python main.py
```

### Game Instructions

1. **Select a Programming Language**: Choose from Python, C++, Java, Rust, or JavaScript
2. **Set Timer Duration**: Select a practice session length from 30 seconds to 3 minutes
3. **Start Game**: Click the "Start Game" button to begin
4. **Type the Code**: Type the displayed code in the input area
5. **View Results**: After completing the code or when time expires, view your performance metrics

## Project Structure

- `main.py`: Entry point for the application
- `typing_game_gui.py`: PySide6 GUI implementation
- `code_generator.py`: Code generation using Hugging Face API

## Code Generation

The game uses the DeepSeek-R1-0528 model from Hugging Face to generate programming examples. If the API is unavailable or no token is provided, the game falls back to built-in sample code for each language.

To use your own Hugging Face API token:

1. Edit the `code_generator.py` file
2. Replace the mock API key with your actual token:
   ```python
   os.environ["HF_TOKEN"] = "your_actual_token_here"
   ```

## Customization

You can customize the game by:

- Adding more programming languages in `code_generator.py`
- Modifying the timer durations in `typing_game_gui.py`
- Changing the visual styling in the GUI classes

## Troubleshooting

### Common Issues

- **Qt Platform Plugin Error**: If you see an error about Qt platform plugins, ensure you have the necessary system libraries:
  ```bash
  # For Ubuntu/Debian
  sudo apt-get install libxcb-cursor0
  ```

- **API Connection Issues**: If code generation fails, check your internet connection and API token. The game will use sample code as a fallback.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the DeepSeek-R1-0528 model
- [PySide6](https://wiki.qt.io/Qt_for_Python) for the GUI framework
