FROM registry.access.redhat.com/ubi8/nodejs-12

LABEL name="CouchDB Views"
LABEL description="Container for deploying Views to CouchDB"
LABEL maintainer="Shorye Chopra"

ENV DBVIEWS /opt/analysis
ADD analysis/ ${DBVIEWS}

USER root
RUN npm install -g grunt grunt-couch grunt-cli

COPY run.sh ${DBVIEWS}
RUN chown -R 1001:0 ${DBVIEWS} && chmod -R ug+rwx ${DBVIEWS} && \
    rpm-file-permissions
    
RUN chmod +x ${DBVIEWS}/run.sh

WORKDIR ${DBVIEWS}
RUN npm install

USER 1001
  
ENTRYPOINT [ "/opt/analysis/run.sh" ]