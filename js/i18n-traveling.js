"use strict";
/* Travel activity captions translated across the portfolio's seven interface languages.
   Personal site/mountain names remain as originally recorded. */
(() => {
  const tr = (ko,zh,es,tw,fr,de) => [null,ko,zh,es,tw,fr,de];
  window.PortfolioDetailedTranslations = {
    traveling: {
      "#activities .sectionhead .eyebrow":tr(
        "03 / 길 위에서","03 / 路上的经历","03 / EN EL CAMINO",
        "03 / 旅途之中","03 / EN CHEMIN","03 / UNTERWEGS"
      ),
      "#activities .sectionhead h2":tr(
        "산과 바다, 그리고 파도.","山径、海洋与浪潮。","Senderos, profundidades y olas.",
        "山徑、海洋與浪潮。","Sentiers, profondeurs et vagues.","Wege, Tiefen und Wellen."
      ),
      "#activities .sectionhead > span":tr(
        "여정의 또 다른 기록","旅程之外的记录","Más allá del itinerario",
        "旅程之外的紀錄","Au-delà de l'itinéraire","Abseits der Reiseroute"
      ),
      "#activities .activity-intro":tr(
        "트레킹, 수중 탐험, 서핑의 기록입니다. 날짜는 개인 여행 기록을 따릅니다.",
        "记录徒步、潜水与冲浪经历。日期来自个人记录。",
        "Un registro de senderismo, buceo y surf. Las fechas provienen de mis notas.",
        "這裡記錄健行、潛水與衝浪。日期來自個人紀錄。",
        "Une archive de randonnées, de plongées et de surf. Les dates proviennent de mes notes.",
        "Ein Archiv für Wanderungen, Tauchgänge und Surfen. Die Daten stammen aus meinen Aufzeichnungen."
      ),
      "#trekkingFold > summary > strong":tr(
        "트레킹","徒步","Senderismo","健行","Randonnée","Wandern"
      ),
      "#scubaFold > summary > strong":tr(
        "스쿠버 다이빙 · AOW","水肺潜水 · AOW","Buceo · AOW","水肺潛水 · AOW","Plongée sous-marine · AOW","Gerätetauchen · AOW"
      ),
      "#surfFold > summary > strong":tr(
        "서핑","冲浪","Surf","衝浪","Surf","Surfen"
      ),
      "#activities .activity-footnote":tr(
        "고도는 직접 도달한 최고점이 아닌 산 정상 또는 명소의 기준 고도입니다. 릴라 일곱 호수는 가장 높은 호수, 레인보우 마운틴은 전망대 기준입니다. 세로토코는 개인 최고 기록으로 강조했습니다(실제 도달 5,604m, 산 정상 5,604m).",
        "海拔为山峰或景点的参考高度，不代表本人一定抵达该高度。七座里拉湖取最高湖泊，彩虹山取观景台高度。Cerro Toco 标为个人纪录（实际到达 5,604 米，山顶 5,604 米）。",
        "Las altitudes indican la cima o la altura de referencia del lugar, no necesariamente el punto alcanzado. Los Siete Lagos de Rila usan el lago más alto y la Montaña Arcoíris, el mirador. Cerro Toco se destaca como récord personal (5.604 m alcanzados; cima de 5.604 m).",
        "海拔為山峰或景點的參考高度，不表示本人一定抵達該高度。七座里拉湖採最高湖泊，彩虹山採觀景臺高度。Cerro Toco 標示為個人紀錄（實際抵達 5,604 公尺，山頂 5,604 公尺）。",
        "Les altitudes sont celles des sommets ou sites de référence, et non forcément celles atteintes. Les sept lacs de Rila utilisent le lac le plus haut ; la montagne Arc-en-ciel, son belvédère. Cerro Toco est mon record personnel (5 604 m atteints ; sommet à 5 604 m).",
        "Die Höhenangaben beziehen sich auf Gipfel oder Orte, nicht unbedingt auf die tatsächlich erreichte Höhe. Bei den Sieben Rila-Seen gilt der höchste See, beim Rainbow Mountain der Aussichtspunkt. Cerro Toco ist mein persönlicher Rekord (5.604 m erreicht; Gipfel 5.604 m)."
      ),
      "#highlights .sectionhead .eyebrow":tr(
        "04 / 여정 너머의 기록","04 / 行程之外","04 / MÁS ALLÁ DEL ITINERARIO",
        "04 / 旅程之外","04 / AU-DELÀ DE L'ITINÉRAIRE","04 / ABSEITS DER ROUTE"
      )
    }
  };
})();
