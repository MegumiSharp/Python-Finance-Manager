import traceback
from src.controllers.app_controller import AppController

# Inizialize the application window, if some error is finded is written in the CLI
def main():
    try: 
        app = AppController()
        app.protocol("WM_DELETE_WINDOW", app.on_closure)       # Ensure that a message box with closing confirmation appear
        app.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")
        traceback.print_exc()

# Make the script executed only when directily runned
if __name__ == "__main__":
    main()