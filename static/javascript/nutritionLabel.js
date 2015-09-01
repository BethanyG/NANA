/*
 ******************************************************************************************************************+
 * NUTRITIONIX.com                                                                                                 |
 *                                                                                                                 |
 * This plugin allows you to create a fully customizable nutrition label                                           |
 *                                                                                                                 |
 * @authors             majin22 (js) and genesis23rd (css and html)                                                |
 * @copyright           Copyright (c) 2012 Nutritionix.                                                            |
 * @license             This Nutritionix jQuery Nutrition Label is dual licensed under the MIT and GPL licenses.   |
 * @link                http://www.nutritionix.com                                                                 |
 * @github              http://github.com/nutritionix/nutrition-label                                              |
 * @current version     6.0.4                                                                                      |
 * @stable version      6.0.2                                                                                      |
 * @supported browser   Firefox, Chrome, IE8+                                                                      |
 *                                                                                                                 |
 ******************************************************************************************************************+
*/
;(function($){
	$.fn.nutritionLabel = function(option, settings){
		if (typeof option === 'object'){
			settings = option;
			init( settings, $(this) );
		}else if (typeof option === 'string' && option !== ''){
			//destroys the nutrition label's html code
			if (option === 'destroy')
				new NutritionLabel().destroy( $(this) );
			//allows the user to hide the nutrition value
			else if (option === 'hide')
				new NutritionLabel().hide( $(this) );
			//allows the user to show the nutrition value
			else if (option === 'show')
				new NutritionLabel().show( $(this) );
			else{
				var values = [];

				var elements = this.each(function(){
					var data = $(this).data('_nutritionLabel');
					if (data){
						if ($.fn.nutritionLabel.defaultSettings[option] !== undefined){
							if (settings !== undefined){
								//set the option and create the nutrition label
								data.settings[option] = settings;
								init( data.settings, $(this) );
							}else
								//return the value of a setting - can only be used after the label is created / initiated
								values.push(data.settings[option]);
						}
					}else if ($.fn.nutritionLabel.defaultSettings[option] !== undefined)
						//set the option and create the nutrition label
						//this is a special case so the single value setting will still work even if the label hasn't been initiated yet
						if (settings !== undefined){
							$.fn.nutritionLabel.defaultSettings[option] = settings;
							init( null, $(this) );
						}
				});

				//return the value of a setting
				if (values.length === 1)
					return values[0];

				//return the setting values or the elements
				return values.length > 0 ? values : elements;
			}
		}else if (typeof option === 'undefined' || option === '')
			//if no value / option is supplied, simply create the label using the default values
			init( settings, $(this) );
	};


	$.fn.nutritionLabel.defaultSettings = {
		//default fixedWidth of the nutrition label
		width : 490,

		//to allow custom width - usually needed for mobile sites
		allowCustomWidth : true,
		widthCustom : 'auto',

		//to allow the label to have no border
		allowNoBorder : true,

		//to enable rounding of the nutritional values based on the FDA rounding rules
		//http://goo.gl/RMD2O
		allowFDARounding : false,

		//when set to true, this will hide the values if they are not applicable
		hideNotAppicableValues : false,

		//the brand name of the item for this label (eg. just salad)
		brandName : 'Brand where this item belongs to',
		//to scroll the ingredients if the innerheight is > scrollHeightComparison
		scrollLongIngredients : false,
		scrollHeightComparison : 100,
		//the height in px of the ingredients div
		scrollHeightPixel : 95,
		//this is to set how many decimal places will be shown on the nutrition values (calories, fat, protein, vitamin a, iron, etc)
		decimalPlacesForNutrition : 3,
		//this is to set how many decimal places will be shown for the "% daily values*"
		decimalPlacesForDailyValues : 3,
		//this is to set how many decimal places will be shown for the serving unit quantity textbox
		decimalPlacesForQuantityTextbox : 1,

		//to scroll the item name if the jQuery.height() is > scrollLongItemNamePixel
		scrollLongItemName : true,
		scrollLongItemNamePixel : 36,

		//show the customizable link at the bottom
		showBottomLink : false,
		//url for the customizable link at the bottom
		urlBottomLink : 'http://www.nutritionix.com',
		//link name for the customizable link at the bottom
		nameBottomLink : 'Nutritionix',

		//this value can be changed and the value of the nutritions will be affected directly
		//the computation is "current nutrition value" * "serving unit quantity value" = "final nutrition value"
		//this can't be less than zero, all values less than zero is converted to zero
		//the textbox to change this value is visible / enabled by default
		//if the initial value of the serving size unit quantity is less than or equal to zero, it is converted to 1.0
		//when enabled, user can change this value by clicking the arrow or changing the value on the textbox and
			//pressing enter. the value on the label will be updated automatically
		//different scenarios and the result if this feature is enabled
			//NOTE 1: [ ] => means a textbox will be shown
			//NOTE 2: on all cases below showServingUnitQuantityTextbox == true AND showServingUnitQuantity == true
					//if showServingUnitQuantity == false, the values that should be on the 'serving size div' are empty or null
			//CASE 1a: valueServingSizeUnit != '' (AND NOT null) && valueServingUnitQuantity >= 0
				//RESULT: textServingSize [valueServingUnitQuantity] valueServingSizeUnit

			//NOTE 3: on all cases below showServingUnitQuantityTextbox == true AND showItemName == true
					//if showItemName == false, the values that should be on the 'item name div' are empty or null
			//CASE 1b: valueServingSizeUnit != '' (AND NOT null) && valueServingUnitQuantity <= 0
				//RESULT: [valueServingUnitQuantity default to 1.0] itemName
			//CASE 3a: valueServingSizeUnit == '' (OR null) && valueServingUnitQuantity > 0
				//RESULT: [valueServingUnitQuantity] itemName
			//CASE 3b: valueServingSizeUnit == '' (OR null) && valueServingUnitQuantity <= 0
				//RESULT: [valueServingUnitQuantity default to 1.0] itemName

			//NOTE 4: to see the different resulting labels, check the html/demo-texbox-case*.html files
		valueServingUnitQuantity : 1.0,
		valueServingSizeUnit : '',
		showServingUnitQuantityTextbox : true,
		//the name of the item for this label (eg. cheese burger or mayonnaise)
		itemName : 'Item / Ingredient Name',
		showServingUnitQuantity : true,
		//allow hiding of the textbox arrows
		hideTextboxArrows : false,

		//these 2 settings are used internally.
		//this is just added here instead of a global variable to prevent a bug when there are multiple instances of the plugin like on the demo pages
		originalServingUnitQuantity : 0,
		//this is used to fix the computation issue on the textbox
		nutritionValueMultiplier : 1,
		//this is used for the computation of the servings per container
		totalContainerQuantity : 1,

		//default calorie intake
		calorieIntake : 2000,

		//these are the recommended daily intake values
		dailyValueTotalFat : 65,
		dailyValueSatFat : 20,
		dailyValueCholesterol : 300,
		dailyValueSodium : 2400,
		dailyValueCarb : 300,
		dailyValueFiber : 25,
		dailyvaluePotassium : 3500,
		dailyvalueMagnesium : 400,
		dailyvaluePhosphorus : 1000,
		dailyvalueVitaminE : 34,
		dailyvalueVitaminD : 400,
		dailyvalueThiamin : 1.5,
		dailyvalueRiboflavin : 1.7,
		dailyvalueNiacin : 20,
		dailyvaluePantothenicAcid : 10,
		dailyvalueVitaminB6 : 2,
		dailyvalueVitaminB12 : 6,
		dailyvalueVitaminK : 80,
		dailyvalueFolate : 400,
		dailyvalueZinc : 15,

		//these values can be change to hide some nutrition values
		showCalories : true,
		showFatCalories : false,
		showTotalFat : true,
		showSatFat : false,
		showTransFat : false,
		showPolyFat : false,
		showMonoFat : false,
		showCholesterol : false,
		showSodium : true,
		showMagnesium : true,
		showPotassium : true,
		showPhosphorus : true,
		showTotalCarb : true,
		showFibers : true,
		showSugars : true,
		showProteins : true,
		showVitaminA : true,
		showVitaminC : true,
		showVitaminE : true,
		showVitaminD : true,
		showThiamin : true,
		showRiboflavin : true,
		showNiacin : true,
		showPantothenicAcid : true,
		showVitaminB6 : true,
		showVitaminB12 : true,
		showVitaminK : true,
		showFolate : true,
		showCalcium : true,
		showIron : true,
		showZinc : true,

		//to show the 'amount per serving' text
		showAmountPerServing : true,
		//to show the 'servings per container' data and replace the default 'Serving Size' value (without unit and servings per container text and value)
		showServingsPerContainer : false,
		//to show the item name. there are special cases where the item name is replaced with 'servings per container' value
		showItemName : true,
		//show the brand where this item belongs to
		showBrandName : false,
		//to show the ingredients value or not
		showIngredients : true,
		//to show the calorie diet info at the bottom of the label
		showCalorieDiet : false,
		//to show the customizable footer which can contain html and js codes
		showCustomFooter : false,

		//to show the disclaimer text or not
		showDisclaimer : false,
		//the height in px of the disclaimer div
		scrollDisclaimerHeightComparison : 100,
		scrollDisclaimer : 95,
		valueDisclaimer : 'Please note that these nutrition values are estimated based on our standard serving portions.  As food servings may have a slight variance each time you visit, please expect these values to be with in 10% +/- of your actual meal.  If you have any questions about our nutrition calculator, please contact Nutritionix.',		ingredientLabel : 'INGREDIENTS:',
		valueCustomFooter : '',

		//the are to set some values as 'not applicable'. this means that the nutrition label will appear but the value will be a 'gray dash'
		naCalories : false,
		naFatCalories : false,
		naTotalFat : false,
		naSatFat : false,
		naTransFat : false,
		naPolyFat : false,
		naMonoFat : false,
		naCholesterol : false,
		naSodium : false,
		naPotassium : false,
		naMagnesium : false,
		naPhosphorus : false,
		naTotalCarb : false,
		naFibers : false,
		naSugars : false,
		naProteins : false,
		naVitaminA : false,
		naVitaminD : false,
		naVitaminC : false,
		naVitaminE : false,
		naThiamin : false,
		naRiboflavin : false,
		naNiacin : false,
		naPantothenicAcid : false,
		naVitaminB6 : false,
		naVitaminB12 : false,
		naVitaminK : false,
		naFolate : false,
		naCalcium : false,
		naIron : false,
		naZinc : false,

		//these are the default values for the nutrition info
		valueServingWeightGrams : 0,
		valueServingPerContainer : 1,
		valueCalories : 0,
		valueFatCalories : 0,
		valueTotalFat : 0,
		valueSatFat : 0,
		valueTransFat : 0,
		valuePolyFat : 0,
		valueMonoFat : 0,
		valueCholesterol : 0,
		valueSodium : 0,
		valuePotassium : 0,
		valueMagnesium : 0,
		valuePhosphorus : 0,
		valueTotalCarb : 0,
		valueFibers : 0,
		valueSugars : 0,
		valueProteins : 0,
		valueVitaminA : 0,
		valueVitaminC : 0,
		valueVitaminE : 0,
		valueVitaminD : 0,
		valueThiamin : 0,
		valueRiboflavin : 0,
		valueNiacin : 0,
		valuePantothenicAcid : 0,
		valueVitaminB6 : 0,
		valueVitaminB12 : 0,
		valueVitaminK : 0,
		valueFolate : 0,
		vlaueCalcium : 0,
		valueIron : 0,
		valueZinc : 0,

		//customizable units for the values
		unitCalories : '',
		unitFatCalories : '',
		unitTotalFat : 'g',
		unitSatFat : 'g',
		unitTransFat : 'g',
		unitPolyFat : 'g',
		unitMonoFat : 'g',
		unitCholesterol : 'mg',
		unitSodium : 'mg',
		unitPotassium : 'mg',
		unitPhosphorus : 'mg',
		unitTotalCarb : 'g',
		unitFibers : 'g',
		unitSugars : 'g',
		unitProteins : 'g',
		unitVitaminA : 'IU',
		unitVitaminC : 'mg',
		unitCalcium : 'mg',
		unitMagnesium : 'mg',
		unitVitaminE : 'mg',
		unitVitaminD : 'IU',
		unitThiamin : 'mg',
		unitRiboflavin : 'mg',
		unitNiacin : 'mg',
		unitPantothenicAcid : 'mg',
		unitVitaminB6 : 'mg',
		unitVitaminB12 : 'mcg',
		unitVitaminK : 'mcg',
		unitFolate : 'mcg',
		unitIron : 'mg',
		unitZinc : 'mg',

		//these are the values for the optional calorie diet
		valueCol1CalorieDiet : 2000,
		valueCol2CalorieDiet : 2500,
		valueCol1DietaryTotalFat : 0,
		valueCol2DietaryTotalFat : 0,
		valueCol1DietarySatFat : 0,
		valueCol2DietarySatFat : 0,
		valueCol1DietaryCholesterol : 0,
		valueCol2DietaryCholesterol : 0,
		valueCol1DietarySodium : 0,
		valueCol2DietarySodium : 0,
		valueCol1DietaryTotalCarb : 0,
		valueCol2DietaryTotalCarb : 0,
		valueCol1Dietary : 0,
		valueCol2Dietary : 0,

		//these text settings is so you can create nutrition labels in different languages or to simply change them to your need
		textNutritionFacts : 'Nutrition Facts',
		textDailyValues : 'Daily Value',
		textServingSize : 'Serving Size:',
		textServingsPerContainer : 'Servings Per Container',
		textAmountPerServing : 'Amount Per Serving',
		textCalories : 'Calories',
		textFatCalories : 'Calories from Fat',
		textTotalFat : 'Total Fat',
		textSatFat : 'Saturated Fat',
		textTransFat : '<i>Trans</i> Fat',
		textPolyFat : 'Polyunsaturated Fat',
		textMonoFat : 'Monounsaturated Fat',
		textCholesterol : 'Cholesterol',
		textSodium : 'Sodium',
		textPotassium : 'Potassium',
		textPhosphorus : 'Phosphorus',
		textTotalCarb : 'Total Carbohydrates',
		textFibers : 'Dietary Fiber',
		textSugars : 'Sugars',
		textProteins : 'Protein',
		textVitaminA : 'Vitamin A',
		textVitaminC : 'Vitamin C',
		textCalcium : 'Calcium',
		textMagnesium : 'Magnesium',
		textVitaminE : 'Vitamin E',
		textVitaminD : 'Vitamin D',
		textThiamin : 'Thiamin',
		textRiboflavin : 'Riboflavin',
		textNiacin : 'Niacin',
		textPantothenicAcid : 'Pantothenic Acid',
		textVitaminB6 : 'Vitamin B-6',
		textVitaminB12 : 'Vitamin B-12',
		textVitaminK : 'Vitamin K',
		textFolate : 'Folate',
		textIron : 'Iron',
		textZinc : 'Zinc',
		ingredientList : 'None',
		textPercentDailyPart1 : 'Percent Daily Values are based on a',
		textPercentDailyPart2 : 'calorie diet'
	};


	//this will store the unique individual properties for each instance of the plugin
	function NutritionLabel(settings, $elem){
		this.nutritionLabel = null;
		this.settings = settings;
		this.$elem = $elem;

		return this;
	}


	function cleanSettings(settings){
		var numericIndex = [
			'width','scrollHeightComparison','scrollHeightPixel','decimalPlacesForNutrition','decimalPlacesForDailyValues',
			'calorieIntake','dailyValueTotalFat','dailyValueSatFat','dailyValueCholesterol','dailyValueSodium','dailyValueCarb',
			'dailyValueFiber','valueServingSize','valueServingWeightGrams','valueServingPerContainer','valueCalories',
			'valueFatCalories','valueTotalFat','valueSatFat','valueTransFat','valuePolyFat','valueMonoFat','valueCholesterol',
			'valueSodium','valuePotassium', 'valuePhosphorus', 'valuePotassium','valueMagnesium','valuePhosphorus','valueVitaminE',
			'valueThiamin','valueRiboflavin','valueNiacin','valuePantothenicAcid','valueVitaminB6','valueVitaminB12','valueVitaminK',
			'valueVitaminD','valueFolate','valueTotalCarb','valueFibers','valueSugars','valueProteins','valueVitaminA','valueVitaminC',
			'valueCalcium','valueIron', 'valueZinc', 'valueCol1CalorieDiet','valueCol2CalorieDiet','valueCol1DietaryTotalFat',
			'valueCol2DietaryTotalFat','valueCol1DietarySatFat','valueCol2DietarySatFat','valueCol1DietaryCholesterol',
			'valueCol2DietaryCholesterol','valueCol1DietarySodium','valueCol2DietarySodium','valueCol1DietaryTotalCarb',
			'valueCol2DietaryTotalCarb','valueCol1Dietary','valueCol2Dietary', 'valueServingUnitQuantity',
			'scrollLongItemNamePixel, decimalPlacesForQuantityTextbox'
		];

		$.each(settings, function(index, value){
			if (jQuery.inArray(index, numericIndex) !== -1){
				settings[index] = parseFloat(settings[index]);
				if (isNaN(settings[index]) || settings[index] === undefined)
					settings[index] = 0;
			}
		});

		if (settings['valueServingUnitQuantity'] < 0)
			settings['valueServingUnitQuantity'] = 0;

		return settings;
	}


	function UpdateNutritionValueWithMultiplier(settings){
		var nutritionIndex = [
			'valueCalories','valueFatCalories','valueTotalFat','valueSatFat','valueTransFat','valuePolyFat','valueMonoFat',
			'valueCholesterol','valueSodium','valueTotalCarb','valueFibers','valueSugars','valueProteins','valueVitaminA',
			'valueVitaminC','valueCalcium','valueIron'
		];

		$.each(settings, function(index, value){
			if (jQuery.inArray(index, nutritionIndex) !== -1){
				settings[index] = parseFloat(settings[index]);
				if (isNaN(settings[index]) || settings[index] === undefined)
					settings[index] = 0;
				settings[index] = parseFloat(settings[index]) * parseFloat(settings['valueServingUnitQuantity']) * parseFloat(settings['nutritionValueMultiplier']);
			}
		});

		if (parseFloat(settings['valueServingUnitQuantity']) == 0)
			settings['valueServingPerContainer'] = 0;
		else if (!isNaN(settings['valueServingPerContainer']) && settings['valueServingPerContainer'] != undefined)
			settings['valueServingPerContainer'] = parseFloat(settings.totalContainerQuantity) / parseFloat(settings['valueServingUnitQuantity']);

		return settings;
	}


	function init(settings, $elem){
		//merge the default settins with the user supplied settings
		var $settings = $.extend( {}, $.fn.nutritionLabel.defaultSettings, settings || {} );
		$settings.totalContainerQuantity = parseFloat($settings.valueServingPerContainer) * parseFloat($settings['valueServingUnitQuantity']);

		var $originalCleanSettings = cleanSettings($.extend( {}, $.fn.nutritionLabel.defaultSettings, settings || {} ));
		$originalCleanSettings.totalContainerQuantity = parseFloat($originalCleanSettings.valueServingPerContainer) * parseFloat($originalCleanSettings['valueServingUnitQuantity']);

		//clean the settings and make sure that all numeric settings are really numeric, if not, force them to be
		$settings = cleanSettings($settings);
		$originalCleanSettings = cleanSettings($originalCleanSettings);

		$settings.nutritionValueMultiplier = $settings.valueServingUnitQuantity <= 0 ? 1 : 1 / $settings.valueServingUnitQuantity;

		//update the nutrition values with the multiplier
		var $updatedsettings = UpdateNutritionValueWithMultiplier($settings);
		$settings.originalServingUnitQuantity = $updatedsettings.valueServingUnitQuantity;

		//if the original value is <= 0, set it to 1.0
		if ($updatedsettings.valueServingUnitQuantity <= 0){
			$originalCleanSettings.valueServingUnitQuantity = 1;
			$updatedsettings = UpdateNutritionValueWithMultiplier($originalCleanSettings);
			$updatedsettings.valueServingUnitQuantity = 1;
		}


		//initalize the nutrition label and create / recreate it
		var nutritionLabel = new NutritionLabel($updatedsettings, $elem);
		$elem.html( nutritionLabel.generate() );


		//scroll the ingredients of the innerheight is > $settings.scrollHeightComparison
			//and the settings showIngredients and scrollLongIngredients are true
		if ($settings.showIngredients && $settings.scrollLongIngredients)
			updateScrollingFeature($elem, $settings);

		//scroll the disclaimer if the height of the disclaimer div is greater than scrollDisclaimerHeightComparison
		if ($settings.showDisclaimer)
			updateScrollingFeatureDisclaimer($elem, $settings);

		//this code is for pages with multiple nutrition labels generated by the plugin like the demo page
		notApplicableHover($elem);

		//add a scroll on long item names
		if ($settings.scrollLongItemName)
			addScrollToItemDiv($elem, $settings);

		//if the text box for the unit quantity is shown
		if ($settings.showServingUnitQuantityTextbox){
			//increase the unit quantity by clicking the up arrow
			$('#'+$elem.attr('id')).delegate('.unitQuantityUp', 'click', function(e){
				e.preventDefault();
				$settingsHolder = $.extend( {}, $.fn.nutritionLabel.defaultSettings, settings || {} );
				$settingsHolder.totalContainerQuantity = $settings.totalContainerQuantity;
				$settingsHolder.originalServingUnitQuantity = $settings.originalServingUnitQuantity;
				$settingsHolder.nutritionValueMultiplier = $settingsHolder.valueServingUnitQuantity <= 0 ? 1 : 1 / $settingsHolder.valueServingUnitQuantity;
				changeQuantityByArrow($(this), 1, $settingsHolder, nutritionLabel, $elem);
			});

			//decrease the unit quantity by clicking the down arrow
			$('#'+$elem.attr('id')).delegate('.unitQuantityDown', 'click', function(e){
				e.preventDefault();
				$settingsHolder = $.extend( {}, $.fn.nutritionLabel.defaultSettings, settings || {} );
				$settingsHolder.originalServingUnitQuantity = $settings.originalServingUnitQuantity;
				$settingsHolder.totalContainerQuantity = $settings.totalContainerQuantity;
				$settingsHolder.nutritionValueMultiplier = $settingsHolder.valueServingUnitQuantity <= 0 ? 1 : 1 / $settingsHolder.valueServingUnitQuantity;
				changeQuantityByArrow($(this), -1, $settingsHolder, nutritionLabel, $elem);
			});

			//the textbox unit quantity value is changed
			$('#'+$elem.attr('id')).delegate('.unitQuantityBox', 'change', function(e){
				e.preventDefault();
				$settingsHolder = $.extend( {}, $.fn.nutritionLabel.defaultSettings, settings || {} );
				$settingsHolder.originalServingUnitQuantity = $settings.originalServingUnitQuantity;
				$settingsHolder.totalContainerQuantity = $settings.totalContainerQuantity;
				$settingsHolder.nutritionValueMultiplier = $settingsHolder.valueServingUnitQuantity <= 0 ? 1 : 1 / $settingsHolder.valueServingUnitQuantity;
				changeQuantityTextbox($(this), $settingsHolder, nutritionLabel, $elem);
			});

			//the textbox unit quantity value is changed
			$('#'+$elem.attr('id')).delegate('.unitQuantityBox', 'keydown', function(e){
				if (e.keyCode == 13){
					e.preventDefault();
					$settingsHolder = $.extend( {}, $.fn.nutritionLabel.defaultSettings, settings || {} );
					$settingsHolder.originalServingUnitQuantity = $settings.originalServingUnitQuantity;
					$settingsHolder.totalContainerQuantity = $settings.totalContainerQuantity;
					$settingsHolder.nutritionValueMultiplier = $settingsHolder.valueServingUnitQuantity <= 0 ? 1 : 1 / $settingsHolder.valueServingUnitQuantity;
					changeQuantityTextbox($(this), $settingsHolder, nutritionLabel, $elem);
				}
			});
		}

		//store the object for later reference
		$elem.data('_nutritionLabel', nutritionLabel);
	}


	function addScrollToItemDiv($elem, $settings){
		if ( $('#'+$elem.attr('id')+' .name.inline').val() != undefined ){
			if ( $('#'+$elem.attr('id')+' .name.inline').height() > ( parseInt($settings.scrollLongItemNamePixel) + 1 ) )
				$('#'+$elem.attr('id')+' .name.inline').css({
					'margin-left' : '3.90em',
					'height' : parseInt($settings.scrollLongItemNamePixel)+'px',
					'overflow-y' : 'auto'
				});
		}else{
			if ( $('#'+$elem.attr('id')+' .name').height() > ( parseInt($settings.scrollLongItemNamePixel) + 1 ) )
				$('#'+$elem.attr('id')+' .name').css({
					'height' : parseInt($settings.scrollLongItemNamePixel)+'px',
					'overflow-y' : 'auto'
				});
		}
	}


	function notApplicableHover($elem){
		//this code is for pages with multiple nutrition labels generated by the plugin like the demo page
		if ($elem.attr('id') !== undefined && $elem.attr('id') !== '')
			$('#'+$elem.attr('id')+' .notApplicable').hover(
				function(){
					$('#'+$elem.attr('id')+' .naTooltip')
						.css({
							'top' : $(this).position().top+'px',
							'left' : $(this).position().left+ 10 +'px'
						}).show();
				},
				function(){
					$('#'+$elem.attr('id')+' .naTooltip').hide();
				}
			);
		else
			$('#'+$elem.attr('id')+' .notApplicable').hover(
				function(){
					$('.naTooltip')
						.css({
							'top' : $(this).position().top+'px',
							'left' : $(this).position().left+ 10 +'px'
						}).show();
				},
				function(){
					$('.naTooltip').hide();
				}
			);
	}


	function updateScrollingFeature($elem, $settings){
		if ($elem.attr('id') !== undefined && $elem.attr('id') !== '')
			//this code is for pages with multiple nutrition labels generated by the plugin like the demo page
			$ingredientListParent = $('#'+$elem.attr('id')+' #ingredientList').parent();
		else
			$ingredientListParent = $('#ingredientList').parent();

		if ($ingredientListParent.innerHeight() > $settings.scrollHeightComparison)
			$ingredientListParent.addClass('scroll').css({
				'height' : $settings.scrollHeightPixel+'px'
			});
	}


	function updateScrollingFeatureDisclaimer($elem, $settings){
		if ($elem.attr('id') !== undefined && $elem.attr('id') !== '')
			//this code is for pages with multiple nutrition labels generated by the plugin like the demo page
			$disclaimerParent = $('#'+$elem.attr('id')+' #calcDisclaimerText').parent();
		else
			$disclaimerParent = $('#calcDisclaimerText').parent();

		if ($disclaimerParent.innerHeight() > $settings.scrollDisclaimerHeightComparison)
			$disclaimerParent.addClass('scroll').css({
				'height' : $settings.scrollDisclaimer+'px'
			});
	}


	function changeQuantityTextbox($thisTextbox, $originalSettings, nutritionLabel, $elem){
		var textBoxValue = parseFloat( $thisTextbox.val() );

		textBoxValue = isNaN(textBoxValue) ? 1.0 : textBoxValue;
		$thisTextbox.val( textBoxValue.toFixed(1) );

		$originalSettings.valueServingUnitQuantity = textBoxValue;
		$originalSettings = UpdateNutritionValueWithMultiplier($originalSettings);

		nutritionLabel = new NutritionLabel($originalSettings, $elem);
		$elem.html( nutritionLabel.generate() );

		//scroll the ingredients of the innerheight is > $settings.scrollHeightComparison
		//and the settings showIngredients and scrollLongIngredients are true
		if ($originalSettings.showIngredients && $originalSettings.scrollLongIngredients)
			updateScrollingFeature($elem, $originalSettings);

		//scroll the disclaimer if the height of the disclaimer div is greater than scrollDisclaimerHeightComparison
		if ($originalSettings.showDisclaimer)
			updateScrollingFeatureDisclaimer($elem, $originalSettings);

		//this code is for pages with multiple nutrition labels generated by the plugin like the demo page
		notApplicableHover($elem);

		//add a scroll on long item names
		if ($originalSettings.scrollLongItemName)
			addScrollToItemDiv($elem, $originalSettings);
	}


	function changeQuantityByArrow($thisQuantity, changeValueBy, $settings, nutritionLabel, $elem){
		//get the current user quantity of the item
		var currentQuantity = parseFloat( $thisQuantity.parent().parent().find('input.unitQuantityBox').val() );
		if ( isNaN(currentQuantity) )
			currentQuantity = 1.0;

		//see https://github.com/nutritionix/nutrition-label/issues/14 for an explanation on this part
		if (currentQuantity <= 1 && changeValueBy == -1){
			changeValueBy = -0.5;
			currentQuantity += changeValueBy;
		}else if (currentQuantity < 1 && changeValueBy == 1){
			changeValueBy = 0.5;
			currentQuantity += changeValueBy;
		}else if (currentQuantity <= 2 && currentQuantity > 1 && changeValueBy == -1)
			currentQuantity = 1;
		else
			currentQuantity += changeValueBy;

		if (currentQuantity < 0)
			currentQuantity = 0;

		$thisQuantity.parent().parent().find('input.unitQuantityBox').val( currentQuantity.toFixed(1) );

		$settings.valueServingUnitQuantity = currentQuantity;
		$settings = UpdateNutritionValueWithMultiplier($settings);

		nutritionLabel = new NutritionLabel($settings, $elem);
		$elem.html( nutritionLabel.generate() );

		//scroll the ingredients of the innerheight is > $settings.scrollHeightComparison
			//and the settings showIngredients and scrollLongIngredients are true
		if ($settings.showIngredients && $settings.scrollLongIngredients)
			updateScrollingFeature($elem, $settings);

		//scroll the disclaimer if the height of the disclaimer div is greater than scrollDisclaimerHeightComparison
		if ($settings.showDisclaimer)
			updateScrollingFeatureDisclaimer($elem, $settings);

		//this code is for pages with multiple nutrition labels generated by the plugin like the demo page
		notApplicableHover($elem);

		//add a scroll on long item names
		if ($settings.scrollLongItemName)
			addScrollToItemDiv($elem, $settings);
	}


	//round the value to the nearest number
	function roundToNearestNum(input, nearest){
		if (nearest < 0)
			return Math.round(input*nearest)/nearest;
		else
			return Math.round(input/nearest)*nearest;
	}


	function roundCalories(toRound, decimalPlace){
		toRound = roundCaloriesRule(toRound);
		if (toRound > 0)
			toRound = parseFloat( toRound.toFixed(decimalPlace) );
		return toRound;
	}


	function roundFat(toRound, decimalPlace){
		toRound = roundFatRule(toRound);
		if (toRound > 0)
			toRound = parseFloat( toRound.toFixed(decimalPlace) );
		return toRound;
	}


	function roundSodium(toRound, decimalPlace){
		toRound = roundSodiumRule(toRound);
		if (toRound > 0)
			toRound = parseFloat( toRound.toFixed(decimalPlace) );
		return toRound;
	}


	function roundCholesterol(toRound, decimalPlace){
		var normalVersion = true;
		var roundResult = roundCholesterolRule(toRound);
		if (roundResult === false)
			normalVersion = false;
		else
			toRound = roundResult;
		if (normalVersion){
			if (toRound > 0)
				toRound = parseFloat( toRound.toFixed(decimalPlace) );
		}else
			toRound = '< 5';
		return toRound;
	}


	function roundCarbFiberSugarProtein(toRound, decimalPlace){
		var normalVersion = true;
		var roundResult = roundCarbFiberSugarProteinRule(toRound);
		if (roundResult === false)
			normalVersion = false;
		else
			toRound = roundResult;
		if (normalVersion){
			if (toRound > 0)
				toRound = parseFloat( toRound.toFixed(decimalPlace) );
		}else
			toRound = '< 1';
		return toRound;
	}


	//Calories and Calories from Fat rounding rule
	function roundCaloriesRule(toRound){
		if (toRound < 5)
			return 0;
		else if (toRound <= 50)
			//50 cal - express to nearest 5 cal increment
			return roundToNearestNum(toRound, 5);
		else
			//> 50 cal - express to nearest 10 cal increment
			return roundToNearestNum(toRound, 10);
	}


	//Total Fat, Saturated Fat, Polyunsaturated Fat and Monounsaturated Fat rounding rule
	function roundFatRule(toRound){
		if (toRound < .5)
			return 0;
		else if (toRound < 5)
			//< 5 g - express to nearest .5g increment
			return roundToNearestNum(toRound, .5);
		else
			//>= 5 g - express to nearest 1 g increment
			return roundToNearestNum(toRound, 1);
	}


	//Sodium rounding rule
	function roundSodiumRule(toRound){
		if (toRound < 5)
			return 0;
		else if (toRound <= 140)
			//5 - 140 mg - express to nearest 5 mg increment
			return roundToNearestNum(toRound, 5);
		else
			//>= 5 g - express to nearest 10 g increment
			return roundToNearestNum(toRound, 10);
	}


	//Cholesterol rounding rule
	function roundCholesterolRule(toRound){
		if (toRound < 2)
			return 0;
		else if (toRound <= 5)
			return false;
		else
			//> 5 mg - express to nearest 5 mg increment
			return roundToNearestNum(toRound, 5);
	}


	//Total Carbohydrate, Dietary Fiber, Sugar and Protein rounding rule
	function roundCarbFiberSugarProteinRule(toRound){
		if (toRound < .5)
			return 0;
		else if (toRound < 1)
			//< 1 g - express as "Contains less than 1g" or "less than 1g"
			return false;
		else
			//> 1 mg - express to nearest 1 g increment
			return roundToNearestNum(toRound, 1);
	}


	//Total Carbohydrate, Dietary Fiber, Sugar and Protein rounding rule
	function roundVitaminsCalciumIron(toRound){
		if (toRound > 0){
			if (toRound < 10)
				//< 10 - round to nearest even number
				return roundToNearestNum(toRound, 2);
			else if (toRound < 50)
				//between 10 and 50, round to the nearest 5 increment
				return roundToNearestNum(toRound, 5);
			else
				//else, round to the nearest 10 increment
				return roundToNearestNum(toRound, 10);
		}else
			return 0;
	}


	NutritionLabel.prototype = {
		generate: function(){
			//this is the function that returns the html code for the nutrition label based on the settings that is supplied by the user
			var $this = this;

			//return the plugin incase it has already been created
			if ($this.nutritionLabel)
				return $this.nutritionLabel;

			if ($this.settings.hideNotAppicableValues){
				$this.settings.showCalories = $this.settings.naCalories ? false : $this.settings.showCalories;
				$this.settings.showFatCalories = $this.settings.naFatCalories ? false : $this.settings.showFatCalories;
				$this.settings.showTotalFat = $this.settings.naTotalFat ? false : $this.settings.showTotalFat;
				$this.settings.showSatFat = $this.settings.naSatFat ? false : $this.settings.showSatFat;
				$this.settings.showTransFat = $this.settings.naTransFat ? false : $this.settings.showTransFat;
				$this.settings.showPolyFat = $this.settings.naPolyFat ? false : $this.settings.showPolyFat;
				$this.settings.showMonoFat = $this.settings.naMonoFat ? false : $this.settings.showMonoFat;
				$this.settings.showCholesterol = $this.settings.naCholesterol ? false : $this.settings.showCholesterol;
				$this.settings.showSodium = $this.settings.naSodium ? false : $this.settings.showSodium;
				$this.settings.showPotassium = $this.settings.naPotassium ? false : $this.settings.showPotassium;
				$this.settings.showPhosphorus = $this.settings.naPhosphorus ? false : $this.settings.showPhosphorus;
				$this.settings.showMagnesium = $this.settings.naMagnesium ? false : $this.settings.showMagnesium;
				$this.settings.showVitaminE = $this.settings.naVitaminE ? false : $this.settings.showVitaminE;
				$this.settings.showVitaminD = $this.settings.naVitaminD ? false : $this.settings.showVitaminD;
				$this.settings.showThiamin = $this.settings.naThiamin ? false : $this.settings.showThiamin;
				$this.settings.showRiboflavin = $this.settings.naRiboflavin ? false : $this.settings.showRiboflavin;
				$this.settings.showNiacin = $this.settings.naNiacin ? false : $this.settings.showNiacin;
				$this.settings.showPantothenicAcid = $this.settings.naPantothenicAcid ? false : $this.settings.showPantothenicAcid;
				$this.settings.showVitaminB6 = $this.settings.naVitaminB6 ? false : $this.settings.showVitaminB6;
				$this.settings.showVitaminB12 = $this.settings.naVitaminB12 ? false : $this.settings.showVitaminB12;
				$this.settings.showVitaminK = $this.settings.naVitaminK ? false : $this.settings.showVitaminK;
				$this.settings.showFolate = $this.settings.naFolate ? false : $this.settings.showFolate;
				$this.settings.showTotalCarb = $this.settings.naTotalCarb ? false : $this.settings.showTotalCarb;
				$this.settings.showFibers = $this.settings.naFibers ? false : $this.settings.showFibers;
				$this.settings.showSugars = $this.settings.naSugars ? false : $this.settings.showSugars;
				$this.settings.showProteins = $this.settings.naProteins ? false : $this.settings.showProteins;
				$this.settings.showVitaminA = $this.settings.naVitaminA ? false : $this.settings.showVitaminA;
				$this.settings.showVitaminC = $this.settings.naVitaminC ? false : $this.settings.showVitaminC;
				$this.settings.showCalcium = $this.settings.naCalcium ? false : $this.settings.showCalcium;
				$this.settings.showIron = $this.settings.naIron ? false : $this.settings.showIron;
			}

			//initializing the tab variables
			//tab variables are used to make the printing of the html code readable when you copy the code using
				//firebug => inspect => copy innerhtml
			//for debugging and editing purposes
			for (x = 1; x < 9; x++){
				var tab = '';
				for (y = 1; y <= x; y++)
					tab += '\t';
				eval('var tab' + x + ' = "' + tab + '";');
			}

			//initialize the not applicable image icon in case we need to use it
			var naValue = '<font class="notApplicable">-&nbsp;</font>';

			var calorieIntakeMod = (parseFloat($this.settings.calorieIntake) / 2000).toFixed(2);

			var borderCSS = '';
			if ($this.settings.allowNoBorder)
				borderCSS = 'border: 0;';

			//creates the html code for the label based on the settings
			var nutritionLabel = '';


			if (!$this.settings.allowCustomWidth)
				nutritionLabel += '<div class="nutritionLabel" style="' + borderCSS + ' width: '+ $this.settings.width + 'px;">\n';
			else
				nutritionLabel += '<div class="nutritionLabel" style="' + borderCSS + ' width: '+ $this.settings.widthCustom + ';">\n';


				nutritionLabel += tab1 + '<div class="title">' + $this.settings.textNutritionFacts + '</div>\n';


		if ($this.settings.showItemName){
			var tabTemp = tab1;
			var itemNameClass = '';
			if ($this.settings.showServingUnitQuantityTextbox){
				if (
					($this.settings.valueServingSizeUnit == null || $this.settings.valueServingSizeUnit == '') ||
					($this.settings.valueServingSizeUnit !== '' && $this.settings.valueServingSizeUnit !== null &&
						$this.settings.originalServingUnitQuantity <= 0)
				){
				nutritionLabel += tab1 + '<div class="cf">\n';
					nutritionLabel += tab2 + '<div class="rel servingSizeField">\n';

					var textboxClass = 'unitQuantityBox';
					if (!$this.settings.hideTextboxArrows){
						nutritionLabel += tab3 + '<div class="setter">\n';
							nutritionLabel += tab4 + '<a href="Increase the quantity" class="unitQuantityUp" rel="nofollow"></a>\n';
							nutritionLabel += tab4 + '<a href="Decrease the quantity" class="unitQuantityDown" rel="nofollow"></a>\n';
						nutritionLabel += tab3 + '</div><!-- closing class="setter" -->\n';
					}else
						textboxClass = 'unitQuantityBox arrowsAreHidden';

						nutritionLabel += tab3 + '<input type="text" value="'+ parseFloat( $this.settings.valueServingUnitQuantity.toFixed($this.settings.decimalPlacesForQuantityTextbox) ) +'" ';
								nutritionLabel += 'class="'+textboxClass+'">\n';
					nutritionLabel += tab2 + '</div><!-- closing class="servingSizeField" -->\n';
					tabTemp = tab2;
					var itemNameClass = 'inline';
				}
			}//end of => if ($this.settings.showServingUnitQuantityTextbox){

				nutritionLabel += tabTemp + '<div class="name '+ itemNameClass +'">';
					nutritionLabel += $this.settings.itemName;
				if ($this.settings.showBrandName && $this.settings.brandName != null && $this.settings.brandName != '')
					nutritionLabel += ' - ' + $this.settings.brandName;
				nutritionLabel += '</div>\n';

			if ($this.settings.showServingUnitQuantityTextbox)
				if (
					($this.settings.valueServingSizeUnit == null || $this.settings.valueServingSizeUnit == '') ||
					($this.settings.valueServingSizeUnit !== '' && $this.settings.valueServingSizeUnit !== null &&
						$this.settings.originalServingUnitQuantity <= 0)
				)
					nutritionLabel += tab1 + '</div><!-- closing class="cf" -->\n';
		}//end of => if ($this.settings.showItemName)


			var servingSizeIsHidden = false;
			var servingContainerIsHidden = false;
			var servingSizeTextClass = '';
			if ($this.settings.showServingUnitQuantity){
				nutritionLabel += tab1 + '<div class="serving">\n';

				if ($this.settings.originalServingUnitQuantity > 0){
					nutritionLabel += tab2 + '<div class="cf">\n';
						nutritionLabel += tab3 + '<div class="servingSizeText fl">' + $this.settings.textServingSize + '</div>\n';
							nutritionLabel += $this.settings.showServingUnitQuantityTextbox ?
								'' : tab3 + '<div class="servingUnitQuantity fl">' + parseFloat( $this.settings.originalServingUnitQuantity.toFixed($this.settings.decimalPlacesForNutrition) ) + '</div>\n';

					var unitAddedClass = '';
					var gramsAddedClass = '';
					if ($this.settings.valueServingSizeUnit !== '' && $this.settings.valueServingSizeUnit !== null){
						if ($this.settings.showServingUnitQuantityTextbox && $this.settings.valueServingSizeUnit != null &&
									$this.settings.valueServingSizeUnit != ''){
							unitAddedClass = 'unitHasTextbox';
							gramsAddedClass = 'gramsHasTextbox';
							nutritionLabel += tab3 + '<div class="rel servingSizeField fl">\n';

							var textboxClass = 'unitQuantityBox';
							if (!$this.settings.hideTextboxArrows){
								nutritionLabel += tab4 + '<div class="setter">\n';
									nutritionLabel += tab5 + '<a href="Increase the quantity" class="unitQuantityUp" rel="nofollow"></a>\n';
									nutritionLabel += tab5 + '<a href="Decrease the quantity" class="unitQuantityDown" rel="nofollow"></a>\n';
								nutritionLabel += tab4 + '</div><!-- closing class="setter" -->\n';
							}else
								textboxClass = 'unitQuantityBox arrowsAreHidden';

								nutritionLabel += tab4 + '<input type="text" value="'+ parseFloat( $this.settings.valueServingUnitQuantity.toFixed($this.settings.decimalPlacesForQuantityTextbox) ) +'" ';
										nutritionLabel += 'class="'+textboxClass+'">\n';
							nutritionLabel += tab3 + '</div><!-- closing class="servingSizeField" -->\n';
						}else if ($this.settings.originalServingUnitQuantity > 0 && $this.settings.showServingUnitQuantityTextbox)
								nutritionLabel += tab3 + '<div class="servingUnitQuantity">' + parseFloat( $this.settings.originalServingUnitQuantity.toFixed($this.settings.decimalPlacesForNutrition) ) + '</div>\n';

							nutritionLabel += tab3 + '<div class="servingUnit fl '+unitAddedClass+'">'+ $this.settings.valueServingSizeUnit + '</div>\n';

					}else if ($this.settings.originalServingUnitQuantity > 0 && $this.settings.showServingUnitQuantityTextbox)
							nutritionLabel += tab3 + '<div class="servingUnitQuantity fl">' + parseFloat( $this.settings.originalServingUnitQuantity.toFixed($this.settings.decimalPlacesForNutrition) ) + '</div>\n';
					//end of => if ($this.settings.valueServingSizeUnit !== '' && $this.settings.valueServingSizeUnit !== null){

					if ($this.settings.valueServingWeightGrams > 0)
							nutritionLabel += tab3 + '<div class="servingWeightGrams fl '+gramsAddedClass+'">('+
								parseFloat( $this.settings.valueServingWeightGrams.toFixed($this.settings.decimalPlacesForNutrition) )
							+ 'g)</div>\n';

				nutritionLabel += tab2 + '</div><!-- closing class="cf" -->\n';
			}else
				servingSizeIsHidden = true;
			//end of => if ($this.settings.originalServingUnitQuantity > 0){


			if ($this.settings.showServingsPerContainer){
				//Serving per container
				if ($this.settings.valueServingPerContainer > 0){
					nutritionLabel += tab2 + '<div>' + $this.settings.textServingsPerContainer + ' ';
						nutritionLabel += parseFloat(
							$this.settings.valueServingPerContainer.toFixed($this.settings.decimalPlacesForNutrition)
						);
					nutritionLabel += '</div>\n';
				}else
					servingContainerIsHidden = true;
			}else
				servingContainerIsHidden = true;

			nutritionLabel += tab1 + '</div><!-- closing class="serving" -->\n';
		}//end of => if ($this.settings.showServingUnitQuantity)


			if ( (!$this.settings.showItemName && !$this.settings.showServingUnitQuantity) ||
						(!$this.settings.showItemName && servingSizeIsHidden && servingContainerIsHidden) )
				nutritionLabel += tab1 + '<div class="headerSpacer"></div>\n';

				nutritionLabel += tab1 + '<div class="bar1"></div>\n';


			if ($this.settings.showAmountPerServing){
				nutritionLabel += tab1 + '<div class="line m">';
					nutritionLabel += '<b>' + $this.settings.textAmountPerServing + '</b>';
				nutritionLabel += '</div>\n';
			}

				nutritionLabel += tab1 + '<div class="line">\n';


				if ($this.settings.showFatCalories){
					nutritionLabel += tab2 + '<div class="fr">';
						nutritionLabel += $this.settings.textFatCalories + ' ';
						nutritionLabel += $this.settings.naFatCalories ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundCalories($this.settings.valueFatCalories, $this.settings.decimalPlacesForNutrition) :
								parseFloat( $this.settings.valueFatCalories.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitFatCalories;
					nutritionLabel += '</div>\n';
				}


				if ($this.settings.showCalories){
					nutritionLabel += tab2 + '<div>';
						nutritionLabel += '<b>' + $this.settings.textCalories + '</b> ';
						nutritionLabel += $this.settings.naCalories ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundCalories($this.settings.valueCalories, $this.settings.decimalPlacesForNutrition) :
								parseFloat( $this.settings.valueCalories.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitCalories;
					nutritionLabel += '</div>\n';
				}else if ($this.settings.showFatCalories)
					nutritionLabel += tab2 + '<div>&nbsp;</div>\n';


				nutritionLabel += tab1 + '</div>\n';
				nutritionLabel += tab1 + '<div class="bar2"></div>\n';

				nutritionLabel += tab1 + '<div class="line ar">';
					nutritionLabel += '<b>% ' + $this.settings.textDailyValues + '<sup>*</sup></b>';
				nutritionLabel += '</div>\n';


			if ($this.settings.showTotalFat){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naTotalFat ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundFatRule($this.settings.valueTotalFat) : $this.settings.valueTotalFat) / ($this.settings.dailyValueTotalFat * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textTotalFat + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naTotalFat ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundFat($this.settings.valueTotalFat, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueTotalFat.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitTotalFat
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showTotalFat){


			if ($this.settings.showSatFat){
				nutritionLabel += tab1 + '<div class="line indent">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naSatFat ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundFatRule($this.settings.valueSatFat) : $this.settings.valueSatFat) / ($this.settings.dailyValueSatFat * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textSatFat + ' ';
						nutritionLabel +=
							(
							$this.settings.naSatFat ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundFat($this.settings.valueSatFat, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueSatFat.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitSatFat
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showSatFat){


			if ($this.settings.showTransFat){
				nutritionLabel += tab1 + '<div class="line indent">\n';
					nutritionLabel += tab2 + $this.settings.textTransFat + ' ';
						nutritionLabel +=
							(
							$this.settings.naTransFat ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundFat($this.settings.valueTransFat, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueTransFat.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitTransFat
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showPolyFat){
				nutritionLabel += tab1 + '<div class="line indent">';
					nutritionLabel += $this.settings.textPolyFat + ' ';
						nutritionLabel += $this.settings.naPolyFat ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundFat($this.settings.valuePolyFat, $this.settings.decimalPlacesForNutrition) :
								parseFloat( $this.settings.valuePolyFat.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitPolyFat;
				nutritionLabel += '</div>\n';
			}


			if ($this.settings.showMonoFat){
				nutritionLabel += tab1 + '<div class="line indent">';
					nutritionLabel += $this.settings.textMonoFat + ' ';
						nutritionLabel += $this.settings.naMonoFat ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundFat($this.settings.valueMonoFat, $this.settings.decimalPlacesForNutrition) :
								parseFloat( $this.settings.valueMonoFat.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitMonoFat;
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showCholesterol){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naCholesterol ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundCholesterolRule($this.settings.valueCholesterol) : $this.settings.valueCholesterol) / ($this.settings.dailyValueCholesterol * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textCholesterol + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naCholesterol ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundCholesterol($this.settings.valueCholesterol, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueCholesterol.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitCholesterol
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showCholesterol){


			if ($this.settings.showSodium){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naSodium ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundSodiumRule($this.settings.valueSodium) : $this.settings.valueSodium) / ($this.settings.dailyValueSodium * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textSodium + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naSodium ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundSodium($this.settings.valueSodium, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueSodium.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitSodium
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showSodium){

		if ($this.settings.showMagnesium){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naMagnesium ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundSodiumRule($this.settings.valueMagnesium) : $this.settings.valueMagnesium) / ($this.settings.dailyValueMagnesium * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textMagnesium + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naMagnesium ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundSodium($this.settings.valueMagnesium, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueMagnesium.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitMagnesium
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showMagnesium){

			if ($this.settings.showPotassium){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naPotassium ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundSodiumRule($this.settings.valuePotassium) : $this.settings.valuePotassium) / ($this.settings.dailyValuePotassium * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textPotassium + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naPotassium ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundSodium($this.settings.valuePotassium, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valuePotassium.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitPotassium
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showPotassium){


			if ($this.settings.showPhosphorus){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naPhosphorus ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundSodiumRule($this.settings.valuePhosphorus) : $this.settings.valuePhosphorus) / ($this.settings.dailyValuePhosphorus * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textPhosphorus + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naPhosphorus ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundPhosphorus($this.settings.valuePhosphorus, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valuePhosphorus.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitPhosphorus
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showPhosphorus){


			if ($this.settings.showTotalCarb){
				nutritionLabel += tab1 + '<div class="line">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naTotalCarb ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundCarbFiberSugarProteinRule($this.settings.valueTotalCarb) : $this.settings.valueTotalCarb) / ($this.settings.dailyValueCarb * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + '<b>' + $this.settings.textTotalCarb + '</b> ';
						nutritionLabel +=
							(
							$this.settings.naTotalCarb ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundCarbFiberSugarProtein($this.settings.valueTotalCarb, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueTotalCarb.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitTotalCarb
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showTotalCarb){


			if ($this.settings.showFibers){
				nutritionLabel += tab1 + '<div class="line indent">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naFibers ?
							naValue :
							'<b>' +
							parseFloat(
								parseFloat(
									(
										($this.settings.allowFDARounding ? roundCarbFiberSugarProteinRule($this.settings.valueFibers) : $this.settings.valueFibers) / ($this.settings.dailyValueFiber * calorieIntakeMod)
									) * 100
								).toFixed($this.settings.decimalPlacesForDailyValues)
							) + '</b>%';
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textFibers + ' ';
						nutritionLabel +=
							(
							$this.settings.naFibers ?
								naValue :
								(
								$this.settings.allowFDARounding ?
									roundCarbFiberSugarProtein($this.settings.valueFibers, $this.settings.decimalPlacesForNutrition) :
									parseFloat( $this.settings.valueFibers.toFixed($this.settings.decimalPlacesForNutrition) )
								) + $this.settings.unitFibers
							) + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}//end of => if ($this.settings.showFibers){


			if ($this.settings.showSugars){
				nutritionLabel += tab1 + '<div class="line indent">';
					nutritionLabel += $this.settings.textSugars + ' ';
						nutritionLabel += $this.settings.naSugars ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundCarbFiberSugarProtein($this.settings.valueSugars, $this.settings.decimalPlacesForNutrition) :
								parseFloat( $this.settings.valueSugars.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitSugars;
				nutritionLabel += '</div>\n';
			}


			if ($this.settings.showProteins){
				nutritionLabel += tab1 + '<div class="line">';
					nutritionLabel += '<b>' + $this.settings.textProteins + '</b> ';
						nutritionLabel += $this.settings.naProteins ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundCarbFiberSugarProtein($this.settings.valueProteins, $this.settings.decimalPlacesForNutrition) :
								parseFloat( $this.settings.valueProteins.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitProteins;
				nutritionLabel += '</div>\n';
			}


			nutritionLabel += tab1 + '<div class="bar1"></div>\n';


			if ($this.settings.showVitaminA){
				nutritionLabel += tab1 + '<div class="line vitaminA">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminA ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminA) :
								parseFloat( $this.settings.valueVitaminA.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminA;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminA + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showVitaminC){
				nutritionLabel += tab1 + '<div class="line vitaminC">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminC ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminC) :
								parseFloat( $this.settings.valueVitaminC.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminC;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminC + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showVitaminE){
				nutritionLabel += tab1 + '<div class="line vitaminE">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminE ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminE) :
								parseFloat( $this.settings.valueVitaminE.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminE;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminE + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showVitaminD){
				nutritionLabel += tab1 + '<div class="line VitaminD">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminD ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminD) :
								parseFloat( $this.settings.valueVitaminD.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminD;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminD + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showThiamin){
				nutritionLabel += tab1 + '<div class="line Thiamin">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naThiamin ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueThiamin) :
								parseFloat( $this.settings.valueThiamin.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitThiamin;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textThiamin + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showRiboflavin){
				nutritionLabel += tab1 + '<div class="line Riboflavin">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naRiboflavin ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueRiboflavin) :
								parseFloat( $this.settings.valueRiboflavin.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitRiboflavin;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textRiboflavin + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showNiacin){
				nutritionLabel += tab1 + '<div class="line Niacin">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naNiacin ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueNiacin) :
								parseFloat( $this.settings.valueNiacin.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitNiacin;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textNiacin + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showPantothenicAcid){
				nutritionLabel += tab1 + '<div class="line Pantothenic Acid">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naPantothenicAcid ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valuePantothenicAcid) :
								parseFloat( $this.settings.valuePantothenicAcid.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitPantothenicAcid;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textPantothenicAcid + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showVitaminB6){
				nutritionLabel += tab1 + '<div class="line vitaminB6">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminB6 ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminB6) :
								parseFloat( $this.settings.valueVitaminB6.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminB6;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminB6 + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showVitaminB12){
				nutritionLabel += tab1 + '<div class="line vitaminB12">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminB12 ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminB12) :
								parseFloat( $this.settings.valueVitaminB12.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminB12;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminB12 + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showVitaminK){
				nutritionLabel += tab1 + '<div class="line vitaminK">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naVitaminK ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueVitaminK) :
								parseFloat( $this.settings.valueVitaminK.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitVitaminK;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textVitaminK + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showFolate){
				nutritionLabel += tab1 + '<div class="line Folate">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naFolate?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueFolate) :
								parseFloat( $this.settings.valueFolate.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitFolate;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textFolate + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showCalcium){
				nutritionLabel += tab1 + '<div class="line calcium">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naCalcium ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueCalcium) :
								parseFloat( $this.settings.valueCalcium.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitCalcium;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textCalcium + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showIron){
				nutritionLabel += tab1 + '<div class="line iron">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naIron ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueIron) :
								parseFloat( $this.settings.valueIron.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitIron;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textIron + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


			if ($this.settings.showZinc){
				nutritionLabel += tab1 + '<div class="line zinc">\n';
					nutritionLabel += tab2 + '<div class="dv">';
						nutritionLabel += $this.settings.naZinc ?
							naValue :
							(
							$this.settings.allowFDARounding ?
								roundVitaminsCalciumIron($this.settings.valueZinc) :
								parseFloat( $this.settings.valueZinc.toFixed($this.settings.decimalPlacesForNutrition) )
							) + $this.settings.unitZinc;
					nutritionLabel += '</div>\n';

					nutritionLabel += tab2 + $this.settings.textZinc + '\n';
				nutritionLabel += tab1 + '</div>\n';
			}


				nutritionLabel += tab1 + '<div class="dvCalorieDiet line">\n';
					nutritionLabel += tab2 + '<div class="calorieNote">\n';
						nutritionLabel += tab3 + '<span class="star">*</span> ' + $this.settings.textPercentDailyPart1 + ' ' + $this.settings.calorieIntake + ' ' + $this.settings.textPercentDailyPart2 + '.\n';
					if ($this.settings.showIngredients){
						nutritionLabel += tab3 + '<br />\n';
						nutritionLabel += tab3 + '<div class="ingredientListDiv">\n';
							nutritionLabel += tab4 + '<b class="active" id="ingredientList">' + $this.settings.ingredientLabel + '</b>\n';
							nutritionLabel += tab4 + $this.settings.ingredientList + '\n';
						nutritionLabel += tab3 + '</div><!-- closing class="ingredientListDiv" -->\n';
					}

					if ($this.settings.showDisclaimer){
						nutritionLabel += tab3 + '<br/>';
						nutritionLabel += tab3 + '<div id="calcDisclaimer">\n';
							nutritionLabel += tab4 + '<span id="calcDisclaimerText">' + $this.settings.valueDisclaimer + '</span>\n';
						nutritionLabel += tab3 + '</div>\n';
						nutritionLabel += tab3 + '<br/>';
					}

					nutritionLabel += tab2 + '</div><!-- closing class="calorieNote" -->\n';


				if ($this.settings.showCalorieDiet){
			  		nutritionLabel += tab2 + '<table class="tblCalorieDiet">\n';
			          nutritionLabel += tab3 + '<thead>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<th>&nbsp;</th>\n';
			              nutritionLabel += tab5 + '<th>Calories</th>\n';
			              nutritionLabel += tab5 + '<th>'+$this.settings.valueCol1CalorieDiet+'</th>\n';
			              nutritionLabel += tab5 + '<th>'+$this.settings.valueCol2CalorieDiet+'</th>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			          nutritionLabel += tab3 + '</thead>\n';
			          nutritionLabel += tab3 + '<tbody>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<td>Total Fat</td>\n';
			              nutritionLabel += tab5 + '<td>Less than</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol1DietaryTotalFat+'g</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol2DietaryTotalFat+'g</td>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<td>&nbsp;&nbsp; Saturated Fat</td>\n';
			              nutritionLabel += tab5 + '<td>Less than</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol1DietarySatFat+'g</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol2DietarySatFat+'g</td>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<td>Cholesterol</td>\n';
			              nutritionLabel += tab5 + '<td>Less than</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol1DietaryCholesterol+'mg</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol2DietaryCholesterol+'mg</td>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<td>Sodium</td>\n';
			              nutritionLabel += tab5 + '<td>Less than</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol1DietarySodium+'mg</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol2DietarySodium+'mg</td>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<td>Total Carbohydrate</td>\n';
			              nutritionLabel += tab5 + '<td>&nbsp;</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol1DietaryTotalCarb+'g</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol2DietaryTotalCarb+'g</td>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			            nutritionLabel += tab4 + '<tr>\n';
			              nutritionLabel += tab5 + '<td>&nbsp;&nbsp; Dietary</td>\n';
			              nutritionLabel += tab5 + '<td>&nbsp;</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol1Dietary+'g</td>\n';
			              nutritionLabel += tab5 + '<td>'+$this.settings.valueCol2Dietary+'g</td>\n';
			            nutritionLabel += tab4 + '</tr>\n';
			          nutritionLabel += tab3 + '</tbody>\n';
			        nutritionLabel += tab2 + '</table>\n';
			  	}//end of => if ($this.settings.showCalorieDiet){
				nutritionLabel += tab1 + '</div><!-- closing class="dvCalorieDiet line" -->\n';


			if ($this.settings.showBottomLink){
				nutritionLabel += tab1 + '<div class="spaceAbove"></div>\n';
				nutritionLabel += tab1 + '<a href="' + $this.settings.urlBottomLink + '" target="_newSite" class="homeLinkPrint">' + $this.settings.nameBottomLink + '</a>\n';
				nutritionLabel += tab1 + '<div class="spaceBelow"></div>\n';
			}

			if ($this.settings.showCustomFooter)
				nutritionLabel += tab1 + '<div class="customFooter">' + $this.settings.valueCustomFooter + '</div>\n';

			nutritionLabel += '</div><!-- closing class="nutritionLabel" -->\n';

			nutritionLabel += '<div class="naTooltip">Data not available</div>\n';

			//returns the html for the nutrition label
			return nutritionLabel;
		}

	};
})(jQuery);