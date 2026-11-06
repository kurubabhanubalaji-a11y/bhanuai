#!/usr/bin/env python3
"""
Bhanu AI - Terminal Assistant
Powered by Google Gemini Free API
"""

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config import get_api_key, get_model, load_config, set_api_key, set_model
from core.gemini_client import GeminiClient
from core.ui import (
    clear_screen,
    print_ai_prefix,
    print_banner,
    print_error,
    print_help_menu,
    print_info,
    print_status,
    print_success,
    print_tool_call,
    print_tool_result,
    print_user_prompt,
    print_warning,
    stream_ai_text,
)
from memory.memory_manager import load_memory
from tools.registry import get_tool_declarations


def prompt_api_key_setup() -> str:
    """Interactively ask the user for their free Gemini API Key on first launch."""
    print("\n" + "=" * 65)
    print(" 🔑 Google Gemini API Key Setup (Gemini 3 Ready)")
    print("=" * 65)
    print(" Bhanu AI connects directly to Google Gemini's latest 3.x models.")
    print(" If you don't have a key yet, get one free in 30 seconds at:")
    print(" 👉 https://aistudio.google.com/apikey\n")

    try:
        key_input = input(" Enter your Gemini API key (or press Enter to skip for now): ").strip().strip("'\"")
    except (EOFError, KeyboardInterrupt):
        return ""

    if key_input:
        is_valid, msg, models = GeminiClient.validate_api_key(key_input)
        set_api_key(key_input)
        if is_valid:
            print_success(f"Gemini API Key verified and saved successfully to config.json! ({len(models)} models accessible)")
        else:
            print_warning(f"Key saved, but validation warning: {msg}")
        return key_input
    else:
        print_warning("No key entered. You can set it later anytime with the '/key' command.\n")
        return ""


def handle_slash_command(cmd: str, client: GeminiClient) -> bool:
    """Handle special terminal slash commands. Return True if command was handled."""
    parts = cmd.strip().split(maxsplit=1)
    keyword = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if keyword in ("/exit", "/quit", "/q"):
        print_info("Goodbye! Have a great day, Bhanu.")
        sys.exit(0)

    elif keyword in ("/help", "/h", "?"):
        print_help_menu()
        return True

    elif keyword in ("/clear", "/cls"):
        clear_screen()
        cfg = load_config()
        print_banner(user_name=cfg.get("user_name", "Bhanu"), model_name=client.model)
        return True

    elif keyword in ("/reset", "/new"):
        client.clear_history()
        print_success("Conversation context reset.")
        return True

    elif keyword in ("/history", "/turns"):
        turns = client.get_history_length()
        print_info(f"Active conversation history: {turns} message turns stored.")
        return True

    elif keyword in ("/memory", "/mem"):
        mem = load_memory()
        print_info("Persistent User Memory:")
        print(f"  • User Name: {mem.get('user_name')}")
        print(f"  • Operating System: {mem.get('preferences', {}).get('os')}")
        notes = mem.get("notes", [])
        if notes:
            print("  • Saved Notes & Facts:")
            for idx, n in enumerate(notes, 1):
                print(f"    {idx}. {n}")
        else:
            print("  • (No custom notes yet)")
        return True

    elif keyword == "/key":
        current_key = get_api_key()
        if arg:
            clean_arg = arg.strip().strip("'\"")
            is_valid, msg, models = GeminiClient.validate_api_key(clean_arg)
            set_api_key(clean_arg)
            client.set_key(clean_arg)
            if is_valid:
                print_success(f"Gemini API key verified & saved! ({len(models)} models accessible)")
            else:
                print_warning(f"Key saved, but validation warning: {msg}")
        else:
            if current_key:
                masked = current_key[:6] + "..." + current_key[-4:] if len(current_key) > 10 else "***"
                print_info(f"Current Gemini API key: {masked}")
            else:
                print_warning("No Gemini API key is configured.")

            print("To update, enter your key below (or press Enter to cancel):")
            try:
                new_key = input("New API Key: ").strip().strip("'\"")
                if new_key:
                    is_valid, msg, models = GeminiClient.validate_api_key(new_key)
                    set_api_key(new_key)
                    client.set_key(new_key)
                    if is_valid:
                        print_success(f"API Key updated and verified! ({len(models)} models accessible)")
                    else:
                        print_warning(f"API Key saved, but validation check reported: {msg}")
            except (EOFError, KeyboardInterrupt):
                pass
        return True

    elif keyword == "/model":
        if arg:
            set_model(arg)
            client.set_model(arg)
            print_success(f"Switched model to '{arg}'.")
        else:
            print_info(f"Current active model: {client.model}")
            print("\nRecommended Gemini 3 models:")
            print("  • gemini-3-flash-preview   (Fastest, recommended default)")
            print("  • gemini-3.5-flash         (High intelligence, multimodal)")
            print("  • gemini-3.1-flash-lite    (Low-latency lightweight)")
            print("  • gemini-3.6-flash         (Advanced reasoning)")
            print("  • gemini-3.8-flash         (Next-gen experimental)")
            print("  • gemini-3.1-pro-preview   (Pro tier preview)")
            print("\nSwitch by typing: /model <model_name>")
        return True

    elif keyword == "/tools":
        tools = get_tool_declarations()
        print_info(f"Bhanu AI Registered Tools ({len(tools)} available):")
        for t in tools:
            print(f"  • \033[1m{t['name']}\033[0m: {t['description']}")
        return True

    return False


def main():
    """Main terminal loop for Bhanu AI."""
    cfg = load_config()
    api_key = get_api_key()

    if not api_key:
        api_key = prompt_api_key_setup()

    client = GeminiClient(api_key=api_key, model=cfg.get("model", "gemini-3-flash-preview"))

    clear_screen()
    print_banner(user_name=cfg.get("user_name", "Bhanu"), model_name=client.model)

    if not api_key:
        print_warning("Note: No Gemini API Key provided yet. Type '/key' to connect to Gemini.\n")

    while True:
        try:
            print_status("LISTENING")
            user_input = print_user_prompt(cfg.get("user_name", "Bhanu"))

            if not user_input:
                continue

            # Check for slash commands
            if user_input.startswith("/"):
                handled = handle_slash_command(user_input, client)
                if handled:
                    print()
                    continue

            # Regular AI prompt
            print_status("THINKING")

            response = client.chat(
                user_message=user_input,
                on_tool_call=lambda name, args: print_tool_call(name, args),
                on_tool_result=lambda name, res: print_tool_result(name, res),
            )

            print_ai_prefix()
            stream_ai_text(response)
            print()

        except KeyboardInterrupt:
            print("\n")
            print_info("Use /exit or press Ctrl+D to exit.")
        except EOFError:
            print("\n")
            print_info("Exiting Bhanu AI. Goodbye!")
            break
        except Exception as e:
            print_error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
