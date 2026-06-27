# Telemetria Riego con Raspberry
Sistema de telemetría para la monitorización y control del riego, nivel de aljibe y trasvase de agua mediante Raspberry Pi, GPIO, Rain Bird, LoRa y base de datos SQLite. Diseñado para funcionar de forma autónoma 24/7 en una comunidad de propietarios


Sistema de telemetría desarrollado para una Comunidad de Vecinos con el objetivo de monitorizar y controlar el sistema de riego y abastecimiento de agua de forma totalmente autónoma.

El proyecto está basado en una Raspberry Pi que actúa como controlador principal, registrando el estado de los sensores, tomando decisiones automáticamente y mostrando toda la información en una interfaz web accesible desde cualquier dispositivo de la red local.

---

## Objetivos

- Control automático del nivel del aljibe.
- Arranque automático del sistema de trasvase.
- Detección del funcionamiento del sistema de riego Rain Bird.
- Registro histórico de todos los eventos.
- Funcionamiento autónomo 24 horas al día.
- Reinicio automático tras un corte eléctrico.
- Interfaz web para consulta desde PC, móvil o pantalla dedicada.

---

## Hardware

- Raspberry Pi B+
- Raspberry Pi OS
- GPIO
- Boya de nivel ESPA
- Rain Bird ESP-TM2
- Relé optoacoplado 3.3 V
- SQLite
- Flask

---

## Funciones actuales

- Monitorización del nivel del aljibe.
- Control automático del trasvase.
- Protección por tiempo máximo de funcionamiento.
- Detección del inicio y final del riego.
- Registro histórico de eventos.
- Interfaz web responsive.

---

## Funciones previstas

- Comunicación LoRa con el cuadro del pozo.
- Confirmación del funcionamiento real de la bomba.
- Estadísticas de consumo.
- Históricos mensuales y anuales.
- Copias de seguridad automáticas.
- Alarmas inteligentes.
- Monitorización remota.

---

## Arquitectura

Boya de nivel
↓
Raspberry Pi
↓
Lógica de control
↓
Relé de trasvase
↓
Sistema hidráulico

Rain Bird
↓
GPIO
↓
Registro histórico

LoRa
↓
Confirmación bomba del pozo

---

## Tecnologías

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Raspberry Pi GPIO

---

## Estado del proyecto

Versión 1.0

Proyecto operativo y en desarrollo continuo.

---

## Autor

Diego M. Muñoz Escañuela

Comunidad de Vecinos

2026
