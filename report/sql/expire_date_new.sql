SELECT prod_id, sale_date as start_date, DATE_ADD(sale_date, INTERVAL '$interval' MONTH) as end_date
        FROM sales
        where sale_date = '$order_id';