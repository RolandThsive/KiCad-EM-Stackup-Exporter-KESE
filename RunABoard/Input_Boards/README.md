# Input Boards

Put each board here inside a folder named `<owner>__<repo>`, after where it is on GitHub, with the folders it is in
in its repository:

    Input_Boards/<owner>__<repo>/<path in the repo>/<board>.kicad_pcb

Cloning the repository does just that, and lets the runner note the commit the board was taken at:

    git clone https://github.com/RolandThsive/Thermometer Input_Boards/RolandThsive__Thermometer

Every `.kicad_pcb` file in here is run, apart from KiCad's backups and autosaves. To run only some, name them after
the command: `python run_a_board.py TheMainBoard`. A board outside an `<owner>__<repo>` folder is left out.

The boards belong to their authors: nothing put here is committed, only this README is.
