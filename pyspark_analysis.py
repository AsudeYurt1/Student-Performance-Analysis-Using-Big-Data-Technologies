from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("StudentPySparkAnalysis") \
    .master("local[*]") \
    .getOrCreate()


# 1) CSV Yükleme

df = spark.read \
    .option("header", "true") \
    .option("sep", ";") \
    .option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/user/asude/student/student-mat.csv")

df.show(5, truncate=False)

# 2) Toplam başarı puanı

df = df.withColumn("total_score", col("G1") + col("G2") + col("G3"))

# 3) Sosyal Aktivite Skoru (0–10)

df = df.withColumn(
    "social_score",
    col("goout")*2 + col("freetime") + col("Walc")
)

# 4) Başarı kategorisi (A/B/C/D)

df = df.withColumn(
    "grade_level",
    when(col("G3") >= 15, "A")
    .when(col("G3") >= 12, "B")
    .when(col("G3") >= 10, "C")
    .otherwise("D")
)

# 5) Risk Skoru (disiplin + alkol + devamsızlık)

df = df.withColumn(
    "risk_score",
    col("failures") * 3 + col("Walc") + col("Dalc") + (col("absences") / 5)
)

# 6) En başarılı 10 öğrenci (Window Function)

w = Window.orderBy(col("total_score").desc())

df_ranked = df.withColumn("rank", rank().over(w))
top10 = df_ranked.filter(col("rank") <= 10)

print("\n=== En Başarılı 10 Öğrenci ===")
top10.select("school", "sex", "total_score", "rank").show()


# 7) Yaşa göre ortalama not ve sosyal skor

print("\n=== Yaşa Göre Ortalama Notlar ===")
df.groupBy("age").agg(
    avg("G3").alias("avg_final"),
    avg("social_score").alias("avg_social"),
    avg("risk_score").alias("avg_risk")
).orderBy("age").show()

# 8) Çalışma süresine göre başarı analizi

print("\n=== Çalışma Süresi - Başarı Analizi ===")
df.groupBy("studytime").agg(
    avg("G1").alias("avg_G1"),
    avg("G2").alias("avg_G2"),
    avg("G3").alias("avg_G3"),
    avg("total_score").alias("avg_total")
).orderBy("studytime").show()


# 9) Korelasyon analizi (notlar / alkol / sosyal hayat)

cols = ["G1", "G2", "G3", "Dalc", "Walc", "goout", "freetime", "absences"]

print("\n=== Korelasyon Analizi ===")
for c in cols:
    corr_val = df.corr("G3", c)
    print(f"Correlation(G3, {c}): {corr_val}")

# 10) İnternet + çalışma süresi ilişkisi

print("\n=== İnternet Olup Olmaması & Başarı ===")
df.groupBy("internet").agg(
    avg("G3").alias("avg_grade"),
    avg("studytime").alias("avg_study"),
    avg("social_score").alias("avg_social")
).orderBy(desc("avg_grade")).show()

# 11) Daha Temiz Son Tablo
print("\n=== Özet Öğrenci Tablosu (Temiz) ===")

selected_cols = [
    "school", "sex", "age", "studytime",
    "goout", "Walc",
    "G1", "G2", "G3",
    "total_score",
    "social_score",
    "risk_score",
    "grade_level"
]

df.select(selected_cols).show(20, truncate=False)
spark.stop()



