FROM abrammer/python_sql_demo

MAINTAINER Alan Brammer <someemail@gmail.com>

USER main


#USER main

# Update conda.
RUN conda install -c anaconda basemap=1.0.7

