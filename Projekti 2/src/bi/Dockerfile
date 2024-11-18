FROM sitespeedio/node:ubuntu-22-04-nodejs-20.11.1
ARG WORKSPACE_DIR=/evidence-workspace

# Split apt-get update and install to debug issues
RUN apt-get update && \
    apt-get install -y curl wget nano git xdg-utils && \
    npm install -g degit && \
    mkdir -p ${WORKSPACE_DIR} && \
    mkdir -p /evidence-bin

# Clean up APT cache only after successful installation
RUN rm -rf /var/lib/apt/lists/*

WORKDIR ${WORKSPACE_DIR}

COPY ./src/bi/bootstrap.sh /evidence-bin/bootstrap.sh

CMD [ "bash", "/evidence-bin/bootstrap.sh" ]
