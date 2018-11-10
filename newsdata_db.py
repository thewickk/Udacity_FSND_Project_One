#!/usr/bin/env python3
import psycopg2


DBNAME = "news"


def fsnd_project_1():
    # Create database connection:
    db = psycopg2.connect(database=DBNAME)

    # If connection to database is successful execute queries:
    if (db):
        print("You are successfully connected "
              "to the {} database!\n".format(DBNAME))

        # Create cursor for database interaction:
        c = db.cursor()

        # Solution to question 1:
        top_three_articles = """
        SELECT * FROM top_three_articles;
        """
        c.execute(top_three_articles)
        print("***Question 1: Top 3 Most Popular Articles***")
        for(article, view) in c.fetchall():
            print("\t\"{}\" - {} views".format(article, view))
        print("\n")

        # Solution to question 2:
        most_popular_authors = """
        SELECT * FROM top_authors;
        """
        c.execute(most_popular_authors)
        print("***Question 2: Most Popular Article Authors of All-Time***")
        for(author, view) in c.fetchall():
            print("\t{} - {} views".format(author, view))
        print("\n")

        # Solution to question 3:
        percent_error = """
        SELECT * FROM percent_error
        WHERE percent_error."Percent Error(%)" > '1';
        """
        c.execute(percent_error)
        print("***Question 3: Days With Greater Than One Percent \"404 NOT "
              "FOUND\" "
              "Errors***")
        for(date, error) in c.fetchall():
            print("\t{} - {:1.1f}% errors".format
                  (date.strftime('%B %d, %Y'), error))


        # Close database connection:
        db.close()

    # Else if database connection fails, display failed to connect message
    else:
        print("Failed to connect to the database")


if __name__ == "__main__":
    fsnd_project_1()
