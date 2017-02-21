
-- input has around ~ 2.2 TB

-- see all files: http://s3.amazonaws.com/datasets.elasticmapreduce/

CREATE EXTERNAL TABLE english_1grams (
 gram string,
 year int,
 occurrences bigint,
 pages bigint,
 books bigint
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS SEQUENCEFILE
location 's3://datasets.elasticmapreduce/ngrams/books/20090715/eng-all/1gram/'

CREATE TABLE normalized (
 gram string,
 year int,
 occurrences bigint
);

INSERT OVERWRITE TABLE normalized
SELECT
 lower(gram),
 year,
 occurrences
FROM
 english_1grams
WHERE
 year >= 1890 AND
 gram REGEXP "^[A-Za-z+'-]+$";
 
-- calculate word ratios by decades

CREATE TABLE by_decade (
 gram string,
 decade int,
 ratio double
);

INSERT OVERWRITE TABLE by_decade
SELECT
 a.gram,
 b.decade,
 sum(a.occurrences) / b.total
FROM
 normalized a
JOIN ( 
 SELECT 
  substr(year, 0, 3) as decade, 
  sum(occurrences) as total
 FROM 
  normalized
 GROUP BY 
  substr(year, 0, 3)
) b
ON
 substr(a.year, 0, 3) = b.decade
GROUP BY
 a.gram,
 b.decade,
 b.total;
 
-- calculate changes by decade

SELECT
 a.gram as gram,
 a.decade as decade,
 a.ratio as ratio,
 a.ratio / b.ratio as increase
FROM 
 by_decade a 
JOIN 
 by_decade b
ON
 a.gram = b.gram and
 a.decade - 1 = b.decade
WHERE
 a.ratio > 0.001 and
 a.decade >= 190
DISTRIBUTE BY
 decade
SORT BY
 decade ASC,
 increase DESC
LIMIT 200;
 
-- based on Amazon tutorial: http://aws.amazon.com/articles/Elastic-MapReduce/5249664154115844


