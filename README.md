# :money_with_wings: Control de Finanzas PRW Backend :money_with_wings:

---
## Autores:
- Manuel Gonzalez Leal (https://github.com/klasinky)
- Juan Daniel Padilla Obando (https://github.com/zclut)
---

## Bitácora

### Miércoles 17 de Marzo (3 horas) :white_check_marck:
    
    - Configuración del proyecto
    - Creación de la base de datos
    
### Jueves 18 de Marzo (5 horas) :white_check_marck:

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

### Viernes 19 de Marzo (2 horas 30 minutos) :white_check_marck:

    - Creación de soft delete del usuario
    - Modificación de las urls
    - Cambios de la base de datos
        + Nuevo campo "is_active" (core_user)     
    - Creación de los test para el soft delete

### Sábado 20 de Marzo (1 hora) :white_check_marck:

    - Cambiar contraseña del usuario (Endpoint)
    - Instalar flake8 (para verificar el código)
    - Tests
        + Cambiar contraseña
        + Cambiar contraseña con la antigua incorrecta
        + Cambiar contraseña sin proporcionar la antigua
        + Comprobar que no se pueda cambiar la contraseña si no se le pasa la nueva
    - Agregamos serializer para cambiar la contraseña

