def open_sample():
    """
    Opens "employees.csv" file with data of employees
    :return: list of all rows in .csv; each row is a list of values
    """
    import csv
    with open('employees.csv') as f:
        reader = csv.reader(f, delimiter=';')
        return list(reader)


def get_command() -> int:
    """
    Prints instructions for a user and gets input
    :return: code of the command: 0, 1, 2, 3
    """
    command = ''
    flag = False
    while command not in {'0', '1', '2', '3'}:
        if flag:
            print("Ошибка ввода")
        print()
        print("0 - завершить")
        print("1 - вывести все отделы")
        print("2 - вывести сводный отчёт")
        print("3 - сохранить отчёт в .csv")
        command = input()
        flag = True
    return int(command)


def get_units(features: list, employees: list) -> set:
    """
    Extracts all units (отделы) from data
    :param features: list of column names of the table
    :param employees: list of rows; each row is a list of values
    :return: set of strings
    """
    index = features.index("Отдел")
    units = set()
    for row in employees:
        unit = row[index].split(' ->')[0]
        units.add(unit)
    return units


def get_stats(features: list, employees: list, units: set) -> list:
    """
    Collects some statistics from data
    :param features: list of column names of the table
    :param employees: list of rows; each row is a list of values
    :param units: set of strings; can be gotten from get_units()
    :return: list of dicts; each dict is a description of a unit
    """
    stats_features = ["Название", "Численность",
                      "Вилка зарплат", "Средняя зарплата"]
    stats = dict.fromkeys(units)
    for unit in units:
        stats[unit] = dict.fromkeys(stats_features, 0)
        stats[unit]["Название"] = unit
        stats[unit]["Список зарплат"] = []
    for row in employees:
        employee = dict(zip(features, row))
        unit = employee["Отдел"].split(" ->")[0]
        stats[unit]["Численность"] += 1
        salary = int(employee["Оклад"])
        stats[unit]["Список зарплат"].append(salary)
        stats[unit]["Средняя зарплата"] += salary
    for unit in units:
        stats[unit]["Средняя зарплата"] /= stats[unit]["Численность"]
        max_salary = str(max(stats[unit]["Список зарплат"]))
        min_salary = str(min(stats[unit]["Список зарплат"]))
        stats[unit]["Вилка зарплат"] = min_salary + " - " + max_salary
        stats[unit].pop("Список зарплат")
    return list(stats.values())


def save_csv(stats: list):
    """
    Saves statistics in a .csv file
    :param stats: list of dicts; can be gotten from get_stats()
    :return: None
    """
    print("Введите имя файла:")
    name_csv = input()
    import csv
    stats_features = ["Название", "Численность",
                      "Вилка зарплат", "Средняя зарплата"]
    with open(f"{name_csv}.csv", "wt", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(stats_features)
        for unit in stats:
            writer.writerow(unit.values())


def main():
    sample = open_sample()
    features = sample[0]
    employees = sample[1::]
    units = set()
    stats = dict()
    command = -1
    while command:
        command = get_command()
        if command == 1:
            if not units:
                units = get_units(features, employees)
            for unit in units:
                print(unit)
        elif command == 2:
            if not units:
                units = get_units(features, employees)
            if not stats:
                stats = get_stats(features, employees, units)
            print(stats)

        elif command == 3:
            if not units:
                units = get_units(features, employees)
            if not stats:
                stats = get_stats(features, employees, units)
            save_csv(stats)


if __name__ == "__main__":
    main()
