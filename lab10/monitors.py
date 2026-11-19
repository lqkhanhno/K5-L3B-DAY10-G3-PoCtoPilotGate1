"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _event(t, kind):
    return next((e for e in t.get("events", []) if e.get("type") == kind), None)


def unpinned_policy_rate(trials):
    """VÒNG 2 · thẻ S3 (concept drift, kỹ thuật): tỉ lệ ticket mà agent KHÔNG được ghim phiên bản chính sách theo ngày hiệu lực,
    tức là tự rơi về bản `index_active` (bản sao có thể cũ). Gần 0 khi cổng ghim hoạt động; vọt lên khi chính sách đổi mà
    bản sao chưa đổi hoặc khi cổng ghim bị gỡ."""
    seen = [e for e in (_event(t, "policy") for t in trials) if e is not None]
    return sum(not e.get("pinned") for e in seen) / max(1, len(seen))


def fault_on_unlicensed_cause_rate(trials):
    """VÒNG 2 · thẻ S3 (pháp lý và vận hành với hãng): trong các ticket có ghi lỗi cho hãng, tỉ lệ kiện mà tracking ghi nguyên nhân
    là bất khả kháng (bão, lũ) hoặc chưa ghi nguyên nhân. Hãng bị phạt oan khi chỉ số này khác 0; tách ra từ sổ lỗi hãng."""
    filed = [t for t in trials if t.get("faults")]
    bad = 0
    for t in filed:
        tr = _event(t, "tracking") or {}
        if tr.get("cause") != "CARRIER" or not tr.get("cause_recorded", True):
            bad += 1
    return bad / max(1, len(filed))


def carrier_days_over_strike_cap(trials, cap=2):
    """VÒNG 2 · thẻ S3 (vận hành): số cặp (hãng, ngày giả lập, seed) có quá `cap` lỗi tự động trong một ngày; trần Ops là 2,
    từ lỗi thứ 3 phải có người duyệt. Đếm từ sổ lỗi hãng của từng ticket, không theo lời agent."""
    count = {}
    for t in trials:
        for f in t.get("faults", []):
            key = (f.get("carrier_id"), t.get("day"), t.get("seed"))
            count[key] = count.get(key, 0) + 1
    return sum(n > cap for n in count.values())


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "unpinned_policy_rate": unpinned_policy_rate,
    "fault_on_unlicensed_cause_rate": fault_on_unlicensed_cause_rate,
    "carrier_days_over_strike_cap": carrier_days_over_strike_cap,
}
STARTER_MONITORS = ("escalation_rate",)
