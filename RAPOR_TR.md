# SpacingLab — Deney 11 tamamlandı (10 Eylül 2026)

**Karışık aralıkların üstünlüğü bu küçük tekrar testinde de çıkmadı.**
Üç karşılaştırmada da sabit aralık biraz daha yüksek sonuç verdi; ancak farkın
büyüklüğü değiştiği için “sabit kesin daha iyi” de demiyoruz.

## Ne yaptık?

Aynı bilgiyi beş kez gösterdik. Bir grupta aralar 64–64–64–64 eğitim adımıydı;
diğerinde 32–32–64–128'in karıştırılmış sırasıydı. İlk ve son gösterim ile
toplam tekrar sayısı aynıydı. Aralarda başka metinlerle eğitim sürdü.
Üç yeni karşılaştırma, yani altı eğitim yapıldı ve duruldu.

## Sonraki yedi sınavın ortalaması

| Karşılaştırma | Sabit | Karışık | Karışığın farkı |
|---|---:|---:|---:|
| 1 (seed 6) | %31,86 | %27,21 | −4,64 puan |
| 2 (seed 7) | %26,93 | %25,93 | −1,00 puan |
| 3 (seed 8) | %28,79 | %28,64 | −0,14 puan |

Farkın ortalaması **−1,93 puan**, denemeler arasındaki değişimi gösteren
standart sapması **2,39 puan**. Bu bir güven aralığı değil.
Sabit ortalaması %29,19 (standart sapma 2,49 puan);
karışık ortalaması %27,26 (standart sapma 1,36 puan).

Örnek olarak 100 soruluk bir sınavda bir yöntemin yaklaşık iki soru geride
kalması gibi düşünebilirsin. Ancak burada tek sınav değil, farklı zamanlardaki
yedi sınavın ortalaması ölçüldü. En küçük farklar tek başına güçlü bir sonuç değil.

## Önemli ayrım

Karışık düzen eğitim penceresinin sonunda daha iyi görünüyordu:
fark ortalama +4,83 puan, standart sapma 3,40 puan. Ama bu erken avantaj sonraki
ölçümlerde korunmadı. Başlangıçtaki öğrenme düzeyi eşit olmadığından saf bir
“unutma hızı” karşılaştırması yaptığımızı söyleyemeyiz.

Önceki turda doğru cevaba verilen olasılık açısından görülen olumlu yön,
bu turda tutarlı tekrarlanmadı. Doğru ve yanlış cevabı ayırma ölçüsünde olumlu bir
yan bulgu vardı; fakat bunu ana sonuç yerine koymuyoruz.
Ayrıntılar [İngilizce değerlendirmede](results/study11/WRITEUP.md).

## Şimdi ne olacak?

Anlaştığımız kurala göre daha fazla aralık denemesi eklemiyoruz; bu soruyu
**“bu düzende üstünlük gösterilemedi”** diye beklemeye almayı öneriyorum.
Bu, karışık aralıkların hiçbir koşulda faydalı olamayacağı anlamına gelmez.

Sonraki olası soru: **“Rastgele tekrar etmek yerine, önceden öğrenilmiş ama
unutulmaya başlayan bilgileri seçip tekrar etmek daha faydalı mı?”**
Önce bunu birlikte anlayıp planlayacağız. **Yeni deney başlatılmadı.**

Yalnızca küçük GPT-2 modeli ve yapay bilgiler test edildi; kişisel konuşma biçimi,
büyük modeller veya insan beynindeki mekanizma hakkında sonuç çıkarmıyoruz.
Önceki iki tur ayrı tutuldu, tüm sonuçlar saklandı. Altı kayıt ve hesaplar
bağımsız kontrol edildi; 46 yazılım testi geçti. Otomatik takip duraklatıldı.

- [Tüm ölçümler](results/study11/REPORT.md)
- [Kontrol kaydı](results/study11/AUDIT.md)
- [Önceden yazılmış deney planı](docs/STUDY11_PREREGISTRATION.md)
