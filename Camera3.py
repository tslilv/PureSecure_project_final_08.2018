"""
Class camera
Camera.py
Tslil Vaitsman
Jan. 2018
python 2.7
"""
import cv2
import smtp3
import Client

# VIDEO NAME
VIDEO_NAME = 'output'
VIDEO_TYPE = '.avi'

# SCREENSHOT NAME
SCREENSHOT_NAME = 'screenshot'
SCREENSHOT_TYPE = '.jpg'

# FRAMES SIZE
WIDTH = 640
HEIGHT = 480
FRAMES_PER_SECOND = 20.0

WINDOW_NAME = "Motion Indicator"
FORMAT = 'XVID'

# mail warning
SUBJECT = 'Pure_Secure WARNING!'
BODY = "motion has detected right now!!"
LOGO_IMG = 'a.jpg'


class Camera():

    video_id = 0
    sh_id = 0
    warning_count = 0

    def __init__(self, user):

        self.email = user
        self.w = WIDTH
        self.h = HEIGHT
        self.fps = FRAMES_PER_SECOND
        self.size = (self.w, self.h)

        # create video capture object
        self.cap = cv2.VideoCapture(0)

        # prepare capture
        self.ret, self.frame = self.cap.read()

        # Prepare output window
        self.win_name = WINDOW_NAME
        cv2.namedWindow(self.win_name, cv2.WINDOW_AUTOSIZE)

        # Read three images first
        self.prev_frame = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_RGB2GRAY)
        self.current_frame = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_RGB2GRAY)
        self.next_frame = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_RGB2GRAY)

        # Define the codec and create VideoWriter object
        self.fourcc = cv2.VideoWriter_fourcc(*FORMAT)
        self.out = cv2.VideoWriter(VIDEO_NAME+str(Camera.video_id)+VIDEO_TYPE, self.fourcc, self.fps, (self.w, self.h))
        Camera.video_id += 1

    @staticmethod
    def diff_img(tprev, tc, tnex):
        """
        Generate the difference from the 3 captured images
        """
        im1 = cv2.absdiff(tnex, tc)
        im2 = cv2.absdiff(tc, tprev)
        return cv2.bitwise_and(im1, im2)

    def capture_video(self):
        """

        """
        # Read in a new frame...
        self.ret, self.frame = self.cap.read()

        # consecutive images
        diffe = self.diff_img(self.prev_frame, self.current_frame, self.next_frame)
        ret, thresh = cv2.threshold(diffe, 80, 255, cv2.THRESH_BINARY)
        # thresh = cv2.blur(thresh, (1, 1))

        if thresh.max() > 0:

            #save frame
            cv2.imwrite(SCREENSHOT_NAME+str(Camera.sh_id)+SCREENSHOT_TYPE, self.current_frame)
            #send to database
            Client.send_save_request(self.email, SCREENSHOT_NAME+str(Camera.sh_id)+SCREENSHOT_TYPE)

            #
            if Camera.warning_count <= 9:
                self.warning()
                Camera.warning_count += 1\

            Camera.sh_id += 1

        cv2.imshow(self.win_name, thresh)

        # Put images in the right order...
        self.prev_frame = self.current_frame
        self.current_frame = self.next_frame
        self.next_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)

    def save_video(self):
        """
        write the frame
        """
        self.out.write(self.frame)

    def __delete__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.out.release()

    def warning(self):
        """
        sends email to user
        """
        smtp3.send_email(self.email, SUBJECT, BODY, [SCREENSHOT_NAME+str(Camera.sh_id)+SCREENSHOT_TYPE, LOGO_IMG])


def main(user="email_user"):
    # Create a camera instance
    cam1 = Camera(user)

    while True:
        # Display the resulting frames...
        cam1.capture_video()    # Live stream of video on screen...
        cam1.save_video()       # Save video to file 'output.avi'...
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

if __name__ == "__main__":
    main()
