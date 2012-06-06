CREATE TABLE text_lines(text string);
LOAD DATA LOCAL INPATH '/home/cloudera/framework-training/words.txt' OVERWRITE INTO TABLE text_lines;
CREATE TABLE words(word string);
INSERT OVERWRITE TABLE words SELECT EXPLODE(split(text, '[ \t]+')) word from text_lines;
SELECT word, count(*) FROM words GROUP BY word;