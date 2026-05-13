# Cajeros Automáticos — Simulador Transaccional Concurrente

> Aplicación que simula operaciones financieras concurrentes en múltiples cajeros bancarios para evidenciar el control de concurrencia y exclusión mutua.

---

## Descripción

El proyecto resuelve el problema de la concurrencia en sistemas bancarios distribuidos, donde múltiples terminales acceden y modifican simultáneamente los saldos de las mismas cuentas. Mediante el uso de hilos y mecanismos de sincronización, el sistema garantiza la consistencia de los datos financieros durante retiros, depósitos y transferencias concurrentes, previniendo condiciones de carrera e interbloqueos.

---

## Flujo del Proyecto

El sistema opera mediante un flujo centralizado de gestión de transacciones donde cada terminal de cajero funciona como un hilo independiente (`threading.Thread`).

1. **Inicialización**: Se cargan los datos base del banco, de los usuarios y de las cuentas iniciales.
2. **Solicitud de Operación**: Un cajero simula una transacción (retiro, depósito, consulta o transferencia) sobre una cuenta específica.
3. **Exclusión Mutua (Sección Crítica)**: El gestor de transacciones solicita el bloqueo (`mutex.acquire()`) de la cuenta objetivo. Para las transferencias, se ordenan lexicográficamente las cuentas involucradas para evitar interbloqueos (deadlocks) al adquirir los candados en un orden predecible.
4. **Ejecución y Registro**: Se actualiza el saldo tras un retardo simulado, se añade el movimiento al historial local de la cuenta y se registra el evento detallado en la bitácora.
5. **Liberación**: Se libera el candado (`mutex.release()`) para permitir que otros hilos accedan a la cuenta.

---

## Stack Tecnológico

* **Lenguaje**: Python 3.
* **Concurrencia**: Librería estándar `threading` empleando las clases `Thread` y `Lock`.
* **Registro de Eventos**: Librería estándar `logging` configurada con salida hacia el archivo `bitacora.log`.
* **Validaciones**: Librería estándar `re` para el control de formatos de entrada mediante expresiones regulares.

---

## Módulos Principales

* **`main.py`**: Interfaz de consola que orquesta la ejecución, gestiona los menús de usuario y lanza las simulaciones de transacciones.
* **`banco.py`**: Administra el almacenamiento central de cuentas registradas y asegura la asignación de identificadores únicos de forma segura mediante exclusión mutua.
* **`usuario.py`**: Modela la entidad del cliente bancario, validando la integridad de sus datos personales y manteniendo la referencia a sus cuentas.
* **`cuenta_billetera.py`**: Estructura de la cuenta bancaria que almacena el saldo, el historial interno de movimientos y expone su propio candado (`mutex`) de sincronización.
* **`gestor_transacciones.py`**: Contiene la lógica central para procesar operaciones financieras aplicando de forma estricta el control de concurrencia sobre las secciones críticas.
* **`simulacion_cajero.py`**: Define el comportamiento autónomo de cada cajero automático simulado como un hilo que compite por el acceso a las cuentas.
* **`bitacora.py`**: Configura el formato y la persistencia de las trazas de ejecución para auditar la adquisición y liberación de bloqueos en el sistema.
* **`excepciones.py`**: Define las clases de excepciones personalizadas para el manejo de errores lógicos y de concurrencia.

---

## Ejecución del Proyecto

1. Asegurar la disponibilidad de Python 3 en el entorno del sistema operativo.
2. Navegar desde la terminal hacia el directorio raíz del código fuente.
3. Ejecutar el script principal:
```bash
python main.py

```


4. Interactuar con las opciones del menú en consola para registrar entidades o iniciar las simulaciones concurrentes.

---

## Integrantes del Grupo

* **Juan Diego Sotomayor**
* **Karel González Ruiz**
