# Hotel_dashboard

## How to set up environment and run
1. Build docker image

  `docker build -t hotel_dashboard .`
  
2. Build docker container

  `docker run -it --name hotel_dashboard -v $PWD\:/app -p 8050:8050 hotel_dashboard`
  
  3. Run file app.py
  
   `python3 dashboard/app.py` 
