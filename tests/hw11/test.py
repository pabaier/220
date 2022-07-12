from pathlib import Path

from assignments.hw11 import sales_person
from helpers import build_test
from tests.hw11.test_data import *
from tests.test_framework import *

person_test_file = Path(os.path.dirname(sales_person.__file__)) / 'sales_person.py'
force_test_file = Path(os.path.dirname(sales_person.__file__)) / 'sales_force.py'


def main():
    test_suit = TestSuit('HW 11')
    sales_person_builder = TestBuilder('Sales Person', person_test_file, 15)
    sales_force_builder = TestBuilder('Sales Force', force_test_file, 16)
    sales_person_builder.add_items(
        build_sales_person_constructor_test(),
        build_sales_person_instance_variables_test(),
        build_sales_person_get_id_test(),
        build_sales_person_get_name_test(),
        build_sales_person_set_name_test(),
        build_sales_person_enter_sale_test(),
        build_sales_person_total_sales_test(),
        build_sales_person_get_sales_test(),
        build_sales_person_met_quota_test(),
        build_sales_person_compare_to_test(),
        build_sales_person_str_test()
    )
    sales_force_builder.add_items(
        build_sales_force_constructor_test(),
        build_sales_force_instance_variables_test(),
        build_sales_force_add_data_test(),
        build_sales_force_quota_report_test(),
        build_sales_force_top_seller_test(),
        build_sales_force_individual_sales_test(),
        build_sales_force_sale_frequencies_test()
    )

    test_suit.add_test_builders(sales_person_builder, sales_force_builder)
    test_suit.run()


def make_sales_person_with_sales(sp_id, sp_name, sale_1, sale_2):
    sales_person = SalesPerson(sp_id, sp_name)
    sales_person.enter_sale(sale_1)
    sales_person.enter_sale(sale_2)
    return sales_person


def build_sales_person_constructor_test():
    return build_test('sales_person_constructor', sales_person_constructor_tests)


def build_sales_person_instance_variables_test():
    return build_test('sales_person_instance_variables', sales_person_instance_variables_tests)


def build_sales_person_get_id_test():
    return build_test('sales_person_get_id', sales_person_get_id_test)


def build_sales_person_get_name_test():
    return build_test('sales_person_get_name', sales_person_get_name_test)


def build_sales_person_set_name_test():
    return build_test('sales_person_set_name', sales_person_set_name_test)


def build_sales_person_enter_sale_test():
    return build_test('sales_person_enter_sale', sales_person_enter_sale_test)


def build_sales_person_total_sales_test():
    return build_test('sales_person_total_sales', sales_person_total_sales_test)


def build_sales_person_get_sales_test():
    return build_test('sales_person_get_sales', sales_person_get_sales_test)


def build_sales_person_met_quota_test():
    return build_test('sales_person_met_quota', sales_person_met_quota_test)


def build_sales_person_compare_to_test():
    return build_test('sales_person_compare_to', sales_person_compare_to_test)


def build_sales_person_str_test():
    return build_test('sales_person_str', sales_person_str_test)


def build_sales_force_constructor_test():
    return build_test('sales_force_constructor', sales_force_constructor_tests)


def build_sales_force_instance_variables_test():
    return build_test('sales_force_instance_variables', sales_force_instance_variables_tests)


def build_sales_force_add_data_test():
    return build_test('sales_force_add_data', sales_force_add_data_test)


def build_sales_force_quota_report_test():
    return build_test('sales_force_quota_report', sales_force_quota_report_test)


def build_sales_force_top_seller_test():
    return build_test('sales_force_top_seller', sales_force_top_seller_test)


def build_sales_force_individual_sales_test():
    return build_test('sales_force_individual_sales', sales_force_individual_sales_test)


def build_sales_force_sale_frequencies_test():
    return build_test('sales_force_sale_frequencies', sales_force_sale_frequencies_test)


if __name__ == '__main__':
    main()
