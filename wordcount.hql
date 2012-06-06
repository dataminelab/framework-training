CREATE TABLE lines(text string);
LOAD DATA LOCAL INPATH '/user/training/words.txt' OVERWRITE INTO TABLE lines;
CREATE TABLE words(word string);
INSERT OVERWRITE TABLE words SELECT EXPLODE(split(text, '[ \t]+')) word from lines;
SELECT word, count(*) FROM words GROUP BY word;