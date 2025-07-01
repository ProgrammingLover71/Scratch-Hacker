from sys import argv

USE_SHELL = ('-s' in argv)

if USE_SHELL or True:
    import main_shell
    main_shell.main()