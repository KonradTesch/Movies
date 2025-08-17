
import menu_functions as menu


MENU_OPTIONS = {
    0 : (menu.quit_program, "Exit"),
    1 : (menu.print_movie_list, "List movies"),
    2 : (menu.add_movie, "Add movie"),
    3 : (menu.delete_movie, "Delete movie"),
    4 : (menu.update_movie, "Update movie"),
    5 : (menu.print_stats, "Stats"),
    6 : (menu.random_movie, "Random movie"),
    7 : (menu.search_movie, "Search movie"),
    8 : (menu.print_sorted_list_rating, "Movies sorted by rating"),
    9 : (menu.print_sorted_list_release, "Movies sorted by release"),
    10 : (menu.filter_movies, "Filter movies"),
    11 : (menu.generate_website, "Generate website"),
    12 : (menu.create_histogram, "Create rating histogram")
}


def print_title(title):
    print(menu.blue_text("-" * 15 + f" {title} " + "-" * 15))


def run_menu():
    """
    prints the menu options
    :return: None
    """
    print()
    print(menu.blue_text("Menu:"))

    for index, option in MENU_OPTIONS.items():
        print(menu.blue_text(f"{index}. {option[1]}"))


    while True:
        try:
            print()
            choice_string = int(menu.green_input(f"Enter choice (0-{len(MENU_OPTIONS)-1}): "))
            # check if the input is between 1 and 10
            if MENU_OPTIONS.get(choice_string):
                function = MENU_OPTIONS.get(choice_string)[0]
                function()
                input("\nPress enter to continue")
                break
            else:
                raise ValueError()
        except ValueError:
            print(menu.red_text("Invalid input, try again."))


def main():
    """
    The main function
    :return: None
    """
    print_title("Movie Database")

    while True:
        run_menu()


if __name__ == "__main__":
    main()