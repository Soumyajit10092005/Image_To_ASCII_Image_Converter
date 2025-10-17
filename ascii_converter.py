# Convert image to ASCII image with the help of Python 
# Written By : MRX
import os
import threading
import pygame
import time
from PIL import Image, ImageOps, ImageEnhance

def img_to_ascii_img(img_path, width, duration):
    start_time = time.time()
    # Open image in Greyscale mode
    img = Image.open(img_path).convert('L')

    # Contrast and adjust the Image
    img = ImageOps.autocontrast(img, cutoff = 1)
    img = ImageEnhance.Brightness(img).enhance(1.3)
    img = ImageEnhance.Contrast(img).enhance(2.2)

    # Resize the image
    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width * 0.55)
    img = img.resize((width, new_height))

    # Brightness mapping
    pixels = img.getdata()
    ascii_chars = " .:-=+*#%@"
    ascii_data = [ascii_chars[p * len(ascii_chars) // 256] for p in pixels]
    total_line = len(ascii_data) // width
    if total_line > 0:
        delay = duration / total_line
    else:
        delay = 0.05

    terminal_width = os.get_terminal_size().columns
    for i in range(0, len(ascii_data), width):
        # Fail Safe
        if time.time() - start_time > duration:
            break
        line = ''.join(ascii_data[i : i + width])
        print(line.center(terminal_width))
        time.sleep(delay)

def bg_music(duration, music_file):
    try: 
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        time.sleep(duration)
        pygame.mixer.stop()
    except Exception as e:
        print(f"Error detected : {e}")

if __name__ == "__main__":
    try: 
        img_path = r''  # Enter the path of your image file  (in between '')
        width = 180  # Enter the width of the output image (in integer) 
        duration = 30 # Set duration to play music
        music_file = r'' # Enter the path of your image file (in between '')
    except Exception as e:
        print(f"Error Find : {e}")

    image_thread = threading.Thread(target = img_to_ascii_img, args = (img_path, width, duration))
    music_thread = threading.Thread(target = bg_music, args = (duration, music_file))

    image_thread.start()
    music_thread.start()

    image_thread.join()
    music_thread.join()
