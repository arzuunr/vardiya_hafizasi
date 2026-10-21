# Vardiya Hafızası

Üretimde mavi yaka ekiplerin notlarını, makine verisini ve insan bilgisini **makineye bağlı tek bir hafızada** toplayan, bu hafızanın üstünde çalışan ajanlarla vardiya devrini, izin dönüşünü, uyarıları ve kök neden analizini üreten bir GenAI prototipi.

KoçSistem GenAI Ideathon, 20 Ekim 2026 için hazırlandı. Tüm veriler **sentetiktir**, gerçek kişi, kurum ya da marka verisi yoktur.

> Sayıyı kod hesaplar, metni ajan yazar, son sözü insan söyler.

## Bağlantılar

| Ne | Bağlantı |
| --- | --- |
| Canlı prototip (ajan dahil) | https://claude.ai/artifact/AvF5s4LY8wsNi71X9fczkV |
| Demo videosu (20 sn) | https://claude.ai/artifact/BDzZWvWQh2NLraURv4u9d1 |
| Teknik doküman | https://claude.ai/code/artifact/089d5c7d-420c-47ef-9e4a-b9be8f0caa18 |
| Ürün Hipotez Kartı | https://claude.ai/code/artifact/ad27130b-6f3e-4424-b24e-9cbddb677d3c |

Bağlantılar claude.ai hesabı ister ve sahibi paylaşana kadar özeldir.

## Hızlı başlangıç

### 1. Prototipi kendi bilgisayarında aç

```bash
git clone <repo-adresi>
cd vardiya-hafizasi
# Ya doğrudan dosyayı aç:
open prototype/index.html          # macOS
start prototype/index.html         # Windows
xdg-open prototype/index.html      # Linux
# Ya da küçük bir sunucuyla:
python3 -m http.server 8000 --directory prototype
# Tarayıcıda http://localhost:8000
```

**Yerelde ne çalışır, ne çalışmaz:**

| Özellik | Yerelde | claude.ai bağlantısında |
| --- | --- | --- |
| Hat haritası, sensör grafikleri, MTBF/MTTR, RFID | Çalışır | Çalışır |
| Anomali tespiti, olasılık (n ile), yetkinlik açığı | Çalışır | Çalışır |
| Not kontrolü, düzeltme ve kapatma | Çalışır (tarayıcıda saklanır) | Çalışır (ortak depoda) |
| Uyarı kuralları ve alıcılar | Çalışır | Çalışır |
| Ajan: not düzenleme, tanı, kök neden, devir dosyası, izin dönüşü, e-posta taslağı, Ajana Sor | **Çalışmaz** | Çalışır |
| Ortak defter (herkes aynı notları görür) | Çalışmaz | Çalışır |

Ajan özellikleri claude.ai yayın ortamının Claude çağırma yetkisini kullanır (`window.claude.use("sample")`). Yerelde bu yetki olmadığı için sayfa “Ajan bu görünümde çalışamıyor” uyarısı gösterir, kod tarafı yine çalışır. Ajanı yerelde çalıştırmak için bkz. [Yol haritası](#yol-haritası).

### 2. Sentetik veriyi yeniden üret

```bash
cd data
python3 gen_synthetic_data.py
# Beklenen çıktı:
# 44 KB 17 downtimes
# PRS-3 5 7
# KYR-2 5 7
```

`data.json` sayfaya `const DATA = …` olarak gömülüdür. Yeni veriyi sayfaya koymak için `prototype/index.html` içindeki `const DATA = {...};` satırını yeni `data.json` içeriğiyle değiştirin. Ayrıntılar: [docs/SYNTHETIC_DATA.md](docs/SYNTHETIC_DATA.md).

## Depo yapısı

```
vardiya-hafizasi/
  README.md
  prototype/
    index.html              Tek dosya prototip: arayüz, kod hesapları, ajan akışları, gömülü veri
  data/
    gen_synthetic_data.py   Sentetik tesis üreticisi (sabit tohum: 7)
    data.json               Üretilmiş veri
  docs/
    ARCHITECTURE.md         Katmanlar, veri modeli, kod ve GenAI ayrımı, ajan akışları
    SYNTHETIC_DATA.md       Verinin nasıl üretildiği, gömülü senaryolar, sınırlar
    DEMO_SCRIPT.md          Slayt 4 konuşma metni, uygulama demosu, jüri soruları
    CLAUDE_CODE_PLAN.md     Ürünleştirme için Claude Code görev planı (T1–T12)
```

Sunum dosyaları (PDF ve PPTX) bu depoda **yok**: KoçSistem’in “Hizmete Özel” şablonu üzerine hazırlandılar. Etkinlik kuralları ve şablonun paylaşım sınıfı netleşmeden herkese açık bir depoya konmamalı.

## Mimari, kısaca

```
Saha telefonu · IoT sensör · ERP ve RFID · İK ve kılavuz
        ↓
Normalize ve makineye bağlama (kod)
        ↓
Makine merkezli hafıza
        ↓
Kod hesapları: durum, eşik, olasılık (n ile), MTBF/MTTR, eğilim, anomali, yetkinlik açığı, not kontrolü
        ↓
Bağlam paketi (kod)
        ↓
Ajanlar (GenAI): not düzenleme, tanı, kök neden, vardiya devri, izin dönüşü, e-posta taslağı, Ajana Sor
        ↓
Kanıt kontrolü (kod): kaynaksız madde ve koddan farklı olasılık düşer
        ↓
İnsan onayı → ekranlar        (düzeltmeler ve onaylar hafızaya geri yazılır)
```

Ayrıntılar: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Ajan ne yapmaz

- İş emri açmaz, makineyi durdurmaz, PLC’ye komut vermez.
- Kişiyi değerlendirmez, puanlamaz, suçlamaz.
- Olasılık uydurmaz, kusur tespiti yapmaz. Kök neden her zaman “hipotez”tir.
- MES, CMMS ya da QMS’in yerini almaz, onların üstünde çalışan bir katmandır.

## Yol haritası

1. Ajan çağrılarını claude.ai dışında çalıştırmak için `sample()` çağrılarını bir sunucu tarafı uç noktasına (KAI ya da Anthropic API) taşıyan ince bir adaptör. API anahtarı tarayıcıda tutulmamalı.
2. Gömülü veri yerine MCP ve endüstriyel adaptörler: OPC-UA/MQTT, ERP bakım modülleri, RFID, vardiya planı.
3. Uygulama içi ses kaydı ve sunucu tarafında yazıya çevirme (claude.ai çerçevesi mikrofona izin vermediği için prototip telefon klavyesi diktesini kullanıyor).
4. Geri bildirimle olasılık kalibrasyonu.

Tam görev listesi: [docs/CLAUDE_CODE_PLAN.md](docs/CLAUDE_CODE_PLAN.md).
