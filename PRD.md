# PRD — Tabeeby (AI Healthcare Operating System)

## 1. نظرة عامة
منصة صحية ذكية (مريض/طبيب/باحث): خدمات FastAPI مستقلة لكل نطاق (patient :8001 وغيرها) على PostgreSQL/SQLite. النطاق المُتحقق كوديا أدناه فقط.

## 2. المستخدمون
- مريض (تسجيل، علامات حيوية، مواعيد، أدوية، طوارئ)
- طبيب (لوحة، دعم قرار، وصفات، أشعة)
- باحث/صحة عامة (RAG، مراقبة، جينوم سكاني)

## 3. الميزات الأساسية (قابلة للاختبار)
1. إدارة مرضى: سرد/عرض/إنشاء (`GET /patients`, `GET /patients/{id}`, `POST /patients`)
2. علامات حيوية: تحديث/سرد/لحظي/اتجاهات (`POST /patients/{id}/vitals`, `GET .../vitals|/vitals/realtime|/health-trends`) مع رفض عدم تطابق الهوية (422)
3. موعد وطوارئ (`POST /patients/{id}/appointment|/emergency`)
4. أدوية: سرد وتسجيل جرعة (`GET .../medications`, `POST .../medications/{med_id}/take`)
5. فحص أعراض وتأثير طقس (`GET .../symptom-check|/weather-impact`)
6. طبيب: لوحة/دعم قرار/وصفة/أشعة (`GET /api/v1/physician/{id}/dashboard|/patient/{id}/imaging`, `POST /api/v1/physician/decision-support|/prescribe`)
7. تشخيص AI: مسح وRAG ومقارنة تاريخية (`POST /api/v1/diagnostic/scan|/rag/query|/compare/historical`, `GET /api/v1/diagnostic/self-learning/status`)
8. اكتشاف دواء: خط أنابيب وحالة ومركّبات (`POST /api/v1/drug-discovery/pipeline`, `GET .../pipeline/{id}/status|/compounds`)
9. صحة وطنية: مراقبة ونظام دواء وجينوم وتشغيل بيني (`GET /api/v1/national/surveillance|/drug-ecosystem|/population-genomics|/interoperability/status`)
10. بحث RAG (`POST /api/v1/rag/query`) وبحث علمي (`POST /api/v1/research/query`, `GET .../population-intelligence|/databases`)

## 4. API endpoints الحقيقية (من الكود فقط)
- Patient-Service (`main.py`): كل مسارات البند 1–5 أعلاه + `GET /health`
- Physician-Service: `GET /health|/api/v1/physician/{id}/dashboard|/patient/{id}/imaging`, `POST /api/v1/physician/decision-support|/prescribe`
- Diagnostic-AI: `GET /health|/api/v1/diagnostic/self-learning/status`, `POST /api/v1/diagnostic/scan|/rag/query|/compare/historical`
- Drug-Discovery: `GET /health|/pipeline/{id}/status|/compounds`, `POST /api/v1/drug-discovery/pipeline`
- National-Health: `GET /health|/surveillance|/drug-ecosystem|/population-genomics|/interoperability/status`
- RAG/Research/Notify/Ultra-IQ/Surgical/Robot: حسب `main.py` لكل خدمة (مثل `POST /api/v1/rag/query`, `POST /api/v1/research/query`, `POST /api/v1/notify/send`, `POST /api/v1/reason|/diagnose|/treatment`)

## 5. بيانات الدخول/الإعداد للاختبار
- `cd tabeeby-healthcare-os && cp .env.example .env && docker compose up --build`؛ patient-service محليا `uvicorn main:app --port 8001`
- لا مصادقة ولا مستخدمين مزروعين في الكود — تُنشأ البيانات عبر `POST /patients`؛ مخازن patient-service in-memory (تُفقد بإعادة التشغيل)

## 6. خارج النطاق (mocked/simulated)
- patient-service يستخدم قواميس in-memory وردود AI/طوارئ/أدوية ثابتة القوالب (ليست نماذج حية)؛ U-Net/ResNet للأشعة وVR/AR والروبوتات وقاعدة 10,000 دواء: ادعاءات README دون عقد API حي مُتحقق هنا؛ خدمات (`vr-ar-platform`, `surgical-suite` إلخ) بنمط `/start|/list` بدائي لا تمثل تنفيذها السريري الحقيقي.
