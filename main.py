from cli.menu import show_main_menu

if __name__ == "__main__":
    print("=== COMP7640 e-com multi merchant platform ===")
    try:
        show_main_menu()
    finally:
        from config.database import Database
        Database.close()
        print("\nprogram exited, database connection closed.")