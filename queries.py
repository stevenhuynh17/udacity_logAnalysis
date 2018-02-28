#!/usr/bin/env python

import psycopg2


def display(data, unit):
    for output in data:
        column_1 = output[0]
        column_2 = output[1]

        print '{column_1} --- {column_2}{unit}'.format(column_1=column_1,
                                                       column_2=column_2,
                                                       unit=unit)
    print '\n'


def popular_article():
    query = """
            select articles.title, count(*) as views
            from log, articles
            where substring(path from 10 for length(path))=articles.slug
            group by title
            order by views
            desc limit 3;
            """
    print '>>> MOST POPULAR THREE ARTICLES:'
    display(get_query_results(query), ' views')


def popular_author():
    query = """
            select name, sum(views) as total
            from authors,
                (select articles.author, articles.title, count(*) as views
                from log, articles
                where substring(path from 10 for length(path))=articles.slug
                group by articles.title, articles.author
                order by views) as artViews
            where authors.id=artViews.author
            group by name
            order by total desc;
            """
    print '>>> MOST POPULAR AUTHOR:'
    display(get_query_results(query), ' views')


def request_errors():
    query = """
            select *
            from
                (select total.date,
                    cast(cast(fails.fails as float)/cast(total.total as float)
                    * 100 as decimal(10,2)) as percent
                from
                    (select to_char(time, 'FMMonth FMDD, YYYY') as date,
                        count(*) as total
                    from log
                    group by date) as TOTAL,
                    (select to_char(time, 'FMMonth FMDD, YYYY') as date,
                        count(*) as fails
                    from log
                    where status not like '200 OK'
                    group by date) as fails
                where total.date=fails.date) as test
            where percent > 1.0;
            """
    print '>>> REQUEST ERROR > 1%:'
    display(get_query_results(query), '%' + ' errors')


def get_query_results(query):
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    popular_article()
    popular_author()
    request_errors()
