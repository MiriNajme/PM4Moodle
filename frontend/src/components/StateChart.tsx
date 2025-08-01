import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import type { Transition } from "../utils/ocelToStateChart";

interface StateChartProps {
  chartData: {
    states: string[];
    transitions: Transition[];
  };
}

export const StateChart: React.FC<StateChartProps> = ({ chartData }) => {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    ref.current.innerHTML = "";
    const stateSet = new Set(chartData.states);

    const cy = cytoscape({
      container: ref.current,
      elements: [
        // Nodes
        ...chartData.states.map((state) => ({
          data: { id: state, label: state },
          classes: state === "Start" || state === "End" ? "endpoint" : "state",
        })),
        // Edges
        ...chartData.transitions
          .filter((t) => stateSet.has(t.from) && stateSet.has(t.to))
          .map((t, i) => ({
            data: { id: `e${i}`, source: t.from, target: t.to },
            classes: t.count > 1 ? "thick-edge" : "",
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
            "background-color": "#e5e7eb",
            "text-outline-color": "#e5e7eb",
            "text-outline-width": 2,
            "border-width": 2,
            "border-color": "#9ca3af",
            width: 90,
            height: 45,
            "font-size": "15px",
            color: "#111827",
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
        {
          selector: "edge.thick-edge",
          style: {
            width: 6,
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
    });

    return () => {
      cy.destroy();
    };
  }, [chartData]);

  return <div ref={ref} className='w-full h-full'></div>;
};
