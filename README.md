# :money_with_wings: Control de Finanzas PRW Backend :money_with_wings:

[![CircleCI](https://circleci.com/gh/klasinky/JuanManuelPRWBackend.svg?style=svg&circle-token=d7afef3e3010d0ac5f16c8a9a75bef6038408c34)](https://circleci.com/gh/klasinky/JuanManuelPRWBackend)


---
## Autores:
- Manuel Gonzalez Leal (https://github.com/klasinky)
- Juan Daniel Padilla Obando (https://github.com/zclut)
---

## Instalación :computer:
```
pip install -r requirements.txt
python manage.py migrate
```

## Test :pencil2:
```
python manage.py test
```

---

## Bitácora

### :white_check_mark: Miércoles 17 de Marzo (3 horas) :white_check_mark:
    
    - Configuración del proyecto
    - Creación de la base de datos
---
### :white_check_mark: Jueves 18 de Marzo (5 horas) :white_check_mark:

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
---
### :white_check_mark: Viernes 19 de Marzo (2 horas 30 minutos) :white_check_mark:

    - Creación de soft delete del usuario
    - Modificación de las urls
    - Cambios de la base de datos
        + Nuevo campo "is_active" (core_user)     
    - Creación de los test para el soft delete
---
### :white_check_mark: Sábado 20 de Marzo (5 horas) :white_check_mark:

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
---
### :white_check_mark: Martes 23 de Marzo (5 horas) :white_check_mark:

    - Creación de los endpoint
        + Entry
        + Expense
    - Implementación de swagger
    - Month endpoint
        + Gráficos (Categoria del mes)
        + No permitir crear dos meses iguales
    - Creación de test
        + Entry
        + Expense
        + Month
---
### :white_check_mark: Miércoles 24 de Marzo (5 horas) :white_check_mark:

    - Creacion de views
        + AmountBaseUploadXLS
        + AmountBaseDownloadXLS
        ```
            Para no repetir el mismo código en Expense y Entry,
            simplemente extendiendo de dichas vistas se podra
            utilizar en cualquiera de las vistas
        ```
    - Editar Serializer EntryModelSerializer y ExpenseModelSerializer
        + Añadir HyperLink
    - Creación de URL
        + Importar XLS (Entry, Expense)
        + Exportar XLS (Entry, Expense)
    - Openpyxl (requirements.txt)
---
### :white_check_mark: Jueves 25 de Marzo (5 horas 30 minutos) :white_check_mark:

#### 2 Horas
    - Creación de Serializer
        + AmountBase (Para usarlo en Entry y Expense)
        ```
            Para no repetir el mismo código en Expense y Entry,
            simplemente extendiendo de dicho serializer se podra
            utilizar en cualquiera de los serializer
        ```
    - Post Endpoint
        + Crear
        + Editar
        + Eliminar
        + Ver 
        + Listar 
        + Finalizar Post
        + Test

#### 3 Horas 30 minutos
    - Creación de los Endpoint
        + Comment
            * Crear
                * Response a otro comentario
            * Eliminar
        + CommentLike
        + PostLike

### :white_check_mark: Lunes 29 de Marzo (3 horas) :white_check_mark:
    - Creación de Cache
        + Post Like
        + Comment Like
        + Post Create
        + Comment Create
        ```
            Esperar cierto tiempo para volver a ejecutar la misma
            acción
        ```
    - Petición a la API Alpha Vantage (Para las acciones)

### :white_check_mark: Martes 30 de Marzo (2 horas) :white_check_mark:
    - Creación de los Endpoint
        + Listar todas las acciones disponibles
        + Suscribirse a una acción
        + Eliminar una suscripción de una acción
        + Listar las acciones a la que esta suscrita el usuario
        + Mostrar los datos del mercado de la compañía
    - Creación de tests

### :white_check_mark: Mircoles 28 de Abril (1 hora) :white_check_mark:
    - Creación del Endpoint para las Currency
    - Refactor en el Endpoint de Profile
    