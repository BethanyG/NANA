Create Table food_descriptions
(
NDB_No VARCHAR(5) PRIMARY KEY,
FdGrp_Cd VARCHAR(4) NOT NULL,
Long_Desc VARCHAR(200) NOT NULL,
Short_Desc VARCHAR(60) NOT NULL,
Comm_Name VARCHAR(100),
Manufact_Name VARCHAR(65),
Survey CHAR(1),
Refuse_Desc VARCHAR(135),
Refuse INTEGER,
Sci_Name VARCHAR(65),
N_Factor NUMERIC,
Pro_Factor NUMERIC,
Fat_Factor NUMERIC,
CHO_Factor NUMERIC
);

CREATE TABLE food_group_descriptions
(
FdGrp_Cd VARCHAR(4) PRIMARY KEY,
FdGrp_Desc VARCHAR(60) NOT NULL
);

CREATE TABLE langual_factors
(
Langual_ID SERIAL PRIMARY KEY,
NDB_No VARCHAR(5),
Factor_Code VARCHAR(5)
);

CREATE TABLE langual_factor_descriptions
(
Factor_Code VARCHAR(5) PRIMARY KEY,
Description VARCHAR(140) NOT NULL
);

CREATE TABLE nutrient_data
(
Food_Nutrient SERIAL PRIMARY KEY, 	
NDB_No VARCHAR(5),
Nutrient_No VARCHAR(3),
Nutrient_Val NUMERIC NOT NULL,
Num_Data_Pts NUMERIC NOT NULL,
Std_Error NUMERIC,
Source_Code VARCHAR(2) NOT NULL,
Derivation_Code VARCHAR(4),
Ref_NDB_No VARCHAR(5),
Add_Nutr_Mark CHAR(1),
Num_Studies NUMERIC,
Min_Value NUMERIC,
Max_Value NUMERIC,
Deg_of_Freedom NUMERIC,
Lower_EB NUMERIC,
Upper_EB NUMERIC,
Stats_Comment VARCHAR(10),
Add_Mod_Date VARCHAR(10),
Confid_Code CHAR(1)
);

CREATE TABLE nutrient_definitions
(
Nutrient_No VARCHAR(3) PRIMARY KEY,
Units VARCHAR(7) NOT NULL,
Tag_name VARCHAR(20),
Nutrient_Desc VARCHAR(60) NOT NULL,
Num_Decimals CHAR(1) NOT NULL,
SR_Order NUMERIC NOT NULL
);

CREATE TABLE source_codes
(
Source_Code VARCHAR(2) PRIMARY KEY,
Source_Code_Desc VARCHAR(60) NOT NULL
);

CREATE TABLE data_derivation_codes
(
Derivation_Code VARCHAR(4) PRIMARY KEY,
Derivation_Description VARCHAR(120) NOT NULL
);

CREATE TABLE weights
(
Weight_ID SERIAL PRIMARY KEY,
NDB_No VARCHAR(5),
Sequence_No VARCHAR(2),
Amount NUMERIC NOT NULL,
Measurement_Desc VARCHAR(84) NOT NULL,
Gram_Weight NUMERIC NOT NULL,
Num_Data_Pts NUMERIC,
Std_Deviation NUMERIC
);

CREATE TABLE footnotes
(
NDB_No VARCHAR(5) PRIMARY KEY,
Footnote_No VARCHAR(4) NOT NULL,
Footnote_Type CHAR(1) NOT NULL,
Nutrient_No VARCHAR(3),
Footnote_Txt VARCHAR(200) NOT NULL
);

CREATE TABLE sources_of_data_link
(
Link_ID SERIAL PRIMARY KEY,
NDB_No VARCHAR(5),
Nutrient_No VARCHAR(3),
Data_Source_ID VARCHAR(6)
);

CREATE TABLE sources_of_data
(
Data_Source_ID VARCHAR(6) PRIMARY KEY,
Authors VARCHAR(255),
Title VARCHAR(255) NOT NULL,
Year VARCHAR(4),
Journal VARCHAR(135),
Volume_City VARCHAR(16),
Issue_State VARCHAR(5),
Start_Page VARCHAR(5),
End_Page VARCHAR(5)
);