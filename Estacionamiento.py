import mysql.connector

from BaseDeDatos import ConexionBaseDatos

class Vehiculo:
    def __init__(self, placa, idTipo=0, marca=""): #tipo 1 motocicleta, 2 carro , 3 camion
        self.idTipo = idTipo
        self.placa = placa
        self.marca = marca

    def agregarVehiculo(self):
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        consulta = "insert into Vehiculo(id, idTipoVehiculo, marca) values(%s , %s, %s)"
        mi_conexion.insertarVehiculo(consulta, self.placa, self.idTipo, self.marca)
        mi_conexion.desconectar()
        print("Se ha registrado exitosamente")
    def __eq__(self, other):
        if isinstance(other, Vehiculo):
            return self.placa == other.placa
        return False
    
    def __str__(self):                                                                      #Sobrecarga de metodo
        return f"Vehiculo: Placa - {self.placa}, Tipo - {self.idTipo}, Marca - {self.marca}"

class Motocicleta(Vehiculo):
    def __init__(self, placa, marca):
        super().__init__(placa, 1, marca)

    def __str__(self):                                                                      #Sobrecarga de metodo
        return f"Motocicleta: Placa - {self.placa}, Marca - {self.marca}"

class Carro(Vehiculo):
    def __init__(self, placa, marca):
        super().__init__(placa, 2, marca)

    def __str__(self):                                                                      #Sobrecarga de metodo
        return f"Carro: Placa - {self.placa}, Marca - {self.marca}"

class Camion(Vehiculo):
    def __init__(self, placa, marca):
        super().__init__(placa, 3, marca)

    def __str__(self):                                                                      #Sobrecarga de metodo
        return f"Camión: Placa - {self.placa}, Marca - {self.marca}"



class EspacioEstacionamiento:
    def __init__(self, id):
        self.id = id
        self.vehiculo_apartado = None
        

    def verificar_disponibilidad(self, hora_inicio, hora_fin):
        mi_conexion = ConexionBaseDatos(self.id)
        mi_conexion.conectar()
        resultados = mi_conexion.ejecutar_consulta_where("SELECT * FROM VehiculoXEspacioEstacionamiento as vee where vee.idEspacioEstacionamiento = %s")
        for fila in resultados:
            #if self.vehiculo_apartado[0] == int(fila["idVehiculo"])
            if(hora_inicio <= fila[3] and hora_fin >= fila[2]) or (hora_fin >= fila[2] and hora_inicio <= fila[3]):
                mi_conexion.desconectar()
                return False
        mi_conexion.desconectar()
        return True
    def apartar_vehiculo(self, vehiculo, hora_inicio, hora_fin):
        self.vehiculo_apartado = (vehiculo.placa, (hora_inicio, hora_fin))
        if self.verificar_disponibilidad(hora_inicio, hora_fin):
            return True
        return False

class Estacionamiento:
    def __init__(self, num_espacios):
        self.espacios = [EspacioEstacionamiento(x+1) for x in range(num_espacios)]


    def calcular_costoTotal(self, placa):
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        resultados = mi_conexion.ejecutar_consulta("CALL SacarCostos();")
        for fila in resultados:
            if fila[0] == placa:
                totalHoras = fila[1]
                costo = fila[2]
                break
        print(f"Usted ha apartado {totalHoras} horas el total, asi que debe {costo}\n")


    def buscar_espacio_disponible(self, vehiculo, hora_inicio, hora_fin):
        espacios_disponibles = []
        for i, espacio in enumerate(self.espacios, start=1):
            if espacio.verificar_disponibilidad(hora_inicio, hora_fin):
                espacios_disponibles.append(i)
                print("_______")
                print(f"|  {i}  |" if i/10<1 else f"| {i}  |")
                print("|     |")
                print("|     |")
                print("-------")

            else:
                print("_______")
                print("| NO  |")
                print("|     |")
                print("|     |")
                print("-------")
                
        if espacios_disponibles:

            print("Espacios disponibles:", espacios_disponibles)
            seleccion = int(input("Elige un espacio de estacionamiento: "))
            if 1 <= seleccion <= len(self.espacios):
                espacio_elegido = self.espacios[seleccion - 1]
                if espacio_elegido.apartar_vehiculo(vehiculo, hora_inicio, hora_fin):
                    mi_conexion = ConexionBaseDatos()
                    mi_conexion.conectar()
                    consulta = "INSERT INTO VehiculoXEspacioEstacionamiento(idVehiculo, idEspacioEstacionamiento, horaInicio, horaFinal) VALUES (%s, %s, %s, %s)"
                    mi_conexion.insertarApartado(consulta, vehiculo.placa, seleccion, hora_inicio, hora_fin)
                    mi_conexion.desconectar()
                    print(f"Espacio {seleccion} apartado con éxito.")
                else:
                    print(f"No se pudo apartar el espacio {seleccion} debido a un choque de horarios.")
            else:
                print("Espacio no válido.")
        else:
            print("No hay espacios de estacionamiento disponibles en este momento.")
            


class Principal:

    def main(self):
        estacionamiento = Estacionamiento(num_espacios=10)  # Crear un estacionamiento con 10 espacios

        while True:
            if self.imprimirMenuPrincipal(estacionamiento):
                break
                
            
    def existeVehiculo(self, vehiculoAcomparar):
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        resultados = mi_conexion.ejecutar_consulta("select * from Vehiculo")
        for fila in resultados:
            if Vehiculo(fila[0], fila[1], fila[2]) == vehiculoAcomparar:  #Uso de la sobrecarga
                return True
        return False

    def imprimirAgregarVehiculo(self):
        placa = int(input("Ingrese el numero de placa: "))
        marca = input("Ingrese la marca: ")
        print("1) Motocicleta \n2) Carro \n3) Camion")
        tipoVehiculo = int(input("Seleccione tipo de vehiculo: "))
        if tipoVehiculo == 1:
            newVehiculo = Motocicleta(placa, marca)
        elif tipoVehiculo == 2:
            newVehiculo = Carro(placa, marca)
        elif tipoVehiculo == 3:
            newVehiculo = Camion(placa, marca)
        if self.existeVehiculo(newVehiculo):
            print(f"El vehiculo {newVehiculo} ya se encuentra registrado.") #Uso de la sobrecarga
            return
        newVehiculo.agregarVehiculo()

    def imprimirVerTodosApartados(self):
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        consulta = """SELECT vee.id, v.id as placa, case 
                        when v.idTipoVehiculo = 1 then 'Motocicleta'
                        when v.idTipoVehiculo = 2 then 'Carro'
                        when v.idTipoVehiculo = 3 then 'Camion'
                        end as Tipo
                        , v.marca, idEspacioEstacionamiento, horaInicio, horaFinal 
                        FROM VehiculoXEspacioEstacionamiento vee 
                        join Vehiculo v on v.id = vee.idVehiculo 
                        join EspacioEstacionamiento ee on ee.id = vee.idEspacioEstacionamiento
                        order by v.id"""
        resultados = mi_conexion.ejecutar_consulta(consulta)
        placa = 0
        for fila in resultados:
            if fila[1] != placa:
                placa = fila[1]
                print(f"\nPlaca: {fila[1]} | Tipo: {fila[2]} | Marca: {fila[3]} | Apartados:")
            print(f"|Numero de reserva {fila[0]} | Numero de estacionamiento: {fila[4]} | Hora de Entrada: {fila[5]} | Hora de salida: {fila[6]}|")
        mi_conexion.desconectar()

    def imprimirVerApartadosPorVehiculo(self, placa):
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        mi_conexion.dato = placa
        consulta = """SELECT vee.id, v.id as placa, case 
                        when v.idTipoVehiculo = 1 then 'Motocicleta'
                        when v.idTipoVehiculo = 2 then 'Carro'
                        when v.idTipoVehiculo = 3 then 'Camion'
                        end as Tipo
                        , v.marca, idEspacioEstacionamiento, horaInicio, horaFinal 
                        FROM VehiculoXEspacioEstacionamiento vee 
                        join Vehiculo v on v.id = vee.idVehiculo 
                        join EspacioEstacionamiento ee on ee.id = vee.idEspacioEstacionamiento
                        having v.id = %s"""
        resultados = mi_conexion.ejecutar_consulta_where(consulta)
        placa = 0
        existenReservas = False
        for fila in resultados:
            if fila[1] != placa:
                existenReservas = True
                placa = fila[1]
                print(f"\nPlaca: {fila[1]} | Tipo: {fila[2]} | Marca: {fila[3]} | Apartados:")
            print(f"|Numero de reserva {fila[0]} | Numero de estacionamiento: {fila[4]} | Hora de Entrada: {fila[5]} | Hora de salida: {fila[6]}|")
        mi_conexion.desconectar()
        if not (existenReservas):
            print("No tiene reservas\n")
        return existenReservas
        



    def imprimirVerVehiculos(self):
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        consulta = """SELECT v.id as placa, case 
                        when v.idTipoVehiculo = 1 then 'Motocicleta'
                        when v.idTipoVehiculo = 2 then 'Carro'
                        when v.idTipoVehiculo = 3 then 'Camion'
                        end as Tipo
                        ,v.marca FROM Vehiculo v;"""
        resultados = mi_conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            print(f"|Placa = {fila[0]} | Tipo = {fila[1]} | Marca = {fila[2]}|")
        mi_conexion.desconectar()

    def imprimirRealizarReserva(self, estacionamiento, placa):
        horaInicio = int(input("Sistema horario de 24 horas\nIngrese la hora de inicio: "))
        horaFinal = int(input("Ingrese la hora Final: "))
        newVehiculo = Vehiculo(placa)
        estacionamiento.buscar_espacio_disponible(newVehiculo, horaInicio, horaFinal)
        
    def imprimirEliminarReserva(self, idReserva):
        mi_conexion = ConexionBaseDatos(idReserva)
        mi_conexion.conectar()
        consulta = """DELETE FROM VehiculoXEspacioEstacionamiento WHERE id = %s;"""
        mi_conexion.ejecutar_consulta_where(consulta)
        print("Se ha eliminado exitosamente")
        mi_conexion.desconectar()

    def imprimirActualizarVehiculo(self,placa):
        print("1) Tipo\n2) Marca")
        opcion = int(input("Ingrese lo que desea cambiar: "))
        if opcion == 1:
            print("1) Motocicleta\n2) Carro\n3) Camion")
            nuevoDato = int(input("Ingrese el nuevo tipo de vehiculo: "))
            consulta = """UPDATE Vehiculo
                SET idTipoVehiculo = %s
                WHERE id = %s;
                ;"""
        elif opcion == 2:
            nuevoDato = input("Ingrese la nueva marca: ")
            consulta = """UPDATE Vehiculo
                SET marca = %s
                WHERE id = %s;
                ;"""
        mi_conexion = ConexionBaseDatos()
        mi_conexion.conectar()
        mi_conexion.actualizarVehiculo(consulta, nuevoDato, placa)
        print("Se ha actualizado exitosamente")
        mi_conexion.desconectar()

    def imprimirMenuPrincipal(self, estacionamiento):
        print("1) Agregar vehiculo")
        print("2) Actualizar vehiculo")
        print("3) Ver vehiculos")
        print("4) Operar Vehiculo")
        print("5) Ver todas las reservas")
        print("6) Salir")

        opcion = int(input("Ingrese una opcion: "))
        if opcion == 1:
            self.imprimirAgregarVehiculo()
        elif opcion == 2:
            self.imprimirVerVehiculos()
            placa = int(input("Ingrese la placa del vehiculo: "))
            self.imprimirActualizarVehiculo(placa)
        elif opcion == 3:
            self.imprimirVerVehiculos()
        elif opcion == 4:
            self.imprimirVerVehiculos()
            placa = int(input("\nIngrese la placa del vehiculo: "))
            while True:
                print("1) Realizar reserva\n2) Ver reservas\n3) Ver mi total\n4) Eliminar Reserva\n5) regresar\n")
                opcion = int(input("Ingrese una opcion: "))
                if opcion == 1:
                    self.imprimirRealizarReserva(estacionamiento,placa)
                elif opcion == 2:
                    self.imprimirVerApartadosPorVehiculo(placa)
                elif opcion == 3:
                    estacionamiento.calcular_costoTotal(placa)
                elif opcion == 4:
                    if self.imprimirVerApartadosPorVehiculo(placa):
                        numReserva = input("Ingrese el numero de reserva a eliminar: ")
                        self.imprimirEliminarReserva(numReserva)
                elif opcion == 5:
                    break
                else:
                    print("Opcion no valida")
        elif opcion == 5:
            self.imprimirVerTodosApartados()
        elif opcion == 6:
            print("Ha salido del programa")
            return True
        else:
            print("Opcion no valida")
            return False
        

sistema = Principal()
sistema.main()


