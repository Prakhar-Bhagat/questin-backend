import { useState, useEffect } from "react";

const API = "http://localhost:8000";
const categories = ["All","Creative","Sports","Social","Learning","Cultural","Wellness"];

export default function Questin() {
  const [view, setView] = useState("home");
  const [userType, setUserType] = useState(null);
  const [gateForm, setGateForm] = useState({name:"",email:"",about:""});
  const [gateSubmitted, setGateSubmitted] = useState(false);
  const [accessGranted, setAccessGranted] = useState(false);
  const [catFilter, setCatFilter] = useState("All");
  const [requestingId, setRequestingId] = useState(null);
  const [requestForm, setRequestForm] = useState({poc:"",phone:"",dates:"",capacity:"",revenue:"",notes:""});
  const [requestSent, setRequestSent] = useState(null);
  const [waitlistEmail, setWaitlistEmail] = useState("");
  const [waitlistDone, setWaitlistDone] = useState(false);
  const [communities, setCommunities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("questin_token") || null);
  const [pitchForm, setPitchForm] = useState({community_name:"",organizer_name:"",email:"",description:"",category:""});
  const [pitchDone, setPitchDone] = useState(false);

  // Read token from approval email link on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const urlToken = params.get("token");
    if (urlToken) {
      localStorage.setItem("questin_token", urlToken);
      setToken(urlToken);
      window.history.replaceState({}, "", window.location.pathname);
    }
  }, []);

  // Fetch communities whenever token is set
  useEffect(() => {
    if (!token) {
      setView("home");
      setAccessGranted(false);
      return;
    }
    const fetchCommunities = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API}/communities/`, {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setCommunities(data.map(c => ({
            id: c.id,
            name: c.name,
            tagline: c.tagline,
            category: c.category,
            groupSize: c.group_size,
            price: c.price_range,
            duration: c.duration,
            venueNeeds: c.venue_needs,
            frequency: c.frequency,
            image: c.image_url,
          })));
          setAccessGranted(true);
          setView("catalogue");
        } else if (res.status === 401) {
          localStorage.removeItem("questin_token");
          setToken(null);
          setAccessGranted(false);
          setView("home");
          setCommunities([]);
        }
      } catch (e) {
        setError("Couldn't load catalogue. Try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchCommunities();
  }, [token]);

  const filtered = communities.filter(c => catFilter==="All" || c.category===catFilter);

  const goHome = () => {
    setView("home");
    setAccessGranted(false);
    setGateSubmitted(false);
    setGateForm({name:"",email:"",about:""});
    setError(null);
  };

  const handleLogout = () => {
    localStorage.removeItem("questin_token");
    setToken(null);
    setCommunities([]);
    goHome();
  };

  const handleWaitlist = async () => {
    if (!waitlistEmail) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/waitlist/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: waitlistEmail })
      });
      if (res.ok || res.status === 409) {
        setWaitlistDone(true);
      }
    } catch (e) {
      setError("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGateSubmit = async () => {
    if (!gateForm.name || !gateForm.email || !gateForm.about) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/access-requests/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: gateForm.name,
          email: gateForm.email,
          about: gateForm.about,
          user_type: userType
        })
      });
      if (res.ok) {
        setGateSubmitted(true);
      } else {
        const data = await res.json();
        setError(data.detail || "Submission failed. Try again.");
      }
    } catch (e) {
      setError("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleRequest = async (id) => {
    if (!requestForm.poc || !requestForm.phone || !requestForm.dates || !requestForm.capacity || !requestForm.revenue) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/venue-requests/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          community_id: id,
          poc: requestForm.poc,
          phone: requestForm.phone,
          dates: requestForm.dates,
          capacity: requestForm.capacity,
          revenue: requestForm.revenue,
          notes: requestForm.notes || null
        })
      });
      if (res.ok) {
        setRequestSent(id);
        setRequestingId(null);
        setRequestForm({poc:"",phone:"",dates:"",capacity:"",revenue:"",notes:""});
        setTimeout(() => setRequestSent(null), 4000);
      } else if (res.status === 401) {
        localStorage.removeItem("questin_token");
        setToken(null);
        setCommunities([]);
        setView("home");
      }
    } catch (e) {
      setError("Couldn't send request. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const handlePitchSubmit = async () => {
    if (!pitchForm.community_name || !pitchForm.organizer_name || !pitchForm.email || !pitchForm.description || !pitchForm.category) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/pitches/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(pitchForm)
      });
      if (res.ok) {
        setPitchDone(true);
      } else {
        setError("Couldn't submit pitch. Try again.");
      }
    } catch (e) {
      setError("Couldn't submit pitch. Try again.");
    } finally {
      setLoading(false);
    }
  };

  const C = {
    bg:"#0A0A0A", surface:"#131313", card:"#181818", border:"#252525",
    lime:"#CDFF00", limeDim:"rgba(205,255,0,0.1)",
    blue:"#3B5EFF", blueDim:"rgba(59,94,255,0.1)",
    cream:"#F0EDE6", creamDim:"rgba(240,237,230,0.06)",
    white:"#F5F5F0", grey:"#8A8A8A", greyMid:"#5A5A5A", greyDark:"#3A3A3A",
  };

  const catColor = (cat) => {
    if(cat==="Creative") return {bg:C.lime,color:"#0A0A0A"};
    if(cat==="Sports") return {bg:C.blue,color:"#fff"};
    return {bg:C.cream,color:"#0A0A0A"};
  };

  return (
    <div style={{fontFamily:"'Inter',system-ui,sans-serif",background:C.bg,color:C.white,minHeight:"100vh",overflowX:"hidden"}}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        *{box-sizing:border-box;margin:0;padding:0}
        ::selection{background:#CDFF00;color:#0A0A0A}
        .fu{animation:fu .5s ease forwards}.f1{animation:fu .5s ease .1s forwards;opacity:0}.f2{animation:fu .5s ease .2s forwards;opacity:0}.f3{animation:fu .5s ease .3s forwards;opacity:0}
        @keyframes fu{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
        .bl{background:#CDFF00;color:#0A0A0A;border:none;padding:14px 24px;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;transition:all .15s;width:100%}
        .bl:hover{filter:brightness(.92);transform:translateY(-1px)}
        .bl:disabled{opacity:0.5;cursor:not-allowed;transform:none}
        .bb{background:#3B5EFF;color:#fff;border:none;padding:14px 24px;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;transition:all .15s;width:100%}
        .bb:hover{filter:brightness(.85);transform:translateY(-1px)}
        .bb:disabled{opacity:0.5;cursor:not-allowed;transform:none}
        .bg{background:transparent;color:#F0EDE6;border:1.5px solid #252525;padding:14px 24px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .15s;width:100%}
        .bg:hover{border-color:#CDFF00;color:#CDFF00}
        .inp{width:100%;padding:12px 14px;background:#131313;border:1.5px solid #252525;border-radius:8px;color:#F5F5F0;font-size:14px;font-family:inherit;outline:none;transition:border-color .15s}
        .inp:focus{border-color:#3B5EFF}.inp::placeholder{color:#3A3A3A}
        .sel{appearance:none;padding:9px 32px 9px 12px;background:#131313;border:1.5px solid #252525;border-radius:8px;color:#F5F5F0;font-size:13px;font-weight:600;font-family:inherit;cursor:pointer;outline:none}
        .sel:focus{border-color:#3B5EFF}
        .crd{background:#181818;border:1px solid #252525;border-radius:10px;overflow:hidden;transition:border-color .2s,transform .2s}
        .crd:hover{border-color:#3A3A3A;transform:translateY(-2px)}
        .mo{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.88);z-index:200;display:flex;align-items:flex-end;justify-content:center}
        .ms{background:#131313;border-radius:16px 16px 0 0;width:100%;max-width:480px;max-height:85vh;overflow-y:auto;padding:24px 20px 36px;animation:su .3s ease}
        @keyframes su{from{transform:translateY(100%)}to{transform:translateY(0)}}
        .bk{display:inline-flex;align-items:center;gap:6px;color:#8A8A8A;font-size:13px;font-weight:600;cursor:pointer;border:none;background:none;font-family:inherit;padding:8px 0;margin-bottom:20px}
        .bk:hover{color:#CDFF00}
        @media(min-width:768px){.cg{grid-template-columns:1fr 1fr !important}.ht{font-size:52px !important}.ms{border-radius:16px;margin-bottom:40px}}
      `}</style>

      <nav style={{padding:"16px 20px",maxWidth:960,margin:"0 auto",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
        <div onClick={goHome} style={{cursor:"pointer"}}>
          <span style={{fontSize:18,fontWeight:900,letterSpacing:"-0.03em",color:C.lime}}>QUES</span>
          <span style={{fontSize:18,fontWeight:900,color:C.lime}}>↗</span>
          <span style={{fontSize:18,fontWeight:900,letterSpacing:"-0.03em",color:C.lime}}>IN</span>
        </div>
        {accessGranted && (
          <button className="bk" onClick={handleLogout} style={{margin:0}}>Sign out</button>
        )}
      </nav>

      {view==="home" && (<>
        <section style={{padding:"48px 20px 32px",maxWidth:520,margin:"0 auto"}}>
          <div className="f1" style={{marginBottom:40}}>
            <div style={{display:"inline-block",padding:"4px 12px",borderRadius:6,background:C.blueDim,color:C.blue,fontSize:11,fontWeight:700,letterSpacing:"0.1em",textTransform:"uppercase",marginBottom:24}}>Jaipur</div>
            <h1 className="ht" style={{fontSize:38,fontWeight:900,lineHeight:1.08,letterSpacing:"-0.035em",marginBottom:18}}>The right communities.<br/>The right venues.<br/>The right people.</h1>
            <p style={{fontSize:15,lineHeight:1.6,color:C.grey,maxWidth:400}}>Questin connects communities who host great things with the spaces and brands that make them happen.</p>
          </div>
          <div className="f2" style={{display:"flex",flexDirection:"column",gap:10}}>
            <button className="bl" onClick={()=>{setUserType("venue");setView("gate");}}>I'm a venue</button>
            <button className="bg" onClick={()=>{setPitchDone(false);setPitchForm({community_name:"",organizer_name:"",email:"",description:"",category:""});setView("pitch");}}>I'm a community</button>
            <button className="bg" onClick={()=>{setUserType("brand");setView("gate");}}>I'm a brand</button>
          </div>
        </section>

        <section style={{padding:"56px 20px",maxWidth:520,margin:"0 auto"}}>
          <div style={{fontSize:11,fontWeight:700,letterSpacing:"0.1em",textTransform:"uppercase",color:C.greyMid,marginBottom:28}}>How it works</div>
          {[{n:"01",t:"Communities pitch",d:"Communities submit what they do and what they need. We review every pitch."},{n:"02",t:"We curate the match",d:"We connect the right community with the right venue based on vibe, audience, and schedule."},{n:"03",t:"Everyone moves",d:"People show up. The venue earns. The community grows. Brands plug in."}].map(s=>(
            <div key={s.n} style={{display:"flex",gap:14,marginBottom:24,alignItems:"flex-start"}}>
              <span style={{fontSize:28,fontWeight:300,color:C.blue,fontStyle:"italic",minWidth:36,fontFamily:"Georgia,serif"}}>{s.n}</span>
              <div><h3 style={{fontSize:15,fontWeight:700,marginBottom:3}}>{s.t}</h3><p style={{fontSize:13,color:C.grey,lineHeight:1.5}}>{s.d}</p></div>
            </div>
          ))}
        </section>

        <section style={{padding:"32px 20px",maxWidth:520,margin:"0 auto"}}>
          {[{title:"For venues",accent:C.lime,items:["Curated footfall on your slow days","Zero operational burden","Feedback report after every session","Data on what's working"]},{title:"For communities",accent:C.blue,items:["Access to venues that match your vibe","A curated audience you can't reach alone","Brand partnership opportunities","You focus on your thing — we handle the rest"]},{title:"For brands",accent:C.cream,items:["Real people in a room, not impressions","Plug into the right community","Turnkey activations","Curated matching based on your campaign"]}].map(col=>(
            <div key={col.title} style={{padding:20,background:C.surface,borderRadius:10,border:`1px solid ${C.border}`,marginBottom:10}}>
              <h3 style={{fontSize:14,fontWeight:800,marginBottom:14,color:col.accent}}>{col.title}</h3>
              {col.items.map((item,i)=><p key={i} style={{fontSize:13,color:C.grey,lineHeight:1.6,marginBottom:6,paddingLeft:14,position:"relative"}}><span style={{position:"absolute",left:0,color:C.greyDark,fontSize:12}}>→</span>{item}</p>)}
            </div>
          ))}
        </section>

        <section style={{padding:"48px 20px",maxWidth:520,margin:"0 auto"}}>
          <div style={{padding:20,background:C.surface,borderRadius:10,border:`1px solid ${C.border}`}}>
            {!waitlistDone ? (<>
              <p style={{fontSize:13,color:C.grey,marginBottom:10}}>Just here to find things to do? We're building something.</p>
              <div style={{display:"flex",gap:8}}>
                <input className="inp" placeholder="your@email.com" type="email" style={{flex:1,padding:"10px 12px",fontSize:13}} value={waitlistEmail} onChange={e=>setWaitlistEmail(e.target.value)} onKeyDown={e=>e.key==="Enter"&&handleWaitlist()} />
                <button style={{background:C.cream,color:C.bg,border:"none",padding:"10px 16px",borderRadius:8,fontWeight:700,fontSize:12,cursor:"pointer",fontFamily:"inherit",whiteSpace:"nowrap",opacity:loading?0.5:1}} onClick={handleWaitlist} disabled={loading}>
                  {loading ? "..." : "Get on the list"}
                </button>
              </div>
            </>) : <p style={{fontSize:14,color:C.lime,fontWeight:600}}>You're in. We'll reach out when it's time.</p>}
          </div>
        </section>

        <footer style={{padding:"28px 20px",borderTop:`1px solid ${C.border}`,maxWidth:520,margin:"0 auto"}}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
            <span style={{fontSize:13,fontWeight:800,color:C.lime}}>QUES↗IN</span>
            <div style={{display:"flex",gap:14,fontSize:12,color:C.greyMid}}>
              <span>Jaipur</span>
              <a href="https://instagram.com/questinhq" target="_blank" rel="noopener noreferrer" style={{color:C.greyMid,textDecoration:"none"}}>@questinhq</a>
            </div>
          </div>
        </footer>
      </>)}

      {view==="gate" && !accessGranted && (
        <section style={{padding:"20px",maxWidth:420,margin:"0 auto"}}>
          <button className="bk" onClick={goHome}>← Back</button>
          {!gateSubmitted ? (<div className="fu">
            <div style={{width:40,height:40,borderRadius:8,background:C.blueDim,display:"flex",alignItems:"center",justifyContent:"center",marginBottom:20,fontSize:18,color:C.blue}}>↗</div>
            <h2 style={{fontSize:26,fontWeight:900,letterSpacing:"-0.03em",marginBottom:6}}>Browse our community catalogue</h2>
            <p style={{fontSize:14,color:C.grey,marginBottom:28,lineHeight:1.5}}>{userType==="brand"?"For brand partners. Request access and we'll get back within 24 hours.":"For venue partners. Request access and we'll get back within 24 hours."}</p>
            <div style={{display:"flex",flexDirection:"column",gap:12}}>
              <div><label style={{fontSize:11,fontWeight:700,color:C.greyMid,display:"block",marginBottom:4,textTransform:"uppercase",letterSpacing:"0.06em"}}>Your name</label><input className="inp" placeholder="Full name" value={gateForm.name} onChange={e=>setGateForm({...gateForm,name:e.target.value})} /></div>
              <div><label style={{fontSize:11,fontWeight:700,color:C.greyMid,display:"block",marginBottom:4,textTransform:"uppercase",letterSpacing:"0.06em"}}>Email</label><input className="inp" placeholder="you@yourvenue.com" type="email" value={gateForm.email} onChange={e=>setGateForm({...gateForm,email:e.target.value})} /></div>
              <div><label style={{fontSize:11,fontWeight:700,color:C.greyMid,display:"block",marginBottom:4,textTransform:"uppercase",letterSpacing:"0.06em"}}>{userType==="brand"?"About your brand":"About your venue"}</label><input className="inp" placeholder={userType==="brand"?"e.g., Jaipur beverage brand, looking for activations":"e.g., Café in C-Scheme, 60 seats, dead on Tuesdays"} value={gateForm.about} onChange={e=>setGateForm({...gateForm,about:e.target.value})} /></div>
              {error && <p style={{fontSize:12,color:"#ff4444",textAlign:"center"}}>{error}</p>}
              <button className="bb" onClick={handleGateSubmit} disabled={loading} style={{marginTop:4}}>
                {loading ? "Submitting..." : "Request access"}
              </button>
              <p style={{fontSize:11,color:C.greyDark,textAlign:"center"}}>We review every request personally.</p>
            </div>
          </div>) : (
            <div className="fu" style={{textAlign:"center",padding:"48px 0"}}>
              <div style={{fontSize:32,color:C.lime,marginBottom:14}}>✓</div>
              <h3 style={{fontSize:20,fontWeight:800,marginBottom:6}}>Request received</h3>
              <p style={{fontSize:14,color:C.grey}}>We'll review and email you within 24 hours.</p>
            </div>
          )}
        </section>
      )}

      {view==="pitch" && (
        <section style={{padding:"20px 20px 100px",maxWidth:420,margin:"0 auto"}}>
          <button className="bk" onClick={goHome}>← Back</button>
          <div className="fu">
            <div style={{width:40,height:40,borderRadius:8,background:C.limeDim,display:"flex",alignItems:"center",justifyContent:"center",marginBottom:20,fontSize:18,color:C.lime}}>✦</div>
            <h2 style={{fontSize:26,fontWeight:900,letterSpacing:"-0.03em",marginBottom:6}}>Pitch your community</h2>
            <p style={{fontSize:14,color:C.grey,marginBottom:10,lineHeight:1.6}}>We connect communities who host great things with the right venues and the right audience in Jaipur.</p>
            <p style={{fontSize:14,color:C.grey,marginBottom:28,lineHeight:1.6}}>Fill out the pitch form. We review within a week. If it's a fit, we'll get you into the right spaces with the right people.</p>

            {!pitchDone ? (
              <div style={{display:"flex",flexDirection:"column",gap:12}}>
                {[
                  {l:"Community name", k:"community_name", p:"e.g., The Sketch Collective"},
                  {l:"Your name",      k:"organizer_name", p:"Organizer or POC"},
                  {l:"Email",          k:"email",          p:"you@example.com"},
                  {l:"Category",       k:"category",       p:"e.g., Creative, Sports, Wellness"},
                ].map(f=>(
                  <div key={f.k}>
                    <label style={{fontSize:11,fontWeight:700,color:C.greyMid,display:"block",marginBottom:4,textTransform:"uppercase",letterSpacing:"0.06em"}}>{f.l}</label>
                    <input className="inp" placeholder={f.p} value={pitchForm[f.k]} onChange={e=>setPitchForm({...pitchForm,[f.k]:e.target.value})} />
                  </div>
                ))}
                <div>
                  <label style={{fontSize:11,fontWeight:700,color:C.greyMid,display:"block",marginBottom:4,textTransform:"uppercase",letterSpacing:"0.06em"}}>What does your community do?</label>
                  <textarea className="inp" rows={4} placeholder="Describe your sessions, audience, and what makes it special." value={pitchForm.description} style={{resize:"vertical"}} onChange={e=>setPitchForm({...pitchForm,description:e.target.value})} />
                </div>
                {error && <p style={{fontSize:12,color:"#ff4444"}}>{error}</p>}
                <button className="bl" onClick={handlePitchSubmit} disabled={loading}>
                  {loading ? "Submitting..." : "Submit pitch →"}
                </button>

                <div style={{marginTop:20,padding:18,background:C.surface,borderRadius:8,border:`1px solid ${C.border}`}}>
                  <p style={{fontSize:12,fontWeight:700,color:C.cream,marginBottom:10}}>What you get with Questin</p>
                  {["Curated venues that fit your vibe","A pre-screened audience for your sessions","Brand partnership opportunities","Feedback reports after every session","You focus on your thing — we handle the rest"].map((item,i)=>(
                    <p key={i} style={{fontSize:12,color:C.grey,lineHeight:1.6,marginBottom:5,paddingLeft:14,position:"relative"}}><span style={{position:"absolute",left:0,color:C.lime,fontSize:11}}>→</span>{item}</p>
                  ))}
                </div>
              </div>
            ) : (
              <div style={{textAlign:"center",padding:"48px 0"}}>
                <div style={{fontSize:32,color:C.lime,marginBottom:14}}>✦</div>
                <h3 style={{fontSize:20,fontWeight:800,marginBottom:6}}>Pitch received</h3>
                <p style={{fontSize:14,color:C.grey}}>We review within a week. If it's a fit, we'll reach out.</p>
              </div>
            )}
          </div>
        </section>
      )}

      {view==="catalogue" && accessGranted && (
        <section style={{padding:"16px 20px 100px",maxWidth:800,margin:"0 auto"}}>
          <button className="bk" onClick={goHome}>← Back</button>
          <div className="f1">
            <h2 style={{fontSize:24,fontWeight:900,letterSpacing:"-0.03em",marginBottom:3}}>Community Catalogue</h2>
            <p style={{fontSize:13,color:C.grey,marginBottom:20}}>{filtered.length} {filtered.length===1?"community":"communities"} available</p>
          </div>
          <div className="f2" style={{marginBottom:20}}>
            <div style={{position:"relative",display:"inline-block"}}>
              <select className="sel" value={catFilter} onChange={e=>setCatFilter(e.target.value)}>
                {categories.map(c=><option key={c} value={c}>{c==="All"?"All categories":c}</option>)}
              </select>
              <span style={{position:"absolute",right:10,top:"50%",transform:"translateY(-50%)",pointerEvents:"none",color:C.grey,fontSize:9}}>▼</span>
            </div>
          </div>

          {loading && (
            <div style={{textAlign:"center",padding:48,color:C.greyMid,fontSize:14}}>Loading communities...</div>
          )}

          {!loading && (
            <div className="cg f3" style={{display:"grid",gridTemplateColumns:"1fr",gap:14}}>
              {filtered.map(c=>{
                const cc=catColor(c.category);
                return (
                  <div key={c.id} className="crd">
                    <div style={{height:130,background:`url(${c.image}) center/cover`,position:"relative"}}>
                      <span style={{position:"absolute",top:10,left:10,padding:"3px 9px",borderRadius:4,fontSize:10,fontWeight:700,letterSpacing:"0.06em",textTransform:"uppercase",background:cc.bg,color:cc.color}}>{c.category}</span>
                    </div>
                    <div style={{padding:14}}>
                      <h3 style={{fontSize:16,fontWeight:800,letterSpacing:"-0.02em",marginBottom:4}}>{c.name}</h3>
                      <p style={{fontSize:13,color:C.grey,lineHeight:1.4,marginBottom:10}}>{c.tagline}</p>
                      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr 1fr",gap:6,marginBottom:10}}>
                        {[{l:"Size",v:c.groupSize},{l:"Price",v:c.price},{l:"Duration",v:c.duration},{l:"Freq",v:c.frequency}].map(d=>(
                          <div key={d.l}><div style={{color:C.greyMid,fontSize:10,textTransform:"uppercase",letterSpacing:"0.04em",marginBottom:1}}>{d.l}</div><div style={{fontSize:12,fontWeight:600}}>{d.v}</div></div>
                        ))}
                      </div>
                      <p style={{fontSize:11,color:C.greyMid,marginBottom:12}}><span style={{fontWeight:700,color:C.grey}}>Needs: </span>{c.venueNeeds}</p>
                      {requestSent===c.id ? (
                        <div style={{padding:10,background:C.limeDim,borderRadius:6,textAlign:"center",fontSize:13,color:C.lime,fontWeight:700}}>Request sent — we'll connect you within 48 hours</div>
                      ) : (
                        <button className="bl" style={{padding:"11px 20px",fontSize:13}} onClick={()=>setRequestingId(c.id)}>Request this community</button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {!loading && filtered.length===0 && (
            <div style={{textAlign:"center",padding:48,color:C.greyMid,fontSize:14}}>No communities match this filter.</div>
          )}

          {requestingId && (
            <div className="mo" onClick={e=>{if(e.target===e.currentTarget)setRequestingId(null);}}>
              <div className="ms">
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:16}}>
                  <h3 style={{fontSize:16,fontWeight:800,color:C.white}}>Request {communities.find(c=>c.id===requestingId)?.name}</h3>
                  <button onClick={()=>setRequestingId(null)} style={{background:"none",border:"none",color:C.grey,fontSize:18,cursor:"pointer"}}>×</button>
                </div>
                <p style={{fontSize:12,color:C.grey,marginBottom:16,lineHeight:1.5}}>Tell us a bit more so we can make the right introduction.</p>
                <div style={{display:"flex",flexDirection:"column",gap:10}}>
                  {[{l:"Point of contact",p:"Who should we coordinate with?",k:"poc"},{l:"Phone / WhatsApp",p:"+91",k:"phone"},{l:"Preferred dates or times",p:"e.g., Tuesday evenings, any weekend",k:"dates"},{l:"Expected capacity",p:"How many people can you host?",k:"capacity"}].map(f=>(
                    <div key={f.k}><label style={{fontSize:10,fontWeight:700,color:C.greyMid,display:"block",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.06em"}}>{f.l}</label><input className="inp" style={{fontSize:13,padding:"10px 12px"}} placeholder={f.p} value={requestForm[f.k]} onChange={e=>setRequestForm({...requestForm,[f.k]:e.target.value})} /></div>
                  ))}
                  <div><label style={{fontSize:10,fontWeight:700,color:C.greyMid,display:"block",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.06em"}}>Revenue model preference</label>
                    <div style={{position:"relative"}}><select className="sel" style={{width:"100%",fontSize:13,padding:"10px 32px 10px 12px"}} value={requestForm.revenue} onChange={e=>setRequestForm({...requestForm,revenue:e.target.value})}><option value="">Select...</option><option value="share">Revenue share on F&B</option><option value="flat">Flat fee per session</option><option value="open">Open to discuss</option></select><span style={{position:"absolute",right:10,top:"50%",transform:"translateY(-50%)",pointerEvents:"none",color:C.grey,fontSize:9}}>▼</span></div>
                  </div>
                  <div><label style={{fontSize:10,fontWeight:700,color:C.greyMid,display:"block",marginBottom:3,textTransform:"uppercase",letterSpacing:"0.06em"}}>Anything else? (optional)</label><input className="inp" style={{fontSize:13,padding:"10px 12px"}} placeholder="Requirements, questions, etc." value={requestForm.notes} onChange={e=>setRequestForm({...requestForm,notes:e.target.value})} /></div>
                  {error && <p style={{fontSize:12,color:"#ff4444"}}>{error}</p>}
                  <button className="bb" style={{marginTop:2,fontSize:14}} onClick={()=>handleRequest(requestingId)} disabled={loading}>
                    {loading ? "Sending..." : "Send request"}
                  </button>
                </div>
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
}