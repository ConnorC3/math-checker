"use client"

import type { Operation } from "@/app/types/api";

interface StepInputProps {
    index: number;
    expression: string;
    operation: Operation;
    wrt: string;
    onExpressionChange: (value: string) => void;
    onOperationChange: (value: Operation) => void;
    onWrtChange: (value: string) => void;
    onRemove: () => void;
    isFirst: boolean;
    error: boolean;
}

const OPERATIONS: { value: Operation; label: string }[] = [
    { value: "simplify", label: "Simplify / Algebra" },
    { value: "differentiate", label: "Differentiate" },
    { value: "integrate", label: "Integrate" },
];

export function StepInput({ 
    index,
    expression,
    operation,
    wrt,
    onExpressionChange,
    onOperationChange,
    onWrtChange,
    onRemove,
    isFirst,
    error
}: StepInputProps){
    const showWrt = operation === "differentiate" || operation === "integrate";

    return (
        <div
            className={`flex items-center gap-3 p-3 rounded-lg border transition-colors ${
                error 
                    ? "border-red-400 bg-red-50"
                    : "border-green-200 bg-white hover:border-gray-300"
            }`}
        >

            <span className="text-sm font-mono text-gray-400 w-6 shrink-0 text-right">
                {index + 1}.
            </span>

            <input 
                className="flex-1 text-gray-800 border border-gray-200 rounded px-3 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
                placeholder={
                    operation === "simplify"
                        ? "e.g. 2*x + 4 = 10  or  6*x"
                        : operation === "differentiate"
                        ? "e.g. 2*x + 3"
                        : "e.g. 3*x**2 + C"
                }
                value={expression}
                onChange={(e) => onExpressionChange(e.target.value)}
            />

            {!isFirst && (
                <select 
                    className="border border-gray-200 rounded px-2 py-2 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
                    value={operation}
                    onChange={(e) => onOperationChange(e.target.value as Operation)}
                >
                    {OPERATIONS.map((op) => (
                        <option key={op.value} value={op.value}>
                            {op.label}
                        </option>
                    ))}
                </select>
            )}

            {!isFirst && showWrt && (
                <div className="flex items-center gap-1">
                    <span className="text-sm text-gray-400">w.r.t.</span>
                    <input 
                        className="w-12 text-gray-800 border border-gray-200 rounded px-2 py-2 font-mono text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-300"
                        placeholder="x"
                        value={wrt}
                        onChange={(e) => onWrtChange(e.target.value)}
                    />
                </div>
            )}

            <button
                className="text-gray-300 hover:text-red-400 transition-colors text-lg leading-none"
                onClick={onRemove}
                aria-label="Remove step"
            >
                ×
            </button>
        </div>
    );
}
