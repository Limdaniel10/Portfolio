"use strict";
/* About: human-reviewed interface translations (EN source remains in HTML).
   Index order: English, Korean, Simplified Chinese, Spanish,
   Traditional Chinese (Taiwan), French, German. */
(() => {
  const tr = (ko, zh, es, tw, fr, de) => [null, ko, zh, es, tw, fr, de];
  window.PortfolioDetailedTranslations = {
    about: {
      ".about-hero .eyebrow": tr(
        "개인 아카이브 &nbsp; / &nbsp; 기록하는 중",
        "个人档案 &nbsp; / &nbsp; 持续更新",
        "ARCHIVO PERSONAL &nbsp; / &nbsp; EN CONSTRUCCIÓN",
        "個人檔案 &nbsp; / &nbsp; 持續更新",
        "ARCHIVES PERSONNELLES &nbsp; / &nbsp; EN COURS",
        "PERSÖNLICHES ARCHIV &nbsp; / &nbsp; IM AUFBAU"
      ),
      ".about-hero h1": tr(
        "소개<span>.</span>", "关于我<span>.</span>", "Sobre mí<span>.</span>",
        "關於我<span>.</span>", "À propos<span>.</span>", "Über mich<span>.</span>"
      ),
      ".about-hero .textlink": tr(
        '나에 대해 더 알아보기 <span>↘</span>',
        '了解更多 <span>↘</span>',
        'Conoce un poco más sobre mí <span>↘</span>',
        '進一步認識我 <span>↘</span>',
        'En savoir plus sur moi <span>↘</span>',
        'Mehr über mich <span>↘</span>'
      ),
      ".orbit-center > span": tr("출발점", "起点", "DESDE", "起點", "DÉPART", "AUS"),
      ".orbit-center > em": tr("세상 어디로든", "走向世界", "hacia cualquier lugar", "走向世界", "vers le monde", "in die ganze Welt"),
      ".orbit-label-one": tr("애틀랜타 · 현재", "亚特兰大 · 现在", "ATLANTA · AHORA", "亞特蘭大 · 現在", "ATLANTA · AUJOURD’HUI", "ATLANTA · JETZT"),
      ".orbit-label-two": tr("피닉스 · 다음", "菲尼克斯 · 下一站", "PHOENIX · PRÓXIMO", "鳳凰城 · 下一站", "PHOENIX · ENSUITE", "PHOENIX · ALS NÄCHSTES"),
      ".art-foot": tr(
        "계속 성장하는 사람 &nbsp; / &nbsp; 2026",
        "不断成长的人 &nbsp; / &nbsp; 2026",
        "UNA HISTORIA EN MARCHA &nbsp; / &nbsp; 2026",
        "持續成長的人 &nbsp; / &nbsp; 2026",
        "UNE PERSONNE EN DEVENIR &nbsp; / &nbsp; 2026",
        "EIN MENSCH IM WANDEL &nbsp; / &nbsp; 2026"
      ),
      "#numbers .section-heading .eyebrow": tr(
        "01 / 숫자로 보는 기록", "01 / 数字中的记录", "01 / EN CIFRAS",
        "01 / 數字中的紀錄", "01 / QUELQUES CHIFFRES", "01 / IN ZAHLEN"
      ),
      "#numbers .section-heading .aside-note": tr(
        "지금도 써 내려가는 몇 개의 장면.", "仍在续写的几个篇章。",
        "Algunos capítulos que siguen creciendo.", "仍在續寫的幾個篇章。",
        "Quelques chapitres, encore en cours.", "Ein paar Kapitel, die weitergehen."
      ),
      "#numbers .number-grid > div:nth-child(1) span": tr(
        "방문 국가", "到访国家", "Países visitados", "造訪國家", "Pays visités", "Besuchte Länder"
      ),
      "#numbers .number-grid > div:nth-child(2) span": tr(
        "완독 도서", "读完的书籍", "Libros leídos", "讀完的書籍", "Livres lus", "Gelesene Bücher"
      ),
      "#numbers .number-grid > div:nth-child(3) span": tr(
        "일기·기록", "日记篇数", "Entradas de diario", "日記篇數", "Notes de journal", "Tagebucheinträge"
      ),
      "#numbers .number-grid > div:nth-child(4) span": tr(
        "공항에서 보낸 밤", "在机场过夜的次数", "Noches en aeropuertos", "在機場過夜的次數", "Nuits passées dans des aéroports", "Nächte auf Flughäfen"
      ),
      "#pursuits .section-heading .eyebrow": tr(
        "02 / 나의 관심사", "02 / 我的热爱", "02 / MIS INTERESES",
        "02 / 我的興趣", "02 / MES CENTRES D’INTÉRÊT", "02 / MEINE INTERESSEN"
      ),
      "#pursuits .section-heading .aside-note": tr(
        "다른 기록도 둘러보세요.", "探索其他档案。",
        "Explora los otros archivos.", "探索其他檔案。",
        "Découvrez les autres archives.", "Entdecke die anderen Archive."
      ),
      "#pursuits .pursuit-grid a:nth-child(1) h3": tr("공학", "工程", "Ingeniería", "工程", "Ingénierie", "Ingenieurwesen"),
      "#pursuits .pursuit-grid a:nth-child(2) h3": tr("글쓰기", "写作", "Escritura", "寫作", "Écriture", "Schreiben"),
      "#pursuits .pursuit-grid a:nth-child(3) h3": tr("여행", "旅行", "Viajes", "旅行", "Voyages", "Reisen"),
      "#pursuits .pursuit-grid a:nth-child(4) h3": tr("독서", "阅读", "Lectura", "閱讀", "Lecture", "Lesen"),
      "#present .section-heading .eyebrow": tr(
        "03 / 현재", "03 / 此时此刻", "03 / EL PRESENTE",
        "03 / 此時此刻", "03 / LE PRÉSENT", "03 / GEGENWART"
      ),
      "#present .section-heading .aside-note": tr(
        "애틀랜타에서 피닉스로.", "从亚特兰大到菲尼克斯。",
        "De Atlanta a Phoenix.", "從亞特蘭大到鳳凰城。",
        "D’Atlanta à Phoenix.", "Von Atlanta nach Phoenix."
      ),
      "#present .now-grid article:nth-child(1) .eyebrow": tr(
        "현재 / 애틀랜타", "现在 / 亚特兰大", "AHORA / ATLANTA",
        "現在 / 亞特蘭大", "AUJOURD’HUI / ATLANTA", "JETZT / ATLANTA"
      ),
      "#present .now-grid article:nth-child(2) .eyebrow": tr(
        "다음 / 피닉스", "下一站 / 菲尼克斯", "PRÓXIMO / PHOENIX",
        "下一站 / 鳳凰城", "ENSUITE / PHOENIX", "ALS NÄCHSTES / PHOENIX"
      ),
      "#present .now-grid article:nth-child(1) p": tr(
        "2027년 5월 졸업을 목표로 항공우주공학 석사과정을 마무리하고 있습니다.",
        "正在完成航空航天工程硕士学位，预计于 2027 年 5 月毕业。",
        "Estoy terminando una maestría en Ingeniería Aeroespacial, con graduación prevista para mayo de 2027.",
        "正在完成航太工程碩士學位，預計於 2027 年 5 月畢業。",
        "Je termine un master en ingénierie aérospatiale, avec une obtention du diplôme prévue en mai 2027.",
        "Ich schließe meinen Master in Luft- und Raumfahrttechnik voraussichtlich im Mai 2027 ab."
      ),
      "#present .now-grid article:nth-child(2) p": tr(
        "2027년 6월부터 리소그래피 모듈 공정 엔지니어로 근무할 예정입니다.",
        "计划于 2027 年 6 月入职，担任光刻模块工艺工程师。",
        "Me incorporaré en junio de 2027 como ingeniero de procesos del módulo de litografía.",
        "預計於 2027 年 6 月到職，擔任微影模組製程工程師。",
        "Je rejoindrai TSMC Arizona en juin 2027 comme ingénieur procédés au sein du module de photolithographie.",
        "Ab Juni 2027 werde ich als Prozessingenieur im Lithografie-Modul arbeiten."
      ),
      "#path .section-heading .eyebrow": tr(
        "04 / 지나온 길", "04 / 走过的路", "04 / MI RECORRIDO",
        "04 / 走過的路", "04 / MON PARCOURS", "04 / MEIN WEG"
      ),
      "#path .section-heading .aside-note": tr(
        "간단히 돌아본 나의 발자취.", "一段简短的个人经历。",
        "Una versión breve de mi recorrido.", "簡短回顧一路走來的足跡。",
        "Mon parcours en quelques étapes.", "Mein Weg in Kürze."
      ),
      "#path .accordion-stack details:nth-child(1) summary": tr(
        '연혁 <span>+</span>', '时间线 <span>+</span>', 'Trayectoria <span>+</span>',
        '時間軸 <span>+</span>', 'Parcours <span>+</span>', 'Zeitleiste <span>+</span>'
      ),
      "#path .accordion-stack details:nth-child(2) summary": tr(
        '연락처 <span>+</span>', '联系方式 <span>+</span>', 'Contacto <span>+</span>',
        '聯絡方式 <span>+</span>', 'Me contacter <span>+</span>', 'Kontakt <span>+</span>'
      ),
      "#path .accordion-stack details:nth-child(1) .time-row:nth-child(1) p": tr(
        "대한민국 부산에서 태어나 자랐습니다.", "出生并成长于韩国釜山。",
        "Nací y crecí en Busan, Corea del Sur.", "在韓國釜山出生、長大。",
        "Je suis originaire de Busan, en Corée du Sud, où j’ai grandi.",
        "Geboren und aufgewachsen in Busan, Südkorea."
      ),
      "#path .accordion-stack details:nth-child(1) .time-row:nth-child(2) p": tr(
        "한국외대부설고 국제과에서 중국어와 국제학을 공부했습니다.",
        "就读于韩国外国语大学附属高中（HAFS），学习中文及国际研究。",
        "Estudié chino y estudios internacionales en Hankuk Academy of Foreign Studies (HAFS).",
        "就讀韓國外國語大學附屬高中（HAFS），學習中文與國際研究。",
        "J’ai étudié le chinois et les relations internationales au lycée Hankuk Academy of Foreign Studies (HAFS).",
        "An der Hankuk Academy of Foreign Studies (HAFS) beschäftigte ich mich mit Chinesisch und internationalen Studien."
      ),
      "#path .accordion-stack details:nth-child(1) .time-row:nth-child(3) p": tr(
        "대한민국 국군정보사령부에서 군 복무를 했습니다.",
        "在韩国国防情报司令部服兵役。",
        "Presté servicio militar en el Mando de Inteligencia de Defensa de Corea del Sur.",
        "於韓國國防情報司令部服兵役。",
        "J’ai effectué mon service militaire au sein du commandement du renseignement de la défense sud-coréen.",
        "Ich leistete meinen Militärdienst beim südkoreanischen Militärnachrichtendienst."
      ),
      "#path .accordion-stack details:nth-child(1) .time-row:nth-child(4) p": tr(
        "조지아텍에서 항공우주공학을 공부하고 있습니다.",
        "在佐治亚理工学院学习航空航天工程。",
        "Estudio ingeniería aeroespacial en Georgia Tech.",
        "在喬治亞理工學院攻讀航太工程。",
        "J’étudie l’ingénierie aérospatiale à Georgia Tech.",
        "Ich studiere Luft- und Raumfahrttechnik an der Georgia Tech."
      ),
      "#path .accordion-stack details:nth-child(1) .time-row:nth-child(5) p": tr(
        "유럽에서 1년간 교환·해외 수학을 했습니다.",
        "在欧洲交流学习了一年。",
        "Pasé un año estudiando en Europa.",
        "曾在歐洲留學一年。",
        "J’ai passé une année d’études en Europe.",
        "Ein Jahr lang studierte ich in Europa."
      ),
      "#path .accordion-stack details:nth-child(1) .time-row:nth-child(6) p": tr(
        "2027년 TSMC Arizona에서 새로운 장을 시작할 예정입니다.",
        "将于 2027 年在 TSMC Arizona 开启新篇章。",
        "En 2027 comenzaré una nueva etapa en TSMC Arizona.",
        "預計於 2027 年在 TSMC Arizona 展開新篇章。",
        "En 2027, une nouvelle étape commencera chez TSMC Arizona.",
        "2027 beginnt für mich bei TSMC Arizona ein neuer Abschnitt."
      ),
      "#path .accordion-stack details:nth-child(2) .accordion-content p": tr(
        '업무나 협업 관련 연락은 <a href="https://www.linkedin.com/in/lim-chaehyun/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>으로 주세요. <a href="../career/">Career 페이지 ↗</a>에서 이메일로도 연락할 수 있습니다.',
        '如需职业交流或合作，欢迎通过 <a href="https://www.linkedin.com/in/lim-chaehyun/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a> 联系我，也可以从 <a href="../career/">职业经历页面 ↗</a> 发送电子邮件。',
        'Para contactos profesionales o colaboraciones, puedes encontrarme en <a href="https://www.linkedin.com/in/lim-chaehyun/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>. También puedes escribirme por correo desde la <a href="../career/">página de trayectoria ↗</a>.',
        '如需職涯交流或合作，歡迎透過 <a href="https://www.linkedin.com/in/lim-chaehyun/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a> 聯絡我，也可以到 <a href="../career/">職涯頁面 ↗</a> 透過電子郵件聯繫。',
        'Pour échanger sur un projet ou une collaboration, retrouvez-moi sur <a href="https://www.linkedin.com/in/lim-chaehyun/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>. Vous pouvez également m’écrire depuis la <a href="../career/">page Parcours ↗</a>.',
        'Für berufliche Anfragen und Kooperationen erreichen Sie mich auf <a href="https://www.linkedin.com/in/lim-chaehyun/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a> oder per E-Mail über die <a href="../career/">Karriereseite ↗</a>.'
      ),
      ".site-footer > span:nth-child(2)": tr(
        "ABOUT / 개인 아카이브", "ABOUT / 个人档案", "ABOUT / ARCHIVO PERSONAL",
        "ABOUT / 個人檔案", "ABOUT / ARCHIVES PERSONNELLES", "ABOUT / PERSÖNLICHES ARCHIV"
      )
    }
  };
})();