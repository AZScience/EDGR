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

## Streamlit — giống local React 100%

Streamlit **widget native không bao giờ** bằng React local (banner, tab cha/con, CSS).

**Cách đúng (pixel-perfect):**

1. Deploy `render.yaml` / `Dockerfile` lên [Render](https://dashboard.render.com) (Blueprint, branch `kiemtranoibo`)
2. Mở `https://YOUR-HOST/ui/` — phải giống React local
3. Streamlit Cloud → Secrets:
   ```toml
   EDGR_PUBLIC_UI_URL = "https://YOUR-HOST/ui/"
   ```
4. Reboot → Streamlit chỉ iframe SPA React thật

**Local:** FastAPI `:8016/ui/` + Streamlit embed (không cần secret).

Chi tiết / fallback native: xem mục Streamlit bên dưới trong lịch sử README cũ hoặc trang hướng dẫn trong app Cloud.
