CREATE DATABASE del_barco;
USE del_barco;
CREATE TABLE proveedor(
						idProveedor INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        nombre VARCHAR(60),
                        mail VARCHAR(80),
                        telefono VARCHAR(20),
                        estado CHAR);

CREATE INDEX idx_prov_nombre ON proveedor (nombre);

CREATE TABLE insumo(
					idInsumo INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    descripcion VARCHAR(80),
                    cantidad_disponible INT,
                    tipo_medida VARCHAR(5),
                    categoria VARCHAR(20),
                    precio_unitario DECIMAL(10,2),
                    proveedor VARCHAR(60),
                    FOREIGN KEY (proveedor) REFERENCES proveedor(nombre));
                    

CREATE TABLE entrada(
						idEntrada INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        idProveedor INT,
                        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                        montoTotal DECIMAL(10,2),
                        FOREIGN KEY(idProveedor) REFERENCES proveedor(idProveedor));
                        
CREATE TABLE entradaDetalle(
								idEntrada INT NOT NULL,
                                idInsumo INT NOT NULL,
                                cantidad INT NOT NULL,
                                precioUnitario DECIMAL(10,2),
                                PRIMARY KEY(idEntrada, idInsumo),
                                FOREIGN KEY(idInsumo) REFERENCES insumo(idInsumo));

CREATE TABLE salida(
						idSalida INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        fecha DATETIME DEFAULT CURRENT_TIMESTAMP);
                        
CREATE TABLE salidaDetalle(
								idSalida INT NOT NULL,
                                idInsumo INT NOT NULL,
                                cantidad INT NOT NULL,
                                PRIMARY KEY(idSalida, idInsumo),
                                FOREIGN KEY(idInsumo) REFERENCES insumo(idInsumo));

CREATE TABLE recetas(
								idReceta INT NOT NULL,
                                nombre VARCHAR(50) NOT NULL,
                                tipo VARCHAR(50) NOT NULL,
                                PRIMARY KEY(idReceta));

CREATE TABLE recetaDetalle(
								idReceta INT NOT NULL,
                                idInsumo INT NOT NULL,
                                cantidad INT NOT NULL,
                                tipo_medida VARCHAR(5),
                                PRIMARY KEY(idReceta, idInsumo),
                                FOREIGN KEY(idInsumo) REFERENCES insumo(idInsumo));

CREATE TABLE punto_reposicion (
    idPuntoReposicion INT NOT NULL PRIMARY KEY,
    idInsumo INT NOT NULL,
    punto_reposicion INT,
    fecha_ultima_compra DATE, 
    FOREIGN KEY (idInsumo) REFERENCES insumo(idInsumo)
);


CREATE TABLE registro_alertas_stock (
    idAlerta INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    descripcion_alerta VARCHAR(25),
    fecha_alerta DATETIME DEFAULT CURRENT_TIMESTAMP
);

                                
                                
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
    IF NEW.cantidad_disponible < (SELECT punto_reposicion FROM punto_reposicion WHERE idInsumo = NEW.idInsumo) THEN
        INSERT INTO registro_alertas_stock (descripcion_alerta) VALUES ('Stock por debajo del punto de reposición');
    END IF;
END //
DELIMITER ;

/*---------------------------------------------------------------
DELIMITER //
CREATE TRIGGER trRestarStock
AFTER INSERT ON movimientoDetalle
FOR EACH ROW
BEGIN
    DECLARE cantidadSalida INT;
    DECLARE stockActual INT;
    
    SELECT cantidad INTO cantidadSalida FROM movimientoDetalle WHERE idMovimiento = NEW.idMovimiento AND idProducto = NEW.idProducto;
    SELECT StockDisponible INTO stockActual FROM producto WHERE IdProducto = NEW.idProducto;
    
    IF cantidadSalida <= stockActual THEN
        UPDATE producto SET StockDisponible = stockActual - cantidadSalida WHERE IdProducto = NEW.idProducto;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente para realizar la salida';
    END IF;
END //
DELIMITER ;

---------------------------------------------------------------*/



