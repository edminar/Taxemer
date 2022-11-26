import face_recognition
from PIL import Image
import pickle
import cv2

def extracting_faces(img_path):
    count = 0
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"img/{count}_face_img.jpg")
        count += 1

    return f"Нашел {count} лицо (лица) на этой фотографии"


def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]
    # print(img1_encodings)

    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)[0]

    result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    # print(result)

    if result[0]:
        print("Добро пожаловать в клуб! :*")
    else:
        print("Извини, не сегодня... Следующий!")


def detect_person_in_video():
    data = pickle.loads(open("Liza_encodings.pickle", "rb").read())
    video = cv2.VideoCapture(0)

    video.set(cv2.CAP_PROP_FPS, 24)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter('output.avi', codec, 25.0, (1280, 720))

    while True:
        ret, image = video.read()

        locations = face_recognition.face_locations(image, model="hog")
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_location in zip(encodings, locations):
            result = face_recognition.compare_faces(data["encodings"], face_encoding)
            match = None

            if True in result:
                match = data["name"]
                print(f"Найдено совпадение! {match}")
            else:
                print("ВНИМАНИЕ! ПОСТОРОННИЙ В КАДРЕ!")

            left_top = (face_location[3], face_location[0])
            right_bottom = (face_location[1], face_location[2])
            color = [0, 0, 255]
            cv2.rectangle(image, left_top, right_bottom, color, 4)

            left_bottom = (face_location[3], face_location[2])
            right_bottom = (face_location[1], face_location[2] + 20)
            cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
            cv2.putText(
                image,
                match,
                (face_location[3] + 10, face_location[2] + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                4
            )

        cv2.imshow("Video Recording window", image)
        out.write(image)

        k = cv2.waitKey(20)
        if k == ord("q"):
            print("Q нажата, камера закрыта")
            break
    out.release()
    video.release()
    cv2.destroyAllWindows()


def main():
    detect_person_in_video()


if __name__ == '__main__':
    main()
