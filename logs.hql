CREATE EXTERNAL TABLE logs (
    remoteAddr STRING,
    remoteLogname STRING,
    user STRING,
    time STRING,
    request STRING,
    status STRING,
    bytes_string STRING,
    referrer STRING,
    browser STRTING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.contrib.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
 "input.regex" =
    '^(\\S+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})\\] "(.+?)" (\\S+) (\\S+) "([^"]*)" "([^"]*)"',
"output.format.string"="%1$s %2$s %3$s %4$s %5$s %6$s %7$s %8$s"
)
STORED AS TEXTFILE LOCATION '/user/training/pig-apache/input/access_log_0';
