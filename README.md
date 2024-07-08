# Medical Device Brochure Search - Question/Answer

## Objective : 
============================
* To Build a GPT system that will enable chat application for Medical Device Brochure Search in real-time.


* Packages Required
============================
pip install -r requirements.txt 


* Module Description
============================
	* train_index.py        - Train the model on document. This code will generate index at faiss_db folder.
	* app.py                - Code to launch the UI for inferencing
    * infer_user_query.py   - Searches the FAISS DB index and returns result
	* prompts.py            - Contains sample prompt
	* count_token.py		- Counts token & cost


* Docker Execution
============================
	* docker build --no-cache -t productgenie .
	* docker run -p 8082:8501 productgenie 
	* localhost:8082
    
# Deploying Docker in Azure
============================
* https://www.coachdevops.com/2019/12/how-to-upload-docker-images-to-azure.html
* Create a container registry
* Login to Azure ML Compute
* Connect to the Azure Compute and Code Repository
* docker build -t productgenie .
* sudo docker images (This will show all the images)
* Login to Azure Container Registry - sudo docker login strykerdscontainer.azurecr.io 
* Copy Paste Username and Password from "Access Keys"
* sudo docker tag productgenie strykerdscontainer.azurecr.io/productgenie
* sudo docker push strykerdscontainer.azurecr.io/productgenie
* Go to Container Registry > Repositories > streamlitapp > Latest > right click > deploy to AZURE APP SERVICE (Provide details and done).

Notes
=======
* View docker container : docker ps
* View docker images	: docker images
* Go inside docker container : docker exec -it <container_name/id> bash

