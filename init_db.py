import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    host = os.getenv("SUPABASE_DB_HOST")
    port = os.getenv("SUPABASE_DB_PORT")
    dbname = os.getenv("SUPABASE_DB_NAME")
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")

    print("Conectando a la base de datos...")
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    cursor = conn.cursor()

    schema = """
    DROP TABLE IF EXISTS venta_detalle CASCADE;
    DROP TABLE IF EXISTS ventas CASCADE;
    DROP TABLE IF EXISTS productos CASCADE;
    DROP TABLE IF EXISTS proveedores CASCADE;
    DROP TABLE IF EXISTS usuarios CASCADE;

    CREATE TABLE usuarios (
        id SERIAL PRIMARY KEY,
        usuario VARCHAR(100) UNIQUE NOT NULL,
        contraseña VARCHAR(100) NOT NULL,
        tipo_usuario VARCHAR(50) NOT NULL
    );

    CREATE TABLE proveedores (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    );

    CREATE TABLE productos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        proveedor_id INT REFERENCES proveedores(id) ON DELETE SET NULL,
        cantidad INT NOT NULL DEFAULT 0,
        precio DECIMAL(10, 2) NOT NULL
    );

    CREATE TABLE ventas (
        id SERIAL PRIMARY KEY,
        empleado_id INT REFERENCES usuarios(id) ON DELETE SET NULL,
        descuento DECIMAL(5, 2) DEFAULT 0,
        total DECIMAL(10, 2) DEFAULT 0,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE venta_detalle (
        id SERIAL PRIMARY KEY,
        venta_id INT REFERENCES ventas(id) ON DELETE CASCADE,
        producto_id INT REFERENCES productos(id) ON DELETE SET NULL,
        cantidad INT NOT NULL,
        subtotal DECIMAL(10, 2) NOT NULL
    );
    """
    
    seed_data = """
    INSERT INTO usuarios (usuario, contraseña, tipo_usuario) VALUES 
    ('admin', 'admin', 'admin'),
    ('empleado1', 'empleadopass', 'empleado'),
    ('empleado2', 'empleadopass', 'empleado');

    INSERT INTO proveedores (nombre) VALUES 
    ('Proveedor A'),
    ('Proveedor B'),
    ('Distribuidora Central');

    INSERT INTO productos (nombre, proveedor_id, cantidad, precio) VALUES 
    ('Producto 1', 1, 50, 1500.00),
    ('Producto 2', 1, 30, 2500.50),
    ('Producto 3', 2, 100, 500.00),
    ('Producto 4', 3, 20, 10000.00);
    """

    print("Creando tablas e insertando datos de prueba...")
    cursor.execute(schema)
    cursor.execute(seed_data)
    conn.commit()
    cursor.close()
    conn.close()
    print("¡Base de datos inicializada y poblada con éxito!")

if __name__ == '__main__':
    init_db()