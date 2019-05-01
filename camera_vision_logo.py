import picamera
from google.cloud import vision

client = vision.ImageAnnotatorClient()
image = 'image.jpg'

def takephoto():
    camera = picamera.PiCamera()
    camera.capture(image)

def main():
    global image
    takephoto() # First take a picture
    """Run a label request on a single image"""

    with open(image, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

if __name__ == '__main__':
    main()
