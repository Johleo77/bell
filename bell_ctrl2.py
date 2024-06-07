#######################################################################################################################
# Module informations
#######################################################################################################################
__project__ = "ECOTRON IDF - Ouverture et fermeture de deux cloches"
__author__ = "Johan Leonard (johanleonard77@gmail.com)"
__modifiers__ = ""
__history__ = """
    - Revision 1.0 (2024/06/04) : First Version.
              """
__date__ = "2024/06/07"
__version__ = "1.0.0"


#######################################################################################################################
import RPi.GPIO as GPIO
import time
import tkinter as tk
import json
import os

# Configuration file path
CONFIG_FILE2 = "conf/config2.json"

GPIO.setwarnings(False)

status = "Unknown"

# Function to read the configuration from a JSON file
def read_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, "rt") as file:
            return json.load(file)
    
# Function to write the configuration to a JSON file
def write_config(config, config_file):
    with open(config_file, "wt") as file:
        json.dump(config, file)

# Read the initial configuration
config = read_config(config_file=CONFIG_FILE2)
bell1_config = config["bell1"]
bell2_config = config["bell2"]

# GPIO pin configuration
# - GPIO. BCM: GPIO Number
GPIO.setmode(GPIO.BCM)
# Bell 1
GPIO.setup(bell1_config["motor_gpio"], GPIO.OUT) # Spindle to control the motor
GPIO.setup(bell1_config["button_gpio"], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pin to read button status
# Bell 2
GPIO.setup(bell2_config["motor_gpio"], GPIO.OUT) # Spindle to control the motor
GPIO.setup(bell2_config["button_gpio"], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pin to read button status

# Function to start the engine for bell 1
def open_bell1():
    print("opening bell 1")
    GPIO.output(bell1_config["motor_gpio"], GPIO.LOW)
    time.sleep(bell1_config["motor_duration"])

# Function to stop the engine for bell 1
def close_bell1():
    print("closing bell 1")
    GPIO.output(bell1_config["motor_gpio"], GPIO.HIGH)
    time.sleep(bell1_config["motor_duration"])

# Function to get the status of bell 1
def get_bell1_status():
    motor_status = GPIO.input(bell1_config["motor_gpio"])
    button_status = GPIO.input(bell1_config["button_gpio"])
    print(f"bell 1 motor_status = {motor_status}, button_status = {button_status}")
    
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

    status = f"Bell 1: {pos_status_str} {move_status_str}"
    status_label.config(text=status)
    print(f"status = {status}")

# Function to start the engine for bell 2
def open_bell2():
    print("opening bell 2")
    GPIO.output(bell2_config["motor_gpio"], GPIO.LOW)
    time.sleep(bell2_config["motor_duration"])

# Function to stop the engine for bell 2
def close_bell2():
    print("closing bell 2")
    GPIO.output(bell2_config["motor_gpio"], GPIO.HIGH)
    time.sleep(bell2_config["motor_duration"])

# Function to get the status of bell 2
def get_bell2_status():
    motor_status = GPIO.input(bell2_config["motor_gpio"])
    button_status = GPIO.input(bell2_config["button_gpio"])
    print(f"bell 2 motor_status = {motor_status}, button_status = {button_status}")
    
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

    status = f"Bell 2: {pos_status_str} {move_status_str}"
    status_label.config(text=status)
    print(f"status = {status}")

# Function to display status of both bells
def show_status():
    get_bell1_status()
    get_bell2_status()

# Creation of the graphical interface
root = tk.Tk()
root.title("opening/closing of bells")

# Bell 1 controls
start_button1 = tk.Button(root, text="Open Bell 1", command=open_bell1)
start_button1.pack(pady=10)

stop_button1 = tk.Button(root, text="Close Bell 1", command=close_bell1)
stop_button1.pack(pady=10)

status_button1 = tk.Button(root, text="Status Bell 1", command=get_bell1_status)
status_button1.pack(pady=10)

# Bell 2 controls
start_button2 = tk.Button(root, text="Open Bell 2", command=open_bell2)
start_button2.pack(pady=10)

stop_button2 = tk.Button(root, text="Close Bell 2", command=close_bell2)
stop_button2.pack(pady=10)

status_button2 = tk.Button(root, text="Status Bell 2", command=get_bell2_status)
status_button2.pack(pady=10)

status_label = tk.Label(root, text=f"Status: {status}")
status_label.pack(pady=10)




# Function to manage the closure of the application
def on_closing():
    GPIO.cleanup()
    write_config(config, CONFIG_FILE2)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop of Tkinter
root.mainloop()
