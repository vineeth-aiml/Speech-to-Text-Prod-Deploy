import React, { useEffect, useRef, useState } from "react";
import MeetingList from "./components/MeetingList.jsx";
import MoMView from "./components/MoMView.jsx";

const API = "http://localhost:8000";

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

export default function App() {
  const [status, setStatus] = useState("idle");
  const [roomId, setRoomId] = useState("default");
  const [language, setLanguage] = useState("auto");
  const [transcript, setTranscript] = useState("");
  const [meta, setMeta] = useState(null);
  const [meetingId, setMeetingId] = useState(String(Date.now()));
  const [meetings, setMeetings] = useState([]);
  const [selected, setSelected] = useState(null);
  const [mom, setMom] = useState(null);

  const wsRef = useRef(null);
  const audioCtxRef = useRef(null);
  const processorRef = useRef(null);
  const streamRef = useRef(null);

  const refreshMeetings = async () => {
    const res = await fetch(`${API}/api/meetings`);
    setMeetings(await res.json());
  };

  useEffect(() => { refreshMeetings(); }, []);

  const start = async () => {
    setStatus("starting");
    setTranscript("");
    setMom(null);
    setMeta(null);
    const id = String(Date.now());
    setMeetingId(id);

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef.current = stream;

    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioCtx = new AudioContext({ sampleRate: 16000 });
    audioCtxRef.current = audioCtx;

    const source = audioCtx.createMediaStreamSource(stream);
    const processor = audioCtx.createScriptProcessor(4096, 1, 1);
    processorRef.current = processor;

    const ws = new WebSocket(
      `ws://localhost:8000/ws/stt?room_id=${encodeURIComponent(roomId)}&lang=${encodeURIComponent(language)}`
    );
    wsRef.current = ws;

    ws.onopen = () => setStatus("live");
    ws.onmessage = (evt) => {
      const msg = JSON.parse(evt.data);
      if (msg.type === "partial") {
        setTranscript(msg.text);
        setMeta(msg.meta || null);
      }
    };
    ws.onerror = () => setStatus("error");
    ws.onclose = () => setStatus("stopped");

    processor.onaudioprocess = (e) => {
      if (!wsRef.current || wsRef.current.readyState !== 1) return;
      const input = e.inputBuffer.getChannelData(0);
      const buf = new ArrayBuffer(input.length * 2);
      const view = new DataView(buf);
      for (let i = 0; i < input.length; i++) {
        let s = Math.max(-1, Math.min(1, input[i]));
        view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
      }
      wsRef.current.send(buf);
    };

    source.connect(processor);
    processor.connect(audioCtx.destination);
  };

  const stop = async () => {
    setStatus("stopping");
    try {
      if (wsRef.current) wsRef.current.close();
      if (processorRef.current) processorRef.current.disconnect();
      if (audioCtxRef.current) await audioCtxRef.current.close();
      if (streamRef.current) streamRef.current.getTracks().forEach((t) => t.stop());
    } catch {}
    setStatus("stopped");
  };

  const saveMeeting = async () => {
    const payload = {
      id: meetingId,
      room_id: roomId,
      language: meta?.language || language,
      transcript
    };
    await fetch(`${API}/api/meetings/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    await refreshMeetings();
  };

  const generateMoM = async () => {
    const lang = meta?.language || language || "auto";
    const res = await fetch(`${API}/api/mom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ meeting_id: meetingId, transcript, language: lang })
    });
    const data = await res.json();
    setMom(data.mom);
    await refreshMeetings();
  };

  const openMeeting = async (id) => {
    const res = await fetch(`${API}/api/meetings/${id}`);
    const data = await res.json();
    setSelected(data);
    setTranscript(data.transcript || "");
    setMom(data.mom || null);
    setMeetingId(data.id);
    setRoomId(data.room_id || "default");
    setLanguage(data.language || "auto");
  };

  const exportTxt = async () => {
    const res = await fetch(`${API}/api/meetings/${meetingId}/export.txt`);
    downloadText(`${meetingId}.txt`, await res.text());
  };

  const exportMd = async () => {
    const res = await fetch(`${API}/api/meetings/${meetingId}/export.md`);
    downloadText(`${meetingId}.md`, await res.text());
  };

  const copy = async () => { try { await navigator.clipboard.writeText(transcript); } catch {} };

  return (
    <div className="container">
      <div className="header">
        <div className="brand">
          <h1>Offline Speech-to-Text + MoM</h1>
          <p>CPU-only • V1/V2/V3 • Rooms • Exports • Docker</p>
        </div>
        <div className="badges">
          <div className="badge">MoM: V2 default</div>
          <div className="badge">Rooms: V3</div>
          <div className="badge">Exports: txt/md</div>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <div className="cardHead">
            <div>
              <div className="h3">Live Meeting</div>
              <div className="muted">Start mic streaming → realtime transcript</div>
            </div>
            <div className="muted small">Status: <b style={{color:"#e8ecff"}}>{status}</b></div>
          </div>
          <div className="cardBody">
            <div className="row">
              <div className="kv"><span>Room</span><input value={roomId} onChange={(e)=>setRoomId(e.target.value)} /></div>
              <div className="kv">
                <span>Language</span>
                <select value={language} onChange={(e)=>setLanguage(e.target.value)}>
                  <option value="auto">auto</option>
                  <option value="en">en</option>
                  <option value="hi">hi</option>
                  <option value="te">te</option>
                  <option value="ta">ta</option>
                  <option value="kn">kn</option>
                  <option value="ml">ml</option>
                  <option value="mr">mr</option>
                  <option value="bn">bn</option>
                </select>
              </div>
              <div className="kv"><span>Detected</span><b>{meta?.language || "—"}</b></div>
            </div>

            <div className="row" style={{marginTop:12}}>
              <button className="btn primary" onClick={start} disabled={status === "live"}>Start</button>
              <button className="btn danger" onClick={stop} disabled={status !== "live"}>Stop</button>
              <button className="btn" onClick={saveMeeting} disabled={!transcript}>Save</button>
              <button className="btn success" onClick={generateMoM} disabled={!transcript}>Generate MoM</button>
              <button className="btn" onClick={exportTxt} disabled={!transcript}>Export .txt</button>
              <button className="btn" onClick={exportMd} disabled={!transcript}>Export .md</button>
              <button className="btn" onClick={copy} disabled={!transcript}>Copy</button>
            </div>

            <div style={{marginTop:12}} className="muted small">
              Meeting ID: <b style={{color:"#e8ecff"}}>{meetingId}</b>
            </div>

            <div style={{marginTop:12}}>
              <textarea value={transcript} onChange={(e)=>setTranscript(e.target.value)} placeholder="Transcript will appear here..." />
            </div>

            <div className="footerHint">
              <b>V3:</b> Open UI in 2 tabs, set same <b>Room</b>, Start in one tab → broadcast to all tabs.
            </div>
          </div>
        </div>

        <MeetingList meetings={meetings} onSelect={openMeeting} />
      </div>

      <div className="split">
        <MoMView mom={mom} />
        <div className="card">
          <div className="cardHead">
            <div>
              <div className="h3">Meeting JSON</div>
              <div className="muted">Stored in data/meetings</div>
            </div>
          </div>
          <div className="cardBody">
            {selected ? <pre>{JSON.stringify(selected, null, 2)}</pre> : <div className="muted">Open a meeting from the list.</div>}
          </div>
        </div>
      </div>
    </div>
  );
}
