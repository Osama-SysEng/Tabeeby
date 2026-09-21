# قاعدة البيانات والتحديث الدوري الآمن

## مبدأ التصميم

لا تُعدّل قاعدة البيانات مخططها عشوائيًا ولا تحذف البيانات ذاتيًا. النمو الآمن يعني أن البيانات الجديدة تدخل عبر عقود bounded، وأن المخطط يتوسع بترحيلات مرقمة ومراجعة، وأن الاحتفاظ والأرشفة محددان بسياسة واضحة. يعتمد التنفيذ على bootstrap idempotent، ترحيلات SQL ذات checksum، وقفل PostgreSQL يمنع تشغيل ترحيلين متزامنين.

## التشغيل الدوري

التشغيل المقترح هو مهمة مضيف مجدولة تستدعي `scripts/maintenance_once.sh`. تنفذ المهمة نسخة احتياطية أولًا، ثم الترحيلات، ثم `ANALYZE`، ثم تسجل حالة الدورة. مشغّل `scripts/maintenance_loop.sh` متاح للتشغيل المستمر لكنه معطل افتراضيًا ويتطلب `AUTO_MAINTENANCE_ENABLED=true` وفاصلًا لا يقل عن خمس دقائق. لا تستخدم هذا المشغّل داخل حاوية لا تحتوي على Docker CLI إذا كانت النسخة الاحتياطية تعتمد على Docker Compose.

مثال جدولة يومية على مضيف مخصص:

```cron
17 2 * * * cd /opt/tabeeby && flock -n /var/lock/tabeeby-maintenance.lock env AUTO_MAINTENANCE_ENABLED=true DATABASE_URL='postgresql://...' POSTGRES_PASSWORD='...' ./scripts/maintenance_once.sh >> /var/log/tabeeby-maintenance.log 2>&1
```

يجب حفظ الأسرار في مدير أسرار أو ملف root-only، وليس داخل crontab المشترك أو المستودع. قبل أول تشغيل، نفّذ المهمة على بيئة staging ببيانات اصطناعية، ثم افحص backup وrestore في بيئة منفصلة.

## سياسة النسخ الاحتياطي

يجب أن يسبق أي تغيير مخطط أو ترحيل نسخة احتياطية ناجحة. استخدم نسخًا full/differential/incremental مع WAL واحتفاظًا مشفرًا، واختبر الاستعادة بدل اعتبار وجود ملف النسخة دليلًا على قابليتها للاستعادة [3]. يجب أن تكون مستودعات النسخ خارج المضيف الرئيسي ومقيدة الصلاحيات.

## حدود الربط والتحديث

كل مصدر خارجي يحتاج `source_id` ومالكًا موثقًا وHTTPS وhostname allowlist وOAuth أو هوية خدمة ونطاقات أقل صلاحية وقيود حجم ومعدل وcursor أو ETag. استخدم UPSERT ومؤشر مصدر ثابت حتى تكون إعادة المحاولة idempotent؛ هذا يتفق مع أفضل ممارسات Airflow التي تعامل المهمة كمعاملة قاعدة بيانات وتمنع نتائج ناقصة أو مكررة عند إعادة المحاولة [2]. لا تُدخل استجابة خارجية إلى قاعدة البيانات قبل التحقق من نوعها وحجمها وسلامة بنيتها وتسجيل provenance.

## التراجع والفشل

إذا فشلت checksum أو الترحيلة، تتوقف العملية fail-closed ولا تُعدّل الترحيلة المطبقة. لا تستخدم downgrade آليًا على بيانات إنتاجية حساسة؛ أنشئ ترحيلًا عكسيًا reviewed أو استعد نسخة إلى بيئة منفصلة ثم نفّذ cutover مخططًا. بعد كل تحديث راقب عمر آخر نسخة احتياطية، نجاح الترحيل، حجم قاعدة البيانات، عمر WAL، زمن الاستعلام، وqueue lag.

## المراجع

[1]: https://alembic.sqlalchemy.org/en/latest/ "Alembic documentation"
[2]: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html "Apache Airflow Best Practices"
[3]: https://pgbackrest.org/user-guide.html "pgBackRest User Guide"
