# Mimari

Temel ilke: **GenAI anlar ve yazar, kod hesaplar.** Olasılık, eşik, süre, yetkinlik eşleşmesi ve kural kontrolü kodda yapılır. Ajan bu sonuçları okur, saha diliyle açıklar ve her cümlesini bir kayda bağlar.

## Katmanlar

| Katman | Görev | GenAI / Kod |
| --- | --- | --- |
| Kaynaklar | Saha telefonu, IoT sensör, ERP ve RFID, İK ve kılavuz | Prototipte gömülü sentetik JSON |
| Normalize ve makineye bağlama | Her kayıt tek biçime iner ve bir makine kimliği alır | Kod |
| Makine merkezli hafıza | Notlar, duruşlar, ölçümler, bileşenler, iş emirleri, kişiler, düzeltmeler | Kod |
| Kod hesapları | Durum, eşik, olasılık (n ile), MTBF/MTTR, eğilim, anomali, yetkinlik açığı, not kontrolü, uyarı kuralları | Kod |
| Bağlam paketi | Görev, makine, zaman penceresi ve rol filtresiyle hazırlanır | Kod |
| Ajanlar | Not düzenleme, tanı, kök neden, vardiya devri, izin dönüşü, e-posta taslağı, Ajana Sor | GenAI |
| Kanıt kontrolü | Kaynaksız madde ve koddan farklı olasılık ekrana çıkmaz | Kod |
| İnsan onayı | Amir devri onaylar, not düzeltilir ya da kapatılır, e-posta onaylanır | İnsan |

Düzeltmeler ve onaylar hafızaya geri yazılır, bir sonraki devir düzeltilmiş kaydı görür.

## Veri modeli

| Varlık | Alanlar | Kimlik |
| --- | --- | --- |
| Machine | `id`, `name`, `type`, `line`, `x`, `y` | `PRS-3` |
| Metric | `key`, `label`, `unit`, `warn`, `crit`, `dir` | makine tipine göre |
| Sensor reading | `[ts, value]`, saatlik | `SN:PRS-3:pressure` |
| RFID component | `tag`, `machine`, `component`, `hours`, `limit` | `RF-4471` |
| Downtime | `id`, `machine`, `start`, `end`, `minutes`, `raw_reason`, `erp_code` | `DT-805` |
| Pattern | `machine`, `ts`, `pattern` | `PT:PRS-3:<ts>` |
| Work order | `id`, `machine`, `title`, `status`, `priority`, `created`, `assigned_role`, `note` | `WO-5521` |
| Staff | `id`, `name`, `role`, `shift`, `certs[]`, `years`, `leave{from,to}` | `P01` |
| Field note | `id`, `ts`, `person`, `machine`, `raw`, `kind`, `source`, `selected_machine`, `structured{}` | `LG-101` |
| Note fix | `machine`, `status` (fixed/confirmed), `at` | not kimliği |
| Anomaly | `id`, `machine`, `type`, `level`, `title`, `text`, kanıt | `AN:PRS-3:pressure:breach` |

Kimlik önekleri ajanın kaynak göstermesi içindir. Ekran her kimliği tıklanabilir rozet olarak gösterir ve kaydın aslını açar. Kişisel bilgi olarak yalnızca rol, vardiya, yetkinlik, kıdem yılı ve izin tarihi tutulur.

## Kodun hesapları

- **Durum:** Açık duruş ya da kritik eşik kırmızı, bakımda mavi, son 1 saatte eşik dışı ölçüm, bugünkü desen ya da ömrü aşılmış bileşen sarı, aksi halde yeşil.
- **Olasılık:** Bugünden önceki desenlerin kaçında 24 saat içinde duruş başladığı. `{value, hits, n, window, low_sample}`, `n < 10` ise düşük örneklem.
- **MTBF ve MTTR:** Son 30 günün kapanmış duruşlarından.
- **Eğilim:** 72 saatlik en küçük kareler eğimi. Değişim, kritik ile uyarı eşiği farkının yarısını geçip kritik yöne gidiyorsa anomali. Kalan süre = (kritik − son değer) / saatlik eğim.
- **Yetkinlik açığı:** Gelen vardiyada izinde olmayan, riskli makinenin tipinde yetkin bakım teknisyeni yoksa açık var.
- **Anomali türleri:** eşik epizotu (saat tekrarı dahil), eğilim, ömrü aşılan bileşen, son 7 günde 2+ ramak kala, bugünkü desen.

## Not kontrolü

| Kontrol | Kural | Öneri |
| --- | --- | --- |
| Makine türü | Notta seçili makine tipine ait terim yok, başka tipe ait en az iki terim var | O tipte en çok anomalisi olan makine |
| Sensör değeri | Nottaki değer, o saatin ±60 dakikasındaki ölçümlerden %15’ten fazla sapıyor | Aynı tipte, o saatte uyumlu makine |
| Yetki ve prosedür | Hidrolik preste valf ayarı, bakım teknisyeni olmayan biri tarafından | Yok, eğitim ya da yetki işareti |
| Vardiya saati | Not saati kişinin vardiyasının ±1 saat dışında | Yok |
| Ajan düzeltmesi | Ajan notu seçilenden başka makineye bağladı | Seçilene geri al |

## Ajan akışları

Ajanlar birbirini çağırmaz ve kendi başına veri aramaz. Kod görev için bir bağlam paketi hazırlar, ajan JSON döndürür, kod doğrular, ekran gösterir. İstisna Ajana Sor: orada ajan altı araçla (makine listesi, makine bağlamı, anomaliler, uyarılar, ekip, not arama) veriyi kendisi sorgular.

**Neden vektör araması yok:** Bu ölçekte soru zaten “hangi makine, hangi zaman, hangi rol” ile tanımlı ve kodla kesin filtrelenir. Kılavuz sayısı yüzlerce dokümana çıktığında yalnızca o küme için vektör araması eklenir.

### Ortak kurallar (her prompt’un başında)

```
- Yalnızca verilen bağlamdaki kayıtlara dayan. Her iddia evidence_ids alanında
  bağlamdaki kimliklerle kaynak göstermeli.
- Olasılık, süre, sayı ÜRETME. Kodla hesaplanmış değerleri olduğu gibi kullan, n'i belirt.
- Kişileri değerlendirme, suçlama, performans yorumu yapma.
- Kök neden "hipotez"tir, kesinlik iddia etme.
- Sade, kısa Türkçe yaz. Saha çalışanı okuyacak.
```

### Çıktı şemaları

| Akış | Çıktı |
| --- | --- |
| Not düzenleme | `machine_id`, `kind`, `summary_plain`, `details[]`, `parts[]`, `safety_flag`, `follow_up`, `question_back`, `mentioned_values[]`, `mentioned_terms[]` |
| Tanı | `summary`, `hypotheses[{title, why, checks[], evidence_ids[]}]`, `safety`, `ask_operator[]` |
| Kök neden | `problem`, `erp_code_check`, `why_chain[]`, `fishbone[{category, finding, evidence_ids[]}]`, `root_cause_hypothesis`, `corrective[]`, `preventive[]`, `escalation`, `missing_data[]`, `evidence_ids[]` |
| Vardiya devri | `summary[]`, `actions[{role, task, reason, probability, evidence_ids[]}]`, `staffing[{person_id, suggestion, reason}]`, `open_questions[]`, `checklist[]` |
| İzin dönüşü | `headline`, `changes[]`, `waiting_for_you[]`, `first_tasks[]`, `ask[]` |
| E-posta | `subject`, `body` |

### Kanıt kontrolü

1. Her maddenin `evidence_ids` alanı dolu olmalı ve her kimlik bir kayda çözülmeli, yoksa madde gösterilmez.
2. Vardiya devrinde ajanın yazdığı her olasılık kodun değeri ve `n` ile birebir eşleşmeli.
3. Ekranın altında kaç maddenin düştüğü yazılır.

## Çalışma ortamı

Prototip claude.ai’de yayınlanan tek bir HTML sayfasıdır. Ajan çağrıları `window.claude.use("sample")`, ortak defter `window.claude.use("db")` (koleksiyonlar: `logs`, `note_fixes`) ile çalışır. Bu ikisi yoksa sayfa tarayıcının yerel depolamasına düşer ve ajan özelliklerini kapatır.

Sınırlar: claude.ai çerçevesi mikrofona doğrudan erişime izin vermez, sayfa telefon klavyesi diktesine geçer. E-posta gönderilmez, yalnızca taslak ve onay vardır. Ses dosyası saklanmaz.

## Pilota geçiş

| Prototipte | Pilotta |
| --- | --- |
| Gömülü sentetik JSON | MCP ve endüstriyel adaptörler |
| claude.ai yayın sayfası | Tesisin kendi alan adında uygulama, model erişimi KAI üzerinden |
| Klavye diktesi | Uygulama içi ses kaydı, sunucuda yazıya çevirme |
| Taslak e-posta | Kurumun e-posta servisi, onay sonrası |
| Sabit eşikler | Makine ve üretici bazında konfigürasyon |
| Geçmiş desenden olasılık | Gerçek geçmiş ve geri bildirimle kalibrasyon |
