"""Compile a gettext .po file to .mo without external dependencies."""
from __future__ import annotations

import ast
import struct
import sys
from pathlib import Path


def _finish(entries, msgid, msgstr, msgctxt, fuzzy):
    if msgid is None or msgstr is None or fuzzy:
        return
    key = msgid if msgctxt is None else "{}\x04{}".format(msgctxt, msgid)
    entries[key] = msgstr


def read_po(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    msgid = None
    msgstr = None
    msgctxt = None
    section = None
    fuzzy = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            _finish(entries, msgid, msgstr, msgctxt, fuzzy)
            msgid = msgstr = msgctxt = section = None
            fuzzy = False
            continue

        if line.startswith("#,") and "fuzzy" in line:
            fuzzy = True
            continue
        if line.startswith("#"):
            continue

        if line.startswith("msgctxt "):
            msgctxt = ast.literal_eval(line[8:].strip())
            section = "ctxt"
            continue
        if line.startswith("msgid "):
            if msgid is not None and msgstr is not None:
                _finish(entries, msgid, msgstr, msgctxt, fuzzy)
            msgid = ast.literal_eval(line[6:].strip())
            msgstr = None
            msgctxt = None
            section = "id"
            fuzzy = False
            continue
        if line.startswith("msgid_plural "):
            section = "id_plural"
            continue
        if line.startswith("msgstr "):
            msgstr = ast.literal_eval(line[7:].strip())
            section = "str"
            continue
        if line.startswith("msgstr["):
            idx = line.find("]")
            value = ast.literal_eval(line[idx + 1 :].strip())
            msgstr = ("{}\x00{}".format(msgstr, value) if msgstr else value)
            section = "str"
            continue
        if line.startswith('"'):
            value = ast.literal_eval(line)
            if section == "ctxt":
                msgctxt = (msgctxt or "") + value
            elif section == "id":
                msgid = (msgid or "") + value
            elif section == "str":
                msgstr = (msgstr or "") + value

    _finish(entries, msgid, msgstr, msgctxt, fuzzy)
    return entries


def write_mo(entries: dict[str, str], path: Path) -> None:
    keys = sorted(entries)
    ids = b""
    strs = b""
    id_offsets = []
    str_offsets = []

    for key in keys:
        encoded_id = key.encode("utf-8")
        id_offsets.append((len(encoded_id), len(ids)))
        ids += encoded_id + b"\0"

        encoded_str = entries[key].encode("utf-8")
        str_offsets.append((len(encoded_str), len(strs)))
        strs += encoded_str + b"\0"

    count = len(keys)
    key_table = 7 * 4
    value_table = key_table + count * 8
    id_base = value_table + count * 8
    str_base = id_base + len(ids)

    output = [
        struct.pack("Iiiiiii", 0x950412DE, 0, count, key_table, value_table, 0, 0)
    ]
    output.extend(struct.pack("ii", length, id_base + offset) for length, offset in id_offsets)
    output.extend(
        struct.pack("ii", length, str_base + offset) for length, offset in str_offsets
    )
    path.write_bytes(b"".join(output) + ids + strs)


def main(argv: list[str]) -> int:
    po_path = Path(argv[1]) if len(argv) > 1 else Path("translations/impress/senaite.impress.po")
    mo_path = Path(argv[2]) if len(argv) > 2 else po_path.with_suffix(".mo")
    entries = read_po(po_path)
    write_mo(entries, mo_path)
    print("compiled {} entries -> {}".format(len(entries), mo_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
