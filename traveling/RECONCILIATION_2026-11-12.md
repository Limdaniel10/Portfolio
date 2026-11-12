# Travel data reconciliation — 2026-11-12

## Author-confirmed policy
- **Final author-confirmed flight count: 278 actually flown legs.** One separate cancelled NAP → GVA booking is excluded. NAP → ZRH was flown after cancellation, followed by a train to Geneva.
- Countries: 193 UN members plus Vatican City are eligible; Taiwan is excluded. 90 visited countries are currently marked, unchanged.
- Airport overnight stays: 45 (confirmed).
- Country/territory map routes: schematic straight connecting lines, not literal track geometry.
- GitHub CSV is the locally maintained archive. If Google Sheets sync is configured, Google Sheets is the build-time source and needs the same verified changes.

## Confirmed changes
- 2024 ATH → ATH: flown diversion returned to origin; ATH → DBV: flown replacement the next day. Both were already in the 277 flown legs. Exact dates remain unresolved; existing broad 2024 month range retained.
- 2026 trans-Siberian train: St Petersburg → Moscow → Irkutsk → Vladivostok, all by train. St Petersburg → Irkutsk journey spanned May–June; Irkutsk → Vladivostok is June. Exact Moscow segment dates remain unspecified.
- 2026 Irkutsk ↔ Khuzhir: Bus/shuttle, not car. Exact dates remain unspecified.
- 2023 Managua airport: MGA; CDG → CPH occurred twice; LAX → LGW was flown.
- 2024 CDG → AUH → ICN; TSF → BVA; CJC → SCL; SCL → AEP were correct in GitHub.
- 2026 ATL ↔ IAH round trip confirmed.

## Pending explicit confirmation — no inferred edits
1. **Resolved:** NAP → GVA was cancelled; NAP → ZRH was flown the next day. Zurich → Geneva was by train, and the final flight total is 278.
2. No globally geolocated city currently for 2026 Honduras; ask author.
3. Additional year-country stay periods lack dated place references: 2011 JP; 2022 PA; 2024 BE; 2025 CL, PE, DK, GT; 2026 FR, FI, EE, CN. Ask author before adding visit/place coordinates.
4. Workbook flight-pair mismatches were previously audited; confirmed pairs above were kept, without inventing new legs.

## Data integrity notes
- Country code GB and MD duplicate category variants are present in the original archived country data and intentionally preserved.
- The surface route CSV has **144 schematic legs**, two more than the original 142: Moscow was added as an intermediate train stop; Zurich Airport → Geneva was added as a 2022 rail transfer.
- The only non-rendered flown flight geometry is ATH → ATH, as its endpoints coincide.

## Additional author verification — 2026-11-12 (follow-up)
- Checked all 278 Flights.csv rows for NAP: only flight-0064 BCN → NAP (recorded_flown) and flight-0065 NAP → GVA (cancelled). Author reports rebooking and flying NAP → GVA, but the other actual flown segment is not independently recorded. Changing status alone would raise flown count from confirmed 277 to 278. Keep flight-0065 unchanged pending reconciliation; do not invent or delete a flight.
- Added existing-city visits: 2024-02 Brussels (Belgium stay window), 2025-10 Copenhagen (month only; did not assume both October visits were in the city), 2025-12 Antigua (Guatemala stay window), 2026-05 Tallinn (Estonia stay window), 2026-06 Beijing (China stay window). All use existing place coordinates; a country-stay window is not a claim of exact city entry/exit dates.
- Author confirmed transit only, no city additions: Honduras 2026-04-30 (border transit), Panama 2022-12-30, Chile 2025-01-02 (SCL airport transit), Finland 2026-05-26 (HEL airport transit).
- Author confirmed a visited city existed, but supplied no city name: Japan 2011 and Peru 2025; no new city or date added. Peru has pre-existing visit records spanning 2024-12 through 2025-01 under year 2024; do not multiply those visits without identifying the 2025 city.
- France 2026-05-23 to 2026-05-25: answer 'ㅍ' insufficient to establish a city, retained as unresolved.
- September/October 2025 Denmark dates span two stay records, but Copenhagen was only confirmed in October, not assigned to a specific stay.
- Source-of-truth: GitHub CSV, unless Google Sheet sync is configured later, in which case these author-confirmed rows must be entered in the live sheet too.

## Final city and replacement-flight confirmations — 2026-11-12
- **Japan, 2011:** both Japan stops were Tokyo. Attached existing place-0006 to the two independently recorded country-stay windows (2011-07-30 and 2011-08-05..06). No new place coordinates or country added.
- **France, 2026:** Paris was visited in the existing 2026-05-23..25 country-stay window. Attached existing place-0021; exact day(s) in the city were not separately specified.
- **Peru → Bolivia:** route Lima → Cusco → Puno → Copacabana confirmed as an itinerary, already represented by place-0189/0190/0191/0192 and late-2024 surface legs Cusco → Puno → Copacabana. No claim about exact transit method for the Lima leg was added; original 2024-12 route dates preserved. The 2024-12 / 2025-01 cross-year visits were already recorded, and the map filter was corrected to honor 2025-01 when the record's primary year is 2024. Recorded 2025-01 SCL → LIM → PTY flights support a separate 2025 stop in Peru but do not establish a second Cusco/Puno/Copacabana trip.
- **Naples cancellation and rebooking:** confirmed cancelled NAP → GVA in July 2022 and actually flown NAP → ZRH on the following day. Kept the existing cancelled record flight-0065, created flown flight-0279 NAP → ZRH, and added ZRH using OurAirports coordinates. Exact day is not confirmed: assigned 2022-07 month only.
- **Flight-count discrepancy RESOLVED by the author:** 278 flown flight legs is the final agreed count, including NAP → ZRH and excluding cancelled NAP → GVA. No other flight was deleted or reclassified.

## Final author confirmation — flight total and Swiss rail transfer
- User confirmed **278 flights** as the final flown-leg total, superseding the earlier 277 estimate. Exactly one cancelled booking remains excluded from this count.
- The July 2022 replacement flight was Naples (NAP) → Zurich (ZRH), followed by **train from Zurich to Geneva**. A schematic rail segment `route-093-leg-01` was added from the recorded Zurich Airport coordinate to the existing Geneva city coordinate; the exact train station and day are not claimed.
- Flight total shown on Traveling is 278, derived from the Flights CSV at build time (with an HTML fallback also updated).
