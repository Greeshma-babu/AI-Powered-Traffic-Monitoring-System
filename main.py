import os
import time
import tempfile
import cv2
import streamlit as st

from datetime import datetime

from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

from database.postgres import (
    create_table,
    save_traffic_data
)


# =====================================================
# STREAMLIT CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Traffic Monitoring System",
    layout="wide"
)


create_table()


st.title("🚦 AI Traffic Monitoring System")



# =====================================================
# INPUT
# =====================================================

uploaded_video = st.file_uploader(
    "Upload Traffic Video",
    type=[
        "mp4",
        "avi",
        "mov"
    ]
)


speed_limit = st.slider(
    "Speed Limit (km/hr)",
    min_value=10,
    max_value=200,
    value=40,
    step=5
)



# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_models():

    model = YOLO(
        "models/yolov8n.pt"
    )


    tracker = DeepSort(

        max_age=60,

        n_init=3,

        max_cosine_distance=0.3,

        embedder="mobilenet"

    )


    return model, tracker



model, tracker = load_models()



# =====================================================
# VEHICLE CLASSES
# =====================================================

vehicle_classes = {

    2: "Car",

    3: "Motorcycle",

    5: "Bus",

    7: "Truck"

}



# BGR COLORS

vehicle_colors = {


    "Car":
        (255,0,0),          # Blue


    "Motorcycle":
        (255,0,255),        # Pink


    "Bus":
        (0,255,255),        # Yellow


    "Truck":
        (0,0,255)           # Red

}



# =====================================================
# VIDEO PROCESSING
# =====================================================

if uploaded_video:


    st.success(
        "Video uploaded successfully"
    )


    temp_file = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".mp4"

    )


    temp_file.write(

        uploaded_video.read()

    )


    input_video = temp_file.name



    cap = cv2.VideoCapture(
        input_video
    )


    if not cap.isOpened():

        st.error(
            "Cannot open video"
        )

        st.stop()



    fps = cap.get(
        cv2.CAP_PROP_FPS
    )


    if fps <= 0:

        fps = 30



    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )


    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )



    # =====================================================
    # OUTPUT VIDEO
    # =====================================================


    os.makedirs(
        "output",
        exist_ok=True
    )


    output = os.path.abspath(
        "output/result.avi"
    )


    fourcc = cv2.VideoWriter_fourcc(
        *"XVID"
    )


    writer = cv2.VideoWriter(

        output,

        fourcc,

        fps,

        (width,height)

    )



    if not writer.isOpened():

        st.error(
            "Video writer failed"
        )

        st.stop()



    frame_window = st.empty()



    # =====================================================
    # COUNTERS
    # =====================================================


    counted_ids = set()

    overspeed_ids = set()



    vehicle_count = {

        "Car":0,

        "Motorcycle":0,

        "Bus":0,

        "Truck":0

    }



    overspeed_count = 0

    frame_count = 0



    # =====================================================
    # FRAME LOOP
    # =====================================================

    while True:


        ret, frame = cap.read()


        if not ret:

            break



        frame_count += 1


        detections = []



        results = model(

            frame,

            conf=0.5,

            verbose=False

        )[0]



        for box in results.boxes:


            cls = int(
                box.cls[0]
            )


            confidence = float(
                box.conf[0]
            )



            if cls in vehicle_classes:


                x1,y1,x2,y2 = map(

                    int,

                    box.xyxy[0]

                )


                detections.append(

                    (

                    [

                    x1,

                    y1,

                    x2-x1,

                    y2-y1

                    ],

                    confidence,

                    vehicle_classes[cls]

                    )

                )



        # DeepSORT

        tracks = tracker.update_tracks(

            detections,

            frame=frame

        )



        for track in tracks:


            if not track.is_confirmed():

                continue



            track_id = track.track_id



            x1,y1,x2,y2 = map(

                int,

                track.to_ltrb()

            )



            vehicle_type = track.get_det_class()



            if vehicle_type is None:

                continue



            # Count vehicles

            if track_id not in counted_ids:


                counted_ids.add(
                    track_id
                )


                vehicle_count[vehicle_type] += 1



            box_color = vehicle_colors.get(

                vehicle_type,

                (255,255,255)

            )



            label = ""

            text_color = box_color



            # Temporary speed

            speed = 50



            if speed > speed_limit:


                label = "OVER SPEED"

                text_color = (0,0,255)


                if track_id not in overspeed_ids:


                    overspeed_count += 1

                    overspeed_ids.add(
                        track_id
                    )



            cv2.rectangle(

                frame,

                (x1,y1),

                (x2,y2),

                box_color,

                3

            )



            cv2.putText(

                frame,

                f"{vehicle_type} ID:{track_id} {label}",

                (x1,y1-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                text_color,

                2

            )



        cv2.putText(

            frame,

            f"Vehicles:{len(counted_ids)} Overspeed:{overspeed_count}",

            (20,40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0,255,0),

            2

        )



        writer.write(frame)



        frame_window.image(

            frame,

            channels="BGR"

        )



    # =====================================================
    # RELEASE
    # =====================================================


    cap.release()

    writer.release()

    cv2.destroyAllWindows()


    time.sleep(3)



    print("======================")
    print("Frames:", frame_count)
    print("Output:", output)

    if os.path.exists(output):

        print(
            "Size:",
            os.path.getsize(output)
        )

    print("======================")



    # =====================================================
    # DATABASE
    # =====================================================


    st.subheader(
        "Vehicle Count"
    )


    st.json(
        vehicle_count
    )



    save_traffic_data(

        datetime.now(),

        vehicle_count,

        overspeed_count

    )


    st.success(
        "Traffic data saved"
    )