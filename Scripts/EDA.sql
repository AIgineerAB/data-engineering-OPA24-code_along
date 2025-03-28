-- describe the table
desc;

-- select all to view the data
SELECT * FROM hemnet;

-- find out nr of rows
SELECT COUNT(*) AS total_rows
FROM hemnet;

-- find out 5 most expensive houses
SELECT * FROM hemnet
ORDER BY final_price DESC
LIMIT 5;

-- find out 5 cheapest houses
SELECT * FROM hemnet
ORDER BY final_price ASC
LIMIT 5;

-- summary statistics for final price
SELECT 
	MIN(final_price) AS min_price,
	MAX(final_price) AS max_price,
	AVG(final_price) AS avg_price,
	MEDIAN(final_price) AS median_price
FROM hemnet;


-- summary statistics for price per area 
SELECT 
	MIN(price_per_area) AS min_price,
	MAX(price_per_area) AS max_price,
	AVG(price_per_area) AS avg_price,
	MEDIAN(price_per_area) AS median_price
FROM hemnet;

-- find unique value for commune column
SELECT COUNT(DISTINCT commune)
FROM hemnet;

-- find unique value for kommun/municipality 
SELECT COUNT(DISTINCT 
trim(split_part(commune, ',', 2))) AS nr_kommun
FROM hemnet;

-- percentage of houses sold over 10Mkr
	-- 1. calculate nr of total houses
    -- 2. calculate nr of expensive houses
    -- 3. using the calculated numbers to calculate a percentage
-- ref for CTE: https://www.geeksforgeeks.org/cte-in-sql/

WITH all_houses AS (SELECT COUNT(*) AS total_count FROM hemnet), 
	 expensive_houses AS (SELECT COUNT(*) AS expensive_count FROM hemnet WHERE final_price > 10000000)
SELECT (eh.expensive_count*100/ah.total_count) AS percentage_expensive_houses
FROM all_houses ah , expensive_houses eh; 


SELECT COUNT(*) AS expensive_count FROM hemnet WHERE final_price > 10000000;
SELECT COUNT(*) AS total_count FROM hemnet;

