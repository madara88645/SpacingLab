# SpacingLab — Mehmet için rapor

**Tek cümlede bulgu:** Küçük bir dil modeline aynı bilgiyi 5 kez öğretirken, bu 5 tekrarı
arka arkaya vermek işe yaramıyor (bilgi öğreniliyor ama 50 adım içinde siliniyor); aynı
5 tekrarı 64 adım arayla vermek bilginin sonradan gelen alakasız eğitimden sonra bile
kalmasını sağlıyor.

## Ne yaptım (deneyin özeti)

- **Model:** GPT-2 (124 milyon parametre, küçük ve laptopta çalışan bir dil modeli).
- **Bilgi:** 200 uydurma cümle, örneğin "Sheipiakvuk'un başkenti Prothkunshend'dir".
  İsimler uydurma olduğu için model bunları önceden bilemez; başlangıç puanı tam 0.
- **Öğretme:** 700 adımlık bir pencerede her bilgi 5 kez gösteriliyor. Modele her adımda
  15 parça sıradan Wikipedia metni veriliyor; bilgi cümlesi bazı adımlarda bu paketin
  yanına ekleniyor. Tek değişken: bir bilginin 5 gösterimi arasında kaç adım var?
  **1** (arka arkaya), **4**, **16** veya **64**.
- **Adil kıyas:** Her koşul aynı sayıda adım, aynı Wikipedia metni, aynı toplam gösterim
  görüyor; bir bilginin *son* gösterim anı da koşullar arasında aynı. Böylece "daha yakın
  zamanda gördü" bahanesi yok.
- **Unutturma:** Sonra 1500 adım daha eğitim: Wikipedia + 50 tane *yeni* uydurma bilgi.
  Eski 200 bilgi bir daha gösterilmiyor.
- **Sınav:** Modele "Sheipiakvuk'un başkenti" deyip devamını yazdırıyorum. Doğru ismi
  yazarsa puan. Ayrıca "ne kadar şaşırdığı" (NLL) ölçülüyor, çünkü tam isabet kaba bir ölçü.
- **Tekrar sayısı:** 5 farklı rastgele tohumla (seed) ana kıyas, 3'er tohumla ara aralıklar.
  Toplam 17 + 20 + 6 + 12 + 15 = 70 koşu (2'si sabaha kaldı), hepsi bu laptopta, koşu başına ~9 dakika.
- **Ön kayıt:** Ne ölçeceğimi, ne beklediğimi ve hangi tuzaklara bakacağımı hiçbir sayı
  görmeden önce dosyaya yazıp commit'ledim (PREREGISTRATION.md). Sonradan 5 ek yaptım,
  hepsinin tarihi ve sebebi orada.

## Sayılar

| 5 gösterim arası | pencere sonunda doğru | unutturma sonunda doğru |
|---|---|---|
| 1 adım (arka arkaya) | %3 | %0 |
| 4 adım | %8 | %1 |
| 16 adım | %35 | %5 |
| 64 adım (aralıklı) | %65 | %14 |

Aralıklı − arka arkaya farkı 5 tohumun 5'inde de aynı yönde; tohumdan tohuma dalgalanma
(0,04) farkın (0,29) yanında küçük.

Asıl sürpriz şu: arka arkaya gösterilen bilgi *öğrenilmiyor* değil. Her bilginin kendi
5. gösteriminin hemen ardından sorarsan arka arkaya **%43**, aralıklı **%81** doğru
(20 kez arka arkaya gösterince %99). Pencere sonunda (en fazla 444 adım sonra) arka
arkaya %3, aralıklı %65. Yani sorun "az öğrenmek" değil, "hızla erimek".

Bir de itiraf: ön kayıtta "pencere sonu puanı %50-95 arasında olmalı, dışına çıkarsa
kalibrasyon hatası diye yazılır" demiştim. Arka arkaya (%3), 4 adım (%8) ve 16 adım
(%35) bu bandın dışında. Bu bir kalibrasyon hatasıdır ve öyle raporlanıyor; hiçbir
ayar sonradan değiştirilmedi.

## Dürüst not: yazdığım hipotez teknik olarak düştü

Ön kayıttaki karar kuralımın 3. maddesi şuydu: "İki koşul başta eşit öğrenmiş olsun,
sonra kim daha çok hatırlıyor bakalım." Arka arkaya koşulu pencere sonunda bile neredeyse
sıfır olduğu için bu kıyas yapılamadı. Kurala göre "hipotez desteklenmedi" yazıyorum.
Bunun yerine çıkan bulgu daha güçlü ama farklı bir cümle: aralık, bilginin *ne kadar
süre dayandığını* değiştiriyor.

## Dört ek deney (her biri çalışmadan önce kayda yazıldı)

| Soru | Beklentim | Sonuç |
|---|---|---|
| Arka arkaya 10 veya 20 kez göstersem kurtarır mı? | Hayır | Doğru çıktı. %99 öğreniyor, pencere sonunda %3-6. |
| Sebep, eğitim algoritmasının "hız kazanma" özelliği (momentum) mı? | Hayır | Doğru çıktı. Momentum kapalıyken fark aynen duruyor (+0,30). |
| Modelin tamamı yerine küçük bir ek parça eğitilirse (LoRA) aynı mı? | Aynı yön | Yarı-sonuç. Pencere sonunda yön aynı (%31 vs %1,5) ama LoRA bu kurulumda hiçbir bilgiyi 1500 adım tutamıyor; kıyas tabana çakıldı. |
| Arka arkaya ama her seferinde farklı cümleyle söylersem aralığın yerini tutar mı? | Kısmen tutar | **Yanıldım.** Hiç tutmuyor. Üstelik farklı cümleler aralıklı koşulda da puanı düşürdü. Ama sınav tek bir cümle biçimiyle yapılıyor ve o biçim bu koşulda sadece 1 kez görüldü; bu yüzden deney bu soruyu temiz cevaplamıyor. |

## Ek soru: silindi mi, gizlendi mi? (senin ilettiğin itiraz)

Danıştığın model haklıydı, iki ölçü ekledim:

- **Ayrım testi:** doğru cevabın NLL'i ile *yem* cevabın (aynı kalıptaki başka bir
  uydurma isim) NLL'i karşılaştırılıyor. "Cevap uydurma bir isim olacak" biçimini öğrenmek
  ikisini eşit etkiler, o yüzden fark sadece bu bilgiye ait olanı gösterir. Sonuç: arka
  arkaya koşulda küçük bir iz var (+0,24…+0,46), aralıklıda on kat büyük (+2,1…+2,6).
  Arka arkaya koşulun NLL'indeki iyileşmenin **%90'ı biçim öğrenmesi**, bilgi değil.
- **Tasarruf testi (Ebbinghaus):** unutturma sonunda her eski bilgiye 1 gösterim, hiç
  görülmemiş 200 kontrol bilgisine de 1 gösterim. Aralıklı bilgiler tek gösterimle
  %16-22'den %33-40'a çıkıyor. Arka arkaya bilgiler **%0'dan %0'a**; kontrol de %0.

Yani arka arkaya öğretilen bilgi kâğıt üstünde tamamen silinmemiş ama tek hatırlatmayla
geri gelmiyor; işe yarar anlamda gitmiş. Ön kayıttaki tahminimin yarısı tuttu (iz var),
yarısı tutmadı (geri çağrılabilir değil).

## Paraphrase deneyi adil sınavla tekrarlandı (Study 4)

2d'de sınav hep aynı kanonik cümleyle yapılıyordu; kopyalı koşul o cümleyi 5 kez, farklı
cümleli koşul 1 kez görmüştü. Bu adil değildi. 12 koşu daha yaptım: her koşul bir de hiç
görülmemiş 6. bir cümle kalıbıyla sınandı.

| unutturma boyunca ortalama doğruluk | bilinen cümle | görülmemiş cümle |
|---|---|---|
| aralıklı, 5 kopya | **%31** | %6 |
| aralıklı, 5 farklı cümle | %9 | **%11** |
| arka arkaya (ikisi de) | %0 | %0 |

Pencere sonunda daha net: 5 kopya bilinen cümlede %67, görülmemişte %28 (40 puan düşüş);
5 farklı cümle %35 ve %37 (düşüş yok). Yani **kopya cümleyi öğretiyor, farklı cümleler
bilgiyi öğretiyor.** 2d'deki "farklı cümleler zarar veriyor" sonucu sınavın hatasıymış;
bunu düzeltiyorum. Ön kayıttaki karar kuralı üç seed'de de geçti ama kıl payı (eşik 0,041;
farklar 0,056 / 0,043 / 0,044); pencere sonu ve ayrım ölçüsünde fark daha geniş olduğu
için sonuca güveniyorum, ama "büyük etki" demiyorum. Arka arkaya gösterimi ikisi de
kurtarmıyor.

Bu 12 koşu ayrıca Study 1 ve 2d'nin sayılarını üçüncü kez birebir tekrarladı (0,306 vs
0,298), ölçüm sağlam.

## Aralık eğrisi uzatıldı (Study 5, 13/15 koşu)

Pencereyi 1400 adıma çıkarıp 128 ve 256 adım aralığı da denedim (tüm aralıklar yeni
pencerede yeniden koşuldu). Sonuç: 1 < 16 < 64 her seed'de yine geçerli, ama **64'ten
sonra eğri düzleşiyor**: 128, üç seed'in ikisinde 64'ün altında, birinde üstünde; seed'ler
arası dalgalanma aralıklar arası farktan büyük. Tahminim ("128 daha iyi olur") düştü.
Mekanik sebep de görünüyor: aralık çok büyüyünce 5. gösterim geldiğinde önceki gösterimler
çoktan erimiş oluyor, kodlama zayıflıyor (%84 → %61 → %58). İnsan literatüründeki "çok
fazla aralık da işe yaramaz" bulgusuyla aynı biçim. Pratik kural: **en az 16, 64 yeterli,
daha fazlası bir şey kazandırmıyor.** İki koşu (gap16 ve gap256, seed 2) sabaha kaldı;
`scripts/study5_runs.sh` kaldığı yerden tamamlar.

## Bu ne göstermiyor

- Tek model (GPT-2, küçük), tek tür bilgi (tek cümlelik uydurma çiftler), tek girişim
  metni (Wikipedia). Büyük modeller, gerçek dünya bilgisi için söylenecek bir şey yok.
- 64 adımdan büyük aralık denenmedi; faydanın nerede durduğu bilinmiyor.
- "Neden eriyor" sorusunun cevabı yok. Momentum değil, o kadar. Beynin "araya bir şey
  girince pekişir" hikayesine benziyor ama bu bir benzetme, kanıt değil.
- Paraphrase'in faydası küçük ve kıl payı; daha büyük etki iddiası için daha çok seed gerekir.

## Pratik çıkarım

Bir modele tekrarla bilgi öğretiyorsan tekrarları birbirinden **en az 16, tercihen 64
adım** uzağa koy. Aynı konudaki dokümanları peş peşe dizen veri hatları tam tersini
yapıyor. Tekrar sayısını artırmak, momentumu kapatmak veya cümleyi değiştirmek bunun
yerine geçmiyor. Tekrarlar zaten aralıklıysa, cümleyi değiştirmek "ezber cümle" yerine
"cümleden bağımsız bilgi" satın alıyor; hangisini istediğine göre seç.

## Devam edilsin mi, ne denenmeli?

Devam etmeye değer, çünkü ana etki büyük, 5 tohumda tekrarlandı ve iki "sıkıcı açıklama"
denemesini (momentum, tekrar sayısı) geçti. Sırasıyla:

1. ~~Paraphrase'i adil sınavla tekrar dene~~ — yapıldı (Study 4).
2. ~~Aralık eğrisini uzat~~ — yapıldı (Study 5): 64'ten sonra düzlük.
3. **Erime mekanizması:** tek bir bilgiyi tek başına enjekte et (diğer 199 yokken).
   Hâlâ eriyorsa sebep diğer bilgilerin üzerine yazması değil, güncellemenin kendisi.

İlk ikisi bir öğleden sonra sürer. Üçüncüsü mekanizma çıkarabilecek tek deney.

## Yöntem notları (sadece kayıt için)

- Kod, ön kayıt, 55 koşunun ham logları ve bu rapor `~/Developer/personal/SpacingLab`
  altında, her adım ayrı commit. GitHub'a gönderilmedi.
- İki Sonnet alt-ajan literatür taraması yaptı (docs/literature.md): bu tam
  manipülasyonu ölçen bir yayın bulunamadı; en yakın çalışma (Chang ve ark. 2024)
  "kopya enjeksiyon paraphrase'den hızlı unutuluyor" diyor.
- Yol boyunca düzelttiğim yanlışlar: LoRA ilk iki öğrenme hızında hiç öğrenmedi (grid
  genişletildi, kayda yazıldı); 20 gösterimli kontrol ilk denemede kod hatası verdi
  (son-gösterim adımı çizimi düzeltildi); bir koşu ortam yenilenirken öldü, tekrar koşuldu.
