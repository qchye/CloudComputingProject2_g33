FROM registry.access.redhat.com/ubi8/python-38

LABEL name="Twitter Harvester"
LABEL description="Twitter harvester Python application"
LABEL maintainer="Shorye Chopra"

ENV HARVESTER_HOME /opt/harvester
ENV FILE_TO_RUN ""

COPY . $HARVESTER_HOME
WORKDIR $HARVESTER_HOME

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

# ENTRYPOINT ["python3"]

CMD ["sh", "-c", "python3 $FILE_TO_RUN"]
