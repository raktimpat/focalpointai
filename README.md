🤖 FocalPoint AI: An End-to-End Smart Image Editor

Hello! This is my portfolio project where I built a complete Machine Learning application from scratch. It's a web-based tool that uses AI to apply cool effects to images, like removing the background or anonymizing people.

I created two full versions to show how a project can evolve with more advanced requirements!

➡️ View the Live Demo Here! (You'll replace this with your actual deployment URL)

What it Looks Like

(I recommend using a tool like Giphy Capture or Kap to create a short GIF of you using the app and putting it here.)

✨ Features

This project is split into two versions, managed on separate Git branches:

v1: Semantic Segmentation (v1-deeplab branch)
This version uses a DeepLabV3 model to understand the scene as a whole.

Background Removal: Automatically makes the background of a person transparent.

Bokeh Effect: Blurs the background, making the person stand out.

Anonymize: Pixelates all people in the image.

v2: Instance Segmentation (v2-maskrcnn branch)
This version uses a more advanced Mask R-CNN model to identify and isolate each individual person.

Person Selection: Detects every individual person and lets you select them with checkboxes.

Targeted Effects: Apply effects to only the people you selected, or to everyone else but them.

Face-Only Anonymization: A special two-stage pipeline that first finds a person, then finds the face within that person's bounding box to apply a precise blur.

🛠️ Tech Stack

ML Framework: PyTorch & torchvision for the pretrained DeepLabV3 and Mask R-CNN models.

Backend API: FastAPI (running on GCP Cloud Run)

Frontend UI: Streamlit

Containerization: Docker

Cloud & Deployment: Google Cloud Platform (Cloud Run, Artifact Registry) & Streamlit Community Cloud

Core Language: Python 3.11

🚀 Getting Started Locally

Want to run this on your own machine? Here's how:

Prerequisites:

Python 3.11+

Git

1. Clone the Repository:

git clone [https://github.com/your-username/FocalPointAI.git](https://github.com/your-username/FocalPointAI.git)
cd FocalPointAI


2. Choose a Version:
Switch to the branch you want to run.

# For the simple, all-person editor
git checkout v1-deeplab

# OR for the advanced, single-person selector
git checkout v2-maskrcnn


3. Set up the Backend:
This runs the FastAPI server that does all the AI work.

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt 

# Run the server!
uvicorn main:app --reload


The backend will be running at http://localhost:8000.

4. Run the Frontend:
Open a new terminal window and navigate to the same project folder.

# Activate the same virtual environment
source venv/bin/activate

# Run the Streamlit app
streamlit run frontend.py


Your web browser should open with the app running locally and communicating with your backend server.

☁️ Deployment Architecture

This project uses a modern microservice architecture:

The Backend (FastAPI) is a heavyweight component with a large ML model. It's packaged in a Docker container and deployed to GCP Cloud Run.

The Frontend (Streamlit) is a Python-based user interface. It can be deployed to services like Streamlit Community Cloud. The Streamlit app communicates with the GCP backend via an HTTP API.

🤔 Challenges & What I Learned

This project was a huge learning experience! Here are some of the hurdles I faced:

Docker Incompatibilities: My first builds kept failing because of Python version issues. I learned how crucial it is to pin your Dockerfile to a stable version (like python:3.11-slim) to ensure builds are reproducible.

State Management in the Frontend: When I first built the UI, the old processed image would stick around when I uploaded a new one. This taught me about Streamlit's session_state and how to properly reset the application's state when an input changes.

Optimizing for Deployment: The default PyTorch library is huge! My first Docker images were over 2GB. I learned to use a CPU-only build of PyTorch for my deployment container, which cut the image size by more than half and made deployments much faster.

💡 Future Ideas

Add more effects like "Cartoonify" or "Grayscale Background".

Allow users to upload their own custom backgrounds.

Cache model predictions to make reapplying different effects to the same image instantaneous.

Thanks for checking out my project!