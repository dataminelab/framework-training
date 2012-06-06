lines = LOAD '/user/training/words.txt' USING TextLoader() AS (sentence:chararray);
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(sentence)) AS word;
groupOfWords = GROUP words BY word;
counts = FOREACH groupOfWords GENERATE group, COUNT(words);
STORE counts INTO '/user/training/output/wordcounts' USING PigStorage();
CAT /user/training/output/wordcounts;
