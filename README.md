# Sales

В решении я использовал pydantic модели для валидации.

Все миграции создаются при запуске приложения с автогенерацией данных.

Не использовал контекстную сессию - предпочел использование собственного генератора.

## Запуск

```shell
docker compose up --build
```

Для более ранних версий

```shell
docker-compose up --build
```

## Реализовано

1) GET /api/products - возвращает список продуктов

Возвращает пустой список если нет продуктов:
```json
{
  "products": []
}
```
Или список наполненный элементами:
```json
{
  "products": [
    {
      "id": 1,
      "name" : "Product 1",
      "category": {
        "id": 1,
        "name": "Category 1"
      }
    },
    ...
  ]
}
```

2) POST /api/products

Принимает JSON:
```json
{
  "name": "Product name",
  "categoryId": 1
}
```

При успешном добавлении вернет:
```json
{
  "error": false,
  "message": "OK",
  "payload": {
    "name": "Product 1",
    "categoryId": 1
  }
}
```

При неудаче вернет:
```json
{
  "error": true,
  "message": "Some exception...",
  "payload": null
}
```

3) PUT /api/products/<int:product_id>

Принимает json
```json
{
  "name": "New product name"
}
```

При успехе возвращает:
```json
{
  "error": false,
  "message": "OK",
  "payload": {
    "name": "New product name"
  }
}
```

При неудаче вернет:
```json
{
  "error": true,
  "message": "Some exception...",
  "payload": null
}
```

4) DELETE /api/products/<int:product_id>

При успехе возвращает:
```json
{
  "error": false,
  "message": "OK",
  "payload": null
}
```

При неудаче вернет:
```json
{
  "error": true,
  "message": "Some exception...",
  "payload": null
}
```

5) GET /api/sales/total

Возвращает:
```json
{
  "total": <total sales sum>
}
```

6) GET /api/sales/top-products

При наличии продуктов возвращает
```json
{
  "products": [
    {
      "id": 1,
      "name": "Product Name",
      "category": "Category Name",
      "total": <total sales sum>
    }
  ]
}
```

При отсутствии продуктов возвращает
```json
{
  "products": []
}
```