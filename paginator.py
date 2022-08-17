from abc import ABCMeta
from typing import List

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardPaginator(metaclass=ABCMeta):
    first_page_label = "<< {}"
    previous_page_label = "< {}"
    current_page_label = ".{}."
    next_page_label = "{} >"
    last_page_label = "{} >>"

    def __init__(self, page_count: int = 2, current_page: int = 1):
        if page_count < 1:
            pass  # TODO error
        self.page_count = tuple(i + 1 for i in range(page_count))
        self.current_page = current_page

        self.inline_keyboard_markup = None
        self._add_before = None
        self._add_after = None

    def _first_page(self) -> int:
        page_number = self.page_count[0]
        return page_number

    def _previous_page(self) -> int:
        previous_val: int = self._current_page() - 1
        if previous_val > self._first_page():
            return previous_val
        return self._first_page()

    def _current_page(self) -> int:
        return self.current_page

    def _next_page(self) -> int:
        next_val: int = self._current_page() + 1
        if next_val < self._last_page():
            return next_val
        return self._last_page()

    def _last_page(self) -> int:
        page_number = self.page_count[-1]
        return page_number

    def _build_buttons(self) -> List[List]:
        # Labels
        fp = self._first_page()
        pp = self._previous_page()
        cp = self._current_page()
        np = self._next_page()
        lp = self._last_page()
        # Buttons
        f_btn = InlineKeyboardButton(self.first_page_label.format(fp), callback_data=f'page#{fp}')
        p_btn = InlineKeyboardButton(self.previous_page_label.format(pp), callback_data=f'page#{pp}')
        c_btn = InlineKeyboardButton(self.current_page_label.format(cp), callback_data=f'page#{cp}')
        n_btn = InlineKeyboardButton(self.next_page_label.format(np), callback_data=f'page#{np}')
        l_btn = InlineKeyboardButton(self.last_page_label.format(lp), callback_data=f'page#{lp}')
        buttons = [
            [f_btn, p_btn, c_btn, n_btn, l_btn],
        ]
        if cp == fp:
            buttons[0].remove(f_btn)
            buttons[0].remove(p_btn)
        elif cp == lp:
            buttons[0].remove(n_btn)
            buttons[0].remove(l_btn)
        if cp == pp:
            if p_btn in buttons[0]:
                buttons[0].remove(p_btn)
        elif cp == np:
            if n_btn in buttons[0]:
                buttons[0].remove(n_btn)

        return buttons

    @property
    def markup(self):
        updated_buttons = self._build_buttons()
        if self._add_before:
            updated_buttons.insert(0, self._add_before[0])
        if self._add_after:
            updated_buttons.append(self._add_after[0])
        self.inline_keyboard_markup = InlineKeyboardMarkup(updated_buttons)
        return self.inline_keyboard_markup

    def add_before(self, inline_keyboards: List[List]):
        if inline_keyboards is None:
            pass  # TODO: raise an error
        self._add_before = inline_keyboards

    def add_after(self, inline_keyboards: List[List]):
        if inline_keyboards is None:
            pass  # TODO: raise an error
        self._add_after = inline_keyboards


class Pagination(InlineKeyboardPaginator):
    def __init__(self, page_count: int = 2, text: str or dict = None):
        super().__init__(page_count)
        if text is None:
            pass  # TODO error
        self.text = text

        self.pages = dict()
        if type(self.text) is str:
            each_page_words = 100
            text_words = text.split(' ')
            remaining, n = len(text_words) % each_page_words, len(text_words) // each_page_words
            page_count = n if remaining == 0 else n + 1  # To catch all pages
            super(Pagination, self).__init__(page_count=page_count)
            for p, i in zip(self.page_count, range(0, len(text_words), each_page_words)):
                words = text_words[i:i + each_page_words]
                self.pages[p] = ' '.join(words)
        elif type(self.text) is dict:
            self.pages = text
        else:
            pass  # TODO raise error

    def display(self, page: int = 1) -> str:
        return self.pages[page]
