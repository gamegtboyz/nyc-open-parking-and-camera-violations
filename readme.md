## DATA SOURCE & QUESTIONS

We gathered this information from the following link:
    https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89/about_data


## INSTALLATION GUIDE

็Here's how to install Apache Airflow through Docker Desktop, and how to maintenance it.

After install Docker Desktop, open VScode and WSL terminal. Then, move to your desired working directory (in this case we named it 'final-projects') and put the following command.
1. curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'    # to download default.yaml file, which include the pack of software i.e. postgres, redis, and airflow.
2. mkdir -p ./dags ./logs ./plugins         # setup airflow directories
3. echo -e "AIRFLOW_UID=$(id -u)" > .env    # set up the permissions of curent user to virtual environment.


## USERS' GUIDE

### How to kickstart your container
Right after you fork this project, you could initialize and start running container using the following commands.
1. docker-compose up airflow-init       # initialize Airflow
2. docker-compose up                    # start running Airflow. you could access airflow UI at this point using localhost:8080 with username == airflow and password == airflow

### How to access your airflow webUI, and how to trigger your dag.
After kickstarting your container, you could check the status from webserver's container. If there's no error, you could access Airflow's webbased UI using localhost:8080. Then used the default username == airflow and password == airflow to login.

Then, you could find the project's dag called 'my-opcv-projects-dag' among the list of example dags. Click into them and you could observe the running stats. Most important, you could manually run the dag using 'trigger DAG' button on the screen's top-right end.

Then you could obtain the running result from the ~/logs/dag_id=my-opcv-projects-dag

### How to access running output
If all tasks in dag run successfully, dag should return 2 tangible outputs, which is data called 'nyc-collisions.csv' and the table in airlow/collisions database. Here's how to access it through VScode.

##### how to access 'nyc-collisions.csv'
After the successful DAG run, we could access those .csv file from ~/includes/outputs folder.

##### how to access db file in database
After the successful DAG run, we should access the database through postgresql's container using the following command, respectively.
1. docker exec -it final-projects-postgres-1 bash   # to access the container's bash terminal. If everything's right, you'll be able to access postgresql's container terminal.
2. psql -U airflow d- airflow   # to enter SQL shell mode with uername == airflow and databased named 'airflow'. We will redefine it later. But right now we could use SQL query to extract the data from table called 'collisions'
3. SELECT * from collisions LIMIT 10;   # extract the first 10 rows of data.



## MAINTENANCE GUIDE
### Webserver is not running
In case of localhost:8080 doesn't load (this happended on my PC when reopen the computer), you could use theis following commands to troubleshoot the issues
1. docker restart final-projects-airflow-webserver-1       # to restart the container

in case of command per 1 doesn't work, please use the following command respectively to reinitiate the airflow
1. docker-compose down --volumes --remove-orphans
2. docker-compose up airflow-init
3. docker-compose up -d

### Docker Image Modifications
1. located the Dockerfile
2. Insert the following commands, in this case we need to install matplotlib.
    FROM apache/airflow:2.10.4
    RUN pip install matplotlib
    ...
3. use the command as follows to build up to build up docker image, in this case we named it as my-de01-airflow.
    docker build -t my-de01-airflow .
4. go to .yaml file and check the x-airflow-common > image section to make sure if airflow are built up with on our customised image.
    image: my-de01-airflow