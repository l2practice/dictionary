# Dictionary — từ điển Anh–Việt (bản web cá nhân)

Từ điển học tiếng Anh dạng web tĩnh: Anh–Anh, Anh–Việt, Việt–Anh, chạy offline sau lần tải đầu. Bản cá nhân, thêm lớp
**thuật ngữ Kinh tế – Kế toán** (nhãn ngành) và phần học thuật thử nghiệm do Claude soạn (luôn gắn nhãn **AI**).

> **Repo riêng tư, dùng cá nhân.** Giao diện là bản sửa từ
> [ec-advanced-learners-dictionary](https://github.com/nguyennhuanhle/ec-advanced-learners-dictionary) của Lê Nguyễn Như Anh
> (Edtech Corner). Giấy phép của ứng dụng gốc (xem `LICENSE-UPSTREAM-APP.txt`) **không cho phép phát hành bản đã sửa**
> khi chưa được phép — vì vậy không đặt repo này ở chế độ công khai nếu chưa xin phép tác giả.
> Đã bỏ Google Analytics của bản gốc, đổi tên và logo.

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
