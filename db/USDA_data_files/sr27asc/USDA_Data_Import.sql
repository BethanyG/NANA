--Food Descriptions
COPY food_descriptions
(
NDB_No,
FdGrp_Cd,
Long_Desc,
Short_Desc,
Comm_Name,
Manufact_Name,
Survey,
Refuse_Desc,
Refuse,
Sci_Name,
N_Factor,
Pro_Factor,
Fat_Factor,
CHO_Factor
)
FROM 'db/sr27asc/FOOD_DES.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

--Food Group Descriptions
COPY food_group_descriptions
(
FdGrp_Cd,
FdGrp_Desc
)
FROM 'db/sr27asc/FD_GROUP.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

--LanguaL Factors
COPY langual_factors
(
NDB_No,
Factor_Code
)
FROM 'db/sr27asc/LANGUAL.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

--LanguaL Factor Descriptions
COPY langual_factor_descriptions
(
Factor_Code,
Description
)
FROM 'db/sr27asc/LANGDESC.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

--Nutrient Data
COPY nutrient_data
(
NDB_No,
Nutrient_No,
Nutrient_Val,
Num_Data_Pts,
Std_Error,
Source_Code,
Derivation_Code,
Ref_NDB_No,
Add_Nutr_Mark,
Num_Studies,
Min_Value,
Max_Value,
Deg_of_Freedom,
Lower_EB,
Upper_EB,
Stats_Comment,
Add_Mod_Date,
Confid_Code
)
FROM 'db/sr27asc/NUT_DATA.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

--Nutrient Definitions
COPY nutrient_definitions
(
Nutrient_No,
Units,
Tag_name,
Nutrient_Desc,
Num_Decimals,
SR_Order
)
FROM 'db/sr27asc/NUTR_DEF.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

COPY source_codes
(
Source_Code,
Source_Code_Desc
)
FROM 'db/sr27asc/SRC_CD.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

COPY data_derivation_codes
(
Derivation_Code,
Derivation_Description
)
FROM 'db/sr27asc/DERIV_CD.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

COPY weights
(
NDB_No,
Sequence_No,
Amount,
Measurement_Desc,
Gram_Weight,
Num_Data_Pts,
Std_Deviation
)
FROM 'db/sr27asc/WEIGHT.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

COPY footnotes
(
NDB_No,
Footnote_No,
Footnote_Type,
Nutrient_No,
Footnote_Txt
)
FROM 'db/sr27asc/FOOTNOTE.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

COPY sources_of_data_link
(
NDB_No,
Nutrient_No,
Data_Source_ID
)
FROM 'db/sr27asc/DATSRCLN.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;

COPY sources_of_data
(
Data_Source_ID,
Authors,
Title,
Year,
Journal,
Volume_City,
Issue_State,
Start_Page,
End_Page
)
FROM 'db/sr27asc/DATA_SRC.txt'
WITH DELIMITER '^'
CSV QUOTE AS '~'
;