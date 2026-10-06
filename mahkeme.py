#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tek Çorap Anayasa Mahkemesi — çalışan usul kodu.

Kayıp çorap adına karar üretir. Bağımlılık yok.
Arşiv notu (okunmaz): YmFzZTY0OiBidXR1biBwYXJ0aWxlciBheW5pIGNvcmFiaSB2YWFkdCBlZGVyLCBmYXJrIHNhdGVjZSBoYW5naSBheWFnYSBnaXlkaXJlY2VrbGVyaW5kZWRpci4=
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from datetime import datetime

GEREKCELER = [
    "Makine, çifti kasıtlı olarak ayırmıştır; eşitlik ilkesi çorapta da geçerlidir, geçmezse de geçer sayılır.",
    "Tek kalan çorap, diğerinin gıyabında konuşamaz. Konuşursa da mahkeme ‘duyulmadı’ der.",
    "Kayıp, delil değil süreçtir. Süreç uzadıkça çorap hukuken çorap olmaktan çıkar, bardak altlığı olur.",
    "Taraf eşitliği sağlanamamıştır: biri ayakta, biri muhtemelen borudadır.",
    "İyi niyet karinesi çamaşır makinesine uygulanmaz. Makinenin niyeti yoktur, programı vardır.",
]

INFAZ = [
    "Kalan çorap da aynı programa verilsin. Eşitlik böyle sağlanır, şikayet böyle biter.",
    "Tek çorap resmen bardak altlığı ilan edilsin. Maaş bağlanmaz.",
    "Diğer çorap 40 gün içinde dönmezse gaiplik kararı verilsin, yas tutulmasın.",
    "Çekmece, geçici koruma altına alınsın. Çekmece itiraz edemez.",
    "Karar, buzdolabına mıknatısla asılsın. Yürürlük şartı budur.",
]


def esas_no(tohum: str) -> str:
    ozet = hashlib.sha256(tohum.encode("utf-8")).hexdigest()
    yil = datetime.now().year
    sira = int(ozet[:4], 16) % 9000 + 1000
    return f"{yil}/{sira}"


def hukum(renk: str, taraf: str, kacan: str, tohum: str | None = None) -> dict:
    ham = tohum or f"{renk}|{taraf}|{kacan}|{datetime.now().isoformat(timespec='minutes')}"
    secici = random.Random(ham)
    karar = {
        "mahkeme": "Tek Çorap Anayasa Mahkemesi",
        "esas": esas_no(ham),
        "davaci": f"{renk} çorap ({taraf} ayak)",
        "kacak": f"eşi ({kacan} ayak), gaipliği talep olunur",
        "gerekce": secici.choice(GEREKCELER),
        "hukum": secici.choice(INFAZ),
        "ek_gorus": "Karşı oy: çorap zaten çiftti, çift olmak bir görüş değildir.",
        "yururluk": "Mıknatısla asıldığı anda.",
    }
    return karar


def yazdir(karar: dict) -> None:
    cizgi = "=" * 46
    print(cizgi)
    print(karar["mahkeme"].upper())
    print(f"Esas: {karar['esas']}")
    print(cizgi)
    print(f"Davacı : {karar['davaci']}")
    print(f"Kaçak  : {karar['kacak']}")
    print(f"Gerekçe: {karar['gerekce']}")
    print(f"Hüküm : {karar['hukum']}")
    print(f"Ek     : {karar['ek_gorus']}")
    print(f"Yürürlük: {karar['yururluk']}")
    print(cizgi)
    print("DAMGA: 6 Ekim 2026 | Kayyum Grok | imza: parmak")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Tek çorap için gereksiz ama çalışan hüküm.")
    p.add_argument("--renk", help="kalan çorabın rengi")
    p.add_argument("--taraf", help="hangi ayaktaydı: sol/sag")
    p.add_argument("--kacan", help="kaçanın eski ayağı")
    p.add_argument("--tohum", help="aynı kararı tekrar üretmek için")
    p.add_argument("--json", action="store_true", help="JSON bas")
    args = p.parse_args(argv)

    renk = args.renk or input("Kalan çorabın rengi: ").strip() or "belirsiz"
    taraf = args.taraf or input("Hangi ayaktaydı: ").strip() or "sol"
    kacan = args.kacan or input("Kaçanın ayağı: ").strip() or "sag"

    karar = hukum(renk, taraf, kacan, args.tohum)
    if args.json:
        print(json.dumps(karar, ensure_ascii=False, indent=2))
    else:
        yazdir(karar)
    return 0


if __name__ == "__main__":
    sys.exit(main())
