DELIMITER //

CREATE PROCEDURE SacarCostos()
BEGIN
    SELECT * FROM VehiculoXEspacioEstacionamiento as vee;
	SELECT v.id, sum(vee.horaFinal - vee.horaInicio) as TotalDeHoras, sum(vee.horaFinal - vee.horaInicio)*tv.precioXHora CostoTotal
	FROM VehiculoXEspacioEstacionamiento as vee
	join Vehiculo v on vee.idVehiculo = v.id
	join EspacioEstacionamiento ee on vee.idEspacioEstacionamiento = ee.id
	join TipoVehiculo tv on tv.id = v.idTipoVehiculo
	group by v.id; 
END //

DELIMITER ;
