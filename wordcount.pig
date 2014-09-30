lines = LOAD '/user/root/words.txt' USING TextLoader() AS (sentence:chararray);
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(sentence)) AS word;
groupOfWords = GROUP words BY word;
counts = FOREACH groupOfWords GENERATE group, COUNT(words);
STORE counts INTO '/user/root/output/wordcounts' USING PigStorage();
CAT /user/root/output/wordcounts;

# see: http://pig.apache.org/docs/r0.7.0/piglatin_ref2.html
