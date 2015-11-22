__author__ = 'ironeagle'

success_true = lambda extra: extra.update({'success': True})
success_false = lambda extra, error, code: extra.update({'success': False, 'error': error, 'code': code})