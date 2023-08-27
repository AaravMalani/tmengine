from __future__ import annotations
import re
import typing
import json
import dataclasses
import os

@dataclasses.dataclass(slots=True, frozen=True)
class TextMateExpression:
    """Dataclass containing a match"""
    name: str
    range: tuple[int]

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.range)

    def __str__(self) -> str:
        return f'TextMateExpression(name={repr(self.name)}, range={self.range})'


class TextMateEngine:
    def __init__(self, data: typing.Union[list[dict], dict]):
        if type(data) is list:
            self.__languages = {i['scopeName']: i for i in data if 'scopeName' in i}
        else:
            self.__languages = {data['scopeName']: data}

    @property
    def languages(self) -> tuple[str]:
        return tuple(self.__languages.keys())

    def parse(self, language: str, string: str, pattern: typing.Optional[dict] = None, add: int = 0) -> list[dict]:
        if not pattern:
            return [x for i in self.__languages[language]['patterns'] for x in self.parse(language, string, i, add)]
        lst = set()
        if pattern.get('include', '').startswith('#'):
            pattern = self.__languages[language]['repository'].get(
                pattern['include'][1:])
        elif pattern.get('include') in self.__languages:
            return set(self.parse(pattern.get('include'), string, add=add))

        if pattern.get('match'):
            for i in string.split('\n'):
                regex = re.search(pattern.get('match'), i)
                if not regex:
                    continue
                if pattern.get('name'):
                    lst.add(TextMateExpression(pattern.get('name'),
                            (regex.start(0)+add, regex.end(0)+add)))
                    if pattern.get('patterns'):
                        for i in pattern.get('patterns'):
                            if i.get('include', '') == '$self':
                                i = pattern
                            lst.update(self.parse(language, string[regex.start(
                                0):regex.end(0)], i, add=add+regex.start(0)))

                for c, i in enumerate(regex.groups()):

                    if pattern.get('captures', {}).get(str(c), {}).get('name'):
                        lst.add(TextMateExpression(pattern.get('captures', {}).get(
                            str(c), {}).get('name'), (regex.start(c)+add, regex.end(c)+add)))

        elif pattern.get('begin') and pattern.get('end'):
            begin = re.compile(pattern.get('begin')).search(string)
            if not begin:
                return lst
            end = re.compile(pattern.get('end')).search(string, begin.end(0))
            if not end:
                return lst
            if pattern.get('beginCaptures'):
                for i in pattern.get('beginCaptures'):
                    if pattern.get('beginCaptures')[i].get('name'):
                        lst.add(TextMateExpression(pattern.get('beginCaptures')[
                                i]['name'], (begin.start(int(i))+add, begin.end(int(i))+add)))
            if pattern.get('endCaptures'):
                for i in pattern.get('endCaptures'):
                    if pattern.get('endCaptures')[i].get('name'):
                        lst.add(TextMateExpression(pattern.get('endCaptures')[
                                i]['name'], (end.start(int(i))+add, end.end(int(i))+add)))

            if pattern.get('contentName'):
                lst.add(TextMateExpression(pattern.get('contentName'),
                        (begin.end(0)+add, end.start(0)+add)))
            if pattern.get('name'):
                lst.add(TextMateExpression(pattern.get('name'),
                        (begin.start(0)+add, end.end(0)+add)))
            if pattern.get('patterns'):
                for i in pattern.get('patterns'):
                    lst.update(self.parse(language, string[begin.end(0):end.start(0)],
                                          pattern=i, add=add+begin.end(0)))
        else:
            if pattern.get('patterns'):
                for i in pattern.get('patterns'):
                    lst.update(self.parse(
                        language, string, pattern=i, add=add))

        return lst
    @classmethod
    def load_folder(cls, folder: str) -> TextMateEngine:
        lst = []
        for i in os.listdir(folder):
            if not i.endswith('.json'):
                continue
            with open(folder+'/'+i) as f:
                try:
                    lst+=[json.load(f)]
                except:
                    pass
        return TextMateEngine(lst)
