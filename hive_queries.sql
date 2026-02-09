-- Student Performance Dataset (student-mat.csv)
CREATE DATABASE IF NOT EXISTS student_db;
use student_db;
-- HDFS'ten dış tablo oluşturma
CREATE EXTERNAL TABLE IF NOT EXISTS student_mat (
    school STRING,
    sex STRING,
    age INT,
    address STRING,
    famsize STRING,
    Pstatus STRING,
    Medu INT,
    Fedu INT,
    Mjob STRING,
    Fjob STRING,
    reason STRING,
    guardian STRING,
    traveltime INT,
    studytime INT,
    failures INT,
    schoolsup STRING,
    famsup STRING,
    paid STRING,
    activities STRING,
    nursery STRING,
    higher STRING,
    internet STRING,
    romantic STRING,
    famrel INT,
    freetime INT,
    goout INT,
    Dalc INT,
    Walc INT,
    health INT,
    absences INT,
    G1 INT,
    G2 INT,
    G3 INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'hdfs://localhost:9000/user/asude/student/';

DESCRIBE student_mat;
-- Yaş 18 üzeri öğrenciler
SELECT school, sex, age, G3
FROM student_mat
WHERE age > 18
LIMIT 10;
-- Destek alan ve almayan öğrencilerin not ortalaması
SELECT schoolsup, AVG(G3) AS avg_final_grade
FROM student_mat
GROUP BY schoolsup;

-- Not ortalaması yüksek olan öğrenciler
SELECT school, sex, (G1 + G2 + G3)/3 AS avg_score
FROM student_mat
ORDER BY avg_score DESC
LIMIT 10;

-- Cinsiyete göre final ortalamaları
SELECT sex, AVG(G3) AS avg_final_grade
FROM student_mat
GROUP BY sex;

  -- En çok devamsızlık yapan öğrenciler
SELECT school, sex, absences
FROM student_mat
ORDER BY absences DESC
LIMIT 10;   

--Devamsızlığı 10 dan fazla olan öğrenci sayısı                                                           
SELECT COUNT(*) AS num_studes
FROM student_mat
WHERE absences > 10; 
-- Geçen ve kalan öğrenci sayısı 
SELECT
    SUM(CASE WHEN G3 >= 10 THEN 1 ELSE 0 END) AS passed,
    SUM(CASE WHEN G3 < 10 THEN 1 ELSE 0 END) AS failed
FROM student_mat;
