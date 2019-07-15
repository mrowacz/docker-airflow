FROM bde2020/spark-master:2.4.1-hadoop2.7

ENV HADOOP_CONF_DIR /spark/conf
ENV CONF_DIR /root/livy/conf
ENV SPARK_HOME /spark
ENV SPARK_CONF_DIR /spark/conf
ADD url ./
RUN pwd
RUN wget `cat url` -O livy.zip && unzip livy.zip && ls -lah && rm livy.zip && mv  apache-livy-0.6.0-incubating-bin livy
#ADD defaults/* defaults/
RUN mkdir -p /livy/logs
CMD ["/livy/bin/livy-server"]
