# SpacingLab — güncel durum (8 Eylül 2026)

**Son kontrol, rastgele tekrarın düzenli tekrardan daha iyi olduğunu gösteremedi;
şimdi tekrarların başlangıcını ve bitişini de eşitleyerek aralıkları karşılaştırıyoruz.**

## Tamamlanan kontrol: Study 8

Örnek: iki öğrenci de aynı bilginin son tekrarını cuma günü yapıyor.
Önceki dört tekrar birinde düzenli, diğerinde rastgele. Her yöntemi üç kez denedik.

Sonraki yedi sınavdaki doğru cevap oranının ortalaması:

| Yöntem | Ortalama | Koşular arası standart sapma | Üç koşudaki aralık |
|---|---:|---:|---:|
| Düzenli | %28,1 | 8,3 yüzde puan | %19,4–36,1 |
| Son tekrarı eşitlenmiş rastgele | %29,7 | 4,2 yüzde puan | %24,9–32,9 |

Eşleştirilmiş avantaj ortalama 1,6 puan, fakat koşudan koşuya değişimi gösteren
standart sapma 4,4 puan. Üç ayrı fark: -3,2, +2,5 ve +5,5 puan.
Bu nedenle “rastgele daha iyi” diyemiyoruz; “ikisi kesin eşit” de diyemiyoruz.
Doğru cevaba verilen olasılığı izleyen NLL ölçüsünde fark -0,054, standart sapma
0,081; bu küçük ve değişken fark da güçlü bir üstünlük göstermiyor.

Önceki Study 7'nin daha büyük avantajı burada tekrarlanmadı. Ancak tüm farkın
sebebinin son tekrar zamanı olduğunu kanıtlamadık: önceki tekrarların dağılımı da
değişti. Başlangıçta öğrenilen miktarlar da eşit değildi.

## Şimdi çalışan deney: Study 9

Beş gösterim arasında dört boşluk var:

- Düzenli: 64 → 64 → 64 → 64 eğitim adımı.
- Değişken: 32, 32, 64, 128 adımlarının her bilgi için karıştırılmış sırası.

İkisinin de toplamı 256, ortalaması 64. Her bilginin ilk ve son gösterimi aynı.
Böylece farklı toplam süreyi veya daha yakın son tekrarı avantaj saymayacağız.
64'ün evrensel en iyi aralık olduğunu varsaymıyoruz.

Plan sonuçlardan önce Git'e kaydedildi; 33 yazılım testi geçti.
Altı yeni koşu sırayla çalışıyor; ilk koşuda eğitim ilerliyor, henüz toplu sonuç yok.
Toplam yaklaşık 1,5–2 saat; bilgisayar açık ve uyanık kalmalı.
Sonuç olumlu da olumsuz da olsa üç koşunun değişkenliğiyle raporlanacak.

Bu deney küçük GPT-2 modelinde yapay bilgiler üzerine. Senin üslubunu öğrenmeyi,
kişisel mesajlarını veya LoRA'yı test etmiyor. Kişisel verilerine dokunulmadı.

- [Study 8 ayrıntılı sonuçları](results/study8/REPORT.md)
- [Study 9 önceden kaydedilmiş planı](docs/STUDY9_PREREGISTRATION.md)
- [Eski veri eşleşmesi hatasının denetimi](docs/PROVENANCE_AUDIT_2026-09-08.md)

Her şey yerelde; GitHub'a gönderim veya paylaşım yapılmadı.
