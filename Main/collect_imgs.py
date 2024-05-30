import os
import cv2

DATA_DIR = './data' #Path to the directory where the captured images will be stored.

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

#number of classes & captured image for every class.
number_of_classes = 27
dataset_size = 100

cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    for j in range(number_of_classes):
        class_dir = os.path.join(DATA_DIR, str(j))
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

        print('Collecting data for class {}'.format(j))

        print("Press 'q' to start collecting images for class {}.".format(j))
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image.")
                continue

            cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            key = cv2.waitKey(25)
            if key == ord('q'):
                break
            if key == 27:  # 27 is the Esc key
                cap.release()
                cv2.destroyAllWindows()
                print("Exited by user.")
                exit()

        counter = 0
        while counter < dataset_size:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image.")
                continue

            cv2.imshow('frame', frame)
            key = cv2.waitKey(25)
            if key == 27:  # 27 is the Esc key
                cap.release()
                cv2.destroyAllWindows()
                print("Exited by user.")
                exit()
            cv2.imwrite(os.path.join(class_dir, '{}.jpg'.format(counter)), frame)

            counter += 1

    cap.release()
    cv2.destroyAllWindows()
