import os

from PIL import Image, ImageDraw, ImageFont

import db_logic

STAR_SIZE = 32
STAR_MARGIN = 12

fontsFolder = '/usr/share/fonts/truetype/lato/'

font_current_count = 'Lato-Regular.ttf'
font_scores = 'Lato-Bold.ttf'

star_x = STAR_MARGIN
star_middle_y = int(200 / 2 - STAR_SIZE / 2)
star_left_y = int(star_middle_y - STAR_MARGIN - STAR_SIZE)
star_right_y = int(star_middle_y + STAR_SIZE + STAR_MARGIN)

star_outline = Image.open("star_thick_outline_512-32.png")
star_filled = Image.open("star_filled_512-32.png")


def create_img():
    row = db_logic.get_last_row()
    total = db_logic.count_total_days()
    img = Image.new('1', (200, 200), 'white')
    fill_stars(img, row.next_star)
    add_current_count(img, row.current_streak)
    add_score(img, row.max_streak, total)
    img.save("output.bmp")


def add_current_count(img, count):
    count = str(count)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join(fontsFolder, font_current_count), 64)
    width, height = font.getsize(count)
    y_pos = int(200 / 2 - width / 2)
    draw.text((y_pos, 50), count, fill = 'black', font = font)


def add_score(img, high_score, total):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join(fontsFolder, font_scores), 16)
    draw.text((125, 140), 'High', fill = 'black', font = font)
    draw.text((170, 140), str(high_score), fill = 'black', font = font)
    draw.text((125, 165), 'Total', fill = 'black', font = font)
    draw.text((170, 165), str(total), fill = 'black', font = font)


#############################
# Stars until next "Joker"
#############################
def fill_stars(img, count):
    if count == 0:
        zero_filled_stars(img)
    elif count == 1:
        one_filled_stars(img)
    elif count == 2:
        two_filled_stars(img)
    elif count == 3:
        three_filled_stars(img)
    else:
        raise ValueError('The star count seems to be incorrect.')


def zero_filled_stars(img):
    img.paste(star_outline, (star_left_y, star_x))
    img.paste(star_outline, (star_middle_y, star_x))
    img.paste(star_outline, (star_right_y, star_x))


def one_filled_stars(img):
    img.paste(star_filled, (star_left_y, star_x))
    img.paste(star_outline, (star_middle_y, star_x))
    img.paste(star_outline, (star_right_y, star_x))


def two_filled_stars(img):
    img.paste(star_filled, (star_left_y, star_x))
    img.paste(star_filled, (star_middle_y, star_x))
    img.paste(star_outline, (star_right_y, star_x))


def three_filled_stars(img):
    img.paste(star_filled, (star_left_y, star_x))
    img.paste(star_filled, (star_middle_y, star_x))
    img.paste(star_filled, (star_right_y, star_x))


if __name__ == "__main__":
    create_img()
