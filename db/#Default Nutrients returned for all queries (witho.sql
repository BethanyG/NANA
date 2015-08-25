#Default Nutrients returned for all queries (without user prefrences)


 nutrient_no |           nutrient_desc            
-------------+------------------------------------
 208         | Energy
 203         | Protein
 204         | Total lipid (fat)

 205         | Carbohydrate, by difference
 291         | Fiber, total dietary
 269         | Sugars, total
 
 301         | Calcium, Ca
 303         | Iron, Fe
 304         | Magnesium, Mg 
 307         | Sodium, Na
 306         | Potassium, K
 305         | Phosphorus, P
 309         | Zinc, Zn
 
 318         | Vitamin A, IU
 404         | Thiamin
 405         | Riboflavin
 406         | Niacin
 410         | Pantothenic acid
 415         | Vitamin B-6
 418         | Vitamin B-12
 324         | Vitamin D
 323         | Vitamin E (alpha-tocopherol) 
 435         | Folate, DFE 
 430         | Vitamin K (phylloquinone)



INSERT INTO 
	user_nutrients (user_id, nutrient_no, nutrient_desc)
	(SELECT 0, nutrient_no, nutrient_desc 
	 FROM nutrient_definitions
	 WHERE nutrient_no
	 IN
		('208','203','204','205','291','269','301','303','304',
		 '307','306','305','309','318','404','405','406','410',
		 '415','418','324','323','435','430'));



