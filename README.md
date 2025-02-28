
# WaterMarker

Watermark images (JPG, PNG, TIFF, BMP), PDFs, Video (MP4, AVI, OGV, WEBM) and even Audio(MP3, WAV) files.

Many security concious organizations do not want their employees to share sensitive documents, images, videos, audios etc. with unauthorized personnel. In order to prevent this, such data is required to be watermarked before being displayed to the employees. This utility is specially designed for such purpose and suitable for such purpose only; as it affects the quality of the images assuming the given scenario.

## Usage

    - First of all, install ImageMagick and ensure that its path is included in the system environment.
    - Install requirements.txt using "pip install requirements.txt"
    - run test.py using "python test.py" which will create separate watermarked files against the given sample files.
    - open test.py and see the implementation. 
    
## Info

    - The library uses CV2 to embed watermarks into the images.
    - Pages are extracted from the PDF files as images and watermarked. A new PDF is with those images and returned.
    - Moiepy is used to watermark video files.
    - Pydub is used to watermark audios. Pydub uses selected voice from the installed voices. Consequently, you may need to check and replace the index of the installed voices to select your choice. In my case English (America) is installed at index 28.
    - I am still working on watermarking audio files.  
    