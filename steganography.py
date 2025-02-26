import cv2
import numpy as np
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message).decode()

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if int(char, 2) != 254)

def hide_data(image_path, secret_message, output_image):
    image = cv2.imread(image_path)
    binary_message = message_to_binary(secret_message) + '1111111111111110'
    data_index = 0
    data_length = len(binary_message)
    rows, cols, channels = image.shape

    for row in range(rows):
        for col in range(cols):
            for channel in range(3):
                if data_index < data_length:
                    pixel_binary = format(image[row, col, channel], '08b')
                    new_pixel_binary = pixel_binary[:-1] + binary_message[data_index]
                    image[row, col, channel] = int(new_pixel_binary, 2)
                    data_index += 1

    cv2.imwrite(output_image, image)

def extract_data(image_path):
    image = cv2.imread(image_path)
    binary_data = ""

    for row in image:
        for pixel in row:
            for channel in pixel:
                binary_data += format(channel, '08b')[-1]

    return binary_to_message(binary_data)
