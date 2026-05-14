import { useState, useEffect } from "react";

const API = import.meta.env.VITE_API_URL;

export default function Admin() {
  const [adminKey, setAdminKey] = useState(() => localStorage.getItem("questin_admin") || "");
  const [authed, setAuthed] = useState(false);
  const [requests, setRequests] = useState([]);
  const [venueReqs, setVenueReqs] = useState([]);
  const [tab, setTab] = useState("access");
  const [loading, setLoading] = useState(false);

  const headers = { "Authorization": `Bearer ${adminKey}` };

  const login = () => {
    localStorage.setItem("questin_admin", adminKey);
    setAuthed(true);
  };

  const fetchAll = async () => {
    setLoading(true);
    try {
      const [a, v] = await Promise.all([
        fetch(`${API}/access-requests/`, { headers }).then(r => r.json()),
        fetch(`${API}/venue-requests/`, { headers }).then(r => r.json()),
      ]);
      setRequests(Array.isArray(a) ? a : []);
      setVenueReqs(Array.isArray(v) ? v : []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (authed) fetchAll(); }, [authed]);

  const updateStatus = async (id, status) => {
    await fetch(`${API}/access-requests/${id}/status?status=${status}`, {
      method: "PATCH", headers
    });
    fetchAll();
  };

  if (!authed) return (
    <div style={{
      fontFamily: "Inter, system-ui, sans-serif",
      background: "#0A0A0A",
      color: "#F5F5F0",
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }}>
      <div style={{ width: 320, display: "flex", flexDirection: "column", gap: 12 }}>
        <h2 style={{ fontSize: 20, fontWeight: 800, color: "#CDFF00", marginBottom: 8 }}>Questin Admin</h2>
        <input
          placeholder="Admin API key"
          type="password"
          value={adminKey}
          onChange={e => setAdminKey(e.target.value)}
          onKeyDown={e => e.key === "Enter" && login()}
          style={{
            padding: "12px 14px",
            background: "#131313",
            border: "0.5px solid #252525",
            borderRadius: 8,
            color: "#F5F5F0",
            fontSize: 14,
            fontFamily: "inherit",
            outline: "none"
          }}
        />
        <button onClick={login} style={{
          padding: 12,
          background: "#CDFF00",
          color: "#0A0A0A",
          border: "none",
          borderRadius: 8,
          fontWeight: 700,
          fontSize: 14,
          cursor: "pointer",
          fontFamily: "inherit"
        }}>
          Enter
        </button>
      </div>
    </div>
  );

  const statusColor = (s) =>
    s === "approved" ? "#7EB800" : s === "rejected" ? "#FF4444" : "#888";

  const statusBg = (s) =>
    s === "approved" ? "rgba(205,255,0,0.1)" : s === "rejected" ? "rgba(255,68,68,0.1)" : "rgba(255,200,40,0.1)";

  const list = tab === "access" ? requests : venueReqs;

  return (
    <div style={{
      fontFamily: "Inter, system-ui, sans-serif",
      background: "#0A0A0A",
      color: "#F5F5F0",
      minHeight: "100vh",
      padding: "24px 20px",
      maxWidth: 760,
      margin: "0 auto"
    }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 28 }}>
        <h1 style={{ fontSize: 18, fontWeight: 900, color: "#CDFF00", letterSpacing: "-0.3px" }}>QUES↗IN Admin</h1>
        <button onClick={fetchAll} style={{
          background: "none",
          border: "0.5px solid #2a2a2a",
          color: "#888",
          padding: "6px 12px",
          borderRadius: 7,
          fontSize: 12,
          cursor: "pointer",
          fontFamily: "inherit",
          display: "flex",
          alignItems: "center",
          gap: 5
        }}>
          ↻ Refresh
        </button>
      </div>

      {/* Tabs */}
      <div style={{
        display: "flex",
        gap: 2,
        marginBottom: 20,
        background: "#131313",
        borderRadius: 8,
        padding: 3,
        width: "fit-content"
      }}>
        {["access", "venues"].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: "7px 16px",
            borderRadius: 6,
            fontSize: 13,
            fontWeight: 600,
            cursor: "pointer",
            fontFamily: "inherit",
            border: "none",
            background: tab === t ? "#CDFF00" : "none",
            color: tab === t ? "#0A0A0A" : "#888",
            transition: "all 0.15s"
          }}>
            {t === "access"
              ? `Access Requests (${requests.length})`
              : `Venue Requests (${venueReqs.length})`}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading && <p style={{ color: "#888", fontSize: 13 }}>Loading...</p>}

      {!loading && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {list.length === 0 && (
            <p style={{ color: "#555", fontSize: 13, padding: "20px 0" }}>No requests yet.</p>
          )}

          {tab === "access" && requests.map(r => (
            <div key={r.id} style={{
              padding: "16px 18px",
              background: "#131313",
              borderRadius: 10,
              border: "0.5px solid #1e1e1e"
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                <div>
                  <p style={{ fontWeight: 700, fontSize: 15, marginBottom: 3 }}>{r.name}</p>
                  <p style={{ fontSize: 12, color: "#666" }}>{r.email} · {r.user_type}</p>
                </div>
                <span style={{
                  fontSize: 10,
                  fontWeight: 700,
                  letterSpacing: "0.07em",
                  textTransform: "uppercase",
                  padding: "3px 8px",
                  borderRadius: 99,
                  background: statusBg(r.status),
                  color: statusColor(r.status),
                  whiteSpace: "nowrap"
                }}>
                  {r.status}
                </span>
              </div>

              {r.about && (
                <p style={{ fontSize: 13, color: "#777", margin: "10px 0", lineHeight: 1.55 }}>{r.about}</p>
              )}

              <p style={{ fontSize: 11, color: "#333", marginBottom: r.status === "pending" ? 12 : 0 }}>
                {new Date(r.created_at).toLocaleString()}
              </p>

              {r.status === "pending" && (
                <div style={{ display: "flex", gap: 8 }}>
                  <button onClick={() => updateStatus(r.id, "approved")} style={{
                    flex: 1,
                    padding: "9px",
                    background: "#CDFF00",
                    color: "#0A0A0A",
                    border: "none",
                    borderRadius: 7,
                    fontWeight: 700,
                    fontSize: 13,
                    cursor: "pointer",
                    fontFamily: "inherit"
                  }}>
                    Approve
                  </button>
                  <button onClick={() => updateStatus(r.id, "rejected")} style={{
                    flex: 1,
                    padding: "9px",
                    background: "none",
                    color: "#FF4444",
                    border: "0.5px solid rgba(255,68,68,0.35)",
                    borderRadius: 7,
                    fontWeight: 700,
                    fontSize: 13,
                    cursor: "pointer",
                    fontFamily: "inherit"
                  }}>
                    Reject
                  </button>
                </div>
              )}
            </div>
          ))}

          {tab === "venues" && venueReqs.map(r => (
            <div key={r.id} style={{
              padding: "16px 18px",
              background: "#131313",
              borderRadius: 10,
              border: "0.5px solid #1e1e1e"
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                <div>
                  <p style={{ fontWeight: 700, fontSize: 15, marginBottom: 3 }}>{r.poc_name}</p>
                  <p style={{ fontSize: 12, color: "#666" }}>{r.phone} · Community #{r.community_id}</p>
                </div>
                <span style={{
                  fontSize: 10,
                  fontWeight: 700,
                  letterSpacing: "0.07em",
                  textTransform: "uppercase",
                  padding: "3px 8px",
                  borderRadius: 99,
                  background: statusBg(r.status),
                  color: statusColor(r.status),
                  whiteSpace: "nowrap"
                }}>
                  {r.status}
                </span>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px 16px", margin: "10px 0 12px" }}>
                {[
                  { l: "Dates", v: r.preferred_dates },
                  { l: "Capacity", v: r.capacity },
                  { l: "Revenue", v: r.revenue_model },
                  { l: "Notes", v: r.notes || "—" }
                ].map(d => (
                  <div key={d.l}>
                    <p style={{ fontSize: 10, color: "#444", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 2 }}>{d.l}</p>
                    <p style={{ fontSize: 13 }}>{d.v}</p>
                  </div>
                ))}
              </div>

              <p style={{ fontSize: 11, color: "#333" }}>{new Date(r.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}