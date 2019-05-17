from backend.db import Interaction

class ManagementUtility(object):
    """
    分发用户指令
    """

    def __init__(self, sys_argv):
        if len(sys_argv) < 2:
            self.help_msg()
        else:
            self.sys_argv = sys_argv
            if hasattr(self, sys_argv[1]):
                func = getattr(self, sys_argv[1])
                func()
            else:
                self.help_msg()

    def help_msg(self):
        print("""help msg:
            输入run    启动堡垒机用户入口
        """)

    def run(self, *args, **kwargs):
        print("--running--")
        Interaction(*args, **kwargs)
