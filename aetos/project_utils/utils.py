__author__ = 'ironeagle'

success_true = lambda extra: extra.update({'success': True}) or extra
success_false = lambda extra, error, code: extra.update({'success': False, 'error': error, 'code': code}) or extra


def debugger():
    from IPython.frontend.terminal.embed import InteractiveShellEmbed
    InteractiveShellEmbed()()