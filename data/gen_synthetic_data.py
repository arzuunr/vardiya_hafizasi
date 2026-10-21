import json, random, math
from datetime import datetime, timedelta
random.seed(7)
NOW = datetime(2026,10,20,13,50)
def iso(d): return d.strftime("%Y-%m-%dT%H:%M")

machines = [
 {"id":"PRS-1","name":"Pres-1","type":"hydraulic_press","line":"A","x":0,"y":0},
 {"id":"PRS-2","name":"Pres-2","type":"hydraulic_press","line":"A","x":1,"y":0},
 {"id":"PRS-3","name":"Pres-3","type":"hydraulic_press","line":"A","x":2,"y":0},
 {"id":"KYR-1","name":"Kaynak Robotu-1","type":"welding_robot","line":"B","x":0,"y":1},
 {"id":"KYR-2","name":"Kaynak Robotu-2","type":"welding_robot","line":"B","x":1,"y":1},
 {"id":"CNC-1","name":"CNC-1","type":"cnc","line":"C","x":0,"y":2},
 {"id":"CNC-2","name":"CNC-2","type":"cnc","line":"C","x":1,"y":2},
 {"id":"KNV-A","name":"Konveyör-A","type":"conveyor","line":"A","x":3,"y":0},
 {"id":"KMP-1","name":"Kompresör-1","type":"compressor","line":"U","x":3,"y":2},
]
metrics = {
 "hydraulic_press":[{"key":"oil_temp","label":"Yağ sıcaklığı","unit":"°C","warn":62,"crit":70,"dir":"high"},
                    {"key":"pressure","label":"Hidrolik basınç","unit":"bar","warn":185,"crit":175,"dir":"low"}],
 "welding_robot":[{"key":"torch_temp","label":"Torç sıcaklığı","unit":"°C","warn":85,"crit":95,"dir":"high"},
                  {"key":"wire_current","label":"Tel besleme akımı","unit":"A","warn":9,"crit":11,"dir":"high"}],
 "cnc":[{"key":"spindle_vib","label":"İş mili titreşimi","unit":"mm/s","warn":4.5,"crit":7.1,"dir":"high"},
        {"key":"spindle_temp","label":"İş mili sıcaklığı","unit":"°C","warn":60,"crit":70,"dir":"high"}],
 "conveyor":[{"key":"motor_current","label":"Motor akımı","unit":"A","warn":14,"crit":17,"dir":"high"}],
 "compressor":[{"key":"line_pressure","label":"Hat basıncı","unit":"bar","warn":6.2,"crit":5.8,"dir":"low"}],
}
base = {"oil_temp":50,"pressure":205,"torch_temp":70,"wire_current":7,"spindle_vib":2.2,"spindle_temp":45,"motor_current":10,"line_pressure":7.2}
noise = {"oil_temp":2,"pressure":3,"torch_temp":3,"wire_current":0.4,"spindle_vib":0.25,"spindle_temp":2,"motor_current":0.6,"line_pressure":0.1}
sensors = {}
for m in machines:
    series = {}
    for mt in metrics[m["type"]]:
        k = mt["key"]; pts=[]
        for h in range(72,-1,-1):
            t = NOW - timedelta(hours=h)
            v = base[k] + random.gauss(0,noise[k])
            hour = t.hour
            if m["id"]=="PRS-3" and k=="pressure" and hour in (6,7):
                v = 171 + random.gauss(0,2)   # cold-start drop every morning
            if m["id"]=="PRS-3" and k=="oil_temp": v += 4*math.sin(hour/24*2*math.pi)
            if m["id"]=="KYR-2" and k=="torch_temp": v += (72-h)*0.25
            if m["id"]=="CNC-2" and k=="spindle_vib": v += (72-h)*0.042
            if m["id"]=="KNV-A" and k=="motor_current" and h<1: v = 0.4
            pts.append([iso(t), round(v,1)])
        series[k]=pts
    sensors[m["id"]]=series

rfid = [
 {"tag":"RF-4471","machine":"PRS-3","component":"Hidrolik pompa","hours":7360,"limit":8000},
 {"tag":"RF-4472","machine":"PRS-3","component":"Basınç valfi","hours":3100,"limit":6000},
 {"tag":"RF-4401","machine":"PRS-1","component":"Hidrolik pompa","hours":2200,"limit":8000},
 {"tag":"RF-4421","machine":"PRS-2","component":"Hidrolik pompa","hours":5100,"limit":8000},
 {"tag":"RF-5120","machine":"KYR-2","component":"Torç nozulu","hours":525,"limit":500},
 {"tag":"RF-5110","machine":"KYR-1","component":"Torç nozulu","hours":210,"limit":500},
 {"tag":"RF-6201","machine":"CNC-2","component":"İş mili rulmanı","hours":15400,"limit":18000},
 {"tag":"RF-6101","machine":"CNC-1","component":"İş mili rulmanı","hours":6000,"limit":18000},
 {"tag":"RF-7001","machine":"KNV-A","component":"Tahrik motoru","hours":9000,"limit":30000},
]

# downtime history 30 days
downtime=[]; did=800
def add_dt(mid, start, mins, raw, erp_code, shift=None):
    global did; did+=1
    downtime.append({"id":f"DT-{did}","machine":mid,"start":iso(start),"end":iso(start+timedelta(minutes=mins)) if mins else None,
      "minutes":mins,"raw_reason":raw,"erp_code":erp_code})
# PRS-3 pattern days: cold start pressure drop events (pattern) on 7 mornings, 5 followed by downtime
pattern_days=[28,24,19,15,11,6,2]
dt_after=[28,24,15,11,2]
patterns=[]
for d in pattern_days:
    t=(NOW-timedelta(days=d)).replace(hour=6,minute=random.choice([5,10,15,20]))
    patterns.append({"machine":"PRS-3","ts":iso(t),"pattern":"cold_start_pressure_drop"})
    if d in dt_after:
        st=t+timedelta(hours=random.choice([3,5,8,11]))
        k=dt_after.index(d)
        add_dt("PRS-3",st,[45,70,95,120,60][k],["basınç gitti kalıp kapanmadı","pres yine bastırmadı, yağ ısınana kadar bekledik","hidrolik zayıf, pompadan ses var","basınç düştü elle toparladık sonra yine gitti","operatör hatası, kalıp ayarı"][k],
          ["Mekanik","Diğer","Diğer","Mekanik","Operatör"][k])
# today's pattern
patterns.append({"machine":"PRS-3","ts":iso(NOW.replace(hour=6,minute=12)),"pattern":"cold_start_pressure_drop"})
for d in [26,17,9,4,1]:
    st=(NOW-timedelta(days=d)).replace(hour=random.choice([9,14,21]),minute=random.choice([0,20,40]))
    k=[26,17,9,4,1].index(d)
    add_dt("KYR-2",st,[20,25,35,30,25][k],["torç tıkandı temizledik","kaynak dikişi bozuk çıktı, nozul","tel takıldı, nozul çapaklı","gözenek çok, torç ısındı","nozul yine tıkandı"][k],["Mekanik","Kalite","Diğer","Kalite","Mekanik"][k])
    patterns.append({"machine":"KYR-2","ts":iso(st-timedelta(hours=random.choice([2,4]))),"pattern":"torch_temp_high"})
for d in [21,12]:
    patterns.append({"machine":"KYR-2","ts":iso((NOW-timedelta(days=d)).replace(hour=11)),"pattern":"torch_temp_high"})
for d in [20,7]:
    st=(NOW-timedelta(days=d)).replace(hour=10,minute=30)
    add_dt("CNC-2",st,60,"titreşim alarmı verdi, takım değişti",random.choice(["Mekanik"]))
for d in [14,8,3]:
    st=(NOW-timedelta(days=d)).replace(hour=random.choice([8,17]),minute=15)
    add_dt("KNV-A",st,random.choice([30,50]),"malzeme gelmedi bekledik","Malzeme")
add_dt("PRS-1",(NOW-timedelta(days=10)).replace(hour=15),40,"kalıp değişimi uzadı","Planlı")
add_dt("KNV-A",NOW.replace(hour=13,minute=20),None,"bant durdu, malzeme yok depo bekleniyor","Malzeme")
downtime.sort(key=lambda x:x["start"])

work_orders=[
 {"id":"WO-5521","machine":"PRS-3","title":"Hidrolik pompa kontrolü","status":"Açık","priority":"Orta","created":iso(NOW-timedelta(days=11)),"assigned_role":"Bakım Teknisyeni","note":"Pompadan ses şikayeti, parça siparişi bekleniyor"},
 {"id":"WO-5540","machine":"KYR-2","title":"Torç nozulu değişimi","status":"Planlandı","priority":"Düşük","created":iso(NOW-timedelta(days=3)),"assigned_role":"Bakım Teknisyeni","note":"Hafta sonu planlı duruşta"},
 {"id":"WO-5547","machine":"CNC-2","title":"Titreşim ölçümü","status":"Açık","priority":"Orta","created":iso(NOW-timedelta(days=6)),"assigned_role":"Bakım Teknisyeni","note":""},
 {"id":"WO-5550","machine":"KNV-A","title":"Malzeme besleme gecikmesi","status":"Açık","priority":"Yüksek","created":iso(NOW.replace(hour=13,minute=25)),"assigned_role":"Planlama","note":"Depo bilgilendirildi"},
]

staff=[
 {"id":"P01","name":"Hasan Usta","role":"Bakım Teknisyeni","shift":"Sabah","certs":["hydraulic_press","electrical"],"years":22,"leave":{"from":"2026-10-08","to":"2026-10-20"}},
 {"id":"P02","name":"Ayşe Y.","role":"Bakım Teknisyeni","shift":"Sabah","certs":["hydraulic_press","cnc"],"years":6,"leave":None},
 {"id":"P03","name":"Kemal D.","role":"Bakım Teknisyeni","shift":"Akşam","certs":["electrical","welding_robot"],"years":2,"leave":None},
 {"id":"P04","name":"Serkan T.","role":"Vardiya Amiri","shift":"Akşam","certs":[],"years":9,"leave":None},
 {"id":"P05","name":"Gülay E.","role":"Vardiya Amiri","shift":"Sabah","certs":[],"years":12,"leave":None},
 {"id":"P06","name":"Murat K.","role":"Operatör","shift":"Gece","certs":["hydraulic_press"],"years":4,"leave":None},
 {"id":"P07","name":"Emre S.","role":"Operatör","shift":"Sabah","certs":["hydraulic_press","conveyor"],"years":3,"leave":None},
 {"id":"P08","name":"Deniz A.","role":"Operatör","shift":"Akşam","certs":["welding_robot"],"years":1,"leave":None},
 {"id":"P09","name":"Burak O.","role":"Operatör","shift":"Akşam","certs":["hydraulic_press","cnc"],"years":5,"leave":None},
 {"id":"P10","name":"Selin Ç.","role":"İSG Uzmanı","shift":"Sabah","certs":[],"years":7,"leave":None},
 {"id":"P11","name":"Okan B.","role":"Kalite Mühendisi","shift":"Sabah","certs":[],"years":5,"leave":None},
 {"id":"P12","name":"Nermin H.","role":"Fabrika Müdürü","shift":"Sabah","certs":[],"years":15,"leave":None},
 {"id":"P13","name":"Tolga V.","role":"Operatör","shift":"Gece","certs":["welding_robot","cnc"],"years":2,"leave":None},
 {"id":"P14","name":"Fatih R.","role":"Bakım Teknisyeni","shift":"Gece","certs":["cnc","electrical"],"years":8,"leave":None},
]

LC=[0]
def L(h_ago, person, machine, text, kind="note"):
    LC[0]+=1
    return {"id":f"LG-{100+LC[0]}","ts":iso(NOW-timedelta(hours=h_ago)),"person":person,"machine":machine,"raw":text,"kind":kind}
logs=[
 L(7.6,"P06","PRS-3","sabah soğukta basınç yine düştü 170lere indi elle ayarladım valfi biraz açtım sonra düzeldi","note"),
 L(31.5,"P06","PRS-3","ilk vuruşta basınç yok bekledik ısınınca düzeldi","note"),
 L(9,"P13","KYR-2","torç çok ısınıyo dikişte gözenek var nozulu fırçaladım","note"),
 L(20,"P08","KYR-2","kaynak çapağı sıçradı perde yırtık bi tarafı, kimseye bişey olmadı","near_miss"),
 L(56,"P13","KYR-2","perdenin altından kıvılcım geçiyo dikkat","near_miss"),
 L(98,"P08","KYR-2","çapak koluma geldi eldiven vardı sıkıntı yok, perde açık kalmış","near_miss"),
 L(5,"P14","CNC-2","iş milinde uğultu var titreşim değeri yükseliyo ölçüm yapılmalı","note"),
 L(3,"P07","KNV-A","bant boş malzeme gelmedi depoya haber verdim","note"),
 L(26,"P02","PRS-3","pompa sesini dinledim, Hasan Usta dönünce bakalım dedik, parça sipariş edildi mi bilmiyorum","note"),
 L(50,"P07","PRS-1","kalıp değişimi tamam deneme baskısı ok","note"),
]
manual = {
 "hydraulic_press":"Soğuk başlangıçta yağ viskozitesi yüksektir. Isınma çevrimi 10 dk çalıştırılmadan tam basınca çıkılmamalı. Basınç 175 bar altına düşerse pompa emiş hattı ve basınç valfi kontrol edilir. Valf ayarı yalnızca yetkili bakım personeli tarafından yapılır.",
 "welding_robot":"Torç nozulu 500 saatte değiştirilir. Nozulda çapak birikimi torç sıcaklığını ve gözenekliliği artırır. Kaynak perdesi hasarlıysa hücre çalıştırılmaz.",
 "cnc":"İş mili titreşimi 4,5 mm/s üzerinde rulman ve takım tutucu kontrol edilir, 7,1 mm/s üzerinde makine durdurulur.",
 "conveyor":"Malzeme beslemesi kesildiğinde bant boşta çalıştırılmaz.",
 "compressor":"Hat basıncı 6 bar altına düşerse sızıntı kontrolü yapılır.",
}
shifts=[{"name":"Gece","start":"00:00","end":"08:00"},{"name":"Sabah","start":"08:00","end":"16:00"},{"name":"Akşam","start":"16:00","end":"24:00"}]
role_matrix={"pressure_pattern":["Bakım Teknisyeni","Vardiya Amiri"],"rfid_overdue":["Bakım Teknisyeni","Planlama"],"near_miss_repeat":["İSG Uzmanı","Vardiya Amiri"],"vibration_warn":["Bakım Teknisyeni"],"open_downtime":["Vardiya Amiri","Planlama"]}
data={"now":iso(NOW),"site":"Örnek Otomotiv Yan Sanayi · Tesis 1","machines":machines,"metrics":metrics,"sensors":sensors,"rfid":rfid,"downtime":downtime,"patterns":patterns,"work_orders":work_orders,"staff":staff,"logs":logs,"manual":manual,"shifts":shifts,"role_matrix":role_matrix}
json.dump(data,open("data.json","w"),ensure_ascii=False,separators=(",",":"))
print(len(json.dumps(data,ensure_ascii=False))//1024,"KB", len(downtime),"downtimes")
# verify pres-3 probability
from datetime import datetime as D
p=[x for x in patterns if x["machine"]=="PRS-3" and x["ts"]<iso(NOW.replace(hour=0))]
hit=0
for x in p:
    t=D.fromisoformat(x["ts"])
    if any(d["machine"]=="PRS-3" and t<=D.fromisoformat(d["start"])<=t+timedelta(hours=24) for d in downtime): hit+=1
print("PRS-3",hit,len(p))
p=[x for x in patterns if x["machine"]=="KYR-2"]
hit=sum(1 for x in p if any(d["machine"]=="KYR-2" and D.fromisoformat(x["ts"])<=D.fromisoformat(d["start"])<=D.fromisoformat(x["ts"])+timedelta(hours=24) for d in downtime))
print("KYR-2",hit,len(p))
