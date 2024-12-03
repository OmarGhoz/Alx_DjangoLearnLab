#include <iostream>
using namespace std;

int main() {
    float salary, net_salary;

    cout << "Enter your salary: ";
    cin >> salary;

    net_salary = salary - (salary * 0.10);
    cout << "The net salary: " << net_salary << endl;

    return 0;
}
