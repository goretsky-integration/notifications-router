**All events must be in following format:**

```json
{
  "type": "Revenue",
  "chat_ids": [
    -10042342345,
    23543064534
  ],
  "payload": {},
  "errors": [
    {
      "unit_name": "Москва 0-0",
      "error": "Connection error"
    }
  ]
}
```

---

### Payload signatures:

- Statistics:
    - [Revenue statistics](#revenue-statistics)
    - [Late delivery vouchers statistics](#late-delivery-vouchers-statistics)
- Stop sales:
    - [Stop sales by ingredients](#stop-sales-by-ingredients)
    - [Stop sales by sales channels](#stop-sales-by-sales-channels)
    - [Stop sales by sectors](#stop-sales-by-sectors)
    - [Instant stop sales by ingredients](#instant-stop-sales-by-ingredients)
- Accounting:
    - [Stocks balance](#stocks-balance)
    - [Losses and excesses](#losses-and-excesses)
    - [Write-offs](#write-offs)
    - [Canceled orders](#canceled-orders)

---

## Payloads

### Revenue statistics

```json
{
  "units_statistics": [
    {
      "revenue_today": 0,
      "revenue_week_before_to_this_time": 0,
      "compared_to_week_before_in_percents": 0
    }
  ],
  "total_statistics": {
    "revenue_today": 0,
    "revenue_week_before_to_this_time": 0,
    "compared_to_week_before_in_percents": 0
  }
}
```

### Stop sales by ingredients

```json
[
  {
    "unit_name": "Москва 0-0",
    "started_at": "2019-10-01T00:00:00Z",
    "reason": "Состав не соответствует стандартам",
    "ingredient_name": "Моцарелла"
  }
]
```

### Stop sales by sales channels

```json
[
  {
    "unit_name": "Москва 0-0",
    "started_at": "2019-10-01T00:00:00Z",
    "reason": "Состав не соответствует стандартам",
    "sales_channel_name": "Доставка"
  }
]
```

### Stop sales by sectors

```json
[
  {
    "unit_name": "Москва 0-0",
    "stops": [
      {
        "started_at": "2019-10-01T00:00:00Z",
        "sector_name": "Совхоз имени Ленина"
      }
    ]
  }
]
```

### Instant stop sales by ingredients

```json
[
  {
    "unit_name": "Москва 0-0",
    "stops": [
      {
        "started_at": "2019-10-01T00:00:00Z",
        "reason": "Состав не соответствует стандартам",
        "ingredient_name": "Моцарелла"
      }
    ]
  }
]
```

### Stocks balance

```json
{
  "unit_name": "Москва 0-0",
  "stocks": [
    {
      "ingredient_name": "Моцарелла",
      "stocks_unit": "кг",
      "stocks_count": 0,
      "enough_for_days": 0
    }
  ]
}
```

### Write-offs

```json
{
  "unit_name": "Москва 0-0",
  "write_off_type": "EXPIRE_AT_15_MINUTES"
}
```

### Losses and excesses

```json
{
  "unit_name": "Москва 0-0",
  "total_loss": {
    "percentage_of_revenue": 10.5,
    "amount": 1000
  },
  "unaccounted_losses": {
    "percentage_of_revenue": 10.5,
    "amount": 1000
  },
  "write_offs": {
    "percentage_of_revenue": 10.5,
    "amount": 1000
  },
  "total_excess": {
    "percentage_of_revenue": 10.5,
    "amount": 1000
  }
}
```

### Late delivery vouchers statistics

```json
[
  {
    "unit_name": "Москва 0-0",
    "certificates_count_today": 0,
    "certificates_count_week_before": 0
  }
]
```

### Canceled orders

```json
[
  {
    "order_id": "00000000-0000-0000-0000-000000000000",
    "order_number": "123-2",
    "unit_name": "Москва 0-0",
    "sold_at": "2019-10-01T00:00:00Z",
    "canceled_at": "2019-10-01T00:00:00Z",
    "sales_channel_name": "Доставка",
    "price": 1000
  }
]
```
