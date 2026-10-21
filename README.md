# Vardiya Hafızası

**Vardiya değişiminde bilgi kaybolmasın.** Üretimde operatörün sesli notunu, sensör verisini, duruş kayıtlarını ve iş emirlerini makineye bağlı tek bir hafızada toplayan, bu hafızanın üstünde çalışan GenAI ajanlarıyla vardiya devrini, izin dönüşünü, uyarıları ve kök neden analizini üreten açık kaynak bir prototip.

> Sayıyı kod hesaplar, metni ajan yazar, son sözü insan söyler.

**In English:** A GenAI prototype for manufacturing shift handovers. Field notes, sensor data, downtime records and work orders are linked to the machine they belong to. Code computes every number (thresholds, trends, downtime probability with sample size, skill gaps). An LLM agent writes the handover file, root cause hypotheses and alerts, citing a source record for every sentence. A human approves. All data is synthetic.

![Hat haritası](docs/images/01-hat-haritasi.png)

**Canlı prototip (ajan dahil):** https://claude.ai/artifact/AvF5s4LY8wsNi71X9fczkV
**Demo videosu (20 sn):** https://claude.ai/artifact/BDzZWvWQh2NLraURv4u9d1

Tüm veriler **sentetiktir**. Tesis, makineler ve kişiler kurgusaldır.

## Neden

Vardiya değiştiğinde üretim durmaz ama bilgi çoğu zaman kesilir. Gece fark edilen bir sorun sözlü devirde unutulur, defterde kalır ya da bir mesajlaşma grubunda kaybolur. Sabah aynı arıza tekrar eder. Deneyimli usta izne çıktığında ya da emekli olduğunda bildiği her şey onunla gider.

Vardiya Hafızası bilgiyi kişiye değil **makineye** bağlar. Kimse kimseye haber vermemiş olsa bile, gelen ekip makinenin son 72 saatini görür.

## Ne yapıyor

Görüntüler canlı prototipten alındı. Ajan çıktıları gerçek model çıktısıdır, düzenlenmedi. Tesis ve veriler sentetik.

### 1. Hat haritası ve makine detayı
Her makinenin durumu sensör eşiklerinden ve geçmiş duruşlardan kodla hesaplanır. Pres-3 sarı, çünkü sabah geçmişte duruşa dönmüş bir desen görüldü. Olasılık örneklem büyüklüğüyle verilir: %71, n=7. Görüntü sayfanın en üstünde.

### 2. Anomali için kök neden analizi
Kod her sabah 06:00 civarında tekrarlayan basınç düşüşünü bulur. Ajan 5 Neden, balık kılçığı ve ERP kodu kontrolü çıkarır, kök nedeni “hipotez” olarak etiketler, duruşa dönmeden yapılacakları ve kesin karar için eksik veriyi yazar.

<p><img src="docs/images/02-kok-neden-5-neden.png" width="49%" alt="Kök neden: 5 Neden ve ERP kodu kontrolü"> <img src="docs/images/03-kok-neden-balik-kilcigi.png" width="49%" alt="Kök neden: balık kılçığı ve duruşa dönmeden"></p>

### 3. Saha telefonu ve vardiya devri
Operatör notunu yazar ya da dikte eder, ajan onu makinenin defterine düzgün bir kayıt olarak işler. Vardiya geçişinde kod son 8 saati, riskleri ve gelen ekipteki yetkinlik açığını toplar, ajan kaynak gösteren devir dosyasını yazar.

<p><img src="docs/images/04-saha-telefonu.png" width="49%" alt="Saha telefonu"> <img src="docs/images/05-vardiya-devri.png" width="49%" alt="Vardiya devri"></p>

### 4. İzin dönüşü, not kontrolü ve uyarılar
İzinden dönen ustaya yokken değişenler ve onu bekleyen işler. Yanlış makineye girilmiş ya da sensörle çelişen notları kod yakalar ve tek tuşla düzeltilir. Uyarılar rol tablosuna göre doğru kişilere gider.

<p><img src="docs/images/06-izin-donusu.png" width="49%" alt="İzin dönüşü brifingi"> <img src="docs/images/07-not-kontrolu-ve-uyarilar.png" width="49%" alt="Not kontrolü ve uyarılar"></p>

### 5. Ajana sor
Ajan veriyi araçlarla kendisi sorgular ve her cümlesine kaynak kimliği ekler.

<p><img src="docs/images/08-ajana-sor-neden.png" width="49%" alt="Ajana sor: Pres-3 neden sabah sorun çıkarıyor"> <img src="docs/images/09-ajana-sor-gunluk-rapor.png" width="49%" alt="Ajana sor: günlük rapor"></p>

### 6. Sınırlarını biliyor
Çalışanları değerlendirmesi istendiğinde reddeder ve süreci anlatır. Verisi olmayan bir soruda (hava durumu) bilmediğini söyler, bağlantı uydurmaz.

<p><img src="docs/images/10-ajana-sor-calisanlar.png" width="49%" alt="Ajana sor: çalışanlar hakkında"> <img src="docs/images/11-ajana-sor-kapsam-disi.png" width="49%" alt="Ajana sor: kapsam dışı soru"></p>

## Mimari

```mermaid
flowchart TD
    A["Saha telefonu<br/>sesli ya da yazılı not"] --> N
    B["IoT sensörler<br/>basınç, sıcaklık, titreşim"] --> N
    C["ERP ve RFID<br/>duruş, iş emri, bileşen ömrü"] --> N
    D["İK ve kılavuz<br/>vardiya, yetkinlik, prosedür"] --> N
    N["Normalize ve makineye bağlama · kod"] --> M["Makine merkezli hafıza"]
    M --> K["Kod hesapları<br/>durum, eşik, olasılık n ile, MTBF/MTTR,<br/>eğilim, anomali, yetkinlik açığı, not kontrolü"]
    K --> P["Bağlam paketi · kod"]
    P --> G["Ajanlar · GenAI<br/>not düzenleme, tanı, kök neden, vardiya devri,<br/>izin dönüşü, e-posta taslağı, ajana sor"]
    G --> E["Kanıt kontrolü · kod<br/>kaynaksız madde ve koddan farklı sayı düşer"]
    E --> H["İnsan onayı"]
    H -. "düzeltmeler ve onaylar" .-> M
    style G fill:#E3EEFB,stroke:#2D6CB5,stroke-width:2px
```

Üç tasarım kararı:

1. **Olasılığı model üretmez.** Kod geçmişte bir desenden sonra kaç kez duruş olduğunu sayar ve örneklem büyüklüğüyle verir (`%71, n=7`). Ajan bu sayıyı yalnızca açıklar.
2. **Vektör araması yok.** Sorular zaten “hangi makine, hangi zaman aralığı, hangi rol” ile tanımlı. Kod bunları kesin olarak filtreler, bu hem daha isabetli hem izlenebilir.
3. **Her iddianın kaynağı var.** Ajan her maddeye bir kayıt kimliği ekler. Kod kimliği çözemezse ya da sayı kendi hesabıyla uyuşmazsa madde ekrana çıkmaz.

Ayrıntılar: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Hızlı başlangıç

```bash
git clone https://github.com/arzuunr/vardiya_hafizasi.git
cd vardiya_hafizasi
python3 -m http.server 8000 --directory prototype
# Tarayıcıda http://localhost:8000
```

Ya da `prototype/index.html` dosyasını doğrudan tarayıcıda açın. Kurulum gerekmez.

| Özellik | Yerelde | Canlı prototipte |
| --- | --- | --- |
| Hat haritası, grafikler, RFID, MTBF/MTTR | Çalışır | Çalışır |
| Anomali tespiti, olasılık, yetkinlik açığı | Çalışır | Çalışır |
| Not kontrolü, düzeltme | Çalışır (tarayıcıda saklanır) | Çalışır (ortak depoda) |
| Uyarı kuralları | Çalışır | Çalışır |
| Ajan: not düzenleme, tanı, kök neden, devir, izin dönüşü, e-posta, ajana sor | Kapalı | Çalışır |

Ajan çağrıları prototipin yayınlandığı claude.ai ortamına bağlıdır (`window.claude.use("sample")`). Yerelde sayfa ajanı kapatır, kodun yaptığı her şey çalışmaya devam eder. Kendi model erişiminizle çalıştırmak için bkz. [Yol haritası](#yol-haritası).

Adım adım tur: [docs/DEMO.md](docs/DEMO.md)

## Sentetik veri

```bash
cd data && python3 gen_synthetic_data.py
# Beklenen: PRS-3 5 7 ve KYR-2 5 7
```

Veri rastgele değil, sistemin her yeteneğini sınayan senaryolarla üretildi: her sabah tekrar eden bir basınç düşüşü, kritik eşiğe yaklaşan bir titreşim, ömrü aşılmış bir kaynak nozulu, farklı kelimelerle yazılmış üç ramak kala bildirimi, yanlış makineye girilmiş notlar, izinden dönen bir usta ve akşam vardiyasında bir yetkinlik açığı. Sabit tohumla üretildiği için her çalıştırmada aynıdır.

Ayrıntılar ve sınırlar: [docs/SYNTHETIC_DATA.md](docs/SYNTHETIC_DATA.md)

## Ajan ne yapmaz

- İş emri açmaz, makineyi durdurmaz, PLC’ye komut vermez.
- Kişiyi değerlendirmez, puanlamaz, suçlamaz.
- Olasılık uydurmaz, kusur tespiti yapmaz. Kök neden her zaman “hipotez”tir.
- MES, CMMS ya da QMS’in yerini almaz, onların üstünde çalışan bir katmandır.

## Depo yapısı

```
prototype/index.html        Tek dosya prototip: arayüz, kod hesapları, ajan akışları, gömülü veri
data/gen_synthetic_data.py  Sentetik tesis üreticisi
data/data.json              Üretilmiş veri
docs/ARCHITECTURE.md        Katmanlar, veri modeli, kod ve GenAI ayrımı, prompt kuralları, çıktı şemaları
docs/SYNTHETIC_DATA.md      Verinin nasıl üretildiği ve sınırları
docs/DEMO.md                Adım adım demo turu
docs/CLAUDE_CODE_PLAN.md    Ürünleştirme için görev planı
docs/images/                Canlı prototipten ekran görüntüleri
```

## Yol haritası

1. Ajan çağrılarını tarayıcıdan bir sunucu tarafı uç noktasına taşıyan ince bir adaptör, böylece prototip kendi model erişiminizle de çalışır. API anahtarı tarayıcıda tutulmaz.
2. Gömülü veri yerine gerçek bağlantılar: OPC-UA/MQTT sensör, ERP bakım modülleri, RFID, vardiya planı.
3. Uygulama içi ses kaydı ve sunucu tarafında yazıya çevirme.
4. Rol tabanlı aksiyonların kabul ve ret geri bildirimiyle olasılık kalibrasyonu.

## Bilinen sınırlar

- Sentetik veri test amaçlıdır. Prototipin bu veride her şeyi yakalaması gerçek bir tesiste aynı sonucu vereceği anlamına gelmez.
- Eşikler ve gürültü seviyeleri gerçek makinelerden kalibre edilmedi.
- Canlı prototipte mikrofon doğrudan kullanılamıyor, sayfa telefon klavyesinin dikte özelliğine geçiyor.
- E-posta gönderilmez, yalnızca taslak ve onay vardır.
