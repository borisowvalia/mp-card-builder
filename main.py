#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import mkdir
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import requests
import pandas as pd
import os
import functools


def get_correct_font_size(text, fontstyle, max_width, max_fontsize):
    # portion of image width you want text width to be
    fontsize=8

    font = ImageFont.truetype(fontstyle)
    while font.getsize(text)[0] < max_width:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(fontstyle, fontsize)
        if fontsize == max_fontsize:
            break
    
    return font

def group_blocks(blocks, margin={"blocks": 24}, vector="vertical", align="left"):

    width_blocks = list(map(lambda x: x.size[0], blocks))
    height_blocks = list(map(lambda x: x.size[1], blocks))

    if vector == "vertical":
        group_block_width = max(width_blocks)
        group_block_height = sum(height_blocks) + margin["blocks"] * (len(blocks) - 1)
    elif vector == "horizontal":
        group_block_height = max(height_blocks)
        group_block_width = sum(width_blocks) + margin["blocks"] * (len(blocks) - 1)

    img = Image.new('RGBA', (group_block_width, group_block_height), (255, 0, 0, 0))

    x, y, = 0, 0
    for block in blocks:

        if (align == "left") & (vector == "vertical"):
            img.paste(block, (x, y), block)
            y += block.size[1] + margin["blocks"]

        elif (align == "right") & (vector == "vertical"):
            img.paste(block, (group_block_width - block.size[0], y), block)
            y += block.size[1] + margin["blocks"]

        elif (align == "center") & (vector == "vertical"):
            img.paste(block, (int((group_block_width - block.size[0])/2), y), block)
            y += block.size[1] + margin["blocks"]

        elif (align == "up") & (vector == "horizontal"):
            img.paste(block, (x, y), block)
            x += block.size[0] + margin["blocks"]
        
        elif (align == "down") & (vector == "horizontal"):
            img.paste(block, (x, group_block_height - block.size[1]), block)
            x += block.size[0] + margin["blocks"]

        elif (align == "center") & (vector == "horizontal"):
            img.paste(block, (x, int((group_block_height - block.size[1])/2)), block)
            x += block.size[0] + margin["blocks"]

    return img


def create_v1_template(title=('клинок, см', 32, 'HelveticaBold.ttf', 'black'),
                                      description=('15,6', 64, 'HelveticaBold.ttf', 'black'),
                                      background_color='#fdeef9',
                                      width=(200, 1000), height = (100, 1000),
                                      padding={
                                        "top": 20,
                                        "buttom": 50,
                                        "left": 20,
                                        "right": 20,
                                        "blocks": 20
                                      },
                                      radius=43):

    font_title = ImageFont.truetype(title[2], title[1])
    font_description = ImageFont.truetype(description[2], description[1])

    title_width, title_height = font_title.getsize(title[0])
    description_width, description_height = font_description.getsize(description[0])
    
    # block w/h between min and max
    block_width = min(width[1], max(width[0], padding["left"] + padding["right"] + max(title_width, description_width)))
    block_height = min(height[1], max(height[0], title_height + description_height \
    + padding["top"] + padding["buttom"] + padding["blocks"]))

    #create tranperent img
    img = Image.new('RGBA', (block_width, block_height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img) 

    draw.rounded_rectangle(((0, 0), (block_width, block_height)), radius=radius, fill=background_color)

    #draw title text
    draw.text(((block_width - title_width)/2, padding["top"]), title[0], font=font_title, fill=title[3])
    # #draw description text
    draw.text(((block_width - description_width)/2, padding["top"] + title_height + padding["blocks"]), description[0], font=font_description, fill=description[3])

    return img




def create_v2_template(title=('NAME', 32, 'HelveticaBold.ttf', 'black'),  background_color='#00000000',
                                      width=(0, 450), height = (0, 200),
                                      padding={
                                        "top": 0,
                                        "buttom": 0,
                                        "left": 0,
                                        "right": 0,
                                        "blocks": 0
                                      },
                                      radius=0):

    font = get_correct_font_size(title[0], fontstyle=title[2], max_width=width[1], max_fontsize=title[1])
    title_width, title_height = font.getsize(title[0])

    # block w/h between min and max
    block_width = min(width[1], max(width[0], padding["left"] + padding["right"] + title_width))
    block_height = min(height[1], max(height[0], title_height + padding["top"] + padding["buttom"]))

    img = Image.new('RGBA', (block_width, block_height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img) 
    draw.rounded_rectangle(((0, 0), (block_width, block_height)), radius=radius, fill=background_color)
    #draw title text
    draw.text(((block_width - title_width)/2, padding["top"]), title[0], font=font, fill=title[3])

    return img


def create_v1_final_template(background, block, margin):

    x = 0
    y = 0

    if ("left" in margin) & ("right" in margin):
        if (margin["left"] == margin["right"]):
            x = int((background.size[0] - block.size[0]) / 2)
    elif "left" in margin:
        x = margin["left"]
    elif "right" in margin:
        x = background.size[0] - (margin["right"] + block.size[0])

    if ("top" in margin) & ("buttom" in margin):
        if (margin["top"] == margin["buttom"]):
            y = int((background.size[1] - block.size[1]) / 2)
    elif "top" in margin:
        y = margin["top"]
    elif "buttom" in margin:
        y = background.size[1] - (margin["buttom"] +  block.size[1])
    background.paste(block, (x, y), block)

    return background

def prop_resize_img(img, height=False, width=False):

    if height:
        width = (height / img.size[1]) * img.size[0]
    elif width:
        height = (width / img.size[0]) * img.size[1]
    else:
        width, height = img.size

    return img.resize((int(width), int(height)))


def create_backgroud(type='wb', color='#000000'):

    if type == 'wb':
        width, height = 1200, 1200

    background = Image.new('RGBA', (width, height), color=color)

    return background


def get_image(url, path):

    r = requests.get(url, allow_redirects=True)
    open(path, 'wb').write(r.content)

    return Image.open(path).convert('RGBA')




def figma():
    import json
    headers = {'X-FIGMA-TOKEN': ''}
    filekey = 'g4deIvp8xEiI0fkDSfumBz'
    url = f'https://api.figma.com/v1/files/{filekey}/nodes?ids=0%3A1'


    r = requests.get(url, headers=headers).json()
    with open('figma.json', 'w') as f:
        json.dump(r, f, indent=4)



def test():

    img = Image.open('new.png').convert("RGBA")
    hit = prop_resize_img(img = Image.open('static/img/hit.png').convert("RGBA"), width=300)

    block1 = create_v1_template(title=('длина', 32, 'static/font/HelveticaBold.ttf', '#8e8e8e'),
                                      description=('15,6', 64, 'static/font/HelveticaBold.ttf', '#cb11ab'),
                                      background_color='#fdeef9',
                                      width=(200, 1000), height = (100, 1000),
                                      padding={
                                        "top": 24,
                                        "buttom": 48,
                                        "left": 24,
                                        "right": 24,
                                        "blocks": 12
                                      },
                                      radius=43)
    block2 = create_v1_template(title=('сталь', 32, 'static/font/HelveticaBold.ttf', '#8e8e8e'),
                                      description=('jnrljgnljrng', 64, 'static/font/HelveticaBold.ttf', '#cb11ab'),
                                      background_color='#fdeef9',
                                      width=(200, 1000), height = (100, 1000),
                                      padding={
                                        "top": 24,
                                        "buttom": 48,
                                        "left": 24,
                                        "right": 24
                                      },
                                      radius=43)

    title1 = create_v2_template(title=('Victorinox', 90, 'static/font/HelveticaBold.ttf', '#8e8e8e'),
                                      background_color='#00000000',
                                      width=(0, 450), height = (0, 1000),
                                      padding={
                                        "top": 0,
                                        "buttom": 0,
                                        "left": 0,
                                        "right": 0
                                      })
    title2 = create_v2_template(title=('Fjvgvhk', 90, 'static/font/HelveticaBold.ttf', '#8e8e8e'),
                                      background_color='#00000000',
                                      width=(0, 450), height = (0, 1000),
                                      padding={
                                        "top": 0,
                                        "buttom": 0,
                                        "left": 0,
                                        "right": 0
                                      })

    characteristics = group_blocks(blocks=[block1, block2], margin={"blocks": 24}, vector="vertical", align="right")
    naming = group_blocks(blocks=[title1, title2], margin={"blocks": 24}, vector="vertical", align="left")

    img = prop_resize_img(img, height=600)
    background = create_backgroud(color="#FFFFFF")

    img = create_v1_final_template(background, img, margin={"top": 0, "buttom": 0, "right": 0, "left": 0})
    img = create_v1_final_template(img, characteristics, margin={"buttom": 50, "right": 50})
    img = create_v1_final_template(img, naming, margin={"top": 50, "left": 50})
    img = create_v1_final_template(img, hit, margin={"top": 350, "left": 50})

    img.show()


def iter_excel():

    import numpy as np
    data = pd.read_excel('wb_foto_knives.xlsx', engine='openpyxl')
    # data.update(data.select_dtypes(include=np.number).applymap('{:,g}'.format))
    data = data.fillna('').astype(str)

    os.mkdir('output')

    fontpath = 'static/font/gteestiprodisplay_medium.otf'
    fontpath_bold = 'static/font/gteestiprodisplay_bold.otf'

    hit = prop_resize_img(img = Image.open('static/img/dealer.png').convert("RGBA"), width=620)

    for _, row in data.iterrows():

        art_wb = str(row['Артикул WB']).replace('/', '_')
        art = row['Артикул']
        brand = row['Бренд']
        model = row['Модель']
        flag_hit = row['Хит (да/нет)']
        barcode = str(row['ШК'])
        input_path = os.path.join('input', f'{barcode}_1.jpg')

        # print(input_path)

        try:
            img = Image.open(input_path).convert('RGBA')
        except:
            print(f'{barcode}_1.jpg не существует')
            continue

        # Коровий переворачиватель на случай прямоугольной фото
        # if img.size[1] / img.size[0] > 1.2:
        #     img = img.rotate(270, Image.NEAREST, expand = 1)
    
        if True:
            margin_hit = {"left": 60, "top": 130}
            padding_description = {
                                    "top": 40,
                                    "buttom": 24,
                                    "left": 32,
                                    "right": 32,
                                    "blocks": 24
                                }
            margin_description = {"buttom": 40, "right": 40}
            padding_title = {
                            "top": 0,
                            "buttom": 0,
                            "left": 0,
                            "right": 0
                            }
            margin_title = {"top": 260, "left": 60}
            align_characteristics = 'right'
            vector_characteristics = 'vertical'
            vector_title = 'vertical'
            align_title = 'left'
    
        # else:
        #     koef = 0.6
        #     margin_hit = {"left": 50, "top": 320}
        #     padding_description = {
        #                             "top": 24,
        #                             "buttom": 40,
        #                             "left": 24,
        #                             "right": 24,
        #                             "blocks": 10
        #                         }
        #     margin_description = {"buttom": 100, "right": 50}
        #     padding_title = {
        #                     "top": 0,
        #                     "buttom": 0,
        #                     "left": 0,
        #                     "right": 0
        #                     }
        #     margin_title = {"top": 50, "left": 50}
        #     vector_characteristics = 'vertical'
        #     align_characteristics = 'right'
        #     vector_title = 'vertical'
        #     align_title = 'left'

        block1 = create_v1_template(title=(row['название1'], 40, fontpath, '#85929e'),
                                      description=(row['значение1'], 80, fontpath_bold, '#005bff'),
                                      background_color='#e5eefe',
                                      width=(260, 1000), height = (224, 1000),
                                      padding=padding_description,
                                      radius=43)
        block2 = create_v1_template(title=(row['название2'], 40, fontpath, '#85929e'),
                                      description=(row['значение2'], 80, fontpath_bold, '#005bff'),
                                      background_color='#e5eefe',
                                      width=(260, 1000), height = (224, 1000),
                                      padding=padding_description,
                                      radius=43)
        block3 = create_v1_template(title=(row['название3'], 40, fontpath, '#85929e'),
                                      description=(row['значение3'], 80, fontpath_bold, '#005bff'),
                                      background_color='#e5eefe',
                                      width=(260, 1000), height = (224, 1000),
                                      padding=padding_description,
                                      radius=43)

        title1 = create_v2_template(title=(brand, 90, fontpath, '#001a34'),
                                      background_color='#00000000',
                                      width=(0, 800), height = (0, 1000),
                                      padding=padding_title)
        title2 = create_v2_template(title=(model, 80, fontpath, '#85929e'),
                                      background_color='#00000000',
                                      width=(0, 450), height = (0, 1000),
                                      padding=padding_title)
        title3 = create_v2_template(title=(art, 80, fontpath, '#85929e'),
                                      background_color='#00000000',
                                      width=(0, 450), height = (0, 1000),
                                      padding=padding_title)

        
        characteristics = group_blocks(blocks=[block1, block2, block3], margin={"blocks": 24}, vector=vector_characteristics, align=align_characteristics)
        naming = group_blocks(blocks=[title1, title2, title3], margin={"blocks": 18}, vector=vector_title, align=align_title)

        img = prop_resize_img(img=img, height=1100)
        background = create_backgroud(color="#FFFFFF")

        img = create_v1_final_template(background, img, margin={"top": 0, "buttom": 0, "right": 0, "left": 0})
        img = create_v1_final_template(img, characteristics, margin=margin_description)
        img = create_v1_final_template(img, naming, margin=margin_title)

        # if flag_hit == "да":
        #     img = create_v1_final_template(img, hit, margin=margin_hit)
        img = create_v1_final_template(img, hit, margin=margin_hit)

        img.convert('RGB').save(os.path.join('output', f'{barcode}_1.jpg'))
        # img.show()

iter_excel()



