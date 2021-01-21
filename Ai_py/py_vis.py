import config_
import os
import requests
import json
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# give the path of the images folder 
image_path ='.\images'

def store(container_name,img_path,key,connect_str,acc_name):

    # Create a container in azure storage if not created (comment the code if already created mannually)
    #----
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # container_name = container_name + str(uuid.uuid4())
    container = ContainerClient.from_connection_string(connect_str, container_name)
    
    # Container check whether it already exists
    try:
        container_properties = container.get_container_properties()
        container_client = ContainerClient.from_connection_string(conn_str=connect_str, container_name=container_name)

    except Exception as e:
        # Create the container
        container_client = blob_service_client.create_container(container_name)
    
    #----

    # block_blob_service = BlockBlobService(account_name=acc_name,account_key=key)
    blob_name=os.path.basename(img_path)
    # block_blob_service.create_blob_from_path(container_client, blob_name, img_path)
    
    # Blob check if the blob already exists
    blob_client = container_client.get_blob_client(blob_name)
    if not (blob_client.exists()):
        with open(img_path, "rb") as data:
            blob_client.upload_blob(data, blob_type="BlockBlob")
    

# Vision analyze api usage
def analyze(key,img,path):
    headers = {'Ocp-Apim-Subscription-Key': key,'Content-Type':'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    data = img
    response = requests.post(path, headers=headers,
                            params=params, data=data)
    response.raise_for_status()
    analysis = response.json()
    json_value=json.dumps(response.json())
    # Gives the complete response
    print(json.dumps(response.json())) ## working on module to save the data in cosmosdb
#     image_caption = analysis["description"]["captions"][0]["text"].capitalize()
#     print(image_caption)


if __name__ == "__main__":
    subs_key=config_.config['Cognitive Services API key']
    cog_url=config_.config['Cognitive Services API Url']+'/vision/v3.1/analyze'
    azstore_key=config_.config['Azure Storage Key']
    azstore_connect_str=config_.config['Azure Storage Connection String']
    azstore_name=config_.config['Azure Storage name']

    path_=os.path.abspath(image_path)
    for files in os.listdir(path_):
        if os.path.isfile(os.path.join(path_,files)):
            if files.split('.')[-1] in ['jpg','png','jpeg']:
                p=os.path.join(path_,files)
                store('imagespy',p,azstore_key,azstore_connect_str,azstore_name)
                img_=open(p,'rb')
                img=img_.read()
                print(files)
                analyze(subs_key,img,cog_url)


