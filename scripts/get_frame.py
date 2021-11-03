import cv2
from os.path import exists
import easyocr


'''get_image function takes in a path to a video as well as a path and name to an image, and produces
   an image from this video and saves it to the path with the image name. The function also returns a 
   list of all of the text found in that frame(could be used to pre-identify camera name without user
   input. See __name__ == __main__ section for example use'''

def get_image(file_path, write_path):
    reader = easyocr.Reader(['en'])
    if(exists(file_path) == False):
        print("Given file_path does not exist")
        return -1

    text_list = []
    vidObj = cv2.VideoCapture(file_path)
    total = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

    vidObj.set(cv2.CAP_PROP_POS_FRAMES, total/2)

    while True:
        success, image = vidObj.read()
        if(success):
            if(cv2.imwrite(write_path, image)) == False:
                print("Bad Write Path")
                return -1
            try:
                for i in reader.readtext(image):
                    text_list.append(i[1])
                return text_list
            except:
                print("Easy OCR failed, but image write was successful, returning 0")
                #return 0



if __name__ == "__main__":
    text = get_image("Videos/ee7ac_o_test.avi", "Images/test_image.jpg")
    print(text)

