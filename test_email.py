from emailer import enviar_correo

ok = enviar_correo(
    "Prueba SantaFe Water Control",
    "Este es un correo de prueba."
)

if ok:
    print("OK")
else:
    print("ERROR")
