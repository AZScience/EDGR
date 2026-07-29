/** Empty = same-origin `/api` (Vite proxy → backend). Override with VITE_API_URL if needed. */
const API_BASE = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, "") ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  let res: Response;
  try {
    res = await fetch(url, {
      headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
      ...init,
    });
  } catch {
    throw new Error(
      `Không kết nối được API (${url || path}). Hãy chạy backend :8015 và frontend :5180.`,
    );
  }
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json() as Promise<T>;
}

export type PipelineTask = {
  id: string;
  title: string;
  title_en: string;
  action: string;
  has_academic?: boolean;
  assessment_score?: number;
};

export type PipelineStep = {
  id: number;
  key: string;
  title: string;
  title_en: string;
  icon: string;
  color?: string;
  goal: string;
  goal_en?: string;
  badge?: string;
  badge_en?: string;
  has_academic?: boolean;
  assessment_score?: number;
  tasks: PipelineTask[];
};

export type PipelineDefinition = {
  topic: string;
  topic_vi: string;
  steps: PipelineStep[];
  step_count: number;
  academic_blocks?: string[];
};

export type AcademicBlocks = {
  csdl: Record<string, unknown> | unknown;
  mo_hinh_toan: Record<string, unknown> | unknown;
  mo_hinh_thuat_toan: Record<string, unknown> | unknown;
  mo_hinh_hoat_dong: Record<string, unknown> | unknown;
  trich_dan: unknown;
  minh_chung: Record<string, unknown> | unknown;
  nhan_dinh_danh_gia: {
    strength?: string;
    limitation?: string;
    verdict?: string;
    score_0_1?: number;
    [k: string]: unknown;
  };
};

export type AcademicPurpose = {
  vi?: string;
  en?: string;
  does_vi?: string;
  does_en?: string;
  task_vi?: string;
  task_en?: string;
};

export type TheoryPack = {
  name_vi?: string;
  name_en?: string;
  /** Step-overview lead-in (shown first). */
  intro_vi?: string;
  intro_en?: string;
  /** Major child tabs map (step overview). */
  child_tabs?: Array<{
    id?: string;
    index?: number;
    title_vi?: string;
    title_en?: string;
    blurb_vi?: string;
    blurb_en?: string;
  }>;
  what_vi?: string;
  what_en?: string;
  why_vi?: string;
  why_en?: string;
  ideas_vi?: string[];
  ideas_en?: string[];
  argument_vi?: string;
  argument_en?: string;
  assumptions_vi?: string[];
  assumptions_en?: string[];
  related_work?: Array<{
    cite?: string;
    role_vi?: string;
    role_en?: string;
  }>;
  frame_vi?: string;
  frame_en?: string;
  scope_vi?: string;
  scope_en?: string;
  refs?: string;
};

export type AcademicPackage = {
  scope: "step" | "task";
  step_id: number;
  task_id: string | null;
  title: string;
  title_en?: string;
  purpose?: AcademicPurpose;
  theory?: TheoryPack;
  goal?: string;
  goal_en?: string;
  scientific_sequence_vi?: Array<
    | string
    | {
        id?: string;
        title_vi?: string;
        title_en?: string;
        explain_vi?: string;
        explain_en?: string;
        anchor?: string;
      }
  >;
  scientific_sequence_en?: Array<
    | string
    | {
        id?: string;
        title_vi?: string;
        title_en?: string;
        explain_vi?: string;
        explain_en?: string;
        anchor?: string;
      }
  >;
  /** Live KG figure for graph-related tabs (shown before Run). */
  graph_preview?: {
    kind?: string;
    title_vi?: string;
    title_en?: string;
    nodes?: Array<{ id: string; label?: string; type?: string; seed?: boolean }>;
    edges?: Array<{
      source: string;
      target: string;
      relation?: string;
      weight?: number;
    }>;
  };
  blocks: AcademicBlocks;
  block_keys: string[];
};

export type TableGuide = {
  field?: string;
  title_vi?: string;
  title_en?: string;
  explain_vi?: string;
  explain_en?: string;
  evaluate_vi?: string;
  evaluate_en?: string;
  verdict_vi?: string;
  verdict_en?: string;
};

export type ResultReviewEvidence = {
  claim_vi?: string;
  claim_en?: string;
  scalars?: Record<string, string | number | boolean>;
  collections?: Array<{
    field: string;
    count: number;
    sample?: unknown;
  }>;
  has_evidence?: boolean;
  tables?: Record<string, TableGuide>;
};

export type ScientificCheck = {
  id: string;
  ok: boolean;
  title_vi?: string;
  title_en?: string;
  detail_vi?: string;
  detail_en?: string;
};

export type ScientificVerification = {
  kind?: string;
  runtime_status?: string;
  runtime_status_vi?: string;
  runtime_status_en?: string;
  passed?: number;
  total?: number;
  runtime_passed?: number;
  runtime_total?: number;
  checks?: ScientificCheck[];
  protocol_vi?: string;
  protocol_en?: string;
  expert?: {
    status?: string;
    status_vi?: string;
    status_en?: string;
    kappa?: number | null;
    n_dual?: number;
    meets_minimum?: boolean;
    next_step_vi?: string;
    next_step_en?: string;
    jump?: { step_id?: number; task_id?: string };
  };
};

export type ResultReview = {
  purpose_vi?: string;
  purpose_en?: string;
  does_vi?: string;
  does_en?: string;
  explain_vi?: string;
  explain_en?: string;
  bullets_vi?: string[];
  bullets_en?: string[];
  how_to_read_vi?: string;
  how_to_read_en?: string;
  evidence?: ResultReviewEvidence;
  tables?: Record<string, TableGuide>;
  scientific_verification?: ScientificVerification;
  assessment?: {
    strength?: string;
    strength_en?: string;
    limitation?: string;
    limitation_en?: string;
    verdict?: string;
    verdict_en?: string;
    score_0_1?: number;
    verification_status?: string;
    expert_status?: string;
  };
};

export type TaskResult = {
  step_id: number;
  step_title: string;
  step_title_en?: string;
  task_id: string;
  task_title: string;
  task_title_en?: string;
  action: string;
  elapsed_ms: number;
  real_computation: boolean;
  computation_kind?: string;
  result: Record<string, unknown>;
  result_review?: ResultReview;
  academic?: AcademicPackage;
};

export type TaskRunBody = {
  query?: string;
  top_k?: number;
  enable_temporal?: boolean;
  enable_graph?: boolean;
  enable_trust_score?: boolean;
  node_id?: string;
  label?: string;
};

export type AppStatus = {
  app_name_vi?: string;
  app_name_en?: string;
  mode?: string;
  simulated?: boolean;
  scripted_answers?: boolean;
  kg_nodes?: number;
  kg_edges?: number;
  evidence_chunks?: number;
  alert_queue_size?: number;
  engine?: string;
  generator?: string;
  realtime_ingest?: string;
  note_vi?: string;
  note_en?: string;
};

export type AppAlert = {
  id: string;
  received_at?: string;
  signature?: string;
  severity?: number;
  category?: string;
  src_ip?: string;
  dest_ip?: string;
  proto?: string;
  query?: string;
  analyzed?: boolean;
  event_type?: string;
  timestamp?: string;
};

export type AppAnalyzeResult = {
  kind?: string;
  mode?: string;
  simulated?: boolean;
  scripted_answers?: boolean;
  query?: string;
  answer?: string;
  confidence?: number;
  faithfulness?: number;
  hallucination_rate?: number;
  latency_ms?: number;
  entities?: unknown[];
  evidence?: Array<Record<string, unknown>>;
  stage_summary?: Array<{
    stage?: number;
    name?: string;
    name_vi?: string;
    duration_ms?: number;
  }>;
  abstained?: boolean;
  apply?: number;
  abstain_reason_vi?: string;
  abstain_reason_en?: string;
  metadata?: Record<string, unknown>;
  live_enrichment?: {
    attempted?: boolean;
    injected?: string[];
    errors?: string[];
    source?: string;
  };
  provenance_vi?: string;
  provenance_en?: string;
  runtime?: Record<string, unknown>;
  [k: string]: unknown;
};

export const api = {
  health: () =>
    request<{
      status: string;
      kg_nodes: number;
      kg_edges: number;
      evidence_chunks: number;
      pipeline_steps: number;
    }>("/api/health"),
  pipeline: () => request<PipelineDefinition>("/api/pipeline"),
  stepAcademic: (stepId: number) =>
    request<AcademicPackage>(`/api/pipeline/${stepId}/academic`),
  taskAcademic: (stepId: number, taskId: string) =>
    request<AcademicPackage>(`/api/pipeline/${stepId}/${taskId}/academic`),
  runTask: (stepId: number, taskId: string, body: TaskRunBody = {}) =>
    request<TaskResult>(`/api/pipeline/${stepId}/${taskId}/run`, {
      method: "POST",
      body: JSON.stringify(body),
    }),
  appStatus: () => request<AppStatus>("/api/app/status"),
  appAnalyze: (body: TaskRunBody & { live_enrich?: boolean } = {}) =>
    request<AppAnalyzeResult>("/api/app/analyze", {
      method: "POST",
      body: JSON.stringify({
        query: body.query,
        top_k: body.top_k,
        enable_temporal: body.enable_temporal,
        enable_graph: body.enable_graph,
        enable_trust_score: body.enable_trust_score,
        extra: { live_enrich: body.live_enrich ?? true },
      }),
    }),
  appAlertSample: () =>
    request<{ alert: Record<string, unknown>; curl_example?: string }>(
      "/api/app/alerts/sample",
    ),
  appListAlerts: (limit = 50) =>
    request<{ count: number; queue_size: number; alerts: AppAlert[] }>(
      `/api/app/alerts?limit=${limit}`,
    ),
  appIngestAlerts: (payload: unknown) =>
    request<{
      ok: boolean;
      accepted: number;
      queue_size: number;
      alerts: AppAlert[];
      note_vi?: string;
      note_en?: string;
    }>("/api/app/alerts", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  appAnalyzeAlert: (alertId: string, topK = 5) =>
    request<AppAnalyzeResult>("/api/app/alerts/analyze", {
      method: "POST",
      body: JSON.stringify({
        alert_id: alertId,
        top_k: topK,
        live_enrich: true,
      }),
    }),
};
