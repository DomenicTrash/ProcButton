import Image

import create_image
import epd1in54


def clear_display():
    epd = epd1in54.EPD()
    epd.init(epd.lut_full_update)
    image = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)  # 255: clear the frame
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()


def display_image():
    epd = epd1in54.EPD()
    epd.init(epd.lut_partial_update)
    image = Image.open('output.bmp')
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()


def create_and_display_image():
    print("image start")
    create_image.create_img()
    print("image created")
    display_image()


if __name__ == '__main__':
    display_image()
    # clear_display()
