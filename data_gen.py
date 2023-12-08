# Databricks notebook source


# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC paralelo

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType, DateType
import random
from datetime import date, datetime
import string

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DateType, TimestampType
from datetime import date, datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import *
import random

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DateType, TimestampType
from datetime import date, datetime

def gera_df_exemplo():
    spark = SparkSession.builder.appName("ExemploDataFrame").getOrCreate()

    schema = StructType([
        StructField("Nome", StringType(), True),
        StructField("cpf_cnpj_corpo", IntegerType(), True),
        StructField("cpf_cnpj_filial", IntegerType(), True),
        StructField("cpf_cnpj_dv", IntegerType(), True),
        StructField("Idade", IntegerType(), True),
        StructField("Salario", FloatType(), True),
        StructField("Cidade", StringType(), True),
        StructField("DataNascimento", DateType(), True),
        StructField("dtultatuz", TimestampType(), True)
    ])

    dados = [
        ("João Silva", 12345678, 1234, 12, 30, 5000.0, "São Paulo", date(1991, 1, 1), datetime(2021, 1, 1, 15, 30, 45, 123000)),
        ("Maria Oliveira", 87654321, 4321, 34, 25, 4500.0, "Rio de Janeiro", date(1996, 2, 15), datetime(2021, 2, 15, 10, 20, 35, 567000)),
        ("Carlos Souza", 23456789, 5678, 56, 40, 5500.0, "Belo Horizonte", date(1981, 8, 23), datetime(2021, 8, 23, 12, 5, 50, 890000)),
        ("Ana Santos", 98765432, 8765, 78, 22, 3000.0, "Brasília", date(1999, 7, 30), datetime(2021, 7, 30, 17, 45, 55, 230000)),
        ("Pedro Rocha", 34567890, 2345, 90, 35, 4000.0, "Curitiba", date(1986, 5, 19), datetime(2021, 5, 19, 8, 33, 10, 456000))
    ]

    return spark.createDataFrame(dados, schema)

def duplicate(df, n=10):
    """
    duplica n registros pra testar o df. 
    """
    first_two_rows = df.limit(n).collect()
    return df.unionAll(df.sparkSession.createDataFrame(first_two_rows, df.schema))

df = gera_df_exemplo()
df = duplicate(df, 10)

df.show(100, False)

base_dataframe = df

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import rand, expr, col, lit
from pyspark.sql.types import IntegerType, StringType, FloatType, DoubleType, DateType, TimestampType
import random
from datetime import datetime, timedelta

# Inicializar a sessão Spark
spark = SparkSession.builder.appName("gerador_dados_sinteticos").getOrCreate()

def gera_dados_sinteticos(df, n=1000, regras_especificas=None):
    # Criar um DataFrame com o mesmo esquema, mas com linhas vazias
    df_vazio = spark.createDataFrame([], df.schema)

    # Adicionar n linhas com valores padrão
    valores_padrao = [lit(None).cast(campo.dataType) for campo in df.schema.fields]
    df_dados_sinteticos = df_vazio.union(spark.range(n).select(*valores_padrao))

    # Aplicar regras específicas, se houver
    for nome_coluna, regra in regras_especificas.items():
        df_dados_sinteticos = df_dados_sinteticos.withColumn(nome_coluna, regra(df_dados_sinteticos))

    # Preencher outras colunas com valores aleatórios
    for campo in df.schema.fields:
        nome_coluna = campo.name
        if nome_coluna not in regras_especificas:
            tipo_dado = campo.dataType
            if isinstance(tipo_dado, StringType):
                df_dados_sinteticos = df_dados_sinteticos.withColumn(nome_coluna, expr("uuid()"))
            elif isinstance(tipo_dado, IntegerType):
                df_dados_sinteticos = df_dados_sinteticos.withColumn(nome_coluna, (rand() * 1000).cast(IntegerType()))
            elif isinstance(tipo_dado, FloatType) or isinstance(tipo_dado, DoubleType):
                df_dados_sinteticos = df_dados_sinteticos.withColumn(nome_coluna, (rand() * 10000))
            elif isinstance(tipo_dado, DateType):
                df_dados_sinteticos = df_dados_sinteticos.withColumn(nome_coluna, expr("add_months(current_date(), - cast(rand() * 1200 as int))"))
            elif isinstance(tipo_dado, TimestampType):
                df_dados_sinteticos = df_dados_sinteticos.withColumn(nome_coluna, expr("current_timestamp() - INTERVAL 1 DAY * cast(rand() * 365 * 100 as int)"))

    return df_dados_sinteticos

# Definição das regras específicas
regras = {
    'cpf_cnpj_filial': lambda df: (rand() * 9999).cast(IntegerType()),
    'cpf_cnpj_corpo': lambda df: expr("case when cpf_cnpj_filial = 0 then cast(rand() * 999999999 as int) else cast(rand() * 99999999 as int) end"),
    'cpf_cnpj_dv': lambda df: (rand() * 99).cast(IntegerType()),
    'Idade': lambda df: (rand() * 80).cast(IntegerType()),
    # Adicione outras regras aqui, se necessário
}

# Supondo que df é o seu DataFrame original
# df = ...

df_dados_sinteticos = gera_dados_sinteticos(df, n=1000, regras_especificas=regras)
df_dados_sinteticos.show()


# COMMAND ----------


