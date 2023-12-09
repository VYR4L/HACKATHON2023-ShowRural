import os
import cv2
import face_recognition
from datetime import datetime
from models import Employee, Visitor, Clock_in, db, ROOT_DIR


webcam = cv2.VideoCapture(0)

class Camera:
    def __init__(self):
        self.reference_images = []
        self.employees_reference = list(db.query(Employee).all())
        self.visitors_reference = list(db.query(Visitor).all())

    def recording(self):
        not_recognize = 0
        while 1:
            for directory, category in [(f'{ROOT_DIR}/employees', self.employees_reference),
                                       (f'{ROOT_DIR}/visitors', self.visitors_reference)]:
                for file in os.listdir(directory):
                    if file.endswith(".jpg"):
                        name_without_extension = os.path.splitext(file)[0]
                        reference_images = face_recognition.load_image_file(os.path.join(directory, file))
                        features_reference = face_recognition.face_encodings(reference_images)[0]
                        category.append(features_reference)

        self.employees_reference.reverse()
        self.visitors_reference.reverse()

        ret, frame = webcam.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(image)
        faces_features = face_recognition.face_encodings(image, faces)

        face_recognized = False

        for face_feature in faces_features:
            for reference_features in reference_images:
                distance = face_recognition.face_distance([reference_features], face_feature)
                if distance < 0.5:
                    face_recognized = True
                    employee_name = name_without_extension
                    if face_recognized and employee_name in self.employees_reference:
                        recognized_employee = Clock_in(
                            type = 'Employee',
                            name = Employee.name,
                            rg = Employee.rg,
                            date = datetime.now()
                        )
                        db.add(recognized_employee)
                        db.commit()
                        self.employees_reference.remove(employee_name)

            if not face_recognized:
                not_recognize += 1
                for index in range(not_recognize):
                    ret, visitor_frame = webcam.read()
                    cv2.imwrite(f'{ROOT_DIR}/visitor/visitor{index}.jpg', visitor_frame)
                    visitor = Clock_in(
                        type = 'Visitor',
                        name = f'Visitor{index}', # TODO
                        rg = index, # TODO
                        date = datetime.now()
                    )
                    db.add(visitor)
                    db.commit()


