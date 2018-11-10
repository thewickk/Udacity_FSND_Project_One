# Udacity_FSND_Project_One

### This is the Log Analysis Project from the Udacity Full Stack Web Developer Nanodegree Program


## Create Views

-Please use the following Views in order to successuflly run the queries contained in the newsdata_db.py Python file.

### View to List Author, Title, and Slug for Articles

CREATE VIEW article_summary AS
SELECT
authors.name AS "Article Author",
articles.title AS "Article Title",
articles.slug AS "Article Slug"
FROM articles
JOIN authors
ON articles.author = authors.id
ORDER BY authors.name;

### View to Seperate Slug from log.path
Ex /article/goats-eat-googles --> goats-eat-googles

CREATE VIEW slug_from_path AS
SELECT
articles.slug
FROM
articles
JOIN log ON substr(log.path, length('/article/')+1) = articles.slug;



### View of Number of Views per Date:

CREATE VIEW total_views_by_date AS
SELECT date(time) AS "Date Viewed", COUNT(*) AS "Number of Views"
FROM log
GROUP BY date(time)
ORDER BY date(time);


### View of Views per Slug
CREATE VIEW slug_and_count AS
SELECT slug AS "Article Slug", COUNT(*) AS "Article View Count"
FROM slug_from_path
GROUP BY slug
ORDER BY "Article View Count" DESC;


### View To Find and Count 404 Errors

CREATE VIEW not_found_error AS
SELECT date(time) AS "Date", COUNT(*) AS "404 Errors"
FROM log
WHERE status LIKE '%404%'
GROUP BY date(time)
ORDER BY date(time);



### View To Find Percent of 404 Errors That Occured

CREATE VIEW percent_error AS
SELECT
not_found_error."Date", (100.00*not_found_error."404 Errors"/total_views_by_date."Number of Views")
AS "Percent Error(%)"
FROM not_found_error
JOIN total_views_by_date
ON not_found_error."Date" = total_views_by_date."Date Viewed"
ORDER BY not_found_error."Date";


### View For Solution to Question 1: What are the most popular three articles of all time?

CREATE VIEW top_three_articles AS
SELECT
article_summary."Article Title" AS "Top Three Articles",
slug_and_count."Article View Count" AS "Number of Views"
FROM article_summary
JOIN slug_and_count
ON article_summary."Article Slug" = slug_and_count."Article Slug"
ORDER BY slug_and_count."Article View Count" DESC
LIMIT 3;

### View For Solution to Question 2: Who are the most popular article authors of all time?

CREATE VIEW top_authors AS
SELECT
article_summary."Article Author",
SUM(slug_and_count."Article View Count") AS "Total Views"
FROM article_summary
JOIN slug_and_count
ON article_summary."Article Slug" = slug_and_count."Article Slug"
GROUP BY article_summary."Article Author"
ORDER BY "Total Views" DESC;



