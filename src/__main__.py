import sys

if ("-s" in sys.argv) or ("--shell" in sys.argv):
    import main_shell
    main_shell.main()
else:
    import main_gui
    main_gui.main()