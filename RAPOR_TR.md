# SpacingLab — güncel durum (9 Eylül 2026)

**Karışık aralıklar ilk denemede ortalamada öne geçti, ama sonuç tutarlı değildi.
Şimdi aynı karşılaştırmayı üç yeni rastgelelik ayarıyla tekrar ediyoruz.**

## Tamamlanan deney: Study 9

Beş gösterim arasında sabit 64–64–64–64 boşlukları ile 32–32–64–128'in
karıştırılmış sırasını karşılaştırdık. İlk ve son gösterim her bilgi için aynıydı.

| Yöntem | Sonraki yedi sınavda ortalama doğruluk | Standart sapma | Üç koşudaki aralık |
|---|---:|---:|---:|
| Sabit aralık | %28,7 | 4,0 yüzde puan | %25,2–33,0 |
| Değişken aralık | %32,9 | 9,7 yüzde puan | %23,2–42,6 |

Standart sapma koşudan koşuya değişkenliği gösterir; güven aralığı değildir.
Üç eşleştirilmiş avantaj: +9,6, +5,1 ve -2,0 puan.
Ortalama fark +4,2 puan; standart sapması 5,9 puan. İki kazanç, bir kayıp:
önceden belirlediğimiz kurala göre sonuç belirsiz. Kesin üstünlük veya eşitlik yok.

Doğru cevaba verilen olasılığı izleyen NLL farkı -0,075, standart sapması 0,083;
küçük ve değişken. Karışık grup son gösterimde de daha iyi öğrenmişti:
doğruluk farkı +4,2 puan, standart sapması 2,0 puan. Bu yüzden avantajı doğrudan
“daha az unutuyor” diye yorumlayamayız. Altı koşunun ham sonuçları Git'te saklandı.

## Şimdi çalışan tekrar: Study 10

Aynı iki yöntemi üç yeni rastgelelik ayarıyla, toplam altı yeni eğitimde deniyoruz.
Model, tekrar sayısı, aralıklar ve toplam eğitim miktarı değişmedi.
Örnek: aynı çalışma yöntemlerini bu kez üç yeni soru setinde sınamak gibi.
Yeni sonuçları eskilere karıştırmadan ayrıca değerlendireceğiz.

Plan sonuçlardan önce kaydedildi; 39 yazılım testi ve iki başlangıç kontrolü geçti.
İlk eğitim başladı. Tüm zincir yaklaşık 1,5–2 saat sürebilir; bilgisayar uyanık kalmalı.
Sonuç iyi görünene kadar koşu eklemeyeceğiz. Üç yeni karşılaştırmanın tamamını
olumlu veya olumsuz fark etmeksizin raporlayacağız.

Sonuçta kısa açıklamaya ek olarak imagegen ile Türkçe bir infografik hazırlanacak:
iki tekrar düzeni, üç ayrı karşılaştırma ve belirsizlik görselde birlikte gösterilecek.
Sonuçları kontrol eden takip görevi 20 dakikada bir çalışacak; normal ilerleyişte
sessiz kalacak, tamamlanınca veya sorun çıkınca haber verecek ve teslimden sonra duracak.

Bu hâlâ küçük GPT-2 modelinde yapay bilgi deneyi. İnsan beyni mekanizmasını,
kişiselleştirmeyi, senin konuşma biçimini veya LoRA'yı kanıtlamıyor.
Kişisel mesajlarına dokunulmadı; her şey yerelde, paylaşım yapılmadı.

- [Study 9 ayrıntılı sonuçları](results/study9/REPORT.md)
- [Study 10 önceden kaydedilmiş planı](docs/STUDY10_PREREGISTRATION.md)
- [Tarihsel veri eşleşmesi denetimi](docs/PROVENANCE_AUDIT_2026-09-08.md)
