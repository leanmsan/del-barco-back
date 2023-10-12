use del_barco;

-- Insertar datos de ejemplo en la tabla 'proveedor'
INSERT INTO proveedor (nombre, mail, telefono, estado) 
VALUES 	('Proveedor 1', 'proveedor1@example.com', '123-456-7890', 'A'), 
		('Proveedor 2', 'proveedor2@example.com', '987-654-3210', 'B');

-- Insertar datos de ejemplo en la tabla 'insumo'
INSERT INTO insumo (descripcion, cantidad_disponible, tipo_medida, categoria, precio_unitario, proveedor)
VALUES
    ('Insumo 1', 100, 'Unid', 'Categoría A', 10.50, 'Proveedor 1'),
    ('Insumo 2', 200, 'Unid', 'Categoría B', 15.75, 'Proveedor 2');