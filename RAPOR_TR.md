# SpacingLab — güncel durum (8 Eylül 2026)

**Son tamamlanan deneyde rastgele tekrar daha iyi çıktı; şimdi bunun “son tekrarı
daha yakın zamanda görme” avantajından kaynaklanıp kaynaklanmadığını kontrol ediyoruz.**

## Tamamlanan sonuç: Study 7

İki yöntemi aynı model ve aynı eğitim metinleriyle üçer kez çalıştırdık.
Sonraki yedi sınavın ortalamasında:

| Yöntem | Doğru cevap ortalaması | Üç koşudaki aralık |
|---|---:|---:|
| Düzenli tekrar | %27,3 | %20,4–36,6 |
| Rastgele tekrar | %36,6 | %31,9–42,9 |

Ortalamaların koşudan koşuya değişimini gösteren standart sapma sırasıyla
8,3 ve 5,7 yüzde puan. Eşleştirilmiş fark ortalama **9,3 puan**; standart sapması
4,6 puan, üç koşudaki farklar 6,4–14,6 puan. Doğru cevaba verilen olasılığı
izleyen NLL ölçüsü de rastgele yöntemi destekledi.

Ama rastgele yöntemde son tekrar daha geç oluyordu. Bu, özel bir hafıza mekanizması
bulduğumuz anlamına gelmiyor. Yeni bilgi öğrenmedeki küçük değişiklikler ve diğer
kontroller [ayrıntılı sonuçta](results/study7/REPORT.md) korunuyor.

## Şimdi çalışan kontrol: Study 8

Örnek: iki öğrenci de aynı bilginin son tekrarını cuma günü yapıyor.
Birinin önceki dört tekrarı düzenli aralıklı, diğerinin rastgele.
Böylece “biri sınavdan daha kısa süre önce gördü” açıklamasını kontrol ediyoruz.

Her bilginin son gösterimi **birebir eşit** olacak; sadece ortalama zaman değil.
İki grubu da yeniden eğitiyoruz: üç farklı rastgelelik ayarı, toplam altı koşu.
Plan başlamadan Git'e kaydedildi; 29 test geçti. İlk koşu başladı, **henüz sonuç yok**.
Tüm zincir yaklaşık 1,5–2 saat sürebilir; bilgisayar açık ve uyanık kalmalı.

Fark devam ederse son tekrarın yakınlığı tek başına açıklama olamaz.
Fark kaybolursa da “sebep kesin buydu” demeyeceğiz: önceki tekrarların dağılımı da
bu kontrolde değişiyor. Tek küçük model ve üç koşuyla evrensel kural çıkarmayacağız.

- [Yeni deneyin önceden kaydedilmiş planı](docs/STUDY8_PREREGISTRATION.md)
- [Tamamlanan Study 7 sonuçları](results/study7/REPORT.md)
- [Eski veri eşleşmesi hatasının denetimi](docs/PROVENANCE_AUDIT_2026-09-08.md)

Eski sonuçlar korundu ve Git'e kaydedildi. GitHub'a gönderim veya paylaşım yapılmadı.
