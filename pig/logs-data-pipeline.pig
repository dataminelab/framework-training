RAW_LOGS = LOAD 's3://testbucket-radek/apache-logs' USING TextLoader as (line:chararray);
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

FILTERED = FILTER REFERRER_ONLY BY referrer matches '.*bing.*' OR referrer matches '.*google.*';

SEARCH_TERMS = FOREACH FILTERED GENERATE FLATTEN(REGEX_EXTRACT(referrer, '.*[&\\?]q=([^&]+).*', 1)) as terms:chararray;
SEARCH_TERMS_FILTERED = FILTER SEARCH_TERMS BY NOT $0 IS NULL;

SEARCH_TERMS_COUNT = FOREACH (GROUP SEARCH_TERMS_FILTERED BY $0) GENERATE $0, COUNT($1) as num;
SEARCH_TERMS_COUNT_SORTED = ORDER SEARCH_TERMS_COUNT BY num DESC;

STORE SEARCH_TERMS_COUNT_SORTED into 's3://testbucket-radek/apache-logs-keywords/';
