import socket
import pyaudio
import threading
import RPi.GPIO as GPIO
# Sender configuration

SENDER_HOST = '0.0.0.0'  # Host IP
RECEIVER_IPS = ['192.168.29.183', '192.168.29.184']  # List of receiver's IP addresses
RECEIVER_PORT = 12346   # Port for receiver
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096  # Maximum size of each packet
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# Initialize PyAudio
audio = pyaudio.PyAudio()
sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Set up sender and receiver sockets
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the receiver sockets for each IP
receiver_sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in RECEIVER_IPS]
for r_socket in receiver_sockets:
    r_socket.bind((SENDER_HOST, RECEIVER_PORT))

def send_audio():
    while True:
        if True:
            data = sender_stream.read(CHUNK)
            for receiver_ip in RECEIVER_IPS:
                for i in range(0, len(data), MAX_PACKET_SIZE):
                    chunk = data[i:i+MAX_PACKET_SIZE]
                    sender_socket.sendto(chunk, (receiver_ip, RECEIVER_PORT))

def receive_audio(receiver_socket):
    keyword = b'alexa'  # Convert the keyword to bytes
    while True:
        data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
        receiver_stream.write(data)
        # Check if the keyword is present in the received data
        if keyword in data:
            GPIO.output(17, GPIO.HIGH)  # Set GPIO pin 17 to HIGH
        else:
            GPIO.output(17, GPIO.LOW)  # Set GPIO pin 17 to LOW


# Start sender and receiver threads
sender_thread = threading.Thread(target=send_audio, daemon=True)
receiver_threads = [threading.Thread(target=receive_audio, args=(r_socket,), daemon=True) for r_socket in receiver_sockets]

sender_thread.start()
for r_thread in receiver_threads:
    r_thread.start()

while True:
    pass
