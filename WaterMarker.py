# Module to watermark images, PDFs, Videos and Audios
# Author: Khalid M. Chandio.

import cv2, numpy as np             #Used to create and merge watermark
from io import BytesIO              #Used to handle all operations in memory as BytesIO
import tempfile                     #Used to save temp files
import pypdfium2 as pdfium          #Used to extract pages from pdf files as images
from moviepy import editor as mpE   #Used to edit videos. This requires ImageMagick to be installed and path included in env variables.
import pyttsx3                      #Used to create computer generated voice for watermarking audios
from pydub import AudioSegment      #Used to overlay audio files
import WaterMark


class WaterMarker():
    """ Class to watermark images, PDFs, videos and audios """

    
        
    def _getBlankWaterMarkImage(self,img, text_to_write: str="Watermark this image"):
        """
        Function returns watermarked blank image for further blending.
        
        :param img: CV2 image which needs to be watermarked. This is used to get width & height of the image only.
        
        :param text_to_write: Text to be used as watermark  

        
        """
        
        #Get size of image
        img_width, img_height = img.shape[1], img.shape[0]
        
        wm=WaterMark.WaterMark(img_width, img_height, text_to_write)
        
        
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
        
        # Convert 0s to 1s and 1s to 0s to invert colors black and white
        out=cv2.bitwise_not(blank)
        return out

    
    # Converts image to watermarked image and returns Watermarked image
    def WaterMarkImage(self, img: bytes, text_to_write: str, extension: str="JPG") -> BytesIO:
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
        
        if(extension=='jpg' or extension=='jpeg'):
            is_success, buffer = cv2.imencode(".jpg", blend)
        elif (extension=='png'):
            is_success, buffer = cv2.imencode(".png", blend)
        else:
            is_success = False
            raise ValueError('Extension can only be jpeg, jpg or png.')
        if is_success:
            decode_image=BytesIO(buffer)
            return decode_image
        else:
            return img
    
    
    # Converts image to watermarked image and returns Watermarked image
    def WaterMark_PNG(self, img: bytes, text_to_write: str) -> BytesIO:
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
        
        is_success, buffer = cv2.imencode(".png", blend)
        
        if is_success:
            decode_image=BytesIO(buffer)
            return decode_image
        else:
            return img
        
    
    # Converts image to watermarked image and returns Watermarked image
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
        
    
    # Converts image to watermarked image and returns Watermarked image
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
    
    # Converts image to watermarked image and returns Watermarked image
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
    
    #Uses Moviepy and ImageMagick to generate watermarked Video
    def WaterMarkVideo(self, video: bytes, text_to_write: str="WaterMark", extension: str="mp4") -> BytesIO:
        '''
        Functions returns watermarked video.
        
        :param video: Retrieved bytes data of a video file.
        
        :param text_to_write: Text to be used as watermark.

        :param extension: The extension to determine the video file format.
        
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
    def WaterMarakPDF_pdfium(self, pdf: bytes, text_to_write: str) -> bytes:
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
            wmImage = self.WaterMarkImage(img=bio,text_to_write=text_to_write, extension="jpg")
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
        return ret.getvalue()

    # This function uses pydub and ffmpeg. install ffmpeg and set environment variable to its bin folder
    def WaterMarkAudio(self, audio: bytes, text_to_write: str, extension: str="wav") -> BytesIO:
        '''
        Function creates a wav file with text to speech, overlays it with original audio and returns overlayed file

        :param audio: Retrived bytes of audio file as retrieved from read() function from database.
        
        :param text_to_write: The text required to be spoken by bot and watermarked in audio file.

        :param extension: The extension/type of data being submitted as audio.
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
            if extension == "wav":
                engine.save_to_file(text=text_to_write, filename=wm.name+".wav")
            elif extension == "mp3":
                engine.save_to_file(text=text_to_write, filename=wm.name+".mp3")
            
            engine.runAndWait()
            if extension == "wav":
                audWM = AudioSegment.from_wav(wm.name+".wav")
            elif extension == "mp3":
                audWM = AudioSegment.from_mp3(wm.name+".mp3")
            # audio is a raw data so save it to temporary file, as pydub accepts file from disk only.
            with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_") as org:
                org.write(audio)
                # load file to audOrigin; the original file
                try:
                    audOrigin = AudioSegment.from_file(file=org.name, format= extension)
                except:
                    audOrigin = AudioSegment.from_file(file=org.name, format= "mp3")
                # overlay both clips
                clip: AudioSegment = audOrigin.overlay(audWM)
                
                # save the newly created clip to temporary file for opening and exporting
                with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_", suffix="."+extension) as f:
                    print(f.name)
                    clip.export(f.name,format=extension)
                    # open saved file and return buffer as BytesIO
                    with open(f.name,"rb") as retFile:
                        buffer = retFile.read()
                        return BytesIO(buffer)

    # This function uses pydub and ffmpeg. install ffmpeg and set environment variable to its bin folder
    def WaterMark_WAV(self, audio: bytes, text_to_write: str) -> BytesIO:
        """
        Function creates a wav file with text to speech, overlays it with original audio and returns overlayed file

        :param audio: Retrived bytes of audio file as retrieved from read() function from database.
        
        :param text_to_write: The text required to be spoken by bot and watermarked in audio file.

        :param extension: The extension/type of data being submitted as audio.
        """
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
            engine.save_to_file(text=text_to_write, filename=wm.name+".wav")
            
            engine.runAndWait()
            audWM = AudioSegment.from_wav(wm.name+".wav")
            
            # audio is a raw data so save it to temporary file, as pydub accepts file from disk only.
            with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_") as org:
                org.write(audio)
                # load file to audOrigin; the original file
                audOrigin = AudioSegment.from_file(file=org.name, format= "wav")
                
                # overlay both clips
                clip: AudioSegment = audOrigin.overlay(audWM)
                
                # save the newly created clip to temporary file for opening and exporting
                with tempfile.NamedTemporaryFile(mode="w+b", delete=False, prefix="Arch_", suffix="."+"wav") as f:
                    print(f.name)
                    clip.export(f.name,format="wav")
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

        :param extension: The extension/type of data being submitted as audio.
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
                    print(f.name)
                    clip.export(f.name,format="mp3")
                    # open saved file and return buffer as BytesIO
                    with open(f.name,"rb") as retFile:
                        buffer = retFile.read()
                        return BytesIO(buffer)
            
