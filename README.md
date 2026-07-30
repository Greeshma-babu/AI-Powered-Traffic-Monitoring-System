# AI Traffic Monitoring & Speed Violation Detection System

## Overview

An AI-powered real-time traffic monitoring system built using **YOLOv8, DeepSORT, OpenCV, Streamlit, and PostgreSQL** to detect, track, count, and analyze vehicles from video streams. The system identifies vehicles such as cars, scooters, and auto-rickshaws, calculates vehicle speed, detects speed limit violations, displays annotated output video in Streamlit, and stores traffic analytics with date/time records in PostgreSQL.

## Technologies Used

- **Python** – Core development language
- **YOLOv8 (Ultralytics)** – Real-time vehicle object detection
- **DeepSORT** – Multi-object tracking and unique vehicle ID assignment
- **OpenCV** – Video processing, bounding boxes, and output video generation
- **Streamlit** – Interactive web dashboard for live video visualization and analytics
- **PostgreSQL** – Database storage for traffic records and violation history
- **NumPy** – Speed calculation and mathematical processing
- **Docker** – Application containerization and deployment

## Key Features

- Real-time vehicle detection and tracking
- Vehicle classification:
  - Car
  - Scooter/Motorcycle
  - Auto-Rickshaw
  - Bus
  - Truck

- Speed estimation for each tracked vehicle
- Bounding box visualization with:
  - Vehicle type
  - Vehicle ID
  - Speed (km/hr)

- Overspeed violation detection
- Alert generation for vehicles exceeding speed limits
- Streamlit dashboard showing:
  - Processed traffic video
  - Vehicle count
  - Speed alerts
  - Traffic statistics

- PostgreSQL database storage:
  - Detection date and time
  - Vehicle category
  - Vehicle count
  - Vehicle speed
  - Speed limit violation details


## System Workflow

Video Input  
↓  
YOLOv8 Vehicle Detection  
↓  
DeepSORT Vehicle Tracking  
↓  
Speed Estimation  
↓  
Overspeed Alert Detection  
↓  
Streamlit Dashboard Display  
↓  
PostgreSQL Traffic Analytics Storage


## Database Records Example
| Date       | Vehicle ID | Vehicle Type | Speed    | Violation    |
| ---------- | ---------- | ------------ | -------- | ------------ |
| 2026-07-29 | Car-1      | Car          | 90 km/hr | Overspeed    |
| 2026-07-29 | Car-2      | Car          | 45 km/hr | No Violation |
| 2026-07-29 | Scooter-1  | Scooter      | 35 km/hr | No Violation |
| 2026-07-29 | Scooter-2  | Scooter      | 80 km/hr | Overspeed    |
| 2026-07-29 | Scooter-3  | Scooter      | 30 km/hr | No Violation |
| 2026-07-29 | Auto-1     | Auto         | 40 km/hr | No Violation |
| 2026-07-29 | Auto-2     | Auto         | 42 km/hr | No Violation |
| 2026-07-29 | Lorry-1    | Lorry        | 50 km/hr | No Violation |

## Summary
| Date       | Total Vehicles | Cars | Autos | Scooters | Lorries | Total Violations |
| ---------- | -------------- | ---- | ----- | -------- | ------- | ---------------- |
| 2026-07-29 | 8              | 2    | 2     | 3        | 1       | 2                |



## Applications

- Smart city traffic monitoring
- Highway surveillance
- Automatic speed violation detection
- Intelligent transportation systems
- Traffic flow analytics
- Road safety monitoring

## Instructions to execute
cd "C:\AI\AI Traffic Monitoring System\AI-Powered-Traffic-Monitoring-System"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py 