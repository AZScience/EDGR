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

**Mặc định:** Streamlit **nhúng UI React gốc** (iframe FastAPI `/ui/`) — layout/CSS/chức năng **y hệt** SPA.  
**Tuỳ chọn sidebar:** «Streamlit native» = bản widget gần đúng (không pixel-perfect).

```powershell
cd d:\DemoTiensi\frontend
npx vite build

cd d:\DemoTiensi\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8016

cd d:\DemoTiensi
python -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

- Streamlit (React embed): http://127.0.0.1:8501  
- React SPA trực tiếp: http://127.0.0.1:8016/ui/ hoặc Vite http://127.0.0.1:5180  
- API docs: http://127.0.0.1:8016/docs  

> Streamlit Community Cloud **không** công khai cổng FastAPI đi kèm → với chế độ React embed, dùng local / Docker / Railway (API+`/ui/`). Trên Cloud hãy chọn sidebar **Streamlit native**.

### Deploy Streamlit Community Cloud (native UI)

1. Repo: https://github.com/AZScience/EDGR (branch `kiemtranoibo`)
2. [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Main file: `streamlit_app.py`
4. Python requirements: `requirements.txt` (root)
5. **Advanced settings → Python version: chọn 3.11 hoặc 3.12** (không dùng 3.14 — `numpy`/`scikit-learn` dễ treo lúc `uv pip install`)
6. Deploy — Cloud tự dùng **Streamlit native** (React iframe cần FastAPI localhost, không public được)

> `runtime.txt` / `.python-version` **không** đổi Python trên Community Cloud — chỉ đổi trong dashboard Settings → Advanced.
