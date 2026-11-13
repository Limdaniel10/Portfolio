"use strict";
/* Career: professional, independently authored seven-language translations.
   Proper nouns, test values, model numbers and credentials retain original meaning.
   English is supplied by the existing HTML. */
(() => {
  const tr = (ko, zh, es, tw, fr, de) => [null, ko, zh, es, tw, fr, de];
  window.PortfolioDetailedTranslations = {
    career: {
      ".hero-main .eyebrow": tr(
        "개인 아카이브 &nbsp; / &nbsp; 엔지니어",
        "个人档案 &nbsp; / &nbsp; 工程师",
        "ARCHIVO PERSONAL &nbsp; / &nbsp; INGENIERÍA",
        "個人檔案 &nbsp; / &nbsp; 工程師",
        "ARCHIVES PERSONNELLES &nbsp; / &nbsp; INGÉNIERIE",
        "PERSÖNLICHES ARCHIV &nbsp; / &nbsp; INGENIEURWESEN"
      ),
      ".hero-main h1": tr(
        "경력<span>.</span>", "职业经历<span>.</span>", "Trayectoria<span>.</span>",
        "職涯<span>.</span>", "Parcours<span>.</span>", "Werdegang<span>.</span>"
      ),
      ".hero-main .links a:nth-child(1)": tr(
        "이력서 PDF 보기 ↗", "查看简历 PDF ↗", "Ver CV en PDF ↗",
        "查看履歷 PDF ↗", "Voir mon CV (PDF) ↗", "Lebenslauf (PDF) ↗"
      ),
      ".hero-main .links a:nth-child(3)": tr(
        "이메일 ↗", "电子邮件 ↗", "Correo ↗",
        "電子郵件 ↗", "E-mail ↗", "E-Mail ↗"
      ),
      ".career-art .art-grid span:nth-child(1)": tr(
        "01 / 시스템", "01 / 系统", "01 / SISTEMAS",
        "01 / 系統", "01 / SYSTÈMES", "01 / SYSTEME"
      ),
      ".career-art .art-grid span:nth-child(2)": tr(
        "02 / 시험", "02 / 测试", "02 / ENSAYOS",
        "02 / 測試", "02 / ESSAIS", "02 / TESTS"
      ),
      ".career-art .art-grid span:nth-child(3)": tr(
        "03 / 통합", "03 / 集成", "03 / INTEGRACIÓN",
        "03 / 整合", "03 / INTÉGRATION", "03 / INTEGRATION"
      ),
      ".career-art .art-grid span:nth-child(4)": tr(
        "04 / 에너지", "04 / 能源", "04 / ENERGÍA",
        "04 / 能源", "04 / ÉNERGIE", "04 / ENERGIE"
      ),
      ".career-art > p": tr(
        "항공우주에서 반도체까지.<br><em>호기심을 엔지니어링하다.</em>",
        "从航空航天到半导体。<br><em>以工程实现好奇心。</em>",
        "De la ingeniería aeroespacial a los semiconductores.<br><em>La curiosidad hecha ingeniería.</em>",
        "從航太到半導體。<br><em>用工程實現好奇心。</em>",
        "De l’aérospatial aux semi-conducteurs.<br><em>La curiosité au service de l’ingénierie.</em>",
        "Von der Luft- und Raumfahrt zur Halbleitertechnik.<br><em>Aus Neugier wird Technik.</em>"
      ),
      ".career-art .art-index": tr(
        "엔지니어링의 기록 &nbsp; / &nbsp; 2027",
        "工程实践记录 &nbsp; / &nbsp; 2027",
        "TRAYECTORIA EN INGENIERÍA &nbsp; / &nbsp; 2027",
        "工程實踐紀錄 &nbsp; / &nbsp; 2027",
        "PARCOURS EN INGÉNIERIE &nbsp; / &nbsp; 2027",
        "INGENIEURPRAXIS &nbsp; / &nbsp; 2027"
      ),
      "#affiliations .kicker": tr(
        "소속 및 학력", "工作单位与教育背景", "Instituciones y formación",
        "任職單位與學歷", "Organisations et formation", "Stationen und Ausbildung"
      ),
      '#affiliations .logo-card:nth-child(1) small': tr(
        "리소그래피 모듈 공정 엔지니어 · 2027년 6월",
        "光刻模块工艺工程师 · 2027 年 6 月",
        "Ingeniero de procesos (litografía) · Jun. 2027",
        "微影模組製程工程師 · 2027 年 6 月",
        "Ingénieur procédés (photolithographie) · Juin 2027",
        "Prozessingenieur (Lithografie) · Juni 2027"
      ),
      '#affiliations .logo-card:nth-child(2) small': tr(
        "학사 2026 · 석사 졸업 예정 2027",
        "学士 2026 · 预计硕士 2027",
        "Grado 2026 · Máster previsto en 2027",
        "學士 2026 · 預計碩士 2027",
        "Licence 2026 · Master prévu en 2027",
        "Bachelor 2026 · Master voraussichtlich 2027"
      ),
      '#affiliations .logo-card:nth-child(3) small': tr(
        "고등학교 · 2017–2020", "高中 · 2017–2020",
        "Bachillerato · 2017–2020", "高中 · 2017–2020",
        "Lycée · 2017–2020", "Gymnasium · 2017–2020"
      ),
      "#work .section-head > span": tr(
        "01 — 05 / 눌러서 자세히 보기", "01 — 05 / 点击展开详情",
        "01 — 05 / ABRIR PARA VER MÁS", "01 — 05 / 點擊展開詳情",
        "01 — 05 / OUVRIR POUR EN SAVOIR PLUS", "01 — 05 / ZUM AUFKLAPPEN KLICKEN"
      ),
      "#work .project:nth-of-type(1) h3": tr(
        "자동화 로봇 충격시험", "机器人冲击试验自动化",
        "Ensayos de impacto robóticos automatizados", "機器人衝擊測試自動化",
        "Essais d’impact robotisés automatisés", "Automatisierte robotergestützte Stoßprüfung"
      ),
      "#work .project:nth-of-type(1) .detail p:nth-of-type(1)": tr(
        "MATLAB 인터페이스를 개발해 Arduino로 제어하는 작동 장치와 힘·가속도 계측을 통합했습니다. 데이터 시각화, 보정, 기록 기능을 포함한 충격시험을 자동화했습니다.",
        "开发 MATLAB 操作界面，将 Arduino 控制的执行机构与力、加速度数据采集系统集成，实现冲击试验的自动化，并提供数据可视化、校准和记录功能。",
        "Desarrollé una interfaz en MATLAB para automatizar ensayos de impacto, integrando actuadores controlados por Arduino con la adquisición de fuerzas y aceleraciones, la visualización de datos, la calibración y el registro de resultados.",
        "開發 MATLAB 操作介面，整合 Arduino 控制的致動機構以及力量、加速度量測，將衝擊測試自動化，並提供資料視覺化、校正與記錄功能。",
        "J’ai développé une interface MATLAB pour automatiser des essais d’impact, en intégrant des actionneurs pilotés par Arduino, l’acquisition des forces et accélérations, la visualisation, l’étalonnage et l’enregistrement des données.",
        "Ich entwickelte eine MATLAB-Oberfläche zur Automatisierung von Stoßversuchen. Sie verbindet Arduino-gesteuerte Aktorik mit Kraft- und Beschleunigungsmessung sowie Visualisierung, Kalibrierung und Protokollierung."
      ),
      "#work .project:nth-of-type(1) .detail p:nth-of-type(2)": tr(
        "카메라 기반 패턴 인식과 목표 좌표 계산을 통합하고, 드라이버 호환성과 MATLAB 상태 관리 문제를 해결했습니다. 보고된 시험 범위는 결합 모드에서 약 250~1,500 N, 분리 모드에서 약 3,000 N입니다.",
        "集成基于摄像头的图案识别与目标坐标计算，并排查驱动兼容性及 MATLAB 状态管理问题。报告的测试力范围在耦合模式下约为 250–1,500 N，在释放模式下约为 3,000 N。",
        "Integré reconocimiento de patrones por cámara y cálculos de coordenadas objetivo, y resolví problemas de compatibilidad de controladores y gestión de estados en MATLAB. Los rangos de fuerza documentados fueron de unos 250–1.500 N en modo acoplado y 3.000 N en modo liberado.",
        "整合攝影機影像辨識與目標座標計算，並排除驅動程式相容性及 MATLAB 狀態管理問題。記錄的測試力範圍在耦合模式約為 250–1,500 N，在釋放模式約為 3,000 N。",
        "J’ai intégré une reconnaissance de motifs par caméra et le calcul des coordonnées cibles, tout en résolvant des problèmes de compatibilité de pilotes et de gestion d’état dans MATLAB. Les plages d’effort rapportées étaient d’environ 250 à 1 500 N en mode couplé et 3 000 N en mode libéré.",
        "Ich integrierte kamerabasierte Mustererkennung und Zielkoordinatenberechnung und behob Treiber- und MATLAB-Zustandsprobleme. Die dokumentierten Prüfkraftbereiche lagen bei etwa 250–1.500 N im gekoppelten und rund 3.000 N im ausgelösten Modus."
      ),
      "#work .project:nth-of-type(1) .tools": tr(
        "중점 — 계측 · 시스템 통합 · 자동화 · 디버깅",
        "重点 — 仪器测量 · 系统集成 · 自动化 · 故障排查",
        "Áreas — Instrumentación · Integración · Automatización · Depuración",
        "重點 — 儀器量測 · 系統整合 · 自動化 · 除錯",
        "Domaines — Instrumentation · Intégration · Automatisation · Débogage",
        "Schwerpunkte — Messtechnik · Integration · Automatisierung · Fehlersuche"
      ),
      "#work .project:nth-of-type(2) h3": tr(
        "하이브리드 전기 틸트로터 설계", "混合动力倾转旋翼机设计",
        "Diseño de aeronave de rotores basculantes híbrida-eléctrica", "混合動力傾轉旋翼機設計",
        "Conception d’un aéronef à rotors basculants hybride-électrique", "Entwurf eines hybrid-elektrischen Kipprotorflugzeugs"
      ),
      "#work .project:nth-of-type(2) .meta": tr(
        "제43회 VFS 학생 설계 대회 · 추진계통 팀장",
        "第 43 届 VFS 学生设计竞赛 · 推进系统负责人",
        "43.º Concurso Estudiantil de Diseño VFS · Responsable de propulsión",
        "第 43 屆 VFS 學生設計競賽 · 推進系統負責人",
        "43e concours étudiant de conception VFS · Responsable propulsion",
        "43. VFS-Studierendenwettbewerb · Leitung Antriebssysteme"
      ),
      "#work .project:nth-of-type(2) .detail p:nth-of-type(1)": tr(
        "호버링·전환비행·순항 전 구간을 대상으로 하이브리드 전기 동력 아키텍처와 MATLAB 기반 임무 에너지 모델을 개발했습니다. 터보제너레이터와 배터리의 출력 분담을 평가하고 공력·구조 팀과 추진계통 인터페이스를 조율했습니다.",
        "构建混合动力电力架构及 MATLAB 任务能耗模型，覆盖悬停、过渡飞行和巡航阶段。评估涡轮发电机与电池之间的功率分配，并与气动、结构团队协调推进系统接口。",
        "Desarrollé la arquitectura de potencia híbrida-eléctrica y modelos de energía de misión en MATLAB para vuelo estacionario, transición y crucero. Evalué el reparto de potencia entre turbogenerador y batería y coordiné interfaces con los equipos de aerodinámica y estructuras.",
        "建立混合動力電力架構與 MATLAB 任務能量模型，涵蓋懸停、轉換飛行及巡航。評估渦輪發電機與電池之間的功率分配，並與氣動及結構團隊協調推進系統介面。",
        "J’ai développé une architecture énergétique hybride-électrique et des modèles MATLAB de consommation en mission couvrant le vol stationnaire, la transition et la croisière. J’ai évalué la répartition de puissance entre turbogénérateur et batterie et coordonné les interfaces avec les équipes aérodynamique et structures.",
        "Ich entwickelte eine hybrid-elektrische Leistungsarchitektur und MATLAB-Modelle für den Energiebedarf in Schwebeflug, Übergang und Reiseflug. Dabei bewertete ich die Leistungsverteilung zwischen Turbogenerator und Batterie und stimmte die Antriebsschnittstellen mit Aerodynamik und Struktur ab."
      ),
      "#work .project:nth-of-type(2) .detail p:nth-of-type(2)": tr(
        "조지아텍 팀은 이 국제대회 학부생 부문에서 2위를 차지했습니다.",
        "佐治亚理工学院团队获得该国际竞赛本科组第二名。",
        "El equipo de Georgia Tech obtuvo el segundo puesto en la categoría de grado de esta competición internacional.",
        "喬治亞理工學院團隊在此國際競賽的大學部組別獲得第二名。",
        "L’équipe de Georgia Tech a obtenu la deuxième place dans la catégorie des étudiants de premier cycle de ce concours international.",
        "Das Team der Georgia Tech belegte in der Bachelor-Kategorie des internationalen Wettbewerbs den zweiten Platz."
      ),
      "#work .project:nth-of-type(2) .tools": tr(
        "중점 — 추진 · 전력 아키텍처 · 다학제 설계",
        "重点 — 推进系统 · 功率架构 · 跨学科设计",
        "Áreas — Propulsión · Arquitectura de potencia · Diseño multidisciplinar",
        "重點 — 推進系統 · 電力架構 · 跨領域設計",
        "Domaines — Propulsion · Architecture de puissance · Conception pluridisciplinaire",
        "Schwerpunkte — Antrieb · Leistungsarchitektur · Interdisziplinärer Entwurf"
      ),
      "#work .project:nth-of-type(3) h3": tr(
        "반작용 휠을 이용한 방향각 제어", "反作用轮航向控制",
        "Control de rumbo mediante rueda de reacción", "反作用輪航向控制",
        "Commande du cap par roue de réaction", "Kursregelung mit Reaktionsrad"
      ),
      "#work .project:nth-of-type(3) .meta": tr(
        "조지아텍 · 제어 및 하드웨어 검증", "佐治亚理工 · 控制与硬件验证",
        "Georgia Tech · Control y validación de hardware", "喬治亞理工 · 控制與硬體驗證",
        "Georgia Tech · Commande et validation matérielle", "Georgia Tech · Regelung und Hardwarevalidierung"
      ),
      "#work .project:nth-of-type(3) .detail p:nth-of-type(1)": tr(
        "단일 축 PI-II 반작용 휠 제어 시제품을 설계하고 검증했습니다. Arduino, IMU, ESC 및 BLDC 하드웨어를 통합했습니다.",
        "设计并验证单轴 PI-II 反作用轮控制原型，集成 Arduino、IMU、ESC 与 BLDC 硬件。",
        "Diseñé y validé un prototipo de control de rumbo de un eje con rueda de reacción y controlador PI-II. Integré Arduino, IMU, ESC y hardware BLDC.",
        "設計並驗證單軸 PI-II 反作用輪控制原型，整合 Arduino、IMU、ESC 與 BLDC 硬體。",
        "J’ai conçu et validé un prototype de commande PI-II monoaxe par roue de réaction, en intégrant Arduino, IMU, ESC et moteur BLDC.",
        "Ich entwarf und validierte einen einachsigen PI-II-Regelungsprototyp mit Reaktionsrad und integrierte Arduino, IMU, ESC und BLDC-Hardware."
      ),
      "#work .project:nth-of-type(3) .detail p:nth-of-type(2)": tr(
        "팀 시험 결과 상승시간 2.7초, 정착시간 5.9초, 오버슈트 8.24% 미만, 방향각 오차 ±2.8°를 기록했습니다. 이 프로젝트는 수업에서 1위를 차지했습니다.",
        "团队测试结果：上升时间 2.7 秒，稳定时间 5.9 秒，超调量低于 8.24%，航向误差为 ±2.8°。项目在课程中排名第一。",
        "Los ensayos del equipo registraron un tiempo de subida de 2,7 s, estabilización de 5,9 s, sobreimpulso inferior al 8,24 % y un error de rumbo de ±2,8°. El proyecto quedó en primer lugar de la clase.",
        "團隊測試結果：上升時間 2.7 秒、安定時間 5.9 秒、超越量低於 8.24%，航向誤差為 ±2.8°。本專案在課程中獲得第一名。",
        "Les essais de l’équipe ont montré un temps de montée de 2,7 s, un temps de stabilisation de 5,9 s, un dépassement inférieur à 8,24 % et une erreur de cap de ±2,8°. Le projet s’est classé premier du cours.",
        "Die Teamtests ergaben 2,7 s Anstiegszeit, 5,9 s Einschwingzeit, weniger als 8,24 % Überschwingen und ±2,8° Kursabweichung. Das Projekt belegte im Kurs den ersten Platz."
      ),
      "#work .project:nth-of-type(3) .tools": tr(
        "중점 — 제어 · 회로 통합 · 실험 검증",
        "重点 — 控制系统 · 电路集成 · 实验验证",
        "Áreas — Control · Integración de circuitos · Validación experimental",
        "重點 — 控制系統 · 電路整合 · 實驗驗證",
        "Domaines — Commande · Intégration de circuits · Validation expérimentale",
        "Schwerpunkte — Regelung · Schaltungsintegration · Experimentelle Validierung"
      ),
      "#work .project:nth-of-type(4) h3": tr(
        "리튬폴리머 배터리 시험", "锂聚合物电池测试",
        "Ensayos de baterías de polímero de litio", "鋰聚合物電池測試",
        "Essais de batteries lithium-polymère", "Prüfung von Lithium-Polymer-Akkus"
      ),
      "#work .project:nth-of-type(4) .meta": tr(
        "Vertical Lift Research Center of Excellence · 배터리 시험 담당",
        "Vertical Lift Research Center of Excellence · 电池测试员",
        "Vertical Lift Research Center of Excellence · Técnico de ensayos de baterías",
        "Vertical Lift Research Center of Excellence · 電池測試員",
        "Vertical Lift Research Center of Excellence · Opérateur d’essais de batteries",
        "Vertical Lift Research Center of Excellence · Batterietests"
      ),
      "#work .project:nth-of-type(4) .detail p:nth-of-type(1)": tr(
        "공개된 시험 절차에 따라 6S 리튬폴리머 팩의 사이클 수명 시험을 수행했습니다. 최대 1C 충전과 750 W 정전력 방전을 적용하고, 시험 기록을 관리하며 용량과 내부저항 측정값을 검토했습니다.",
        "按照公开测试规程执行 6S 锂聚合物电池组循环寿命试验，充电倍率最高 1C，并以 750 W 恒功率放电。维护测试记录并审查容量及内阻测量结果。",
        "Realicé ensayos de vida útil por ciclos de paquetes de baterías LiPo 6S siguiendo un protocolo publicado: carga de hasta 1C y descarga a potencia constante de 750 W. Mantuve los registros y revisé mediciones de capacidad y resistencia interna.",
        "依公開測試程序執行 6S 鋰聚合物電池組的循環壽命測試，最高以 1C 充電，並採 750 W 定功率放電。維護測試紀錄並檢視容量與內阻量測值。",
        "J’ai réalisé des essais de durée de vie en cyclage sur des batteries LiPo 6S selon un protocole publié, avec charge jusqu’à 1C et décharge à puissance constante de 750 W. J’ai tenu les registres et analysé les mesures de capacité et de résistance interne.",
        "Ich führte Zykluslebensdauertests an 6S-LiPo-Akkupacks nach einem veröffentlichten Protokoll durch: Laden mit bis zu 1C und Entladen bei konstant 750 W. Ich dokumentierte die Versuche und prüfte Kapazitäts- und Innenwiderstandswerte."
      ),
      "#work .project:nth-of-type(4) .tools": tr(
        "중점 — 배터리 충·방전 사이클 · 계측 · 데이터 검토",
        "重点 — 电池循环测试 · 测量 · 数据核查",
        "Áreas — Ciclos de batería · Medición · Revisión de datos",
        "重點 — 電池循環測試 · 量測 · 資料檢視",
        "Domaines — Cyclage des batteries · Mesures · Analyse des données",
        "Schwerpunkte — Batterietests · Messtechnik · Datenauswertung"
      ),
      "#work .project:nth-of-type(4) .media-caption": tr(
        "시험: 리튬폴리머 배터리 충·방전 사이클 및 측정, Excel 기반 데이터 검토.",
        "测试：锂聚合物电池循环与测量；使用 Excel 检查数据。",
        "Ensayos: ciclos y medición de baterías LiPo; revisión de datos en Excel.",
        "測試：鋰聚合物電池循環與量測；使用 Excel 檢視資料。",
        "Essais : cyclage et mesures sur batteries LiPo ; examen des données dans Excel.",
        "Prüfung: LiPo-Akkuzyklen und Messungen; Datenauswertung mit Excel."
      ),
      "#work .project:nth-of-type(5) h3": tr(
        "무인항공시스템", "无人航空系统", "Sistemas aéreos no tripulados",
        "無人航空系統", "Systèmes aériens sans pilote", "Unbemannte Luftfahrtsysteme"
      ),
      "#work .project:nth-of-type(5) .meta": tr(
        "개인 UAV 프로젝트 · 시스템 설계 및 비행 운용",
        "个人无人机项目 · 系统设计与飞行运行",
        "Proyectos independientes de UAV · Diseño de sistemas y operaciones de vuelo",
        "個人 UAV 專案 · 系統設計與飛行操作",
        "Projets UAV indépendants · Conception de systèmes et opérations de vol",
        "Eigene UAV-Projekte · Systementwurf und Flugbetrieb"
      ),
      "#work .project:nth-of-type(5) .detail p:nth-of-type(1)": tr(
        "무인기 구조물, 3D 프린팅 배터리 하우징, 열·광학 센서 탑재체를 통합했습니다. 사전 설정된 웨이포인트 비행으로 안정성과 탑재체 기능을 평가했습니다.",
        "集成无人机机体结构、3D 打印电池舱以及热成像和光学传感器载荷，通过预设航点飞行评估稳定性与载荷功能。",
        "Integré estructuras de UAV, una carcasa de batería impresa en 3D y cargas útiles con sensores térmicos y ópticos. Realicé vuelos por puntos de ruta preprogramados para evaluar la estabilidad y las funciones de la carga útil.",
        "整合無人機機體結構、3D 列印電池外殼，以及熱影像與光學感測器酬載，並透過預設航點飛行評估穩定性與酬載功能。",
        "J’ai intégré des structures de drone, un boîtier de batterie imprimé en 3D et des charges utiles avec capteurs thermiques et optiques. Des vols sur points de passage préprogrammés ont permis d’évaluer la stabilité et le fonctionnement des charges utiles.",
        "Ich integrierte UAV-Strukturen, ein 3D-gedrucktes Batteriegehäuse sowie thermische und optische Sensor-Nutzlasten. Vorprogrammierte Wegpunktflüge dienten zur Bewertung der Stabilität und Nutzlastfunktion."
      ),
      "#work .project:nth-of-type(5) .tools": tr(
        "중점 — 무인기 시스템 통합 · 센서 · 비행시험",
        "重点 — 无人机集成 · 传感器 · 飞行测试",
        "Áreas — Integración UAV · Sensores · Ensayos de vuelo",
        "重點 — 無人機整合 · 感測器 · 飛行測試",
        "Domaines — Intégration UAV · Capteurs · Essais en vol",
        "Schwerpunkte — UAV-Integration · Sensorik · Flugtests"
      ),
      "#experience .section-head > span": tr(
        "엔지니어링 및 리더십", "工程与领导经验", "INGENIERÍA Y LIDERAZGO",
        "工程與領導經驗", "INGÉNIERIE ET RESPONSABILITÉS", "INGENIEURWESEN UND FÜHRUNG"
      ),
      "#experience .timeline-item:nth-of-type(2) .date": tr(
        "2027년 6월 입사 예정", "预计 2027 年 6 月入职", "Incorporación en junio de 2027",
        "預計 2027 年 6 月到職", "Prise de poste en juin 2027", "Berufseinstieg im Juni 2027"
      ),
      "#experience .timeline-item:nth-of-type(2) p": tr(
        "모듈 공정 엔지니어 — 리소그래피 · 미국 애리조나주 피닉스",
        "模块工艺工程师 — 光刻 · 美国亚利桑那州菲尼克斯",
        "Ingeniero de procesos — Litografía · Phoenix, Arizona",
        "模組製程工程師 — 微影 · 美國亞利桑那州鳳凰城",
        "Ingénieur procédés — Photolithographie · Phoenix, Arizona",
        "Prozessingenieur — Lithografie · Phoenix, Arizona"
      ),
      "#experience .timeline-item:nth-of-type(3) p": tr(
        "학부 연구원 · 조지아텍 · 로봇 충격시험 및 계측",
        "本科研究助理 · 佐治亚理工 · 机器人冲击试验与测量",
        "Investigador de grado · Georgia Tech · Ensayos de impacto e instrumentación",
        "大學部研究助理 · 喬治亞理工 · 機器人衝擊測試與量測",
        "Assistant de recherche (licence) · Georgia Tech · Essais d’impact et instrumentation",
        "Studentische Forschungskraft · Georgia Tech · Stoßprüfung und Messtechnik"
      ),
      "#experience .timeline-item:nth-of-type(4) p": tr(
        "추진계통 팀장 · 하이브리드 전기 틸트로터 개념설계",
        "推进系统负责人 · 混合动力倾转旋翼机概念设计",
        "Responsable de propulsión · Diseño conceptual de aeronave híbrida de rotores basculantes",
        "推進系統負責人 · 混合動力傾轉旋翼機概念設計",
        "Responsable propulsion · Conception préliminaire de tiltrotor hybride-électrique",
        "Leitung Antriebssysteme · Konzeptentwurf eines hybrid-elektrischen Kipprotorflugzeugs"
      ),
      "#experience .timeline-item:nth-of-type(5) p": tr(
        "배터리 시험 담당 · 리튬폴리머 배터리 시험",
        "电池测试员 · 锂聚合物电池试验",
        "Técnico de ensayos · Baterías de polímero de litio",
        "電池測試員 · 鋰聚合物電池測試",
        "Opérateur d’essais · Batteries lithium-polymère",
        "Batterietests · Lithium-Polymer-Akkus"
      ),
      "#experience .timeline-item:nth-of-type(6) p": tr(
        "분대장 및 정보 편집병 · 11명 분대 지휘, 국방·항공우주 정보 보고 조율",
        "班长兼情报编辑 · 带领 11 人班组，协调国防与航空航天情报报告",
        "Jefe de escuadra y editor de inteligencia · Dirigí a un equipo de 11 personas y coordiné informes de defensa y aeronáutica",
        "班長兼情報編輯 · 帶領 11 人班組，協調國防與航太情報報告",
        "Chef de groupe et rédacteur en renseignement · Encadrement de 11 personnes et coordination de rapports sur la défense et l’aérospatial",
        "Gruppenführer und Nachrichtenredakteur · Führung einer elfköpfigen Gruppe und Koordination von Berichten zu Verteidigung und Luft- und Raumfahrt"
      ),
      "#education .section-head > span": tr(
        "학력", "教育背景", "FORMACIÓN ACADÉMICA",
        "學歷", "FORMATION", "AUSBILDUNG"
      ),
      "#education .timeline-item:nth-of-type(2) .date": tr(
        "2027년 5월 졸업 예정", "预计 2027 年 5 月毕业",
        "Graduación prevista en mayo de 2027", "預計 2027 年 5 月畢業",
        "Diplôme prévu en mai 2027", "Abschluss voraussichtlich Mai 2027"
      ),
      "#education .timeline-item:nth-of-type(2) p": tr(
        "항공우주공학 석사 · 비논문 과정",
        "航空航天工程硕士 · 非论文项目",
        "Máster en Ingeniería Aeroespacial · Modalidad sin tesis",
        "航太工程碩士 · 非論文組",
        "Master en ingénierie aérospatiale · Parcours sans mémoire",
        "Master Luft- und Raumfahrttechnik · Ohne Abschlussarbeit"
      ),
      "#education .timeline-item:nth-of-type(3) .date": tr(
        "2026년 5월", "2026 年 5 月", "Mayo de 2026",
        "2026 年 5 月", "Mai 2026", "Mai 2026"
      ),
      "#education .timeline-item:nth-of-type(3) p": tr(
        "항공우주공학 학사 · GPA 3.65 / 4.00 · 최우등 졸업",
        "航空航天工程学士 · GPA 3.65 / 4.00 · 最高荣誉毕业",
        "Grado en Ingeniería Aeroespacial · GPA 3,65 / 4,00 · Máximos honores",
        "航太工程學士 · GPA 3.65 / 4.00 · 最高榮譽畢業",
        "Bachelor of Science en ingénierie aérospatiale · GPA 3,65 / 4,00 · Plus haute distinction",
        "Bachelor Luft- und Raumfahrttechnik · GPA 3,65 / 4,00 · Mit höchster Auszeichnung"
      ),
      "#education .timeline-item:nth-of-type(4) p": tr(
        "HAFS · 대한민국", "HAFS · 韩国", "HAFS · Corea del Sur",
        "HAFS · 韓國", "HAFS · Corée du Sud", "HAFS · Südkorea"
      ),
      "#skills .section-head > span": tr(
        "주요 역량", "主要技能", "SELECCIÓN",
        "主要技能", "SÉLECTION", "AUSWAHL"
      ),
      "#skills .skills:nth-of-type(2) > div:nth-child(1)": tr(
        "시험 및 제작", "测试与制造", "Ensayos y fabricación",
        "測試與製作", "Essais et fabrication", "Prüfung und Fertigung"
      ),
      "#skills .skills:nth-of-type(2) > div:nth-child(2)": tr(
        "시험 자동화 · NI cDAQ · LabJack T7-PRO · 3D 프린팅",
        "测试自动化 · NI cDAQ · LabJack T7-PRO · 3D 打印",
        "Automatización de ensayos · NI cDAQ · LabJack T7-PRO · Impresión 3D",
        "測試自動化 · NI cDAQ · LabJack T7-PRO · 3D 列印",
        "Automatisation des essais · NI cDAQ · LabJack T7-PRO · Impression 3D",
        "Testautomatisierung · NI cDAQ · LabJack T7-PRO · 3D-Druck"
      ),
      "#skills .skills:nth-of-type(3) > div:nth-child(1)": tr(
        "데이터 및 통계", "数据与统计", "Datos y estadística",
        "資料與統計", "Données et statistiques", "Daten und Statistik"
      ),
      "#skills .skills:nth-of-type(3) > div:nth-child(2)": tr(
        "실험계획법(DOE) · R · Excel · 통계 분석",
        "试验设计(DOE) · R · Excel · 统计分析",
        "Diseño de Experimentos (DOE) · R · Excel · Análisis estadístico",
        "實驗設計(DOE) · R · Excel · 統計分析",
        "Plans d’expériences (DOE) · R · Excel · Analyse statistique",
        "Versuchsplanung (DOE) · R · Excel · Statistische Analyse"
      ),
      "#skills .skills:nth-of-type(4) > div:nth-child(1)": tr(
        "공학 및 소프트웨어", "工程与软件", "Ingeniería y software",
        "工程與軟體", "Ingénierie et logiciels", "Ingenieurwesen und Software"
      ),
      "#skills .skills:nth-of-type(5) > div:nth-child(1)": tr(
        "자격증", "资格认证", "Certificaciones",
        "專業證照", "Certifications", "Zertifikate"
      ),
      "#skills .skills:nth-of-type(5) > div:nth-child(2)": tr(
        "FAA Part 107 · EASA A1/A3 · 대한민국 무인항공기 조종자 자격",
        "FAA Part 107 · EASA A1/A3 · 韩国无人机驾驶资格",
        "FAA Part 107 · EASA A1/A3 · Habilitación de piloto UAV de Corea del Sur",
        "FAA Part 107 · EASA A1/A3 · 韓國無人機操作資格",
        "FAA Part 107 · EASA A1/A3 · Qualification coréenne de pilote de drone",
        "FAA Part 107 · EASA A1/A3 · Südkoreanische UAV-Pilotenqualifikation"
      ),
      "#skills .skills:nth-of-type(6) > div:nth-child(1)": tr(
        "언어", "语言", "Idiomas",
        "語言", "Langues", "Sprachen"
      ),
      "#skills .skills:nth-of-type(6) > div:nth-child(2)": tr(
        "한국어 · 영어 · 중국어(HSK 5급)", "韩语 · 英语 · 汉语（HSK 5 级）",
        "Coreano · Inglés · Chino mandarín (HSK 5)", "韓文 · 英文 · 中文（HSK 5 級）",
        "Coréen · Anglais · Mandarin (HSK 5)", "Koreanisch · Englisch · Mandarin (HSK 5)"
      ),
      "#connect .section-head > span": tr(
        "연락처", "联系方式", "CONTACTO",
        "聯絡方式", "CONTACT", "KONTAKT"
      ),
      "#connect > p": tr(
        "업무 관련 문의, 프로젝트 논의 또는 협업 제안은 아래로 연락해 주세요.",
        "欢迎联系我，交流职业机会、项目或合作事宜。",
        "Para consultas profesionales, proyectos o propuestas de colaboración, ponte en contacto conmigo.",
        "歡迎聯絡我，交流工作機會、專案或合作事宜。",
        "Pour toute question professionnelle, discussion de projet ou proposition de collaboration, n’hésitez pas à me contacter.",
        "Bei beruflichen Anfragen, Projektideen oder Kooperationsvorschlägen freue ich mich über eine Nachricht."
      ),
      "#connect .links a:nth-child(1)": tr(
        "이메일 ↗", "电子邮件 ↗", "Correo ↗",
        "電子郵件 ↗", "E-mail ↗", "E-Mail ↗"
      ),
      "#connect .links a:nth-child(3)": tr(
        "이력서 PDF 보기 ↗", "查看简历 PDF ↗", "Ver CV en PDF ↗",
        "查看履歷 PDF ↗", "Voir mon CV (PDF) ↗", "Lebenslauf (PDF) ↗"
      ),
      ".site-footer > span:nth-child(2)": tr(
        "CAREER / 엔지니어링", "CAREER / 工程", "TRAYECTORIA / INGENIERÍA",
        "CAREER / 工程", "PARCOURS / INGÉNIERIE", "WERDEGANG / INGENIEURWESEN"
      )
    }
  };
})();