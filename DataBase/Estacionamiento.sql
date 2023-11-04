use estacionamiento;
#SELECT USER(), CURRENT_USER();

drop table VehiculoXEspacioEstacionamiento;
drop table EspacioEstacionamiento;
drop table Vehiculo;
drop table TipoVehiculo;


create table TipoVehiculo(
    id int Primary key,
    tipo varchar(255),
    precioXHora int
);

create table Vehiculo(
    id int Primary key,
    idTipoVehiculo int,
    marca varchar(255),
	foreign key(idTipoVehiculo) references TipoVehiculo(id)
);

create table EspacioEstacionamiento(
	id int Primary key
);

create table VehiculoXEspacioEstacionamiento(
	idVehiculo int,
	idEspacioEstacionamiento int,
	horaInicio int,
	horaFinal int,
    foreign key (idVehiculo) references Vehiculo(id),
	foreign key (idEspacioEstacionamiento) references EspacioEstacionamiento(id)
);


insert into TipoVehiculo(id, tipo, precioXHora)
values(1, 'Motocicleta', 250),
(2, 'Carro', 500),
(3, 'Camion', 1000);

insert into Vehiculo(id, idTipoVehiculo,marca)
values(1 , 2, 'Toyota'),
(2, 1, 'BMW'),
(3, 3, 'Suzuki');

insert into EspacioEstacionamiento(id)
values(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);
insert into VehiculoXEspacioEstacionamiento(idVehiculo, idEspacioEstacionamiento, horaInicio, horaFinal)
values( 1, 2, 5, 10),
(3, 3, 11, 15),
(2, 2, 11, 15);

SELECT * FROM VehiculoXEspacioEstacionamiento as vee;
SELECT v.id, sum(vee.horaFinal - vee.horaInicio) as TotalDeHoras, sum(vee.horaFinal - vee.horaInicio)*tv.precioXHora CostoTotal
FROM VehiculoXEspacioEstacionamiento as vee
join Vehiculo v on vee.idVehiculo = v.id
join EspacioEstacionamiento ee on vee.idEspacioEstacionamiento = ee.id
join TipoVehiculo tv on tv.id = v.idTipoVehiculo
group by v.id; 