export interface AssessmentDriver {
  label: string;
  weight?: number;
}

export interface Evidence {
  source: string;
  clause_id: string;
}

export interface AssessmentResult {
  risk: number;
  drivers: AssessmentDriver[];
  evidence: Evidence[];
}

export interface PlanAction {
  [key: string]: any;
}

export interface PlanOption {
  type: string;
  actions: PlanAction[];
  rationale: string;
}

export interface PlanResult {
  plans: PlanOption[];
}

export interface ActResult {
  artifactType: string;
  payload: any;
}
