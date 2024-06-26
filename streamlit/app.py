import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pickle
import os
import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.write(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4); /* Adjust the alpha value to control darkness */
            z-index: -1;
        }}
        .horizontal-values {{
            display: flex;
            justify-content: space-around;
            padding: 10px;
        }}
        .value-box {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            width: 30%;
        }}
      


        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_from_local('BG.jpg')

# Function to load the sign language model
@st.cache_resource
def load_sign_language_model(model_path):
    with open(model_path, 'rb') as f:
        model_dict = pickle.load(f)
    return model_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Load the model and labels
model_path = '/Users/khaled2509/Desktop/Bootcamp/HandTalk_Project/model.p'  # Adjust the path if necessary
if not os.path.exists(model_path):
    st.error(f"Model file not found: {model_path}")
else:
    model = load_sign_language_model(model_path)

    labels_dict = {0: 'Nothing', 1: 'B', 2: 'C', 3: 'A', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J',
                   11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T',
                   21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}

    expected_feature_size = 84

    # Set up the Streamlit interface
    title_html = """
    <h1 style="color:;font-family ,font-size: 44px ; text-shadow: 2px 2px 5px rgba(0,0,0,0.5); ">American Sign Language Detection</h1>
    """
    st.markdown(title_html, unsafe_allow_html=True)
    text_html = """
    <h2 style="color:white
 ;font-size: 22px ;">Capture live video from your webcam to detect American Sign Language.</h2>
    """
    st.markdown(text_html, unsafe_allow_html=True)

    use_webcam = st.checkbox("Use webcam")


    if use_webcam:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Error: Could not open webcam.")
        else:
            stframe = st.empty()
            # Load background image

            try:

                while True:
                    data_aux = []
                    x_ = []
                    y_ = []

                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to grab frame.")
                        break

                    H, W, _ = frame.shape

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    results = hands.process(frame_rgb)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                frame,  # image to draw
                                hand_landmarks,  # model output
                                mp_hands.HAND_CONNECTIONS,  # hand connections
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style()
                            )

                            for i in range(len(hand_landmarks.landmark)):
                                x = hand_landmarks.landmark[i].x
                                y = hand_landmarks.landmark[i].y

                                x_.append(x)
                                y_.append(y)

                            for i in range(len(hand_landmarks.landmark)):
                                x = hand_landmarks.landmark[i].x
                                y = hand_landmarks.landmark[i].y
                                data_aux.append(x - min(x_))
                                data_aux.append(y - min(y_))

                            # Padding data_aux to match the expected feature size
                            while len(data_aux) < expected_feature_size:
                                data_aux.append(0.0)

                            if len(data_aux) == expected_feature_size:
                                prediction = model.predict([np.asarray(data_aux)])
                                predicted_character = labels_dict[int(prediction[0])]

                                x1 = int(min(x_) * W) - 10
                                y1 = int(min(y_) * H) - 10
                                x2 = int(max(x_) * W) - 10
                                y2 = int(max(y_) * H) - 10

                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

                    stframe.image(frame, channels="BGR")

                    if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
                        break
            finally:
                cap.release()
                cv2.destroyAllWindows()
