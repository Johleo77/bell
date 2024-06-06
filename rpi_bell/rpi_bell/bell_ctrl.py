#######################################################################################################################
# Module informations
#######################################################################################################################
__project__ = "ECOTRON IDF - Ouverture et fermeture d'une cloche"
__author__ = "Johan Leonard (johanleonard77@gmail.com)"
__modifiers__ = ""
__history__ = """
    - Revision 1.0 (2024/06/04) : First Version.
              """
__date__ = "2024/06/06"
__version__ = "1.0.2"


#######################################################################################################################
import RPi.GPIO as GPIO
import time
import tkinter as tk
import json
import os

# Configuration file path
CONFIG_FILE = "conf/config.json"

GPIO.setwarnings(False)

status = "Unknown"

# Function to read the configuration from a JSON file
def read_config(config_file):
    if os.path.exists(config_file):
        print(config_file)
        with open(config_file, "rt") as file:
            return json.load(file)
    
# Function to write the configuration to a JSON filedef write_config(config_file):
    with open(config_file, "wt") as file:
        json.dump(config, file)

# Read the initial configuration
config = read_config(config_file=CONFIG_FILE)
motor_gpio = config["motor_gpio"]
button_gpio = config["button_gpio"]
motor_duration = config["motor_duration"]

# GPIO pin configuration
# - GPIO. BCM: GPIO Number
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_gpio, GPIO.OUT) # Spindle to control the motor
GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pin to read button status

# Function to start the engine
def open_bell():
    print("opening the bell")
    GPIO.output(motor_gpio, GPIO.LOW)
    time.sleep(motor_duration)

# Function to stop the engine
def close_bell():
    print("closing the bell")
    GPIO.output(motor_gpio, GPIO.HIGH)
    time.sleep(motor_duration)
    
# Function to know the position of the bell
def get_bell_status():
    motor_status = GPIO.input(motor_gpio)
    button_status = GPIO.input(button_gpio)
    print(f"motor_status = {motor_status}, button_status = {button_status}")
    
    pos_status_str = ""
    move_status_str = ""
    
    if motor_status == GPIO.HIGH:
        pos_status_str = "close"
    else:
        pos_status_str = "open"
        

    if button_status == GPIO.LOW:
        move_status_str = "move"
    else:
        move_status_str = "stop"

    status = pos_status_str + " " + move_status_str
    status_label.config(text=status)
    print(f"status = {status}")

# Function to display status
def show_status():
    current_status = status_bell()
    status_label.config(text=f"Status: {current_status}")

# Creation of the graphical interface
root = tk.Tk()
root.title("Contrôle du moteur")

start_button = tk.Button(root, text="Open", command=open_bell)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Close", command=close_bell)
stop_button.pack(pady=10)

status_button = tk.Button(root, text="Status", command=get_bell_status)
status_button.pack(pady=10)

status_label = tk.Label(root, text=f"Status: {status}")
status_label.pack(pady=10)

# Function to manage the closure of the application
def on_closing():
    GPIO.cleanup()
    write_config(config)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop of Tkinter
root.mainloop()
