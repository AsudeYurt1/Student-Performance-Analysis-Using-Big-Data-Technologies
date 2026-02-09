import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

val spark = SparkSession.builder()
  .appName("StudentScalaAnalysis")
  .master("local[*]")
  .getOrCreate()

import spark.implicits._

// 1) CSV Yükleme

val df = spark.read
  .option("header", "true")
  .option("sep", ";")
  .option("inferSchema", "true")
  .csv("hdfs://localhost:9000/user/asude/student/student-mat.csv")

println("==== Orijinal Veri (Temiz Gösterim) ====")

val dfClean = df.select(
  col("school").alias("sch"),
  col("sex"),
  col("age"),
  col("address").alias("addr"),
  col("famsize").alias("fam"),
  col("studytime").alias("study"),
  col("failures").alias("fail"),
  col("internet").alias("net"),
  col("G1"), col("G2"), col("G3")
)

dfClean.show(5, false)

// 2) Toplam başarı puanı ekleme

val df2 = df.withColumn("total_score", col("G1") + col("G2") + col("G3"))

// 3) Null sayımı (daha temiz çıktı)

val nullCounts = df2.columns.map(c =>
  (c, df2.filter(col(c).isNull).count())
).toSeq.toDF("column", "null_count")

println("==== Null Sayıları ====")
nullCounts.show(50, false)

// 4) Geçen / Kalan belirleme

val df3 = df2.withColumn("passed",
  when(col("G3") >= 10, "yes").otherwise("no")
)

println("==== Geçen / Kalan Örnek ====")
df3.select("school", "sex", "G3", "total_score", "passed")
  .show(10, false)

// 5) Çalışma süresine göre başarı

println("==== Çalışma Süresine Göre Ortalama Not ====")

df3.groupBy("studytime")
  .agg(avg("G3").alias("avg_final_grade"))
  .orderBy("studytime")
  .show(false)

// 6) Günlük / Haftalık alkol tüketimi – başarı ilişkisi

println("==== Alkol Tüketimi ve Başarı İlişkisi ====")

df3.groupBy("Dalc", "Walc")
  .agg(avg("G3").alias("avg_grade"))
  .orderBy(desc("avg_grade"))
  .show(20, false)
// 7) Okula göre final notu ortalaması

println("==== Okullara Göre Ortalama Final Notu (G3) ====")

df3.groupBy("school")
  .agg(avg("G3").alias("avg_final_grade"))
  .orderBy(desc("avg_final_grade"))
  .show(false)

