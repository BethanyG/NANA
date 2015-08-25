# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:46:38 2015

@author: bethanygarcia
"""

SELECT 
		w.measurement_desc,
		round((w.gram_weight * ndat.nutrient_val / 100), 4) as Value_per_portion,
		ndef.units,
		ndef.nutrient_desc, ndef.num_decimals,
		ndat.num_data_pts
FROM 
		weights as w
JOIN
		nutrient_data as ndat
		ON w.ndb_no = ndat.ndb_no
JOIN 
		nutrient_definitions as ndef
		ON ndat.nutrient_no = ndef.nutrient_no
JOIN
		user_nutrients as unut
		ON ndat.nutrient_no = unut.nutrient_no and unut.user_id = 0
WHERE
		ndat.ndb_no = '02014' and w.measurement_desc = 'tbsp, whole';