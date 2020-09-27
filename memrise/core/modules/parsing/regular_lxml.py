"""
===============================================================================================
Конкретный модуль вытягивания данных с помощью библиотеки lxml для обычных слов учебного курса
===============================================================================================

Это копия старого класса парсинга memrise, его необходимо переписать или хотя бы пересмотреть
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass
from typing import List, TYPE_CHECKING, ClassVar

from lxml.html import fromstring

from memrise import logger
from memrise.core.domains.entities import LevelEntity, WordEntity
from memrise.core.modules.parsing.base import Parser

if TYPE_CHECKING:
    from lxml.html import HtmlElement


@dataclass
class RegularLXML(Parser):
    page: ClassVar[HtmlElement]

    def parse(self, response: str, level_number: int) -> LevelEntity:
        self.page = fromstring(response)
        course_id = self._fetch_course_id(self.page)
        level_id = self._fetch_level_id(self.page)
        name = self._fetch_level_name(self.page)
        self.level = LevelEntity(
            number=level_number, course_id=course_id, name=name, id=level_id
        )
        elements = self._fetch_word_elements(self.page)
        self._fetch_level_words(elements)

        return self.level

    def _fetch_course_id(self, tree: "HtmlElement") -> int:
        """Получаем ID курса в учебном курсе"""
        cls_name = "rebrand reverse-header-ruled level-view"
        elements = tree.find_class(cls_name)
        if len(elements) > 1:
            logger.warning("Found more than one element")

        return int(elements[0].attrib["data-course-id"])

    def _fetch_level_id(self, tree: "HtmlElement") -> int:
        """Получаем ID курса в учебном курсе"""
        cls_name = "rebrand reverse-header-ruled level-view"
        elements = tree.find_class(cls_name)
        if len(elements) > 1:
            logger.warning("Found more than one element")

        return int(elements[0].attrib["data-level-id"])

    def _fetch_level_name(self, tree: "HtmlElement") -> str:
        """Получаем конкретное название уровня в учебном курсе"""
        cls_name = "progress-box-title"
        elements = tree.find_class(cls_name)
        if len(elements) > 1:
            logger.warning("Found more than one element")

        return elements[0].text.strip()

    def _fetch_word_elements(self, tree: "HtmlElement") -> List["HtmlElement"]:
        """Получаем объекты дерево всех слов в уровне"""
        cls_name = "thing text-text"
        return tree.find_class(cls_name)

    def _fetch_couple_words(self, tree: "HtmlElement") -> List["HtmlElement"]:
        """Получаем группы слов `A`-слово в оригинале и `B`-слово перевод """
        cls_name = "col text"
        return tree.find_class(cls_name)

    def _fetch_concrete_word(self, tree: "HtmlElement") -> str:
        """Вытаскиваем конкретное слово из контейнера"""
        cls = "div[contains(@class, 'text')]/text()"
        return tree.xpath(cls)[0]

    def _fetch_level_words(self, elements: List["HtmlElement"]) -> None:
        """Вытаскиваем слова из уровня"""
        for element in elements:
            thing_id = int(element.attrib["data-thing-id"])
            word_container = self._fetch_couple_words(element)
            # TODO: Слелать chunks объектом с описанием полей и пересмотреть логику ниже.
            chunks = []
            for thing in word_container:
                try:
                    word_text = self._fetch_concrete_word(thing)
                    chunks.append(word_text)
                except IndexError:
                    chunks.append("N/A")
                    continue
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    chunks.append("FAILED")
                    logger.error(
                        f"OOPS!! Something strange happened when processing. Please check the course "
                        f"database for this word_content to generate sure that everything looks okay. "
                        f"Here is the error that caused a problem:"
                    )
                    logger.error(e)
                    traceback.print_exc()
                    continue

            level_id = self._fetch_level_id(self.page)
            self.level.add_word(
                WordEntity(
                    id=thing_id, word_a=chunks[0], word_b=chunks[1], level_id=level_id
                )
            )
