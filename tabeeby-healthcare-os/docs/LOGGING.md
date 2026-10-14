# Structured Logging — Tabeeby API Gateway

- الوحدة: `backend/api-gateway/logging_utils.py` بجانب `main.py` (stdlib فقط، `SERVICE=tabeeby-api-gateway`). باقي الخدمات لم تُمس.
- السكيما لكل سطر JSON: `timestamp` (UTC ISO-8601 ms) + `level` + `service` + `env` + `version` + `request_id` + `event` + `message`.
- الربط: `gateway_middleware` في `main.py` يقرأ `x-request-id` (أو يولّد `new_request_id()`)، يخزّنه في `request_id_ctx` و`request.state.request_id`، يعيده في `X-Request-ID`، ويسجّل سطر وصول واحد (`http.access`: method + path + client_ip). تُسجَّل البيانات الوصفية فقط — ممنوع query strings أو `Authorization` أو الحمولات السريرية.
- المتغيرات (`.env.example` في جذر المشروع): `SERVICE_NAME=tabeeby-api-gateway`، `LOG_LEVEL=info`، `GIT_SHA=dev`، و`TABEEBY_ENV` للبيئة.
- الأسرار: تقنيع تلقائي (`***`) للحقول الحساسة (password/token/secret/authorization/cookie/…). ممنوع تسجيل أسرار حقيقية.
