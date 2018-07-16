#! /usr/bin/env python3
import re
from deoplete.source.base import Base


class Source(Base):

    # Base options
    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = "typescript"
        self.mark = self.vim.vars['nvim_typescript#completion_mark']
        self.rank = 1000
        self.min_pattern_length = 1
        self.max_abbr_width = 0
        self.max_kind_width = 0
        self.max_menu_width = 0
        self.input_pattern = r'(\.|::)\w*'
        self.filetypes = ["typescript", "tsx", "typescript.tsx", "typescriptreact"]
        if self.vim.vars["nvim_typescript#javascript_support"]:
            self.filetypes.extend(["javascript", "jsx", "javascript.jsx"])
        if self.vim.vars["nvim_typescript#vue_support"]:
            self.filetypes.extend(["vue"])

    def log(self, message):
        """
        Log message to vim echo
        """
        self.debug('************')
        self.vim.out_write('{} \n'.format(message))
        self.debug('************')

    def get_complete_position(self, context):
        m = re.search(r"\w*$", context["input"], re.IGNORECASE)
        return m.start() if m else -1

    def gather_candidates(self, context):
        try:
            [offset] = context["complete_position"] + 1,
            self.vim.funcs.TSDeoplete(context["complete_str"], offset)
            res = self.vim.vars["nvim_typescript#completionRes"]
            if len(res) == 0:
                return []
            return res
        except:
            return []
