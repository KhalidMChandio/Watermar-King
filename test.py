from io import BytesIO
import WaterMarker, os
from PIL import Image



def create_foler():
    if not os.path.exists("output"):
        os.makedirs("output")


def watermark_jpeg(img, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(img, "rb") as image:
        f = image.read()
        b = bytearray(f)
        out = wm.WaterMark_JPEG(bytes(b), text_to_write=text_to_write)
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())
    print("JPEG file created")

def watermark_png(img, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(img, "rb") as image:
        f = image.read()
        b = bytearray(f)
        out = wm.WaterMark_PNG(bytes(b), text_to_write=text_to_write)
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())
    print("PNG file created")

def watermark_tiff(img, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(img, "rb") as image:
        f = image.read()
        b = bytearray(f)
        out = wm.WaterMark_TIFF(bytes(b), text_to_write=text_to_write)
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())
    print("TIFF file created")

def watermark_bmp(img, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(img, "rb") as image:
        f = image.read()
        b = bytearray(f)
        out = wm.WaterMark_BMP(bytes(b), text_to_write=text_to_write)
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())
    print("BMP file created")

def watermark_video(video, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(video, "rb") as vid:
        f = vid.read()
        b = bytearray(f)
        out = wm.WaterMarkVideo(bytes(b), text_to_write=text_to_write, extension="mp4")
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())            
    print("MP4 file created")

def watermark_mp3(audio, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(audio, "rb") as vid:
        f = vid.read()
        b = bytearray(f)
        out = wm.WaterMark_MP3(bytes(b), text_to_write=text_to_write)
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())
    print("MP3 file created")            

def watermark_wav(audio, text_to_write, file_name):
    wm = WaterMarker.WaterMarker()
    create_foler()
    file_name = os.path.join(os.getcwd(), "output", file_name) 
    with open(audio, "rb") as vid:
        f = vid.read()
        b = bytearray(f)
        out = wm.WaterMark_WAV(bytes(b), text_to_write=text_to_write)
        with open(file_name, "wb") as f:
            f.write(out.getbuffer())        
    print ("WAV file created")

if __name__ == "__main__":
    watermark_jpeg("sample_jpeg.jpg", "Watermarking this image", "output_jpeg.jpg")    
    watermark_png("sample_png.png", "Watermarking this image", "output_png.png")
    watermark_tiff("sample_tiff.tiff", "Watermarking this image", "output_tiff.tiff")
    watermark_bmp("sample_bmp.bmp", "Watermarking this image", "output_bmp.bmp")
    watermark_mp3("sample_mp3.mp3", "Watermarking this Audio", "output_mp3.mp3")
    watermark_wav("sample_wav.wav", "Watermarking this Audio", "output_wav.wav")
    watermark_video("sample_mp4.mp4", "Watermarking this video", "output_mp4.mp4")
