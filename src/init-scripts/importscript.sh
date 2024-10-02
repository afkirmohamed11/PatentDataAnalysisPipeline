#!/bin/bash

mongoimport --db='cipo' --collection='datacipo' --file='/tmp/cipo.json' --jsonArray --username='admin' --password='admin' --authenticationDatabase=admin
mongoimport --db='espacenet' --collection='dataespacenet' --file='/tmp/espacenetjson' --jsonArray --username='admin' --password='admin' --authenticationDatabase=admin
mongoimport --db='googlepatent' --collection='datagooglepatent' --file='/tmp/googlepatent.json' --jsonArray --username='admin' --password='admin' --authenticationDatabase=admin
mongoimport --db='uspto' --collection='datauspto' --file='/tmp/uspto.json' --jsonArray --username='admin' --password='admin' --authenticationDatabase=admin
mongoimport --db='epo' --collection='dataepo' --file='/tmp/epo.json' --jsonArray --username='admin' --password='admin' --authenticationDatabase=admin