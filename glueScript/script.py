import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args  = getResolvedOptions(sys.argv, ['JOB_NAME',
                                      'output_path'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'],args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database = "input",
    table_name= "csv_customers",
    transformation_ctx = "datasource0"
)

applymapping1 = ApplyMapping.apply(
    frame = datasource0,
    mappings= [
        ("customerid","long","customerid","long"),
        ("namestyle","boolean","namestyle","boolean"),
        ("title","string","title","string"),
        ("firstname","string","firstname","string"),
        ("middlename","string","middlename","string"),
        ("lastname","string","lastname","string"),
        ("suffix","string","suffix","string"),
        ("companyname","string","companyname","string"),
        ("salesperson","string","salesperson","string"),
        ("emailaddress","string","emailaddress","string"),
        ("phone","string","phone","string"),
        ("passwordhash","string","passwordhash","string"),
        ("passwordsalt","string","passwordsalt","string"),
        ("rowguid","string","rowguid","string"),
        ("modifieddate","string","modifieddate","string"),
        ]
)

resolvechoice2 = ResolveChoice.apply(
    frame= applymapping1,
    choice= "make_struct",
    transformation_ctx="resolvechoice2"
)

dropnullfields3 = DropNullFields.apply(
    frame= resolvechoice2,
    transformation_ctx="dropnullfields3"
)

datasynk4 = glueContext.write_dynamic_frame.from_options(
    frame=dropnullfields3,
    connection_type= "s3",
    connection_options = {
        "path": args['output_path']
    },
    format = "parquet",
    transformation_ctx = "datasynk4"
)
job.commit()