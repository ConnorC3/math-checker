"use client";

import { useEffect, useState } from "react";

interface HistoryStep {
    position: number;
    expression: string;
    operation: string;
    is_error: boolean;
}

interface HistorySession {
    id: number;
    created_at: string;
    valid: boolean;
    error_step: number | null;
    steps: HistoryStep[];
}

export default function HistoryPage() {
    const [sessions, setSessions] = useState<HistorySession[]>([]);

    useEffect(() => {
        async function fetchHistory() {
            const res = await fetch("http://127.0.0.1:8000/history");
            const data = await res.json();
            setSessions(data);
        }

        fetchHistory();
    }, []);

    return (
        <>
            <h1 className="text-2xl text-gray-900 font-bold mb-6">Past Sessions</h1>
            <div className="flex flex-col gap-4">
                {sessions.map((s) => (
                    <div key={s.id} className={`border rounded-lg p-4 ${s.valid ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}`}>
                        <div className="flex justify-between text-sm text-gray-500 mb-2">
                            <span>{new Date(s.created_at).toLocaleString()}</span>
                            <span className={s.valid ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
                                {s.valid ? "Correct" : `Error at step ${s.error_step}`}
                            </span>
                        </div>
                        <ol className="flex flex-col gap-1">
                            {s.steps.map((step) => (
                                <li key={step.position} className={`font-mono text-sm px-2 py-1 rounded ${step.is_error ? "bg-red-100 text-red-700" : "text-gray-700"}`}>
                                    {step.position + 1}. {step.expression}
                                    <span className="text-xs text-gray-400 ml-2">[{step.operation}]</span>
                                </li>
                            ))}
                        </ol>
                    </div>
                ))}
            </div>
        </>
    );
}
