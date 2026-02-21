import { StepInput, CheckResponse, ApiError } from '@/app/types/api';

export async function checkSteps(steps: StepInput[]): Promise<CheckResponse> {
    const res = await fetch("http://127.0.0.1:8000/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(steps),
    })

    if (!res.ok) {
        const err: ApiError = await res.json();
        throw err;
    }

    return res.json();
}
