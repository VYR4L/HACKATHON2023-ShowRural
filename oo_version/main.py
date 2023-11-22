import threading
from face_recognition_oo import Camera, db


if __name__ == "__main__":
    camera_instance = Camera()
    face_thread = threading.Thread(target=camera_instance.recording)
    face_thread.start()

    try:
        face_thread.join()
    finally:
        db.close()