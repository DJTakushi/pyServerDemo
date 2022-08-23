# https://auth0.com/blog/image-processing-in-python-with-pillow/
from PIL import Image
import os


def getFiles():
    file_l = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            # print(name)
            file_l.append(name)
        #   print(os.path.join(root, name))
        # for name in dirs:
        #   print(os.path.join(root, name))
    return file_l
def genNewName(nameIn,suffix):
    nameParts = nameIn.split(".")
    nameOut = nameParts[0]+suffix+"."+nameParts[1]
    return nameOut
def isImage(nameIn):
    output=False
    extIn = nameIn.split(".")[1]
    imgExtensions = ["JPG","jpg","png"]
    for i in imgExtensions:
        if extIn == i:
            output = True
            break;
    return output

if __name__ == "__main__":
    print("...starting img.py...")
    file_l = getFiles()
    for i in file_l:
        if isImage(i):
            image = Image.open(i)
            image.thumbnail((1500,1500))
            print(image.size)
            image.save(genNewName(i,"_resize"))
    print("done.")
