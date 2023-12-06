############################################
##### Script to call GUI functionality #####
############################################
from source.gui.main_page import MainPage


def run_gui_main_loop(project_name):
    main_page = MainPage(project_name)

    main_page.set_file_manager()
    main_page.set_dag_editor()

    main_page.mainloop()
