from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os


class TemplateCartV1():
    def __init__(self, product,
                 title_blocks, title_blocks_config,
                 info_blocks, info_blocks_config):
        
        self.product = product
        self.title_blocks = title_blocks
        self.title_blocks_config = title_blocks_config
        self.info_blocks = info_blocks
        self.info_blocks_config = info_blocks_config
    
    def group_blocks(self, block_type='info'):

        if block_type == 'info':
            blocks = self.info_blocks
            config = self.info_blocks_config
        elif block_type == 'title':
            blocks = self.title_blocks
            config = self.title_blocks_config

        width_blocks = list(map(lambda x: x.size[0], blocks))
        height_blocks = list(map(lambda x: x.size[1], blocks))

        #w/h of group blocks
        if config.get('vector') == "vertical":
            group_block_width = max(width_blocks)
            group_block_height = sum(height_blocks) + config.get('margin').get('blocks') * (len(blocks) - 1)
        elif config.get('vector') == "horizontal":
            group_block_height = max(height_blocks)
            group_block_width = sum(width_blocks) + config.get('margin').get('blocks') * (len(blocks) - 1)
        
        #Create transparent bg
        img = Image.new('RGBA', (group_block_width, group_block_height), (255, 0, 0, 0))
        
        #configure blocks to group
        x, y, = 0, 0
        for block in blocks:
            if (config.get('align') == 'left') & (config.get('vector') == 'vertical'):
                img.paste(block, (x, y), block)
                y += block.size[1] + config.get('margin').get('blocks')

            elif (config.get('align') == 'right') & (config.get('vector') == 'vertical'):
                img.paste(block, (group_block_width - block.size[0], y), block)
                y += block.size[1] + config.get('margin').get('blocks')

            elif (config.get('align') == 'center') & (config.get('vector') == 'vertical'):
                img.paste(block, (int((group_block_width - block.size[0])/2), y), block)
                y += block.size[1] + config.get('margin').get('blocks')

            elif (config.get('align') == 'up') & (config.get('vector') == 'horizontal'):
                img.paste(block, (x, y), block)
                x += block.size[0] + config.get('margin').get('blocks')
            
            elif (config.get('align') == 'down') & (config.get('vector') == 'horizontal'):
                img.paste(block, (x, group_block_height - block.size[1]), block)
                x += block.size[0] + config.get('margin').get('blocks')

            elif (config.get('align') == 'center') & (config.get('vector') == 'horizontal'):
                img.paste(block, (x, int((group_block_height - block.size[1])/2)), block)
                x += block.size[0] + config.get('margin').get('blocks')

        return img

    def get_image():
        pass