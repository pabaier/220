import os
import random

import helpers

try:
    from assignments.hw11.sales_person import SalesPerson
except:
    SalesPerson = None

try:
    from assignments.hw11.sales_force import SalesForce
except:
    SalesForce = None

from tests.test import Test


def sales_person_constructor_tests():
    return [Test(lambda id, name: SalesPerson(id, name), 'Construct SalesPerson with two parameters', (7, "Alice"),
                 comparator=lambda a, e: True).run()]


def sales_person_instance_variables_tests():
    employee_id = random.randint(1, 100)
    name = helpers.get_random_string()
    tests = [
        Test(lambda i, n: SalesPerson(i, n), f'employee_id instance variable {employee_id}', (employee_id, name),
             comparator=lambda a, e: a.employee_id == employee_id).run(),
        Test(lambda i, n: SalesPerson(i, n), 'employee_id instance variable type int', (employee_id, name),
             comparator=lambda a, e: type(a.employee_id) == int).run(),
        Test(lambda i, n: SalesPerson(i, n), f'name instance variable "{name}"', (employee_id, name),
             comparator=lambda a, e: a.name == name).run(),
        Test(lambda i, n: SalesPerson(i, n), 'name instance variable type string', (employee_id, name),
             comparator=lambda a, e: type(a.name) == str).run()
    ]
    return tests


# methods

def sales_person_get_id_test():
    employee_id = random.randint(1, 100)
    name = helpers.get_random_string()

    return [Test(lambda i, n: SalesPerson(i, n).get_id(), employee_id, (employee_id, name)).run()]


def sales_person_get_name_test():
    employee_id = random.randint(1, 100)
    name = helpers.get_random_string()
    return [Test(lambda i, n: SalesPerson(i, n).get_name(), name, (employee_id, name)).run()]


def sales_person_set_name_test():
    employee_id = random.randint(1, 100)
    name = helpers.get_random_string()
    new_name = helpers.get_random_string()

    def set_name_comp_func(old):
        def cf(a, e):
            old_name = a.name
            a.set_name(e)
            return old_name == old and a.name == e

        return cf

    return [
        Test(lambda i, n: SalesPerson(i, n), new_name, (employee_id, name), comparator=set_name_comp_func(name)).run()]


def sales_person_enter_sale_test():
    def enter_sale_comp_func(a: SalesPerson, e):
        a.enter_sale(e[0])
        a.enter_sale(e[1])
        return a.sales[0] == e[0] and a.sales[1] == e[1]

    sale_amount_1 = random.uniform(0, 100.00)
    sale_amount_2 = random.uniform(0, 100.00)
    return [
        Test(lambda: SalesPerson(7, 'Alice'), (sale_amount_1, sale_amount_2), comparator=enter_sale_comp_func).run()
    ]


def sales_person_total_sales_test():
    sale_amount_1 = random.uniform(0, 100.00)
    sale_amount_2 = random.uniform(0, 100.00)

    def total_sales_comp_func(sale1, sale2):
        def cf(actual, expected):
            actual.sales = [sale1, sale2]
            return actual.total_sales() == expected

        return cf

    total_sales = sale_amount_1 + sale_amount_2
    return [
        Test(lambda: SalesPerson(7, 'Alice'), total_sales,
             comparator=total_sales_comp_func(sale_amount_1, sale_amount_2)).run()
    ]


def sales_person_get_sales_test():
    sale_amount_1 = random.uniform(0, 100.00)
    sale_amount_2 = random.uniform(0, 100.00)

    def get_sales_comp_func(sale1, sale2):
        def cf(actual, expected):
            actual.sales = [sale1, sale2]
            return actual.get_sales() == expected

        return cf

    get_sales_sales = [sale_amount_1, sale_amount_2]
    return [
        Test(lambda: SalesPerson(7, 'Alice'), get_sales_sales,
             comparator=get_sales_comp_func(sale_amount_1, sale_amount_2)).run()
    ]


def sales_person_met_quota_test():
    sale_amount_1 = random.uniform(0, 100.00)
    sale_amount_2 = random.uniform(0, 100.00)

    def met_quota_comp_func(sales, quota):
        def cf(actual, expected):
            actual.sales = sales
            return actual.met_quota(quota) == expected

        return cf

    hit_quota = sale_amount_1 + sale_amount_2 - 0.01
    equal_quota = sale_amount_1 + sale_amount_2
    miss_quota = sale_amount_1 + sale_amount_2 + 0.01

    met_quota_sales = [sale_amount_1, sale_amount_2]
    return [
        Test(lambda: SalesPerson(7, 'Alice'), False, comparator=met_quota_comp_func(met_quota_sales, miss_quota)).run(),
        Test(lambda: SalesPerson(7, 'Alice'), True, comparator=met_quota_comp_func(met_quota_sales, equal_quota)).run(),
        Test(lambda: SalesPerson(7, 'Alice'), True, comparator=met_quota_comp_func(met_quota_sales, hit_quota)).run()
    ]


def sales_person_compare_to_test():
    sale_amount_1 = random.uniform(0, 100.00)
    sale_amount_2 = random.uniform(0, 100.00)

    def compare_to_comp_func(alice_sales, bob_sales):
        def cf(actual, expected):
            alice = actual[0]
            bob = actual[1]
            alice.sales = [alice_sales]
            bob.sales = [bob_sales]
            return alice.compare_to(bob) == expected

        return cf

    alice_total_sales = sale_amount_1 + sale_amount_2
    bob_more_total_sales = alice_total_sales + 0.01
    bob_equal_total_sales = alice_total_sales
    bob_less_than_total_sales = alice_total_sales - 0.01

    return [
        Test(lambda: (SalesPerson(7, 'Alice'), SalesPerson(13, 'Bob')), -1,
             comparator=compare_to_comp_func(alice_total_sales, bob_more_total_sales)).run(),
        Test(lambda: (SalesPerson(7, 'Alice'), SalesPerson(13, 'Bob')), 0,
             comparator=compare_to_comp_func(alice_total_sales, bob_equal_total_sales)).run(),
        Test(lambda: (SalesPerson(7, 'Alice'), SalesPerson(13, 'Bob')), 1,
             comparator=compare_to_comp_func(alice_total_sales, bob_less_than_total_sales)).run()
    ]


def sales_person_str_test():
    sale_amount_1 = random.uniform(0, 100.00)
    sale_amount_2 = random.uniform(0, 100.00)

    name = helpers.get_random_string()
    emp_id = random.randint(1, 100)

    def str_comp_func(sales):
        def cf(actual: SalesPerson, expected):
            actual.sales = [sales]
            actual_string: str = actual.__str__()
            return actual_string.replace(' ', '') == expected.replace(' ', '')

        return cf

    return [Test(lambda e, n: SalesPerson(e, n), f'{emp_id}-{name}: {sale_amount_1 + sale_amount_2}', (emp_id, name),
                 comparator=str_comp_func(sale_amount_1 + sale_amount_2)).run()]


def sales_force_constructor_tests():
    return [Test(lambda: SalesForce(), 'Construct SalesForce with no parameters', comparator=lambda a, e: True).run()]


def sales_force_instance_variables_tests():
    return [Test(lambda: SalesForce(), 'sales_people list instance variable',
                 comparator=lambda a, e: type(a.sales_people) == list).run()]


# methods
# add data
def sales_force_add_data_test():
    sales_data = build_sales_data(5)
    file_name = 'test_hw10_data_b02fce0e'
    write_sales_data(sales_data, file_name)

    def comp_func(file, s_data):
        def cf(actual: SalesForce, expected):
            actual.add_data(file)
            for i, data in enumerate(s_data):
                seller = actual.sales_people[i]
                if not (seller.employee_id == data[0] and seller.name == data[1] and seller.sales == data[2]):
                    os.remove(file_name)
                    return False
            os.remove(file_name)
            return True

        return cf

    return [Test(lambda: SalesForce(), f'imports sales data {sales_data}',
                 comparator=comp_func(file_name, sales_data)).run()]


# quota report
def sales_force_quota_report_test():
    tests = []
    quota = random.randint(200, 700)
    sales_force_amount = 5
    quota_sales_force_data_expected = build_sales_data(sales_force_amount)

    def comp_func(i):
        def cf(actual, expected):
            quota_sales_force = get_full_sales_force(expected)
            quota_report_actual = quota_sales_force.quota_report(actual)
            total_sales = sum(quota_sales_force_data_expected[i][2])
            id_check = quota_report_actual[i][0] == quota_sales_force_data_expected[i][0]
            name_check = quota_report_actual[i][1] == quota_sales_force_data_expected[i][1]
            total_sales_check = quota_report_actual[i][2] == total_sales
            hit_quota_check = quota_report_actual[i][3] == (total_sales >= actual)
            return id_check and name_check and total_sales_check and hit_quota_check

        return cf

    for j in range(sales_force_amount):
        tests.append(
            Test(lambda: quota, quota_sales_force_data_expected, comparator=comp_func(j)).run()
        )
    return tests


# top seller
def sales_force_top_seller_test():
    tests = []

    # top_seller one
    top_seller_sales_force_data = build_sales_data(5)

    def comp_func(actual, expected):
        expected_top_seller = SalesPerson(701, helpers.get_random_full_name())
        top_seller_sales = random.randint(7000, 80000)
        expected_top_seller.enter_sale(top_seller_sales)
        top_seller_sales_force = get_full_sales_force(expected)
        top_seller_sales_force.sales_people.append(expected_top_seller)
        return top_seller_sales_force.top_seller() == [expected_top_seller]

    tests.append(
        Test(lambda: "Wrong Top Seller", top_seller_sales_force_data, comparator=comp_func).run()
    )

    # top_seller many
    top_seller_many_sales_force_data = build_sales_data(5)

    def many_comp_func(actual, expected):
        expected_top_seller_many = SalesPerson(701, helpers.get_random_full_name())
        expected_top_seller_many.enter_sale(random.randint(7000, 80000))
        top_seller_many_sales_force = get_full_sales_force(expected)
        top_seller_many_sales_force.sales_people.append(expected_top_seller_many)
        top_seller_many_sales_force.sales_people.append(expected_top_seller_many)
        return top_seller_many_sales_force.top_seller() == [expected_top_seller_many, expected_top_seller_many]

    tests.append(
        Test(lambda: "Wrong top sellers", top_seller_many_sales_force_data, comparator=many_comp_func).run()
    )

    return tests


def sales_force_individual_sales_test():
    tests = []
    employee_id = random.randint(1, 50)

    def comp_func(actual, expected):
        emp_id, exists = expected
        individual_seller_one = SalesPerson(emp_id, helpers.get_random_full_name())
        individual_seller_sales_force = get_full_sales_force(build_sales_data(5))
        individual_seller_sales_force.sales_people.insert(
            random.randrange(0, len(individual_seller_sales_force.sales_people)), individual_seller_one)
        if exists:
            return individual_seller_sales_force.individual_sales(emp_id) == individual_seller_one
        return individual_seller_sales_force.individual_sales(emp_id + 1) is None

    return [
        Test(lambda: f'employee {employee_id} does not exist but should', (employee_id, True),
             comparator=comp_func).run(),
        Test(lambda: f'employee {employee_id + 1} exists but should not', (employee_id, False),
             comparator=comp_func).run()
    ]


def sales_force_sale_frequencies_test():
    sale_frequencies_data = build_sale_frequencies_data(5)
    vals = []
    counts = []
    for person in sale_frequencies_data:
        sales = person[2]
        for sale in sales:
            if sale in vals:
                location = vals.index(sale)
                counts[location] += 1
            else:
                vals.append(sale)
                counts.append(1)
    expected_values = {key: value for (key, value) in zip(vals, counts)}
    tests = []

    def comp_func(data, key):
        def cf(actual, expected):
            sale_frequencies_sales_force = get_full_sales_force(data)
            result = sale_frequencies_sales_force.get_sale_frequencies()
            return expected == result[key]

        return cf

    for key, value in expected_values.items():
        tests.append(
            Test(lambda: 'Incorrect Frequency', value, comparator=comp_func(sale_frequencies_data, key)).run()
        )
    return tests


# helpers
def get_full_sales_force(data):
    sf = SalesForce()
    for d in data:
        person = SalesPerson(d[0], d[1])
        person.sales = d[2]
        sf.sales_people.append(person)
    return sf


def build_sales_data(number_of_sales_people):
    """
    returns a list of sales people (no ids are less than 100)
    [
        [id, name, sales]
    ]
    """
    data = []
    for i in range(1, number_of_sales_people + 1):
        id = random.randint(i * 100 + 1, i * 100 + 100)
        name = helpers.get_random_full_name()
        sales_count = random.randint(1, 5)
        sales = []
        for j in range(sales_count):
            sales.append(round(random.uniform(100, 500), 2))
        data.append([id, name, sales])
    return data


def write_sales_data(data, file_name):
    with open(file_name, 'w') as test_data_file:
        for person in data:
            id = str(person[0])
            name = person[1]
            sales = ' '.join(map(str, person[2]))
            test_data_file.write(f'{id}, {name}, {sales}\n')


def build_sale_frequencies_data(number_of_sales_people):
    data = build_sales_data(number_of_sales_people)
    possible_sales_count = 10
    possible_sales = []
    for i in range(possible_sales_count):
        possible_sales.append(round(random.uniform(100, 500), 2))
    for person in data:
        sales = person[2]
        for i in range(len(sales)):
            sales[i] = random.choice(possible_sales)
    return data
