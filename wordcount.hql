create table textlines(text string);
load data local inpath 'C:\work\ClearPoint\Data20\data\words.txt' overwrite into table textlines;
create table words(word string);
insert overwrite table words select explode(split(text, '[ \t]+')) word from textlines;
select word, count(*) from words group by word;