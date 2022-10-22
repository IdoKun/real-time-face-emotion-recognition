## Import the data and store it in data/

# Imports
from roboflow import Roboflow
from dotenv import load_dotenv
import sys
import os
import shutil
load_dotenv()

try :
    API_KEY=os.environ.get("API_KEY")
    print("API_KEY loaded")
except :
    print("Failed to load an APIKEY from .env")
    sys.exit()


def load_from_robotflow(project_name="google-scraping-dataset",version=4,):
    rf = Roboflow(api_key=API_KEY)
    project = rf.workspace("facial-emotion-recognition").project(project_name)
    dataset_name, data_folder = project_name, os.path.join("rtfer","data")
    if not dataset_name in os.listdir(data_folder):
        os.mkdir(os.path.join(data_folder,dataset_name))
    location=os.path.join(data_folder,dataset_name)
    print(location)
    dataset = project.version(version).download("yolov5",location=os.path.join(data_folder,dataset_name) )

load_from_robotflow()
