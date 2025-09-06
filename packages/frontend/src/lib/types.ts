export interface Claim {
  [key: string]: any;
}

export interface AssessmentResult {
  risk: number;
  drivers: { issue: string; contribution: number }[];
  evidence: { source: string; clauseId: string; snippet: string }[];
}

export interface PlanAction {
  addModifier?: string;
  replaceDx?: string;
}

export interface PlanOption {
  type: string;
  rationale: string;
  actions: PlanAction[];
  citation?: string;
}

export interface PlanResult {
  plans: PlanOption[];
}

export interface ActResult {
  artifactType: 'corrected_claim' | 'appeal_letter';
  correctedClaim?: Claim;
  appealLetter?: string;
}

export interface BriefItem {
  score: number;
  claim: Claim;
  why: string;
  eta: string;
  delta: number;
  deadline: string;
}

export interface BriefResult {
  highlights: string[];
  queue: BriefItem[];
}
