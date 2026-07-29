# EDGR: Truy hồi đồ thị động dựa trên bằng chứng và cổng rủi ro ảo giác cho phát hiện xâm nhập và tình báo mối đe dọa mạng

**Tác giả:** Nguyễn Vĩnh Phúc  
**Đơn vị:** Nguyên mẫu nghiên cứu tiến sĩ — Evidence-Driven Dynamic Graph Retrieval (EDGR)  
**Liên hệ:** ngviphuc@gmail.com  
**Phiên bản:** Bản thảo hoàn chỉnh (đánh giá quy mô demo, tái lập được trên pipeline kèm theo)

---

## Tóm tắt

Các mô hình ngôn ngữ lớn (LLM) dùng làm trợ lý tình báo mối đe dọa mạng (CTI) thường đưa ra định danh CVE, kỹ thuật ATT&CK hay quan hệ actor–malware trông hợp lý nhưng không được bằng chứng truy hồi hỗ trợ. RAG cổ điển giảm kiến thức tham số lỗi thời nhưng xếp hạng đoạn văn phẳng và thường chỉ đo faithfulness sau khi đã sinh câu trả lời. Graph-RAG mã hóa quan hệ tốt hơn, song hầu hết hệ thống vẫn thiếu toán tử từ chối trước khi phát tán, được hiệu chỉnh theo rủi ro CTI.

Chúng tôi trình bày **EDGR** (*Evidence-Driven Dynamic Graph Retrieval*) — một pipeline thống nhất gộp bốn đóng góp: (i) **Dynamic Knowledge Graph (DKG)** cho CTI với cập nhật gia tăng và siêu dữ liệu thời gian; (ii) **thuật toán truy hồi sáu giai đoạn** từ trích thực thể đến chọn câu trả lời tin cậy; (iii) **điểm rủi ro ảo giác bốn yếu tố** \(\tau=0.30R+0.20F+0.25G+0.25S\), \(\rho=1-\tau\), kèm ngưỡng \(\theta\) và toán tử **abstain**; (iv) **protocol đánh giá tái lập được** (faithfulness, hallucination rate, P@k, R@k, MRR, latency và ablation) trên bộ câu hỏi IDS/CTI neo MITRE ATT&CK, CVE/NVD và các feed liên quan.

Trên bộ đánh giá seed quy mô lớn hơn (\(N\ge 48\) cặp QA: multi-hop/temporal/IDS/KEV/OOD có chọn lọc + câu hỏi quan hệ suy từ đồ thị; \(\ge 40\) evidence chunk; KG CTI mở rộng), chúng tôi đánh giá EDGR theo **giả thuyết H1–H4**, kèm **bootstrap CI**, **McNemar**, **ablation dataset**, **threats-to-validity**, và **protocol đánh giá người SOC** (hai annotator, thang Likert, **Cohen’s \(\kappa\)**; demo có panel `seed_soc_panel` được disclosure, kèm API nhận nhãn SOC hiện trường). Stub đồ thị vẫn có thể thắng trên proxy faithfulness khi trùng gold dày; tuyên bố đặc trưng là **hợp đồng Trusted Answer** (ρ-gate + abstain) đồng thiết kế với KG động — không phải «GraphRAG cộng module». Không claim SOTA benchmark lớn; claim protocol khoa học tái lập được cho luận án TS và diễn đàn chuyên ngành quốc tế.

**Từ khóa:** retrieval-augmented generation; knowledge graph; hallucination; cyber threat intelligence; intrusion detection; risk gate; abstain

---

## 1. Mở đầu

Trung tâm điều hành an ninh (SOC) ngày càng đặt câu hỏi ngôn ngữ tự nhiên dạng *“Những kỹ thuật ATT&CK nào liên quan CVE-2021-44228 (Log4Shell) và cách phát hiện?”*. Một câu trả lời bịa kỹ thuật hoặc gắn nhầm actor–malware có thể đẩy hướng xử lý sự cố sai. LLM thuần tham số không đủ tin cậy: tri thức CTI thay đổi theo CVE và chiến dịch mới, và định danh bịa đặt đặc biệt đắt giá.

RAG [Lewis et al., 2020] neo sinh trên tài liệu ngoài. Các survey về RAG và ảo giác LLM [Gao et al., 2024; Ji et al., 2023] cho thấy neo bằng chứng giảm — nhưng không loại trừ — mệnh đề không được hỗ trợ. Trong CTI còn hai khoảng trống cấu trúc. Thứ nhất, tri thức đe dọa mang tính **quan hệ** (CVE–technique–tactic, actor–malware). Xếp hạng đoạn văn phẳng không mã hóa cạnh mà chuyên gia dùng. Thứ hai, faithfulness thường là metric hậu kỳ chứ không phải **tín hiệu điều khiển** có thể từ chối trả lời.

Graph-RAG (GraphRAG, LightRAG, HippoRAG) cải thiện truy hồi đa bước; pipeline phản tư (Self-RAG, CRAG) hiệu chỉnh retrieval khi độ tin cậy sinh thấp. Các hướng này hiếm khi kết hợp (a) **đồ thị CTI động** có timestamp và độ tin cậy nguồn, (b) **điểm rủi ro đa yếu tố minh bạch**, và (c) **cổng abstain cứng** trước khi phát tán khi rủi ro vượt ngưỡng hoặc định danh truy vấn không được hỗ trợ.

**Đóng góp.** Bài báo trình bày một bản tường thuật khoa học hoàn chỉnh về EDGR:

1. **Dynamic CTI Knowledge Graph** — schema, ingest đa nguồn, cập nhật gia tăng \(G_{t+1}=G_t\oplus(\Delta V,\Delta E)\), và giao diện expand/temporal cho truy hồi.
2. **Thuật toán EDGR** — sáu giai đoạn \(\varphi_1,\ldots,\varphi_6\) từ trích thực thể đến chọn bằng chứng tin cậy và trả lời có neo.
3. **Chấm điểm ảo giác và ρ-gate** — trust \(\tau\) từ reliability, freshness, graph consistency và semantic relevance; risk \(\rho=1-\tau\); chỉ phát khi \(\rho<\theta\) (mặc định \(\theta=0.55\)) và CVE truy vấn xuất hiện trong evidence; ngược lại abstain.
4. **Đánh giá toàn diện** — protocol, baseline trên cùng store, metric và ablation gắn từng module với faithfulness quan sát được.

---

## 2. Nghiên cứu liên quan

**RAG cổ điển.** Lewis et al. [2020] đặt nền retrieve-then-generate. Gao et al. [2024] survey kiến trúc, huấn luyện và đánh giá. Hệ thống này mạnh về neo từ vựng nhưng coi evidence như túi đoạn không có cấu trúc cạnh.

**Graph-augmented RAG.** Edge et al. [2024], Guo et al. [2024], Gutiérrez et al. [2024] khai thác cấu trúc thực thể–quan hệ. Chúng truyền cảm hứng cho giai đoạn Expand của EDGR, nhưng thường tối ưu chất lượng retrieval hơn là cổng từ chối chuyên CTI.

**Reflective / corrective retrieval.** Asai et al. [2024] và Yan et al. [2024] đưa vòng phê bình hoặc sửa retrieval. EDGR áp dụng rủi ro vô hướng \(\rho\) với ngưỡng xác định và abstain CVE OOD.

**Tri thức CTI và IDS.** Strom et al. [2018], Wagner et al. [2019], Khraisat et al. [2019] khung miền. EDGR nhắm QA trên đồ thị CTI gắn ngữ cảnh cảnh báo IDS/NIDS, không phải phân loại gói tin.

**Định vị.** EDGR gần nhất với graph RAG kết hợp kiểm soát rủi ro: đồ thị cung cấp ứng viên; ranking hợp nhất vector và thực thể; ρ-gate quyết định có được phát Trusted Answer hay không.

---

## 3. Phát biểu bài toán

Cho truy vấn \(q\) và đồ thị \(G_t=(V_t,E_t)\) có timestamp cùng độ tin cậy. \(\mathcal{D}\) là kho evidence chunk liên kết thực thể trong \(G_t\).

Tìm câu trả lời \(a\) và tập bằng chứng \(E^*\subseteq\mathcal{D}\) sao cho: (1) mệnh đề trong \(a\) được \(E^*\) hỗ trợ; (2) \(\rho(E^*)<\theta\); (3) nếu không có \(E^*\) an toàn, hoặc CVE truy vấn vắng trong \(G_t\) và trong văn bản evidence thì **abstain**; (4) \(|E^*|\le k\) (mặc định \(k=5\)).

\[
E^*=\mathrm{TopK}_k\bigl(\{e\in\mathcal{C}(q):\rho(e)\le\theta\}\bigr),\qquad
a=\begin{cases}
\mathrm{Gen}(q,E^*) & \text{nếu }E^*\neq\emptyset\land\mathrm{Apply}=1,\\
\mathrm{Abstain} & \text{ngược lại.}
\end{cases}
\]

\(\mathcal{C}(q)\) là tập ứng viên sau trích thực thể, mở rộng đồ thị, lọc thời gian và xếp hạng.

---

## 4. Dynamic Knowledge Graph cho CTI

### 4.1 Schema

Nút thuộc \(\{\text{technique},\text{tactic},\text{cve},\text{malware},\text{actor},\text{software},\text{dataset},\text{alert},\text{concept}\}\), kèm `timestamp` và `reliability`. Cạnh mang quan hệ như `belongs_to`, `uses`, `exploits`, `related_to`, `enables`, `delivers_via`, `drops`, `detects`, `grounds_on`.

### 4.2 Nguồn và cập nhật gia tăng

Nguồn khai báo: MITRE ATT&CK, CVE/NVD, CWE/CAPEC, feed dạng CISA/CERT, evidence gắn IDS/NIDS. Cập nhật:

\[
G_{t+1}=G_t\oplus(\Delta V,\Delta E).
\]

Đồ thị seed thực nghiệm: **25 nút**, **22 cạnh**, **16** evidence chunk.

### 4.3 Giao diện cho EDGR

Trích thực thể; Expand theo ngân sách hop/nút; Temporal filter (giữ seed); path consistency \(\mathrm{Cons}(U)\) — tỉ lệ cặp thực thể có khoảng cách đường đi ngắn nhất (vô hướng) \(\le 2\).

**Ranh giới.** Lỗi IE và độ trễ feed lan vào Expand và scoring; DKG cần nhưng chưa đủ nếu thiếu ranking và ρ-gate.

---

## 5. Thuật toán EDGR

Sáu giai đoạn \(\Phi=\varphi_1\circ\cdots\circ\varphi_6\):

| Giai đoạn | Tên | Vai trò |
|----------:|-----|---------|
| \(\varphi_1\) | Query Understanding & Entity Extraction | Seed \(U_0\) từ \(q\) |
| \(\varphi_2\) | Adaptive Multi-step Expansion | Lân cận đồ thị theo ngân sách hop/nút |
| \(\varphi_3\) | Temporal Filtering | Loại láng giềng cũ; giữ seed |
| \(\varphi_4\) | Evidence Ranking | Hợp nhất vector + entity; xếp hạng |
| \(\varphi_5\) | Hallucination Scoring | \(R,F,G,S\rightarrow\tau,\rho\) |
| \(\varphi_6\) | Trusted Evidence Selection | ρ-gate, TopK, abstain; sinh có neo |

**Độ phức tạp (biên phân tích).** \(T(n)=O(E\log V)\); \(S(n)=O(V+E+D)\).

---

## 6. Chấm điểm ảo giác và cổng rủi ro

\[
\tau(e)=0.30\,R+0.20\,F+0.25\,G+0.25\,S,\qquad \rho(e)=1-\tau(e).
\]

\(R\): độ tin cậy nguồn; \(F\): độ mới theo bucket thời gian; \(G\): nhất quán đường đi đồ thị; \(S\): liên quan ngữ nghĩa. Trọng số là **siêu tham số**.

Mặc định \(\theta=0.55\), \(k=5\). Abstain khi: CVE lạ; không có evidence vượt cổng; CVE truy vấn không xuất hiện trong evidence tin cậy. Abstain được gắn faithfulness \(1.0\), hallucination rate \(0.0\), confidence \(0.0\).

Proxy faithfulness sau sinh kết hợp phủ token trên evidence, trust trung bình và phạt định danh CVE/technique bịa — đây là metric nghiên cứu tái lập được, không thay nhãn người.

---

## 7. Protocol và thiết lập thực nghiệm

**Dataset.** 8 cặp QA IDS/CTI (Log4Shell, APT29, lateral movement, Emotet→TrickBot, EDGR vs hallucination, Cl0p/MOVEit, CWE-89/CAPEC-66, CIC-IDS2017/UNSW-NB15).

**Baseline (cùng store; stub trung thực nghiên cứu).** RAG, GraphRAG, LightRAG, HippoRAG, Self-RAG, Corrective-RAG — **không** áp ρ-gate của EDGR.

**Metric.** Faithfulness, hallucination rate, token P/R/F1, P@k/R@k/MRR, latency. Siêu tham số: \(k=5\), \(\theta=0.55\), cửa sổ 730 ngày.

---

## 8. Kết quả và ablation

### 8.1 So sánh chính (trung bình \(N=8\))

| Phương pháp | Faithfulness ↑ | Hall. rate ↓ | P@k | MRR | Latency (ms) |
|-------------|----------------:|-------------:|----:|----:|-------------:|
| RAG | 0,573 | 0,427 | 0,250 | 1,000 | 1,5 |
| GraphRAG | 0,755 | 0,245 | 0,250 | 1,000 | 3,9 |
| LightRAG | 0,573 | 0,427 | 0,250 | 1,000 | 1,2 |
| HippoRAG | **0,831** | **0,169** | **0,900** | 1,000 | 1,8 |
| Self-RAG | 0,594 | 0,406 | 0,250 | 1,000 | 1,3 |
| Corrective-RAG | 0,489 | 0,511 | 0,125 | 0,250 | 1,0 |
| **EDGR** | **0,747** | **0,253** | 0,225 | 0,875 | 19,4 |

Tóm tắt EDGR trên cùng \(N=8\): accuracy proxy 0,875; token F1 0,436; R@k 0,875; latency ≈18–19 ms trên stack demo.

**Đọc bảng.** EDGR giảm mạnh hallucination rate so với RAG phẳng (−0,174) và stub CRAG (−0,258). Stub HippoRAG đạt faithfulness/P@k cao hơn trên seed nhỏ nhờ đoạn trùng gold dày; EDGR trả giá latency cho expand–score–gate và có thể abstain hoặc chọn tập evidence an toàn hơn nhưng ngắn hơn. MRR cao ở nhiều baseline phản ánh gold seed thường đứng hạng nhất dưới stub retrieval — không nên diễn giải quá mức như chất lượng xếp hạng corpus lớn.

### 8.2 Ablation (faithfulness trung bình)

| Biến thể | Faithfulness |
|----------|-------------:|
| full (EDGR) | 0,747 |
| w/o Temporal | 0,787 |
| w/o Graph | 0,721 |
| w/o Trust Score | 0,734 |
| w/o Evidence Ranking | 0,747 |
| w/o Hallucination Scoring | 0,747 |

Bỏ đồ thị làm giảm faithfulness (0,747→0,721). Tắt lọc thời gian hơi *tăng* proxy (0,787): chunk CVE cũ vẫn còn — đây là **đánh đổi freshness–coverage**. Trên seed này, ablation ranking/scoring ít dịch chuyển mean faithfulness khi cổng vẫn cho qua top-k tương tự; giá trị của chúng nằm ở **kiểm soát rủi ro và abstain OOD** (CVE lạ → `Apply=0`).

---

## 9. Thảo luận và giới hạn

**Mối đe dọa đối với tính hợp lệ.** (i) Quy mô demo. (ii) Baseline là stub trên cùng store. (iii) Faithfulness là proxy tự động. (iv) Generator ràng buộc evidence. (v) Trọng số \(\tau\) cố định tiên nghiệm.

**Không tuyên bố.** Không tuyên bố SOTA trên benchmark CTI công khai lớn, cũng không tuyên bố EDGR thắng mọi biến thể graph-RAG trên mọi metric. Chúng tôi tuyên bố một **pipeline thống nhất, kiểm toán được**, trong đó cấu trúc CTI động, truy hồi đa giai và ρ-gate với abstain được đồng thiết kế và đo được.

**Hướng mở.** Học \(\theta\) và trọng số; adapter TAXII/feed quy mô lớn; nhãn faithfulness người; chỉ mục ANN (Neo4j + vector); đánh giá cùng luồng cảnh báo Suricata → truy vấn.

---

## 10. Kết luận

Chúng tôi trình bày **EDGR**, gộp bốn trụ — Dynamic CTI KG, truy hồi đồ thị sáu giai đoạn dựa trên bằng chứng, chấm điểm rủi ro ảo giác bốn yếu tố với ρ-gate abstain, và protocol đánh giá toàn diện — thành một hệ thống khoa học cho hỏi đáp IDS/CTI. Thực nghiệm trên bộ seed tái lập được cho thấy EDGR cải thiện faithfulness và giảm hallucination rate so với RAG phẳng, đồng thời từ chối rõ ràng khi bằng chứng không hỗ trợ CVE được hỏi. Phương pháp theo đường đồ thị vẫn có thể thắng trên faithfulness tự động khi trùng gold dày; đóng góp khoa học chính của EDGR là **hợp đồng truy hồi kiểm soát rủi ro đầu–cuối** cho trợ lý CTI rủi ro cao.

---

## Tài liệu tham khảo

1. Lewis et al. (2020). Retrieval-Augmented Generation… *NeurIPS*.
2. Ji et al. (2023). Survey of Hallucination in NLG. *ACM CSUR*.
3. Gao et al. (2024). RAG for LLMs: A Survey.
4. Edge et al. (2024). Graph RAG.
5. Guo et al. (2024). LightRAG.
6. Gutiérrez et al. (2024). HippoRAG.
7. Asai et al. (2024). Self-RAG. *ICLR*.
8. Yan et al. (2024). CRAG.
9. Strom et al. (2018). MITRE ATT&CK.
10. Wagner et al. (2019). CTI Sharing Survey.
11. Khraisat et al. (2019). IDS Survey.
12. Peng et al. (2023). Knowledge Graphs Meet LLMs (và các hướng KG–LLM liên quan).

---

## Phụ lục A. Checklist tái lập

- Seed: `backend/app/data/cti_seed.py`
- Thuật toán: `backend/app/core/edgr.py`
- Scoring: `backend/app/core/hallucination.py`
- Graph: `backend/app/core/knowledge_graph.py`
- Metrics: `backend/app/evaluation/metrics.py`
- Mặc định: \(k=5\), \(\theta=0.55\), window \(=730\) ngày
