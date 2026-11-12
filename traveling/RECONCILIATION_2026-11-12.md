# Travel data reconciliation — 2026-11-12

## Author-confirmed policy
- Flight count: 277 currently recorded flown legs; do not increase without reconciling the extra Naples–Geneva flight.
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
1. NAP → GVA, July 2022: author says cancelled then rebooked and flown; GitHub currently marks flight-0065 cancelled and counts 277 other flown legs. Changing it to flown yields 278. Confirm where that extra leg should reconcile before changing status/count.
2. No globally geolocated city currently for 2026 Honduras; ask author.
3. Additional year-country stay periods lack dated place references: 2011 JP; 2022 PA; 2024 BE; 2025 CL, PE, DK, GT; 2026 FR, FI, EE, CN. Ask author before adding visit/place coordinates.
4. Workbook flight-pair mismatches were previously audited; confirmed pairs above were kept, without inventing new legs.

## Data integrity notes
- Country code GB and MD duplicate category variants are present in the original archived country data and intentionally preserved.
- The surface route CSV now has 143 schematic legs, one more than the previous baseline because Moscow was confirmed as an intermediate train stop.
- The only non-rendered flown flight geometry is ATH → ATH, as its endpoints coincide.
