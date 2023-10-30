
CREATE DATABASE del_barco;
USE del_barco;

CREATE TABLE proveedor (
    idProveedor INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60) UNIQUE NOT NULL,
    mail VARCHAR(80),
    telefono VARCHAR(20),
    estado CHAR
);
CREATE INDEX idx_prov_nombre ON proveedor (nombre);

CREATE TABLE insumo (
    idInsumo INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(80) UNIQUE NOT NULL,
    cantidad_disponible INT,
    tipo_medida VARCHAR(10),
    categoria VARCHAR(20),
    precio_unitario DECIMAL(10 , 2 ),
    proveedor VARCHAR(60),
    FOREIGN KEY (proveedor)
        REFERENCES proveedor (nombre)
);
                    

CREATE TABLE entrada (
    idEntrada INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    idProveedor INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    montoTotal DECIMAL(10 , 2 ),
    FOREIGN KEY (idProveedor)
        REFERENCES proveedor (idProveedor)
);
                        
CREATE TABLE entradaDetalle (
    idEntrada INT NOT NULL,
    idInsumo INT NOT NULL,
    cantidad INT NOT NULL,
    precioUnitario DECIMAL(10 , 2 ),
    PRIMARY KEY (idEntrada , idInsumo),
    FOREIGN KEY (idInsumo)
        REFERENCES insumo (idInsumo),
	FOREIGN KEY (idEntrada)
        REFERENCES entrada (idEntrada)
);

CREATE TABLE salida (
    idSalida INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);
                        
CREATE TABLE salidaDetalle (
    idSalida INT NOT NULL,
    idInsumo INT NOT NULL,
    cantidad INT NOT NULL,
    PRIMARY KEY (idSalida , idInsumo),
    FOREIGN KEY (idInsumo)
        REFERENCES insumo (idInsumo),
	FOREIGN KEY (idSalida)
        REFERENCES salida (idSalida)
);

CREATE TABLE receta (
    idReceta INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    PRIMARY KEY (idReceta)
);
CREATE INDEX idx_rec_nombre ON receta (nombre);

CREATE TABLE recetaDetalle (
    idReceta INT NOT NULL,
    idInsumo INT NOT NULL,
    cantidad INT NOT NULL,
    tipo_medida VARCHAR(10),
    PRIMARY KEY (idReceta , idInsumo),
    FOREIGN KEY (idInsumo)
        REFERENCES insumo (idInsumo),
	FOREIGN KEY (idReceta)
        REFERENCES receta (idReceta)
);

CREATE TABLE coccion (
    idCoccion INT NOT NULL AUTO_INCREMENT,
    fechaCoccion DATE NOT NULL,
    idReceta INT NOT NULL,
    volumenProducido DECIMAL(10 , 2 ) NOT NULL,
    PRIMARY KEY (idCoccion),
    FOREIGN KEY (idReceta)
        REFERENCES receta (idReceta)
);


CREATE TABLE punto_reposicion (
    idPuntoReposicion INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    idInsumo INT NOT NULL,
    punto_reposicion INT,
    fecha_ultima_compra DATE,
    FOREIGN KEY (idInsumo)
        REFERENCES insumo (idInsumo)
);

CREATE TABLE registro_alertas_stock (
    idAlerta INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    descripcion_alerta VARCHAR(100),
    fecha_alerta DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- Datos de prueba para la tabla proveedor
INSERT INTO proveedor (nombre, mail, telefono, estado) VALUES
('Proveedor A', 'proveedorA@mail.com', '123-456-7890', 'A'),
('Proveedor B', 'proveedorB@mail.com', '987-654-3210', 'B'),
('Proveedor C', 'proveedorC@mail.com', '111-222-3333', 'C');

-- Datos de prueba para la tabla insumo
INSERT INTO insumo (descripcion, cantidad_disponible, tipo_medida, categoria, precio_unitario, proveedor) VALUES
('Insumo 1', 100, 'Unidad', 'Categoria A', 10.50, 'Proveedor A'),
('Insumo 2', 200, 'Unidad', 'Categoria B', 5.75, 'Proveedor B'),
('Insumo 3', 50, 'Unidad', 'Categoria A', 15.25, 'Proveedor C');

-- Datos de prueba para la tabla entrada
INSERT INTO entrada (idProveedor, montoTotal) VALUES
(1, 105.00),
(2, 80.25),
(3, 100.00);

-- Datos de prueba para la tabla entradaDetalle
INSERT INTO entradaDetalle (idEntrada, idInsumo, cantidad, precioUnitario) VALUES
(1, 1, 10, 10.50),
(1, 2, 20, 5.75),
(2, 2, 15, 5.75),
(3, 3, 5, 15.25);

-- Datos de prueba para la tabla salida
INSERT INTO salida () VALUES (), (), ();

-- Datos de prueba para la tabla salidaDetalle
INSERT INTO salidaDetalle (idSalida, idInsumo, cantidad) VALUES
(1, 1, 2),
(1, 2, 5),
(2, 2, 3),
(2, 3, 2),
(3, 1, 3),
(3, 3, 1);

-- Datos de prueba para la tabla receta
INSERT INTO receta (idReceta, nombre, tipo) VALUES
(1, 'Receta 1', 'Tipo A'),
(2, 'Receta 2', 'Tipo B');

-- Datos de prueba para la tabla recetaDetalle
INSERT INTO recetaDetalle (idReceta, idInsumo, cantidad, tipo_medida) VALUES
(1, 1, 3, 'Unidad'),
(1, 2, 2, 'Unidad'),
(2, 2, 4, 'Unidad'),
(2, 3, 5, 'Unidad');

-- Datos de prueba para la tabla coccion
INSERT INTO coccion (fechaCoccion, idReceta, volumenProducido) VALUES
('2023-10-15', 1, 50.00),
('2023-10-16', 2, 30.00),
('2023-10-17', 1, 60.00);

-- Datos de prueba para la tabla punto_reposicion con 'idPuntoReposicion' auto incremental
INSERT INTO punto_reposicion (idInsumo, punto_reposicion, fecha_ultima_compra) VALUES
(1, 20, '2023-10-12'),
(2, 10, '2023-10-10'),
(3, 15, '2023-10-11');

-- Datos de prueba para la tabla registro_alertas_stock
INSERT INTO registro_alertas_stock (descripcion_alerta) VALUES
('Insumo ID: 1, Nombre: Insumo 1'),
('Insumo ID: 2, Nombre: Insumo 2');

DELIMITER //
CREATE TRIGGER trEntrada
AFTER INSERT ON entradaDetalle
FOR EACH ROW
BEGIN
    -- Actualiza la cantidad_disponible en la tabla 'insumo'
    UPDATE insumo SET cantidad_disponible = cantidad_disponible + NEW.cantidad WHERE idInsumo = NEW.idInsumo;

    -- Actualiza la fecha_ultima_compra en la tabla 'punto_reposicion' con la fecha actual
    UPDATE punto_reposicion SET fecha_ultima_compra = CURDATE() WHERE idInsumo = NEW.idInsumo;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER trSalidaDetalle
AFTER INSERT ON salidaDetalle
FOR EACH ROW
BEGIN
	UPDATE insumo SET cantidad_disponible = cantidad_disponible - NEW.cantidad WHERE idInsumo = NEW.idInsumo;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER tr_alerta_punto_reposicion
AFTER UPDATE ON insumo
FOR EACH ROW
BEGIN
    DECLARE insumo_descripcion VARCHAR(100);
    SET insumo_descripcion = CONCAT('Insumo ID: ', NEW.idInsumo, ', Nombre: ', (SELECT descripcion FROM insumo WHERE idInsumo = NEW.idInsumo));
    
    IF NEW.cantidad_disponible < (SELECT punto_reposicion FROM punto_reposicion WHERE idInsumo = NEW.idInsumo) THEN
        INSERT INTO registro_alertas_stock (descripcion_alerta) VALUES (insumo_descripcion);
    END IF;
END //
DELIMITER ;


DELIMITER //

CREATE TRIGGER tr_descuento_insumos_despues_insert
AFTER INSERT ON coccion
FOR EACH ROW
BEGIN
    -- Obtener el ID de la receta asociada a la cocción
    DECLARE receta_id INT;
    SET receta_id = NEW.idReceta;
    
    -- Realizar el descuento de cantidad en la tabla insumo
    UPDATE insumo i
    JOIN recetaDetalle rd ON i.idInsumo = rd.idInsumo AND rd.idReceta = receta_id
    SET i.cantidad_disponible = i.cantidad_disponible - rd.cantidad;
    
END;
//

DELIMITER ;


