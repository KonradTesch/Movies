import menu_functions as menu


MENU_OPTIONS = {
    0 : (menu.quit_program, "Exit"),
    1 : (menu.print_movie_list, "List movies"),
    2 : (menu.add_movie, "Add movie"),
    3 : (menu.delete_movie, "Delete movie"),
    4 : (menu.print_stats, "Stats"),
    5 : (menu.random_movie, "Random movie"),
    6 : (menu.search_movie, "Search movie"),
    7 : (menu.print_sorted_list_rating, "Movies sorted by rating"),
    8 : (menu.print_sorted_list_release, "Movies sorted by release"),
    9 : (menu.filter_movies, "Filter movies"),
    10 : (menu.generate_website, "Generate website"),
    11 : (menu.create_histogram, "Create rating histogram")
}


def print_title(title):
    """
    Prints the formatted title for the program.
    :param title: title string
    :return: None
    """
    print(menu.blue_text("-" * 15 + f" {title} " + "-" * 15))


def run_menu():
    """
    Prints the menu options and handles user input.
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
    Main function that prints the title and runs the menu loop.
    :return: None
    """
    print_title("Movie Database")

    while True:
        run_menu()


if __name__ == "__main__":
    main()
