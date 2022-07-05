SELECT * FROM test;


ALTER TABLE test
ADD COLUMN createdAt timestamp,
ADD COLUMN updatedAt timestamp;

UPDATE test
SET createdAt = NOW(), updatedAt = NOW()



DROP TABLE test;

CREATE TABLE test (
	id serial PRIMARY KEY
	, num integer
	, data varchar
	, createdAt timestamp
	, updatedAt timestamp
);
INSERT INTO test (num, data, createdAt, updatedAt)
VALUES
(2, 'apple', NOW(), NOW()),
(3, 'orange', NOW(), NOW()),
(4, 'lemon', NOW(), NOW()),
(5, 'strawberry', NOW(), NOW()),
(6, 'banana', NOW(), NOW());

SELECT * FROM test;