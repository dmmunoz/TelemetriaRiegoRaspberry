from alarmas import crear_alarma, resolver_alarma

crear_alarma(
    "PRUEBA",
    "TEST_ALARMA",
    "Prueba del sistema de alarmas",
    "Esta es una prueba controlada del sistema de alarmas."
)

print("Alarma creada")

# Descomenta esta línea si quieres probar resolución:
# resolver_alarma("TEST_ALARMA", "Prueba de alarma resuelta correctamente")
