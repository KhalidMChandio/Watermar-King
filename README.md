
# WaterMarker

Watermark images (JPG, PNG, TIFF, BMP), PDFs, Video (MP4, AVI, OGV, WEBM) and even Audio(MP3, WAV, OGG) files.

Many security concious organizations do not want their employees to share sensitive documents, images, videos, audios etc. with unauthorized personnel. In order to prevent this, such data is required to be watermarked before being displayed to the employees. This utility is specially designed for such purpose and suitable for such purpose only; as it affects the quality of the images assuming the given scenario.

## Info

- The library uses CV2 to embed watermarks into the images.
- Pages are extracted from the PDF files as images and watermarked. A new PDF is created with those images and returned.
- Moviepy is used to watermark video files.
- Pydub is used to watermark audios. Pydub uses selected voice from the installed voices. Consequently, you may need to check and replace the index of the installed voices to select your choice. In my case English (America) is installed at index 28.

## Installation

- First of all, install ImageMagick and ensure that its path is included in the system environment.
- Install watermar_king package

    pip3 install watermar_king
- Within your top level directory use following command to test its working

    python -m tests.test
- An output directory will be created in the main directory. All sample files will be watermarked and put into that directory.

## Usage  

The test.py file in the tests folder contains implementation. All conversion methods accept binary data and return BytesIO().

### Watermark PDF

    def watermark_pdf(img, text_to_write, file_name):
        wm = WaterMarker()
        with open(img, "rb") as image:
            f = image.read()
            b = bytearray(f)
            out = wm.WaterMark_PDF(bytes(b), text_to_write=text_to_write)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())
        print("PDF file created")

### Watermark JPEG Image

    def watermark_jpeg(img, text_to_write, file_name):
        wm = WaterMarker()
        with open(img, "rb") as image:
            f = image.read()
            b = bytearray(f)
            out = wm.WaterMark_JPEG(bytes(b), text_to_write=text_to_write)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())
        print("JPEG file created")

### Watermark PNG Image

    def watermark_png(img, text_to_write, file_name):
        wm = WaterMarker()
        with open(img, "rb") as image:
            f = image.read()
            b = bytearray(f)
            out = wm.WaterMark_PNG(bytes(b), text_to_write=text_to_write)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())
        print("PNG file created")

### Watermark TIFF Image

    def watermark_tiff(img, text_to_write, file_name):
        wm = WaterMarker()
        with open(img, "rb") as image:
            f = image.read()
            b = bytearray(f)
            out = wm.WaterMark_TIFF(bytes(b), text_to_write=text_to_write)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())
        print("TIFF file created")

### Watermark Bitmap BMP Image

    def watermark_bmp(img, text_to_write, file_name):
        wm = WaterMarker()
        with open(img, "rb") as image:
            f = image.read()
            b = bytearray(f)
            out = wm.WaterMark_BMP(bytes(b), text_to_write=text_to_write)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())
        print("BMP file created")

### Watermark Video File

    # The extensions can be one of the mp4, avi, ogv and webm.
    def watermark_video(video, text_to_write, file_name):
        wm = WaterMarker()
        with open(video, "rb") as vid:
            f = vid.read()
            b = bytearray(f)
            out = wm.WaterMark_Video(bytes(b), text_to_write=text_to_write, extension="mp4")
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())            
        print("MP4 file created")

### Watermarking Audio Files

The class uses pydub to convert given text to speech. pydub installs many voices which may vary as per individual system settings, therefore, use this code to check on which index your selected voice is installed. Following code will print all voices installed on your system.

    import pyttsx3

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices: 
        print(f'voice: {voice.name}')

### Watermark MP3 Audio

    def watermark_mp3(audio, text_to_write, file_name):
        wm = WaterMarker()
        with open(audio, "rb") as vid:
            f = vid.read()
            b = bytearray(f)
            out = wm.WaterMark_MP3(bytes(b), text_to_write=text_to_write, voice_index=28)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())
        print("MP3 file created")

### Watermark Wav Audio

    def watermark_wav(audio, text_to_write, file_name):
        wm = WaterMarker()
        with open(audio, "rb") as vid:
            f = vid.read()
            b = bytearray(f)
            out = wm.WaterMark_WAV(bytes(b), text_to_write=text_to_write,voice_index=28)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())        
        print ("WAV file created")

### Watermark Ogg Audio

    def watermark_ogg(audio, text_to_write, file_name):
        wm = WaterMarker()
        with open(audio, "rb") as vid:
            f = vid.read()
            b = bytearray(f)
            out = wm.WaterMark_OGG(bytes(b), text_to_write=text_to_write,voice_index=28)
            with open(file_name, "wb") as f:
                f.write(out.getbuffer())        
        print ("OGG file created")
