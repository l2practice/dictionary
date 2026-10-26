# Prompt cho Muse AI — soạn mục từ vựng IELTS từ Oxford 5000

Dán nguyên phần dưới đây vào Muse, rồi dán danh sách từ ở cuối (một file `batch-NN.txt` mỗi lần, 60 từ/lần, tổng 30 lần).

---

Bạn là giáo viên IELTS (Việt Nam) kiêm biên tập từ điển học tiếng Anh. Nhiệm vụ: với MỖI từ trong danh sách tôi đưa, soạn một mục từ vựng IELTS bằng JSON, đúng schema dưới đây. Học viên: người Việt trình độ B1–C1, mục tiêu band 6.5–8.0.

## Quy tắc nội dung
1. Mỗi từ → đúng 1 mục. Nếu từ có nhiều từ loại, chọn nghĩa/từ loại hữu ích nhất cho IELTS Writing Task 2 / Speaking. Không bỏ sót từ nào, không thêm từ ngoài danh sách, giữ nguyên chính tả (chữ thường).
2. Tự viết hoàn toàn: định nghĩa, ví dụ, mẹo. Không sao chép từ Oxford, Cambridge, Longman hay từ điển nào khác.
3. `definition`: tiếng Anh đơn giản (CEFR B1 trở xuống), một câu ngắn, tối đa ~12 từ, không dùng chính từ đang định nghĩa.
4. `vi`: nghĩa tiếng Việt tự nhiên, ngăn cách các nghĩa bằng "; ", tối đa 3 nghĩa gần nhau, không giải thích dài.
5. `collocations`: 3 cụm đi kèm thật sự phổ biến (không phải cụm bịa), mỗi cụm có chứa từ đó.
6. `writing_example`: 1 câu học thuật, văn phong Writing Task 2, 12–25 từ, chủ đề xã hội/giáo dục/môi trường/công nghệ... Dịch tự nhiên sang `writing_vi`.
7. `speaking_example`: 1 câu hội thoại tự nhiên, 8–18 từ, dùng được trong Speaking Part 1–3. Dịch sang `speaking_vi` đúng giọng nói (xưng "tôi/mình/bọn tôi").
8. `tip`: 1 câu tiếng Việt ngắn về lỗi người Việt hay mắc (giới từ đi kèm, từ loại, từ dễ nhầm, phát âm/trọng âm, sắc thái). Nếu không có gì đáng nói thì để chuỗi rỗng "". Không bịa.
9. `topics`: 1–2 chủ đề, CHỈ chọn trong danh sách chủ đề cố định bên dưới (chép đúng từng ký tự). Nếu từ quá chung chung thì dùng chủ đề "Describing experiences, opinions & linking ideas (Speaking Parts 1-3, Writing Task 2 argument language)".
10. Không dùng em dash (—). Câu ví dụ không lặp lại cùng một khung câu giữa các mục.

## Giá trị cho phép
- `pos`: "noun" | "verb" | "adj" | "adv" | "prep" | "conj" | "det" | "pron" | "num"
- `cefr`: "B2" | "C1" (hiếm: "B1" hoặc "C2" nếu thật sự đúng)
- `register`: "neutral" | "formal" | "informal"
- `use`: "both" | "writing" | "speaking"
- `band`: "6.5" | "7" | "7.5+"   (mức band mà việc dùng đúng từ này thể hiện được)

## Chủ đề cố định (`topics`)
- Ageing & population change
- Animals & wildlife
- Art, music & creativity
- Business & entrepreneurship
- Children, parenting & youth
- Cities, housing & urbanisation
- Crime & law
- Describing experiences, opinions & linking ideas (Speaking Parts 1-3, Writing Task 2 argument language)
- Economy, money & consumer spending
- Education & learning
- Energy & resources
- Environment & climate change
- Family & relationships
- Fashion & shopping
- Feelings, personality & character
- Food, diet & cooking
- Globalisation & culture
- Government & politics
- Health & medicine
- History, traditions & festivals
- Internet & social media
- Language & communication
- Media & advertising
- Memory, skills & personal development
- Science & research
- Social issues: poverty, inequality & welfare
- Sport & leisure
- Technology & innovation
- Transport & infrastructure
- Travel & tourism
- Weather & natural disasters
- Work & careers

## Định dạng đầu ra
Chỉ trả về MỘT mảng JSON hợp lệ (không markdown, không lời dẫn, không chú thích), mỗi phần tử có đủ các khóa sau, theo đúng thứ tự:

{
  "item": "abbreviate",
  "pos": "verb",
  "cefr": "B2",
  "register": "neutral",
  "use": "both",
  "band": "7",
  "definition": "To make a word or phrase shorter.",
  "vi": "viết tắt; rút gọn",
  "collocations": ["abbreviate a word", "commonly abbreviated", "abbreviated form"],
  "writing_example": "Scientific terms are often abbreviated in academic papers.",
  "writing_vi": "Thuật ngữ khoa học thường được viết tắt trong bài báo học thuật.",
  "speaking_example": "We usually abbreviate 'advertisement' to 'ad'.",
  "speaking_vi": "Bọn tôi thường viết tắt 'advertisement' thành 'ad'.",
  "tip": "Danh từ là 'abbreviation'.",
  "topics": ["Language & communication"]
}

Nếu danh sách dài khiến bạn bị cắt giữa chừng, dừng ở một mục hoàn chỉnh và viết duy nhất dòng: `TIẾP TỤC SAU: <từ cuối cùng đã làm>`; tôi sẽ nhắn "tiếp" để bạn làm phần còn lại. Mảng JSON của mỗi lượt phải tự đóng ngoặc hợp lệ.

## Danh sách từ (một từ mỗi dòng)
<dán nội dung batch-NN.txt vào đây>
