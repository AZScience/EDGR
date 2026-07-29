# EDGR: Truy hồi đồ thị động dựa trên bằng chứng với cổng rủi ro ảo giác cho IDS/CTI

**Loại bài:** Research Article  
**Bố cục:** Tóm tắt → Giới thiệu → Cấu trúc mô hình → Thí nghiệm → Phân tích kết quả → Phân tích mạnh mẽ → Kết luận → Phụ lục biên tập → Tài liệu tham khảo (khung MDPI)

---

**Tác giả:** Nguyễn Vĩnh Phúc ^{1,*}  

^{1} Nghiên cứu tiến sĩ — Evidence-Driven Dynamic Graph Retrieval (EDGR) cho Intrusion Detection & Cyber Threat Intelligence (IDS/CTI)  
\* Tác giả liên hệ: ngviphuc@gmail.com  

**Nhận / Sửa đổi / Chấp nhận / Xuất bản:** *(điền khi nộp)*  

---

## Tóm tắt

Trả lời câu hỏi tình báo đe dọa mạng (CTI) bằng mô hình ngôn ngữ lớn thường phát sinh mã CVE, kỹ thuật ATT&CK hoặc quan hệ actor–malware nghe có vẻ hợp lý nhưng không được bằng chứng truy hồi hỗ trợ. RAG cổ điển giảm kiến thức tham số lỗi thời nhưng xếp hạng đoạn văn phẳng và thường chỉ đo faithfulness sau khi đã sinh câu trả lời. RAG gắn đồ thị cải thiện quan hệ đa bước, song hầu hết hệ thống vẫn thiếu toán tử từ chối trước khi phát dành riêng cho rủi ro CTI.

Bài báo đề xuất mô hình **EDGR** (*Evidence-Driven Dynamic Graph Retrieval*). Đầu tiên, **Đồ thị tri thức động (DKG)** có nhãn thời gian và độ tin cậy nguồn cung cấp ngữ cảnh quan hệ qua mở rộng đa bước thích ứng và lọc thời gian. Sau đó, bằng chứng vector và bằng chứng gắn thực thể được hợp nhất–xếp hạng. Điểm tin cậy bốn nhân tố

\[
\tau(e)=0.30\,R+0.20\,F+0.25\,G+0.25\,S,\qquad \rho(e)=1-\tau(e)
\]

được tính cho từng bằng chứng; **cổng ρ** với ngưỡng \(\theta\) (mặc định \(\theta=0.55\)) chỉ cho phép bằng chứng rủi ro thấp đi vào sinh câu trả lời; nếu không đủ an toàn thì hệ thống **abstain**.

Trên bộ seed IDS/CTI tái lập được (\(N=54\) cặp QA, 40 đoạn bằng chứng, đồ thị \(V=40\), \(E=41\)), đánh giá full EDGR đạt faithfulness trung bình **0,702**, hallucination rate **0,298**, R@k **0,852**, MRR **0,803**. Trên \(n=52\) câu không OOD, faithfulness trung bình của EDGR là **0,698** [0,649; 0,745] so với RAG phẳng **0,558** [0,509; 0,607] (CI bootstrap 95%). Gỡ mở rộng đồ thị làm giảm faithfulness trung bình **0,104** (ablation H3). Chúng tôi **không** tuyên bố SOTA trên benchmark CTI lớn; đóng góp là giao thức **Trusted Answer** thống nhất, kiểm chứng được — DKG + sáu giai đoạn + cổng ρ/abstain + giả thuyết H1–H4, CI bootstrap, McNemar, ablation, threats-to-validity, và đánh giá chuyên gia SOC với Cohen’s \(\kappa\).

**Từ khóa:** truy hồi tăng cường sinh; đồ thị tri thức; giảm ảo giác; tình báo đe dọa mạng; phát hiện xâm nhập; cổng rủi ro; abstain; xếp hạng bằng chứng  

**MSC:** 68T50; 68P20; 68M25  

---

## 1. Giới thiệu

Trung tâm vận hành an ninh (SOC) ngày càng đặt câu hỏi ngôn ngữ tự nhiên dạng *“Những kỹ thuật ATT&CK nào liên quan tới CVE-2021-44228 (Log4Shell), và phát hiện nào áp dụng?”*. Một câu trả lời bịa kỹ thuật hoặc gắn sai actor–malware có thể làm lệch ứng cứu sự cố. LLM thuần tham số không đủ tin cậy trong miền này: tri thức CTI thay đổi khi CVE/campaign mới xuất hiện, và mã định danh bịa đặt đặc biệt nguy hiểm [1–3].

RAG [1] neo sinh câu trả lời vào đoạn văn ngoài. Các khảo sát về RAG và ảo giác LLM [2,3] cho thấy neo bằng chứng giảm—nhưng không loại trừ—các khẳng định không hỗ trợ. Trong CTI còn hai khoảng trống cấu trúc. Thứ nhất, tri thức đe dọa mang tính **quan hệ**; xếp hạng đoạn phẳng không mã hóa cạnh mà chuyên gia dùng [4–6]. Thứ hai, faithfulness thường chỉ là chỉ số hậu kiểm, chưa phải tín hiệu điều khiển có thể từ chối trả lời [7,8].

RAG gắn đồ thị (GraphRAG, LightRAG, HippoRAG) cải thiện truy hồi đa bước [4–6]; các pipeline phản tư (Self-RAG, CRAG) hiệu chỉnh truy hồi khi độ tin cậy thấp [7,8]. Các hướng này hiếm khi kết hợp đồng thời: (a) đồ thị CTI động có timestamp và độ tin cậy nguồn [9–11], (b) điểm rủi ro đa nhân tố minh bạch, và (c) cổng abstain cứng trước khi phát.

**Đóng góp.** Bài báo đề xuất **EDGR**, gom bốn trụ cột trong một hệ thống:

1. **Đồ thị tri thức CTI động** — schema, nạp đa nguồn, cập nhật tăng dần \(G_{t+1}=G_t\oplus(\Delta V,\Delta E)\).  
2. **Thuật toán sáu giai đoạn** \(\Phi=\varphi_1\circ\cdots\circ\varphi_6\).  
3. **Chấm điểm ảo giác và cổng ρ** — \(\tau\) từ \(R,F,G,S\); \(\rho=1-\tau\); abstain khi không an toàn.  
4. **Giao thức đánh giá toàn diện** — faithfulness, hallucination rate, P@k, R@k, MRR, latency, ablation, H1–H4, CI bootstrap, McNemar, threats-to-validity, human-eval SOC với Cohen’s \(\kappa\).

**Phần còn lại.** Phần 2 trình bày mô hình. Phần 3 mô tả dữ liệu và chỉ số. Phần 4 báo cáo kết quả. Phần 5 phân tích độ mạnh mẽ. Phần 6 kết luận.

---

## 2. Cấu trúc mô hình

### 2.1. Đồ thị tri thức động cho CTI

Nút thuộc các kiểu \(\{\text{technique},\text{tactic},\text{cve},\text{malware},\text{actor},\text{software},\text{dataset},\text{alert},\text{concept}\}\), kèm `timestamp` và `reliability`. Cạnh là quan hệ có kiểu như `belongs_to`, `uses`, `exploits`, `related_to`, `enables`, `delivers_via`, `drops`, `detects`, `grounds_on` [9–11].

Nguồn khai báo gồm MITRE ATT&CK, CVE/NVD, CWE/CAPEC, feed kiểu CISA/CERT và đoạn bằng chứng gắn IDS/NIDS. Cập nhật tăng dần:

\[
G_{t+1}=G_t\oplus(\Delta V,\Delta E).
\]

Đồ thị seed live: **40 nút**, **41 cạnh**, **40** đoạn bằng chứng.

Giao diện EDGR: trích thực thể; expand theo ngân sách hop; lọc thời gian (seed luôn giữ); nhất quán đường đi \(G=\mathrm{Cons}(U)\).

**Biên hệ thống.** Lỗi trích xuất và độ trễ feed lan vào Expand và scoring; DKG cần thiết nhưng chưa đủ nếu thiếu xếp hạng và cổng ρ.

### 2.2. Phát biểu bài toán

Cho truy vấn \(q\) và đồ thị thời gian \(G_t=(V_t,E_t)\), kho bằng chứng \(\mathcal{D}\). Tìm câu trả lời \(a\) và tập \(E^*\subseteq\mathcal{D}\) sao cho khẳng định được hỗ trợ, \(\rho(E^*)<\theta\), abstain khi không an toàn, và \(|E^*|\le k\) (mặc định \(k=5\)).

\[
E^*=\mathrm{TopK}_k\bigl(\{e\in\mathcal{C}(q):\rho(e)\le\theta\}\bigr),\qquad
a=\begin{cases}
\mathrm{Gen}(q,E^*) & \text{nếu }E^*\neq\emptyset\land\mathrm{Apply}=1,\\
\mathrm{Abstain} & \text{ngược lại.}
\end{cases}
\]

### 2.3. RAG cổ điển và RAG gắn đồ thị (baseline)

**RAG cổ điển** truy hồi đoạn theo tương đồng lexical/vector rồi sinh có điều kiện [1]. **RAG gắn đồ thị** mở rộng lân cận thực thể [4–6]; biến thể phản tư phê bình/hiệu chỉnh truy hồi [7,8]. Trong thí nghiệm, baseline là **stub trung thành nghiên cứu trên cùng kho** — chia sẻ bằng chứng/KG khi phù hợp nhưng **không áp dụng cổng ρ của EDGR**.

### 2.4. Chấm điểm rủi ro ảo giác

\[
\tau(e)=0.30\,R+0.20\,F+0.25\,G+0.25\,S,\qquad \rho(e)=1-\tau(e).
\]

| Nhân tố | Ý nghĩa |
|---------|---------|
| \(R\) | Độ tin cậy nguồn/đoạn |
| \(F\) | Độ mới theo timestamp (CVE lịch sử có sàn, không loại cứng) |
| \(G\) | Nhất quán đường đi trên đồ thị |
| \(S\) | Liên quan ngữ nghĩa từ truy hồi |

Trọng số là **siêu tham số**, không tuyên bố tối ưu toàn cục.

### 2.5. Cổng ρ và toán tử abstain

Mặc định \(\theta=0.55\), \(k=5\). Abstain khi: CVE không biết; không còn bằng chứng \(\rho\le\theta\); CVE truy vấn không xuất hiện trong bằng chứng tin cậy. Abstain được chấm \(F=1{,}0\), \(H=0{,}0\), confidence \(0{,}0\).

\[
\mathrm{Emit}(q)\iff E^*\neq\emptyset\land\rho(E^*)<\theta\land\mathrm{ID}(q)\subseteq\mathrm{Supp}.
\]

### 2.6. Thành phần pipeline EDGR

Sáu giai đoạn \(\Phi=\varphi_1\circ\cdots\circ\varphi_6\) (Hình 1): trích thực thể → mở rộng đa bước → lọc thời gian → xếp hạng bằng chứng → chấm \(\tau,\rho\) → chọn bằng chứng tin cậy / abstain.

**Hình 1.** Pipeline EDGR (\(\varphi_1\)–\(\varphi_6\)) với cổng ρ.  
*File:* `docs/papers/figures/fig1_edgr_pipeline.svg`

**Độ phức tạp (cận phân tích).** \(T(n)=O(E\log V)\); \(S(n)=O(V+E+D)\).

**Proxy faithfulness (chỉ số nghiên cứu, chưa phải nhãn người):**

\[
F=\mathrm{clip}\bigl(0.55\cdot\mathrm{coverage}+0.45\cdot\overline{\tau}-\mathrm{invent\_penalty}\bigr),\quad H=1-F.
\]

---

## 3. Thí nghiệm

### 3.1. Dữ liệu và corpus

**Bộ QA.** 54 cặp hỏi–đáp IDS/CTI (Log4Shell, APT TTP, NIDS lateral movement, chuỗi malware, KEV, đa bước/thời gian, quan hệ từ đồ thị, OOD abstain).

**Bằng chứng / đồ thị (đo live):** 40 đoạn; \(V=40\), \(E=41\).

### 3.2. Baseline

| Họ | Hành vi stub |
|----|--------------|
| RAG | Truy hồi vector phẳng → sinh |
| GraphRAG / LightRAG / HippoRAG | Truy hồi gắn đường/đồ thị (không cổng ρ) |
| Self-RAG / Corrective-RAG | Stub phản tư/hiệu chỉnh (không cổng ρ) |
| **EDGR** | Đầy đủ \(\varphi_1\)–\(\varphi_6\) + cổng ρ |

**Công bố.** Mọi baseline ≠ EDGR là family stub trên cùng kho bằng chứng.

### 3.3. Chỉ số đánh giá

Faithfulness \(F\) ↑; hallucination rate \(H=1-F\) ↓; P@k / R@k / MRR; latency; thành công OOD (abstain đúng). Siêu tham số: \(k=5\), \(\theta=0{,}55\), cửa sổ 730 ngày. Thống kê: CI bootstrap (\(n_{\mathrm{boot}}=1000\), \(\alpha=0{,}05\)); McNemar exact; ablation dataset cho H3.

### 3.4. Giả thuyết

| ID | Giả thuyết |
|----|------------|
| **H1** | Faithfulness trung bình(EDGR) > RAG trên cùng kho |
| **H2** | Với CVE OOD, EDGR abstain |
| **H3** | Gỡ Graph hoặc cổng ρ làm giảm faithfulness trung bình |
| **H4** | Cùng seed + cấu hình ⇒ cùng bảng chỉ số |

---

## 4. Phân tích kết quả

### 4.1. So sánh trung bình theo phương pháp (\(n=52\))

Bảng 1 và Hình 2 báo cáo trung bình trên các câu không OOD.

**Bảng 1.** Trung bình dataset (chạy live; stub đã công bố).

| Phương pháp | TB \(F\) ↑ | CI 95% (\(F\)) | TB \(H\) ↓ | Stub? |
|-------------|-----------:|----------------|-----------:|:-----:|
| RAG | 0,558 | [0,509; 0,607] | 0,443 | có |
| GraphRAG | 0,545 | [0,502; 0,586] | 0,455 | có |
| LightRAG | 0,842† | [0,794; 0,887] | 0,158 | có |
| HippoRAG | 0,742 | [0,700; 0,783] | 0,258 | có |
| Self-RAG | 0,471 | [0,426; 0,514] | 0,529 | có |
| Corrective-RAG | 0,471 | [0,425; 0,518] | 0,529 | có |
| **EDGR** | **0,698** | **[0,649; 0,745]** | **0,302** | không |

† Stub LightRAG có thể đạt proxy \(F\) cao khi chồng lấp gold dày; **không** tương đương hợp đồng Trusted Answer (không cổng ρ/abstain).

**Hình 2.** Faithfulness trung bình theo phương pháp (\(n=52\)).  
*File:* `docs/papers/figures/fig2_mean_faithfulness.svg`

**Cặp EDGR vs RAG (\(N=54\)).** TB \(F\): EDGR **0,709** [0,658; 0,756] vs RAG **0,559** [0,510; 0,606]; Δ**+0,150** [0,107; 0,197]. McNemar trên proxy đúng/sai nhị phân: \(p=0{,}375\) (**không** có ý nghĩa ở \(\alpha=0{,}05\)). H1 được hỗ trợ trên biên **faithfulness liên tục** (CI Δ không chứa 0); proxy nhị phân còn yếu lực tại \(N\) này.

### 4.2. Tóm tắt full-dataset EDGR

| Chỉ số | Giá trị |
|--------|--------:|
| Faithfulness ↑ | **0,702** |
| Hallucination rate ↓ | **0,298** |
| P@k | 0,363 |
| R@k | **0,852** |
| MRR | **0,803** |
| Token F1 | 0,268 |
| Latency TB (ms) | 192,9 |

**Theo nhóm (chọn lọc):** core 0,759; multi-hop 0,672; KEV 0,686; IDS-alert 0,771; temporal 0,735; OOD-abstain **1,000**; gate-theory 0,894; graph-derived 0,621.

### 4.3. Hành vi cổng định tính

Với CVE vắng trong \(G_t\) và bằng chứng, EDGR abstain thay vì bịa tường thuật CTI (H2).

### 4.4. Quan sát độ phức tạp

Thời gian giai đoạn thực nghiệm ủng hộ cận \(T(n)=O(E\log V)\); latency tăng theo ngân sách \(k\).

---

## 5. Phân tích mạnh mẽ

### 5.1. Nghiên cứu cắt bỏ (Ablation)

**Bảng 2.** Ablation vs EDGR đầy đủ (\(n=52\)).

| Biến thể | TB \(F\) | CI 95% | Δ so full |
|----------|---------:|--------|----------:|
| full (EDGR) | 0,698 | [0,649; 0,745] | 0,000 |
| w/o Temporal | 0,697 | [0,653; 0,740] | −0,000 |
| **w/o Graph** | **0,594** | **[0,551; 0,638]** | **−0,104** |
| w/o Trust Score | 0,677 | [0,621; 0,730] | −0,021 |
| w/o Evidence Ranking | 0,699 | [0,651; 0,746] | +0,001 |
| w/o Hallucination Scoring | 0,698 | [0,649; 0,745] | 0,000 |

**Hình 3.** Δ faithfulness trung bình khi gỡ từng thành phần.  
*File:* `docs/papers/figures/fig3_ablation.svg`

Gỡ mở rộng đồ thị gây sụt lớn nhất (−0,104), ủng hộ H3. Lọc thời gian gần như trung tính trên seed này (đánh đổi freshness–coverage). Ranking/scoring có thể ít đổi TB \(F\) khi cổng vẫn nhận top-\(k\) tương tự; giá trị nằm ở **kiểm soát rủi ro và abstain OOD**.

### 5.2. Mối đe dọa đối với tính hợp lệ

| Mối đe dọa | Phát biểu |
|------------|-----------|
| Nội tại | Seed \(N\) có kiểm soát — rủi ro overfitting giao thức |
| Ngoại tại | Chưa phải benchmark CTI lớn / telemetry SOC thật |
| Cấu trúc đo | Proxy \(F/H\) ≠ phán đoán chuyên gia; stub có thể “ăn” \(F\) |
| Kết luận | McNemar ở \(N\) vừa có thể yếu lực — báo CI; tránh SOTA |
| Triển khai | Stub chia sẻ kho (công bằng dữ liệu, không công bằng mã vendor) |

### 5.3. Đánh giá người (Cohen’s \(\kappa\))

Trên seed SOC panel:

| Chiều | Cohen’s \(\kappa\) |
|-------|-------------------:|
| Groundedness | 0,386 |
| Unsupported IDs | 0,760 |
| Actionability | 0,591 |
| Abstain OK | 1,000 |

Groundedness mới ở mức fair–moderate; **nhãn SOC thực địa nên thay seed panel khi sửa bản nộp tạp chí**.

### 5.4. Định vị so với nghiên cứu trước

EDGR gần nhất với **graph RAG + kiểm soát rủi ro**. Tuyên bố đặc trưng: hợp đồng **Trusted Answer** (cổng ρ + abstain) đồng thiết kế với đồ thị CTI động.

---

## 6. Kết luận và hướng phát triển

Chúng tôi trình bày **EDGR** — gom DKG CTI động, truy hồi sáu giai đoạn, chấm rủi ro bốn nhân tố với cổng ρ/abstain, và giao thức đánh giá toàn diện — thành một hệ thống khoa học cho QA IDS/CTI. Trên seed live (\(N=54\), \(|D|=40\), \(V=40\), \(E=41\)), EDGR đạt faithfulness **0,702**, hallucination rate **0,298**, R@k **0,852**, MRR **0,803**. So với RAG phẳng, biên faithfulness dương với CI bootstrap không chứa 0 (Δ≈+0,15); ablation đồ thị xác nhận đóng góp **−0,104**. Stub theo đường đồ thị vẫn có thể thắng proxy \(F\) khi chồng lấp gold dày; đóng góp khoa học chính là **hợp đồng truy hồi kiểm soát rủi ro đầu–cuối** cho trợ lý CTI rủi ro cao.

**Hướng tiếp.** Học \(\theta\) và trọng số; adapter TAXII/feed quy mô; nhãn SOC thực địa; chỉ mục ANN cho latency sản xuất; đánh giá chung với luồng alert Suricata; benchmark CTI QA công khai lớn hơn.

---

## Đóng góp của tác giả

Khái niệm hóa, phương pháp, phần mềm, kiểm chứng, phân tích hình thức, điều tra, dữ liệu, viết bản thảo và hiệu đính: N.V.P. Giám sát: *(cố vấn — điền tên)*. Tác giả đã đọc và đồng ý với phiên bản xuất bản.

## Tài trợ

Nghiên cứu này không nhận tài trợ bên ngoài *(cập nhật nếu có)*.

## Tuyên bố sẵn có dữ liệu

Prototype tái lập được, seed QA/bằng chứng/KG và script đánh giá nằm trong kho dự án đi kèm.

## Xung đột lợi ích

Tác giả tuyên bố không có xung đột lợi ích.

---

## Tài liệu tham khảo

1. Lewis, P.; Perez, E.; Piktus, A.; Petroni, F.; Karpukhin, V.; Goyal, N.; Küttler, H.; Lewis, M.; Yih, W.; Rocktäschel, T.; Riedel, S.; Kiela, D. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Adv. Neural Inf. Process. Syst.* **2020**, *33*, 9459–9474.  
2. Ji, Z.; Lee, N.; Frieske, R.; Yu, T.; Su, D.; Xu, Y.; Ishii, E.; Bang, Y.J.; Madotto, A.; Fung, P. Survey of Hallucination in Natural Language Generation. *ACM Comput. Surv.* **2023**, *55*, 248. https://doi.org/10.1145/3571730  
3. Gao, Y.; Xiong, Y.; Gao, X.; Jia, K.; Pan, J.; Bi, Y.; Dai, Y.; Sun, J.; Wang, M.; Wang, H. Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv* **2023**, arXiv:2312.10997.  
4. Edge, D.; Trinh, H.; Cheng, N.; Bradley, J.; Chao, A.; Mody, A.; Truitt, S.; Larson, J. From Local to Global: A Graph RAG Approach to Query-Focused Summarization. *arXiv* **2024**, arXiv:2404.16130.  
5. Guo, Z.; Xia, L.; Yu, Y.; Ao, X.; Huang, C. LightRAG: Simple and Fast Retrieval-Augmented Generation. *arXiv* **2024**, arXiv:2410.05779.  
6. Gutiérrez, B.J.; Shu, Y.; Gu, Y.; Yasunaga, M.; Su, Y. HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. *Adv. Neural Inf. Process. Syst.* **2024**.  
7. Asai, A.; Wu, Z.; Wang, Y.; Sil, A.; Hajishirzi, H. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In *Proceedings of the International Conference on Learning Representations (ICLR)*, 2024.  
8. Yan, S.-Q.; Gu, J.-C.; Zhu, Y.; Ling, Z.-H. Corrective Retrieval Augmented Generation. *arXiv* **2024**, arXiv:2401.15884.  
9. Strom, B.E.; Applebaum, A.; Miller, D.P.; Nickels, K.C.; Pennington, A.G.; Thomas, C.B. *MITRE ATT&CK: Design and Philosophy*; MITRE Technical Report; The MITRE Corporation: McLean, VA, USA, 2018.  
10. Wagner, T.D.; Mahbub, K.; Palomar, E.; Abdallah, A.E. Cyber Threat Intelligence Sharing: Survey and Research Directions. *Comput. Secur.* **2019**, *87*, 101589.  
11. Khraisat, A.; Gondal, I.; Vamplew, P.; Kamruzzaman, J. Survey of Intrusion Detection Systems: Techniques, Datasets and Challenges. *Cybersecurity* **2019**, *2*, 20. https://doi.org/10.1186/s42400-019-0038-7  
12. Pan, S.; Luo, L.; Wang, Y.; Chen, C.; Wang, J.; Wu, X. Unifying Large Language Models and Knowledge Graphs: A Roadmap. *IEEE Trans. Knowl. Data Eng.* **2024**, *36*, 3580–3599.  

---

## Phụ lục A. Checklist tái lập

| Hạng mục | Ghi chú |
|----------|---------|
| Seed QA / bằng chứng / KG | Module dữ liệu trong kho dự án |
| Thuật toán / scoring / đồ thị | Module core EDGR |
| Metrics / so sánh / ablation | Module evaluation + scientific rigor |
| Human eval / κ | Giao thức SOC hai người chú thích |
| Mặc định | \(k=5\), \(\theta=0{,}55\), cửa sổ 730 ngày |
| Hình | `docs/papers/figures/fig1_edgr_pipeline.svg`, `fig2_mean_faithfulness.svg`, `fig3_ablation.svg` |

## Phụ lục B. Đạo đức và dual-use

Trợ lý CTI có thể bị lạm dụng tấn công. Công trình nhắm quy trình SOC phòng thủ, từ chối khẳng định định danh không hỗ trợ qua abstain, và chỉ dùng kỹ thuật/CVE mô tả công khai trong corpus seed.
