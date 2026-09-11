# SpacingLab — Deney 13 tamamlandı (10 Eylül 2026)

**İki yönteme de eşit sayıda farklı bilgiyi tekrar ettirdiğimizde, unutulmaya
başlayanları seçmek üç karşılaştırmada da daha iyi sonuç verdi.**

## Ne yaptık?

Aynı öğrenilmiş modelin iki kopyasını kullandık. İkisi de **80 farklı bilgiyi
birer kez** tekrar etti; birisi rastgele seçti, diğeri ilk öğrendiği zamana göre
doğru cevabına daha az güvenmeye başladığı bilgileri seçti. Eğitim miktarı ve
tekrar zamanları eşitti. Sonra eski 200 bilginin tamamını beş ayrı zamanda sorduk.

Bir öğrencinin tekrar için rastgele 80 kart seçmesiyle, eskiden bildiği ama artık
karıştırmaya başladığı 80 kartı seçmesini karşılaştırmak gibi.

## Sonuç

| Karşılaştırma | Seçici tekrarın avantajı |
|---|---:|
| 1 | +6,6 puan |
| 2 | +2,2 puan |
| 3 | +4,7 puan |

Ortalama avantaj **4,5 puan**, denemeler arası değişimi gösteren standart sapma
**2,21 puan**. Bu bir güven aralığı değil. Rastgele yöntem %41,30 doğruluk
(standart sapma 4,24 puan), seçici yöntem %45,80 (4,60 puan) aldı.

100 soruluk sınavlarda ortalama yaklaşık **4–5 soru daha doğru** gibi.
Bu, tek son sınavın değil, beş farklı zamandaki sınavların ortalaması.

## Neyi öğrendik, neyi öğrenmedik?

Bu deneyde avantajı “daha fazla farklı bilgiye baktı” diye açıklayamıyoruz:
ikisinde de sayı tam 80. Bu, unutulmaya başlayanları seçme fikri için olumlu
ama küçük ölçekli bir bulgu.

**Her ölçüm olumlu değildi:** yalnızca en son sınava bakınca bir karşılaştırmada
seçici yöntem az farkla gerideydi. Doğru cevabı yanlış alternatifinden ayırma
ölçüsünde de tutarlı ek avantaj yok. “Modelin içindeki hafızayı güçlendirdik”
ya da “her zaman daha iyi” demiyoruz.

Yalnızca küçük GPT-2 ve yapay bilgiler test edildi. Senin konuşma biçimini öğrenme,
büyük modeller veya insan beyni hakkında sonuç yok. Önceki deneyde iki yöntemin
kuralları farklıydı; bu sonuç onun nedenini kesin olarak açıklamıyor.

## Sırada ne olabilir?

Devam etmeye değer buluyorum. Bir sonraki soru şu olabilir:
**“Unutulmaya başlayanları mı seçmeliyiz, yoksa şu anda en zor gelenleri mi?”**
Önceden bilip karıştırmaya başladığın kartla, zaten zor gelen kart aynı şey değil.

Bu yalnızca öneri. **Eğitim tamamlandı; yeni koşu başlatılmadı.**
Sen anlayıp açıkça onaylamadan yeni deneye geçmeyeceğiz.

Ham kayıtlar, eşit başlangıç ve tekrar koşulları doğrulandı; 80 yazılım testi geçti.

- [İngilizce değerlendirme](results/study13/WRITEUP.md)
- [Tüm ölçümler](results/study13/REPORT.md)
- [Kontroller ve sınırları](results/study13/AUDIT.md)
- [Önceden kaydedilen plan](docs/STUDY13_PREREGISTRATION.md)
