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

  const C = { bg:"#0A0A0A", surface:"#131313", border:"#252525", lime:"#CDFF00", blue:"#3B5EFF", white:"#F5F5F0", grey:"#8A8A8A", red:"#FF4444" };

  if (!authed) return (
    <div style={{fontFamily:"Inter,system-ui,sans-serif",background:C.bg,color:C.white,minHeight:"100vh",display:"flex",alignItems:"center",justifyContent:"center"}}>
      <div style={{width:320,display:"flex",flexDirection:"column",gap:12}}>
        <h2 style={{fontSize:20,fontWeight:800,color:C.lime,marginBottom:8}}>Questin Admin</h2>
        <input placeholder="Admin API key" type="password" value={adminKey} onChange={e=>setAdminKey(e.target.value)}
          onKeyDown={e=>e.key==="Enter"&&login()}
          style={{padding:"12px 14px",background:C.surface,border:`1.5px solid ${C.border}`,borderRadius:8,color:C.white,fontSize:14,fontFamily:"inherit",outline:"none"}} />
        <button onClick={login} style={{padding:"12px",background:C.lime,color:"#0A0A0A",border:"none",borderRadius:8,fontWeight:700,fontSize:14,cursor:"pointer",fontFamily:"inherit"}}>Enter</button>
      </div>
    </div>
  );

  const statusColor = (s) => s==="approved" ? C.lime : s==="rejected" ? C.red : C.grey;

  return (
    <div style={{fontFamily:"Inter,system-ui,sans-serif",background:C.bg,color:C.white,minHeight:"100vh",padding:"24px 20px",maxWidth:800,margin:"0 auto"}}>
      <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:24}}>
        <h1 style={{fontSize:20,fontWeight:900,color:C.lime}}>QUES↗IN Admin</h1>
        <button onClick={fetchAll} style={{background:"none",border:`1px solid ${C.border}`,color:C.grey,padding:"6px 14px",borderRadius:6,fontSize:12,cursor:"pointer",fontFamily:"inherit"}}>↻ Refresh</button>
      </div>

      <div style={{display:"flex",gap:8,marginBottom:20}}>
        {["access","venues"].map(t=>(
          <button key={t} onClick={()=>setTab(t)}
            style={{padding:"8px 16px",borderRadius:6,fontSize:13,fontWeight:600,cursor:"pointer",fontFamily:"inherit",border:"none",background:tab===t?C.lime:C.surface,color:tab===t?"#0A0A0A":C.grey}}>
            {t==="access"?`Access Requests (${requests.length})`:`Venue Requests (${venueReqs.length})`}
          </button>
        ))}
      </div>

      {loading && <p style={{color:C.grey,fontSize:13}}>Loading...</p>}

      {!loading && tab==="access" && (
        <div style={{display:"flex",flexDirection:"column",gap:10}}>
          {requests.length===0 && <p style={{color:C.grey,fontSize:13}}>No access requests yet.</p>}
          {requests.map(r=>(
            <div key={r.id} style={{padding:16,background:C.surface,borderRadius:10,border:`1px solid ${C.border}`}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:8}}>
                <div>
                  <p style={{fontWeight:700,fontSize:15,marginBottom:2}}>{r.name}</p>
                  <p style={{fontSize:12,color:C.grey}}>{r.email} · {r.user_type}</p>
                </div>
                <span style={{fontSize:11,fontWeight:700,color:statusColor(r.status),textTransform:"uppercase",letterSpacing:"0.06em"}}>{r.status}</span>
              </div>
              <p style={{fontSize:13,color:C.grey,marginBottom:12,lineHeight:1.5}}>{r.about}</p>
              <p style={{fontSize:11,color:"#3A3A3A",marginBottom:10}}>{new Date(r.created_at).toLocaleString()}</p>
              {r.status==="pending" && (
                <div style={{display:"flex",gap:8}}>
                  <button onClick={()=>updateStatus(r.id,"approved")}
                    style={{flex:1,padding:"8px",background:C.lime,color:"#0A0A0A",border:"none",borderRadius:6,fontWeight:700,fontSize:13,cursor:"pointer",fontFamily:"inherit"}}>
                    Approve
                  </button>
                  <button onClick={()=>updateStatus(r.id,"rejected")}
                    style={{flex:1,padding:"8px",background:"none",color:C.red,border:`1px solid ${C.red}`,borderRadius:6,fontWeight:700,fontSize:13,cursor:"pointer",fontFamily:"inherit"}}>
                    Reject
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {!loading && tab==="venues" && (
        <div style={{display:"flex",flexDirection:"column",gap:10}}>
          {venueReqs.length===0 && <p style={{color:C.grey,fontSize:13}}>No venue requests yet.</p>}
          {venueReqs.map(r=>(
            <div key={r.id} style={{padding:16,background:C.surface,borderRadius:10,border:`1px solid ${C.border}`}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:8}}>
                <div>
                  <p style={{fontWeight:700,fontSize:15,marginBottom:2}}>{r.poc_name}</p>
                  <p style={{fontSize:12,color:C.grey}}>{r.phone} · Community #{r.community_id}</p>
                </div>
                <span style={{fontSize:11,fontWeight:700,color:statusColor(r.status),textTransform:"uppercase",letterSpacing:"0.06em"}}>{r.status}</span>
              </div>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:6,marginBottom:8}}>
                {[{l:"Dates",v:r.preferred_dates},{l:"Capacity",v:r.capacity},{l:"Revenue",v:r.revenue_model},{l:"Notes",v:r.notes||"—"}].map(d=>(
                  <div key={d.l}><p style={{fontSize:10,color:"#3A3A3A",textTransform:"uppercase",letterSpacing:"0.04em",marginBottom:1}}>{d.l}</p><p style={{fontSize:13}}>{d.v}</p></div>
                ))}
              </div>
              <p style={{fontSize:11,color:"#3A3A3A"}}>{new Date(r.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}