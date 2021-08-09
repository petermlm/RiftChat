import urwid


class CmdPropmt(urwid.Edit):
    _metaclass_ = urwid.signals.MetaSignals
    signals = ["done", "scroll_up", "scroll_down"]

    def __init__(self, prompt):
        super(CmdPropmt, self).__init__(prompt)

    def keypress(self, size, key):
        if key == "enter":
            text = self.get_edit_text()

            if text == "":
                return

            urwid.emit_signal(self, "done", self, text)
            super(CmdPropmt, self).set_edit_text("")

            return

        elif key == "up":
            # TODO
            return

        elif key == "down":
            # TODO
            return

        elif key == "page up":
            urwid.emit_signal(self, "scroll_up")
            return

        elif key == "page down":
            urwid.emit_signal(self, "scroll_down")
            return

        elif key == "esc":
            super(CmdPropmt, self).set_edit_text("")
            return

        urwid.Edit.keypress(self, size, key)


class ClientInterface:
    def __init__(self, new_cmd_callback):
        # Every time a new command is instead this call back is called
        self.new_cmd_callback = new_cmd_callback

        # This list will have the texts in the output area
        self.text_list_walker = urwid.SimpleListWalker([])
        self.text_list = urwid.ListBox(self.text_list_walker)

        # This is a command prompt
        self.cmd_prompt = CmdPropmt("> ")
        self.cmd_prompt_pile = urwid.Pile([self.cmd_prompt])

        # This is the divider that will frame the output are and divide the
        # # output are from the cmd
        self.div = urwid.Divider("=")

        # The main layout
        self.main_layout = urwid.Pile(
            [
                ("flow", self.div),
                self.text_list,
                ("flow", self.div),
                ("flow", self.cmd_prompt_pile),
            ]
        )
        self.main_layout.focus_position = 3

        # Set signals
        urwid.connect_signal(self.cmd_prompt, "change", self.onCmdPromptChange)
        urwid.connect_signal(self.cmd_prompt, "done", self.onCmdPromptDone)
        urwid.connect_signal(self.cmd_prompt, "scroll_up", self.onCmdPromptScrollUp)
        urwid.connect_signal(self.cmd_prompt, "scroll_down", self.onCmdPromptScrollDown)

    def startInterface(self):
        self.main_loop = urwid.MainLoop(self.main_layout, [])
        self.main_loop.handle_mouse = False

        try:
            self.main_loop.run()
        except KeyboardInterrupt:
            return

    def exit(self):
        raise urwid.ExitMainLoop()

    def scrollBottom(self):
        list_len = len(self.text_list_walker) - 1
        if list_len <= 0:
            return
        self.text_list.set_focus(list_len)

    def addLine(self, line):
        self.text_list_walker.append(urwid.Text(line))
        self.main_loop.draw_screen()

    def onCmdPromptChange(self, edit, new_edit_text):
        pass

    def onCmdPromptDone(self, edit, text):
        self.scrollBottom()
        self.new_cmd_callback(text)

    def onCmdPromptScrollUp(self):
        cur_focus = self.text_list.get_focus()[1]

        new_focus = cur_focus - 5
        new_focus = 0 if new_focus < 0 else new_focus

        self.text_list.set_focus(new_focus)

    def onCmdPromptScrollDown(self):
        cur_focus = self.text_list.get_focus()[1]

        list_len = len(self.text_list_walker) - 1
        new_focus = cur_focus + 1
        new_focus = list_len if new_focus >= list_len else new_focus

        self.text_list.set_focus(new_focus)
