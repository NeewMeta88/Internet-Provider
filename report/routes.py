import os
from access import login_required, group_required

from flask import (
    Blueprint, render_template,
    request, current_app,
    session, redirect, url_for
)

from database.operations import select, insert, delete, check, call_proc, exists
from database.sql_provider import SQLProvider

blueprint_report = Blueprint(
    'blueprint_report',
    __name__,
    template_folder='templates',
    static_folder='static'
)

blueprint_check = Blueprint(
    'blueprint_check',
    __name__,
    template_folder='templates',
    static_folder='static'
)

blueprint_report_view = Blueprint(
    'blueprint_report_view',
    __name__,
    template_folder='templates',
    static_folder='static'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/add', methods=['GET', 'POST'])
@group_required
def add_item():
    if request.method == 'GET':

        return render_template('add_item.html')
    else:
        prod_name = request.form.get('item_name')
        prod_price = request.form.get('item_price')
        sql = provider.get('add.sql', prod_name=prod_name, prod_price=int(prod_price))
        insert(sql)

        return render_template('success_add.html')


@blueprint_report.route('/remove', methods=['GET', 'POST'])
@group_required
def remove_item():
    # db_config = current_app.config['db_config']
    if request.method == 'GET':

        return render_template('remove_item.html')
    else:
        prod_name = request.form.get('item_name')

        sql = provider.get('remove.sql', prod_name=prod_name)
        # sql2 = provider.get('check.sql', prod_name=prod_name)
        #
        # items = select(db_config, sql2)
        #
        # # a = check(sql2)
        # print(items)

        delete(sql)

        return render_template('success_add.html')
        # else:
        #
        #     return render_template('remove_item.html', message='Товар не найден')


@blueprint_check.route('/')
@group_required
def check_item():
    db_config = current_app.config['db_config']

    sql = provider.get('all_items.sql')
    items = select(db_config, sql)

    return render_template('check_item.html', items=items)


@blueprint_report_view.route('/', methods=['GET', 'POST'])
@group_required
def view_report():
    if request.method == 'GET':
        db_config = current_app.config['db_config']

        sql3 = provider.get('available_date.sql')
        available = select(db_config, sql3)
        return render_template('view_report.html', available=available)
    else:
        db_config = current_app.config['db_config']

        year = request.form.get('year')
        month = request.form.get('month')
        print("year =",year)
        print("month =",month)

        sql3 = provider.get('available_date.sql')
        available = select(db_config, sql3)
        print(available)

        sql2 = provider.get('no_such_order.sql', year=year, month=month)
        dates = select(db_config, sql2)

        sql = provider.get('view_reports.sql', year=year, month=month)
        items = select(db_config, sql)

        return render_template('view_report.html', available=available, items=items, dates=dates, message='По указанной дате нет отчетов!')

@blueprint_report_view.route('/active', methods=['GET', 'POST'])
@group_required
def view_active():
    if request.method == 'GET':
        db_config = current_app.config['db_config']

        sql1 = provider.get('order_id.sql', )
        order_id = select(db_config, sql1)[0]['max(sale_date)']

        sql2 = provider.get('expire_date.sql', order_id=order_id)
        items = select(db_config, sql2)

        return render_template('market/active.html', items=items)


# @blueprint_report_view.route('/active', methods=['GET', 'POST'])
# @group_required
# def view_active():
#     if request.method == 'GET':
#         db_config = current_app.config['db_config']
#
#         sql1 = provider.get('order_id.sql', )
#         order_id = select(db_config, sql1)[0]['max(sale_date)']
#
#         sql2 = provider.get('expire_date.sql', order_id=order_id)
#         items = select(db_config, sql2)
#
#         return render_template('active.html', items=items)
#     else:
#         db_config = current_app.config['db_config']
#
#         sql1 = provider.get('order_id.sql', )
#         order_id = select(db_config, sql1)[0]['max(sale_date)']
#
#         sql3 = provider.get('interval.sql', interval=request.form.get('year'), order_id=order_id)
#         insert(sql3)
#         sql4 = provider.get('interval_id', order_id=order_id)
#         interval = select(db_config, sql4)[0]['interval_num']
#         print(interval)
#
#         sql2 = provider.get('expire_date_new.sql', order_id=order_id, interval=interval)
#         items = select(db_config, sql2)
#
#         return render_template('active.html', items=items)


@blueprint_report_view.route('/create', methods=['GET', 'POST'])
@group_required
def create_report():
    if request.method == 'GET':
        return render_template('create_report.html')
    else:
        db_config = current_app.config['db_config']
        rep_year = request.form.get('year')
        rep_month = request.form.get('month')

        sql1 = provider.get('exists.sql', year=request.form.get('year'), month=request.form.get('month'))
        sql2 = provider.get('no_such_order.sql', year=request.form.get('year'), month=request.form.get('month'))

        items = select(db_config, sql1)
        dates = select(db_config, sql2)

        call_proc('generate_report', rep_month, rep_year)
        return render_template('exists.html', items=items, dates=dates)
