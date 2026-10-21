# Sentetik veri

Veri `data/gen_synthetic_data.py` ile üretilir. Rastgele bir tesis değil, sistemin her yeteneğini sınayan **senaryolar** önce tasarlandı, veri bu senaryoları içerecek şekilde üretildi.

## Adımlar

1. **Sabit başlangıç:** `random.seed(7)`, her çalıştırmada aynı veri. “Şimdi” 20 Ekim 2026, 13:50.
2. **Makineler:** 9 makine, 3 hat ve yardımcı tesis (3 hidrolik pres, 2 kaynak robotu, 2 CNC, konveyör, kompresör), harita konumlarıyla.
3. **Eşikler:** Her makine tipi için metrik, birim, uyarı ve kritik eşik, yön. Gerçek bir makinenin eşikleri değildir.
4. **Sensörler:** Son 72 saat, saatlik. `taban + gauss(0, gürültü)` ve üstüne senaryo:
   - Pres-3 basıncı 06:00 ve 07:00’de ~171 bar (soğuk başlangıç)
   - Kaynak Robotu-2 torç sıcaklığı saatte +0,25 °C
   - CNC-2 titreşimi saatte +0,042 mm/s
   - Konveyör-A akımı son saatte sıfır
5. **Duruşlar ve desenler:** Pres-3 için 30 günde 7 sabah deseni, 5’inin ardından 3–11 saat içinde duruş, bugün 06:12’de yeni desen. Kod 5/7 = %71 bulur, script bunu kendisi doğrular. Kaynak Robotu-2 için aynı kurgu. Duruşlarda operatör cümlesi ve ERP kodu ayrı, bazıları bilerek çelişkili.
6. **RFID, iş emirleri, personel:** 9 bileşen (Pres-3 pompası %92, Kaynak Robotu-2 nozulu %105), 4 iş emri, 14 kurgusal kişi. Hasan Usta izinde, yarın dönüyor. Akşam vardiyasında hidrolik yetkin bakımcı bilerek yok.
7. **Saha notları:** 10 not, argo ve yazım hatalarıyla, 3’ü aynı sorunu farklı kelimelerle anlatan ramak kala.
8. **Sayfada eklenenler:** Not kontrolü için iki yanlış not (`LG-111` yanlış makine tipi, `LG-112` sensörle çelişen değer) ve bir not saatinin vardiyaya uydurulması.

## Gömülü senaryolar

1. Pres-3 soğuk başlangıç: desen, %71 (n=7), sabaha aktarılmamış gece notu, ömrünün sonundaki pompa, yanlış kodlanmış ERP duruşları.
2. Kaynak Robotu-2: yükselen torç sıcaklığı (kritiğe ~8 saat), ömrü aşılmış nozul, 3 ramak kala.
3. CNC-2: yükselen titreşim (kritiğe ~50 saat).
4. Konveyör-A: malzeme yok, makine arızası değil.
5. Hasan Usta: izin dönüşü, notlarda adı geçen bekleyen iş.
6. Akşam vardiyası yetkinlik açığı.
7. Yanlış girilen iki not.

## Sınırlar

- Veri test amaçlıdır. Sistemin bulması gerekenler bilerek yerleştirildi. Prototipin bu veride her şeyi yakalaması gerçek bir tesiste aynı başarıyı göstereceği anlamına gelmez.
- Gürültü, duruş sıklığı ve süreleri gerçek bir tesisten kalibre edilmedi.
- Tüm isimler kurgusaldır.
