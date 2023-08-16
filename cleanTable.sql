CREATE TABLE test (
    key_str text,
    article text,
    section text,
    content text
);

INSERT INTO test VALUES('CONS#0#0#0#0#XIX A#SECTION 1', 'XIX A', 'SECTION 1','Blah blah blah');
INSERT INTO test VALUES('CONS#0#0#0#0#XIX A#SECTION 1', 'XIX A', 'SECTION 2','Blah blah blah');
INSERT INTO test VALUES('CONS#0#0#0#0#2#1', '69', '2','Blah blah blah blah');

UPDATE
    test
SET
    section = REPLACE(section,'SECTION','')
WHERE
    section IS NOT NULL;

UPDATE [test] SET [section] = REPLACE([section], 'SECTION ', '');

SELECT CAST(total_tokens as SIGNED);

SELECT CAST(division as double);
SELECT CAST(title as double);
SELECT CAST(part as double);
SELECT CAST(chapter as double);


UPDATE test
SET 
    section = CAST(section as integer)
WHERE
    section IS NOT NULL;

