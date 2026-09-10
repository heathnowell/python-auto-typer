import tkinter as tk
from tkinter import ttk
from pynput import keyboard
from pynput.keyboard import Controller, Key
import threading
import time
import random
import re


# Globals
kb = Controller()
typing = False
paused = False
cursor_index = 0
typed_text = ""
hotkey = "<print_screen>"
type_delay = 60 / (100 * 5)  # was 150, now 100 WPM
error_chance = 0.03
pause_chance = 0.02
start_time = None


# New pause settings
pause_word_min = 10  # Minimum words before a pause
pause_word_max = 15  # Maximum words before a pause
pause_duration = 3.5 # Pause duration in seconds
pause_pattern = []   # List of word counts between pauses


# Typing stats
characters_typed = 0
words_typed = 0


adjacent_keys = {
    'a': ['q', 'w', 's', 'z'], 'b': ['v', 'g', 'h', 'n'], 'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'], 'e': ['w', 's', 'd', 'r'], 'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'], 'h': ['g', 'y', 'u', 'j', 'n', 'b'], 'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'n', 'm'], 'k': ['j', 'i', 'o', 'l', 'm'], 'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'], 'n': ['b', 'h', 'j', 'm'], 'o': ['i', 'k', 'l', 'p'], 'p': ['o', 'l'],
    'q': ['a', 's', 'w'], 'r': ['e', 'd', 'f', 't'], 's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'f', 'g', 'y'], 'u': ['y', 'h', 'j', 'i'], 'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'a', 's', 'e'], 'x': ['z', 's', 'd', 'c'], 'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x'], '1': ['2', 'q'], '2': ['1', 'q', 'w', '3'], '3': ['2', 'w', 'e', '4'],
    '4': ['3', 'e', 'r', '5'], '5': ['4', 'r', 't', '6'], '6': ['5', 't', 'y', '7'],
    '7': ['6', 'y', 'u', '8'], '8': ['7', 'u', 'i', '9'], '9': ['8', 'i', 'o', '0'], '0': ['9', 'o', 'p']
}


def get_adjacent_keys(char):
    return adjacent_keys.get(char.lower(), [char])


def generate_pause_pattern(total_words, min_words, max_words):
    """
    Generates a predetermined list of word counts between pauses,
    such that the sum covers all words in the text.
    """
    pattern = []
    words_left = total_words
    rng = random.Random(42)  # Fixed seed for reproducibility
    while words_left > 0:
        next_count = rng.randint(min_words, max_words)
        if next_count > words_left:
            next_count = words_left
        pattern.append(next_count)
        words_left -= next_count
    return pattern


def calculate_initial_time():
    remaining_chars = len(typed_text)
    base_time = remaining_chars * type_delay
    estimated_errors = error_chance * remaining_chars
    estimated_pauses = pause_chance * remaining_chars
    error_time = estimated_errors * type_delay * 6  # more realistic
    pause_time = estimated_pauses * 1.0


    # Calculate number of words in the text
    planned_word_pauses = len(pause_pattern)
    planned_pause_time = planned_word_pauses * pause_duration


    return base_time + error_time + pause_time + planned_pause_time


def update_timer_and_progress():
    total_chars = len(typed_text)
    total_estimated_time = calculate_initial_time()
    start = time.time()
    dynamic_remaining = total_estimated_time


    while typing:
        elapsed = time.time() - start
        progress = cursor_index / total_chars
        ideal_remaining = (1 - progress) * total_estimated_time
        dynamic_remaining = dynamic_remaining * 0.9 + ideal_remaining * 0.1


        # Update time and progress bar
        if dynamic_remaining >= 60:
            mins = int(dynamic_remaining // 60)
            secs = int(dynamic_remaining % 60)
            time_display = f"{mins} minutes and {secs} seconds left"
        else:
            time_display = f"{dynamic_remaining:.1f} seconds left"


        progress_bar["value"] = progress * 100
        progress_label.config(text=f"Typing Progress: {progress * 100:.2f}%")
        time_label.config(text=time_display)
        root.update_idletasks()
        time.sleep(0.05)


def auto_type():
    global typing, paused, cursor_index, characters_typed, words_typed


    total_length = len(typed_text)
    threading.Thread(target=update_timer_and_progress, daemon=True).start()


    word_pause_index = 0
    words_since_pause = 0
    next_pause_at = pause_pattern[word_pause_index] if pause_pattern else float('inf')
    in_word = False  # Track if currently inside a word


    while typing and cursor_index < total_length:
        if paused:
            time.sleep(0.1)
            continue


        char = typed_text[cursor_index]


        if random.random() < pause_chance:
            time.sleep(2.5)  # random pause for realism


        if random.random() < error_chance and char not in (' ', '\n', '\t'):
            wrong_char = random.choice(get_adjacent_keys(char))
            kb.press(wrong_char)
            kb.release(wrong_char)
            time.sleep(type_delay * 2.5)
            kb.press(Key.backspace)
            kb.release(Key.backspace)
            time.sleep(type_delay / 2)


        if char == '\n':
            kb.press(Key.enter)
            kb.release(Key.enter)
        else:
            kb.press(char)
            kb.release(char)
        time.sleep(type_delay)


        characters_typed += 1


        # Word boundary logic: only count a word after a non-space followed by a space or newline
        if char not in (' ', '\n', '\t'):
            in_word = True
        elif in_word and char in (' ', '\n', '\t'):
            words_typed += 1
            words_since_pause += 1
            in_word = False


            # Only pause at predetermined word boundaries
            if words_since_pause == next_pause_at:
                time.sleep(pause_duration)
                words_since_pause = 0
                word_pause_index += 1
                if word_pause_index < len(pause_pattern):
                    next_pause_at = pause_pattern[word_pause_index]
                else:
                    next_pause_at = float('inf')


        cursor_index += 1


    typing = False
    progress_bar["value"] = 100
    progress_label.config(text="Typing Complete!")
    time_label.config(text="0.0 seconds left")


def on_activate():
    global typing, paused
    if typing:
        paused = not paused
        if paused:
            status_label.config(text="Paused. Press hotkey again to resume.", foreground="orange")
        else:
            status_label.config(text="Resumed typing.", foreground="blue")
    else:
        typing = True
        paused = False
        threading.Thread(target=auto_type, daemon=True).start()


def start_hotkey_listener():
    def listener_thread():
        with keyboard.GlobalHotKeys({hotkey: on_activate}) as h:
            h.join()
    threading.Thread(target=listener_thread, daemon=True).start()


def apply_settings():
    global type_delay, error_chance
    try:
        wpm = int(wpm_entry.get())
        type_delay = 60 / (wpm * 5)
    except:
        type_delay = 60 / (100 * 5)
    try:
        val = int(typo_entry.get())
        error_chance = val / 100
    except:
        error_chance = 0.03
    status_label.config(text=f"Speed: {wpm_entry.get()} WPM, Typos: {typo_entry.get()}%", foreground="blue")


def set_wpm(): apply_settings()
def set_typos(): apply_settings()


def start_typing():
    global typed_text, cursor_index, typing, paused, pause_pattern, words_typed
    apply_settings()
    typed_text = text_entry.get("1.0", tk.END).rstrip('\n')
    if not typed_text.strip():
        status_label.config(text="Text box is empty!", foreground="red")
        return
    cursor_index = 0
    typing = False
    paused = False
    words_typed = 0
    progress_bar["value"] = 0
    progress_label.config(text="Typing Progress: 0.00%")
    # Count words as groups of non-space between spaces/newlines
    total_words = len(re.findall(r'\b\S+\b', typed_text))
    pause_pattern.clear()
    pause_pattern.extend(generate_pause_pattern(total_words, pause_word_min, pause_word_max))
    remaining = calculate_initial_time()
    if remaining >= 60:
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        time_label.config(text=f"{mins} minutes and {secs} seconds")
    else:
        time_label.config(text=f"{remaining:.1f} seconds")
    start_hotkey_listener()
    status_label.config(text="Ready. Press PRTSC to start.", foreground="blue")
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    hotkey_btn.config(state="disabled")


def stop_typing():
    global typing, paused, cursor_index
    typing = False
    paused = False
    cursor_index = 0
    progress_bar["value"] = 0
    progress_label.config(text="Typing Progress: 0.00%")
    time_label.config(text="")
    status_label.config(text="Stopped.", foreground="gray")
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")
    hotkey_btn.config(state="normal")


def capture_hotkey():
    status_label.config(text="Press any key to set hotkey...", foreground="green")
    def on_press(key):
        global hotkey
        try:
            hk = f"<{key.char}>"
        except AttributeError:
            hk = f"<{key.name}>"
        hotkey = hk
        hotkey_display.config(text=f"Hotkey: {hotkey}")
        status_label.config(text="Hotkey set!", foreground="blue")
        return False
    threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).run(), daemon=True).start()


def on_close():
    stop_typing()
    root.quit()


root = tk.Tk()
root.title("Auto Typer v2")
root.geometry("465x390")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)
root.attributes("-topmost", True)


main_frame = ttk.Frame(root, padding="15")
main_frame.grid(row=0, column=0, padx=10, pady=0)


font_main = ("Arial", 10)
font_status = ("Arial", 8)


ttk.Label(main_frame, text="Auto Typer v2", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=0, sticky="nsew")


start_btn = ttk.Button(main_frame, text="Start Typing", command=start_typing)
start_btn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
stop_btn = ttk.Button(main_frame, text="Stop", command=stop_typing, state="disabled")
stop_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")


hotkey_btn = ttk.Button(main_frame, text="Set Hotkey", command=capture_hotkey)
hotkey_btn.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
hotkey_display = ttk.Label(main_frame, text="Hotkey: PRTSC", font=font_main)
hotkey_display.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")


ttk.Label(main_frame, text="WPM:", font=font_main).grid(row=2, column=0, sticky="w")
wpm_entry = ttk.Entry(main_frame, width=10)
wpm_entry.insert(0, "100")
wpm_entry.grid(row=2, column=1, padx=5)
wpm_btn = ttk.Button(main_frame, text="Set", command=set_wpm)
wpm_btn.grid(row=2, column=2, padx=5, pady=5)


ttk.Label(main_frame, text="Error Rate (%):", font=font_main).grid(row=3, column=0, sticky="w")
typo_entry = ttk.Entry(main_frame, width=10)
typo_entry.insert(0, "3")
typo_entry.grid(row=3, column=1, padx=5)
typo_btn = ttk.Button(main_frame, text="Set", command=set_typos)
typo_btn.grid(row=3, column=2, padx=5, pady=5)


text_entry = tk.Text(main_frame, wrap=tk.WORD, height=8, width=50)
text_entry.grid(row=4, column=0, columnspan=4, padx=5, pady=5)


status_label = ttk.Label(main_frame, text="Ready. Press PRTSC to start.", font=font_status, foreground="blue")
status_label.grid(row=5, column=0, columnspan=4, pady=5)


progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
progress_label = ttk.Label(main_frame, text="Typing Progress: 0.00%", font=font_status)
progress_label.grid(row=7, column=0, columnspan=4, pady=0)
time_label = ttk.Label(main_frame, text="0.0 seconds left", font=font_status)
time_label.grid(row=8, column=0, columnspan=4, pady=0)


root.mainloop()