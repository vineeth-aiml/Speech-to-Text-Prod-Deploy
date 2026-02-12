import React from "react";

export default function MeetingList({ meetings, onSelect }) {
  return (
    <div className="card">
      <div className="cardHead">
        <div>
          <div className="h3">Meetings</div>
          <div className="muted">Saved transcripts + MoM</div>
        </div>
        <div className="muted small">{meetings.length} items</div>
      </div>
      <div className="cardBody">
        {meetings.length === 0 ? (
          <div className="muted">No meetings yet. Click Start to begin.</div>
        ) : (
          <ol className="list">
            {meetings.map((m) => (
              <li key={m.id}>
                <button className="btn" onClick={() => onSelect(m.id)}>
                  Open {m.id} {m.language ? `(${m.language})` : ""}
                </button>
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  );
}
