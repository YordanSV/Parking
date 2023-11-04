# Ejemplo de uso:
estacionamiento = Estacionamiento(num_espacios=10)  # Crear un estacionamiento con 10 espacios

# Apartar espacio para un vehículo
vehiculo1 = Motocicleta("ABC123")
vehiculo2 = Camion("XYZ789")
estacionamiento.buscar_espacio_disponible(vehiculo1, 8, 11)
estacionamiento.buscar_espacio_disponible(vehiculo2, 14, 16)
estacionamiento.buscar_espacio_disponible(vehiculo1,15, 16)
estacionamiento.buscar_espacio_disponible(vehiculo1,17, 18)


# Calcular costo para un vehículo (puedes implementar la lógica para calcular el costo en función de todos los apartados)
costo1 = vehiculo1.calcular_costo(8, 12)
costo2 = vehiculo1.calcular_costo(14, 16)
costo3 = vehiculo1.calcular_costo(15, 16)


print("Costo total para vehículo 1: $", costo1+costo3)
print("Costo total para vehículo 2: $", costo2)


# Liberar espacio para un vehículo
estacionamiento.liberar_espacio(vehiculo1)
estacionamiento.liberar_espacio(vehiculo2)
