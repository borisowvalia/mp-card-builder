from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os

class Title():
    def __init__(self, text, fontsize, fontpath, color='black'):
        self.text = text
        self.fontsize = fontsize
        self.fontpath = fontpath
        self.color = color
        self.font = ImageFont.truetype(font=self.fontpath, size=self.fontsize)
        self.size = tuple(self.font.getsize(self.text))

    @property
    def image(self):
        img = Image.new('RGBA', self.size, (255, 0, 0, 0))
        draw = ImageDraw.Draw(img) 
        draw.text(xy=(0,0), text=self.text, font=self.font, fill=self.color)

        return img
    

class TemplateInfoWithName():
    def __init__(self, name: Title, info: Title, size: dict, padding: dict, bg_color, radius):
        self.name = name
        self.info = info
        self.size = size
        self.padding = padding
        self.bg_color = bg_color
        self.radius = radius
    
    @property
    def optimize_size(self):
        # block w/h between min and max
        block_width = min(self.size['width'][1], \
                          max(self.size['width'][0], self.padding['left'] + self.padding['right'] \
                              + max(self.name.size[0], self.info.size[0])))
        
        block_height = min(self.size['height'][1], \
                           max(self.size['height'][0], self.name.size[1] + self.info.size[1] \
                                        + self.padding['top'] + self.padding['buttom'] + self.padding['blocks']))
        
        return (block_width, block_height)
    
    def get_image(self):
        #create transperent img
        block_size = self.optimize_size
        img = Image.new('RGBA', block_size, (255, 0, 0, 0))
        draw = ImageDraw.Draw(img) 
        draw.rounded_rectangle(((0, 0), block_size), radius=self.radius, fill=self.bg_color)

        #draw title text
        name_xy = ((block_size[0] - self.name.size[0])/2, self.padding['top'])
        draw.text(name_xy, self.name.text, font=self.name.font, fill=self.name.color)
        # #draw description text
        info_xy = ((block_size[0] - self.info.size[0])/2, self.padding['top'] + self.name.size[1] + self.padding['blocks'])
        draw.text(info_xy, self.info.text, font=self.info.font, fill=self.info.color)

        return img


class TemplateName():
    def __init__(self, name: Title, size: dict, padding: dict, bg_color, radius):
        self.name = name
        self.size = size
        self.padding = padding
        self.bg_color = bg_color
        self.radius = radius

    @property
    def correct_name(self):
        fontsize=8
        new_font = Title(text=self.name.text, fontpath=self.name.fontpath, fontsize=fontsize, color=self.name.color)

        while new_font.size[0] < self.size['width'][1]:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            new_font = Title(text=self.name.text, fontpath=self.name.fontpath, fontsize=fontsize, color=self.name.color)
            if fontsize == self.name.fontsize:
                break
        
        return new_font
    
    @property
    def optimize_size(self):
        # block w/h between min and max
        block_width = min(self.size['width'][1],\
                          max(self.size['width'][0], self.padding['left'] + self.padding['right'] + self.correct_name.size[0]))
        block_height = min(self.size['height'][1],\
                           max(self.size['height'][0], self.correct_name.size[1] + self.padding['top'] + self.padding['buttom']))
        
        return (block_width, block_height)
    
    
    def get_image(self):
        block_size = self.optimize_size
        img = Image.new('RGBA', block_size, (255, 0, 0, 0))
        draw = ImageDraw.Draw(img) 
        draw.rounded_rectangle(((0, 0), block_size), radius=self.radius, fill=self.bg_color)
        #draw title text
        name_xy = ((block_size[0] - self.correct_name.size[0])/2, self.padding['top'])
        draw.text(name_xy, self.correct_name.text, font=self.correct_name.font, fill=self.correct_name.color)

        return img


class TemplateCartV1():
    def __init__(self,
                 title_blocks, title_blocks_config,
                 info_blocks, info_blocks_config,
                 product=None):
        
        self.product = product
        self.title_blocks = title_blocks
        self.title_blocks_config = title_blocks_config
        self.info_blocks = info_blocks
        self.info_blocks_config = info_blocks_config
    
    def group_blocks(self, blocks, config):

        width_blocks = list(map(lambda x: x.optimize_size[0], blocks))
        height_blocks = list(map(lambda x: x.optimize_size[1], blocks))

        #w/h of group blocks
        if config.get('vector') == 'vertical':
            group_block_width = max(width_blocks)
            group_block_height = sum(height_blocks) + config.get('margin').get('blocks') * (len(blocks) - 1)
        elif config.get('vector') == 'horizontal':
            group_block_height = max(height_blocks)
            group_block_width = sum(width_blocks) + config.get('margin').get('blocks') * (len(blocks) - 1)
        
        #Create transparent bg
        img = Image.new('RGBA', (group_block_width, group_block_height), (255, 0, 0, 0))
        
        #configure blocks to group
        x, y, = 0, 0
        for block in blocks:
            block_image = block.get_image()
            block_size = block.optimize_size

            if (config.get('align') == 'left') & (config.get('vector') == 'vertical'):
                img.paste(block, (x, y), block)
                y += block_size[1] + config.get('margin').get('blocks')

            elif (config.get('align') == 'right') & (config.get('vector') == 'vertical'):
                img.paste(block_image, (group_block_width - block_size[0], y), block_image)
                y += block_size[1] + config.get('margin').get('blocks')

            elif (config.get('align') == 'center') & (config.get('vector') == 'vertical'):
                img.paste(block_image, (int((group_block_width - block_size[0])/2), y), block_image)
                y += block_size[1] + config.get('margin').get('blocks')

            elif (config.get('align') == 'up') & (config.get('vector') == 'horizontal'):
                img.paste(block_image, (x, y), block_image)
                x += block_size[0] + config.get('margin').get('blocks')
            
            elif (config.get('align') == 'down') & (config.get('vector') == 'horizontal'):
                img.paste(block_image, (x, group_block_height - block_size[1]), block_image)
                x += block_size[0] + config.get('margin').get('blocks')

            elif (config.get('align') == 'center') & (config.get('vector') == 'horizontal'):
                img.paste(block_image, (x, int((group_block_height - block_size[1])/2)), block_image)
                x += block_size[0] + config.get('margin').get('blocks')

        return img
    

def test():
    fontpath = os.path.join(os.path.dirname(__file__), 'static/font/HelveticaBold.ttf')
    
    name = Title(text='Название', fontsize=15, fontpath=fontpath, color='black')
    info = Title(text='Текс', fontsize=27, fontpath=fontpath, color='black')
    title = Title(text='НАЗВАНИЕ', fontsize=90, fontpath=fontpath, color='black')

    size_info = {
        'width': (200, 1000),
        'height': (100, 1000)
        }
    padding = {
        "top": 20,
        "buttom": 50,
        "left": 20,
        "right": 20,
        "blocks": 20
        }
    bg_color = '#fdeef9'

    size_title = {
        'width': (200, 1000),
        'height': (100, 1000)
        }
    padding_title = {
        "top": 0,
        "buttom": 0,
        "left": 0,
        "right": 0,
        "blocks": 0
        }
    bg_color_title = '#00000000'

    info_config = {
        'margin': {
            'blocks': 24
        },
        'vector': 'vertical',
        'align': 'right'
    }
    title_config = {
        'margin': {
            'blocks': 24
        },
        'vector': 'vertical',
        'align': 'right'
    }

    card_info = TemplateInfoWithName(name=name, info=info, size=size_info, padding=padding, radius=43, bg_color=bg_color)
    card_title = TemplateName(name=title, size=size_title, padding=padding_title, radius=0, bg_color=bg_color_title)
    card = TemplateCartV1(info_blocks=[card_info], info_blocks_config=info_config,
                          title_blocks=[card_title], title_blocks_config=title_config)
    
    card.group_blocks(blocks=[card_info, card_info, card_title], config=info_config).show()

test()

