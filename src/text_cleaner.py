import re
from html import unescape

class TextCleaner:
    """
    Limpia texto técnico conservando información útil para clasificación.
    """
    def clean(self, text: str) -> str:
        if text is None:
            return ""
        text = str(text)
        text = unescape(text)
        text = text.lower()
        text = self._remove_html(text)
        text = self._remove_urls(text)
        text = self._normalize_technical_terms(text)
        text = self._remove_unwanted_chars(text)
        text = self._normalize_spaces(text)
        return text

    def _remove_html(self, text: str) -> str:
        return re.sub(r"<[^>]+>", " ", text)

    def _remove_urls(self, text: str) -> str:
        return re.sub(r"http\S+|www\.\S+", " ", text)

    def _normalize_technical_terms(self, text: str) -> str:
        replacements = {
            "node js": "node.js",
            "nodejs": "node.js",
            "reactjs": "react.js",
            "vuejs": "vue.js",
            "dot net": ".net",
            "c sharp": "c#",
            "postgres": "postgresql",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _remove_unwanted_chars(self, text: str) -> str:
        """
        Conserva letras, números, espacios y símbolos técnicos frecuentes:
        punto, numeral, guion bajo, signo más y slash.
        """
        return re.sub(r"[^a-záéíóúñ0-9\s\.\#\+\-_/]", " ", text)

    def _normalize_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()
