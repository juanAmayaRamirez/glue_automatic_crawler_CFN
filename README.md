# Glue Auto Crawler

![alt text](.files/Glue%20crawler%202023-03-10%2017.34.21.excalidraw.png)

1.  csv file ingestion into [[S3]].
2. Event triggers lambda.
3. [[lambda]] starts crawler.
4. [[Glue#AWS Glue Crawler]] finds new csv files
5. [[Glue#AWS Glue Crawler]] updates the glue datacatalog
6. [[glue]] reads from the data catalog updated table
7. [[glue]] converts writes data into [[s3]] as parquet
8. [[Glue#AWS Glue Crawler]] finds new parquet files
9. [[Glue#AWS Glue Crawler]] updates the glue data catalog


# References
* https://www.youtube.com/watch?v=AtG_QD1JAZk&list=PL8JO6Q_xfjemIypT6_2Q6fGmvpRsofGG-&index=2
* https://aws.amazon.com/es/blogs/big-data/run-aws-glue-crawlers-using-amazon-s3-event-notifications/
* https://github.com/aws-samples/aws-glue-crawler-utilities
* https://devnote.tech/2023/01/having-aws-glue-crawler-crawl-based-on-events-with-sqs/