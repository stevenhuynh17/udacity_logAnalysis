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
    db = psycopg2.connect("dbname='news'")
    cur = db.cursor()

    query = """
            select articles.title, count(*) as views
            from log, articles
            where substring(path from 10 for length(path))=articles.slug
            group by title
            order by views
            desc limit 3;
            """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    db.close()

    print '>>> MOST POPULAR THREE ARTICLES:'
    display(data, ' views')


def popular_author():
    db = psycopg2.connect("dbname='news'")
    cur = db.cursor()

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
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    db.close()

    print '>>> MOST POPULAR AUTHOR:'
    display(data, ' views')


def request_errors():
    db = psycopg2.connect("dbname='news'")
    cur = db.cursor()

    query = """
            select *
            from
                (select total.date,
                    cast(cast(fails.fails as float)/cast(total.total as float)
                    * 100 as decimal(10,2)) as percent
                from
                    (select substring(cast(time as text) for 10) as date,
                        count(*) as total
                    from log
                    group by date) as TOTAL,
                    (select substring(cast(time as text) for 10) as date,
                        count(*) as fails
                    from log
                    where status not like '200 OK'
                    group by date) as fails
                where total.date=fails.date) as test
            where percent > 1.0;
            """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    db.close()

    print '>>> REQUEST ERROR > 1%:'
    display(data, '%' + ' errors')


try:
    popular_article()
    popular_author()
    request_errors()
except Exception as e:
    print('FAILURE TO CONNECT\n')
    print(e)
