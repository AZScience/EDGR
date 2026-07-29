# EDGR — PhD Research Pipeline (16 bước A→Z)

**An Evidence-Driven Dynamic Graph Retrieval Algorithm for Hallucination Mitigation in Large Language Models for Intrusion Detection and Cyber Threat Intelligence.**

Ứng dụng dạng **pipeline 16 tab** (đúng sơ đồ quy trình); mỗi tab có **pipeline công việc con**. Mọi nút gọi API và tính toán thật trên KG/vector store demo.

## 16 bước

| # | Bước | Công việc chính |
|---|---|---|
| 1 | Khảo sát tài liệu | RAG, GraphRAG, KG, Hallucination, CTI, IDS/NIDS, Catalog APA, Ma trận |
| 2 | Xác định khoảng trống | Phương pháp, Hạn chế, Gaps, Đóng góp |
| 3 | Xây dựng bài toán | I/O, Mô hình hóa, Mục tiêu |
| 4 | Đề xuất EDGR | 6 bước thuật toán + full |
| 5 | Dynamic Knowledge Graph | Nguồn, Trích xuất, Incremental, Lưu trữ |
| 6 | Hallucination Scoring | R / F / G / S + Score 0–1 |
| 7 | Xây dựng dữ liệu | MITRE, CVE, CWE, CISA, Feeds, IDS → QA |
| 8 | Triển khai hệ thống | Architecture, KG, Vector, LLM, E2E |
| 9 | Thực nghiệm & So sánh | RAG…CRAG vs EDGR (baseline = family stub cùng store) |
| 10 | Đánh giá | Accuracy, F1, Faithfulness, Hall, P@k/MRR, Latency, Resource |
| 11 | Ablation Study | w/o Temporal / Graph / Trust / Ranking / Scoring |
| 12 | Phân tích thuật toán | Time, Space, Correctness, Convergence, Scalability |
| 13 | Công bố khoa học | 4 papers (EDGR, DKG, Scoring, Evaluation) |
| 14 | Viết luận án | 8 chương (outline + live artifacts) |
| 15 | Bảo vệ luận án | Present, Defend Q&A, Checklist, Success |
| 16 | Ứng dụng thực tế | IDS/CTI console — `/api/app/analyze` live EDGR |

## Chạy

```powershell
cd d:\DemoTiensi\backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8015

cd d:\DemoTiensi\frontend
npm run dev -- --host 127.0.0.1 --port 5180
```

- UI: http://127.0.0.1:5180  
- API: http://127.0.0.1:8015/docs  

```
GET  /api/pipeline
GET  /api/pipeline/{step_id}/academic
GET  /api/pipeline/{step_id}/{task_id}/academic
POST /api/pipeline/{step_id}/{task_id}/run
GET  /api/app/status
POST /api/app/analyze
POST /api/app/alerts
```

Mỗi tab cha/con (trừ Step 16 app) có khung học thuật: CSDL · Mô hình toán · Mô hình thuật toán · Mô hình hoạt động · Trích dẫn · Minh chứng · Nhận định đánh giá.

## Streamlit

**Mục tiêu:** UI **giống hệt React local** → Streamlit chỉ iframe SPA thật (không mock widget).

### Local (pixel-perfect)

```powershell
cd d:\DemoTiensi\frontend
npx vite build

cd d:\DemoTiensi\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8016

cd d:\DemoTiensi
python -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

- Streamlit (React iframe): http://127.0.0.1:8501  
- React trực tiếp: http://127.0.0.1:8016/ui/ hoặc Vite http://127.0.0.1:5180  
- API docs: http://127.0.0.1:8016/docs  

### Streamlit Cloud — giống React local (bắt buộc host `/ui/` công khai)

Streamlit Cloud **không** mở được `127.0.0.1`. Cần 2 bước:

**1) Deploy FastAPI + React (`Dockerfile` ở root)** lên Railway / Render / Fly:

```powershell
cd d:\DemoTiensi\frontend
npx vite build
# Commit frontend/dist nếu chưa có, rồi deploy Docker image từ root Dockerfile
```

Kiểm tra: `https://YOUR-HOST/ui/` phải giống UI React local, `https://YOUR-HOST/api/health` → `ok`.

**2) Streamlit Cloud → Settings → Secrets:**

```toml
EDGR_PUBLIC_UI_URL = "https://YOUR-HOST/ui/"
```

Reboot app → Streamlit nhúng đúng SPA React (cùng CSS/layout/API).

> Python trên Cloud: Advanced settings chọn **3.11 hoặc 3.12** (tránh 3.14).  
> Fallback tạm: sidebar «Streamlit native» nếu chưa có `EDGR_PUBLIC_UI_URL`.

Ví dụ secrets: xem `.streamlit/secrets.toml.example`.
