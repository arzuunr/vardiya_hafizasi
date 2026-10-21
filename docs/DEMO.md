# Demo turu (yaklaşık 2 dakika)

Canlı prototipte ajan özellikleri çalışır: https://claude.ai/artifact/AvF5s4LY8wsNi71X9fczkV
Yerelde açarsanız 1, 4 ve 5. adımlar çalışır, ajan adımları kapalıdır.

Ajan bir isteğe 20–60 saniye düşünebilir. Birine göstermeden önce devir dosyasını bir kez oluşturun.

## 1. Hat haritası
**Tıkla:** Pres-3

Makinenin rengi sensör eşiklerinden ve geçmiş duruşlardan kodla hesaplanır. Pres-3 sarı, çünkü sabah 06:12’de geçmişte duruşa dönmüş bir desen görüldü. Basınç grafiği her sabah aynı saatte kritik eşiğin altına iniyor. Olasılık %71, yanında n=7: yedi örnekten çıkan bir oran, kesin tahmin değil.

Aşağı kaydırınca **Anomaliler** bölümü var. Her anomalinin yanındaki **Kök neden** tuşu 5 Neden, balık kılçığı ve “duruşa dönmeden yapılacaklar” üretir.

## 2. Saha telefonu
**Tıkla:** Saha telefonu → Sesli yaz
**Söyle ya da yaz:** `akşam basınç yine titredi valfe dokunmadım bakımcı yok`
**Tıkla:** Deftere işle

Ajan dağınık notu düzgün bir kayda çevirir, Pres-3’e bağlar ve sonraki vardiyaya iş bırakır.

## 3. Vardiya devri
**Seç:** Sabah → Akşam
**Tıkla:** Devir dosyası oluştur

Sağ panel kodun hazırladığı bağlamdır: riskler ve akşam ekibindeki yetkinlik açığı. Sol panel ajanın yazdığı devir dosyasıdır. Bir kaynak rozetine tıklayınca dayandığı kayıt açılır.

## 4. Uyarılar ve not kontrolü
**Tıkla:** Uyarılar

En üstte yanlış girilmiş notlar var. Pres-2’ye girilmiş not kaynak robotu terimleri içeriyor.
**Tıkla:** Kaynak Robotu-2 olarak düzelt

Not doğru makinenin geçmişine taşınır, bir sonraki devir düzeltilmiş kaydı görür.

## 5. İzin dönüşü
**Tıkla:** İzin dönüşü → Dönüş brifingi hazırla

İzindeki ustanın makinelerinde değişenler ve onu bekleyen işler.

## Sık sorulan

**Olasılığı model mi uyduruyor?** Hayır. Kod geçmişte bu desenden sonra kaç kez duruş olduğunu sayar. Ajan sayıyı yalnızca açıklar, kanıt kontrolü koddan farklı bir sayıyı ekrana çıkarmaz.

**Çalışanlar bunu gözetim olarak görmez mi?** Kayıt kişiyi değil makineyi anlatır. Sistem kimseyi puanlamaz. Not kontrolü bile “bu bir suçlama değil” der. Cezalandırılacağını düşünen çalışan not bırakmaz, bu yüzden bu tasarımın merkezinde.

**Mevcut sistemlerin yerini mi alıyor?** Hayır. MES, CMMS ve QMS’in üstünde çalışan bir bilgi katmanıdır. Makineye komut vermez, kalite kararı vermez.
