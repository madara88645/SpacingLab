# SpacingLab — Durum raporu (7 Eylül 2026)

**Tek cümlede bulgu:** Küçük bir dil modeline aynı bilgiyi 5 kez öğretirken tekrarları
arka arkaya vermek işe yaramıyor (bilgi öğreniliyor ama 50 adım içinde siliniyor); aynı
5 tekrarı 16–64 adım arayla vermek bilginin sonradan gelen alakasız eğitimden sonra bile
kalmasını sağlıyor, 64'ten daha geniş aralık ise ek bir şey kazandırmıyor.

Bu, 70 koşu ve 5 ayrı çalışmayla sınandı; her çalışmanın tahmini koşulardan önce yazıldı
ve düşen tahminler aşağıda olduğu gibi duruyor.

---

## 1. Ne yaptım (deneyin özeti)

- **Model:** GPT-2 (124 milyon parametre; laptopta çalışan küçük bir dil modeli).
- **Bilgi:** 200 uydurma cümle, örneğin "Sheipiakvuk'un başkenti Prothkunshend'dir".
  İsimler uydurma, model önceden bilemez; başlangıç puanı tam 0.
- **Öğretme:** 700 adımlık bir pencerede her bilgi 5 kez gösteriliyor. Modele her adımda
  15 parça sıradan Wikipedia metni veriliyor; bilgi cümlesi bazı adımlarda bu paketin
  yanına ekleniyor. **Tek değişken:** bir bilginin 5 gösterimi arasında kaç adım var:
  1 (arka arkaya), 4, 16, 64 (sonradan 128 ve 256 de eklendi).
- **Adil kıyas:** Her koşul aynı sayıda adım, aynı Wikipedia metni, aynı toplam gösterim
  görüyor; bir bilginin *son* gösterim anı koşullar arasında aynı. Böylece "daha yakın
  zamanda gördü" bahanesi yok.
- **Unutturma:** 1500 adım daha eğitim: Wikipedia + 50 tane *yeni* uydurma bilgi. Eski
  200 bilgi bir daha gösterilmiyor.
- **Sınav:** Modele "Sheipiakvuk'un başkenti" deyip devamını yazdırıyorum; doğru ismi
  yazarsa puan. Ayrıca NLL (modelin doğru cevaba ne kadar "şaşırdığı"; düşükse iyi) ve
  sonradan eklenen iki ölçü daha (aşağıda).
- **Tekrar ve kayıt:** Ana kıyas 5 tohumla (seed; rastgelelik ayarı), diğerleri 3'er.
  Ne ölçeceğim, ne beklediğim, hangi tuzaklara bakacağım hiçbir sayı görmeden önce
  dosyaya yazıldı (PREREGISTRATION.md); sonradan 8 ek, hepsinin tarihi ve sebebi orada.
  Aynı koşuyu iki kez koşunca fark 0,014; bundan küçük farklar okunmuyor.

## 2. Sayılar (ana kıyas, Study 1)

| 5 gösterim arası | pencere sonunda doğru | unutturma sonunda doğru | unutturma boyunca ortalama |
|---|---|---|---|
| 1 adım (arka arkaya) | %3 | %0 | 0,001 |
| 4 adım | %8 | %1 | 0,023 |
| 16 adım | %35 | %5 | 0,124 |
| 64 adım (aralıklı) | %65 | %14 | 0,285 |

Aralıklı − arka arkaya farkı 5 tohumun 5'inde aynı yönde (+0,24 ile +0,35 arası);
tohumdan tohuma dalgalanma 0,04, yani fark gürültünün 7 katı.

**Asıl sürpriz:** arka arkaya gösterilen bilgi *öğrenilmiyor* değil. Kendi 5. gösteriminin
hemen ardından sorarsan arka arkaya **%43**, aralıklı **%81** doğru. Pencere sonunda (en
fazla 444 adım sonra) arka arkaya %3, aralıklı %65. Sorun "az öğrenmek" değil, "hızla
erimek". Arka arkaya öğrenen model doğru türde uydurma isimler üretiyor ("Zusvrox" gibi)
ama doğru olanı değil: cümlenin *biçimini* öğrenmiş, *bilgiyi* kaybetmiş.

## 3. Dürüst not: yazdığım hipotez kâğıt üstünde düştü

Ön kayıttaki karar kuralımın 3. maddesi "iki koşul başta eşit öğrenmiş olsun, sonra kim
daha çok hatırlıyor bakalım" diyordu. Arka arkaya koşulu pencere sonunda bile neredeyse
sıfır olduğu için bu kıyas yapılamadı. Kurala göre "hipotez desteklenmedi" yazıyorum.
Ayrıca ön kayıtta "pencere sonu puanı %50–95 arasında olmalı, dışına çıkarsa kalibrasyon
hatası diye yazılır" demiştim; arka arkaya (%3), 4 adım (%8) ve 16 adım (%35) bu bandın
dışında. Bu bir kalibrasyon hatasıdır, öyle raporlanıyor, hiçbir ayar sonradan
değiştirilmedi. Bunun yerine çıkan bulgu daha güçlü ama farklı bir cümle: aralık,
bilginin *ne kadar süre dayandığını* değiştiriyor.

## 4. Dört ek deney: arka arkayayı ne kurtarmıyor? (Study 2)

| Soru | Beklentim | Sonuç |
|---|---|---|
| Arka arkaya 10 veya 20 kez göstersem? | Kurtarmaz | Doğru. %99 öğreniyor, pencere sonunda %3–6. |
| Sebep, eğitim algoritmasının "hız kazanma" özelliği (momentum) mi? | Hayır | Doğru, ama dar okunmalı: Adam'ın birinci-moment momentumu (β₁) kapalıyken fark aynen duruyor (+0,30); β₂ kısmı (geçmiş gradyan büyüklükleri) hâlâ açık, o test edilmedi. Momentum arka arkaya *kodlamayı* bozuyormuş (%43 → %96), erimeyi değil. |
| Modelin tamamı yerine küçük bir ek parça eğitilirse (LoRA)? | Aynı yön | Yarı-sonuç. Pencere sonunda yön aynı (%31 vs %1,5) ama LoRA bu kurulumda hiçbir bilgiyi 1500 adım tutamıyor; kıyas tabana çakıldı, büyüklük okunmuyor. |
| Arka arkaya ama her seferinde farklı cümleyle? | Kısmen kurtarır | **Yanıldım.** Kurtarmıyor. (Bu deneyin sınavı adil değildi; düzeltmesi Study 4'te.) |

## 5. Silindi mi, gizlendi mi? (Study 3)

Senin ilettiğin itiraz haklıydı: "accuracy sıfır ama NLL düşüyor, demek ki bir şey var".
İki ölçü ekledim:

- **Ayrım testi:** doğru cevabın NLL'i ile *yem* cevabın (aynı kalıptaki başka bir uydurma
  isim) NLL'i karşılaştırılıyor. "Cevap uydurma bir isim olur" biçimini öğrenmek ikisini
  eşit etkiler; fark sadece bu bilgiye ait olanı gösterir. Sonuç: arka arkaya koşulda
  küçük bir iz var (+0,24…+0,46), aralıklıda on kat büyük (+2,1…+2,6). Arka arkaya
  koşulun NLL'indeki iyileşmenin **%90'ı biçim öğrenmesi**, bilgi değil.
- **Tasarruf testi (Ebbinghaus):** unutturma sonunda her eski bilgiye 1 gösterim, hiç
  görülmemiş 200 kontrol bilgisine de 1 gösterim. Aralıklı bilgiler tek gösterimle
  %16–22'den %33–40'a çıkıyor. Arka arkaya bilgiler **%0'dan %0'a**; kontrol de %0.

Yani arka arkaya öğretilen bilgi kâğıt üstünde tamamen silinmemiş ama tek hatırlatmayla
geri gelmiyor; işe yarar anlamda gitmiş. Tahminimin yarısı tuttu (iz var), yarısı
tutmadı (geri çağrılabilir değil).

## 6. Farklı cümleler, adil sınavla (Study 4)

Study 2'deki sınav hep aynı kanonik cümleyle yapılıyordu; kopyalı koşul o cümleyi 5 kez,
farklı-cümleli koşul 1 kez görmüştü. 12 koşu daha: her koşul bir de **hiç görülmemiş 6.
bir cümle kalıbıyla** sınandı.

| unutturma boyunca ortalama doğruluk | bilinen cümle | görülmemiş cümle |
|---|---|---|
| aralıklı, 5 kopya | **0,31** | 0,06 |
| aralıklı, 5 farklı cümle | 0,09 | **0,11** |
| arka arkaya (ikisi de) | 0,00 | 0,00 |

Pencere sonunda daha net: 5 kopya bilinen cümlede %67, görülmemişte %28 (40 puan düşüş);
5 farklı cümle %35 ve %37 (düşüş yok). **Kopya, çalışılan cümlede daha iyi; farklı cümleler yeni bir ifadeye aktarımda daha iyi.** Ön kayıtlı kural üç tohumda da geçti ama kıl payı (eşik 0,041; farklar
0,056 / 0,043 / 0,044); pencere sonu ve ayrım ölçüsünde fark daha geniş olduğu için
sonuca güveniyorum, "büyük etki" demiyorum. Study 2'deki "farklı cümleler zarar veriyor"
sonucu sınavın hatasıymış, düzeltildi. Bu 12 koşu ayrıca ana sayıları üçüncü kez birebir
tekrarladı (0,306 vs 0,298).

## 7. Aralık ne kadar açılmalı? (Study 5)

Pencere 1400 adıma çıkarıldı, aralıklar 1 / 16 / 64 / 128 / 256 yeniden koşuldu (15 koşu).

| aralık | 1 | 16 | 64 | 128 | 256 |
|---|---|---|---|---|---|
| unutturma boyunca ortalama (3 tohum) | 0,002 | 0,128 | **0,261** | 0,238 | 0,231 |

1 < 16 < 64 her tohumda geçerli. 64'ten sonra eğri **düzleşiyor**: 128, üç tohumun
ikisinde 64'ün altında; tohumlar arası dalgalanma aralıklar arası farktan büyük. "128 daha
iyi olur" tahminim düştü; kural "doyuma ulaşıyor" dedi. Mekanik ipucu: aralık çok
büyüyünce 5. gösterim geldiğinde önceki gösterimler çoktan erimiş oluyor, kodlama
zayıflıyor (%84 → %61 → %58). İnsan hafızasındaki "çok fazla aralık da işe yaramaz"
bulgusuyla (Cepeda 2008) aynı biçim.

## 8. Toplam tablo

| Soru | Cevap |
|---|---|
| Aralıklı > arka arkaya? | Evet, büyük fark, üç kez tekrarlandı |
| Daha çok arka arkaya tekrar kurtarır mı? | Hayır |
| Momentum sebep mi? | β₁ momentumu değil; Adam'ın geri kalanı test edilmedi |
| LoRA'da da mı? | Yön aynı, ölçüm tabanda |
| Arka arkaya bilgi gizli mi, silinmiş mi? | Küçük iz var, geri çağrılamıyor |
| Farklı cümleler işe yarar mı? | Arka arkayayı kurtarmıyor; aralıklıda cümle-ezberi yerine bilgi satın alıyor |
| Aralık ne kadar açılmalı? | En az 16, 64 yeterli, fazlası bir şey kazandırmıyor |
| Sıradan karıştırma yeter mi? | Evet; düzenli aralığa eşit ya da biraz daha iyi |

## 9. Bu ne göstermiyor

- Tek model (GPT-2, küçük), tek tür bilgi (tek cümlelik uydurma çiftler), tek girişim
  metni (Wikipedia), tek öğrenme hızı. Büyük modeller ve gerçek dünya bilgisi için
  söylenecek bir şey yok.
- "Neden eriyor" sorusunun cevabı yok. Momentum değil, az öğrenme değil, geri
  çağrılabilir değil; o kadar. Beynin "araya bir şey girince pekişir" hikayesine
  benziyor ama bu bir benzetme, kanıt değil.
- Farklı-cümle faydası küçük ve kıl payı; daha çok tohum gerekir.
- 64'ten sonraki düzlüğün konumu unutturma süresine bağlı olabilir (insanlarda öyle);
  bunu değiştirmedim.

## 10. Pratik çıkarım

Bir modele tekrarla bilgi öğretiyorsan tekrarları birbirinden **en az 16, tercihen 64
adım** uzağa koy; daha fazlası gerekmiyor. Aynı konudaki dokümanları peş peşe dizen veri
hatları tam tersini yapıyor. Tekrar sayısını artırmak, momentumu kapatmak veya cümleyi
değiştirmek arka arkaya gösterimi kurtarmıyor. Tekrarlar zaten aralıklıysa, cümleyi
değiştirmek "ezber cümle" yerine "cümleden bağımsız bilgi" satın alıyor; hangisini
istediğine göre seç.

## 11. Dış hakem değerlendirmesi (ChatGPT Pro, 7 Eylül)

Projenin özetini ChatGPT Pro'ya verdim (prompt: docs/chatgpt_pro_prompt.md; rapor:
docs/external_review_chatgpt_pro_2026-09-07.md, 7.200 kelime). Genel hükmü: **"Bulgu
gerçek ve büyük, ama mekanizma keşfi değil; dikkatli sınırlandırılırsa yararlı bir
zamanlama bulgusu ve ölçüm dersi."** Bizim yazdığımızla uyumlu. Haklı bulduğum itirazlar:

| İtiraz | Ne demek | Ne yapacağız |
|---|---|---|
| **Gerçekten sadece aralık mı değişti?** | Kayıp, bir adımdaki cümle sayısına bölünüyor. Bir adımda kaç bilgi cümlesi olduğu koşula göre farklıysa bir cümlenin *etkin ağırlığı* da farklı. Ölçmedim. | Kayıtlardan hesaplanır, koşu gerekmez. **Önce bu.** |
| **Sıradan karıştırma zaten yeter mi?** | Pratikte kimse 5 kopyayı arka arkaya koymaz; rastgele yerleştirmeyle kıyas yok. Pilotlarda rastgele ≈ aralıklı çıkmıştı ama tek tohum, kısa unutturma. | 3 koşu, ~30 dk. |
| **"Momentum sebep değil" fazla geniş** | Sadece β₁ kapatıldı; Adam'ın β₂ kısmı duruyor. | Dil düzeltildi (bölüm 4 ve 8). |
| **Dil fazla keskin** | "50 adımda sildi" → "doğru cevabı üretme başarısı 50 adımda düştü". "Kopya cümleyi, farklı cümle bilgiyi öğretir" → "aktarımda daha iyi". "%90 biçim" hesabı seçilen yeme bağlı. | Düzeltildi. |
| **Tekrar sayısı az** | Study 4'ün farkları eşiği 0,002–0,015 ile geçiyor; K=10/20 tek tohum. | Kabul; "kıl payı" zaten yazılı. Daha çok tohum gerekirse sonra. |

Kısmen haklı: Chang ve ark. 2024'ün kopya koşulu da 100 adım aralıklıymış; "kopya vs
paraphrase farkı" yeni değil, bizim katkı "sabit gösterim sayısı + eşlenmiş son gösterim
altında aralığın kendisini ayırmak". Yanlış: "70 koşu bitmiş mi belirsiz" (bitmiş);
"0,01 içinde tekrarlandı" itirazı haklı çıktı çünkü 3 tohumu 5 tohum ortalamasıyla
karşılaştırmışım (düzeltildi: 3 tohum vs 3 tohum, fark 0,008).

Yayın görüşü: blog + depo şimdi paylaşılabilir; arXiv teknik rapor mümkün; ana konferans
değil; TMLR ancak ek kontrollerle. Önerdiği başlık: "Sabit gösterim bütçesinde tekrar
zamanlaması: GPT-2'de edinim, unutma ve soru biçiminin ayrıştırılması". "İnsan benzeri
hafıza pekişmesi" iddiası yazılmayacak.

## 12. Sırada ne var (yeni plan)

Hakemin sırası doğru: önce kıyasın adilliğini kanıtla, sonra pratik taban çizgisi, en son
mekanizma. Adımlar:

1. **Etkin ağırlık denetimi (0 koşu, bugün).** Her koşu ve adım için: adımdaki bilgi
   cümlesi sayısı, her cümlenin kayıptaki payı, koşullar arası dağılım. Fark anlamsızsa
   (beklentim: ortalama cümle/adım her koşulda 1,4; pay ≈ 1/16,4) "sadece aralık değişti"
   cümlesi ayakta kalır. Farklıysa ana yorum "bu yerleştirme düzeninin toplam etkisi"
   diye daralır.
2. **Rastgele yerleştirme taban çizgisi (3 koşu, ~30 dk).** Her bilginin 5 gösterimi
   rastgele adımlara. Tahmin: aralıklıya (64) yakın çıkar, arka arkayadan çok uzak.
   Sonuç ne olursa olsun pratik cümle netleşir: "sıradan karıştırma yeter, tek tehlike
   kopyaların kümelenmesi" ya da "düzenli aralık karıştırmadan da iyi".
3. **Sonra karar:** 1 ve 2 temizse blog yazısı + depo paylaşımı (hakemin önerdiği
   başlıkla, H1'in düşüşü merkezde). Mekanizma deneyleri (tek bilgiyi tek başına enjekte
   etmek; β₂ kapalı Adam; bozucu veri türü dalları) ancak bundan sonra ve sen istersen.
4. **Yapmayacağız:** LoRA'yı kalibre etmeden tekrar denemek; daha büyük model; "64 evrensel
   optimum" iddiası.

## 13. Hakemin iki denetimi yapıldı (Study 6, 7 Eylül)

**6a. Sadece aralık mı değişti?** Kayıp her adımda cümle sayısına bölündüğü için arka
arkaya yığılan gösterimler biraz daha az ağırlık alıyor: **%2,8 daha az** (kayıtlardan
hesaplandı, koşu yok). Ön kayıttaki %5 eşiğinin altında; yönü etki lehine ama Study 2'de
2–4 kat gösterim bile kurtaramamıştı, o yüzden %3 farkı açıklayamaz. Ana bulgu ayakta.

**6b. Sıradan karıştırma zaten yeter mi?** Her bilginin 5 gösterimi pencereye rastgele
dağıtıldı (3 tohum). Sonuç: rastgele 0,36, düzenli 64 aralık 0,30, arka arkaya 0,00.
Rastgele, düzenli aralığa **eşit ya da biraz daha iyi** (+0,09 / +0,03 / +0,07; "daha
iyi" için 3/3 eşik üstü gerekiyordu, 2/3 çıktı). Küçük bir çekince: rastgele koşulda son
gösterimler ortalamada biraz daha geç, yani hafif "yeni gördü" avantajı var.

**Pratik cümle değişti:** "aralık dayat" değil, **"karıştır, ve kopyaları yeniden
kümeleyen bir şey olmasın."** Tehlike programın yokluğu değil; aynı kaynaktaki dokümanları
peş peşe dizmek, tekrar örnekleri aynı parçaya yığmak gibi kümeleyen adımlar.

## 14. Sırada ne var (güncel)

1 ve 2 temiz çıktı. Şimdi: blog yazısı + depo paylaşımı (hakemin önerdiği başlıkla,
düşen H1 merkezde). Mekanizma deneyleri (tek bilgiyi tek başına enjekte etmek; β₂ kapalı
Adam) sen istersen.

## 15. Kayıt

- Depo: ~/Developer/personal/SpacingLab; 73 koşu, 47 commit, GitHub'a gönderilmedi.
- İngilizce yazı: README.md. Ön kayıt + 8 ek: PREREGISTRATION.md. Literatür: docs/literature.md.
- Dış hakem raporu ve promptu: docs/external_review_chatgpt_pro_2026-09-07.md, docs/chatgpt_pro_prompt.md.
- Grafikler: results/retention.png (Study 1), results/study2.png (Study 2).
- Yol boyunca düzeltilen hatalar: LoRA ilk iki öğrenme hızında hiç öğrenmedi (grid
  genişletildi, kayda yazıldı); 20 gösterimli kontrol ilk denemede kod hatası verdi
  (düzeltildi); bir koşu ortam yenilenirken öldü, tekrar koşuldu; Sonnet eleştirmen
  açılış cümlesinde karışık zaman noktaları buldu, düzeltildi.
