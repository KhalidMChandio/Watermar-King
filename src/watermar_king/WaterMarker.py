# Module to watermark images, PDFs, Videos and Audios
# Author: Khalid M. Chandio.

import cv2, numpy as np             #Used to create and merge watermark
from io import BytesIO              #Used to handle all operations in memory as BytesIO
import tempfile                     #Used to save temp files
import pypdfium2 as pdfium          #Used to extract pages from pdf files as images
from moviepy import editor as mpE   #Used to edit videos. This requires ImageMagick to be installed and path included in env variables.
import pyttsx3                      #Used to create computer generated voice for watermarking audios
from pydub import AudioSegment      #Used to overlay audio files

class _waterMark():
    """
    Class to watermark images, PDFs, videos and audios.
    """
    def __init__(self, width:int=0, height:int=0, text_to_write:str="watermark"):
        """
        Initializes the WaterMark object with the given dimensions and text.

        :param width: The width of the image where watermark will be applied.
        :param height: The height of the image where watermark will be applied.
        :param text_to_write: The text to be used as the watermark.

        This constructor sets the default font, calculates the appropriate font size and thickness
        based on the image width, and determines the position for centering the watermark text.
        """

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
        


class WaterMarker():
    """ 
    Class to watermark images, PDFs, videos and audios 
    
    """
        
    def _getBlankWaterMarkImage(self,img, text_to_write: str="Watermark this image"):
        
        """
        :Private Function:

        Creates a blank image with watermark text placed at specified intervals.

        This function generates a blank image of the same size as the input image, with the given
        text written as a watermark across multiple lines at specified vertical positions.

        :param img: The input image from which dimensions are derived for the blank watermark image.
        :param text_to_write: The watermark text to be placed on the blank image. Default is "Watermark this image".
        :return: A blank image with the watermark text applied, with colors inverted for visibility.

        """
        #Get size of image
        img_width, img_height = img.shape[1], img.shape[0]
        
        wm=_waterMark(img_width, img_height, text_to_write)
        
        
        #Create blank image with all zeros. Width is doubled for rotations
        blank = np.zeros(shape=img.shape, dtype=np.uint8)
        
        #First line
        num= int(img_height * 25/100)
        
        text_location=(wm.textX, num)
        cv2.putText(blank, text=text_to_write, org = text_location, fontFace = wm.font, fontScale = wm.font_size, color=(200, 200, 200), thickness=wm.thickness, lineType=cv2.LINE_8)
        
        #Second line
        num= int(img_height * 50/100)
        text_location=(wm.textX, num)
        cv2.putText(blank, text=text_to_write, org = text_location, fontFace = wm.font, fontScale = wm.font_size, color=(200, 200, 200), thickness=wm.thickness, lineType=cv2.LINE_8)
        
        #Third line
        num= int(img_height * 75/100)
        text_location=(wm.textX, num)
        cv2.putText(blank, text=text_to_write, org = text_location, fontFace = wm.font, fontScale = wm.font_size, color=(200, 200, 200), thickness=wm.thickness, lineType=cv2.LINE_8)

        #Rotate and merge image - NOT IN USE
        #angle=0
        #M=cv2.getRotationMatrix2D(text_location,angle,1)
        #out=cv2.warpAffine(blank,M,(img_width, img_height))
        
        # Convert 0s to 1s and 1s to 0s to invert colors black and white for readability
        out=cv2.bitwise_not(blank)
        return out
   
    # Converts PNG image to watermarked image and returns Watermarked image
    def WaterMark_PNG(self, img: bytes, text_to_write: str) -> BytesIO:
        
        """
        Functions returns watermarked image with blend.
        
        :param img: bytes of image object which needs to be watermarked.
        
        ::

            img = cur.execute(qryArch, param).fetchval()
        
        :param text_to_write: Text to be used as watermark  
        
        :param extension: The extension of the img format which can be JPG, JPEG or PNG
        
        """
        nparr = np.fromstring(img, np.uint8)
        given_image=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imgWM = self._getBlankWaterMarkImage(given_image, text_to_write)
        
        blend = cv2.addWeighted(src1=given_image, alpha=0.7, src2=imgWM, beta=0.3,gamma=0.5)
        
        is_success, buffer = cv2.imencode(".png", blend)
        
        if is_success:
            decode_image=BytesIO(buffer)
            return decode_image
        else:
            return img
    
    # Converts TIFF image to watermarked image and returns Watermarked image
    def WaterMark_TIFF(self, img: bytes, text_to_write: str) -> BytesIO:
        '''
        Functions returns watermarked image with blend.
        
        :param img: bytes of image object which needs to be watermarked.
        
        ::

            img = cur.execute(qryArch, param).fetchval()
        
        :param text_to_write: Text to be used as watermark  
        
        :param extension: The extension of the img format which can be JPG, JPEG or PNG
        
        '''
        nparr = np.fromstring(img, np.uint8)
        given_image=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imgWM = self._getBlankWaterMarkImage(given_image, text_to_write)
        
        blend = cv2.addWeighted(src1=given_image, alpha=0.7, src2=imgWM, beta=0.3,gamma=0.5)
        
        is_success, buffer = cv2.imencode(".tiff", blend)
        
        if is_success:
            decode_image=BytesIO(buffer)
            return decode_image
        else:
            return img
    
    # Converts JPG image to watermarked image and returns Watermarked image
    def WaterMark_JPEG(self, img: bytes, text_to_write: str) -> BytesIO:
        '''
        Functions returns watermarked image with blend.
        
        :param img: bytes of image object which needs to be watermarked.
        
        ::

            img = cur.execute(qryArch, param).fetchval()
        
        :param text_to_write: Text to be used as watermark  
        
        :param extension: The extension of the img format which can be JPG, JPEG or PNG
        
        '''
        nparr = np.fromstring(img, np.uint8)
        given_image=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imgWM = self._getBlankWaterMarkImage(given_image, text_to_write)
        
        blend = cv2.addWeighted(src1=given_image, alpha=0.7, src2=imgWM, beta=0.3,gamma=0.5)
        
        is_success, buffer = cv2.imencode(".jpg", blend)
        
        if is_success:
            decode_image=BytesIO(buffer)
            return decode_image
        else:
            return img

        # IN USE
    
    # Converts BMP image to watermarked image and returns Watermarked image
    def WaterMark_BMP(self, img: bytes, text_to_write: str) -> BytesIO:
        '''
        Functions returns watermarked image with blend.
        
        :param img: bytes of image object which needs to be watermarked.
        
        ::

            img = cur.execute(qryArch, param).fetchval()
        
        :param text_to_write: Text to be used as watermark  
        
        :param extension: The extension of the img format which can be JPG, JPEG or PNG
        
        '''
        nparr = np.fromstring(img, np.uint8)
        given_image=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imgWM = self._getBlankWaterMarkImage(given_image, text_to_write)
        
        blend = cv2.addWeighted(src1=given_image, alpha=0.7, src2=imgWM, beta=0.3,gamma=0.5)
        
        is_success, buffer = cv2.imencode(".bmp", blend)
        
        if is_success:
            decode_image=BytesIO(buffer)
            return decode_image
        else:
            return img
    
    #Uses Moviepy to generate watermarked Video
    def WaterMark_Video(self, video: bytes, text_to_write: str="WaterMark", extension: str="mp4") -> BytesIO:
        '''
        Functions returns watermarked video.
        
        :param video: Retrieved bytes data of a video file.
        
        :param text_to_write: Text to be used as watermark.

        :param extension: The extension to determine the video file format. These can be mp4, avi, ogv, webm.
        
        '''
        
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(video)
            
            vid = mpE.VideoFileClip(fp.name)
            width, height = vid.size
            dur = vid.duration
            #logo = TextClip(txt=text_to_write,size=(width,height),bg_color='transparent')
            
            txtClip = (mpE.TextClip(text_to_write, fontsize=15,
                font="Century-Schoolbook-Roman", color="gray")
                .margin(top=int((height/2)-15), opacity=0)
                .set_position(("center","top")))
            
            final = (mpE.CompositeVideoClip(size=(width,height),clips=[vid, txtClip],bg_color=None,use_bgclip=True)
            .set_duration(dur))
            ext="."+extension
            Kodek = 'libx264'
            if ext == '.mp4':
                Kodek = 'libx264' 
            elif ext == '.avi':
                Kodek = 'rawvideo'
            elif ext == '.ogv':
                Kodek = 'libvorbis'
            elif ext == '.webm':
                Kodek == 'libvpx'
                
            with tempfile.NamedTemporaryFile(delete=True) as f:
                final.write_videofile(f.name + ext, codec=Kodek)
                
                with open (f.name+ext,'rb') as file:
                    cont = file.read()
                    file.close()
            return BytesIO(cont)
    
    # Method using pdfium to return watermarked PDF
    def WaterMark_PDF(self, pdf: bytes, text_to_write: str) -> BytesIO:
        '''
        Functions uses pdfium to create and return watermarked PDF file.
        
        :param pdf: Retrived bytes of pdf file which needs to be watermarked.
        
        :param text_to_write: Text to be used as watermark  

        '''
        # Create an empty array for holding the pages data read from given PDF file.
        ImgList=[]
        pd = pdfium.PdfDocument(BytesIO(pdf))
        # read all pages from pdf, convert to bitmap PIL images and save into a list
        for page in pd:
            # get pages - currently scale is 2 for increased quality of images
            img = page.render(scale=2)
            # append read image to list
            ImgList.append(img.to_pil())
        
        # Generate a new empty pdf        
        pdNew = pdfium.PdfDocument.new()
        # convert all images in the list to watermakred jpg images and insert into new PDF
        for img in ImgList: # img is in PIL Bitmap image
            # setting initial value to page as A4, will be changed later
            width, height = (595, 842) #Set width & height to A4
            # convert PIL image to RGB
            img = img.convert('RGB')
            # create BytesIO to save PIL img to bytes
            img_byte_arr = BytesIO()
            # save img to BytesIO
            img.save(img_byte_arr,format="JPEG",quality=80, optimize=True, progressive=True)
            # read the saved image back to BytesIO
            bio=BytesIO()
            bio = img_byte_arr.getvalue()
            # send image for watermarking
            wmImage = self.WaterMark_JPEG(img=bio,text_to_write=text_to_write)
            # now wmImage has our watermarked image
            # create new pdfBitmap image to be included in pdNew
            image = pdfium.PdfImage.new(pdNew)
            # load watermakred image into pdfBitmap
            image.load_jpeg((wmImage))
            # get size of img to get matrix for setting size of pdfBitmap
            width,height = img.size
            matrix = pdfium.PdfMatrix().scale(width, height)
            # set image matrix
            image.set_matrix(matrix)
            # create new empty page of width height
            page = pdNew.new_page(width, height)
            #write image into page
            page.insert_obj(image)
            # generate page
            page.gen_content()
        
        # now all images inserted and pdf is ready to be saved
        # Save new pdf to memory and return 
        ret = BytesIO()
        pdNew.save(ret)
        return BytesIO(ret.getvalue())

    # This function uses pydub and ffmpeg. install ffmpeg and set environment variable to its bin folder
    def WaterMark_WAV(self, audio: bytes, text_to_write: str) -> BytesIO:
        """
        Creates a wav file with text to speech, overlays it with original audio and returns overlayed file

        :param audio: Retrived bytes of audio file as retrieved from read() function from database.
        
        :param text_to_write: The text required to be spoken by bot and watermarked in audio file.
        
        """
        # Create wave audio clip for overlaying
        
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-100)
        voices = engine.getProperty('voices') 
        # Uncomment the following lines to see all the available voices
        #for voice in voices: 
        #    print(f'voice: {voice.name}')
        
        # This function depends on the voices installed in the system and requires index of the installed voices; which may vary.
        engine.setProperty('voice', voices[28].id)
        # Save created clip as tempory file and load into audWM
        with tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="Arch_") as wm:
            engine.save_to_file(text=text_to_write, filename=wm.name+".wav")
            
            engine.runAndWait()
            audWM = AudioSegment.from_wav(wm.name+".wav")
            
            # audio is a raw data so save it to temporary file, as pydub accepts file from disk only.
            with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_") as org:
                org.write(audio)
                # load file to audOrigin; the original file
                audOrigin = AudioSegment.from_file(file=org.name, format= "wav")
                
                # overlay both clips
                clip: AudioSegment = audOrigin.overlay(audWM,loop=1)
                
                # save the newly created clip to temporary file for opening and exporting
                with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_", suffix="."+"wav") as f:
                    clip.export(f.name,format="wav")
                    # open saved file and return buffer as BytesIO
                    with open(f.name,"rb") as retFile:
                        buffer = retFile.read()
                        return BytesIO(buffer)

    def WaterMark_OGG(self, audio: bytes, text_to_write: str) -> BytesIO:
        """
        Creates a wav file with text to speech, overlays it with original audio and returns overlayed file

        :param audio: Retrived bytes of audio file as retrieved from read() function from database.
        
        :param text_to_write: The text required to be spoken by bot and watermarked in audio file.
        
        """
        # Create wave audio clip for overlaying
        
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-100)
        voices = engine.getProperty('voices') 
        # Uncomment the following lines to see all the available voices
        #for voice in voices: 
        #    print(f'voice: {voice.name}')
        
        # This function depends on the voices installed in the system and requires index of the installed voices; which may vary.
        engine.setProperty('voice', voices[28].id)
        # Save created clip as tempory file and load into audWM
        with tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="Arch_") as wm:
            engine.save_to_file(text=text_to_write, filename=wm.name+".wav")
            
            engine.runAndWait()
            audWM = AudioSegment.from_wav(wm.name+".wav")
            
            # audio is a raw data so save it to temporary file, as pydub accepts file from disk only.
            with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_") as org:
                org.write(audio)
                # load file to audOrigin; the original file
                audOrigin = AudioSegment.from_ogg(file=org.name)
                
                # overlay both clips
                clip: AudioSegment = audOrigin.overlay(audWM,loop=1)
                
                # save the newly created clip to temporary file for opening and exporting
                with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_", suffix="."+"ogg") as f:
                    clip.export(f.name,format="ogg")
                    # open saved file and return buffer as BytesIO
                    with open(f.name,"rb") as retFile:
                        buffer = retFile.read()
                        return BytesIO(buffer)

    # This function uses pydub and ffmpeg. install ffmpeg and set environment variable to its bin folder
    def WaterMark_MP3(self, audio: bytes, text_to_write: str) -> BytesIO:
        '''
        Function creates a wav file with text to speech, overlays it with original audio and returns overlayed file

        :param audio: Retrived bytes of audio file as retrieved from read() function from database.
        
        :param text_to_write: The text required to be spoken by bot and watermarked in audio file.
        
        '''
        # Create wave audio clip for overlaying
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-100)
        voices = engine.getProperty('voices')
        #for voice in voices:
        #    print(f'voice: {voice.name}')
        
        # This function depends on the voices installed in the system and requires index of the installed voices; which may vary.
        engine.setProperty('voice', voices[28].id)
        # Save created clip as tempory file and load into audWM
        with tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="Arch_") as wm:
            engine.save_to_file(text=text_to_write, filename=wm.name+".mp3")
            
            engine.runAndWait()
            audWM = AudioSegment.from_mp3(wm.name+".mp3")
            # audio is a raw data so save it to temporary file, as pydub accepts file from disk only.
            with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_") as org:
                org.write(audio)
                # load file to audOrigin; the original file
                try:
                    audOrigin = AudioSegment.from_file(file=org.name, format= "mp3")
                except:
                    audOrigin = AudioSegment.from_file(file=org.name, format= "mp3")
                # overlay both clips
                clip: AudioSegment = audOrigin.overlay(audWM)
                
                # save the newly created clip to temporary file for opening and exporting
                with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_", suffix="."+"mp3") as f:
                    clip.export(f.name,format="mp3")
                    # open saved file and return buffer as BytesIO
                    with open(f.name,"rb") as retFile:
                        buffer = retFile.read()
                        return BytesIO(buffer)
            
