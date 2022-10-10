# Hotel_dashboard
   
## How to run dashboard and set up environment for development
1. `git clone https://github.com/KanokpatS/Weather_dasboard.git`
2. `git checkout -b {your branch}`
3. Build docker image

   `docker build -t hotel_dashboard .`
  
4. Build docker container

   `docker run -it --name hotel_dashboard -v $PWD\:/app -p 8080:8080 hotel_dashboard`
  
5. Run file app.py
  
    `python3 dashboard/app.py` 
   
## How to deploy dashboard
1. Use dockerfile in branch deployment
2. Build docker image

   `docker build -t hotel_dashboard .`
  
3. Test docker container

   `docker run -it --name hotel_dashboard -p 8080:8080 hotel_dashboard`
  
4. Login dokerhub

   `docker login`

5. Tag and push docker image into dokcerhub

   `docker tag hotel_dashboard {docker username}/hotel_dashboard:{version}`

   `docker push {docker username}hotel_dashboard:{version}`
  
6. Open Azure portal
7. Open Azure webapp
8. Launch a new web app service as shown below
9. Select subscription of your choice and resource group, we can name our web app anything as we like but needs to be unique as per Azure
10. Choose Linux as OS and proceed to next page for docker setting. From the publish option, let’s choose Docker container and go to next page
11. From this page, we need to choose Docker Hub as our source of image from Single container option.
12. Add setting follow 
   Use WEBSITES_PORT app settings with value of 3000 to expose to that port
   Use WEBSITES_CONTAINER_START_TIME_LIMIT and increase value to 400
