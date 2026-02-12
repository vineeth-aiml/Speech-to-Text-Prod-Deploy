import React from "react";

function renderList(v) {
  if (!v) return null;
  if (!Array.isArray(v)) return <div>{String(v)}</div>;
  return (
    <ul className="list">
      {v.map((it, i) => (
        <li key={i}>
          {typeof it === "string"
            ? it
            : `${it.task || ""}${it.owner ? ` (Owner: ${it.owner})` : ""}${it.due_date ? ` (Due: ${it.due_date})` : ""}`}
        </li>
      ))}
    </ul>
  );
}

export default function MoMView({ mom }) {
  return (
    <div className="card">
      <div className="cardHead">
        <div>
          <div className="h3">MoM</div>
          <div className="muted">V2 (Ollama) or V1 fallback</div>
        </div>
        <div className="muted small">
          {mom ? `Engine: ${mom.engine || "—"} | Lang: ${mom.language || "—"}` : "No MoM yet"}
        </div>
      </div>
      <div className="cardBody">
        {!mom ? (
          <div className="muted">Generate MoM to see summary, decisions, action items.</div>
        ) : (
          <>
            <div className="h3" style={{ marginTop: 0 }}>Summary</div>
            {renderList(mom.summary)}
            <div className="h3" style={{ marginTop: 14 }}>Decisions</div>
            {renderList(mom.decisions)}
            <div className="h3" style={{ marginTop: 14 }}>Action Items</div>
            {renderList(mom.action_items)}
            <div className="h3" style={{ marginTop: 14 }}>Risks</div>
            {renderList(mom.risks)}
            <div className="h3" style={{ marginTop: 14 }}>Next Steps</div>
            {renderList(mom.next_steps)}
            {mom.raw ? (
              <>
                <div className="h3" style={{ marginTop: 14 }}>Raw</div>
                <pre>{mom.raw}</pre>
              </>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}
