# Astur — Window Trace State Reconciliation (2026-11-07)

## Trạng thái và phạm vi

- Branch triển khai: `feat/astur-window-state-reconcile-20261107`; worktree: `D:\Project\Astur-window-state-reconcile-20261107`.
- Baseline source ban đầu: `feat/astur-pinned-overlay-20261106` tại `947544ee626f6de69aea11b4ee27d17d8c72a26e`, dựa trên native-drag `6bf0a2cffc20a868dea9a7e7aa2a3e1850353fed`. Sau checkpoint `e902f23`, nhánh pinned upstream đã tiến tới `86a95b7954379bd788bbe56bb6b76643a24167d9`; hợp nhất qua merge thường (không rewrite lịch sử), giữ lại các bản sửa upstream về CI, Clippy và membership workspace ẩn.
- Binary trên máy tại thời điểm P0: `C:\Users\Vu Tuan\AppData\Local\Programs\Astur\Astur.exe`, SHA-256 `D13CEA702666994C490DE19BE8AB0ED1500BA312D54FAE95F3E9C82ED8C5EE38`, PID `41796`. FileVersion metadata không khai báo. **Không suy ra source commit từ SHA này**.
- Không restart, thay cấu hình, cài đặt, di chuyển cửa sổ thật hoặc can thiệp MT5/SignalOps; dữ liệu trace gốc và titles/chat không đưa lên Git.
- Gate cuối vẫn là desktop acceptance trên phiên Windows thử nghiệm riêng, không phải desktop đang chạy broker.

## Evidence và lỗi

Báo cáo audit đã xác định Telegram HWND 133652 nhận FOREGROUND lúc 13:55:10.306 nhưng còn tại vị trí park `(480,1355)`, `visible=true`, `minimized=false`, và chỉ lên màn hình lúc 13:55:43.173. Tọa độ khớp `park_spot()`. Đây là **runtime symptom confirmed**; chưa chứng minh exact command path trên binary live, vì binary chưa được source-map.

Các source gaps trên PR #13: `strip_reveal` trả về khi thiếu slot membership; BarFocus/ActivateWindow/FocusMouse và hidden-workspace transitions lệch nhau; minimize cập nhật `ws.focused` nhưng không đồng bộ `overlay.active`; `refresh_monitors` chỉ giữ `Strip`; layout switch giữ overlay cũ.

## Code scope

1. `PinnedOverlay::reconcile_members`: tái cấu trúc membership giữ nguyên slot cho HWND còn tồn tại, bỏ ghost/duplicate, admit HWND re-homed; không chạm floating.
2. `PinnedOverlay::minimize_successor`: real minimize giữ HWND trong reserved slot, thay active member nếu có; kế nhiệm cùng slot trước các slot khác/background.
3. `strip_reveal`: reconcile model và physical placement; không silent-return cho HWND managed/tiled thiếu membership; nếu đang park, dùng retile instant. Giữ quy tắc background native và scratchpad.
4. `Cmd::ActivateWindow`, `Cmd::Focused`, `BarFocus`, `FocusMouse`, `BarClick`: mọi explicit activation đi qua reveal/restore chung, kể cả sau hidden-workspace switch; synthetic focus guard không được ngăn phục hồi pinned HWND vật lý còn park.
5. `refresh_monitors`: snapshot `PinnedOverlay`, strip và focused HWND; khôi phục theo surviving HMONITOR sau re-home, xác thực external native background, rồi retile.
6. `set_monitor_layout`: giải phóng overlay khi rời scrolling để không giữ slot cũ.
7. Thêm unit tests pure overlay state và debug log không có title/content, chỉ HWND/monitor/ws/slot/visibility/parked.

## Gates không được bỏ

- Windows: `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace`, `cargo build --release --workspace`, các Python self-tests của CI.
- Local toolchain tồn tại (`cargo 1.99.1`, `rustc 1.99.1`) nhưng `cargo test -p astur --locked` đầu tiên bị **environment blocker** `link.exe not found` (MSVC linker không trong môi trường). Không gọi đây là code FAIL hoặc PASS.
- CI đầu tiên trên `e902f23` FAIL ở `Clippy`: `E0599` do upstream mới thêm `#[cfg(test)]` cho `PinnedOverlay::valid`, trong khi `reconcile_members` gọi method này ở production. Đã chẩn đoán từ job #128365307822, sửa theo đúng source merge. CI phải có fresh evidence trên commit cuối; không dùng PASS của source branch cũ.
- Codex CLI (`gpt-6-luna`, `--sandbox read-only`) lần đầu phát hiện `Cmd::Focused` thiếu reveal sau hidden-workspace switch: đã sửa trong cùng lifecycle, thêm regression test cho focus guard. Lần review lại trên `a40592d` không tìm ra P0/P1 mới, nhưng hai reviewer lane phụ không chạy được; **không tuyên bố independent-review PASS**.
- Fresh Windows CI trên `a40592d7d9ea69d98e9e8795c27f21015cf12b8a` (Actions run `42551633462`) PASS: format, translation contract, packaging safety, notification diagnostics, Clippy `-D warnings`, `cargo test --workspace`, `cargo build --release --workspace`. Đây là bằng chứng build/test code trước thay đổi workflow xuất bản QA artifact, chưa thay cho CI trên commit cuối.
- Windows CI trên `dc874225c4bf9961056379d93eb9003709b7ad87` (run `42552080324`) PASS: 354 tests, 0 failed, 3 ignored; Clippy, release build và upload QA portable đều PASS. Artifact `13645513931` đã tạo, nhưng tên dùng SHA merge tạm của PR (`4fab10c...`), không phải SHA source head. Workflow mới ghi cả `CheckoutMergeSha` và `SourceHeadSha`, và đặt tên QA artifact theo source head để bảo toàn provenance; **fresh CI trên commit cuối mới là gate**. Gói chỉ chứa `astur.exe`, `astur-settings.exe`, checksum SHA-256, provenance và checklist; không phải installer/release, không được chạy đồng thời với Astur live hoặc MT5.
- A01–A14 trong `docs/vi/PINNED_OVERLAY_QA_ACCEPTANCE_20261106.md` vẫn bắt buộc trên disposable Windows session. Bổ sung trace check: không `FOREGROUND && !IsIconic && parked` sau settle, không ghost/duplicate slot, CS1 không tự minimize hàng xóm, CS1→CS2 drag và cross-monitor ổn định.
- Không đóng gói installer, promote, merge hoặc tự cài trước khi desktop gate PASS.

## Resume / rollback

- Primary writer là CodeLocal, không ghi song song `main.rs`.
- So sánh với PR #13 và #12, review độc lập, xử lý defect rồi **fresh verify sau thay đổi cuối**.
- Rollback source là commit `947544e` trên nhánh pinned-overlay gốc; executable live không đổi. Không force-push/rewrite.
- Trạng thái tài liệu này được cập nhật bằng fresh evidence khi kết thúc checkpoint. Không dùng nó như bằng chứng rằng runtime đã PASS.
