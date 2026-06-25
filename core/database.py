import sqlite3
from contextlib import contextmanager
from config import DB_PATH


class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._create_tables()
        self._initialized = True
    
    def _create_tables(self):
        """Solo creamos la tabla de productos por ahora"""
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                descripcion TEXT NOT NULL,
                precio_unitario REAL NOT NULL,
                fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Índice para búsquedas rápidas por código
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_codigo 
            ON productos(codigo)
        """)
        self._conn.commit()
    
    @contextmanager
    def get_cursor(self):
        cursor = self._conn.cursor()
        try:
            yield cursor
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
    
    def execute(self, query, params=None):
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
    
    def fetch_all(self, query, params=None):
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def close(self):
        if self._conn:
            self._conn.close()
            Database._instance = None