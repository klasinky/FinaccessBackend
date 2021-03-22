# :money_with_wings: Control de Finanzas PRW Backend :money_with_wings:

[![CircleCI](https://circleci.com/gh/klasinky/JuanManuelPRWBackend.svg?style=svg&circle-token=d7afef3e3010d0ac5f16c8a9a75bef6038408c34)](https://circleci.com/gh/klasinky/JuanManuelPRWBackend)


---
## Autores:
- Manuel Gonzalez Leal (https://github.com/klasinky)
- Juan Daniel Padilla Obando (https://github.com/zclut)
---

## Bitácora

### Miércoles 17 de Marzo (3 horas) :white_check_mark:
    
    - Configuración del proyecto
    - Creación de la base de datos
    
### Jueves 18 de Marzo (5 horas) :white_check_mark:

    - Creación de los endpoint de usuario
        + Login
        + Register
        + Profile
        + Detail
        + Update
    - Creación de los test pertinentes
    - Cambios en la base de datos
    - Permisos
    - Tokens

### Viernes 19 de Marzo (2 horas 30 minutos) :white_check_mark:

    - Creación de soft delete del usuario
    - Modificación de las urls
    - Cambios de la base de datos
        + Nuevo campo "is_active" (core_user)     
    - Creación de los test para el soft delete

### Sábado 20 de Marzo (5 horas) :white_check_mark:

#### 1 Hora
    - Cambiar contraseña del usuario (Endpoint)
    - Instalar flake8 (para verificar el código)
    - Tests
        + Cambiar contraseña
        + Cambiar contraseña con la antigua incorrecta
        + Cambiar contraseña sin proporcionar la antigua
        + Comprobar que no se pueda cambiar la contraseña si no se le pasa la nueva
    - Agregamos serializer para cambiar la contraseña
#### 4 horas
    - Creación de los endpoints de Month
        + Crear
        + Editar
        + Eliminar
        + Ver (Solo se pueden ver los del usuario)
        + Listar (Solo se pueden ver los del usuario)
    - Creacion de los serializer
        + Expense
        + Entry
        + Category
        + Month
    - Creación de un test
        + Creación de mes
