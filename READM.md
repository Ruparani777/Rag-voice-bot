# 🚌 Movi — Multimodal Transport Management Agent

Movi is an AI-powered, multimodal assistant built for the MoveInSync Shuttle admin console. It helps transport managers orchestrate both static (Stops, Paths, Routes) and dynamic (Trips, Deployments, Vehicles) operations using text, voice and image inputs. The project bundles a FastAPI backend, a React/Vite admin console, and a seeded SQLite database for demos.

This README summarizes architecture, setup, demo steps, agent capabilities, and troubleshooting notes.

---

## Key highlights

- LangGraph-style stateful agent implemented as a lightweight state machine (no external graph library required)
- Multimodal frontend: text chat, voice (Web Speech API), and image filename matching (mock/vision stub)
- Consequence-aware actions: confirmation required before risky operations (e.g., removing a vehicle with bookings)
- Seeded SQLite DB for immediate demos (stops, paths, routes, vehicles, drivers, trips, deployments)
- ≥10 data-aware actions (CRUD and query operations for transport objects)

---

## Repository layout

```
movi-ai-transport-agent/
├── backend/               # FastAPI backend (SQLModel + SQLite)
│   ├── app/
│   │   ├── main.py        # FastAPI entrypoint
│   │   ├── models.py      # SQLModel ORM models
│   │   ├── crud.py        # DB helpers
│   │   ├── schemas.py     # Pydantic/SQLModel schemas
│   │   ├── database.py    # SQLite configuration & seed
│   │   └── seed_data.py   # DB seeding logic
│   ├── db/
│   │   └── movi.db        # Seeded SQLite file (created on first run)
│   └── requirements.txt
├── frontend/              # React + Vite admin console
│   ├── src/
│   │   ├── components/    # UI components (MoviAssistant, BusDashboard, ManageRoute)
│   │   ├── hooks/         # useSpeech, etc.
│   │   └── lib/           # api client
│   ├── package.json
│   └── vite.config.ts
├── langgraph_agent/       # Lightweight agent state machine + tools
│   ├── graph.py
│   └── tools.py
└── README.md
```

---

## Architecture (overview)

[React Admin Console]  <--REST-->  [FastAPI Backend]  <--SQLModel-->  [SQLite DB]
       |                                   |
       | Web Speech API / file uploads     | LangGraph-style state machine
       v                                   v
  Movi Assistant Panel ---------> MoviAgent.handle_action()
                                      • 10+ DB tools (CRUD + queries)
                                      • Consequence checks & confirmation loop

The frontend proxies `/api` requests to `http://localhost:8000`, so run both apps concurrently for a full local demo.

---

## Agent capabilities (sample actions)

Implemented tools include (but not limited to):

- list_unassigned_vehicles
- get_trip_status
- list_stops_for_path
- list_routes_using_path
- assign_vehicle_to_trip
- remove_vehicle_from_trip (requires confirmation when consequence detected)
- create_stop
- create_path
- create_route
- update_route_status
- list_daily_trips
- list_deployments
- list_available_drivers

Consequence checking warns when an action may be risky (e.g., removing a vehicle that has bookings) and requires an explicit confirmation to proceed.

---

## Prerequisites

- Python 3.11+ (for backend)
- Node.js 18+ and npm (for frontend)
- pnpm optional
- Git (optional for cloning)

Windows-specific notes: the README commands below use PowerShell-friendly forms where appropriate.

---

## Quickstart (local)

Run the backend and frontend concurrently. The first backend run creates `db/movi.db` and seeds it with demo data.

1) Backend (FastAPI)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start with auto-reload
uvicorn app.main:app --reload
```

On first run the server will create and seed `backend/db/movi.db` with:

- 5 stops, 2 paths, 2 routes
- 3 vehicles (2 active, 1 inactive), 3 drivers
- 2 daily trips and 1 active deployment

2) Frontend (React + Vite)

```powershell
cd frontend
npm install
npm run dev
```

Open the app in your browser (default Vite URL shown in terminal, typically `http://127.0.0.1:5173`). The frontend proxies API calls to `http://localhost:8000`.

---

## Demo script (2–5 minutes)

1. Show static assets: open ManageRoute and list Stops/Paths/Routes.
2. From ManageRoute, add a new Stop using the form (Movi executes the action).
3. Switch to BusDashboard. Ask Movi (chat panel): “List unassigned vehicles.”
4. Trigger “Remove the vehicle from ‘Bulk - 00:01’.” Show consequence warning, confirm, then proceed.
5. Upload a sample screenshot named `Bulk-00-01.png` to `/vision/match` to demonstrate mock image matching.
6. Use voice: ask “What is the status of Bulk - 08:30?” to demo STT & TTS flow.

---

## API examples

Agent action (example request):

```http
POST http://127.0.0.1:8000/agent/action
Content-Type: application/json

{
  "intent": "list_daily_trips",
  "parameters": {},
  "context": { "currentPage": "busDashboard" }
}
```

Response when consequence detected (example):

```json
{
  "message": "Confirmation required before executing action.",
  "consequence": {
    "requires_confirmation": true,
    "reason": "60% of seats already booked for Bulk – 08:30."
  },
  "data": null
}
```

To confirm and proceed:

```http
POST http://127.0.0.1:8000/agent/action
Content-Type: application/json

{
  "intent": "remove_vehicle_from_trip",
  "parameters": { "trip_id": 1, "confirmed": true },
  "context": { "currentPage": "busDashboard" }
}
```

Vision mock API (upload):

```http
POST http://127.0.0.1:8000/vision/match
Content-Type: multipart/form-data
file: <screenshot.png>
```

The mock maps filenames to trip names and returns a confidence score for demo purposes.

---

## Database schema (high level)

- Stops: stop_id, name, latitude, longitude
- Paths: path_id, path_name, ordered_stop_ids
- Routes: route_id, path_id, display_name, shift_time, direction, status
- Vehicles: vehicle_id, license_plate, type, capacity, is_active
- Drivers: driver_id, name, phone_number, is_available
- DailyTrips: trip_id, route_id, display_name, booking_status_percentage, live_status
- Deployments: deployment_id, trip_id, vehicle_id, driver_id

---

## Debugging & utilities

Start backend with debug logs:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level debug
```

If port 8000 is in use (PowerShell):

```powershell
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

Reset the seeded database (deletes `db/movi.db`):

```powershell
Remove-Item backend\db\movi.db -ErrorAction SilentlyContinue
# Restart backend to recreate and reseed
```

Test the agent endpoint from PowerShell:

```powershell
$body = @{
    intent = "list_daily_trips"
    parameters = @{}
    context = @{ currentPage = "busDashboard" }
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/agent/action' `
  -Method POST `
  -ContentType 'application/json' `
  -Body $body
```

---

## Testing & validation

- Use cURL/Postman to hit REST endpoints (`/stops`, `/routes`, `/deployments`, `/agent/action`).
- Frontend: run `npm run lint` and follow the demo script for manual validation.

---

## Future enhancements

- Replace filename-based vision stub with an actual OCR/vision pipeline
- Expand LangGraph-style agent to use LLM-based intent parsing and memory
- Add role-based access control and multi-user session contexts
- Integrate live telemetry for real-time vehicle tracking

---

## Credits

- Prepared for Movi_ai_transport agent
- Author: Ruparani Thupakula
- Date: November 2025

---

If you'd like, I can also:

- Add a quick `docker-compose` to run both backend and frontend together
- Produce a short demo video script and checklist
- Generate Postman collection for the main API endpoints

Tell me which addition you'd like and I will add it.
