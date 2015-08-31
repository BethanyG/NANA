# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:46:38 2015

@author: bethanygarcia
"""

SELECT 
		weights.measurement_desc,
		round((weights.gram_weight * nutrient_data.nutrient_val / 100), 4) as Value_per_portion,
		nutrient_definitions.units,
		nutrient_definitions.nutrient_desc, nutrient_definitions.num_decimals,
		nutrient_data.num_data_pts
FROM 
		weights
JOIN
		nutrient_data
		ON weights.ndb_no = nutrient_data.ndb_no
JOIN 
		nutrient_definitions
		ON nutrient_data.nutrient_no = nutrient_definition.nutrient_no
JOIN
		user_nutrients
		ON nutrient_data.nutrient_no = user_nutrients.nutrient_no and user_nutrients.user_id = 0
WHERE
		nutrient_data.ndb_no = '02014' and weights.measurement_desc = 'tbsp, whole'
		ORDER BY nutrient_definition.nutrient_desc ASC;


