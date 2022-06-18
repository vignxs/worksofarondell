from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StringType, StructType, StructField

sc = SparkContext("local[4]", "SparkContextBuilder-Application")
spark = SparkSession.builder.appName("SparkSessionBuilder-Application").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("FileName", StringType(), True),
    StructField("age", StringType(), True),
    StructField("BronzeLoadDate", StringType(), True)
])

#creating empty RDD
process_rec = sc.emptyRDD()

#creating empty DF
df1 = spark.createDataFrame(process_rec, schema)
df1.show()

lst = []

print("#"*100)

# method which accepts a row (rdd single line) object 
def conToUpper(row):
    # print(type(row))
    x = row['FileName'].upper()*2
    # process_rec = sc.union(process_rec, row)
    # lst.append(row)
    # print(x)
    return row

# Method to create a df and return. To be used with ConToUpper method.
# Will be passing each line of this df to conToUpper method
def createTupleDF():
    BronzetupleData = [("Vivek", 20, "2022-05-18 13:44:16.841648"), ("Aakash", 28, "2022-05-17 13:44:16.841648"),
                       ("Sumit", 22, "2022-05-17 13:45:16.841648"), ("Vijay", 30, "2022-05-18 19:44:16.841648"),
                       ("Shivang", 4, "2022-04-19 13:44:16.841648"), ("Prakash", 30, "2022-05-18 13:44:16.841648"),
                       ("Vivek", 32, "2022-07-11 19:44:16.841648")]

    df = spark.createDataFrame(BronzetupleData).toDF("FileName", "age", "BronzeLoadDate")
    return df

#getting DF from createTupleDF method here.
data = createTupleDF()
data.show()

rdd2 = data.rdd.map(lambda x: conToUpper(x))

# print(rdd2.take(10))
print("no of partitions of df is  = ", data.rdd.getNumPartitions())
print("#"*100)

print(lst)
print(rdd2.take(8))
spark.createDataFrame(rdd2).show(truncate=False)