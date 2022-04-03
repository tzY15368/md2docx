import copy
import logging
from typing import List
from docx.text.paragraph import Paragraph
import re

from md2paper.v2 import backend


class BasePreprocessor():
    MATCH_ANY = '.*'

    def __init__(self, root_block: backend.Block) -> None:
        self.root_block = root_block
        self.parts: List[str] = []
        pass

    """
    initialize_template returns the exact paragraph
    where block render will begin.
    May return None, in which case render will begin
    at the last paragraph.
    """

    def initialize_template(self) -> Paragraph:
        return None

    """
    preprocess 将原始block中数据与预定义的模板，如论文或英文文献翻译进行比对，
    检查缺少的内容，同时读取填充metadata用于在initialize_template的时候填充到
    文档头(如果需要）
    """

    def __compare_parts(self, incoming: List[str]):
        i = 0
        parts = copy.deepcopy(self.parts)
        while len(parts) != 0:
            if i >= len(incoming):
                if len(parts) != 0:
                    logging.warning('preprocess: unmatched parts:', parts)
                return
            offset = 1
            part = parts[0]
            if part == self.MATCH_ANY and len(parts) >= 2:
                part = parts[1]
                offset = 2
            while i < len(incoming) and not re.match(f"^{part}$", incoming[i]):
                if offset != 2:
                    logging.warning(
                        "preprocess: unexpected part {}".format(incoming[i]))
                i = i + 1
                if i == len(incoming):
                    logging.warning("preprocess: unmatched parts:", parts)
                    return
            parts = parts[offset:]
            i = i + 1

    def preprocess(self):
        real_parts = []
        for blk in self.root_block.sub_blocks:
            real_parts.append(blk.title)
        self.__compare_parts()
