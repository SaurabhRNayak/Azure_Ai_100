from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import config_
import os

credentials = CognitiveServicesCredentials(config_.config['Cognitive Services API key'])
client = ComputerVisionClient(
    endpoint=r"https://sherlockcog.cognitiveservices.azure.com/",
    credentials=credentials
)
f=open(".\images\Analysis_1.jpg","r")
print(f)
# image_analysis = client.analyze_image(f,visual_features=[VisualFeatureTypes.description,VisualFeatureTypes.tags])
# print(image_analysis)
# for tag in image_analysis.tags:
#     print(tag)