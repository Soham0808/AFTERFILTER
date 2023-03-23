
import numpy as np 
import cv2
from tkinter.filedialog import *

c=int(input("Choose a number between 1-7 and see the magic!!\n\nEnter: "))

'''
1. B/W to Colour conversion
2. Animated Image Conversion
3. Colour to Sketch Conversion
4. Colour to B/W Conversion
5. Colour to Negative Image
6. Colour to Binary Image
7. Colour to ASCII Image
'''

#1. B/W to Colour conversion
if c==1:
    print("Select a B/W Image:")
    net = cv2.dnn.readNetFromCaffe('D:\Project With Visual Studio Code/MODEL/colorization_deploy_v2.prototxt','D:\Project With Visual Studio Code/MODEL/colorization_release_v2.caffemodel')
    pts = np.load('D:\Project With Visual Studio Code/MODEL/pts_in_hull.npy')
 

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2,313,1,1)

    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1,313],2.606,dtype='float32')]

    photo = askopenfilename()
    img = cv2.imread(photo)

    scale_p=3.50
    width=620
    height=770
    dimension=(width, height)

    image=cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

    scaled = image.astype("float32")/255.0
    lab = cv2.cvtColor(scaled,cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab,(224,224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1,2,0))

    ab = cv2.resize(ab, (image.shape[1],image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2)

    colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized,0,1)

    colorized = (255 * colorized).astype("uint8") #colorized

    Hori = np.concatenate((image, colorized), axis=1)
    cv2.imshow('Original VS Colorized', Hori)

    #To save the modified picture.
    c1=int(input("Do you want to save the Colour Picture? Press 1 for Yes and 2 for No: "))
    if c1==1 :
        cv2.imwrite("Colour pic.png", colorized)
        print("Picture Saved!!")
    else:
        print("Okay!! Picture Not Saved.")

    cv2.waitKey(0)



#2. Animated Image
elif c==2:
    print("Select an Image:")
    photo = askopenfilename()
    image = cv2.imread(photo)

    scale_p=3.50
    width=620
    height=770
    dimension=(width, height)

    img=cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = cv2.medianBlur(grey, 5)
    edges = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    #cartoonize
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask = edges)

    Hori = np.concatenate((img, cartoon), axis=1)
    cv2.imshow('Original VS Animated', Hori)

    #To save the modified picture.
    c1=int(input("Do you want to save the Animated Picture? Press 1 for Yes and 2 for No: "))
    if c1==1 :
        cv2.imwrite("Animation.png", cartoon)
        print("Picture Saved!!")
    else:
        print("Okay!! Picture Not Saved.")
    
    cv2.waitKey(0)



#3. Pen(cil) sketches the image
elif c==3:
    print("Select an Image:")
    photo = askopenfilename()
    image = cv2.imread(photo) #show real image

    scale_p=3.50
    width=620
    height=770
    dimension=(width, height)

    img=cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    inv_grey_img=255-grey_img
    blur_img=cv2.GaussianBlur(inv_grey_img, (21,21), 0)
    inv_blur=255-blur_img
    sktch_img=cv2.divide(grey_img, inv_blur, scale=256.0)

    cv2.imshow('Original Image',img)
    penSktch_img=cv2.divide(grey_img, inv_grey_img, scale=256.0) #Image sketched with Pencil
    cv2.imshow('Pen Sketched Image',penSktch_img)

    #Hori = np.concatenate((img, sktch_img), axis=1)
    #cv2.imshow('Original VS Sketched', Hori)


#To save the modified picture.
    c1=int(input("Do you want to save the Sketched Picture? Press 1 for Yes and 2 for No: "))
    if c1==1 :
        cv2.imwrite("Sketch.png", penSktch_img)
        print("Picture Saved!!")
    else:
        print("Okay!! Picture Not Saved.")
    
    cv2.waitKey(0)



#4. Colour to B/W Conversion
elif c==4:
    print("Select an Image:")
    photo = askopenfilename()
    image = cv2.imread(photo)

    scale_p=3.50
    width=620
    height=770
    dimension=(width, height)

    img=cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #shows BnW image

    #Hori = np.concatenate((img, grey_img), axis=1)
    #cv2.imshow('Original VS B/W', Hori)
    cv2.imshow('Original Image',img)
    cv2.imshow('B/W Image',grey_img) 

    #To save the modified picture.
    c1=int(input("Do you want to save the B/W Picture? Press 1 for Yes and 2 for No: "))
    if c1==1 :
        cv2.imwrite("BW.png", grey_img)
        print("Picture Saved!!")
    else:
        print("Okay!! Picture Not Saved.")
    
    cv2.waitKey(0)



#5. Colour to Negative Image
elif c==5:
    print("Select an Image:")
    photo = askopenfilename()
    image = cv2.imread(photo)

    scale_p=3.50
    width=620
    height=770
    dimension=(width, height)

    img=cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    inv_grey_img=255-grey_img #shows negative image

    #Hori = np.concatenate((img, grey_img), axis=1)
    #cv2.imshow('Original VS B/W', Hori)
    cv2.imshow('Original Image',img)
    cv2.imshow('Negative Image',inv_grey_img)

    #To save the modified picture.
    c1=int(input("Do you want to save the Negative Picture? Press 1 for Yes and 2 for No: "))
    if c1==1 :
        cv2.imwrite("-ve.png", inv_grey_img)
        print("Picture Saved!!")
    else:
        print("Okay!! Picture Not Saved.")
    
    cv2.waitKey(0)



#6. Colour to Binary Image
elif c==6:
    print("Select an Image:")
    photo = askopenfilename()
    image=cv2.imread(photo)

    scale_p=3.50
    width=500
    height=500
    dimension=(width, height)

    img=cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

    cv2.imshow("Original", img)

    grey_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, bin_img = cv2.threshold(grey_img, 127, 255, cv2.THRESH_BINARY)

    cv2.imshow("Binary", bin_img) #displays Binary image

    #To save the modified picture.
    c1=int(input("Do you want to save the Negative Picture? Press 1 for Yes and 2 for No: "))
    if c1==1 :
        cv2.imwrite("Binary image.png", bin_img)
        print("Picture Saved!!")
    else:
        print("Okay!! Picture Not Saved.")

    cv2.waitKey(0)



#7. Colour to ASCII Image
elif c==7:
    import ascii_magic
    c1=input("Enter 'U' to import image from URL and 'D' to import image from Device: ")

    if c1 == 'U' or c1 == 'u':
        loc=input("Please Give the Image URL: ")
        try:
            my_art = ascii_magic.from_url(loc, columns=100)
        except OSError as e:
            print(f'Could not load the image, server said: {e.code} {e.msg}')

    elif c1 == 'D' or c1 == 'd':
        loc=input("Please Give the Image location: ")
        my_art = ascii_magic.from_image_file(loc)

    else:
        print("Improper Image Source!")

    print("\nResults:\n\n")
    ascii_magic.to_terminal(my_art) #displays the ASCII image in terminal


#default case
else:
    print("SORRY! Wrong Operation Chosen. :)))")