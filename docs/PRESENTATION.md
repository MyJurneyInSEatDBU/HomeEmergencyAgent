# Home Emergency Agent —

## — Hook, Problem & Goal

**Quick question :**
- If your kitchen caught fire right now, how many of you could respond in **10 seconds**?
- What if it was a flood while you’re **not home**?

**Problem:** Homes face sudden emergencies (fire, flood).  
Manual response is slow, inconsistent, and sometimes impossible.

**Goal:** Build an **autonomous emergency agent** that:
- detects the state (`none`, `fire`, `flood`)
- deploys the right response
- clears materials from danger zones
- keeps clear logs + owner notification (simulated)

---

##  2 — What We Built

**Autonomous response flow**
1. Status change triggers detection
2. Drone dispatch
3. Fire suppression or flood evacuation
4. Material clearance
5. Resolution + owner notification

**Why this is a goal‑based agent**
- **Goal:** bring the home back to a safe state  
- **State:** emergency type, fire intensity, flood level, materials inside/outside  
- **Actions:** move drone, spray water, evacuate, clear materials  
- **Decision loop:** keep acting until the goal state (`emergency = none`) is reached
**Live visual system**
- Fire, flood, drone, materials, and water spray

---

##  3 — Architecture (Simple View)

**Flow (summary)**

```

