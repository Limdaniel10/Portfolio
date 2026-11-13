"use strict";
/* Lightweight interface-only localization. Original articles, quotations, book titles,
   travel records and technical project details are never machine-translated. */
(() => {
  const codes = ["en", "ko", "zh-Hans", "es"];
  const names = ["English", "한국어", "中文", "Español"];
  const navLabels = {
    Home: ["Home", "홈", "首页", "Inicio"],
    Career: ["Career", "경력", "经历", "Trayectoria"],
    Travel: ["Travel", "여행", "旅行", "Viajes"],
    Writing: ["Writing", "글", "写作", "Escritos"],
    Reading: ["Reading", "독서", "阅读", "Lecturas"],
    About: ["About", "소개", "关于", "Sobre mí"]
  };
  const texts = {
    home: {
      ".hero .tagline": ["Curiosity at every scale.", "모든 규모에서 피어나는 호기심.", "跨越尺度的好奇心。", "Curiosidad a todas las escalas."],
      ".hero .intro": ["Engineering the details. Exploring the world. Writing the stories.", "작은 것을 설계하고, 넓은 세상을 탐험하고, 이야기를 기록합니다.", "钻研工程细节，探索广阔世界，记录沿途故事。", "Diseñar los detalles. Explorar el mundo. Escribir las historias."],
      ".panel-heading span:first-child": ["THE WORLD, EXPLORED", "발자취를 남긴 세계", "走过的世界", "EL MUNDO RECORRIDO"],
      ".map-note": ["Countries visited, highlighted on the map.", "방문한 국가를 지도에 표시했습니다.", "地图标出了我到访过的国家。", "El mapa destaca los países que he visitado."],
      ".map-link": ["Explore travels <span aria-hidden=\"true\">↗</span>", "여행 기록 보기 <span aria-hidden=\"true\">↗</span>", "探索旅程 <span aria-hidden=\"true\">↗</span>", "Explorar viajes <span aria-hidden=\"true\">↗</span>"],
      ".tile:nth-child(1) h2": ["Career", "경력", "经历", "Trayectoria"],
      ".tile:nth-child(2) h2": ["Writing", "글", "写作", "Escritos"],
      ".tile:nth-child(3) h2": ["Traveling", "여행", "旅行", "Viajes"],
      ".tile:nth-child(4) h2": ["Reading", "독서", "阅读", "Lecturas"],
      ".tile:nth-child(1) p": ["GT · Engineer", "조지아텍 · 엔지니어", "佐治亚理工 · 工程师", "Georgia Tech · Ingeniero"],
      ".tile:nth-child(2) p": ["5 Brunch essay collections", "브런치 연재 에세이집 5편", "5 部 Brunch 随笔集", "5 colecciones de ensayos en Brunch"],
      ".about-link": ["A little more about me <span>↗</span>", "나에 대해 더 알아보기 <span>↗</span>", "了解更多关于我的故事 <span>↗</span>", "Conoce un poco más sobre mí <span>↗</span>"]
    },
    about: {
      ".about-hero .lead": ["Different pursuits.<br>One curiosity.", "서로 다른 길.<br>하나의 호기심.", "不同的追寻。<br>同一份好奇。", "Distintos caminos.<br>Una misma curiosidad."],
      ".about-hero .prose": ["An aerospace engineer from Busan, South Korea, completing a master's degree at Georgia Tech. Drawn to the details of how things work and to the places, books, and stories beyond them.", "부산에서 태어나 조지아텍에서 항공우주공학 석사과정을 마무리하고 있습니다. 사물이 작동하는 원리부터 세계의 장소, 책, 이야기까지 호기심을 따라갑니다.", "我来自韩国釜山，正在佐治亚理工学院完成航空航天工程硕士学位。我热衷于探究事物的运作原理，也喜欢世界各地的风景、书籍与故事。", "Soy ingeniero aeroespacial de Busan, Corea del Sur, y estoy terminando una maestría en Georgia Tech. Me atrae tanto entender cómo funcionan las cosas como explorar lugares, libros e historias."],
      "#numbers .section-heading h2": ["Pieces of the picture.", "숫자로 보는 나의 기록.", "数字中的点滴。", "Retrato en cifras."],
      ".pursuit-grid a:nth-child(1) p": ["Building, testing, learning.", "만들고, 시험하고, 배웁니다.", "设计、测试、学习。", "Diseñar, probar, aprender."],
      ".pursuit-grid a:nth-child(2) p": ["Stories worth carrying.", "오래 간직할 이야기들.", "值得珍藏的故事。", "Historias que vale la pena guardar."],
      ".pursuit-grid a:nth-child(3) p": ["Somewhere along the way.", "여정의 어느 길목에서.", "旅途中的某个地方。", "En algún lugar del camino."],
      ".pursuit-grid a:nth-child(4) p": ["Pages that stay with me.", "마음에 오래 남은 책들.", "那些留在心里的书页。", "Páginas que permanecen conmigo."],
      ".about-section:nth-of-type(3) .section-heading h2": ["Now &amp; next.", "지금, 그리고 다음.", "当下与未来。", "Ahora y después."]
    },
    career: {
      ".hero-main .intro": ["From aerospace systems and experimental testing to semiconductor manufacturing.", "항공우주 시스템과 실험·시험에서 반도체 제조까지.", "从航天系统与实验测试，到半导体制造。", "De los sistemas aeroespaciales y las pruebas experimentales a la fabricación de semiconductores."],
      ".hero-main .sub": ["Aerospace engineer trained at Georgia Tech, with experience in robotic test automation, hybrid-electric propulsion, battery testing, and hardware integration.", "조지아텍에서 항공우주공학을 공부하며 로봇 시험 자동화, 하이브리드 전기 추진, 배터리 시험, 하드웨어 통합 프로젝트를 수행했습니다.", "我在佐治亚理工学院接受航空航天工程训练，参与过机器人测试自动化、混合动力推进、电池测试及硬件集成项目。", "Formado en ingeniería aeroespacial en Georgia Tech, con experiencia en automatización de pruebas, propulsión híbrida-eléctrica, ensayos de baterías e integración de hardware."],
      "#work .section-head h2": ["Selected Work", "대표 프로젝트", "代表项目", "Proyectos destacados"]
    },
    traveling: {
      ".hero .lead": ["A life measured in places,<br>and the journeys between them.", "장소와 그 사이의 여정으로<br>기록한 삶.", "以去过的地方和一路上的旅程，<br>丈量生活。", "Una vida medida en lugares<br>y en los caminos entre ellos."],
      ".hero .intro": ["Six continents. Familiar streets and unfamiliar horizons.<br>A personal atlas, still unfolding.", "여섯 대륙, 익숙한 거리와 낯선 지평선.<br>지금도 이어지는 나만의 지도.", "六大洲，熟悉的街道与陌生的天际。<br>一本仍在续写的个人地图集。", "Seis continentes. Calles conocidas y horizontes nuevos.<br>Un atlas personal que sigue creciendo."],
      "#atlas .sectionhead h2": ["An atlas in motion.", "이어지는 여정의 지도.", "不断延伸的旅途地图。", "Un atlas en movimiento."],
      "#atlas .sectionhead p": ["Unfold a year. Follow a month.", "연도를 펼치고 월별 여정을 살펴보세요.", "展开年份，探索每个月的旅程。", "Abre un año y explora cada mes."],
      "#places .sectionhead h2": ["Somewhere along the way.", "여행길 위의 장소들.", "旅途中的地方。", "Lugares del camino."],
      "#highlights .sectionhead h2": ["What stays with me.", "여행이 남긴 것.", "旅途留下的记忆。", "Lo que permanece."],
      "#allYears": ["All years ↗", "전체 연도 ↗", "所有年份 ↗", "Todos los años ↗"],
      "#cumulative": ["Cumulative", "누적", "累计", "Acumulado"],
      "#periodOnly": ["Period only", "선택 기간", "仅所选期间", "Solo este período"],
      "#resetMap": ["↗ World view", "↗ 세계지도", "↗ 世界地图", "↗ Vista mundial"]
    },
    reading: {
      ".reading-hero .lead": ["A lifetime in the margins,<br>one book at a time.", "책 한 권, 한 권의 여백에<br>쌓이는 삶의 기록.", "一本接一本，<br>在书页之间记录人生。", "Una vida entre márgenes,<br>libro a libro."],
      ".reading-hero .prose": ["A record of completed books, the pages that filled the months, and ideas worth returning to. Browse the years, explore a month, or simply follow the titles.", "완독한 책, 매월 읽은 페이지, 오래 간직하고 싶은 생각을 기록했습니다. 연도별·월별로 둘러보거나 책 제목을 따라가 보세요.", "记录读完的书、每个月读过的页数，以及值得回味的想法。可以按年份、月份或书名浏览。", "Un registro de libros terminados, páginas leídas cada mes e ideas para revisitar. Explora por año, mes o título."],
      "#reading-years .section-heading h2": ["Pages over time.", "시간 속에 쌓인 페이지.", "岁月中的书页。", "Páginas a lo largo del tiempo."],
      "#reading-years .section-heading .aside-note": ["Select a year, then a month.", "연도를 선택한 뒤 월을 선택하세요.", "先选年份，再选月份。", "Elige un año y luego un mes."],
      "#metricBooks": ["Books", "권수", "书籍", "Libros"],
      "#metricPages": ["Pages", "페이지", "页数", "Páginas"],
      ".month-section-title h3": ["A closer look.", "월별로 자세히.", "按月细看。", "Una mirada más cercana."],
      "#highlightsHeading": ["Lines worth keeping.", "오래 간직할 문장들.", "值得珍藏的句子。", "Frases para guardar."]
    },
    writing: {
      ".hero-lead": ["Stories from elsewhere, kept in one place.", "여행길의 이야기들을 한곳에 모았습니다.", "把旅途中的故事收藏在这里。", "Historias de otros lugares, reunidas aquí."],
      ".archive-language-note": ["Travel essays originally written in Korean and serialized on Brunch.", "한국어로 쓰고 브런치에 연재한 여행 에세이입니다.", "旅行随笔原文为韩语，最初连载于 Brunch。", "Ensayos de viaje escritos originalmente en coreano y publicados en Brunch."],
      ".portal-grid .portal-card:nth-child(1) h2": ["Collections", "연재 작품", "作品集", "Colecciones"],
      ".portal-grid .portal-card:nth-child(2) h2": ["Fiction", "소설", "小说", "Ficción"],
      ".portal-grid .portal-card:nth-child(3) h2": ["Essays", "에세이", "随笔", "Ensayos"],
      ".portal-grid .portal-card:nth-child(4) h2": ["Readings", "독서 기록", "读书笔记", "Lecturas"],
      ".portal-grid .portal-card:nth-child(1) p": ["Collected travel essays and ongoing series", "여행 에세이와 연재 중인 이야기", "旅行随笔与连载作品", "Ensayos de viaje y series en curso"],
      ".portal-grid .portal-card:nth-child(2) p": ["A world imagined in three volumes", "세 권으로 펼쳐질 이야기", "三卷构成的虚构世界", "Un mundo imaginado en tres volúmenes"],
      ".portal-grid .portal-card:nth-child(3) p": ["Standalone stories, scenes &amp; reflections", "독립된 이야기와 단상", "独立故事、片段与感想", "Relatos y reflexiones independientes"],
      ".portal-grid .portal-card:nth-child(4) p": ["A line or a paragraph, Book Reviews", "한 줄, 한 문단과 독서 감상", "一行一段与读书感想", "Una línea, un párrafo y reseñas de libros"]
    }
  };
  const generic = {
    "Back to top ↑": ["Back to top ↑", "맨 위로 ↑", "返回顶部 ↑", "Volver arriba ↑"],
    "Selected Work": ["Selected Work", "대표 프로젝트", "代表项目", "Proyectos destacados"],
    "Experience": ["Experience", "경력", "经历", "Experiencia"],
    "Education": ["Education", "학력", "教育背景", "Formación"],
    "Skills & Credentials": ["Skills & Credentials", "기술 및 자격", "技能与资质", "Habilidades y certificaciones"],
    "Connect": ["Connect", "연락하기", "联系", "Contacto"],
    "Many interests, one direction.": ["Many interests, one direction.", "서로 다른 관심사, 하나의 방향.", "兴趣多元，方向如一。", "Muchos intereses, una dirección."],
    "Somewhere in between.": ["Somewhere in between.", "그 사이의 여정.", "一路走来。", "En algún punto del camino."],
    "Now & next.": ["Now & next.", "지금, 그리고 다음.", "当下与未来。", "Ahora y después."],
    "Different pursuits.": ["Different pursuits.", "서로 다른 길.", "不同的追寻。", "Distintos caminos."],
    "Still writing.": ["Still writing.", "계속 쓰는 중.", "仍在书写。", "Sigo escribiendo."],
    "Writing home": ["Writing home", "글 메인", "写作主页", "Inicio de escritos"],
    "Explore the archive": ["Explore the archive", "기록 둘러보기", "浏览档案", "Explorar el archivo"],
    "Follow the journey": ["Follow the journey", "여행 따라가기", "跟随旅程", "Seguir el viaje"],
    "A little more about me": ["A little more about me", "더 알아보기", "了解更多", "Más sobre mí"]
  };
  let chosen = "en";
  try { const saved = localStorage.getItem("portfolio-language"); if (codes.includes(saved)) chosen = saved; } catch (_) {}
  const requested = new URLSearchParams(window.location.search).get("lang");
  if (codes.includes(requested)) chosen = requested;
  const page = location.pathname.includes("/career/") ? "career" :
    location.pathname.includes("/traveling/") ? "traveling" :
    location.pathname.includes("/reading/") ? "reading" :
    location.pathname.includes("/about/") ? "about" :
    location.pathname.includes("/writing/") ? "writing" : "home";
  const host = document.querySelector(".site-nav .shell, header.top, header.shell, .topbar-inner");
  if (!host) return;
  const picker = document.createElement("div");
  picker.className = "lang-switcher";
  const label = document.createElement("label");
  label.htmlFor = "portfolio-language";
  label.className = "lang-visually-hidden";
  label.textContent = "Interface language";
  const select = document.createElement("select");
  select.id = "portfolio-language";
  select.setAttribute("aria-label", "Interface language");
  codes.forEach((code, i) => {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = names[i];
    select.appendChild(option);
  });
  picker.append(label, select);
  host.appendChild(picker);
  const selectors = texts[page] || {};
  const originals = new Map();
  for (const css of Object.keys(selectors)) {
    const el = document.querySelector(css);
    if (el) originals.set(css, el.innerHTML);
  }
  const navLinks = Array.from(host.querySelectorAll("nav a"));
  const navOriginals = navLinks.map(el => el.textContent.trim());
  const genericElements = Array.from(document.querySelectorAll("h2, .site-footer a, .footer a, .footer strong, .section-head h2"));
  const genericOriginals = genericElements.map(el => el.textContent.trim());
  const notice = document.createElement("p");
  notice.className = "lang-original-notice";
  notice.setAttribute("role", "note");
  const noteText = [
    "",
    "안내: 메뉴와 주요 소개 문구만 번역됩니다. 작품 본문과 도서·여행 기록은 원어로 유지됩니다.",
    "提示：仅导航和主要简介提供翻译。文章正文、书籍及旅行记录保持原文。",
    "Nota: solo se traducen los menús y las introducciones principales. Los textos, libros y registros de viaje conservan su idioma original."
  ];
  const main = document.querySelector("main");
  if (main) main.prepend(notice);
  function apply(lang) {
    chosen = lang;
    const i = codes.indexOf(chosen);
    select.value = chosen;
    select.setAttribute("aria-label", ["Interface language", "화면 언어", "界面语言", "Idioma de la interfaz"][i]);
    document.documentElement.lang = chosen;
    document.documentElement.dataset.interfaceLanguage = chosen;
    navLinks.forEach((el, j) => {
      const label = navLabels[navOriginals[j]];
      if (label) el.textContent = label[i];
    });
    for (const [css, variants] of Object.entries(selectors)) {
      const el = document.querySelector(css);
      if (el) el.innerHTML = i === 0 ? originals.get(css) || variants[0] : variants[i];
    }
    genericElements.forEach((el, j) => {
      const variants = generic[genericOriginals[j]];
      if (variants && el.children.length === 0) el.textContent = variants[i];
    });
    notice.textContent = noteText[i];
    notice.hidden = i === 0;
    try { localStorage.setItem("portfolio-language", chosen); } catch (_) {}
    refreshCounts();
  }
  function refreshCounts() {
    const i = codes.indexOf(chosen);
    if (page !== "home") return;
    for (const id of ["country-count", "travel-tile-count"]) {
      const node = document.getElementById(id);
      if (!node) continue;
      const n = node.textContent.match(/[\d,]+/);
      if (!n) continue;
      node.textContent = [n[0] + " countries", n[0] + "개국", n[0] + " 个国家", n[0] + " países"][i];
    }
    const books = document.getElementById("reading-tile-count");
    if (books) {
      const n = books.textContent.match(/[\d,]+\+?/);
      if (n) books.textContent = [n[0] + " books", n[0] + "권", n[0] + " 本书", n[0] + " libros"][i];
    }
  }
  select.addEventListener("change", () => apply(select.value));
  window.PortfolioI18n = { refreshCounts, getLanguage: () => chosen };
  apply(chosen);
})();