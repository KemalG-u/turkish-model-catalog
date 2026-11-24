"""Özgün kataloğu yükler (190 kayıt).

Varsayılan: arastirma/katalog.json (depoyla birlikte gelir).
İsteğe bağlı: MODEL_CATALOG_HTML ortam değişkeni, `<script id="veri" type="application/json">`
bölümü olan özgün katalog HTML'sinin yolunu verirse kayıtlar oradan okunur.
Dönüş: (katalog, kaynak_yolu) — kaynak_yolu ortam değişkeni kullanılmadıysa None.
"""
import json
import os
import re
from pathlib import Path


def load_catalog(root):
    env = os.environ.get('MODEL_CATALOG_HTML')
    if env:
        src = Path(env)
        text = src.read_text(encoding='utf-8-sig')
        match = re.search(r'<script id="veri" type="application/json">([\s\S]*?)</script>', text)
        if not match:
            raise ValueError('Kaynak katalog JSON bölümü bulunamadı: ' + str(src))
        return json.loads(match.group(1)), src
    path = Path(root) / 'arastirma' / 'katalog.json'
    return json.loads(path.read_text(encoding='utf-8-sig')), None
