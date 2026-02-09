# Student Performance Analysis – Hive, Scala Spark, PySpark

## Kullanılan Veri Seti
**student-mat.csv** dosyası; öğrencilerin demografik bilgileri, aile yapısı, sosyal aktiviteleri, çalışma süreleri ve üç sınav notunu (G1, G2, G3) içermektedir.

Veri seti HDFS üzerinde şu dizinde tutulmuştur:
hdfs://localhost:9000/user/asude/student/student-mat.csv
 ## Not: Tüm dosyalar aynı klasörde tutulmalı ve çalıştırmadan önce HDFS, YARN ve Hive servislerinin açık olduğundan emin olunmalıdır.
start-dfs.sh
start-yarn.sh 

# 1️- Hive Analizi – `hive_queries.sql`

Hive ile;
- Temel istatistikler
- Gruplama ve ortalama hesaplamaları
- Destek programları ile başarı arasındaki ilişki
- Aile desteği – başarı ilişkisi  
gibi sorgular çalıştırılmıştır.

### Çalıştırmak için:

hive -f /home/asude/student/hive_queries.sql

# 2- Scala Spark Analizi – 'scala_analysis.scala'

Scala ile Spark üzerinde:
- Toplam başarı puanı (total_score)
- Null değer sayımı
- Başarı durumunun sınıflandırılması (passed / failed)
- Çalışma süresi – başarı ilişkisi
- Alkol tüketimi – başarı ilişkisi
- Temel gösterimler (df.show())
### Çalıştırmak için:
spark-shell -i /home/asude/student/scala_analysis.scala
 
# 3️- PySpark Analizi – pyspark_analysis.py

Python ile Spark üzerinde daha gelişmiş bir analiz yapılmıştır:

✨ Uygulanan işlemler:

- Feature Engineering
- total_score
- social_score (goout, freetime, Walc)
- risk_score (failures + alkol + devamsızlık)
- Başarı kategorisi (A/B/C/D)
- Window Function ile en başarılı 10 öğrenci
- Yaş bazlı başarı analizi
- Çalışma süresi → not ortalaması ilişkisi
- Korelasyon analizi
- İnternet erişimi → başarı etkisi
### Çalıştırmak için:
spark-submit /home/asude/student/pyspark_analysis.py

## Kullanılan Teknolojiler
- Apache Hadoop (HDFS)
- Apache Hive
- Apache Spark
  Spark SQL
  PySpark
  Scala
- Linux / Ubuntu
- HDFS üzerinde veri işleme
