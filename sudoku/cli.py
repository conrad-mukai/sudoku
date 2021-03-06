"""
sudoku.cli

CLI for the sudoku script. This module handles the command line options as well
as the event loop.
"""

# system imports
import argparse
import sys
import curses

# project imports
from sudoku.solver import Solver
from sudoku.display import Display


def main(argv=sys.argv):
    try:
        args = _parse_cmdline(argv)
        try:
            _solve(args.debug, args.puzzle, args.slow)
        finally:
            _close_args(args)
    except SystemExit, e:
        return e
    except Exception, e:
        if 'args' in locals() and args.traceback:
            import traceback
            traceback.print_exc()
        else:
            sys.stderr.write("[error]: %s\n" % e)
        return 1
    return 0


def _parse_cmdline(argv):
    parser = argparse.ArgumentParser(description="Sudoku puzzle solver.")
    parser.add_argument('-s', '--slow', action='store_true',
                        help="slow mode: show puzzle being solved")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="don't use curses to run in a debugger")
    parser.add_argument('-t', '--traceback', action='store_true',
                        help="display call stack when exceptions are raised")
    parser.add_argument('puzzle', type=argparse.FileType('r'), nargs='?',
                        default=None, help="puzzle file")
    return parser.parse_args(argv[1:])


def _close_args(args):
    if args.puzzle:
        args.puzzle.close()


def _solve(debug, puzzle, slow):
    if debug:
        from sudoku.debug import mock_curses
        mock_curses()
    curses.wrapper(_loop, puzzle, slow)


def _loop(stdscr, puzzle, slow):
    Display.draw_screen(stdscr)
    try:
        solver = Solver(puzzle, slow)
        Display.prompt("press any key to continue")
        solver.backtrack()
        Display.prompt("%d iterations, press any key to exit"
                       % solver.iteration)
    finally:
        Display.close_screen()
