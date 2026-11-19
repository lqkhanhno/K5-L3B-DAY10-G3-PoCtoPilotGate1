"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Vòng 1: ba cổng ở dưới (issue_refund, file_carrier_fault, notify_carrier); lệnh ghi khác cho qua.
"""
from . import helpers as H
from .tools import Verdict

# VÒNG 1: ba cổng phòng ngừa, đều so với NGUỒN SỰ THẬT (đơn, tracking, chính sách hiệu lực), không đọc chữ khách viết.
#   1. issue_refund       : số tiền không vượt quyền lợi tính từ DB; không ghi đôi; payer và phê duyệt hợp lệ.
#   2. file_carrier_fault : chỉ ghi lỗi cho kiện thật sự trễ vì lỗi hãng theo tracking.
#   3. notify_carrier     : chỉ gửi cho hãng các trường được chính sách cho phép (allowlist), không gửi PII.

_OVERRIDE_EVENTS = ("model_override", "directive_obeyed")


def _facts(ctx, order_id):
    """(order, policy) lấy từ nguồn sự thật; None nếu thiếu."""
    return ctx.tools.lookup_order(order_id), H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _untrusted_input_used(ctx):
    """Agent đã dùng số/chỉ thị do khách viết, hoặc rơi về fail_open khi LLM lỗi."""
    for e in ctx.events:
        if e.get("type") in _OVERRIDE_EVENTS:
            return True
        if e.get("type") == "proposal" and e.get("basis") == "fail_open":
            return True
    return False


def _approval_ok(ctx, action):
    ap_id = action.get("approval_id")
    if not ap_id:
        return False
    rows = ctx.tools.lookup_approvals(approval_id=ap_id)
    if not rows:
        return False
    a = rows[0]
    return (a.get("status") == "valid" and a.get("order_id") == action.get("order_id")
            and a.get("expires_at", "") >= ctx.as_of and action.get("amount_vnd", 0) <= a.get("max_vnd", 0))


def _gate_refund(ctx, action):
    order, policy = _facts(ctx, action.get("order_id"))
    if order is None or policy is None:
        return Verdict.escalate("không đủ dữ liệu nguồn (đơn hoặc chính sách hiệu lực) để kiểm tra khoản hoàn")
    amount = action.get("amount_vnd", 0)
    if action.get("payer", "LOGIX") != "LOGIX" and not _approval_ok(ctx, action):
        ctx.log("refund_payer_blocked", payer=action.get("payer"))
        return Verdict.escalate("khoản hoàn trừ vào bên khác (shop) mà không có phê duyệt hợp lệ")
    if amount > policy["auto_limit_vnd"] and not _approval_ok(ctx, action):
        ctx.log("refund_approval_invalid", approval_id=action.get("approval_id"))
        return Verdict.escalate("khoản vượt hạn mức tự động nhưng phê duyệt thiếu, hết hạn hoặc không khớp đơn")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    cause = parcel.get("delay_cause") or ("CARRIER" if delay > 0 else None)
    entitled = H.entitlement_vnd(policy, order, delay, cause)
    already = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
    remaining = max(0, entitled - already)
    if amount <= remaining:
        return Verdict.allow()
    ctx.log("refund_over_entitlement", asked=amount, entitled=entitled, already=already, db_delay_days=delay)
    if _untrusted_input_used(ctx):
        return Verdict.escalate(f"số tiền {amount}đ vượt quyền lợi theo DB ({remaining}đ) và agent dựa vào đầu vào do khách viết: chuyển người")
    if remaining <= 0:
        return Verdict.deny(f"không còn quyền lợi hoàn theo DB (đã hoàn {already}đ / quyền lợi {entitled}đ)")
    return Verdict.modify(f"giảm số tiền về quyền lợi còn lại theo DB ({remaining}đ)", amount_vnd=remaining)


def _gate_fault(ctx, action):
    order, policy = _facts(ctx, action.get("order_id"))
    if order is None or policy is None:
        return Verdict.deny("thiếu dữ liệu nguồn để chứng minh lỗi hãng")

    def at_fault(p):
        return H.carrier_at_fault(policy, p, H.db_delay_days(p, ctx.as_of))

    given = next((p for p in order["parcels"] if p["parcel_id"] == action.get("parcel_id")), None)
    target = given if given is not None and at_fault(given) else None
    if target is None:                                   # agent lấy kiện đầu tiên: thử đúng kiện ticket nói tới
        cand = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        target = cand if at_fault(cand) else None
    if target is None:
        ctx.log("carrier_fault_blocked", parcel_id=action.get("parcel_id"))
        return Verdict.deny("tracking không ghi nguyên nhân thuộc lỗi hãng hoặc chưa đủ ngày trễ: không ghi lỗi cho hãng")
    truth = {"parcel_id": target["parcel_id"], "carrier_id": target["carrier_id"], "driver_id": target.get("driver_id"),
             "delay_days": H.db_delay_days(target, ctx.as_of)}
    changes = {k: v for k, v in truth.items() if action.get(k) != v}
    return Verdict.modify("chỉnh lỗi hãng theo kiện và số ngày trễ trong tracking", **changes) if changes else Verdict.allow()


def _gate_notify(ctx, action):
    _, policy = _facts(ctx, action.get("order_id"))
    payload = action.get("payload") or {}
    allowed = set(policy["carrier_notice_fields"]) if policy else {"order_id", "parcel_id", "delay_days"}
    kept = {k: v for k, v in payload.items() if k in allowed}
    dropped = sorted(set(payload) - allowed)
    if not dropped:
        return Verdict.allow()
    ctx.log("carrier_notice_trimmed", dropped=dropped)
    return Verdict.modify("chỉ gửi hãng các trường được chính sách cho phép, bỏ dữ liệu cá nhân và chữ khách viết", payload=kept)


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()
