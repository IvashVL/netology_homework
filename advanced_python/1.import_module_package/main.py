from datetime import datetime as d
from application.salary import calculate_salary
from application.db.people import get_employees


if __name__ == '__main__':
    print(d.now().date())
    calculate_salary()
    get_employees()
