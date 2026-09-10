# SpacingLab — Deney 12 tamamlandı (10 Eylül 2026)

> Güncelleme: Onayınla Deney 13 başlatıldı. Bu kez iki yöntem de 80 farklı
> bilgiyi birer kez tekrar ediyor. Henüz sonucu yok; aşağıdaki rapor tamamlanmış
> Deney 12'ye ait. Bu kontrolün ötesinde yeni bir deney başlatılmayacak.

**Unutulmaya başlayan bilgileri seçip tekrar etmek, bu küçük deneyde rastgele
tekrardan daha iyi sonuç verdi.**

## Ne yaptık?

Aynı öğrenilmiş modelin iki kopyasına eşit miktarda yeni veri ve **80 tekrar hakkı**
verdik. A, önceden öğrendiği bilgilerden rastgele seçti. B, başlangıca göre cevabına
daha az güvenmeye başladığı bilgileri seçti. Yalnızca seçilenleri değil, eski
200 bilginin tamamını daha sonra beş kez sınadık.

## Sonuç

| Karşılaştırma | B'nin A'ya göre avantajı |
|---|---:|
| 1 | +2,4 puan |
| 2 | +2,2 puan |
| 3 | +5,1 puan |

Ortalama avantaj **3,23 puan**. Denemeler arasındaki değişimi gösteren standart
sapma **1,62 puan**; bu bir güven aralığı değil. Rastgele yöntemin ortalaması
%43,63 (standart sapma 3,59 puan), seçici yöntemin %46,87 (4,61 puan).

100 soruluk sınavlarda ortalama yaklaşık **üç soru daha doğru** gibi düşünebilirsin.
Burada tek sınav değil, beş farklı zamandaki sınavın ortalamasına bakıyoruz.
Üçünde de aynı yön çıktı ve önceden belirlediğimiz küçük-test koşulu karşılandı.
Ama üç deneme, “kesin ve her yerde daha iyi” demek için yeterli değil.

## Henüz neyi bilmiyoruz?

Seçici yöntem aynı 80 hakkı **daha fazla farklı bilgiye** dağıtmış. Belki avantajın
bir kısmı, unutmayı ölçmekten değil, aynı bilgiyi tekrar tekrar seçmemekten geliyor.
Doğruyla yanlış cevabı ayırma ölçüsünde de tutarlı bir ek iyileşme bulmadık.
Bu nedenle “modelin içindeki hafızayı güçlendirdik” demiyoruz.

Yalnızca küçük GPT-2 ve yapay bilgiler test edildi. Senin konuşma biçimini öğrenme,
büyük modeller veya insan beyninin çalışma şekli hakkında henüz sonuç yok.

## Sırada ne olabilir?

**Devam etmeye değer.** Bir sonraki karşılaştırmada rastgele yöntemin de daha fazla
farklı bilgiyi ziyaret etmesini sağlayabiliriz. Böylece “unutulanı seçmek mi,
yoksa tekrarı daha geniş dağıtmak mı faydalı?” sorusunu ayırırız.

Bu yalnızca öneri. **Eğitim bitti; yeni deney başlatılmadı.** Yeni planı birlikte
netleştirip sen onaylamadan devam etmeyeceğiz.

Ham kayıtlar ve eşit başlangıç/tekrar kontrolleri doğrulandı; 60 yazılım testi geçti.

- [İngilizce değerlendirme](results/study12/WRITEUP.md)
- [Tüm ana ölçümler](results/study12/REPORT.md)
- [Kontrol kaydı ve sınırları](results/study12/AUDIT.md)
- [Deneyden önce kaydedilmiş plan](docs/STUDY12_PREREGISTRATION.md)
- [Önceki aralık deneyi: ayrı, belirsiz sonuç](results/study11/WRITEUP.md)
