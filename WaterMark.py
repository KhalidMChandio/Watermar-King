import cv2

class WaterMark():
    def __init__(self, width:int=0, height:int=0, text_to_write:str="watermark"):
        self.image_width = width
        self.image_height = height
        self.text_to_write = text_to_write
        self.font = cv2.FONT_HERSHEY_TRIPLEX
        # initialize
        self.textX = 0
        self.font_size = 1.1
        self.thickness = 4

        # determine font size and thickness
        if (self.image_width >= 5000):
            self.font_size = 10.1
            self.thickness = 30
        elif (self.image_width >= 4000 and self.image_width < 5000):
            self.font_size = 8.1
            self.thickness = 25
        elif (self.image_width >= 3000 and self.image_width < 4000):
            self.font_size = 6.1
            self.thickness = 18
        elif (self.image_width >= 2000 and self.image_width < 3000):
            self.font_size = 4.1
            self.thickness = 11
        elif (self.image_width >= 1000 and self.image_width < 2000):
            self.font_size = 2.1
            self.thickness = 5
        else:
            self.font_size = 1.1
            self.thickness = 2
        
        # get size of text
        textsize = cv2.getTextSize(text = text_to_write, fontFace = self.font, fontScale = self.font_size, thickness = self.thickness)[0]
        # adjust text size if it is too big
        while textsize[0] > self.image_width:
            self.font_size -= 0.1
            textsize = cv2.getTextSize(text = text_to_write, fontFace = self.font, fontScale = self.font_size, thickness = self.thickness)[0]
        
        # set X position of the text
        self.textX = (self.image_width - textsize[0]) // 2
        