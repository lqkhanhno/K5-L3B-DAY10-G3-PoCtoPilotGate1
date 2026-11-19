# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `G3`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-G3-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đoàn Đăng Khoa | 2A202603766 | Kỹ sư cổng |  |
|   2 | Vũ Đình Thắng | 2A202603753 | Sản phẩm và kinh doanh |  |
|   3 | Lê Quốc Khánh | 2A202603742 | Vận hành và pháp lý |  |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## LeQuocKhanh-2A202603742

### Phần việc phụ trách

Trưởng nhóm, phụ trách vận hành và pháp lý. Soạn mục tiêu đối soát và duyệt ca ở A1, tín hiệu lộ dữ liệu ở A2, HAZOP, checklist và runbook ở B4–B7. Đối chiếu danh sách thành viên với hồ sơ nộp.

### Đóng góp cụ thể

Đã dùng Codex để gộp nhánh, đối chiếu README, rà các chỗ mâu thuẫn giữa Phiếu A/B và config, và đồng bộ tên người phụ trách theo bảng thành viên.

### Bằng chứng

Bản nháp vận hành ở commit `5ad6a40`. Xem Phiếu A mục A1–A2 và Phiếu B mục B4–B7.

### Exit ticket

*(Lê Quốc Khánh tự điền sau buổi lab.)*

## VuDinhThang-2A202603753

### Phần việc phụ trách

Vai Sản phẩm và kinh doanh. Vòng 1: soạn tiêu chí chấp nhận (Phiếu A), cổng business và các mục B3, B6, B7.4 của Phiếu B; nâng `pass_rate_min` lên 0.93 và `pass_k_min` lên 0.86, viết bốn dòng `decision_rule` loại trừ nhau và phủ đủ trường hợp; ký tiêu chí trước lần đo đầu tiên. Vòng 2 (thẻ S3): ghim chính sách theo ngày, đặt trần 2 lỗi hãng mỗi ngày, thêm 3 chỉ số theo dõi, điền mục kỹ thuật của Phiếu C, C11, C12 (quyết định v2 giữ **Thu hẹp**) và `submission/submission.json`.

### Đóng góp cụ thể

- Chọn PRD v1.1 và eval card của Lab 9 làm tài liệu chung, bám PRD §2, §3, §6 khi viết câu 1.1 và 1.2.
- Ký tiêu chí ở commit `1354c4d` (15:41:05), sau đó sửa tham chiếu ở A5 và B5 dòng 9 từ `f07df1a` thành `1354c4d` cho khớp lịch sử git.
- Nhận thẻ S3 và đưa dữ liệu sự cố vào repo (`incidents/S3`).
- Sửa cổng ở `lab10/guards.py` và thêm `lab10/monitors.py` cho S3.
- Viết ba câu `three_lines` chép từ C12: giả định môi trường (`delay_cause` do hãng nhập có thể trống hoặc khai bão), điều cổng ngăn được và chỉ giảm được (chi phí tăng lên 6.038đ/ticket khi chuyển cả khoản hoàn sang người), và điều cần đo lại trong pilot.
- Sửa B8 và C12 về nhóm kho `?`: `pilot_scope` không loại được nhóm này nên cắt bằng quy trình, rồi gom lại `submission/`.

### Bằng chứng

Commit `a43b890`, `fe30377`, `18756df`, `1354c4d`, `3a24954` (vòng 1); `aabc4fa`, `c863785`, `cf03333`, `3070f3e`, `e4fa669` (vòng 2). Xem Phiếu A, Phiếu B mục B3, B6, B7.4, B8, Phiếu C mục C11, C12 và `submission/submission.json`.

### Exit ticket

*(Vũ Đình Thắng tự điền sau buổi lab.)*
