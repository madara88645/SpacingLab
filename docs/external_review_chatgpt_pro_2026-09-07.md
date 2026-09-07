# SpacingLab
## Kontrollü bulgu, açık mekanizma ve sonraki deney

**Kapsamlı araştırma değerlendirmesi • Mehmet için • 7 Eylül 2026**

Bu rapor, paylaştığın proje özetini değerlendirir; özel depodaki kodun, ham sonuçların veya ön kayıt tarihçesinin bağımsız denetimi değildir. Deney sayıları [P] kaynağından alınmıştır. Basit hesaplamalar ayrıca belirtilmiştir. Literatür karşılaştırması dış kaynak araştırmasıdır; mekanizmalar ve yeni deneyler ise bu raporun önerileridir, yapılmış deneyler değildir.

## 0. Önce: sayıların ve iddiaların denetimi

**Ana bulguya geçmeden önce, birkaç raporlama farkı ile kanıtın taşıyamayacağı kadar güçlü ifadeyi düzeltmek gerekiyor.**

Aşağıdaki teknik ayrım için: gradyan, hatanın ağırlıklardaki değişimlere duyarlılığını gösteren türevdir. Adam, bu türevlerin geçmişini kullanarak ağırlık değişimini hesaplayan yöntemdir; momentum geçmiş gradyan yönlerinin yeni güncellemeye taşınmasıdır.

| Denetlenecek nokta | Sorun | Bu raporda benimsenen okuma |
|---|---|---|
| Toplam koşu sayısı | Çalışma başlıkları 17 + 20 + 6 + 12 + 15 = 70 ediyor; ayrıca 5 pilot var. Çalışma 5’te iki sonuç hâlâ bekliyor. | 70’in planlanan mı tamamlanan mı olduğu belirsiz. Koşu listesinde pilot, tamamlanmış, bekleyen ve yeniden kullanılan kayıtlar ayrı gösterilmeli. Bu, tek başına veri hatası kanıtı değil. |
| Ana etki büyüklüğü | Yazılı ortalamalardan 0,285 − 0,001 = 0,284 çıkıyor; eşleştirilmiş fark +0,29 diye verilmiş. | Hesap aynı koşuları kapsıyorsa ham sonuçlardan yeniden üretilmeli. Burada tablo değerleri korunuyor; yaklaşık 28–29 yüzde puanlık fark deniyor. |
| “0,01 içinde tekrarlandı” | Çalışma 4’te 0,306, Çalışma 1’de 0,285 var; fark 0,021. | Üç ortak rastgelelik başlangıcının karşılaştırılması bunu açıklayabilir. Aynı koşuların alt kümesi gösterilmeden bu cümle doğrulanmış sayılmıyor. |
| Çalışma 5’in tamamlanması | 16 ve 256 aralıklarında birer sonuç eksik; öğretme penceresi de değişmiş. | 700 ve 1.400 adımlık çalışmalar tek, kesintisiz sonuç eğrisi gibi birleştirilmiyor. Eksikler açıkça işaretleniyor. |
| 0,014 gürültü / 0,041 eşik | Tek tekrar koşusu, rastlantısal oynaklığın güven aralığını belirlemez. 0,041’in türetimi özette verilmemiş. | Bunlar kayıtlı değerler; istatistiksel kesinlik ölçüleri olarak kullanılmıyor. Eşiğin önceden nasıl seçildiği ayrıca gösterilmeli. |
| “Momentum mekanizma değil” | Yalnızca β₁ sıfırlanmış; Adam’ın geçmiş gradyan büyüklüklerini tutan β₂ bileşeni kalmış. | “Birinci momentli momentum, farkın oluşması için gerekli değil” denebilir. Bütün optimizasyon açıklamaları elenmiş değildir. |

**Kaynak:** [P], Çalışmalar 1–5 ve koşu bilgileri; çıkarma ve toplama işlemleri bu raporda yapıldı. Adam ayrımı için [9, 16]. “Seed”, deneyde veri üretimi ve sıralama gibi rastlantısal seçimleri belirleyen başlangıç değeri demektir; aşağıda “rastgelelik başlangıcı” veya “bağımsız koşu çifti” kullanılıyor.

İki dil düzeltmesi de önemli. “50 adımda sildi” yerine “yaklaşık 50 adımda doğru cevabı üretme başarısı hızla düştü” denmeli; küçük bir bilgi izi bulunduğunu Çalışma 3 zaten bildiriyor. “LoRA da kurtarmadı” ise olumlu bir mekanizma elemesi değil: LoRA, ana ağırlıklar yerine küçük ek matrislerin eğitildiği yöntem; burada karşılaştırma yeterince öğrenmeyen ve sonunda sıfıra inen koşullar arasında kalmış. [P, Çalışmalar 2b ve 3]

## 1. Tek paragraf özet

**SpacingLab, bu küçük dil modeli düzeninde tekrarların zamanlamasının sonraki hatırlama başarısını güçlü biçimde değiştirdiğini gösteriyor; bunun nedenini henüz göstermiyor.** GPT-2’ye aynı yapay bilgi beş kez öğretildiğinde, 64 adım aralıklı gösterimlerin hatırlama skoru 0,285, ardışık gösterimlerin skoru 0,001 olarak bildirilmiş. Fakat aralıklı koşul öğretme penceresinin sonunda da çok daha başarılı olduğu için, başlangıç öğrenmesinden bağımsız dayanıklılığı sınayan önceden yazılmış ana hipotezin, yani H1’in karar kuralı sağlanmıyor. Ardışık koşulun son gösterim anında öğrenmiş olması, “hiç öğrenemedi” açıklamasını zayıflatıyor; tek yeniden gösterimde başarı gelmemesi ise bilginin tamamen silindiğini kanıtlamıyor. Farklı anlatımla öğretim, çalışılmamış bir cümleyle sorulduğunda daha iyi sonuç veriyor; 64’ten daha büyük aralıklar için tutarlı ek kazanç gösterilmiş değil. En değerli sonraki adım, daha büyük aralıkları taramak değil, etkin eğitim ağırlığını denetlemek ve öğrenilmiş bir bilginin sonraki hangi güncellemelerde bozulduğunu kontrollü biçimde ayırmak. [P, Çalışmalar 1–5; son cümle değerlendirme]

### 1.1. Deney gerçekte neyi ölçüyor?

**Hatırlama skoru, yedi sonraki ölçümdeki mutlak doğruluğun ortalamasıdır; öğrenilen bilginin yüzde kaçının korunduğu değildir.**

| Bileşen | Deneydeki karşılığı |
|---|---|
| Model ve eğitim | GPT-2, 124 milyon parametre, yani eğitimle değiştirilebilen sayı; tüm ağırlıkların güncellendiği ince ayar. |
| Öğretilecek malzeme | Beş şablondan türetilmiş, uydurma isimler içeren 200 bilgi. Her bilgiye beş gösterim. |
| Aradaki eğitim | Her adımda WikiText-103’ten 15 × 64 token; token, modelin metni böldüğü parçadır. Planlanmış bilgi cümleleri ayrıca eklenir. |
| Zaman çizgisi | 100 adım ısınma → 700 adım öğretme → 1.500 adım başka metinler ve 50 yeni bilgiyle eğitim. |
| Değiştirilen değişken | Aynı bilginin gösterimleri arasındaki 1 / 4 / 16 / 64 adımlık mesafe. Son gösterim zamanı eşleştirilir. |
| Doğruluk | Modelin en olası parçaları sırayla seçerek ürettiği cevabın tam eşleşmesi. Kısmi doğru cevap da yanlış sayılabilir. |
| NLL | Doğru cevaba atanan olasılığın negatif logaritması; düşük değer daha yüksek olasılık demektir. Uzunluk başına mı toplam mı hesaplandığı açıklanmalı. |
| Hatırlama skoru | Müdahale sonrasındaki 50, 100, 200, 400, 800, 1.200 ve 1.500. adımlarda doğruluğun eşit ağırlıklı ortalaması. |
| Ayırt etme | Aynı türden yanlış cevabın NLL’si eksi doğru cevabın NLL’si; pozitif olması doğru eşleştirmeye görece tercih olduğunu gösterir. |

**Eğitim ayarları:** AdamW; öğrenme hızı 0,0001; β₁ = 0,9 ve β₂ = 0,999; ağırlık küçültme cezası yok; nöronların rastgele kapatılması kapalı; gradyan büyüklüğünü sınırlama eşiği 1,0. Apple-Silicon üzerindeki MPS hesaplama altyapısı kullanılmış. Bu ayarlar kaynakta bildirilenlerdir.

**Kaynak:** [P, deney düzeni]. “Müdahale sonrası” burada öğretme penceresi bittikten sonraki yeni eğitim dönemidir. Bu dönemdeki 50. adım, her bilginin kendi son gösteriminden sonraki 50. adımı değildir.

Bu ayrım H1 için belirleyici. Pencere sonunda “anlık” denilen ölçüm, daha önce son kez gösterilmiş bilgiler açısından zaten gecikmeli bir testtir. Her bilginin kendi son gösteriminden itibaren geçen eğitim adımlarını ayrıca hizalamak gerekir.

### 1.2. Ana sonuç: etki büyük, yorumun kapsamı dar

**1’den 64’e kadar aralık arttıkça hem pencere sonu başarısı hem sonraki başarı artıyor.**

| Aralık | Pencere sonu doğruluk | Hatırlama skoru | Sonraki 1.500. adım doğruluğu |
|---|---:|---:|---:|
| 1 adım, ardışık | 0,03 | 0,001 | 0,00 |
| 4 adım | 0,08 | 0,023 | 0,01 |
| 16 adım | 0,35 | 0,124 | 0,05 |
| 64 adım | 0,65 | 0,285 | 0,14 |

**Kaynak:** [P, Çalışma 1]. Ana karşılaştırmada beş, ara aralıklarda üç rastgelelik başlangıcı kullanıldığı bildirilmiş. Tablo, ham koşular yeniden hesaplanmadan aktarılmıştır.

0,285 ile 0,001 arasındaki farkı “%28,4 daha iyi” diye yazmak yanlış olur: bunlar doğruluk oranlarıdır; fark yaklaşık **28,4 yüzde puandır**. Ardışık koşul neredeyse sıfır olduğu için “285 kat daha iyi” gibi oranlar teknik olarak hesaplanabilse de sonucu anlamayı güçleştirir. Ayrıca buradan “öğrenilen bilgilerin %28,5’i hayatta kaldı” sonucu çıkmaz.

Ardışık koşulun kendi son gösterimindeki 0,43 başarısı ile pencere sonundaki 0,03 başarısı, edinilmiş başarının hızla kaybolduğunu destekler. Buna karşılık 0,43 → 0,03 ve 0,81 → 0,65 okları bütün bilgiler için eşit, tam 50 adımlık süreyi temsil etmez. [P, Çalışma 1]

### 1.3. Farklı anlatım ve büyük aralıklar: iki ayrı sonuç

**Farklı anlatımın değeri sorunun nasıl sorulduğuna bağlı; büyük aralıklarda ise kesin bir optimum değil, belirsiz bir yataylaşma var.**

| Aralıklı eğitim biçimi | Çalışılan cümlede hatırlama | Görülmemiş altıncı cümlede hatırlama |
|---|---:|---:|
| Aynı cümlenin kopyaları | 0,306 | 0,060 |
| Beş farklı anlatım | 0,092 | 0,108 |

**Kaynak:** [P, Çalışma 4]. Görülmemiş anlatımdaki fark 0,048, yani 4,8 yüzde puandır; bu raporda hesaplandı. Tek bir yeni anlatım üzerinden genel dilsel sağlamlık kanıtlanmış değildir.

“Farklı cümle bilgiyi öğretir” yararlı bir sezgi ama fazla keskin bir sonuçtur. Daha savunulabilir ifade şudur: farklı anlatımlar, bu çalışmadaki yeni ifade biçimine aktarımı artırıyor; aynı cümleler çalışılan ifadede daha yüksek performans sağlıyor. Hiçbir koşul için genel anlamda “anlama” kanıtı çıkarılmamalı.

| 1.400 adımlık pencere | Aralık 1 | Aralık 16 | Aralık 64 | Aralık 128 | Aralık 256 |
|---|---:|---:|---:|---:|---:|
| Başlangıç 0 | 0,004 | 0,171 | 0,366 | 0,280 | 0,296 |
| Başlangıç 1 | 0,000 | 0,108 | 0,194 | 0,274 | 0,222 |
| Başlangıç 2 | 0,002 | Bekliyor | 0,224 | 0,161 | Bekliyor |

**Kaynak:** [P, Çalışma 5]. Eksik sonuçlar sıfırla doldurulmamıştır.

Üç eşleştirilmiş koşuda 128 − 64 farkları −0,086, +0,080 ve −0,063; ortalaması −0,023’tür. Bu hesap “128 daha iyi” öngörüsünü desteklemez. Ama üç koşudan “64 ile 128 eşdeğer” veya “optimum kesin 64” de çıkmaz; küçük ve oynak bir örneklem, eşdeğerliği gösterecek hassasiyeti sağlamayabilir.

## 2. Sert hakem değerlendirmesi: beş temel itiraz

**Bir hakemin en güçlü itirazı modelin küçük olması değil, ölçülen toplam avantaj ile ona yüklenen mekanizma açıklamasının birbirine karışması olur.** Aşağıdaki eleştiriler verinin geçersiz olduğunu varsaymıyor; hangi iddianın hangi ek kontrole ihtiyaç duyduğunu ayırıyor.

### 2.1. “Daha kalıcı öğrenme” ile “başlangıçta daha fazla öğrenme” ayrılmamış

**H1’in desteklenmediğini korumalısın; sonradan eklenen ölçümlerle önceden yazılmış sonucu başarılı ilan etmemelisin.**

**Neden önemli?** Aralıklı koşul hem başlangıçta hem daha sonra daha yüksekse, sonraki farkın ne kadarı başlangıç üstünlüğünden geliyor sorusu açık kalır. Sabit eğitim bütçesindeki toplam zamanlama etkisi yine değerlidir; fakat aynı başlangıç başarısından sonra daha yavaş bozulma ayrı bir iddiadır.

**Mevcut veri cevaplıyor mu?** Kısmen. Son gösterimden hemen sonra öğrenme bulunması; β₁ = 0 iken ardışık koşulun 0,95–0,98’e çıkıp sonra düşmesi; düşük NLL’li alt kümede de fark kalması, “ardışık hiç öğrenmedi” açıklamasını ciddi biçimde zayıflatır. Fakat iki koşulda sonradan “iyi öğrenilmiş” bilgileri seçmek, tedavinin etkilediği bir özelliğe göre farklı alt kümeler seçmektir; tam bir nedensel eşleştirme değildir. [P, Çalışmalar 1 ve 2a]

**En ucuz çözüm:** Önce mevcut bilgi-bazlı sonuçları son gösterim yaşına göre yeniden çiz. Ardından ayrı bir tanısal deneyde başlangıç doğruluğunu ve doğru–yanlış cevap ayrımını birbirine yaklaştırıp aynı sonraki eğitimle karşılaştır. Bunun için tekrar sayısını değiştirmen gerekirse, yeni deneyin artık sabit K = 5 sorusu olmadığını açıkça yaz. Bu, H1’i geriye dönük kurtarmaz; yeni bir soruyu cevaplar.

### 2.2. Eşit token bütçesi, eşit etkin eğitim ağırlığı demek değil

**Programlama ve veri karıştırma ayrıntıları açıklığa kavuşmadan “yalnızca zaman aralığı değişti” ifadesi gereğinden güçlü kalabilir.**

**Neden önemli?** Diyelim bir adımda bir, başka adımda dört bilgi cümlesi var. Kayıp, yani modelin eğitim sırasında küçültmeye çalıştığı hata, o adımdaki tüm geçerli tokenlara bölünüyorsa her cümlenin ağırlığı değişebilir. Aynı toplam token sayısı bu adım-bazlı farkı ortadan kaldırmaz. Güncelleme büyüklüğünü sınırlayan kırpma da kalabalık adımları farklı etkileyebilir.

**Mevcut veri cevaplıyor mu?** Toplam token ve adım korumaları iyi bir başlangıçtır; özette adım-bazlı kayıp paydası, bilgi çakışmaları, kırpma oranları ve dolgu metinlerinin birebir sırası yok. Bir hata olduğunu bilmiyorum. Kod görülmeden emin değilim.

**En ucuz çözüm:** Önce eğitim yapmadan planı denetle. Her adımda bilgi sayısını, kayba giren token sayısını, her bilginin etkin katsayısını ve dolgu metni kimliğini çıkar. Sonra gerekiyorsa bilgi ve dolgu kaybını açık, sabit katsayılarla birleştiren iki koşullu tekrar yap. Sabit katsayılarla etkide büyük değişim, eski sonucu “saf aralık” yerine “bu veri yerleştirme düzeninin toplam etkisi” olarak yeniden çerçevelemeyi gerektirir.

Ayrıca son gösterimleri eşitlemek, ilk gösterimleri eşitlemez: 64 aralığında beş gösterim 256 adımlık alan kaplar; ardışık gösterimler dört adımlık alan kaplar. Bu, yanlış tasarım değil; hangi eğitim geçmişinin değiştiğinin açık tanımıdır. Erken format öğrenimi ve dönemsel bilgi yoğunluğu olası aracı etkenlerdir.

### 2.3. Sıfır doğru cevap, sıfır bilgi değildir

**Ölçümler “cevaba erişilemiyor” ile “bilgi izi yok” ayrımını henüz kesinleştirmiyor.**

**Neden önemli?** Tam cevap eşleşmesi sert bir eşiğe sahiptir. Doğru isim ikinci en olası seçenek olduğunda da model sıfır puan alabilir. Aynı şekilde, hem eski bilgiler hem yeni kontroller tek gösterimde sıfırda kalıyorsa yeniden öğrenme testi küçük avantajları göremiyor olabilir.

**Mevcut veri cevaplıyor mu?** Ayırt etme ölçüsü gerçekten yardımcı: ardışık koşulun +0,24 ile +0,46 aralığında olması, başlangıçtaki +0,05’e göre küçük bir ilişki iziyle tutarlı. Ama 3,15 / 3,5 = %90 hesabı yalnızca NLL kazancının büyük bölümünün seçilmiş yanlış cevapla ortak olduğunu gösterir. “Tam %90 format, %10 bilgi” diye kesin bir parçalama yapmaz; yanlış cevabın uygunluğu önemlidir. [P, Çalışma 3]

**En ucuz çözüm:** Kaydedilmiş ağırlıklarda birden fazla, benzer token uzunluğunda yanlış cevapla ölç. Doğru cevabın adaylar arasındaki sırasını da raporla. Yeniden öğrenmede 1, 2, 4 ve 8 gösterimlik eğri kullan; kontrol bilgilerinin öğrenilebildiğini önceden doğrula. Eski ve yeni bilgilerin öğrenme hızı arasında ayrım çıkmazsa “bu duyarlılıkta geri kazanım avantajı yok” de; “tamamen silinmiş” deme.

### 2.4. Bağımsız tekrar az; eşikler ve yardımcı testler olduğundan kesin gösterilebilir

**200 bilgi ve yedi ölçüm noktası, 1.400 bağımsız deney anlamına gelmez.**

**Neden önemli?** Aynı modeldeki bilgiler ortak güncellemelerden etkilenir; aynı modelin yedi ölçümü de ilişkilidir. Koşul farkı için asıl bağımsızlık birimi, eşleştirilmiş rastgelelik başlangıçlarıdır. Beş çift güçlü bir ilk işaret verebilir; küçük etkilerin hassas büyüklüğünü belirlemek daha zordur.

**Mevcut veri cevaplıyor mu?** Ana farkın beş çiftin hepsinde aynı yönde olması ve büyük olması destekleyicidir. Fakat Çalışma 4’te üç farkın 0,041 eşiğini yalnızca 0,015, 0,002 ve 0,003 aşması daha ihtiyatlı dil gerektirir. K = 10 / 20 testi de yalnızca bir başlangıçta yapılmış. Sekiz tarihli değişiklik, kayıt disiplinidir; değişikliklerin hangi önceki sonuçlara dayanarak yapıldığını göstermenin yerini tutmaz. [P]

**En ucuz çözüm:** Her karşılaştırma için bütün eşleştirilmiş farkları yayımla; ana ve keşifsel analizleri, yani önceden kararlaştırılan ve sonradan fikir veren analizleri ayır. Belirsizlik aralıkları koşu düzeyinde hesaplanmalı. Makine oynaklığı için tek yeniden çalıştırmayı evrensel eşik yapma; önemli küçük farklarda ek bağımsız çiftlerle doğrula.

Hatırlama skorunun yedi noktaya eşit ağırlık vermesini değiştirme. Fakat yardımcı kontrolde geç dönem başarısını ve zamanla ağırlıklandırılmış eğri alanını ayrıca göster. Böylece sonuç, sık erken ölçümlere bağlı mı anlaşılır; yeni ölçüm eskisinin yerine geçirilmez.

### 2.5. Pratik karşılaştırma ve dış geçerlilik eksik

**Ardışık gösterime üstünlük, sıradan rastgele karıştırmaya veya başka modellerdeki eğitime üstünlük demek değildir.**

**Neden önemli?** Bugün veri hazırlayan birinin gerçek seçeneği çoğu zaman “beş kopyayı zorunlu olarak arka arkaya koymak” değildir. Zaten karıştırılmış veri, uygun dağılımı kendiliğinden sağlayabilir. Ayrıca uydurma isimlerin parçalanma biçimi, şablon benzerliği ve tek öğrenme hızı sonucu etkileyebilir.

**Mevcut veri cevaplıyor mu?** Parafraz, yani aynı bilginin farklı sözcüklerle anlatılması, ve geniş aralık testleri kapsamı biraz açıyor; ikinci mimari, doğal isimler ve başarılı LoRA karşılaştırması yok. Dolayısıyla ana iddianın “genel bir dil modeli reçetesi” olması savunulamaz. [P, kapsam ve Çalışmalar 2–5]

**En ucuz çözüm:** Önce aynı bütçeli rastgele yerleştirme taban çizgisini, yani basit karşılaştırma yöntemini ekle. Son gösterim, başlangıç ve toplam açıklık gibi sınırların hangilerini eşlediğini belirt. Sonra benzer büyüklükte ikinci bir modelde iki uç koşulu dene. LoRA karşılaştırmasını ancak önce yeterli öğrenme ve ölçülebilir unutma sağlayabiliyorsan yap.

## 3. Yenilik değerlendirmesi

**Özgünlük iddian “dil modellerine aralıklı tekrarı getirmek” değil, olgu-bazlı zamanlamayı sıkı kontrollere bağlayan dar bir deney protokolü olabilir.**

### 3.1. Chang ve arkadaşları: en yakın karşılaştırma

**Chang’ın kopya koşulu da aralıklı; onun bulgusunu ardışık–aralıklı karşılaştırması gibi anlatmamalısın.** NeurIPS 2024 çalışmasında kurgusal bilgiler kopya ve farklı anlatım koşullarında 100 eğitim adımı arayla, toplam on kez ekleniyor. Dolayısıyla kopya–parafraz ayrımı var, fakat senin 1 / 4 / 16 / 64 karşılaştırman aynı biçimde yapılmıyor. Ayrıca “retainability”, bilgi kazanım tepesine göre normalize edilen log-olasılık ölçüsü; senin yedi tam-eşleşme doğruluğu ortalamanla aynı sayı değil. [1]

Bu yüzden “farklı anlatım genellemeyi ve kalıcılığı değiştirebilir” yeni bir keşif olarak sunulmamalı. Senin olası ek katkın, aynı tekrar sayısı ve eşleştirilmiş son gösterimle zamanlamanın etkisini daha doğrudan ayırmak. Önceden bilinen sonuca benzer bir sonuç almak, dikkatli bir kontrollü doğrulama olabilir; otomatik olarak özgün mekanizma keşfi olmaz.

### 3.2. Kaynak listene eklenmesi gereken 2026 çalışmaları

**FOREVER ve MSSR, geniş yenilik iddiasını doğrudan sınırlandıran yakın çalışmalardır.** FOREVER’ın 20 Nisan 2026 tarihli ikinci sürümü, yeni görevler öğrenilirken eskilerini korumayı amaçlayan sürekli öğrenmede, eski örnekleri yeniden eğitime katma zamanını, adım sayısı yerine birikmiş ağırlık güncellemesi büyüklüğüne bağlar. MSSR’ın 10 Mart 2026 önbaskısı ise örneklerin tahmini hatırlanma durumuna göre yeniden gösterimi ve aralıkları ayarlar; farklı aralık düzenlerini de karşılaştırır. [5, 6]

Buradaki ayrım, “onlar zamanlamayı hiç çalışmamış” değildir. Onlar yeni görevler öğrenilirken eski örnekleri yeniden gösteren yöntemler geliştiriyor. SpacingLab ise eski bilginin beş gösterimini belirli bir pencerede bitirip, sonrasında tekrar vermeden nasıl dayandığını inceliyor. Taranan metinlerde senin bütün kontrol koşullarını birlikte sağlayan aynı deney görülmedi; bunun literatürde hiç bulunmadığından emin değilim. Kesin öncelik iddiası için daha sistematik tarama ve açık protokol karşılaştırması gerekir.

MSSR önbaskısının bir aralık tablosunda başlık ile “unutma” sütununun yönü de birbiriyle uyumsuz görünüyor. Bu rapor o sayıları performans kanıtı olarak kullanmıyor; çalışmayı yakın bir yöntem fikrinin yayımlanmış olması nedeniyle anıyor. Önbaskı varlığı, sonuçlarının bağımsız doğrulandığı anlamına gelmez. [6, Tablo 4]

### 3.3. Diğer çalışmalarla sınır çizgisi

| Çalışma | Doğrulanan yakınlık | SpacingLab açısından anlamı |
|---|---|---|
| Allen-Zhu ve Li, Physics 3.1, ICML 2024 [2] | Bilginin saklanması ile farklı soru biçimlerinden çıkarılması ayrılıyor; veri çeşitlendirme önemli. | “Ezberlenmiş cümleye başarı, farklı anlatıma başarı değildir” fikri yeni değil. |
| Sun ve arkadaşları, 2025 [3] | Öğretmen modelden öğrenci modele bilgi aktarımında zamanlama; odak genelleme. | Aynı bilginin beş gösterim aralığını ve sonrasındaki unutmayı ölçen deneyle aynı düzen değil. |
| Sun ve arkadaşları, Patterns 2026 [4] | Biyolojik ve yapay sistemlerde aralığın genellemeye katkısı. | Sinir ağlarında aralık fikrinin ilk uygulaması iddia edilemez. Tam yöntem bu incelemede erişilemedi; ayrıntılı eşdeğerlik için emin değilim. |
| Düzenlenmiş bilgi üzerine çalışma, 2025 [7] | Modele eklenmiş/düzeltilmiş bilginin sonraki ince ayarda tutulması inceleniyor. | “Sonraki eğitim yeni bilgiyi silebilir” gözlemi tek başına yeni değil. |
| Hernandez 2022; Muennighoff 2023 [11, 12] | Tekrarlanan veri ve sınırlı veri bütçesinin etkileri. | Tekrar miktarı ile tekrarlar arasındaki zamanlama farklı eksenler; karıştırılmamalı. |
| Cepeda ve arkadaşları, 2008 [8] | İnsanlarda uygun çalışma aralığı, bilginin ne kadar sonra hatırlanacağına bağlı. | Bir aralık taramasındaki yataylaşma, aynı biyolojik mekanizmayı göstermez. |

**Kaynak notu:** Patterns makalesinin varlığı ve genel konusu doğrulandı; bu incelemede tam metin yöntemine erişilemedi. Diğer ana karşılaştırmalar birincil makale metinleri veya resmi yayın kayıtlarına dayanıyor. İnsanlarda genişleyen–sabit aralık üstünlüğü hakkında ayrıca doğrulanmamış bir hüküm bu rapora eklenmedi.

### 3.4. Kullanılabilecek katkı cümlesi

**En savunulabilir katkı, geniş bir biyolojik benzetmeden daha küçük ama daha ölçülebilir bir cümledir:**

“GPT-2’de yapay olguların sabit sayıda gösterimini, eşleştirilmiş son-gösterim zamanları altında farklı eğitim aralıklarına dağıttık. Zamanlamanın sonraki üretim başarısıyla güçlü ilişkisini, başlangıç edinimi, soru biçimi ve ayırt etme ölçümleriyle birlikte raporladık; başlangıçtan bağımsız dayanıklılığa ilişkin önceden yazılmış hipotez desteklenmedi.”

Kod denetimi ve adım-bazlı ağırlık kontrolleri tamamlanınca “ilişkisini” yerine, bu protokolün kapsamıyla sınırlı olarak “etkisini” daha rahat kullanabilirsin. “İlk”, “insan benzeri hafıza pekişmesi kanıtlandı” ve “evrensel 64 adım optimumu” ifadelerini kullanmamalısın.

## 4. Mekanizma: en güçlü üç açıklama ve nasıl sınanacakları

**İlk araştıracağım açıklama yıkıcı güncelleme etkileşimi olur; dar bir ağırlık bölgesine yerleşme ve Adam’ın kalan hafızası ikinci aşamada incelenmeli.** Bunlar bulgu değil, sonuçları ayıracak deney önerileridir. Aynı cümlenin tekrar edilmesi, beş özdeş gradyan adımı atıldığı anlamına gelmez: modelin ağırlıkları ve birlikte eğitildiği metinler değişir.

### 4.1. Başka bilgilerin ve genel metnin güncellemeleri eski eşleştirmeyi bozuyor

**Aralıklı tekrar, bilgiye değişmiş eğitim bağlamlarında yeniden uyum sağlatıyor olabilir; ardışık tekrar bunu sağlayamıyor olabilir.**

Gradyan, hatanın ağırlıklardaki küçük değişimlere hangi yönde ve ne kadar duyarlı olduğunu gösteren türevler bütünüdür. Eski A bilgisinin kaybı L_A, bunun gradyanı g_A ve modelin gerçekten uyguladığı ağırlık değişimi Δθ olsun. Küçük bir güncellemede:

`L_A(θ + Δθ) − L_A(θ) ≈ g_A · Δθ`

Sağ taraf pozitifse bu güncelleme eski bilginin kaybını artırma yönündedir. Noktasal çarpım, iki vektörün aynı veya zıt yönde ne kadar bileşeni olduğunu ölçer. Basit gradyan inişinde Δθ = −ηg_B olduğundan, g_A · g_B negatifse B eğitimi A’ya zarar verme yönündedir. Buradaki η adım büyüklüğüdür. Adam’da geçmiş bilgiler de güncellemeyi etkilediği için yalnızca ham gradyanlar değil, **gerçek uygulanan Δθ** incelenmeli. Formül küçük değişimler için birinci dereceden yaklaşımdır; büyük adımlarda gerçek kayıp değişimiyle doğrulanmalıdır.

**Somut ölçüm:** Önceden seçilmiş birkaç bilgi için kendi son gösteriminden sonraki kısa dönemde gerçek kayıp değişimini ve g_A · Δθ değerini kaydet. Güncellemeleri yalnız genel metin, aynı şablondan başka bilgiler ve farklı şablondan bilgiler diye ayır. Toplam yerine katman katman, yani modelin işlem aşamaları boyunca katkıyı da incele.

**Ayırıcı müdahale:** Aynı kaydedilmiş model durumundan üç kısa dal başlat: yalnız genel metin; genel metin + aynı şablonlu rakip bilgiler; genel metin + farklı şablonlu bilgiler. Token bütçelerini, kayıp katsayılarını ve adım sayılarını eşle. Dallar arasında aynı başlangıç ağırlıkları kullanıldığı için ek zarar, sonradan verilen veri türüne daha doğrudan bağlanabilir.

**Kritik ayrıntı:** Dalları ardışık koşulun zaten sıfıra indiği pencere sonunda başlatma. Önceden belirlenmiş hedef bilginin son gösteriminden hemen sonraki model durumunu kullan. Az sayıda hedefle yapılan ilk testin bütün 200 bilgiye genellendiğini de varsayma.

**Maliyet:** Kaydedilmiş uygun durumlar varsa yeni tam koşu gerekmez; 3 başlangıç × 2 zamanlama × 3 kısa dal = 18 kısa devam gerekir. Durumlar yoksa 6 ana koşu, verilen hızla 0,9–1,2 saatlik temel eğitimdir. Sık gradyan ölçümü ve kayıt yüküyle toplam için 1,5–3 saatlik bütçe ayırmak makul bir planlama tahminidir; bu ek yük ölçülmüş değil.

### 4.2. Ardışık eğitim, sonraki değişimlere hassas bir çözüm üretiyor

**Aynı doğruluk, ağırlıklarda aynı sağlamlık demek değildir; ardışık koşul küçük değişimlerle daha kolay bozulabilir.**

Keskinlik, ağırlıkları biraz değiştirdiğinde kaybın ne kadar hızla yükseldiğidir. Bir noktada düşük kayıp olması, o noktanın çevresinin de iyi olması anlamına gelmez. Ancak “keskin çözüm kötüdür” evrensel bir yasa değildir; ağırlıkların matematiksel ifade biçimi bile ham keskinlik ölçülerini değiştirebilir. Bu nedenle rastgele tek bir eğrilik sayısı yerine, gerçekten sonraki eğitimin gittiği yönlerde ölçüm gerekir. [10]

**Somut ölçüm:** Sonraki güncellemenin yönünü uzunluğu bir olacak biçimde ölçekleyerek u oluştur. Küçük bir ε miktarı için şu üç kaybı hesapla: L_A(θ), L_A(θ + εu), L_A(θ − εu). Ardından:

`C(u, ε) = [L_A(θ + εu) + L_A(θ − εu) − 2L_A(θ)] / ε²`

Bu, o yöndeki yerel eğriliğin yaklaşık ölçüsüdür. Ölçümü birkaç ε değeri, gerçek güncelleme yönü, bilgi gradyanı yönü ve aynı büyüklükte rastgele kontrol yönleriyle yap. Nokta gerçek bir minimum olmayabileceğinden doğrusal eğimi g_A · u da raporla.

**Ayırıcı sonuç:** Başlangıç kaybı benzerken, eşit büyüklükteki gerçekçi bozucu değişim ardışık koşulda sistematik olarak daha fazla kayıp yaratıyorsa kırılganlık açıklaması güçlenir. Sonraki gerçek unutma ile bağlantı bulunmazsa salt keskinlik hikâyesini bırak. Hangi katmanın ağırlık değişimlerini durdurmanın veya küçültmenin kaybı azalttığını sınamak, korelasyondan daha güçlü bir sonraki kontrol olur.

**Maliyet:** Uygun 6 model durumu varsa sıfır yeni tam eğitim koşusu; birkaç yön, büyüklük ve hedef üzerinde ileri hesaplama gerekir. Yoksa aynı 6 koşu diğer mekanizma testleriyle paylaşılabilir. Ek ölçüm için yaklaşık 0,5–1,5 saatlik pilot bütçe düşünülebilir; gerçek süre hedef sayısına bağlıdır. Tam modelin ikinci türev matrisini hesaplamayı önermiyorum.

### 4.3. Adam’ın kalan geçmişi ve etkin güncelleme miktarı fark yaratıyor

**β₁ = 0 sonucu yönlü momentumun zorunlu olmadığını gösterir; bütün eğitim geçmişini sıfırlamaz.** Adam, güncellemeyi hem geçmiş gradyanların ortalamasına hem karelerinin ortalamasına göre ölçekler. β₁ ilkini, β₂ ikincisini kontrol eder. β₁ sıfırken bile β₂ = 0,999, geçmiş büyüklüklerin etkisini taşır. [9, 16]

`m_t = β₁ m_(t−1) + (1−β₁) g_t`

`v_t = β₂ v_(t−1) + (1−β₂) g_t²`

`Δθ_t = −η m̂_t / (sqrt(v̂_t) + ε)`

Burada m yönlü ortalamayı, v kare büyüklüklerin ortalamasını, şapka işareti başlangıç yanlılığını düzelten sürümü gösterir. Son satırın ε değeri, sıfıra bölünmeyi engelleyen küçük sayıdır; bir önceki keskinlik testindeki bozma büyüklüğüyle aynı şey değildir.

**Somut ölçüm:** Beş gösterimin her birinde bilgi gradyanının büyüklüğünü, uygulanan güncellemenin büyüklüğünü, kırpma katsayısını ve cevap kaybındaki iyileşmeyi kaydet. Beş gösterim sayısının iki koşulda aynı olması, beş gösterimin aynı etkin değişimi yaptığı anlamına gelmeyebilir.

**Ayırıcı müdahale:** Aynı ağırlıkları iki dala ayır; birinde kendi optimizasyon durumunu koru, diğerinde tanımlanmış ortak bir ikinci-moment durumu kullan. Bias düzeltmesindeki adım sayısını ve gerçek güncelleme ölçeğini kontrol et. v’yi dikkatsizce sıfırlamak büyük ilk adım oluşturabilir; o zaman farklı mekanizmayı test etmiş olursun.

**Maliyet ve durdurma:** Aynı 6 ana koşudan kısa devamlarla başlanabilir; temel eğitim 0,9–1,2 saat, ek kayıt ve dallar için ölçülmemiş bir ek bütçe gerekir. Gerçek güncelleme büyüklükleri eşlendiğinde durum değişimi farkı açıklamıyorsa bu hattı öncelikten düşür. Zaten güçlü edinimden sonra unutma bulunduğu için “sonraki kopyaların gradyanı küçüldü” açıklamasını tek başına yeterli görmüyorum.

## 5. Önceliklendirilmiş deney planı

**Önce karşılaştırmanın doğruluğunu ve pratik taban çizgisini sağlamlaştır; sonra mekanizma ve genelleme için bütçe harca.** Aşağıdaki eşikler mevcut bulgu değil, sonraki koşulardan önce kabul edilebilecek taslak karar kurallarıdır. “Ön kayıt”, hipotezi, ölçümü ve karar kuralını sonuçları görmeden yazmak demektir.

Üç bağımsız çift, pahalı olmayan bir eleme deneyi için kullanılabilir; tek başına dar belirsizlik aralığı veya eşdeğerlik kanıtı sağlamaz. “Üçünde de aynı yön + ortalama en az 0,05” gibi kapılar aşağıda **hangi işe devam edileceğini seçmek içindir**, evrensel bilimsel kanıt eşiği değildir.

### 5.1. Öncelik 1 — Eğitim ağırlığı ve zamanlama denetimi

**Soru ve öngörü:** Etkin bilgi katsayıları, dolgu sırası ve son-gösterim eşleşmeleri kontrol edildiğinde zamanlama avantajı sürüyor mu? Taslak öngörü: fark yalnızca değişken kayıp paydasından doğmuyorsa korunur.

**Karar kuralı:** Önce bütün bilgi–koşu çiftlerinde K, son gösterim, pencere sınırı, toplam geçerli token ve dolgu kimliklerini otomatik doğrula. Eksik kayıt varsa koşuyu denetlenmiş sayma. Gerekli düzeltmeden sonraki yeni 3 çiftte ortalama fark en az 0,05 ve üç fark da pozitifse sonraki araştırmaya devam et; ham farkları ayrıca raporla.

**Maliyet:** Kayıtlar yeterliyse 0 yeni koşu. Yeniden eğitim gerekirse 6 koşu: 0,9–1,2 saat temel süre; ayrıntılı kayıtla yaklaşık 1–2 saatlik bütçe. Kod yazma süresi dahil değildir.

**Durdurma / pratik etkisi:** Kontrol değişikliği farkı ortadan kaldırır veya tersine çevirirse eski “salt aralık” yorumunu durdur. Bu deney **pratik öneriyi de değiştirebilir**; önce uygulanmalı.

### 5.2. Öncelik 2 — Rastgele karıştırma zaten yeterli mi?

**Soru ve öngörü:** Düzenli 64 adım, sıradan rastgele dağıtımdan daha iyi mi? Taslak öngörü: ana yarar yalnızca tekrar yığılmasını önlemekse rastgele dağıtım da ardışık koşuldan iyi olabilir; 64’e üstünlük veya eşdeğerlik baştan varsayılmamalı.

**Karar kuralı:** Her bilgi için beş gösterimi ve son gösterimi eşle; rastgele koşulun izin verilen ilk–son gösterim açıklığını önceden tanımla. 1 / 64 / rastgele olmak üzere üç koşul kullan. Rastgele ile 64 arasındaki eşleştirilmiş farkı ve belirsizlik aralığını raporla. “Pratikte eşdeğer” için, örneğin bütün belirsizlik aralığının −0,02 ile +0,02 içinde kalmasını önceden şart koş; üç başlangıçta bu hassasiyete ulaşılamazsa sonuç belirsizdir.

**Maliyet:** 3 başlangıç × 3 koşul = 9 koşu; mevcut hızla 1,35–1,8 saat temel eğitim. Eski uç koşullar gerçekten aynı düzenle uyumluysa yalnız 3 yeni rastgele koşu yeterli olabilir; karşılaştırma eşleşmesi doğrulanmalı.

**Durdurma / pratik etkisi:** Rastgele dağıtım yeterince iyi çıkarsa özel 64-adım düzenini üretim tavsiyesi olarak takip etmeyi bırak; “tekrarları dağıt” önerisine dön. **Doğrudan pratik deneydir.** Belirsizlik aralığı genişse eşdeğerlik ilan etme.

### 5.3. Öncelik 3 — Öğrenilmiş bilgiyi hangi sonraki veri bozuyor?

**Soru ve öngörü:** Hızlı kaybın ana kaynağı genel metin mi, aynı şablondaki diğer bilgiler mi? Taslak öngörü: rekabet eden eşleştirmeler belirleyiciyse aynı şablonlu dal, eşleştirilmiş genel-metne göre daha fazla zarar verir.

**Karar kuralı:** Önceden seçilmiş hedeflerin son gösteriminden başlayan, 50 ve 100 adımlık dallarda doğru cevabın NLL artışını ana tanısal ölçü yap. Doğruluğu ve ayırt etmeyi yardımcı ölç. Aynı şablonlu dalın ek zararı üç başlangıçta aynı yönde değilse veya yalnız kayıp ağırlığı farkıyla ortaya çıkıyorsa mekanizma lehine karar verme.

**Maliyet:** 6 ana koşu + 18 kısa dal; uygun durumlar kayıtlıysa yalnız dallar. Ana süre 0,9–1,2 saat; toplam için 1,5–3 saatlik, ölçüm yükü henüz doğrulanmamış bütçe.

**Durdurma / pratik etkisi:** Rakip bilgi dalı ek zarar yaratmıyorsa “diğer 199 bilgi temel neden” açıklamasını öncelikten düşür. Yaratıyorsa sonraki kontrol, bilgi yoğunluğunu azaltıp metin ve kayıp katsayılarını eşlemektir. **Mekanizma ve pratik veri karışımı açısından yararlı.**

### 5.4. Öncelik 4 — Benzer başlangıç öğrenmesinden sonra hangi koşul daha dayanıklı?

**Soru ve öngörü:** Edinim düzeyi yaklaştırılınca aralık avantajı kalıyor mu? Taslak öngörü: zamanlama yalnız ilk edinimi değil sonrasındaki hassasiyeti de etkiliyorsa avantaj sürer.

**Karar kuralı:** Ayrı pilot bilgilerde, son-gösterim doğruluk farkı en fazla 0,05 olacak ve cevap NLL dağılımları belirgin biçimde ayrışmayacak bir karşılaştırma kur. Pilot bilgiler ana testte kullanılmasın. Ana ölçüm aynı bilgi yaşlarında sonraki kayıp artışı ve doğru cevaba tercih olsun. Başlangıç eşleştirme sınırları sağlanmıyorsa “eşit öğrenmeden sonra” testi yapılmış sayılmasın.

**Maliyet:** 2 pilot + 6 ana koşu = 8; temel süre 1,2–1,6 saat. Yoğun bilgi-bazlı ölçümle 1,5–3 saatlik bütçe gerekebilir.

**Durdurma / pratik etkisi:** İki pilotla makul eşleşme sağlanamıyorsa sonuca ulaşana kadar parametre arama; bu tasarımın kalibre edilemediğini kaydet. Avantaj kaybolursa daha güçlü “bağımsız dayanıklılık” iddiasını bırak; sabit bütçedeki toplam yarar ayrı kalır. **Öncelikle bilimsel yorumu değiştirir.**

### 5.5. Öncelik 5 — Ölçüm tuzakları ve yeniden öğrenmenin duyarlılığı

**Soru ve öngörü:** Görülmemiş cümle avantajı bir ifade biçimine mi bağlı; küçük ardışık bilgi izi yeniden öğrenmede kullanılabiliyor mu? Taslak öngörü: ifade çeşitliliği gerçek aktarımı artırıyorsa yön birden fazla tutulmuş anlatımda sürer. Yeniden öğrenme avantajının çıkacağı garanti edilmemeli.

**Karar kuralı:** Önceden yazılmış, eğitimde hiç kullanılmamış en az üç anlatımı ve aynı türden birden fazla yanlış cevabı değerlendirmeye ekle. Sonuçları anlatım başına ayrı göster. Yeniden öğrenmede eski ve yeni bilgilerin 1 / 2 / 4 / 8 gösterim eğrisini karşılaştır; yeni kontrol grubunun ölçülebilir biçimde öğrendiği bir aralık bulunmadan eski–yeni eşitliğini yorumlama.

**Maliyet:** Kaydedilmiş modeller varsa ifade/yanlış-cevap testi 0 yeni tam koşu. Yeniden öğrenme için 3 başlangıç × 2 zamanlama = 6 kısa devam; uygun durumlar yoksa 6 ana koşu eklenir. Var olan durumlarla yaklaşık 0,5–1,5 saatlik ölçüm bütçesi; ana koşular gerekirse ayrıca 0,9–1,2 saat. Gerçek süre ölçüm sayısına bağlıdır.

**Durdurma / pratik etkisi:** Avantaj tek anlatıma özgüyse genelleme tavsiyesini daralt. Kontrol grubu bile öğrenmiyorsa yeniden öğrenme testini sonuçsuz say. **Parafraz tavsiyesini ve “silinme” yorumunu değiştirebilir.**

### 5.6. Öncelik 6 — Güncelleme yönü, keskinlik ve Adam durumunu birlikte sınama

**Soru ve öngörü:** Aynı başlangıç başarısı ve eşit değişim büyüklüğünde, ardışık koşul gerçekten daha kırılgan mı? Taslak öngörü: yönlü geometri önemliyse gerçek bozucu yönlerdeki duyarlılık sonraki kayıpla birlikte artar; Adam durumu önemliyse aynı ağırlıklarda durum değişimi kaybı değiştirir.

**Karar kuralı:** Bölüm 4’teki sonlu-fark, yani küçük artı/eksi değişimlerle türevi yaklaşık ölçme testini, gerçek güncelleme yönünde ve eşit büyüklükte kontrol yönlerinde yap. Sonra Adam durumunu değiştiren dallarda gerçek adım büyüklüğünü eşle. Yalnızca rastgele bir keskinlik sayısı ile sonucu ilişkilendirmek mekanizma kanıtı sayılmasın.

**Maliyet:** Önceki deneylerin 6 model durumu yeniden kullanılabilir; sıfır yeni ana koşu + kısa dallar ve ek hesaplama. Paylaşılan durumlarla 1–2 saatlik pilot bütçe; yoksa ayrıca 6 koşunun 0,9–1,2 saatlik temel süresi.

**Durdurma / pratik etkisi:** Durum veya yön müdahalesi öngörülen ayrımı üretmezse geometrik hikâyeyi büyütme. **Öncelikle bilimsel deneydir**; güvenilir bir ayar değişikliği bulursa pratiğe dönüşür.

### 5.7. Öncelik 7 — İkinci model ve doğal bilgilerde aşamalı tekrar

**Soru ve öngörü:** Etki GPT-2’nin uydurma isimleri öğrenmesine özgü mü? Taslak öngörü: daha genel bir zamanlama etkisi varsa başka bir küçük mimaride de aynı yön görülebilir; büyüklüğün aynı olması beklenmemeli.

**Karar kuralı:** Önce yalnız model değiştir: 3 başlangıç × 2 aralık. Yeterli başlangıç öğrenmesi ve sıfıra sıkışmayan sonraki ölçüm sağlanırsa, ayrı aşamada doğal isimlerle seçilmiş düşük başlangıç bilgili bir veri setine geç. Model ve veri aynı anda değiştirilirse hangi unsurun fark yarattığı belirsizleşir. Önceden bilinen gerçekleri, başlangıçta bilinmeyen sentetik bilgilerle doğrudan aynı havuzda karşılaştırma.

**Maliyet:** İlk aşama 6 koşu, ikinci aşama isteğe bağlı 6 koşu. Mevcut protokol hızındaki karşılık aşama başına 0,9–1,2 saat, toplam 1,8–2,4 saattir; yeni modelin gerçek süresi ilk pilotta ölçülmeli, bu sayı garanti değildir.

**Durdurma / pratik etkisi:** İkinci modelde kalibre edilmiş karşılaştırma etkiyi üretmiyorsa genel öneriyi durdur ve mimariye/ölçeğe bağlılık diye raporla. **Dış geçerliliği ve kullanım alanını doğrudan değiştirir.**

### 5.8. Öncelik 8 — LoRA’yı yalnız kalibrasyon geçerse yeniden deneme

**Soru ve öngörü:** Önceki LoRA sonuçları ölçüm tabanına mı sıkışmıştı, yoksa öğrenme yolu mu farklı? Taslak öngörü: her iki koşul da yeterince öğrenirse aralık farkı ölçülebilir olabilir; olumlu sonuç şart değildir.

**Karar kuralı:** En fazla dört pilot için arama alanını baştan yaz. İki koşulda da pencere sonu doğruluğu hedef [0,5; 0,95] bandına girmeli ve sonraki ölçümler hep sıfır olmamalı. Sağlanırsa yeni bilgilerle 3 başlangıç × 2 koşulluk doğrulama yap. K, pencere veya öğrenme hızı değişirse bunun farklı protokol olduğunu belirt.

**Maliyet:** En fazla 4 pilot + 6 ana koşu = 10. Mevcut koşu hızına göre 1,5–2 saatlik temel karşılık; LoRA’nın gerçek çalışma süresi ayrıca ölçülmeli.

**Durdurma / pratik etkisi:** Dört pilotta kalibrasyon yoksa bırak. “LoRA’da aralık işe yaramaz” değil, “bu bütçeyle karşılaştırma kurulamadı” sonucu ver. **LoRA kullanıcılarına öneriyi doğrudan etkiler.**

### 5.9. Bütçe kararı

**Bu sekiz deneyi bir yapılacaklar borcuna dönüştürme; ilk iki kapı geçilmeden bütün plana kaynak ayırma.** Önce kayıt denetimi, ardından rastgele dağıtım karşılaştırması; bilimsel açıklama için devam edilecekse erken model durumundan veri-türü dalları. Eksik iki Çalışma 5 koşusunu tamamlamak tabloyu temizler, ancak tek başına ana yorum sorununu çözmez.

Sürelerin tümü verilen 9–12 dakika/koşu bilgisinden türetilmiş eğitim karşılıkları veya açıkça etiketlenmiş pilot bütçeleridir. Programlama, hata ayıklama, cihaz ısınması, farklı model hızı ve değerlendirme yoğunluğu dahil değildir. Bunlar yapılmış zaman ölçümleri değildir. 24 GB cihazda model durumlarını aynı anda çoğaltmak yerine dalları sırayla çalıştır; bu öneri de deney sonucundan değil kaynak sınırından türetilmiştir.

## 6. Pratik değer

**Bugünkü savunulabilir öneri, “bu düzende tekrarları yığma ve 16–64 aralığını başlangıç taraması olarak kullan”dır; herkese 64 adım önermek değildir.** [P, Çalışmalar 1 ve 5]

Bilgiyi ince ayarla ekleyen kişiler için proje, toplam tekrar sayısının yanında veri sırasını da kaydetmek gerektiğini gösteren dar kapsamlı bir örnek olabilir. Sürekli öğrenmeyle çalışanlar için, öğrenmenin hemen sonrası ile sonraki başarının ayrılmasını sağlayan bir test düzeni sunar. Veri hazırlama araçlarını yazanlar için ise kopyaların aynı bölümde toplanıp toplanmadığını denetleme fikri verir. Bunlar bu raporun kullanım çıkarımlarıdır; üretim sisteminde ölçülmüş maliyet veya kalite kazançları değildir.

| Kullanım amacı | Şimdi önerilebilecek | Henüz önerilemeyecek |
|---|---|---|
| Benzer GPT-2 bilgi ekleme deneyi | Ardışık ve dağıtılmış tekrarları aynı bütçeyle karşılaştır. | “64 her durumda en iyidir.” |
| Farklı biçimlerde sorulacak bilgi | Eğitimden farklı cümlelerle değerlendirme yap; parafrazı ayrı koşul olarak dene. | “Parafraz her ölçütte üstün.” |
| Olağan veri hazırlama | Tekrar kümelerini ve rastgele karıştırmayı denetle. | “Özel aralık programı normal karıştırmadan daha iyi.” |
| LoRA veya daha büyük model | Önce öğrenme/unutma ölçüm aralığını kalibre et. | “Tam ince ayardaki fark aynen taşınır.” |

Daha geniş öneri için ikinci model, gerçek bilgiye daha yakın veri, öğrenme hızı ve bilgi yoğunluğunda sağlamlık, doğru ölçüm ve başarılı LoRA kalibrasyonu gerekir. “64 adım” farklı paket boyutlarında ve öğrenme hızlarında aynı miktarda model değişimi demek değildir; yakın literatür de bu ayrımı açıkça ele alıyor. [5]

## 7. Yayın ve paylaşım potansiyeli

**Bugünkü en gerçekçi çıktı, sayısal denetimi tamamlanmış açık bir araştırma raporu; daha güçlü makale için daha çok tarama değil, daha ayırıcı kontrol gerekiyor.** Aşağıdaki uygunluk değerlendirmeleri benim değerlendirmemdir; kabul olasılığı tahmini değildir.

| Çıktı / yer | Şimdiki değerlendirme | Eksik olan |
|---|---|---|
| Teknik blog + çalıştırılabilir depo | Denetim düzeltmeleriyle paylaşılabilir. | Ham eşleştirilmiş sonuçlar, çalıştırma komutları, başarısız H1, eksikler ve kapsam sınırı. |
| arXiv araştırma raporu | Çalışmayı dondurmak için anlamlı; hakemli kabul değildir. | Kaynakları güncellenmiş metin, yöntem ayrıntıları, yeniden üretilebilir tablolar. |
| CoLLAs gibi sürekli öğrenme konferansları | Soru tematik olarak uygun; deneysel katkı dar biçimde kurulmalı. | En az bir ayırıcı kontrol, uygun taban çizgisi, kapsamın dürüst sınırlandırılması. |
| I Can’t Believe It’s Not Better türü çalışma toplantıları | Olumsuz sonuç ve metodolojik ders yönü uygun olabilir. | Açık başarısızlık dersi; sentetik deneyi gerçek kullanım iddiasıyla karıştırmamak. |
| TMLR | Yeni rekor veya büyük özgünlük tek başına şart değil; dikkatli ampirik çalışma değerlendirilebilir. | Sonuç–kanıt uyumu, ilgi çekici araştırma sorusu, yeniden üretilebilirlik ve yeterli kontroller. |
| NeurIPS / ICLR ana konferansı | Mevcut özetle güçlü bir ana konferans iddiası kurmazdım. | Basit karşılaştırmaya üstünlük, daha iyi nedensel ayrım, daha geniş doğrulama veya ikna edici mekanizma katkısı. |

**Güncellik notu, 7 Eylül 2026:** CoLLAs 2026’nın doğrulanan tam makale son tarihi 15 Nisan 2026’ydı; bu bir açık başvuru çağrısı değildir. Burada adı geçen I Can’t Believe It’s Not Better örneği ICLR 2025 etkinliğidir; 2026/2027’de aynı çağrının açık olduğunu doğrulamış değilim. TMLR’nin resmi ölçütleri, iddiaların kanıtla desteklenmesini ve okur ilgisini öne çıkarır; yenilik veya en iyi sonuç zorunluluğu diye sunulmamalıdır. [13–15]

Bir makaleyi kurtarmak için H1’i gizlemek yerine, “önceden belirlenen dayanıklılık kararı neden başarısız oldu ve hangi ölçümler daha dar sonucu destekledi?” sorusunu anlatının merkezine koy. Yalnız tek başarısız ayar, iyi bir olumsuz-sonuç makalesi değildir; neden öğretici olduğu ve ölçümün yeterince duyarlı olduğu gösterilmelidir.

Önerdiğim başlık: **“Sabit gösterim bütçesinde tekrar zamanlaması: GPT-2’de edinim, unutma ve soru biçiminin ayrıştırılması.”** Başlığa “insan benzeri hafıza pekişmesi” yazmazdım.

## 8. Öğrenme haritası: projeyi gerçekten sahiplenmek için beş kavram

**Bu projeyi sahiplenmenin ölçütü daha çok terim bilmek değil, bir sonucu hangi alternatif açıklamanın üretebileceğini kendin gösterebilmektir.** Aşağıdaki alıştırmaların amacı yeni büyük deney çıkarmak değil; her biri tek bir araştırma kararını açıklayabilmeni sağlamak.

### 8.1. Adam: nominal hız ile gerçek güncelleme farklıdır

**Öğrenilecek fikir:** Öğrenme hızı aynı kalsa bile geçmiş gradyanlar ve kırpma, gerçek ağırlık değişimini değiştirebilir. Bu nedenle “aynı beş gösterim” ifadesi, aynı öğrenme etkisiyle eşanlamlı değildir. β₁ ve β₂’nin farklı geçmişleri tuttuğunu, sıfırlanan parçadan hareketle bütün optimizasyonu elememek gerektiğini bilmelisin. [9]

**Alıştırma:** İki parametreli bir oyuncak modelde üç gradyan ver. NumPy ile m, v, başlangıç düzeltmesi ve gerçek adımı hesapla. β₁ = 0 yaptığında hangi bellek kaldığını göster. Sonra yalnız son gradyanı sabit tutup geçmişi değiştir: son adım neden değişiyor, sayıyla açıkla.

**Bitirme ölçütü:** “Momentum kapalıysa geçmiş kalmaz” iddiasını somut iki güncellemeyle yanlışlayabiliyorsan bu kavramı kullanabiliyorsun.

### 8.2. Yıkıcı etkileşim: yeni eğitim eski işi neden bozabilir?

**Öğrenilecek fikir:** Aynı ağırlıklar farklı bilgileri desteklediğinde yeni bilginin işine gelen değişim eskisine ters gelebilir. Ancak büyüklük ve yön ayrı şeylerdir. Ham gradyanların karşıtlığı bir işaret verir; Adam’da gerçek adımın eski kayıp üzerindeki yönü esas alınmalıdır. Bölüm 4.1’deki formül bu ayrımın yerel matematiksel ifadesidir.

**Alıştırma:** Önce basit iki görevli bir doğrusal model kur. B görevinin tek güncellemesinden önce ve sonra A kaybını ölç; tahmini g_A · Δθ ile gerçek değişimi karşılaştır. Adımı on kat küçültünce yaklaşımın iyileşip iyileşmediğini kontrol et. Sonra projendeki tek bir genel-metin adımına aynı mantığı uygula.

**Bitirme ölçütü:** Pozitif veya negatif noktasal çarpımın anlamını, gradyan–gradyan ile gradyan–güncelleme karşılaştırmalarında işaret karıştırmadan anlatabilmelisin.

### 8.3. Keskinlik: düşük kayıp, sağlam çözüm demek değildir

**Öğrenilecek fikir:** Bir çözüm, çok küçük ağırlık değişimleriyle bozulabilir; başka bir çözüm aynı başlangıç hatasında daha dayanıklı olabilir. Fakat bu, rastgele tek bir eğrilik sayısının genel başarının evrensel ölçüsü olduğu anlamına gelmez. Ölçek ve hangi yönde değişim uygulandığı önemlidir. [10]

**Alıştırma:** `L₁(x,y) = x² + 100y²` ve `L₂(x,y) = x² + y²` üzerinde aynı uzaklıktaki noktaları dene. x ve y yönündeki eşit değişimlerin zararını karşılaştır. Ardından basit koordinat ölçeklemesiyle aynı işlevi farklı parametrelerle yaz; ham eğriliğin nasıl değiştiğini göster.

**Bitirme ölçütü:** “Keskinlik hangi yönde, hangi ölçekte ve hangi parametreleştirmede?” sorusunu sormadan sonuç yorumlamamalısın.

### 8.4. Ölçüm ve nedensel karşılaştırma: aynı sonuç, farklı hikâyeler

**Öğrenilecek fikir:** Tam cevap doğruluğu, doğru cevabın olasılığı ve yanlış cevaba karşı tercihi farklı soruları cevaplar. Başlangıçta daha iyi olma, daha yavaş unutmayla aynı değildir. Sonradan yalnız öğrenilen bilgileri seçmek, karşılaştırılan grupların bileşimini değiştirebilir. Bu ayrımlar çalışmanın H1 kararının özüdür. [P]

**Alıştırma:** Uydurma iki koşuda doğru cevabın olasılığını 0,49 ve 0,51 yap; rakip cevapla birlikte üretim sırasını incele. Ardından yalnız kazanan örnekleri seçtiğinde grupların nasıl değiştiğini göster. Projende üç çıktıyı yan yana çıkar: bütün bilgiler, her koşulda ayrı öğrenilmiş alt küme, iki koşulda ortak öğrenilmiş alt küme. Son ikisini nedensel kanıt değil duyarlılık kontrolü diye etiketle.

**Bitirme ölçütü:** “Doğruluk sıfırsa NLL neden değişebilir?” ve “200 bilgi neden 200 bağımsız model tekrarı değildir?” sorularını örnekle cevaplayabilmelisin.

### 8.5. Aralık, gecikme, yeniden öğrenme ve değişken anlatım

**Öğrenilecek fikir:** Aralık etkisi, dağıtılmış tekrarın yığılmış tekrarla farkıdır; gecikme etkisi, aralığın uzunluğuyla başarının nasıl değiştiğidir; yeniden öğrenme tasarrufu, eski bilginin yeniden öğrenilmesinin yeni bilgiden kolay olmasıdır. İfade çeşitliliği ise aynı içeriğin farklı biçimlerde görülmesidir. Bunlar ilişkili ama birbirinin yerine geçmeyen kavramlardır. İnsan deneylerindeki zaman ölçeğini eğitim adımlarına doğrudan taşıyamazsın. [8; tanımların projeye uygulanışı bu rapor]

**Alıştırma:** Son gösterimi E olan beş tekrar için `[E−4g, E−3g, E−2g, E−g, E]` programını yaz. Her bilgi için beş kayıt, ortak son zaman ve pencere sınırları test edilsin. g = 64’te ilk–son açıklığın 256 olduğunu göster. Sonra hiçbir ağırlık güncellemesi yapmadan yalnız beklemenin deterministik değerlendirmede sonucu değiştirmediğini kontrol et.

**Bitirme ölçütü:** Projedeki “zaman”, saatin akması değil ağırlıkları değiştiren eğitim geçmişidir. Bunu hem kod testinde hem açıklamada ayırabilmelisin.

## 9. İnfografiğin denetlenebilir metin eki

**Aşağıdaki metin, önceki görselin sayılarını kontrol etmeye ve fazla güçlü ifadeleri daha dikkatli yazmaya yarar; yeni bir görsel değildir.** Deney değerleri yalnız [P] kaynağından alınmıştır.

1. **Başlık:** SpacingLab — Aynı bilgi, farklı tekrar aralıkları.
2. **Alt başlık:** GPT-2 124M • 200 yapay bilgi • Bilgi başına 5 gösterim.
3. **Zaman çizgisi:** Isınma: 100 adım, yalnız genel metin → Öğretme: 700 adım, tekrar aralıkları 1 / 4 / 16 / 64 → Unutturma: 1.500 adım, genel metin ve 50 yeni bilgi.
4. **Eşleştirme:** Toplam gösterim, adım ve token bütçeleri ile her bilginin son gösterim zamanı eşleştirildiği bildiriliyor; adım-bazlı etkin ağırlık ayrıca denetlenmeli.
5. **Ana grafik:** Hatırlama skoru, sonraki yedi kontrol noktasındaki ortalama doğruluktur. Aralık 1: 0,001; aralık 4: 0,023; aralık 16: 0,124; aralık 64: 0,285.
6. **Büyük aralık notu:** Ayrı, 1.400 adımlık öğretme penceresinde 128 / 256’nın 64’e karşı tutarlı ek üstünlüğü gösterilmedi. İki sonuç bekliyor; kesin optimum belirlenmedi.
7. **Edinim ve kayıp:** Kendi son gösteriminden hemen sonra → öğretme penceresi sonunda: ardışık 0,43 → 0,03; 64 aralıklı 0,81 → 0,65. Oklar bütün bilgiler için tam 50 adımı temsil etmez. Ardışık koşulda yaklaşık 50 adım içinde hızlı üretim kaybı bildiriliyor; tamamen silinme kanıtı değil.
8. **Dört kontrol:** Daha çok tekrar: 10 / 20 gösterim, tek başlangıçta kalıcı yüksek başarı sağlamadı. β₁ = 0: avantaj sürdü; Adam’ın bütün geçmişi kapatılmadı. LoRA: kalibrasyon ve sıfıra sıkışma nedeniyle kalıcılık karşılaştırması yetersiz. Farklı cümleler: ardışık koşulu kurtarmadı.
9. **Soru biçimi:** Aralıklı kopyalar — çalışılan cümle 0,306, görülmemiş cümle 0,060. Aralıklı farklı anlatımlar — çalışılan cümle 0,092, görülmemiş cümle 0,108. Kopyalar çalışılan ifadede, farklı anlatımlar bu yeni ifadede daha iyi.
10. **Pratik cümle:** Bu düzende tekrarları üst üste yığma; 16–64 adımı başlangıç taraması olarak dene. 64 evrensel optimum değil.
11. **Bilimsel sınır:** Önceden yazılmış H1 desteklenmedi: başlangıç öğrenmesi ile unutmaya dayanıklılık tam ayrılmadı.

## 10. Son değerlendirme

**Proje şu anda bir “mekanizma keşfi” değil; dikkatli sınırlandırılırsa yararlı bir deneysel zamanlama bulgusu ve ölçüm dersi.** En kuvvetli tarafı büyük ana fark, son gösterim zamanını eşleme ve başarısız kararın kayda geçirilmesi. En zayıf tarafı ise etkin eğitim ağırlığı, başlangıç öğrenmesi ve ölçüm duyarlılığı açıkken bu farkı tek bir hafıza mekanizmasına bağlama riski. [P; değerlendirme]

Benim önerim: önce denetim dosyasını çıkar, sonra rastgele karıştırma taban çizgisini ekle. Bilimsel açıklama için bir adım daha atılacaksa, son gösterim anındaki modelden farklı bozucu veri dalları başlat. Bu sıra, daha çok koşu üretmekten önce hangi sorunun gerçekten cevaplandığını netleştirir.

## Kaynaklar ve doğrulama sınırları

**Deney sonuçlarının tek kaynağı paylaşılan proje özeti; dış yayınlar yalnız karşılaştırma ve yöntem değerlendirmesi için kullanıldı.** Dış kaynakların sonuçları bu çalışma tarafından yeniden üretilmedi. Erişim/değerlendirme tarihi: 7 Eylül 2026.

[P] Mehmet. “Pasted markdown.md”, bu konuşmada paylaşılan SpacingLab proje özeti. Çalışmalar 1–5, deney düzeni ve kısıtlar. Özel depo ve ham koşu kayıtları bu incelemede incelenmedi.

[1] Chang ve arkadaşları (2024). How Do Large Language Models Acquire Factual Knowledge During Pretraining? NeurIPS 2024. Tam metin, özellikle Bölüm 3–4 ve Ek D. https://arxiv.org/html/2406.11813v2

[2] Allen-Zhu, Z. ve Li, Y. (2024). Physics of Language Models: Part 3.1, Knowledge Storage and Extraction. ICML, PMLR 235. Resmi yayın kaydı. https://proceedings.mlr.press/v235/allen-zhu24a.html

[3] Sun ve arkadaşları (2025). Right Time to Learn: Promoting Generalization via Bio-inspired Spacing Effect in Knowledge Distillation. arXiv:2502.06192, v2. https://arxiv.org/html/2502.06192v2

[4] Sun ve arkadaşları (2026). Spacing effect improves generalization in biological and artificial systems. Patterns 7(6), 101564. DOI: 10.1016/j.patter.2026.101564. Yayın kaydı ve kurum özeti doğrulandı; tam yöntem bu incelemede erişilemedi. https://www.sciencedirect.com/science/article/pii/S2666389926000735

[5] Feng ve arkadaşları (2026). FOREVER: Forgetting Curve-Inspired Memory Replay for Language Model Continual Learning. arXiv:2601.03938; incelenen ikinci sürüm 20 Nisan 2026. https://arxiv.org/html/2601.03938v2

[6] Lu, Y., He, Y., Chen, J. ve Zha, H. (2026). MSSR: Memory-Aware Adaptive Replay for Continual LLM Fine-Tuning. arXiv:2603.09892, 10 Mart 2026 önbaskısı. https://arxiv.org/html/2603.09892v1

[7] Wen ve Zhang (2025). On the Retention of Edited Knowledge in Fine-tuned Language Models; özet kaydında Retention analysis of edited knowledge after fine-tuning başlığıyla da yer alıyor. arXiv:2507.14198v2. https://arxiv.org/html/2507.14198v2

[8] Cepeda ve arkadaşları (2008). Spacing Effects in Learning: A Temporal Ridgeline of Optimal Retention. Psychological Science 19(11), 1095–1102. DOI: 10.1111/j.1467-9280.2008.02209.x. Resmi yayın özeti. https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.2008.02209.x/

[9] Kingma, D. P. ve Ba, J. Adam: A Method for Stochastic Optimization. arXiv:1412.6980; ICLR 2015. https://arxiv.org/abs/1412.6980

[10] Dinh, L., Pascanu, R., Bengio, S. ve Bengio, Y. (2017). Sharp Minima Can Generalize For Deep Nets. arXiv:1703.04933. https://arxiv.org/abs/1703.04933

[11] Hernandez ve arkadaşları (2022). Scaling Laws and Interpretability of Learning from Repeated Data. arXiv:2205.10487. https://arxiv.org/abs/2205.10487

[12] Muennighoff ve arkadaşları (2023). Scaling Data-Constrained Language Models. arXiv:2305.16264. https://arxiv.org/abs/2305.16264

[13] TMLR. Resmi kabul ölçütleri ve yayın politikaları. https://jmlr.org/tmlr/acceptance-criteria.html

[14] CoLLAs 2026. Program başkanlarının tam makale çağrısı; doğrulanan son tarih 15 Nisan 2026. https://groups.google.com/g/ml-news/c/fP11vk8F7Dc

[15] I Can’t Believe It’s Not Better! ICLR 2025 çalışma toplantısının resmi sayfası. Güncel açık başvuru önerisi değil, tarihsel yer örneği. https://sites.google.com/view/icbinb-2025

[16] PyTorch. AdamW resmi uygulama belgesi; güncelleme kuralı ve betas parametresi. https://docs.pytorch.org/docs/main/generated/torch.optim.adamw.AdamW_class.html
