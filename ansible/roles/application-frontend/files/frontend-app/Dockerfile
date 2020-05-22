FROM registry.access.redhat.com/ubi8/python-38

LABEL name="Twitter Harvester"
LABEL description="Frontend Python application"
LABEL maintainer="Shorye Chopra"

ENV FRONTEND /opt/frontend
ENV FILE_TO_RUN ""

USER root

ADD app/ $FRONTEND
WORKDIR ${FRONTEND}

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

RUN chown -R 1001:0 ${FRONTEND} && \
    chmod -R ug+rwx ${FRONTEND} && \
    rpm-file-permissions

USER 1001

CMD ["sh", "-c", "python3 $FILE_TO_RUN"]