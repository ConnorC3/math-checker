export type Operation = "simplify" | "differentiate" | "integrate";

export interface StepInput {
    expression: string;
    operation: Operation;
    wrt?: string | null;
}

export interface CheckResponse {
    valid: boolean;
    error_step?: number | null;
    message: string
}

export interface ApiError {
    detail: {
        step: number;
        error: string;
    };
}
