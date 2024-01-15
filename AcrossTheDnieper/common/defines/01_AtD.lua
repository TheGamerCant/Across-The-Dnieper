
NDefines.NGame.START_DATE = "2014.1.1.1"		--base is 1936.1.1.12
NDefines.NGame.END_DATE = "2100.1.1.1"		--base is 1949.1.1.1
NDefines.NGame.MAP_SCALE_PIXEL_TO_KM = 0.4	--base is 7.114

NDefines.NDiplomacy.VOLUNTEERS_TRANSFER_SPEED = 2	--base is 14
NDefines.NDiplomacy.REVOKE_EMBARGO_COST = 50		--base is 0

NDefines.NBuildings.RADAR_RANGE_BASE = 160		--base is 20
NDefines.NBuildings.RADAR_RANGE_MIN = 160			--base is 20
NDefines.NBuildings.RADAR_RANGE_MAX = 1300		--base is 200
NDefines.NRailwayGun.RAILWAY_GUN_RANGE = 160		--base is 30

NDefines.NCountry.MIN_STABILITY = -1.0
NDefines.NCountry.MIN_WAR_SUPPORT = -1.0
NDefines.NCountry.POLITICAL_POWER_LOWER_CAP = -2000.0
NDefines.NCountry.MIN_MAJOR_COUNTRIES = 3 -- was 1, should result in at least 3 countries being assigned the major tag, no real change to gameplay
NDefines.NCountry.EVENT_PROCESS_OFFSET = 30	--base is 20, this should reduce lag
NDefines.NCountry.BASE_SURRENDER_LIMIT = 0.65		--base is 0.8
NDefines.NCountry.SURRENDER_LIMIT_REDUCTION_PER_COLLABORATION = 0.2		-- base is 0.3

NDefines.NProduction.DEFAULT_MAX_NAV_FACTORIES_PER_LINE = 15		--base is 10
NDefines.NProduction.CAPITAL_SHIP_MAX_NAV_FACTORIES_PER_LINE = 15		--base is 5
NDefines.NProduction.RAILWAY_GUN_MAX_MIL_FACTORIES_PER_LINE = 15		--base is 5

--All of this AI stuff doesn't affect strategy, just used to increase performance
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_DOCTRINE = 90  --7 the ai will check what the best doctrine they can have is once every 3 months
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_TEMPLATE = 30  --7 the ai will check what the best division template they can have is once every month
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_EQUIPMENT = 30 --7 the ai will check what the best equipment they can have is once every month
NDefines.NAI.RESEARCH_DAYS_BETWEEN_WEIGHT_UPDATE = 14 --7 the ai will refreshes need scores based on country situation
NDefines.NAI.AI_UPDATE_ROLES_FREQUENCY_HOURS = 360  --48 the ai will change templates less frequently
NDefines.NAI.UPDATE_SUPPLY_MOTORIZATION_FREQUENCY_HOURS = 120    --52 every 5 days the ai will check weather they should increase supply motorization
NDefines.NAI.UPDATE_SUPPLY_BOTTLENECKS_FREQUENCY_HOURS = 320    --168 every 15 days the ai will check for supply related bottlenecks and try to fix them
NDefines.NAI.AREA_DEFENSE_SETTING_VP = true --False (AI will garrison cities as well as coasts)
NDefines.NAI.MAX_MICRO_ATTACKS_PER_ORDER = 5    --3 (might improve the AI's ability to wage war for some cost in performance, should be neglegeble as its only active at war)


NDefines.NMilitary.CORPS_COMMANDER_DIVISIONS_CAP = 72				--base is 24
NDefines.NMilitary.FIELD_MARSHAL_DIVISIONS_CAP = 72				--base is 24
NDefines.NMilitary.FIELD_MARSHAL_ARMIES_CAP = 8					--base is 5
NDefines.NMilitary.LAND_SPEED_MODIFIER = 0.55					--base is 0.05
NDefines.NMilitary.ATTRITION_EQUIPMENT_LOSS_CHANCE = 0.02			--base is 0.1
NDefines.NMilitary.ATTRITION_DAMAGE_ORG = 0.02					--base is 0.08
NDefines.NMilitary.ATTRITION_EQUIPMENT_PER_TYPE_LOSS_CHANCE = 0.02		--base is 0.1
NDefines.NMilitary.MAX_ARMY_EXPERIENCE = 999					--base is 500
NDefines.NMilitary.MAX_NAVY_EXPERIENCE = 999					--base is 500
NDefines.NMilitary.MAX_AIR_EXPERIENCE = 999					--base is 500
NDefines.NMilitary.BASE_DIVISION_BRIGADE_GROUP_COST = 2				--base is 5	
NDefines.NMilitary.BASE_DIVISION_BRIGADE_CHANGE_COST = 2			--base is 5
NDefines.NMilitary.BASE_DIVISION_SUPPORT_SLOT_COST = 4				--base is 10
NDefines.NMilitary.RIVER_CROSSING_PENALTY = -0.4				--base is -0.3
NDefines.NMilitary.RIVER_CROSSING_PENALTY_LARGE = -0.7				--base is -0.6
NDefines.NMilitary.RIVER_CROSSING_SPEED_PENALTY = -0.35				--base is -0.25
NDefines.NMilitary.RIVER_CROSSING_SPEED_PENALTY_LARGE = -0.6			--base is -0.5
NDefines.NMilitary.INFRASTRUCTURE_MOVEMENT_SPEED_IMPACT = -0.1			--base is -0.05 (speed penalty per infrastucture below maximum)
NDefines.NMilitary.BASE_FORT_PENALTY = -0.12					--base is -0.15, bunkers now give less defence and have 5 levels max but are cheaper 
NDefines.NMilitary.ENCIRCLED_PENALTY = -0.6					--base is -0.3, encirclements are now more punishing

NDefines.NFocus.FOCUS_POINT_DAYS = 1			--base is 7
NDefines.NFocus.MAX_SAVED_FOCUS_PROGRESS = 30   --10 (lets you not pick a focus for some time)

NDefines.NSupply.NODE_INITIAL_SUPPLY_FLOW = 5.6		--base is 2.8

-- These make on-map GUIs and indicators show up when zoomed out further
NDefines_Graphics.NGraphics.VICTORY_POINT_MAP_ICON_TEXT_CUTOFF = {500, 1000, 2250}			--base is 150, 250, 500
NDefines_Graphics.NGraphics.VICTORY_POINTS_DISTANCE_CUTOFF = {750, 1250, 2250}			--base is 250, 500, 1000
NDefines_Graphics.NGraphics.AIRBASE_ICON_DISTANCE_CUTOFF = 1800						--base is 900
NDefines_Graphics.NGraphics.NAVALBASE_ICON_DISTANCE_CUTOFF = 1800						--base is 900
NDefines_Graphics.NGraphics.RADAR_ICON_DISTANCE_CUTOFF = 2000						--base is 1100
NDefines_Graphics.NGraphics.RESOURCE_MAP_ICON_TEXT_CUTOFF = 2500						--base is 800
NDefines_Graphics.NGraphics.UNITS_DISTANCE_CUTOFF = 400							--base is 120
NDefines_Graphics.NGraphics.SHIPS_DISTANCE_CUTOFF = 720							--base is 240
NDefines_Graphics.NGraphics.LAND_COMBAT_DISTANCE_CUTOFF = 2250						--base is 1500
NDefines_Graphics.NGraphics.PROV_CONSTRUCTION_ICON_DISTANCE_CUTOFF = 1200				--base is 400
NDefines_Graphics.NGraphics.STATE_CONSTRUCTION_ICON_DISTANCE_CUTOFF = 2200				--base is 800
NDefines_Graphics.NGraphics.UNITS_ICONS_DISTANCE_CUTOFF = 2250						--base is 900
NDefines_Graphics.NGraphics.UNIT_ARROW_DISTANCE_CUTOFF = 2250						--base is 875
NDefines_Graphics.NGraphics.CAPITAL_ICON_CUTOFF = 2250							--base is 1100
NDefines_Graphics.NGraphics.DECISION_MAP_ICON_DISTANCE_CUTOFF = 2500					--base is 1000
NDefines_Graphics.NGraphics.RESISTANCE_MAP_ICON_MODIFIERS_DISTANCE_CUTOFF = 1800			--base is 500
NDefines_Graphics.NGraphics.RESISTANCE_MAP_ICON_DISTANCE_CUTOFF = 2500					--base is 1200	

NDefines_Graphics.NGraphics.MAX_NUMBER_OF_TEXTURES = 20000	
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_REFRESH_FREQ = 0.2
NDefines_Graphics.NGraphics.BORDER_WIDTH = 1 --vanilla 1.5
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_FIELD_COUNTRY_REFRESH = 25 --vanilla 10
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_THICKNESS_COUNTRY_HIGH = 20 --vanilla 25
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_COUNTRY_CENTER_THICKNESS = 1.75 --vanilla 2
NDefines_Graphics.NGraphics.MAX_MESHES_LOADED_PER_FRAME = 5
NDefines_Graphics.NGraphics.ADJACENCY_RULE_DISTANCE_CUTOFF = 1200
NDefines_Graphics.NGraphics.LAND_COMBAT_DISTANCE_CUTOFF = 1200
NDefines_Graphics.NGraphics.SUPPLY_ICON_CUTOFF = 1500
NDefines_Graphics.NGraphics.MAPICON_GROUP_PASSES = 5
NDefines_Graphics.NGraphics.ROOT_FRONT_OFFSET = 2

NDefines_Graphics.NMapMode.MAP_MODE_MANPOWER_RANGE_MAX = 5000000				--base is 20000000

--Gameplay Changes (taken from high performance mods, adjusted for ATD) (Paul_)
NDefines.NGame.LAG_DAYS_FOR_LOWER_SPEED = 15
NDefines.NGame.LAG_DAYS_FOR_PAUSE = 30

NDefines.NMilitary.COMBAT_MINIMUM_TIME = 1  -- affects micro, much smoother

NDefines.NDiplomacy.BASE_SEND_ATTACHE_COST = 50     --100
NDefines.NDiplomacy.BASE_SEND_ATTACHE_CP_COST = 10.0    --50
NDefines.NCountry.SPECIAL_FORCES_CAP_BASE = 0.1 --0.05

NDefines.NOperatives.AGENCY_CREATION_DAYS = 0   --30
NDefines.NOperatives.AGENCY_CREATION_FACTORIES = 0  --5
NDefines.NOperatives.AGENCY_UPGRADE_DAYS = 30   --30
NDefines.NOperatives.AGENCY_OPERATIVE_RECRUITMENT_TIME = 30  --30
NDefines.NOperatives.BECOME_SPYMASTER_PP_COST = 25   --50
NDefines.NOperatives.MAX_OPERATIVE_SLOT_FROM_AGENCY_UPGRADES = 2 -- two spies on 6th upgrade base is 1

NDefines.NInterface.MINIMAP_PING_DELAY_BETWEEN_PINGS = 1 --vanilla 0.30 -- delay between consecutive pings


--Air Balance (designer stuff mainly but also some other stuff regarding air combat)

--Stats should no longer be limited. In vanilla 100 stats are max, meaning any extra is wasted. This should make it so no stats are wasted
NDefines.NAir.AIR_WING_MAX_STATS_ATTACK = 200   -- 100
NDefines.NAir.AIR_WING_MAX_STATS_DEFENCE = 200  -- 100
NDefines.NAir.AIR_WING_MAX_STATS_AGILITY = 200  -- 100
NDefines.NAir.AIR_WING_MAX_STATS_BOMBING = 200  -- 100
NDefines.NAir.AIR_WING_MAX_STATS_SPEED = 1200   -- 1000

NDefines.NAir.DETECT_CHANCE_FROM_NIGHT = -0.4   -- -0.2 How much the night can reduce the air detection. (making plane radar more effective)