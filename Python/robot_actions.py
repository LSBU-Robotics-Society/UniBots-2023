import settings
import robot_interface as rb
import vision


# Search for a tag and move the robot towards it
def move_to_tag(index):
    image = rb.get_image()
    vision.image_process(image)

    if vision.tag_visible(index):
        rb.turn_stop()
        rb.move_forward()
    else:
        rb.move_stop()
        rb.turn_left()


# Go to the starting position
def move_to_home():
    move_to_tag(settings.HOME_TAG)



def dead_stop():
    rb.turn_stop()
    rb.move_stop()

