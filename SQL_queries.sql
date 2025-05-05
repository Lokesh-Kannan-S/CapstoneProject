show tables;
select * from category_table;
select * from complex_table;
select * from competitor_table;

-- category_table

-- 1 
select category_id,category_name,competition_name from category_table;
-- 2
select category_name,count(competition_name) as "Number of Competitions" from category_table group by category_name;
-- 3
select competition_name,`type` from category_table where type = 'doubles';
-- 4
select competition_name,category_name from category_table where category_name='ITF Men';
-- 5
select parent_id,competition_id,competition_name from category_table order by parent_id desc;
-- 6
select `type`, count(competition_name) as "Distribution of Competitions" from category_table group by `type`;
-- 7
select competition_id,competition_name from category_table where parent_id ="N/A";
-- ---------------------------------------------------------------------------------------------------------------------------------------

-- complex_table

-- 1
select venue_name,complex_name from complex_table;
-- 2
select complex_name,count(venue_name) from complex_table group by complex_name;
-- 3
select venue_id,venue_name,city_name from complex_table where country_name ='Chile';
-- 4 
select venue_name,timezone from complex_table;
-- 5
select complex_name, count(venue_name) as "venue count" from complex_table group by complex_name having count(venue_name) > 1;
-- 6
select country_name, group_concat(venue_name) as "venues name" from complex_table group by country_name;
-- 7
select complex_name, (venue_name) from complex_table where complex_name = 'Nacional';
-- ------------------------------------------------------------------------------------------------------------------------------------------

-- competitor_table

-- 1
select `name`,`rank`,points from competitor_table;
-- 2
select `name`,`rank` from competitor_table order by `rank` asc limit 5;
-- 3
select `name` as "competitor_with_stable_rank" from competitor_table where movement = 0;
-- 4
select country,sum(points) as "Total points" from competitor_table where country = 'Croatia';
-- for all countires
select country, sum(points) as "Total points" from competitor_table group by country;
-- 5
select country,count(`name`) as "Competitors" from competitor_table group by country;
-- 6
select `name`,points from competitor_table order by points desc limit 7;
