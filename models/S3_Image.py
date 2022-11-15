from PIL import Image
from io import BytesIO



class S3_Image:
    def __init__(self, key: str, body):
        self.id = key
        self.body = body
    
    def display_image(self):
        # Code for showing images from byte data saved in S3
        print(type(BytesIO(self.body)))
        img = Image.open(BytesIO(self.body))
        img.show()