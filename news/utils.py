class MyMixin(object):
    mixin_prop = ''

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()

    def get_user_context(self, **kwargs):
        context = kwargs
        return context
