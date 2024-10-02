// Initialize database connections
const db1 = db.getSiblingDB('cipo');
const db2 = db.getSiblingDB('googlepatent');
const db3 = db.getSiblingDB('uspto');
const db4 = db.getSiblingDB('espacenet');
const db5 = db.getSiblingDB('epo');


// Create collections in each database
db1.createCollection('datacipo');
db2.createCollection('datagoogle');
db3.createCollection('datauspto');
db4.createCollection('dataespacenet');
db5.createCollection('dataepo');

print('Initialization script completed successfully.');
