# Bhanu AI - Terminal Assistant 🚀

**Bhanu AI** is a fast, intelligent, voice-and-terminal-ready AI assistant engineered for Linux systems. Powered by Google's **Gemini 3 models**, it provides an interactive command-line interface with real-time autonomous system control, file management, live web search, developer tools, and persistent memory.

---

## ⚡ Quick Start

### 1. Run in Terminal
Navigate to the project folder and launch Bhanu AI:

```bash
cd ~/Desktop/bhanuai
./run.sh
```
*(or run directly with Python)*:
```bash
python3 main.py
```

### 2. Connect Your Free Google Gemini API Key
On first launch, Bhanu AI will prompt you to enter your Gemini API key.
1. Get a 100% free API key at **[Google AI Studio](https://aistudio.google.com/apikey)**.
2. Paste your key into the terminal prompt.
3. The key is automatically saved in `config.json` so you only need to enter it once!

> You can also update or switch keys anytime in the chat using `/key`.

---

## ✨ Features & Capabilities

| Capability | Example Terminal Commands |
|---|---|
| 🖥️ **Bash & Terminal** | *"Check my disk space"*, *"List running python processes"*, *"Show git status"* |
| 📁 **File Controller** | *"List files on my Desktop"*, *"Read main.py"*, *"Create a python script called hello.py"* |
| 🌐 **Live Web Search** | *"Search latest news on AI"*, *"Who won yesterday's football match?"* |
| 🌦️ **Weather Forecast** | *"What's the weather in Hyderabad today?"*, *"Is it raining in London?"* |
| ⚙️ **System Control** | *"Increase volume by 10%"*, *"Mute volume"*, *"Take a screenshot"*, *"Send a notification"* |
| 🚀 **App Launcher** | *"Open Chrome"*, *"Launch VS Code"*, *"Open Dolphin file manager"* |
| 💻 **Code Helper** | *"Write a python script to parse JSON"*, *"Check syntax of script.py"*, *"Run test.py"* |
| 🧠 **Persistent Memory** | Remembers your preferences, project details, and notes across sessions. |

---

## ⌨️ Terminal Slash Commands

Inside the Bhanu AI terminal, you can type special slash commands anytime:

- `/help` — Display full command and capability menu
- `/key` — View or update your Google Gemini API Key
- `/model` — Switch active Gemini 3 model (`gemini-3-flash-preview`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemini-3.8-flash`)
- `/tools` — Inspect all active tool declarations and parameters
- `/memory` — View persistent facts and saved user notes
- `/history` — Check the current session conversation turn count
- `/reset` — Reset the active conversation context
- `/clear` — Clear the terminal screen and reprint the Bhanu AI banner
- `/exit` — Exit Bhanu AI

---

## 📂 Project Architecture

```
~/Desktop/bhanuai/
├── main.py              # Main terminal application loop
├── run.sh               # Quick executable launcher
├── config.json          # User configuration & API key storage
├── requirements.txt     # Optional lightweight dependencies
├── README.md            # Project documentation
│
├── core/
│   ├── gemini_client.py # Gemini API client with function-calling loops
│   ├── config.py        # Configuration manager
│   ├── prompt.py        # Bhanu AI system prompt & personality
│   └── ui.py            # ANSI terminal UI styling, banners, spinners
│
├── tools/
│   ├── registry.py      # Tool dispatcher & Gemini schema declarations
│   ├── system_tools.py  # Bash commands, system stats, volume, apps, screenshots
│   ├── file_tools.py    # File reading, writing, searching, disk analysis
│   ├── web_tools.py     # Live DuckDuckGo & Wikipedia search, weather, URL fetcher
│   └── dev_tools.py     # Python code execution, syntax checking, code writing
│
└── memory/
    ├── memory_manager.py# Persistent long-term memory controller
    └── memory.json      # Saved user facts, notes, and preferences
```

---

## 🛠️ Zero External Dependency Design

Bhanu AI is engineered with Linux native tools and the Python standard library. It runs immediately on modern Linux (Fedora, Ubuntu, Debian, Arch) without requiring compilation or risky package installations!
