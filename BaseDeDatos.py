import mysql.connector

class ConexionBaseDatos:
    def __init__(self,dato=""):
        self.host = "localhost"
        self.user = "root"
        self.password = "1234"
        self.database = "estacionamiento"
        self.conexion = None
        self.dato = dato

    def conectar(self):
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def desconectar(self):
        if self.conexion:
            self.conexion.close()

    def ejecutar_consulta(self, consulta):
        if self.conexion:
            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        
    def ejecutar_consulta_where(self, consulta):
        if self.conexion:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, (self.dato,))
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        
    def insertarApartado(self, consulta, idVehiculo, idEspacioEstacionamiento, horaInicio, horaFinal):
        if self.conexion:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, (idVehiculo, idEspacioEstacionamiento, horaInicio, horaFinal))
            self.conexion.commit()
            cursor.close()

    def mostrarTotal(self, consulta, idVehiculo):
        if self.conexion:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, (idVehiculo,))
            self.conexion.commit()
            cursor.close()

    def insertarVehiculo(self, consulta, placa, tipo, marca):
        if self.conexion:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, (placa, tipo, marca))
            self.conexion.commit()
            cursor.close()
# Ejemplo de uso
#mi_conexion = ConexionBaseDatos()
#mi_conexion.conectar()

#resultados = mi_conexion.ejecutar_consulta("SELECT * FROM nombre_de_tabla")

#for fila in resultados:
#    print(fila)

#mi_conexion.desconectar()
