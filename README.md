# Python Auto Typer

A desktop typing-automation application built with Python and Tkinter.

The application accepts user-provided text and types it through the keyboard controller at a configurable speed. It also includes hotkey controls, progress tracking, estimated completion time, optional simulated typing errors, and pauses.

## Features

- Desktop GUI built with Tkinter
- Paste or enter text to be typed automatically
- Adjustable typing speed in words per minute (WPM)
- Adjustable simulated typo rate
- Configurable global hotkey
- Start, stop, pause, and resume controls
- Progress bar and percentage tracking
- Estimated remaining time
- Word-based and randomized pauses
- Simulated nearby-key typing mistakes followed by correction
- Background threads so the interface remains responsive

## Technologies

- Python
- Tkinter
- `pynput`
- Threading
- Regular expressions
- Randomization
- Time-based event handling

## Project Structure

```text
python-auto-typer/
├── autotype.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/python-auto-typer.git
cd python-auto-typer
```

Install the required dependency:

```bash
pip install pynput
```

Tkinter is included with many standard Python installations. Depending on your operating system, it may need to be installed separately.

If the repository includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python autotype.py
```

Then:

1. Enter or paste text into the text box.
2. Set the desired WPM.
3. Set the desired typo percentage.
4. Optionally choose a custom hotkey.
5. Click **Start Typing**.
6. Move your cursor to the application where the text should be entered.
7. Press the configured hotkey to begin.
8. Press the hotkey again to pause or resume.
9. Use **Stop** to end the typing process.

The default hotkey is:

```text
Print Screen
```

## How It Works

### Typing Speed

The program converts the selected WPM into a delay between characters:

```python
type_delay = 60 / (wpm * 5)
```

### Typing Automation

The application uses `pynput.keyboard.Controller` to send keyboard input one character at a time.

### Simulated Errors

The project includes a map of nearby keyboard keys. When an error is triggered, it types a nearby character, waits briefly, presses Backspace, and then continues.

### Pause Pattern

The program creates a repeatable sequence of word-count intervals and pauses after those intervals while typing.

### Progress and Time Estimation

A background thread tracks:

- Characters typed
- Percentage complete
- Estimated time remaining

This allows the GUI to update while the typing process is running.

## What I Learned

This project helped me practice:

- GUI development with Tkinter
- Keyboard input automation
- Multithreading
- Global hotkey handling
- State management
- Event-driven programming
- Timing and progress calculations
- User-configurable application settings
- Debugging a larger Python application

## Future Improvements

Possible future improvements include:

- Save user settings between sessions
- Cleaner separation between GUI and typing logic
- Cross-platform hotkey testing
- More robust input validation
- Additional pause behavior controls
- Packaging the application as a standalone executable
- Automated tests for timing and text-processing logic

## Responsible Use

This project is intended for legitimate automation, testing, accessibility, and personal programming practice. Users are responsible for following the rules, policies, and terms of service of any software or platform where the tool is used.
