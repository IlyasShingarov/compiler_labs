import os

from finite_automata import FiniteAutomata
from syntax_tree import SyntaxTree
from pprint import pprint
from graphviz import Digraph


def check_expression(expression, automata: FiniteAutomata):
    state = automata.start[0]
    print(f'Текущее состояние: {state}')
    for c in expression:
        print(state, c)
        if (state, c) not in automata.transitions:
            print(f'Нет перехода из {state} по {c}')
            return False
        state = automata.transitions[(state, c)][0]
        print(f'Новое состояние {state}')
    result = state in automata.end
    if not result:
        print('Автомат не дошел до конечного состояния.\n')
    else:
        print(f'Автомат допускает слово {expression}.\n')
    return result


def main_test():
    # expression = '(a|b)*abb#'
    # expression = '(a|b)*aabb#'
    # tree = SyntaxTree(expression)
    # tree.print_tree()
    # d_finite_automata = FiniteAutomata.from_tree(tree)
    # d_finite_automata.graph.view(filename='dfa0')
    # print('\n\n')
    # pprint(f'start - {d_finite_automata.start}')
    # pprint(f'end - {d_finite_automata.end}')
    # pprint(f'transitions')
    # pprint(d_finite_automata.transitions)
    # d_finite_automata = d_finite_automata.rename_nodes()
    # d_finite_automata.graph.view(filename='dfa1')
    #
    # min_1_dfa = (d_finite_automata
    #              .reverse()
    #              .to_dfa())
    #
    # min_1_dfa.graph.view(filename='min_1_dfa')
    #
    # min_2_dfa = (min_1_dfa
    #              .rename_nodes()
    #              .reverse()
    #              .to_dfa()
    #              .rename_nodes())
    #
    # min_2_dfa.graph.view(filename='min_2_dfa')

    # print()
    # print(check_expression('aaaaabb', min_2_dfa))
    # print()
    # print(check_expression('baaaabb', min_2_dfa))
    # print()
    # print(check_expression('babababb', min_2_dfa))
    # print()
    # print(check_expression('aaaaaba', min_2_dfa))

    # expression = '((0110)|(1001)|(1010)|(0101)|(11)|(00))*1((0110)|(1001)|(1010)|(0101)|(11)|(00))*#'
    # expression = '((0110)|(1001)|(1010)|(0101)|(11)|(00))*#'
    # expression = '((0|1)(0|1)(0|1))*#'
    # expression = '((000*)|1)*#'
    expression = '(a|b)*abb#'

    tree = SyntaxTree(expression)
    tree.print_tree()
    d_finite_automata = FiniteAutomata.from_tree(tree)
    # d_finite_automata.graph.view()

    d_finite_automata = d_finite_automata.rename_nodes()
    # d_finite_automata.graph.view()
    d_finite_automata.reverse().to_dfa().rename_nodes().reverse().to_dfa().rename_nodes().graph.view()


def main():
    # expression = '(a|b)*abb#'
    expression = '(a|b)*aabb#'
    current_tree = SyntaxTree(expression)
    current_dfa = None
    mininmised = False
    os.system('clear')
    while True:
        print(f"Текущее регулярное выражение: {expression}\n"
              f"1. Ввести новое регулярное выражение.\n"
              f"2. Вывести дерево разбора.\n"
              f"3. Вывести детерминированный конечный автомат.\n"
              f"4. Провести минимизацию ДКА и вывести его.\n"
              f"5. Моделировать работу ДКА\n"
              f"0. Выход\n")

        if current_dfa is None: print("ДКА не построен.")
        else:
            if mininmised: print("ДКА построен. Минимизирован.")
            else: print("ДКА построен. Не минимизирован.")

        command = input('Введите команду >> ')
        os.system('clear')
        match command:
            case "1":
                expression = input('Новое регулярное выражение >> ')
                expression += '#'
                current_tree = SyntaxTree(expression)
                mininmised = False
                current_dfa = None
                print('Задано новое выражение. Текущий ДКА сброшен.')
            case "2":
                current_tree.print_tree()
            case "3":
                current_dfa = FiniteAutomata.from_tree(current_tree)
                current_dfa.graph.view(filename='all_pos_non_min', cleanup=True)
                current_dfa.rename_nodes().graph.view(filename='rename_pos_non_min', cleanup=True)
                if mininmised:
                    print('Минимизированный автомат перезаписан. Он больше не минимизирован.')
                    mininmised = False
            case "4":
                if current_dfa is None:
                    current_dfa = FiniteAutomata.from_tree(current_tree)
                current_dfa = (current_dfa.rename_nodes().reverse()
                               .to_dfa()
                               .rename_nodes()
                               .reverse()
                               .to_dfa())
                mininmised = True
                current_dfa.graph.view(filename='all_pos_min', cleanup=True)
                current_dfa.rename_nodes().graph.view(filename='rename_pos_min', cleanup=True)
            case "5":
                if current_dfa is None:
                    print("ДКА еще не построен.")
                else:
                    curr_expression = input('Введите строку для проверки >> ')
                    check_expression(curr_expression, current_dfa)
            case "0":
                exit(0)
            case _:
                print('Вы ввели недопустимую команду.')


if __name__ == '__main__':
    main()
