from typing import Optional
from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
import logging
import json

logger = logging.getLogger("cassandra")

class CassandraConfig:
    def __init__(self):
        self.cluster: Optional[Cluster] = None
        self.session: Optional[Session] = None
        self.keyspace = "museo_auditoria"

    def conectar(self):
        """Inicializa la conexión segura hacia la nube de DataStax Astra DB"""
        try:
            # 1. Leer el archivo JSON con tus credenciales secretas
            with open("cluster_museo_uneg-token.json") as f:
                secrets = json.load(f)
            
            CLIENT_ID = secrets["clientId"]
            CLIENT_SECRET = secrets["secret"]
            
            # 2. Configurar la autenticación segura de la nube
            auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
            
            # 3. Apuntar al archivo zip de conexión (Secure Connect Bundle)
            cloud_config = {
                'secure_connect_bundle': 'secure-connect-cluster-museo-uneg.zip'
            }
            
            # 4. Conectar al clúster remoto en internet
            self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = self.cluster.connect()
            
            # 5. Posicionarnos en el Keyspace que creaste en la nube
            self.session.set_keyspace(self.keyspace)
            print(f"[AstraDB] ¡Conexión en la nube exitosa en el keyspace: '{self.keyspace}'!")
            
            row = self.session.execute("select release_version from system.local").one()
            if row:
                print(f"🚀 Versión oficial de tu Cassandra en la nube: {row[0]}")
            else:
                print("⚠️ Se conectó, pero no se pudo leer la versión.")
            
        except Exception as e:
            logger.error(f"Error crítico al conectar con DataStax Astra DB en la nube: {e}")
            raise e

    def cerrar(self):
        """Cierra la conexión de red de forma limpia"""
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
        print("[AstraDB] Conexión en la nube cerrada de forma segura.")

conexion_cassandra = CassandraConfig()