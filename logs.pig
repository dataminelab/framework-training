register file:/usr/lib/pig/contrib/piggybank/java/piggybank.jar;
DEFINE EXTRACT org.apache.pig.piggybank.evaluation.string.EXTRACT;
LOGS = FOREACH RAW_LOGS GENERATE 
    FLATTEN( 
      EXTRACT(line, '^(\\S+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})\\] "(.+?)" (\\S+) (\\S+) "([^"]*)" "([^"]*)"')
    ) 
    as (
      remoteAddr:    chararray, 
      remoteLogname: chararray, 
      user:          chararray, 
      time:          chararray, 
      request:       chararray, 
      status:        int, 
      bytes_string:  chararray, 
      referrer:      chararray, 
      browser:       chararray
  );
DOMAINS = FOREACH LOGS GENERATE FLATTEN(EXTRACT(referrer, 'http[s]?://(^/+)[/]?.*')) as terms:chararray;

