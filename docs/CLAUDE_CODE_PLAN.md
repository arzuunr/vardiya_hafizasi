# Devir Teslim Ajanı · Claude Code Çalışma Planı (v3, üretim mavi yaka + sigorta)

Claude Code bu dosyayı sırayla uygular. Kabul kriteri doğrulanmadan sonraki göreve geçilmez. Tüm veri sentetiktir. T1–T8 ilk sürüm, T9 sonrası yol haritası.

Başlangıç komutu:

```
claude "PLAN.md ve CLAUDE.md dosyalarını oku. T1'den başla. Her görev sonunda kabul kriterini çalıştırıp sonucu raporla. Kabul geçmezse düzelt, sonra devam et."
```

## Mimari özeti

```
L0 adapters → L1 normalize (Event) → L2 entity resolution (EntityLink)
→ L3 semantic graph (nodes, edges, provenance) → L4 analytics (code only)
→ L5 context builder (ContextPack) → L6 agents (GenAI)
→ L7 evidence validator → L8 approval → L9 feedback → L10 external share
```

Ajanlar birbirini çağırmaz. Hepsi L5'ten ContextPack alır, taslak üretir, L7 ve L8'den geçer.

## Depo yapısı

```
devir-teslim-ajani/
  PLAN.md
  CLAUDE.md
  config/
    automotive_supplier.yaml  food.yaml  chemical.yaml
  data/
    <sector>/ voice_notes.json (transkript + ses_id) downtime.csv work_orders.json
              near_miss.json sensor.csv rfid.csv machine_qr.json
  prompts/
    handover_p1_extract.md
    handover_p2_questions.md
    handover_p3_document.md
    skill_feedback.md
    briefing.md            (T9)
    action_card.md         (T9)
    evidence_pack.md       (T10)
  src/
    adapters/              L0, her kaynak için bir dosya
    normalize.py           L1
    entities.py            L2
    graph.py               L3, networkx tabanlı, JSON dışa aktarım
    analytics.py           L4, MTBF, MTTR, Pareto, conditional probability
    context.py             L5
    chain.py               L6, --mode manual | api
    validate.py            L7
    feedback.py            L9
    build_ui_data.py
  ui/index.html
  eval/cases.json  eval/run_eval.py  eval/report.md
  out/<sector>/<mode>/...
```

## CLAUDE.md

```
- Kullanıcıya dönük metin Türkçe. Kod, alan ve değişken adları İngilizce.
- Python 3.11, stdlib + pyyaml + networkx. anthropic SDK yalnızca chain.py --mode api içinde.
- Graf makine merkezlidir. İşçi adı sigorta çıktısına girmez, yalnızca rol ve vardiya.
- Gerçek kişi, kurum, marka adı yok. Sentetik: Pres-3, RFID-4471, Karar 2026/41, Marka-X.
- Prompt gövdesi sektörden bağımsız. Sektör içeriği yalnızca config/*.yaml'dan {değişken} olarak gelir.
- Hesap, eşik, olasılık yalnızca analytics.py ve rules içinde. Prompt'a [KOD ADIMI: ...] işareti konur, sonuç girdi olarak verilir.
- Her olasılık {value, n, window} taşır. n < 10 ise "low_sample: true".
- Her çıktı kalemi node_id taşır. validate.py geçmeyen çıktı out/ altına yazılmaz.
- Metinlerde noktalı virgül ve uzun tire kullanma.
```

## Veri sözleşmeleri

```
Event       {event_id, ts, source, event_type, text, shift_id, author_id}
EntityLink  {event_id, entity_id, confidence, status: linked|ambiguous}
Node        {node_id, node_type, label, attrs}
Edge        {src, dst, edge_type, provenance: {source, event_id, ts, confidence}}
Probability {value, n, window, low_sample}
ContextPack {task, mode, window, role, sector, nodes[], edges[], metrics[]}
HandoverDoc {done[], open_items[], pending_decisions[], tacit_knowledge[],
             watch_list[], questions[], feedback_checklist[], handover_to}
             her kalem: {text, node_ids[]}
```

## Görevler (ilk sürüm)

### T1 · Konfigürasyon
Üç yaml, aynı anahtarlar: `sector`, `asset_type`, `entity_dictionary` (id, label, synonyms), `terminology`, `critical_info_rules`, `sources`, `handover_template`, `modes` (shift, personnel), `idle_task_days: 30`, `repeat_threshold: 3`, `confidence_threshold: 0.7`, `role_matrix`.
Kabul: üç dosyanın anahtar seti `diff` ile aynı, değerler farklı.

### T2 · Sentetik veri
Üç alt sektör için aynı yapı. Vardiya notları kısa, argo ve yazım hatalı sesli not transkripti gibi yazılır. Her sektörde: 2 hat, 6 makine, 30 gün, 3 vardiya/gün. `downtime.csv` (ts_start, ts_end, asset_id, cause_text, shift_id), `work_orders.json`, `shift_notes.json` (serbest Türkçe metin), `sensor.csv` (Pres-3 için hidrolik sıcaklık ve basınç), `rfid.csv` (component_id, asset_id, installed_at, hours).
Zorunlu zor vakalar:
- automotive_supplier: Pres-3'te soğuk başlangıç sonrası basınç düşüşü 7 kez, 5'inde 24 saat içinde duruş. Talimat notu yok, sadece voice_notes'ta "elle ayarlandı".
- food: gece vardiyası sesli notunda "alerjen hattı yıkandı mı emin değilim", sabah vardiyasına hiçbir kayıtta geçmemiş.
- chemical: aynı vanada 3 ramak kala bildirimi, farklı vardiyalar ve farklı kelimelerle, hiçbiri iş emrine dönmemiş.
Kabul: zor vaka kayıtları `grep` ile bulunur, gerçek ad yok, automotive_supplier'da 7 desen ve 5 duruş sayısı script ile doğrulanır.

### T3 · Normalize ve varlık çözümleme (L1, L2)
Kabul: her sektör için 200+ Event, her Event'te `event_id`, `ts`, `shift_id` dolu. Eşleşmeyenler `ambiguous`.

### T4 · Semantik graf (L3)
Düğüm ve kenar tipleri brain notundaki ontolojiye göre. `graph.py --sector automotive_supplier --export out/automotive_supplier/graph.json`. Her kenarda provenance.
Kabul: `Downtime → Asset → Component → WorkOrder → Person → Shift` zinciri en az bir olay için yürünebilir, test bunu yazdırır.

### T5 · Analitik (L4)
MTBF, MTTR, neden Pareto'su, koşullu olasılık: "desen X'ten sonra 24 saat içinde duruş" = olumlu / toplam desen.
Kabul: Pres-3 için `{value: 0.71, n: 7, window: "24h", low_sample: true}` döner.

### T6 · Bağlam derleyici ve prompt zinciri (L5, L6)
`context.py --mode shift --line L1 --shift 2026-10-18-gece` ve `--mode personnel --person teknisyen-07 --from ... --to ...`.
Üç handover prompt'u + `skill_feedback.md` (devralan seviyesi `{receiver_level}` deneyimsiz ise "kontrol et" ve "uzmana sor" maddeleri).
`chain.py --mode manual` doldurulmuş prompt'ları yazar, Copilot çıktısı elle yapıştırılır, model adı `out/.../model.txt`.
Kabul: shift ve personnel modlarında prompt gövdesi aynı, `diff` yalnızca değişkenleri gösterir. Üç sektörde manual çıktı üretilir.

### T7 · Kanıt doğrulayıcı (L7)
Her kalemde node_id var ve grafta mevcut. Metindeki her sayı L4 çıktısıyla birebir. Uymayan kalem `dropped.json`'a.
Kabul: uydurma node_id ve değiştirilmiş bir olasılık testte düşer.

### T8 · Arayüz ve değerlendirme
Mavi yaka görünümü: makine QR ekranı (son 72 saat, en fazla 5 madde, büyük yazı). Amir görünümü: devir dosyası ve onay.
`ui/index.html`, tek dosya, gömülü veri. Sol: vault ağacı ve graf görünümü (düğüme tıklayınca komşular). Orta: not ya da olay. Sağ: mod seçici (Vardiya / Personel), devralan seviyesi, "Devir dosyası oluştur". Sekmeler: Devir Dosyası · Sorular · Dikkat Listesi. Olasılıklarda `n` rozeti, `low_sample` uyarısı. Üstte sektör değiştirici, altta aktif config değişkenleri.
`eval/run_eval.py`: üç zor vaka yakalandı mı.
Kabul: tarayıcıda çift tıkla açılır, konsol hatasız, üç vaka eval'de geçer.

## Görevler (yol haritası)

### T9 · Brifing ve Aksiyon ajanları
`briefing.md`: gün sonu, fabrika müdürü, tek sayfa. `action_card.md`: rol bazlı, `role_matrix` ile görev tanımına düşen kart, Probability zorunlu.
Kabul: her kart bir rol, bir gerekçe, bir Probability ve en az bir node_id taşır.

### T10 · Kanıt Paketi (sigorta) ve L10
`evidence_pack.md`: olay zaman çizelgesi, bakım geçmişi, sensör kanıtı, graf yolu. Kök neden "hypothesis" etiketi zorunlu. Dışa aktarım yalnızca `consent: true` ile.
Kabul: onaysız istek reddedilir, paket hiçbir kişisel değerlendirme içermez.

### T11 · Geri bildirim döngüsü (L9)
Kabul/ret ve gerçekleşen sonuç kaydı, olasılıkların yeniden hesabı, ret gerekçelerinin sınıflanması, sözlük güncelleme önerisi (insan onaylı).

### T12 · Gerçek bağlayıcılar
OPC-UA/MQTT, ERP (SAP PM), PLM, RFID, Obsidian, Trello adaptörleri. Model erişimi kurumun kendi model geçidi ya da Anthropic API üzerinden.

