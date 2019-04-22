use sakila;

-- 1a Display the first and last names of all actors from the table actor.
SELECT first_name, last_name
	FROM actor;

-- 1b Display the first and last name of each actor in a single column in upper case letters. 
--    Name the column Actor Name.
 SELECT CONCAT(first_name,' ', last_name) AS Actor_Name 
	FROM actor;

-- 2a Find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
SELECT actor_id, first_name, last_name
	FROM actor
WHERE first_name = 'Joe';

-- 2b Find all actors whose last name contain the letters GEN.
SELECT first_name, last_name
	FROM actor
WHERE last_name like '%GEN%';

--  2c. Find all actors whose last names contain the letters LI. 
--      This time, order the rows by last name and first name, in that order:
select last_name, first_name
	from actor 
where last_name like '%LI%';

-- 2d Using IN, display the country_id and country columns of the following countries 
--    Afghanistan, Bangladesh, and China.
SELECT 
    country_id, country
FROM
    country
WHERE
    country IN ('Afghanistan' , 'Bangladesh', 'China');

-- 3a You want to keep a description of each actor. 
--    You don't think you will be performing queries on a description, 
--    so create a column in the table actor named description and use the data type BLOB.
ALTER TABLE sakila.actor
	add description BLOB;
SELECT * from actor LIMIT 3;

-- 3b Delete the description column.
alter table actor drop column description;
SELECT * from actor LIMIT 3;

-- 4a List the last names of actors, as well as how many actors have that last name.
select last_name, count(last_name)
	from actor
group by last_name;
  -- query to check results of above^^^
select last_name, first_name
	from actor
where last_name = 'akroyd';

-- 4b List last names of actors and the number of actors who have that last name, 
--     but only for names that are shared by at least two actors.
select last_name, count(last_name)
	from actor
group by last_name
having count(last_name) >1;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. 
--    Write a query to fix the record.
update actor
	set first_name = 'Harpo'
where first_name = 'Groucho';
-- Groucho appeared more than once in the table. 
-- The above query modified all three. Must reset table using the inverse. 
update actor
	set first_name = 'Groucho'
where first_name = 'Harpo';
-- check the reset
select first_name, last_name
	from actor 
where first_name = 'Groucho';

-- set correct only the Groucho Williams entry.
update actor
	set first_name = 'Harpo'
where first_name = 'Groucho' and last_name = 'Williams';
-- check result
select first_name, last_name
	from actor
where first_name = 'Groucho' or first_name = 'Harpo';

-- 4d In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
update actor
	set first_name = 'Groucho'
where first_name = 'Harpo' and last_name = 'Williams';
-- check results
select first_name 
	from actor 
where first_name in ('Harpo', 'Groucho');

-- 5a You cannot locate the schema of the address table. Which query would you use to re-create it?
select *
	from address;
-- solution 2
SELECT *
	FROM INFORMATION_SCHEMA.TABLES
WHERE tables.table_name like '%address%';
--solution 3
show columns 
	from address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. 
--     Use the tables staff and address:
SELECT s.first_name, s.last_name, a.address
	FROM staff s 
		LEFT JOIN address a 
			ON s.address_id = a.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. 
--     Use tables staff and payment.
select * from payment;
select CONCAT(s.first_name,' ', s.last_name) AS Staff_Name, sum(p.amount) as 'Total Transactions'
	from payment p
		join staff s
		on p.staff_id = s.staff_id
where p.payment_date between '2005-08-01' and '2005-08-31'
group by p.staff_id; 
-- alternate method
select CONCAT(s.first_name,' ', s.last_name) AS Staff_Name, sum(p.amount) as 'Total Transactions'
	from payment p
		join staff s
			on p.staff_id = s.staff_id
where p.payment_date like '2005-08%'
group by p.staff_id; 

-- 6c. List each film and the number of actors who are listed for that film. 
--     Use tables film_actor and film. Use inner join.
select f.title, count(fa.actor_id) as 'Actor Count'
	from film_actor fa
		inner join film f
			on fa.film_id = f.film_id
group by fa.film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
select f.title, count(i.film_id) as 'Inv Count'
	from inventory i
		join film f
			on i.film_id = f.film_id
where f.title like '%Hunchback Impossible%'; 

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer.
--    List the customers alphabetically by last name:
select c.first_name,c.last_name, sum(p.amount) as  'Total Paid'
	from payment p
		join customer c
			on p.customer_id = c.customer_id
group by p.customer_id
order by c.last_name asc;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
--     As an unintended consequence, films starting with the letters K and Q have also soared in popularity.
--     Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
select title
	from film
where language_id in ( select language_id
							from language
                        where language.name like '%English%') and title like'k%' or title like 'q%';
                        
-- check results. the language_id for English = 1
select title, language_id
	from film
where title like 'K%';

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
select first_name
	from actor
where actor.actor_id in (
						select actor_id
							from film_actor
						where film_actor.film_id in ( 
                             select film_id
								from film
							where film.title like '%Alone Trip%'
                        ));	

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. 
--     Use joins to retrieve this information.
select CONCAT(cust.first_name,' ', cust.last_name) AS Customer_Name, cust.email, cntry.country
	from customer cust
		join address addy
			on cust.address_id = addy.address_id
		join city cty
			on addy.city_id = cty.city_id
		join country cntry
			on cty.country_id = cntry.country_id
where cntry.country like '%Canada%'
order by Customer_Name asc;    
-- result
-- DERRICK	DERRICK.BOURQUE@sakilacustomer.org
-- DARRELL	DARRELL.POWER@sakilacustomer.org
-- LORETTA	LORETTA.CARPENTER@sakilacustomer.org
-- CURTIS	CURTIS.IRBY@sakilacustomer.org
-- TROY	TROY.QUIGLEY@sakilacustomer.org
-- check results
select country_id, country
from country
where country like '%Canada%';
-- canada country id = 20
select address_id
from customer 
where first_name in ('DERRICK','DARRELL','LORETTA','CURTIS','TROY');
-- result 193 415 441 468 481
select city_id
from address
where address_id in ('193', '415', '441', '468', '481');
-- result 383 430 565 196 179
select country_id
from city
where city_id in ('383', '430', '565', '196', '179');
-- result 20, 20, 20, 20, 20 

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
--     Identify all movies categorized as family films.
select film.title, film.rating, filmcat.category_id, cat.name
	from film
		join film_category filmcat
			on film.film_id = filmcat.film_id
		join category cat
			on filmcat.category_id = cat.category_id
where cat.name like '%Family%'
order by film.title asc;

-- 7e. Display the most frequently rented movies in descending order.
select rent_count.title, count(rent_count.rents_inv_loc) as rental_count
from
	(select film.title, count(rent.inventory_id) as rents_inv_loc
		from rental rent
	join inventory i
		on rent.inventory_id = i.inventory_id
	join film
		on i.film_id= film.film_id
	group by rent.inventory_id) rent_count
group by rent_count.title
order by rental_count desc;
    
-- 7f. Write a query to display how much business, in dollars, each store brought in.
select s.store_id, sum(p.amount)
from payment p
	join rental r
		on p.rental_id = r.rental_id
	join inventory i 
		on r.inventory_id = i.inventory_id
	join store s
		on i.store_id = s.store_id
group by s.store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
select s.store_id, cty.city, cntry.country
from store s
	join address a
		on s.address_id = a.address_id
	join city cty
		on a.city_id = cty.city_id
	join country cntry
		on cty.country_id = cntry.country_id;

-- 7h. List the top five genres in gross revenue in descending order. 
--     (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
-- checking to see if one payment covers multiple rentals. 1:1 relation.
select payment_id, count(rental_id)
	from payment
group by payment_id;
-- checking the inverse of above^^^. If one rental can have multiple payments. 1:1 relation.
select rental_id, count(payment_id)
	from payment
group by rental_id;
-- Solution query
select cat.name,cat.category_id, sum(p.amount) as Gross_Revenue
	from payment p
		join rental r
			on p.rental_id = r.rental_id
		join inventory i
			on r.inventory_id = i.inventory_id
		join film_category filmcat
			on i.film_id = filmcat.film_id
		join category cat
			on filmcat.category_id = cat.category_id
	group by cat.category_id
	order by Gross_Revenue desc limit 5;


-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
--     Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
create view Top_Five_Genres as
	select cat.name,cat.category_id, sum(p.amount) as Gross_Revenue
		from payment p
			join rental r
				on p.rental_id = r.rental_id
			join inventory i
				on r.inventory_id = i.inventory_id
			join film_category filmcat
				on i.film_id = filmcat.film_id
			join category cat
				on filmcat.category_id = cat.category_id
	group by cat.category_id
	order by Gross_Revenue desc limit 5;

-- 8b. How would you display the view that you created in 8a?
select * 
	from top_five_genres;
    
-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view top_five_genres;








