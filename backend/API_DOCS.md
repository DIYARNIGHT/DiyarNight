# Superonline SmartNet API Dokümantasyonu

## API Base URL
```
http://localhost:8000/api/v1
```

## Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication
Şu anda authentication sistemi yoktur. Tüm endpoint'ler herkese açıktır.

---

## 1. USERS API (/api/v1/users)

### GET /users/{user_id}
Kullanıcı bilgilerini getirir.

**Response:**
```json
{
  "user_id": "U1",
  "name": "Ayşe Kaya",
  "address_id": "A1",
  "current_plan_id": "P100",
  "modem_mac": "00:11:22:33:44:55"
}
```

### GET /users/{user_id}/usage
Kullanıcının kota kullanım bilgilerini getirir.

**Response:**
```json
{
  "total_used_gb": 150.5,
  "quota_gb": 300,
  "usage_percentage": 50.17,
  "daily_usage": [...],
  "recommendations": [
    "Normal kullanım devam edebilir"
  ]
}
```

### GET /users/{user_id}/dashboard
Kullanıcının tam dashboard verilerini getirir.

**Response:**
```json
{
  "user": {...},
  "current_plan": {...},
  "usage_info": {...},
  "address_info": {...},
  "recommendations": [...]
}
```

### POST /users/{user_id}/change-plan
Kullanıcının paketini değiştirir.

**Request Body:**
```json
{
  "new_plan_id": "P200"
}
```

### GET /users/{user_id}/speed-test
Mock hız testi yapar.

**Response:**
```json
{
  "download_speed": 95.8,
  "upload_speed": 19.2,
  "ping": 12.5,
  "timestamp": "2025-10-02T10:00:00Z"
}
```

---

## 2. ADDRESSES API (/api/v1/addresses)

### GET /addresses/{address_id}/coverage
Adres kapsama bilgilerini getirir.

**Response:**
```json
{
  "address_id": "A1",
  "city": "Istanbul",
  "district": "Kadikoy",
  "fiber_available": true,
  "vdsl_available": true,
  "adsl_available": false,
  "max_speed_mbps": 200,
  "recommended_plans": [...]
}
```

### GET /addresses/
Tüm adresleri listeler.

### GET /addresses/search?city=Istanbul&district=Kadikoy
Adresleri şehir/ilçe ile arar.

### GET /addresses/cities
Mevcut şehirleri listeler.

### GET /addresses/districts/{city}
Belirtilen şehirdeki ilçeleri listeler.

---

## 3. PLANS API (/api/v1/plans)

### GET /plans/
Tüm paketleri listeler.

**Response:**
```json
[
  {
    "plan_id": "P100",
    "name": "Fiber 100",
    "quota_gb": 300,
    "speed_mbps": 100,
    "monthly_price": 399
  }
]
```

### GET /plans/{plan_id}
Belirli paket detaylarını getirir.

### GET /plans/speed/{max_speed}
Belirtilen maksimum hıza uygun paketleri listeler.

### GET /plans/filter/by-criteria
Çeşitli kriterlere göre paketleri filtreler.

**Query Parameters:**
- min_speed, max_speed
- min_quota, max_quota  
- max_price

### GET /plans/recommendations/{current_plan_id}?usage_percentage=85
Mevcut pakete ve kullanıma göre öneriler.

---

## 4. ADDONS API (/api/v1/addons)

### GET /addons/
Tüm ek paketleri listeler.

**Response:**
```json
[
  {
    "addon_id": "A20",
    "name": "+20GB Ek Kota",
    "extra_gb": 20,
    "price": 29.0
  }
]
```

### GET /addons/{addon_id}
Belirli ek paket detaylarını getirir.

### POST /addons/purchase/{user_id}
Kullanıcı için ek paket satın alır.

**Request Body:**
```json
{
  "addon_id": "A20"
}
```

### GET /addons/recommendations/{user_id}?usage_percentage=90
Kullanıcıya ek paket önerileri.

### GET /addons/filter/by-size
Boyut ve fiyata göre ek paketleri filtreler.

---

## 5. SUPPORT API (/api/v1/support)

### POST /support/reset-modem?user_id=U1
Kullanıcının modemini resetler.

**Response:**
```json
{
  "status": "ok",
  "message": "Modem reset komutu gönderildi."
}
```

### POST /support/create-ticket?user_id=U1
Destek talebi oluşturur.

**Request Body:**
```json
{
  "issue": "İnternet Yavaş",
  "description": "Bağlantı çok yavaş"
}
```

**Response:**
```json
{
  "ticket_id": "T-12345",
  "status": "created",
  "message": "Destek talebi oluşturuldu."
}
```

### GET /support/tickets/{user_id}
Kullanıcının tüm taleplerini listeler.

### GET /support/ticket/{ticket_id}
Belirli talep detaylarını getirir.

### PUT /support/ticket/{ticket_id}/status
Talep durumunu günceller.

**Request Body:**
```json
{
  "new_status": "resolved"
}
```

### GET /support/tickets/status/{status}
Belirli durumdaki talepleri listeler.

### GET /support/statistics
Destek istatistiklerini getirir.

---

## 6. USAGE API (/api/v1/usage)

### GET /usage/{user_id}/daily?days=30
Günlük kullanım verilerini getirir.

### GET /usage/{user_id}/monthly?year=2025&month=10
Aylık kullanım özetini getirir.

**Response:**
```json
{
  "user_id": "U1",
  "year": 2025,
  "month": 10,
  "total_usage_gb": 150.5,
  "quota_gb": 300,
  "usage_percentage": 50.17,
  "avg_daily_usage_gb": 5.02,
  "days_of_data": 30,
  "daily_breakdown": [...]
}
```

### GET /usage/{user_id}/statistics
Kapsamlı kullanım istatistiklerini getirir.

### GET /usage/{user_id}/predictions
Aylık kullanım tahminlerini getirir.

**Response:**
```json
{
  "user_id": "U1",
  "predicted_total_gb": 280.5,
  "predicted_percentage": 93.5,
  "risk_level": "medium",
  "recommendations": ["Kullanımınızı takip edin"]
}
```

### POST /usage/{user_id}/add-usage
Yeni kullanım kaydı ekler (test/admin amaçlı).

**Request Body:**
```json
{
  "date": "2025-10-02",
  "used_gb": 15.5
}
```

---

## Test Kullanıcıları

| User ID | Name | City | Current Plan | Address ID |
|---------|------|------|-------------|------------|
| U1 | Ayşe Kaya | Istanbul | Fiber 100 | A1 |
| U2 | Mehmet Yılmaz | Ankara | VDSL 35 | A2 |
| U3 | Fatma Demir | Izmir | Fiber 200 | A3 |
| U4 | Ali Öztürk | Bursa | Fiber 100 | A4 |
| U5 | Zeynep Şahin | Antalya | Fiber 1000 | A5 |

## Error Codes

| Code | Description |
|------|------------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

## Rate Limiting
Şu anda rate limiting uygulanmamıştır.

## CORS
Tüm origin'ler için CORS açıktır (development amaçlı).