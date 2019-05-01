"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import picamera
import os
from PIL import Image, ImageDraw

from google.cloud import vision
client = vision.ImageAnnotatorClient()
image_name = 'image.jpg'

def takephoto():
    camera = picamera.PiCamera()
    camera.capture(image_name)

def draw_face_rectangle(image_in, rect_in):
    im = Image.open(image_in)
    f,e = os.path.splitext(image_in)
    image_out = f + "_out_boundrectangle" + e
    print("image out is named: "+ image_out)

    draw = ImageDraw.ImageDraw(im)
    draw.rectangle(rect_in)
    im.save(image_out)

def main():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    with open(image_name, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations
    # print(faces)

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        rectangle = []
        rectangle.append((face.bounding_poly.vertices[0].x,face.bounding_poly.vertices[0].y))
        rectangle.append((face.bounding_poly.vertices[2].x,face.bounding_poly.vertices[2].y))
        print('face bounds: {}'.format(','.join(vertices)))

        draw_face_rectangle(image_name, rectangle)



if __name__ == '__main__':

    main()
