from picamera import PiCamera
from time import sleep

def create_dataset(nrOfImagesToCreate, offset):
    camera = PiCamera()
    camera.rotation = 180

    camera.start_preview()
    sleep(2)
    for i in range(nrOfImagesToCreate):
        camera.capture('brain/dataset_owner/ana/000' + str(i+offset) + '.jpg')
        sleep(1)
    camera.stop_preview()

create_dataset(20, 200)
