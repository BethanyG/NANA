SELECT
		ndb_no, long_desc, similarity(long_desc, 'asparagus stalks') AS sim_score
FROM
		food_descriptions 
WHERE 
		long_desc % 'asparagus stalks' 
AND 
		similarity(long_desc, 'asparagus stalks') > 0.35;



SELECT
		ndb_no, measurement_desc, similarity(measurement_desc, '1/2 tablespoon') AS sim_score
FROM
		weights
WHERE

		similarity(measurement_desc, '1/2 tablespoon') > 0.7;



SELECT
		food_descriptions.ndb_no, food_descriptions.long_desc, weights.amount, weights.measurement_desc, weights.gram_weight, similarity(food_descriptions.long_desc, 'avocado') AS sim_score, similarity(weights.measurement_desc, 'a') AS sim_score_measure
FROM
		food_descriptions
JOIN
		weights ON food_descriptions.ndb_no = weights.ndb_no
WHERE
		food_descriptions.long_desc % 'avocados' 
		AND 
			similarity(food_descriptions.long_desc, 'avocado') > 0.35
		AND 
			similarity(weights.measurement_desc, 'a') > 0.035
		ORDER BY similarity(food_descriptions.long_desc, 'avocado') > 0.35 DESC;


SELECT
		food_descriptions.ndb_no, food_descriptions.long_desc, weights.amount, 
		weights.measurement_desc, weights.gram_weight, 
		similarity(food_descriptions.long_desc, 'avocado') AS sim_score, 
		similarity(weights.measurement_desc, 'cup') AS sim_score_measure
FROM
		food_descriptions
JOIN
		weights ON food_descriptions.ndb_no = weights.ndb_no
WHERE
		long_desc @@ to_tsquery('english', 'avocado')
		AND 
			similarity(weights.measurement_desc, '') > 0.035
		ORDER BY similarity(food_descriptions.long_desc, 'avocado') > 0.35 DESC;



SELECT
		food_descriptions.ndb_no, food_descriptions.long_desc, weights.amount, 
		weights.measurement_desc, weights.gram_weight, 
		similarity(food_descriptions.long_desc, 'celery stalks') AS sim_score, 
		similarity(weights.measurement_desc, 'stalk') AS sim_score_measure
FROM
		food_descriptions
JOIN
		weights ON food_descriptions.ndb_no = weights.ndb_no
WHERE
		long_desc @@ plainto_tsquery('english', 'celery')
	AND 
		similarity(weights.measurement_desc, 'stalk') > 0.035
	ORDER BY similarity(food_descriptions.long_desc, 'celery stalks') > 0.35 DESC;






