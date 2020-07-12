from .notifier import Notifier


class Door:
    is_opened: bool = False

    def __init__(self, is_opened: bool = False):
        self.is_opened = is_opened

    def open(self, is_mail_enabled: bool = False,
             notifier: Notifier = None):
        if(self.is_opened is False and is_mail_enabled is True):
            # door state toggle from close => open
            notifier.send_mail(
                '[door] Door opened',
                'Front door state went: closed -> opened')
        if(self.is_opened is False):
            self.is_opened = True
            return True
        self.is_opened = True
        return False

    def close(self, is_mail_enabled: bool = False,
              notifier: Notifier = None):
        if(self.is_opened is True and is_mail_enabled is True):
            # door state toggle from open => close
            notifier.send_mail(
                '[door] Door closed',
                'Front door state went: opened -> close')
        if self.is_opened is True:
            self.is_opened = False
            return True
        self.is_opened = False
        return False

    def is_opened(self) -> bool:
        return self.is_opened
