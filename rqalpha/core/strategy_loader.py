# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
from rqalpha.interface import AbstractStrategyLoader
from rqalpha.utils.strategy_loader_help import compile_strategy
import os
from rqalpha.utils.logger import system_log
from rqalpha.utils.i18n import gettext as _

class FileStrategyLoader(AbstractStrategyLoader):
    def __init__(self, strategy_file_path):
        self._strategy_file_path = strategy_file_path

    def load(self, scope):
        if os.path.basename(self._strategy_file_path).split(".")[1] == "ipynb":
            import io
            from nbformat import read
            from IPython.core.interactiveshell import InteractiveShell
            with io.open(self._strategy_file_path, 'r', encoding='utf-8') as f:
                nb = read(f, 4)
            try:
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        source_code = InteractiveShell.instance().input_transformer_manager.transform_cell(cell.source)
                        break  # 只取第一个cell,
            except Exception as e:
                system_log.error(_(u"load ipynb {file} failed, exception: {e}").format(file=self._strategy_file_path, e=e))
        else:
            with codecs.open(self._strategy_file_path, encoding="utf-8") as f:
                source_code = f.read()

        return compile_strategy(source_code, self._strategy_file_path, scope)


class SourceCodeStrategyLoader(AbstractStrategyLoader):
    def __init__(self, code):
        self._code = code

    def load(self, scope):
        return compile_strategy(self._code, "strategy.py", scope)


class UserFuncStrategyLoader(AbstractStrategyLoader):
    def __init__(self, user_funcs):
        self._user_funcs = user_funcs

    def load(self, scope):
        return self._user_funcs
