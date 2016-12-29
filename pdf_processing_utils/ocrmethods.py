from PIL import Image
import pytesseract

def convert_image(origname,newname):
    im = Image.open(origname)
    im.save(newname)

def get_text_from_image(image_filename,engine="tesseract"):
    if engine == "tesseract":
        text = pytesseract.image_to_string(Image.open(image_filename))
        return text
    else:
        raise NotImplementedError