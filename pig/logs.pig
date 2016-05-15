
RAW_LOGS = LOAD 's3://elasticmapreduce/samples/pig-apache/input/' USING TextLoader as (line:chararray);
LOGS = FOREACH RAW_LOGS GENERATE 
    FLATTEN( 
      REGEX_EXTRACT_ALL(line, '^(\\S+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})\\] "(.+?)" (\\S+) (\\S+) "([^"]*)" "([^"]*)"')
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
REFERRER_ONLY = FOREACH LOGS GENERATE referrer;

TEMP = LIMIT REFERRER_ONLY 15;
DUMP TEMP;

FILTERED = FILTER REFERRER_ONLY BY referrer matches '.*bing.*' OR referrer matches '.*google.*';
TEMP = LIMIT FILTERED 10;
DUMP TEMP;

SEARCH_TERMS = FOREACH FILTERED GENERATE FLATTEN(REGEX_EXTRACT(referrer, '.*[&\\?]q=([^&]+).*', 1)) as terms:chararray;
SEARCH_TERMS_FILTERED = FILTER SEARCH_TERMS BY NOT $0 IS NULL;
DUMP SEARCH_TERMS_FILTERED;

SEARCH_TERMS_COUNT = FOREACH (GROUP SEARCH_TERMS_FILTERED BY $0) GENERATE $0, COUNT($1) as num;
SEARCH_TERMS_COUNT_SORTED = ORDER SEARCH_TERMS_COUNT BY num DESC;
DUMP SEARCH_TERMS_COUNT_SORTED;

STORE SEARCH_TERMS_COUNT_SORTED into '/user/root/output/run0';
CAT /user/root/output/run0;
