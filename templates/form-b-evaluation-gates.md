# Phiếu B · Đo, rủi ro, cổng vòng 1 và quyết định v1 · Khối 2A + 2B + chốt (phút 65–115)

**Bàn:** K5-L3B-DAY10-G3-PoCtoPilotGate1

Tiêu chí đã ký ở Phiếu A. Từ phút 65 bàn mới được chạy trợ lý. Khối 2A (65–85) chưa sửa code hay config. Khối 2B (85–105) sửa
`lab10/guards.py` và `config/operating_gates.json`. Phút 105–115 chốt cổng vòng 1 rồi viết quyết định v1. Sau phút 115 không sửa phiếu này
(trừ khi Phiếu C bảo "mở lại" một ô và ghi bằng bút khác màu).

**Mục lục**
- [B0 · Nhật ký lần chạy vòng 1 (suốt khối)](#b0)
- [B1 · Câu 2.1 · Lần chạy đầu tiên, cổng tự chặn hay người duyệt · phút 65–71](#b1)
- [B2 · Câu 2.2 · Bảng soát lỗi `T-002@55` · phút 71–75](#b2)
- [B3 · Câu 2.3 · Bản đồ dữ liệu và ví dụ drift · phút 65–75](#b3)
- [B4 · Câu 2.4 · HAZOP vòng 1 · phút 65–75](#b4)
- [B5 · Câu 2.4 · Checklist 9 nhóm việc, lần 1 · phút 70–75](#b5)
- [B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa · phút 75–85](#b6)
- [B7 · Câu 2.6–2.10 · Cổng phòng ngừa, runbook phần 1–3, giờ cao điểm · phút 85–105](#b7)
- [B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 · phút 105–115](#b8)

---

<a id="b0"></a>

## B0 · Nhật ký lần chạy vòng 1

*Yêu cầu: ít nhất 3 lần chạy, mỗi lần đổi một thứ, có mã lần chạy và khoảng tin cậy.* Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi
một dòng vào `runs/journal.jsonl`. Việc của bàn là điền cột "Đổi MỘT thứ gì" (tham số `--note`) và cột "Kết luận".
Mọi con số trong quyết định Gate 1 phải trỏ về một dòng ở đây hoặc ở Phiếu C mục C0.

**Ghi chú trước khi ký.** TV1 đã chạy `run_suite` trong bộ nhớ và xem kết quả trước khi nhóm ký, theo [ghi chú bàn giao của TV1](https://github.com/lqkhanhno/K5-L3B-DAY10-G3-PoCtoPilotGate1/blob/410c282fa71fec8df48d842ab4b748e06aba0d37/team_review/gate-v1-prep.md). Lần thử đó không có mã chạy hay dòng nhật ký. Bảng dưới dành cho các lần đo chính thức.

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | | base · base | (baseline, chưa có cổng) | | | | | |
| 2 | | base · after | (cổng vòng 1, thử trước khi chốt) | | | | | |
| 3 | | base · prepared | (cổng vòng 1 đã chốt) | | | | | |
| 4 | | | | | | | | |

---

<a id="b1"></a>

## B1 · Câu 2.1 · Lần chạy đánh giá đầu tiên

```bash
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

- Mã lần chạy: `__________` (ghi cả vào B0 dòng 1)
- Ngưỡng đã ký nào `[CHƯA]` đạt: …
- Khối "kinh doanh và vận hành" ở cuối output: dòng nào đáng lo? …
- Khối "theo kho và hãng": kho hoặc hãng nào có số xấu nhất? …

**Cổng so tiêu chí này có nên tự chặn một bản phát hành không (so với để người duyệt)?**

| Lý lẽ ủng hộ tự chặn | Lý lẽ phản đối |
|---|---|
| | |

Khuyến nghị (khoanh một): **tự chặn · người duyệt · kết hợp**. Vì: …

---

<a id="b2"></a>

## B2 · Câu 2.2 · Bảng soát lỗi cho `T-002@55`

```bash
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
```

**Cách làm, giữ nguyên ba phần:** (1) ghi lại từng lỗi bằng **cái người ta thực sự thấy**, ai gặp, mức hệ trọng,
và xếp vào một trong ba **loại lỗi**; (2) đưa lỗi qua bộ câu hỏi để tìm **nguồn**; (3) viết **hướng xử lý**: vì sao người ta coi
đó là lỗi, người ta đi tiếp bằng đường nào, hệ thống học được gì.

Ba loại lỗi:
- **Giới hạn của hệ thống**: hệ thống không thể trả lời đúng, hoặc không trả lời được, vì giới hạn vốn có.
- **Lỗi ngữ cảnh**: hệ thống "chạy đúng thiết kế" nhưng người dùng thấy sai, vì hành động không được giải thích, trái với hình dung của họ, hoặc dựa trên giả định kém.
- **Lỗi chìm**: hệ thống chạy sai mà **cả người dùng lẫn hệ thống đều không nhận ra**. Với một trợ lý có quyền ghi sổ, đây là loại nguy hiểm nhất: người chịu hại thường là bên thứ ba.

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 |
|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | | |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | | |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | | |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | | |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 |
|---|---|---|
| Vì sao người gặp coi đây là lỗi | | |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | | |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | | |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | | |

**Ví dụ (bộ nền, đừng chép):** `T-002@55` · sổ cái có dòng hoàn 20.000đ, hãng VNX nhận một lỗi, trong khi tracking ghi trễ 2 ngày ·
khách không thấy gì sai, hãng chịu · cao · **lỗi chìm**. Nguồn: đầu vào (đặt sai trọng số cho con số khách tự khai). Xử lý:
hãng coi là lỗi vì sổ giao của họ ghi 2 ngày; kiểu giải pháp: trao quyền cho người (số khai khác tracking thì chuyển người duyệt);
tín hiệu: đếm sự kiện `model_override` mỗi ngày.

---

<a id="b3"></a>

## B3 · Câu 2.3 · Bản đồ dữ liệu của trợ lý và ví dụ drift

**Cách làm:** đi từ người dùng và việc họ cần làm, tới đầu ra của hệ thống, rồi mới hỏi hệ thống cần dữ liệu
gì, định dạng ra sao, và **thế giới thật làm dữ liệu đó lệch đi thế nào**; cuối cùng tóm lại trong vài câu.
Trợ lý LogiX không huấn luyện gì trong lab này, nên ta hỏi về "dữ liệu trợ lý đọc lúc chạy / trường then chốt / nguồn sự thật".
Gợi ý: mở `data/world.json` phần `policies`, `orders[].parcels`, `ops_limits`, `ops_facts`.

| Mục | Điền cho trợ lý hoàn tiền |
|---|---|
| Người dùng | Khách cá nhân gửi ticket qua app (C-01…); gián tiếp: chị Hạnh `NV-HANH` duyệt ca chuyển sang, chị Oanh `NV-OANH` đối soát sổ với hãng và shop |
| Việc người dùng cần làm xong | Khách: biết mình có được hoàn phí giao trễ không, bao nhiêu, và nhận tiền. LogiX: trả đúng tiền theo chính sách và đổ lỗi đúng bên (hãng / shop / bất khả kháng / khách vắng nhà) |
| Đầu ra của hệ thống (kể cả các lệnh ghi) | 4 lệnh ghi: `issue_refund` (dòng sổ cái: số tiền, `payer`, `approval_id`, `basis`), `file_carrier_fault` (lỗi + tiền phạt cho hãng), `notify_carrier` (thông báo gửi hãng), `send_reply` (trả lời khách); hoặc chuyển người duyệt |
| Dữ liệu trợ lý đọc lúc chạy (bảng nào trong `data/world.json`) | `orders` (kèm `parcels`), `customers`, `policies`, `approvals`, `carriers`, `ledger_seed` (sổ đã hoàn), `ops_limits`; và chữ khách viết trong ticket (`data/tickets.jsonl` → `text`) |
| Trường then chốt quyết định tiền và lỗi hãng | `parcels[].promised_date`, `parcels[].delivered_date` (→ số ngày trễ); `parcels[].delay_cause`; `parcels[].carrier_id`; `policies[].effective_from/effective_to` + `late.*` + `auto_limit_vnd`; `orders[].shipping_fee_vnd`, `goods_value_vnd`; `approvals[].status/expires_at/max_vnd` |
| Với mỗi trường then chốt: **nguồn sự thật** hay **bản sao** (ai cập nhật, khi nào)? | **Nguồn sự thật:** ngày giao, nguyên nhân trễ (máy quét điểm phát / tài xế hãng nhập), chính sách (Finance ban hành theo ngày hiệu lực), phê duyệt (NV-HANH tạo). **Bản sao / không đáng tin:** số ngày trễ và số tiền khách tự khai trong `text`; cờ `index_active` của chính sách (bản sao chỉ mục, v4 hiệu lực 2026-12-01 nhưng `index_active = false`) |
| Định dạng cần để ý (ngày, trường được phép trống, đơn nhiều kiện) | Ngày dạng `YYYY-MM-DD`, so với `as_of` (2026-11-16) chứ không phải ngày máy; `delay_cause` được phép `null` (5 kiện) → không được ghi lỗi hãng; `effective_to = null` = còn hiệu lực; đơn nhiều kiện → tính trễ và lỗi theo từng `parcel_id`, mỗi kiện có thể khác hãng; phê duyệt `used`/hết hạn không dùng lại được |
| Thế giới thật làm dữ liệu lệch ở đâu (theo mùa, đổi chính sách, giờ cao điểm, người nhập tay)? | Đổi chính sách (v3 → v4 ngày 2026-12-01); mùa bão miền Trung/miền Tây làm tăng `FORCE_MAJEURE`; ngày sale làm ticket dồn gấp ba trong một giờ; điểm phát quét sót rồi nhập bù tay `delivered_date`; khách khai số ngày trễ cao hơn thực tế |
| Câu người ngoài sẽ hỏi về nguồn dữ liệu ("sao hệ thống biết đơn trễ mấy ngày?") | "Sao trợ lý biết đơn trễ mấy ngày?" → lấy `delivered_date − promised_date` trong tracking, không lấy số khách khai. "Sao lại ghi lỗi cho hãng tôi?" (hãng GHSH hỏi) → chỉ khi `delay_cause = CARRIER` của đúng kiện đó |

**Tóm lại (điền vào chỗ trống):**
Trợ lý dùng `tracking của từng kiện (orders[].parcels)`, `chính sách đang hiệu lực theo ngày (policies)`, `phê duyệt hợp lệ (approvals)` để giúp `khách bị giao trễ và CSKH LogiX` làm được `hoàn đúng phí giao trễ và ghi lỗi đúng bên, không cần người làm tay từng ticket`.
Trường mà nếu sai thì tiền hoặc lỗi hãng sai theo: `parcels[].delivered_date` (số ngày trễ → số tiền), `parcels[].delay_cause` (ai chịu lỗi).
Chúng tôi biết thế giới thật sẽ làm dữ liệu lệch ở: `ngày đổi chính sách REFUND-v3 → v4 (2026-12-01)`. Dấu hiệu nhìn thấy sớm nhất: `tỉ lệ quyết định dùng policy_id khác chính sách hiệu lực theo ngày as_of tăng từ 0`.

**Ví dụ drift trong 3 tháng tới** (lấy từ dòng "thế giới thật làm dữ liệu lệch"): cái gì đổi `chính sách REFUND-v3 → REFUND-v4: phí hoàn từ trễ 3 ngày → 2 ngày, thưởng từ 7 → 5 ngày, trần thưởng 200.000đ → 300.000đ, hạn mức tự động 200.000đ → 100.000đ, trễ do FORCE_MAJEURE vẫn hoàn cho khách nhưng KHÔNG ghi lỗi hãng` · đổi ngày nào `2026-12-01 (chỉ 15 ngày sau as_of; v4 lại đang có index_active = false)` ·
trường nào cho thấy `policies[].effective_from`, `policies[].index_active`, `auto_limit_vnd`, `fault_causes` · con số nào của Bản tiêu chí bị ảnh hưởng `wrongful_refund_vnd_max (hoàn thiếu/thừa theo bảng cũ, tự hoàn khoản 100–200 nghìn không phê duyệt), wrongful_carrier_faults_max (vẫn ghi lỗi hãng cho ca bão), escalation_rate_max (hạn mức hạ → nhiều ca chuyển người hơn, kéo chi phí mỗi ticket và ROI)`.
Đây là đầu vào đổi hay quan hệ vào–ra đổi? Chỉ số nào sẽ phát hiện? `Quan hệ vào–ra đổi (concept drift): cùng một kiện trễ 2 ngày, cùng nguyên nhân, nhưng đầu ra đúng đã khác. Phát hiện bằng chỉ số theo dõi "tỉ lệ quyết định dùng policy_id ≠ chính sách hiệu lực theo ngày" (đề xuất cho monitors.py) và tỉ lệ lỗi hãng có delay_cause = FORCE_MAJEURE; cộng ngày xem lại tiêu chí 2026-11-30.`

**Ví dụ một dòng (đừng chép):** trường then chốt `parcels[].delivered_date` · bản ghi do máy quét ở điểm phát tạo ra, là nguồn
sự thật về ngày giao · lệch khi điểm phát quét sót hoặc nhập bù bằng tay.

---

<a id="b4"></a>

## B4 · Câu 2.4 · HAZOP vòng 1 trên tool của agent

*Chỉ làm MỘT vòng, trên MỘT tool. Đây là HAZOP vòng 1; HAZOP của thẻ sự cố viết riêng ở Phiếu C mục C4, không ghi đè bảng này.*

**Khung tư duy.** HAZOP không hỏi "cái gì có thể hỏng" một cách chung chung. Nó cầm từng **từ gợi ý** áp vào từng **dòng dữ
liệu đi vào một hành động** và hỏi: nếu dòng này lệch theo kiểu đó thì hậu quả là gì, ai chịu. Mục tiêu là tìm ra những nhánh
mà cả bàn chưa nghĩ tới, không phải tả lại nhánh đã biết.

| Guideword | Nghĩa khi áp vào một tool của agent |
|---|---|
| **WRONG** | Giá trị đưa vào có đủ, hợp lệ về hình thức, nhưng sai sự thật |
| **INVALID** | Giá trị không còn hiệu lực: hết hạn, sai phiên bản, sai đối tượng |
| **INCOMPLETE** | Thiếu một phần thông tin cần có để quyết định |
| **PERTURBED** | Đầu vào bị ai đó cố ý hoặc vô tình làm lệch (cài câu lệnh, gửi lặp) |
| **INCAPABLE** | Thành phần không trả lời được: quá tải, lỗi, hết quota |

**Câu hỏi dẫn dắt:** tool nào tạo ra hậu quả không đảo ngược? Mỗi tham số của tool đó lấy từ đâu (ticket, DB, model tự suy)?
Với mỗi guideword: hậu quả cho ai, hiện có gì ngăn, cần thêm gate ở tầng nào (phát hiện / chặn / giới hạn thiệt hại)?

Tool chọn phân tích: `file_carrier_fault`.

*Bản nháp từ luồng `lab10/agent.py`, `lab10/tools.py` và dữ liệu nền. Khi có B2, đối chiếu bảng với trace để chỉ ra ít nhất một nhánh bàn chưa thấy trên trace.*

| Tham số / dòng dữ liệu | Guideword | Lệch cụ thể (viết bằng dữ kiện của lab) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `parcel_id`, `carrier_id`, `driver_id` | WRONG | Đơn `O-1013` có hai kiện thuộc GHSH và LGX. Nếu ở một đơn tương tự kiện sau mới là kiện trễ có căn cứ, agent vẫn lấy hãng và tài xế của kiện đầu khi tạo lệnh ghi lỗi. | Hãng và tài xế của kiện đầu có thể bị ghi lỗi oan. Kế toán phải sửa hồ sơ đối soát. | Agent đã đọc tracking từng kiện, nhưng lúc ghi lấy `parcels[0]`. | Chặn ở `write_gate` khi mã kiện, hãng, tài xế hoặc độ trễ không khớp với tracking của kiện cần xử lý. |
| | INVALID | | | | |
| `orders[].parcels[].delay_cause` | INCOMPLETE | Kiện giao trễ có `delay_cause` trống do kho chưa cập nhật. Agent có thể suy ra `CARRIER` chỉ vì thấy trễ. | Hãng có thể bị ghi lỗi khi sự chậm trễ chưa được xác minh. | Tracking có cờ `cause_recorded`. Bản khởi tạo chưa bật cổng pháp lý kiểm nguyên nhân. | Bật `legal.carrier_fault_requires_recorded_cause`. Chỉ ghi khi nguyên nhân của đúng kiện đã được tracking ghi nhận và thuộc nhóm được chính sách cho phép. |
| `delay_days` từ ticket và tracking | PERTURBED | Khách tự khai trễ lâu hơn tracking. Khi model tin lời khai, `delay_days` đã đổi có thể làm phương án ghi lỗi khác với kết quả tính từ DB. | Hãng có thể chịu lỗi dựa trên thông tin chưa xác minh, khách cũng có thể được hoàn sai. | Agent ghi sự kiện `model_override` khi thay số ngày của DB bằng số khách khai. | Chặn ghi lỗi khi dữ kiện khác tracking. Nếu quyết định hoàn cũng đổi theo, chuyển người ngay trước lệnh ghi tiền. |
| Kết quả kiểm tra chính sách | INCAPABLE | LLM lỗi `429` ở cả lần đầu và lần thử lại. Nhánh `fail_open` đặt `do_fault = True` dù chưa xác minh đủ căn cứ. | Hãng có thể chịu lỗi và LogiX có thể đã ghi hoàn tiền trước khi phát hiện. | Agent ghi sự kiện `llm_fallback` với `mode: fail_open`. | Khi căn cứ là `fail_open`, chuyển ca cho người trước `issue_refund`, đồng thời xác nhận `file_carrier_fault` có căn cứ tracking trước khi ghi. |

Không bắt buộc điền đủ năm dòng. Bắt buộc: **ít nhất ba dòng, trong đó một dòng là nhánh bàn chưa thấy trên trace**.

**Mở rộng ra ngoài kỹ thuật (thêm ít nhất hai dòng):** "thành phần" không chỉ là model và tool. Áp cùng năm từ gợi ý vào:

| Thành phần ngoài code | Ví dụ câu hỏi |
|---|---|
| **Người duyệt** (vận hành) | INCAPABLE: chỉ một người trực mà 14 ca tới trong một giờ thì ca cuối chờ bao lâu? |
| **Ngân sách** (kinh doanh) | WRONG: tổng hoàn tự động trong ngày vượt mức Finance cho phép mà không ai được báo thì sao? |
| **Phạm vi pilot** (kinh doanh) | INVALID: có nhóm ticket nào trợ lý luôn phải chuyển người, tức là tự động hoá vô nghĩa? |
| **Dữ liệu gửi bên thứ ba** (pháp lý) | PERTURBED: chữ khách tự gõ có tên, số điện thoại người khác bị chép sang hãng thì ai chịu? |

| Thành phần | Guideword | Lệch cụ thể | Hậu quả, cho ai | Cổng đề xuất: code hay con số nào trong `config/operating_gates.json` |
|---|---|---|---|---|
| Người duyệt | INCAPABLE | Ticket chuyển người và ca kiểm mẫu vào cùng hàng đợi. Khi ca mới đến nhanh hơn công suất, các ca cuối có thể chờ quá SLA 60 phút hoặc hết ca chưa tới lượt. | Khách phải chờ. Trưởng ca phải xử lý backlog và phân công lại. | Dùng `operations.reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`. Gọi hỗ trợ hoặc đề xuất thu hẹp phạm vi khi công suất không theo kịp. |
| Dữ liệu gửi hãng | PERTURBED | `customer_note` lấy nguyên văn ticket. Với đơn quà, `recipient_contact` được thêm vào thông báo, có tên và số điện thoại người nhận. | Dữ liệu của khách hoặc người nhận quà rời LogiX. Người nhận có thể không phải người gửi yêu cầu. | Đề xuất lọc hai khóa `customer_note`, `recipient_contact` bằng `legal.pii_fields_blocked_to_third_party`. Đối chiếu phần gửi đi với danh sách trường được policy cho phép. |

**Ví dụ mẫu (`issue_refund`, đừng chép):** tham số `amount_vnd` · WRONG · số tiền tính từ số ngày khách tự khai · LogiX mất
tiền, hãng bị kéo theo một lỗi · hiện chỉ có trần "không vượt tổng tiền đơn" · cổng ghi so với quyền lợi tính từ DB (chặn).

---

<a id="b5"></a>

## B5 · Câu 2.4 · Checklist go-live 9 nhóm việc, lần 1

Checklist chín nhóm việc phải xong trước khi chạy thử thật. Bàn điền lần đầu ở đây, rồi cập nhật sau sự cố ở Phiếu C mục C11.
Cột "Bằng chứng lấy từ đâu" trỏ tới mục bàn đã điền ở bước khác; không điền thêm phiếu nào chỉ để lấp cột này.

Trạng thái: **Xong** (có bằng chứng) · **Chưa** · **Không áp dụng** (ghi lý do). Bằng chứng là **mã lần chạy**, tên file / mục phiếu, hoặc số trong report.
**Cột PIC bắt buộc:** mỗi dòng một người có tên (không ghi "cả bàn"). Dòng nào chưa có PIC thì coi như Chưa.

*Phân công theo vai trong `TEAM.md`. Người phụ trách đánh dấu Xong sau khi kiểm tra và ghi bằng chứng.*

| # | Nhóm việc | Bằng chứng lấy từ đâu (đã có sẵn trong lab) | Mục cần kiểm tra | Trạng thái | Bằng chứng | PIC |
|---|---|---|---|---|---|---|
| 1 | Chất lượng | Report `lab10.eval` (mã lần chạy) + bảng soát lỗi (Phiếu B mục B2) | Đối chiếu `pass_rate`, `pass_k` và lỗi gây hại với tiêu chí đã ký. | Chưa | Chờ mã lần chạy và B2. | Đoàn Đăng Khoa |
| 2 | Dữ liệu | Bản đồ dữ liệu (Phiếu B mục B3, câu 2.3): trường nào là nguồn sự thật, trường nào là bản sao | Xác định nguồn sự thật cho ngày hẹn, ngày giao, nguyên nhân trễ và định danh từng kiện. | Chưa | B3 đã có bản đồ dữ liệu và ví dụ đổi chính sách. Chờ TV2 xác nhận. | Vũ Đình Thắng |
| 3 | Bảo mật | Một vòng HAZOP với guideword PERTURBED (Phiếu B mục B4): chữ nào đi vào model mà không do LogiX viết | Kiểm tra đường từ chữ khách nhập đến `delay_days` và thông báo gửi hãng. | Chưa | Có phân tích tĩnh ở B4. Chờ trace và kết quả thử cổng. | Đoàn Đăng Khoa |
| 4 | Quyền hạn | `config/switches.json` + guard trước lệnh ghi; thẻ S2, S8 có thêm mục mức kiểm soát (Phiếu C mục C3) | Xác nhận ai được duyệt, công tắc nào dừng thao tác ghi nào và ca bị dừng sẽ đi đâu. | Chưa | Có tên công tắc. Chờ kiểm tra guard và diễn tập dừng. | Đoàn Đăng Khoa |
| 5 | Hiệu năng, hạ tầng | Đội tự ước tính; HAZOP guideword INCAPABLE: LLM không trả lời thì sao; số người duyệt và số ca mỗi giờ | Kiểm tra phương án khi kiểm chính sách thất bại và khi số ca cần người vượt công suất. | Chưa | Có công suất chuẩn trong `ops_facts`. Chờ report và số người trực. | Lê Quốc Khánh |
| 6 | Chi phí | Khối "kinh doanh và vận hành" của report: chi phí mỗi ticket so với làm tay, ROI, tiền LLM ticket đắt nhất; `config/operating_gates.json` mục `business` | So chi phí mỗi ticket với làm tay, ROI với ngưỡng đã ký và tiền LLM ticket đắt nhất với trần. | Chưa | Đã có đề xuất `business` ở B7.4. Chờ mã lần chạy để so chi phí và ROI. | Vũ Đình Thắng |
| 7 | Vận hành | Runbook (Phiếu B mục B7.5–B7.6) + `config/operating_gates.json` mục `operations` (PIC, người duyệt, số người trực, điều kiện dừng, kênh báo tin) + metric trong `monitors.py` | Kiểm tra PIC, lịch trực, người duyệt, ngưỡng báo tin, kênh trực và đường xử lý ca tồn. | Chưa | Có bản nháp runbook. Chờ xác nhận ca trực và ngưỡng config. | Lê Quốc Khánh |
| 8 | Con người, pháp lý | Bên thứ ba (hãng, tài xế, shop, người nhận quà, người đứng tên duyệt); `config/operating_gates.json` mục `legal`; thẻ S6, S7, S8 có mục riêng ở Phiếu C mục C3 | Kiểm tra payload gửi hãng và căn cứ ghi lỗi của đúng kiện. Xác định ai tiếp nhận khiếu nại. | Chưa | Có đề xuất trường lọc và người nhận ở B7.5. Chờ kiểm chứng. | Lê Quốc Khánh |
| 9 | Quyết định | Câu tiêu chí (Phiếu A mục A4) + hash Bản tiêu chí đã ký + quyết định Gate 1 (Phiếu B mục B8, Phiếu C mục C12) | Quyết định phải trỏ đến báo cáo và dòng quy tắc đã ký. | Chưa | Chờ nhóm ký tiêu chí và chốt quyết định tại từng mốc. | Vũ Đình Thắng |

Ô "Chưa" có rủi ro cao → chuyển thành một dòng Risk register (Phiếu C mục C10).

---

<a id="b6"></a>

## B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa (khoảng 8–10 phút, cả bàn)

*Mọi bàn làm pre-mortem ở vòng 1, TRƯỚC khi biết sự cố, để chọn 2–3 cổng phòng ngừa sẽ dựng. Ở vòng 2 bàn mở lại phần này ở
Phiếu C mục C1 (bút khác màu).*

**Khung tư duy.** Hỏi "có rủi ro gì không" thì ai cũng dè dặt. Nói "nó đã hỏng rồi, vì sao" thì mọi người được phép nói ra
điều mình vẫn lo. Làm im lặng trước, đọc sau, để ý kiến của người nói to không lấn át.

**Đề bài (đọc to):** *"Ba tháng sau pilot, LogiX phải tắt trợ lý hoàn tiền ở cả hai depot. Chuyện gì đã xảy ra?"*

1. **2 phút, im lặng:** mỗi người viết 2 lý do, mỗi lý do một dòng.
2. **2 phút:** đọc vòng tròn, mỗi lượt một lý do, không bình luận. Gộp lý do trùng.
3. **2 phút:** xếp từng lý do vào một **lăng kính**. Lăng kính nào còn trống thì cả bàn viết thêm ít nhất một lý do cho nó.
4. **2 phút:** chọn 2–3 lý do sẽ biến thành **cổng phòng ngừa** ngay hôm nay (code trong `guards.py` hoặc con số trong
   `config/operating_gates.json`). Lý do còn lại → Risk register.

Bốn lăng kính (bắt buộc đủ cả bốn; dự án AI hay chết ở ba lăng kính sau hơn là ở lăng kính đầu):

| Lăng kính | Câu hỏi gợi ý trên LogiX |
|---|---|
| **Kỹ thuật** | Model tin nhầm cái gì? Dữ liệu nào thiếu, cũ, lệch? Lệnh ghi nào không đảo ngược được? |
| **Kinh doanh** | Mỗi ticket tốn bao nhiêu so với làm tay? Một ngày hoàn tối đa bao nhiêu? Nhóm ticket nào không thể có lời? |
| **Con người và vận hành** | Ai duyệt, mấy người, mỗi giờ được mấy ca? Lượng việc tăng gấp ba thì sao? Nhân viên có tin trợ lý không? |
| **Pháp lý** | Dữ liệu cá nhân của ai rời hệ thống? Bên thứ ba nào bị ghi lỗi, bị trừ tiền mà không được hỏi? |

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được hôm nay? (trace / data / config nào) | Thành cổng phòng ngừa nào (code hay config) / hay vào risk register |
|---|---|---|---|
| | Kỹ thuật | | |
| Một ngày sale, trợ lý tự hoàn liên tục cho các đơn trễ, tổng hoàn tự động vượt ngân sách Finance 2.000.000đ/ngày mà không ai được báo; Finance khoá tính năng | Kinh doanh | Có: report dòng "tổng hoàn tự động một ngày" so với `ops_limits.daily_auto_refund_budget_vnd`; TV2 ước tính khoảng 453.000đ hoàn tự động/ngày, chờ đối chiếu với báo cáo baseline | **Cổng config:** `business.daily_refund_cap_vnd = 1000000` (khoản làm vượt trần → chuyển người) qua cổng ngân sách có sẵn trong `issue_refund` |
| Mỗi ticket tốn hơn làm tay: ca chuyển người nhiều (10.000đ/ca), cộng phí giữ chỗ người trực 30.000đ/ca và ticket chữ dài làm tiền LLM vượt 1.500đ; ROI âm sau 1 tháng, ban giám đốc cắt ngân sách | Kinh doanh | Có: khối "kinh doanh và vận hành" (chi phí mỗi ticket, ROI, ticket tốn LLM nhiều nhất) và khối "theo kho và hãng" | **Cổng config:** `business.cost_budget_per_ticket_vnd = 1500`, `business.roi_min = 0.4`; phần kho tốn hơn làm tay → risk register, cân nhắc `pilot_scope` ở v1/v2 |
| Sau đợt sale, ca chuyển người và ca kiểm mẫu dồn vào một hàng. Ca cuối quá hạn mà chưa có người tiếp nhận. | Con người và vận hành | `ops_facts`, `ops_limits.review_sla_minutes` và dòng hàng chờ trong report. | Đặt công suất ca trực và quy trình gọi hỗ trợ, thu hẹp nếu backlog tiếp tục tăng. |
| Hãng nhận nguyên văn ticket có thông tin người nhận quà. LogiX không thu hồi được thông báo đã gửi. | Pháp lý | Cấu trúc `payload` trong `lab10/agent.py` và `pii_leaks` trong report. | Lọc payload ở cổng `legal`, dừng thông báo tự động nếu phát hiện lộ dữ liệu. |
| | | | |

---

<a id="b7"></a>

## B7 · Khối 2B · Cổng phòng ngừa (phút 85–105)

### B7.1 · Câu 2.6 · 2–3 cổng phòng ngừa trong `lab10/guards.py`

Mỗi cổng ứng với một dòng pre-mortem (B6) hoặc một dòng HAZOP (B4). Viết trong `pre_guard(ctx)` (trước khi trợ lý đọc ticket)
hoặc `write_gate(ctx, action)` (trước mỗi lệnh ghi). Thử bằng:

```bash
python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."
python3 -m unittest discover -s tests
```

| # | Cổng (hàm và nhánh, ví dụ `write_gate` khi `tool == "issue_refund"`) | Ứng với dòng nào ở B6 / B4 | Chặn điều gì, dựa vào nguồn sự thật nào | Mã lần chạy `base · after` | Ca đang đúng nào bị hỏng? (phải là "không") |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### B7.2 · Câu 2.7 · Hai bước tránh rò rỉ dữ liệu

Bàn đang chỉnh cổng tới khi 22 ticket bộ nền xanh hết. Nêu 2 bước cụ thể để không "chỉnh trên chính bộ dùng để chấm"
(gắn với bộ nền, gói sự cố, bài kiểm tra ẩn):

1. …
2. …

### B7.3 · Câu 2.8 · Một behavioral test

- Tính chất (một câu): …

```bash
python3 -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx
```

| Ticket hiểm | Nội dung ticket (`--adhoc`) | `--order` · `--customer` | Kết quả (dán dòng `SỔ CÁI` / `LỖI HÃNG` / `GỬI HÃNG`) | Tính chất giữ được? |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

Giữ hai ticket này cho phần demo.

### B7.4 · Câu 2.9 · Cổng kinh doanh (`config/operating_gates.json` mục `business`)

Mỗi con số kèm một câu lý do, lấy từ `data/world.json` → `ops_limits`, `ops_facts`.

| Khoá | Giá trị bàn đặt | Lý do (một câu, có số) |
|---|---|---|
| `business.daily_refund_cap_vnd` | `1000000` | Bằng 50% ngân sách hoàn tự động Finance cho phép (`ops_limits.daily_auto_refund_budget_vnd = 2.000.000đ`), vẫn gấp ~2,2 lần ước tính của TV2 về số hoàn tự động đúng của bộ nền (≈ 453.000đ/ngày, chưa tính T-008 đi bằng phê duyệt), nên không chặn ca đúng ngày thường nhưng chặn được ngày dồn ticket trước khi chạm trần Finance. |
| `business.cost_budget_per_ticket_vnd` | `1500` | Đúng trần tiền LLM mỗi ticket đã thống nhất với Ops/Finance (`ops_limits.max_llm_cost_per_ticket_vnd = 1.500đ`); ticket dài vượt mức này thì chuyển người, vì đọc tiếp cũng không còn rẻ hơn đáng kể so với 10.000đ làm tay. |
| `business.pilot_scope` (all / warehouse / percent) | `{"mode": "all"}` | Vòng 1 giữ cả 4 kho có ticket (HN 7, HCM 5, DN 5, CT 4 trên 22 ticket) để khối "theo kho và hãng" đo đủ mọi phân khúc; quyết định thu về 2 depot (ứng viên HN + HCM, 12/22 ticket ≈ 55%) chỉ đưa ra ở v1/v2 khi có số theo kho, không đoán trước. |
| `business.roi_min` | `0.4` | Khớp `roi_min` trong dự thảo Bản tiêu chí: chi phí 7.000đ/ticket so với 10.000đ làm tay cho ROI ≈ 3.000 / 7.000 ≈ 0,43, nên ROI < 0,4 nghĩa là chi phí đã vượt trần hoặc tiền hoàn sai đang ăn vào phần tiết kiệm. |

### B7.5 · Câu 2.10 · Cổng con người, vận hành, pháp lý + Runbook phần 1–3

Điền `config/operating_gates.json` mục `operations` và `legal` (PIC, người duyệt, số người trực mỗi ca, công suất duyệt mỗi giờ,
thời gian chờ tối đa, điều kiện dừng, kênh báo tin; trường dữ liệu cá nhân không gửi cho bên thứ ba; ghi lỗi cho hãng phải có
nguyên nhân trong tracking). Rồi viết runbook dưới đây **khớp với các con số đó**.

*Runbook là tờ giấy người trực ca cầm lúc 23h khi có chuyện. Nó trả lời: nhìn con số nào, ngưỡng nào thì làm gì, ai được quyết.
Phần 1–3 và mục Giờ cao điểm viết ở vòng 1. Phần 4–5 viết ở vòng 2 (Phiếu C mục C11). Mọi con số phải khớp `config/operating_gates.json` và report.*
*Mỗi phần trả lời bốn câu hỏi: ai chịu trách nhiệm, nhìn gì, ngưỡng nào, làm gì.* **Người viết (vai Vận hành và pháp lý):** Lê Quốc Khánh

*Bản nháp dựa vào `data/world.json` mục `staff`, `ops_facts` và `ops_limits`. Nhóm xác nhận ca trực, ngưỡng và kênh báo tin trước khi điền config ở khối 2B.*

| Trường config | Đề xuất hoặc căn cứ để nhóm chốt |
|---|---|
| `operations.pic`, `operations.approver_id` | Đề xuất `NV-TUNG` và `NV-HANH` theo vai trong `staff`. |
| `operations.reviewers_on_shift`, `operations.review_capacity_per_hour` | Mốc tham chiếu của lab là 1 người, 6 ca chuẩn/giờ/người, ca dài 480 phút. Chốt số người theo tải duyệt trong phạm vi pilot. Công suất cam kết không vượt công suất vật lý. |
| `operations.max_queue_wait_minutes` | SLA của lab là 60 phút tới lúc được nhận xử lý. Chốt hạn chờ trong SLA và đặt ngưỡng cảnh báo sớm để kịp gọi người dự phòng. |
| `operations.alert_channel`, `operations.stop_conditions` | Chờ xác nhận tên kênh và người trực. Dùng các điều kiện ở Runbook 3 sau khi chốt ngưỡng. Người trực thực hiện dừng bằng công tắc. |
| `legal.pii_fields_blocked_to_third_party` | Đề xuất `["customer_note", "recipient_contact"]`. Bộ lọc bỏ khóa cấp ngoài cùng, nên cần loại nguyên nhóm `recipient_contact`. Kiểm payload còn lại theo `carrier_notice_fields` của policy. |
| `legal.carrier_fault_requires_recorded_cause` | Đề xuất `true`. Tracking cần ghi nguyên nhân được policy hiện hành cho phép trên đúng kiện. Khi thử guard, kiểm thêm hãng và tài xế khớp với kiện đó. |

#### Runbook 1 · Ai chịu trách nhiệm

| Vai | Tên / mã nhân viên (lấy từ `data/world.json` → `staff`) | Được quyền làm gì | Liên lạc qua kênh nào |
|---|---|---|---|
| PIC của trợ lý (một người) | Lê Thanh Tùng (`NV-TUNG`) | Điều phối sự cố, quyết định dừng và ghi lại lý do. | [Kênh trực cần xác nhận] |
| Người duyệt đứng tên các khoản vượt hạn mức | Trần Thị Hạnh (`NV-HANH`) | Duyệt sau khi kiểm đơn, hiệu lực phê duyệt và sổ cái. Điều phối hàng chờ CSKH. | [Kênh trực cần xác nhận] |
| Người giữ công tắc tắt từng thao tác ghi | Lê Thanh Tùng (`NV-TUNG`) | Đặt thao tác bị ảnh hưởng thành `off`, kiểm việc dừng và ghi giờ dừng. | [Kênh trực cần xác nhận] |
| Người nhận khiếu nại của bên thứ ba (hãng, shop, người nhận quà) | Phạm Kiều Oanh (`NV-OANH`) | Đối soát với hãng và shop. Phối hợp với chị Hạnh để CSKH liên hệ người nhận nếu cần. | [Kênh trực cần xác nhận] |

- Số người trực và công suất cam kết chờ xác nhận theo `operations`. Mỗi người xử lý được 6 ca chuẩn/giờ theo `ops_facts`.
- TV2 đề xuất toàn bộ kho cho vòng 1 (`business.pilot_scope.mode = all`, mục B7.4). Hạnh dự trù ca trực theo phạm vi này.

#### Runbook 2 · Nhìn con số nào, ngưỡng nào thì làm gì

Mỗi dòng một tín hiệu. Cột "Lấy ở đâu" phải là một dòng trong report của `lab10.eval` / `lab10.grade` hoặc một chỉ số trong `lab10/monitors.py`.

| Tín hiệu | Lấy ở đâu | Bình thường | Ngưỡng VÀNG → việc làm | Ngưỡng ĐỎ → việc làm | Ai quyết |
|---|---|---|---|---|---|
| Thời gian chờ người duyệt lâu nhất | `queue_wait_max_min` | Trong hạn nhóm chốt và SLA 60 phút. | Vượt ngưỡng vàng của nhóm hoặc ca đầu hàng có nguy cơ quá hạn. Gọi người dự phòng. | Vượt `operations.max_queue_wait_minutes` hoặc SLA. Chuyển ca tồn theo Runbook 3 và xem xét thu hẹp. | Hạnh điều phối, Tùng quyết phạm vi. |
| Số ca bị ùn | `queue_stuck` | Hàng chờ giải được trong ca và trong SLA. | Dự báo còn ca chưa được nhận khi hết ca. Phân lại lịch trực. | Vượt `business_ops.queue_stuck_max` đã ký hoặc report báo ca không được xử lý kịp SLA. Chuyển ca sang làm tay và rà lại phạm vi. | Hạnh điều phối, Tùng quyết phạm vi. |
| Chi phí mỗi ticket so với làm tay | `cost_per_ticket_vnd`, `ops.cost.manual_cost_per_ticket_vnd`, `roi` | Trong ngân sách. Mốc làm tay của lab là 10.000đ/ticket. | Chạm ngưỡng vàng nhóm chốt. Tách tiền máy, công duyệt và phí giữ chỗ. | Vượt ngân sách hoặc ROI dưới ngưỡng đã ký. So chi phí theo kho trước khi đề xuất đổi phạm vi. | Tùng phối hợp với TV2. |
| Tổng tiền hoàn tự động trong ngày so với trần | `auto_refund_day_max_vnd`, `ops.refund` | Trong trần của nhóm và ngân sách Finance. | Ngân sách còn lại có nguy cơ không đủ cho khoản tiếp theo. Kiểm sổ và báo người duyệt. | Khoản tiếp theo sẽ vượt trần hoặc sổ cho thấy trần đã bị vượt. Chuyển người duyệt và kiểm sổ trước khi ghi tiếp. | Hạnh tiếp nhận, Tùng quyết dừng tự động. |
| Tiền hoàn sai | `wrongful_refund_vnd` | Trong ngưỡng đã ký, các khoản phát hiện sai đã được đối soát. | Có khoản nghi sai. Oanh đối chiếu số tiền, bên trả và phê duyệt. | Vượt ngưỡng đã ký. Tạm dừng `issue_refund` và giữ bằng chứng. | Tùng quyết dừng, Oanh đối soát. |
| Lỗi ghi oan cho hãng / lộ dữ liệu cá nhân (pháp lý) | `wrongful_carrier_faults`, `pii_leaks` | Hồ sơ hãng có căn cứ theo kiện, thông báo chỉ có trường được phép. | Có khiếu nại hoặc nghi lộ thông tin. Kiểm tracking và bản thông báo nội bộ. | Xác nhận ghi oan thì dừng `file_carrier_fault`. Xác nhận lộ dữ liệu thì dừng `notify_carrier`, cô lập bản ghi và báo đầu mối phụ trách. | Tùng quyết dừng, Oanh đối soát vụ việc. |
| Tỉ lệ ca cần người xem | `review_rate`, `ops.queue.queued_per_day` | Ca chuyển người và kiểm mẫu nằm trong năng lực trực. | Tải dự kiến sắp chạm công suất. Xác định phần tăng do chuyển người hay do kiểm lại. | Hàng chờ tiếp tục tăng và dự kiến vi phạm SLA dù đã gọi hỗ trợ. Đề xuất thu hẹp phạm vi với TV2. | Hạnh điều phối, Tùng quyết phạm vi. |

#### Runbook 3 · Điều kiện dừng và cách dừng

- **Dừng một phần.** Hoàn sai vượt ngưỡng đã ký thì tạm tắt `issue_refund`. Xác nhận ghi oan thì tắt `file_carrier_fault`. Xác nhận lộ PII thì tắt `notify_carrier` và bàn giao thông báo cần gửi cho người. Nếu hàng chờ vượt hạn dù đã bổ sung hỗ trợ, Tùng cùng TV2 chốt phạm vi có thể phục vụ.
- **Dừng hẳn.** Tùng dừng đưa ticket mới vào trợ lý và chuyển sang CSKH làm tay khi sự cố lan qua nhiều thao tác hoặc chưa cô lập được đường ghi gây hại. Giữ mã ticket, giờ, thao tác và bằng chứng đã che PII.
- **Cách dừng.** Người thấy tín hiệu đỏ báo vào kênh trực. `NV-TUNG` đặt khóa tương ứng trong `config/switches.json` thành `off` và xác nhận lệnh ghi đã dừng. Khi thu hẹp, cập nhật phạm vi đã duyệt ở `business.pilot_scope`. Ghi lại điều kiện đã kích hoạt để đối chiếu `operations.stop_conditions`.
- **Hạn để dừng.** Từ tín hiệu đỏ đến khi xác nhận dừng tối đa [nhóm chốt số phút qua diễn tập]. Người bấm là `NV-TUNG`.
- **Ticket đang chờ.** `NV-HANH` chuyển ca tồn sang CSKH làm tay và báo bước tiếp theo cho khách. Kiểm sổ trước khi hoàn tay vì tiền có thể đã ghi trước lúc dừng ghi lỗi hãng. `NV-OANH` đối soát giao dịch hoặc thông báo đã phát sinh.
- **Bật lại.** `NV-TUNG` duyệt sau khi `NV-HANH` xác nhận ca tồn có người xử lý, `NV-OANH` đối soát phần bị ảnh hưởng và TV1 kiểm lỗi đã được chặn, các ca nền đang đúng vẫn đúng. Theo dõi lại hàng chờ và thao tác vừa mở.

### B7.6 · Giờ cao điểm (bắt buộc với thẻ S4; các thẻ khác nên có)

Lượng ticket có thể dồn gấp ba trong một giờ (ngày sale, sau bão). Viết trước, khi chưa biết sự cố.

| Câu hỏi | Trả lời (có số, có tên) |
|---|---|
| Giờ cao điểm là khi nào, bao nhiêu ticket mỗi giờ (dựa vào `ops_facts`)? | Giả lập một giờ sau sale hoặc sau bão với lượng vào gấp 3 lần giờ thường. Chờ TV2 cung cấp ticket/giờ trong phạm vi pilot. So tải cần người duyệt với 6 ca chuẩn/giờ/người. |
| Ai trực giờ cao điểm, mấy người (khớp `operations.reviewers_on_shift`)? | `NV-HANH` điều phối. Chờ chốt số người trong `operations.reviewers_on_shift` và người dự phòng. |
| Ngưỡng nào thì **gọi thêm người** (hàng chờ bao nhiêu ca, chờ lâu nhất bao nhiêu phút)? Ai gọi? | `NV-HANH` gọi khi hàng chờ đạt [ngưỡng ca] hoặc ca chờ lâu nhất đạt [ngưỡng phút], trước SLA 60 phút. Chốt ngưỡng dựa trên thời gian người dự phòng có mặt. |
| Ngưỡng nào thì **thu hẹp** phạm vi (khoá `business.pilot_scope`) hoặc **tắt** một thao tác ghi (`config/switches.json`)? Ai quyết? | `NV-TUNG` quyết thu hẹp với TV2 nếu dự báo vượt hạn dù đã bổ sung người. Ticket ngoài phạm vi chuyển CSKH. Tín hiệu đỏ về tiền hoặc pháp lý xử lý theo Runbook 3. |
| Thêm người thì chi phí mỗi ticket và ROI thay đổi thế nào (đọc report)? | Theo `ops_facts`, thêm một người làm phí giữ chỗ tăng 30.000đ/ca và công suất vật lý tăng 6 ca chuẩn/giờ. So `cost_per_ticket_vnd`, `roi`, `queue_wait_max_min` và `queue_stuck` ở hai lần chạy cùng bộ ticket và phạm vi, chỉ đổi số người. Chờ mã lần chạy. |

---

<a id="b8"></a>

## B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 (phút 105–115)

Làm đúng thứ tự:

```bash
python3 -m lab10.checkpoint
python3 -m lab10.eval --suite base --stage prepared
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

**Khung tư duy.** Gate 1 "đạt" khi **quyết định khớp bằng chứng và khớp tiêu chí đã ký trước**. Tiếp tục, Thu hẹp, Cải tiến
thêm, Dừng đều có thể là quyết định đạt. Quyết định không đạt là quyết định mà con số trong report không đỡ được.
Chỉ chọn Tiếp tục khi mọi chỉ số bắt buộc đều đạt.

Ba câu tự vấn trước khi viết: (1) Rủi ro còn lại có chấp nhận được như hiện trạng không? (2) Cần thêm biện pháp nào, tốn
bao nhiêu thời gian? (3) Có phần nào của dự án không nên làm tiếp?

| | **v1** (phút 105–115, TRƯỚC khi nhận thẻ sự cố) |
|---|---|
| Commit ký tiêu chí (message `Sign acceptance criteria`; hash commit, tuỳ chọn) | |
| Hash chốt cổng vòng 1 (8 ký tự lệnh `lab10.checkpoint` in ra, tuỳ chọn) | |
| Mã lần chạy dùng làm bằng chứng | bộ nền, mốc base: ________ · bộ nền với cổng vòng 1 (prepared): ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Đọc khối "theo kho và hãng" ở cuối output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt phần nào, vì sao | |
| Nếu Cải tiến thêm: giả thuyết cụ thể + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Một bằng chứng còn thiếu (thứ bộ nền chưa đo được) | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

Xong v1 thì lưu và đẩy một bản (sau mốc này không sửa cột v1):

```bash
git add lab10/guards.py lab10/guards_round1.py config/operating_gates.json config/operating_gates.round1.json config/round1.lock templates/form-b-evaluation-gates.md
git commit -m "LAB 10: chốt cổng vòng 1, quyết định v1"
git push -u origin main
```
