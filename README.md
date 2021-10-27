
---
## Authors :man_technologist:
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

## Endpoints :chart_with_upwards_trend:

- **GET** /categories/all
- **DELETE** /comment/{id}/delete
- **PUT** /comment/{id}/like 
- **GET** /currencies
- **GET/PATCH/PUT/DELETE** /entries/{id}
- **GET/PATCH/PUT/DELETE** /expense/{id} 
- **POST** /months
- **GET** /months/all
- **GET** /months/overview
- **GET**/DELETE /months/{id}
- **GET** /months/{id}/amounts 
- **GET** /months/{id}/analysis
- **GET** /months/{id}/category/stats/entry
- **GET** /months/{id}/category/stats/expense
- **POST** /months/{id}/create/entry
- **POST** /months/{id}/create/expense
- **GET** /months/{id}/export/entry
- **GET** /months/{id}/export/expense
- **GET** /months/{id}/import/entry
- **GET** /months/{id}/import/expense
- **GET** /notifications
- **PUT** /notifications/{id} 
- **GET/POST** /posts
- **GET** /posts/filter/{username}
- **POST** /posts/{idpost}/comment
- **GET** /posts/{idpost}/comment/all
- **GET/PUT/PATCH/DELETE** /posts/{idpost}
- **PATCH** /posts/{id}/finished
- **PUT** /posts/{id}/like
- **GET** /posts/{id}/recommendation 
- **GET** /stocks
- **GET** /stocks/all
- **GET** /stocks/{id}
- **POST**/DELETE /stocks/{id}
- **GET** /tags
- **GET** /tags/detail 
- **GET** /users/check
- **POST** /users/login
- **GET/PUT/PATCH** /users/me
- **PATCH** /users/me/changepassword
- **PATCH** /users/me/delete
- **GET** /users/profile/{username}
- **PATCH** /users/profile/{username}
- **POST** /users/register
- **POST** /users/tops