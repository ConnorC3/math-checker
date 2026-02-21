"use client"

import { useState } from "react";
import { StepInput } from "./components/StepInput";
import { checkSteps } from "./lib/api";
import type { CheckResponse, Operation, ApiError } from "./types/api";

interface StepState {
  expression: string;
  operation: Operation;
  wrt: string;
}

function makeStep(): StepState {
  return { expression: "", operation: "simplify", wrt: "x" };
}

export default function Home() {
  const [steps, setSteps] = useState<StepState[]>([makeStep()]);
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [apiError, setApiError] = useState<ApiError | null>(null);
  const [loading, setLoading] = useState(false);

  const updateStep = (index: number, patch: Partial<StepState>) => {
    setSteps((prev) => 
      prev.map((s, i) => (i === index ? {...s, ...patch} : s))
    );
  };

  const addStep = () => setSteps((prev) => [...prev, makeStep()]);

  const removeStep = (index: number) => {
    if (steps.length === 1) return;
    setSteps((prev) => prev.filter((_, i) => i !== index));
    setResult(null);
    setApiError(null);
  };

  const submit = async () => {
    setResult(null);
    setApiError(null);
    setLoading(true);

    try {
      const payload = steps.map((s) => ({
        expression: s.expression,
        operation: s.operation,
        wrt: s.wrt || null,
      }));

      const res = await checkSteps(payload);
      setResult(res);
    } catch (e) {
      setApiError(e as ApiError);
    } finally {
      setLoading(false);
    }
  };

  // Subtract 1 bc index is 0-based
  const errorIndex =
    result && !result.valid && result.error_step != null
      ? result.error_step - 1
      : apiError?.detail?.step != null
      ? apiError.detail.step - 1
      : null;


  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Math Step Checker
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            Enter each step of your solution. For calculus steps, 
            select the operation and the variable.
          </p>
        </div>

        <div className="flex gap-4 mb-4 text-xs text-gray-400">
          <span>
            <span className="font-semibold text-gray-600">Simpilfy</span> - algebraic equivalence
          </span>
          <span>
            <span className="font-semibold text-gray-600">Differentiate</span> - validates d/dx
          </span>
          <span>
            <span className="font-semibold text-gray-600">Integrate</span> - validates ∫ dx
          </span>
        </div>

        <div className="flex flex-col gap-2 mb-4">
          {steps.map((step, i) => (
            <StepInput 
              key={i}
              index={i}
              expression={step.expression}
              operation={step.operation}
              wrt={step.wrt}
              onExpressionChange={(v) => updateStep(i, { expression: v })}
              onOperationChange={(v) => updateStep(i, { operation: v })}
              onWrtChange={(v) => updateStep(i, { wrt: v })}
              onRemove={() => removeStep(i)}
              isFirst={i === 0}
              error={errorIndex === i}
            />
          ))}
        </div>

        <div className="flex gap-2 mb-6">
          <button
            className="border rounded px-4 py-2 text-sm bg-white hover:bg-gray-50 border-gray-200 text-gray-700 transition-colors"
            onClick={addStep}
          >
            + Add Step
          </button>
          <button
            className="ml-auto border rounded px-4 py-2 text-sm bg-blue-500 hover:bg-blue-600 text-white font-medium transition-colors disabled:opacity-50"
            onClick={submit}
            disabled={loading}
          >
            {loading ? "Checking..." : "Check Steps"}
          </button>
        </div>

        {result && (
          <div
            className={`rounded-lg px-4 py-3 text-sm font-medium ${
              result.valid
                ? "bg-green-50 border border-green-200 text-green-700"
                : "bg-red-50 border border-red-200 text-red-700"  
            }`}
          >
            {result.message}
          </div>
        )}

        {apiError && (
          <div className="rounded-lg px-4 py-3 text-sm bg-red-50 border border-red-200 text-red-700">
            <span className="font-semibold">
              Step {apiError.detail.step} could not be parsed:
            </span>{" "}
            {apiError.detail.error}
          </div>
        )}
      </div>
    </main>
  );
}
