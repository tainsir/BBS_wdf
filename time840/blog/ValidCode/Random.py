import random


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )


def random_word(length):
    word=''
    for i in range(length):
        x = str(random.randint(0, 9))
        y = chr(random.randint(65, 90))
        z = chr(random.randint(97, 122))
        word += random.choice([x,y,z])
    return word


def random_point(draw,width,height):
    for i in range(50):
        draw.point([random.randint(0, width), random.randint(0, height)],fill=random_color())


def random_line(draw,width,height):
    for i in range(8):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2),fill=random_color())


def random_arc(draw,width,height):
    for i in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())