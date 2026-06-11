CREATE KEYSPACE IF NOT EXISTS museo_auditoria
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE museo_auditoria;