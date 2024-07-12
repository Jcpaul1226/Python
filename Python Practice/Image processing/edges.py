#find faces in picture


from PIL import Image
import face_recognition

#load file into numpy array
image = face_recognition.load_image_file("office.jpg")

#Find all the faces in the image using the default HOG-based model
#not as accurate as cnn and not GPU accelerated

face_locations = face_recognition.face.locations(image)

for face_location in face_locations:

    #print the location of each face in this image
    top,right,bottom,left = face_location

    #you can access the actual face itself like this
    face_image = image[top:bottom,left:right]
    pil_image = image.fromarray(face_image)
    pil_image.show()