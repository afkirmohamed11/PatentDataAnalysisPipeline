FROM mongo:latest

COPY src/init-scripts/cipo.json /tmp/cipo.json
COPY src/init-scripts/espacenet.json /tmp/espacenetjson
COPY src/init-scripts/googlepatent.json /tmp/googlepatent.json
COPY src/init-scripts/uspto.json /tmp/uspto.json
COPY src/init-scripts/epo.json /tmp/epo.json

COPY src/init-scripts/importscript.sh /docker-entrypoint-initdb.d/

ADD src/init-scripts/init.js /docker-entrypoint-initdb.d/

