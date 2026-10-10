# Dictionary — từ điển Anh–Việt (bản web)

Từ điển học tiếng Anh dạng web tĩnh: Anh–Anh, Anh–Việt, Việt–Anh, chạy offline sau lần tải đầu. Bản cá nhân, thêm lớp
**thuật ngữ Kinh tế – Kế toán** (nhãn ngành) và phần học thuật thử nghiệm do Claude soạn (luôn gắn nhãn **AI**).

> Giao diện là bản sửa từ [ec-advanced-learners-dictionary](https://github.com/nguyennhuanhle/ec-advanced-learners-dictionary)
> của Lê Nguyễn Như Anh (Edtech Corner), **được tác giả đồng ý bằng email** cho việc phát hành bản sửa này.
> Giấy phép gốc: `LICENSE-UPSTREAM-APP.txt`. Bản này đã bỏ Google Analytics của bản gốc, đổi tên và logo;
> tên và logo "EC Advanced Learners' Dictionary" / Edtech Corner vẫn thuộc về tác giả gốc.

## Chạy thử trên máy

```bash
python3 serve.py        # → http://127.0.0.1:4173/dictionary/
```

## Cấu trúc

- `index.html`, `_app/`: giao diện đã dựng (`BASE_PATH=/dictionary`), phục vụ được bằng GitHub Pages.
- `data/`: dữ liệu từ điển chia shard (manifest.json + `v/<phiên bản>/`).
- `source/app/`: mã nguồn giao diện (SvelteKit). Dựng lại: `cd source/app && npm install && BASE_PATH=/dictionary VITE_DATA_BASE=/dictionary/data/ npm run build:web`.
- `tools/overlay.py`: ghép nhãn ngành + phần học thuật Claude vào shard. `tools/export.py`: xuất CSV/JSONL.
- `tools/econ/`: danh sách thuật ngữ ngành (Wiktionary categories).
- `export/`: dữ liệu xuất cho Writing / Speaking.

## Dữ liệu và ghi công

Dữ liệu dựng sẵn từ bản web của dictionary.edtechcorner.com (CC BY-SA 4.0): Wiktionary (en, vi; Wiktextract/kaikki.org),
Open English WordNet (CC BY 4.0), CEFR-J và Octanove Vocabulary Profile, Tatoeba (CC BY 2.0 FR), ECDICT (MIT).
Chi tiết nguồn và giấy phép: `data/v/*/LICENSES.md` và trang *About* trong ứng dụng. Phần dữ liệu bổ sung (nhãn ngành từ
Wiktionary categories; nghĩa do Claude soạn) cùng giấy phép CC BY-SA 4.0.

## Dùng cho Writing / Speaking

`export/writing-speaking/` có bộ CEFR lớn hơn (20.952 từ thay cho 9.394) đúng định dạng của hai repo:
`aw-cefr.js` (thay file cùng tên ở artwrite), `cefr-dict.js` (thay file cùng tên ở fluentalk), `cefr-map.json`,
`cefr-source.json` (từ nào cấp do AI ước lượng) và `glossary-vi.json` (nghĩa Việt + định nghĩa ngắn cho ~19.800 từ).
Tạo lại: `python3.12 tools/make_cefr_map.py <aw-cefr.js gốc> <cefr-dict.js gốc>`.
