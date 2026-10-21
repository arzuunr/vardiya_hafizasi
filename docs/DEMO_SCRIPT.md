# Demo ve konuşma metni

## Slayt 4 (yaklaşık 75 sn)

> Size en güçlü örneğimizi göstereyim. Otomotiv yan sanayi tesisinde, Pres-3 için sabah vardiyasından akşam vardiyasına bir devir dosyası.
>
> Girdi, kodun hazırladığı bir bağlam paketi: son 72 saatin sensör verisi, 30 günlük duruşlar, üç saha notu, RFID bilgisi, açık iş emirleri ve akşam ekibi. Hepsi sentetik.
>
> Prompt’un en önemli kısmı KOD ADIMI. Olasılığı, yetkinlik açığını ve eşikleri ajan değil kod hesaplıyor. Pres-3 için yüzde 71, yanında n eşittir 7. Yedi örnekten çıkan bir oran, kesin tahmin değil. Ajan bu sayıyı değiştiremez, sadece açıklar.
>
> Çıktı tek şemaya oturuyor: özet, rol bazlı aksiyonlar, personel önerisi, dikkat listesi. Her maddenin kaynağı var, kaynağı doğrulanamayan madde ekrana çıkmıyor.
>
> Zor vaka: bir operatör “titreşim 5’in üstüne çıktı” notunu yanlışlıkla CNC-1’e girmiş. CNC-1 o saatte 2 gösteriyor. Sistem bunu yakalıyor ve değerin CNC-2 ile uyuştuğunu söylüyor, ama düzeltmeyi kendisi yapmıyor. Kararı amir veriyor. Devir dosyası da gelen amir onaylamadan kimseye gitmiyor.
>
> Sayıyı kod hesaplıyor, metni ajan yazıyor, son sözü insan söylüyor.

“Seviye A” ancak örnekler prototipte çalıştırılıp kanıt dosyasına eklendiyse söylenmeli.

## Uygulama demosu (yaklaşık 90 sn)

Önce prototipi açıp devir dosyasını bir kez oluşturun, ajan 20–60 sn sürebilir.

1. **Hat haritası:** Pres-3’e tıkla. Renk kodla hesaplanıyor, sabah 06:12’de duruşa dönmüş desen görüldü, basınç her sabah eşiğin altında.
2. **Saha telefonu:** “Sesli yaz”, ardından “akşam basınç yine titredi valfe dokunmadım bakımcı yok”, “Deftere işle”. Dağınık not düzgün kayda dönüşüp Pres-3’e bağlanıyor.
3. **Vardiya devri:** Sağda kodun bağlamı ve akşam ekibindeki yetkinlik açığı, solda ajanın devir dosyası. Bir kaynak rozetine tıkla, notun aslı açılsın.
4. **Uyarılar:** Pres-2’ye girilmiş kaynak robotu notu. “Kaynak Robotu-2 olarak düzelt”, not doğru makinenin geçmişine taşınır.
5. **Kapanış:** Sayıyı kod hesaplıyor, metni ajan yazıyor, son sözü insan söylüyor.

**Ters giderse:** Ajan geç cevap verirse sağdaki kod bağlamını anlatın. İzin penceresi çıkarsa onaylayın. İnternet yoksa demo videosuna geçin.

## Jüri soruları

- **Olasılığı model mi uyduruyor?** Hayır, geçmişte bu desenden sonra kaç duruş olduğunu kod sayıyor. Yediden beşi, örneklem küçük olduğu için ekranda yazıyor.
- **Siemens bunu yapmıyor mu?** Siemens kendi ekosisteminde ve mühendislikte güçlü. Biz marka bağımsız bir katmanız, Türkçe saha diline odaklanıyoruz.
- **Gözetim olarak görülmez mi?** Kayıt kişiyi değil makineyi anlatıyor, sistem puan vermiyor. Çalışan cezalandırılacağını düşünürse not bırakmaz, bu yüzden tasarımın merkezinde.
