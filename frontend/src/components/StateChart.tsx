import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

interface StateChartProps {
  chartData: {
    states: string[];
    transitions: { from: string; to: string }[];
  };
}

export const StateChart: React.FC<StateChartProps> = ({ chartData }) => {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    ref.current.innerHTML = "";

    const cy = cytoscape({
      container: ref.current,
      elements: [
        // Nodes
        ...chartData.states.map((state) => ({
          data: { id: state, label: state },
          classes: state === "Start" || state === "End" ? "endpoint" : "state",
        })),
        // Edges
        ...chartData.transitions.map((t, i) => ({
          data: { id: `e${i}`, source: t.from, target: t.to },
        })),
      ],
      style: [
        {
          selector: "node.endpoint",
          style: {
            shape: "ellipse",
            "background-color": "#2563eb",
            "text-outline-color": "#2563eb",
            "text-outline-width": 2,
            "border-width": 3,
            "border-color": "#1e293b",
            width: 45,
            height: 45,
            "font-size": "15px",
            color: "#fff",
            label: "data(label)",
            "text-valign": "center",
            "text-halign": "center",
          },
        },
        {
          selector: "node.state",
          style: {
            shape: "roundrectangle",
            "background-color": "#e5e7eb", // Tailwind gray-200
            "text-outline-color": "#e5e7eb",
            "text-outline-width": 2,
            "border-width": 2,
            "border-color": "#9ca3af", // Tailwind gray-400
            width: 90,
            height: 45,
            "font-size": "15px",
            color: "#111827", // Tailwind gray-900
            label: "data(label)",
            "text-valign": "center",
            "text-halign": "center",
          },
        },
        {
          selector: "edge",
          style: {
            width: 3,
            "line-color": "#93c5fd",
            "target-arrow-color": "#2563eb",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
          },
        },
      ],
      layout: {
        name: "grid",
        rows: 1,
      },
    });

    return () => {
      cy.destroy();
    };
  }, [chartData]);

  return (
    <div
      ref={ref}
      className='w-full h-full rounded-xl bg-blue-50 shadow-inner'
    />
  );
};
