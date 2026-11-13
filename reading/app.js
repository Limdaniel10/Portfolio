"use strict";
// Keep the established Reading Archive UI. Only data loading changed:
// book counts/list come from books.json; all page figures come from monthly-pages.json.
const $ = selector => document.querySelector(selector);
const fmt = n => Number(n).toLocaleString("en-US");
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const bookUnit = n => n === 1 ? "book" : "books";
const NOTION_BY_YEAR = Object.freeze({
  "2020": "https://app.notion.com/p/130f8fb4581b80a1b86aeb048ddd2278",
  "2021": "https://app.notion.com/p/130f8fb4581b8026879cfe2ab98e48b8",
  "2022": "https://app.notion.com/p/130f8fb4581b803fb6a0e040d5fceacc",
  "2023": "https://app.notion.com/p/130f8fb4581b80a8816eee87307607c4",
  "2024": "https://app.notion.com/p/130f8fb4581b809e85c4e345f95dbba6",
  "2025": "https://app.notion.com/p/17ef8fb4581b80a2a968eee1550764b7"
});
let years = [];
let bookLookup = new Map();
let activeYear, activeMonth, showAllBooks = false, chartMetric = "books";

function groupArchive(books, monthlyPages) {
  if (!Array.isArray(books) || !Array.isArray(monthlyPages)) {
    throw new Error("Invalid JSON schema: expected book and monthly-pages arrays.");
  }
  const pageMap = new Map();
  const yearSet = new Set();
  for (const record of monthlyPages) {
    const year = Number(record.year), month = Number(record.month), pages = Number(record.pages_read);
    if (!Number.isInteger(year) || !Number.isInteger(month) || month < 1 || month > 12 || !Number.isInteger(pages) || pages < 0) {
      throw new Error("Invalid monthly page record.");
    }
    const key = `${year}-${month}`;
    if (pageMap.has(key)) throw new Error(`Duplicate month: ${key}`);
    pageMap.set(key, pages);
    yearSet.add(year);
  }
  bookLookup = new Map();
  const seenIds = new Set();
  for (const book of books) {
    const year = Number(book.year), month = Number(book.month);
    if (!book.id || seenIds.has(book.id) || !book.title || !book.author || !Number.isInteger(year) || !Number.isInteger(month) || month < 1 || month > 12 || book.status !== "Completed") {
      throw new Error("Invalid or duplicate completed-book record.");
    }
    seenIds.add(book.id);
    yearSet.add(year);
    const key = `${year}-${month}`;
    if (!bookLookup.has(key)) bookLookup.set(key, []);
    bookLookup.get(key).push(book);
  }
  for (const entries of bookLookup.values()) entries.sort((a, b) => Number(a.month_order) - Number(b.month_order) || a.id.localeCompare(b.id));
  return [...yearSet].sort((a, b) => a - b).map(year => {
    const months = MONTHS.map((_, i) => {
      const month = i + 1;
      const count = (bookLookup.get(`${year}-${month}`) || []).length;
      return { month, books: count, pages: pageMap.get(`${year}-${month}`) ?? 0 };
    });
    return { year, books: months.reduce((a, m) => a + m.books, 0), pages: months.reduce((a, m) => a + m.pages, 0), months, notion: NOTION_BY_YEAR[String(year)] };
  });
}

function drawBars() {
  const max = Math.max(1, ...years.map(y => y[chartMetric]));
  $("#bars").replaceChildren(...years.map(y => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "barrow" + (y.year === activeYear ? " active" : "");
    btn.setAttribute("aria-pressed", String(y.year === activeYear));
    btn.setAttribute("aria-label", `${y.year}: ${y.books} ${bookUnit(y.books)}, ${fmt(y.pages)} pages recorded`);
    const label = document.createElement("span"); label.className = "yearlabel"; label.textContent = y.year;
    const track = document.createElement("span"); track.className = "track";
    const fill = document.createElement("span"); fill.className = "fill";
    fill.style.width = (100 * y[chartMetric] / max) + "%";
    track.append(fill);
    const qty = document.createElement("span"); qty.className = "qty"; qty.textContent = fmt(y[chartMetric]);
    btn.append(label, track, qty);
    btn.onclick = () => {
      activeYear = y.year;
      activeMonth = y.months.find(m => m.books > 0)?.month || 1;
      showAllBooks = false;
      draw();
    };
    return btn;
  }));
}

function draw() {
  drawBars();
  const y = years.find(x => x.year === activeYear);
  $("#selectedYear").textContent = String(y.year);
  $("#selectedBooks").textContent = fmt(y.books) + " " + bookUnit(y.books);
  $("#selectedPages").textContent = fmt(y.pages) + " pages";
  $("#monthgrid").replaceChildren(...y.months.map(m => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "month" + (m.month === activeMonth ? " active" : "");
    btn.setAttribute("aria-pressed", String(m.month === activeMonth));
    const heading = document.createElement("small"); heading.textContent = MONTHS[m.month - 1].slice(0, 3);
    const count = document.createElement("b"); count.textContent = fmt(m.books) + " " + bookUnit(m.books);
    const pages = document.createElement("em"); pages.className="month-pages"; pages.textContent=fmt(m.pages)+" pages"; btn.append(heading, count, pages);
    btn.onclick = () => { activeMonth = m.month; showAllBooks = false; drawMonth(); };
    return btn;
  }));
  drawMonth();
  $("#notionlink").replaceChildren();
  if (y.notion) {
    const link = document.createElement("a");
    link.href = y.notion;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = `View ${y.year} reading notes on Notion`;
    $("#notionlink").append(link);
  }
}

function renderBooks(target, books) {
  target.replaceChildren(...books.map((b, i) => {
    const item = document.createElement("li"); item.className = "bookitem";
    const number = document.createElement("span"); number.className = "bookindex"; number.textContent = String(i + 1).padStart(2, "0");
    const info = document.createElement("span"); info.className = "bookinfo";
    const title = document.createElement("span"); title.className = "booktitle"; title.textContent = b.title;
    const author = document.createElement("span"); author.className = "bookauthor"; author.textContent = b.author;
    info.append(title, author); item.append(number, info);
    return item;
  }));
}

function drawBookList() {
  const completed = bookLookup.get(`${activeYear}-${activeMonth}`) || [];
  const hasMore = completed.length > 12;
  const visible = hasMore && !showAllBooks ? completed.slice(0, 12) : completed;
  $("#booksHeading").textContent = `${MONTHS[activeMonth - 1]} ${activeYear} · Books read`;
  $("#bookCount").textContent = `${fmt(completed.length)} ${bookUnit(completed.length)} · Titles and authors`;
  renderBooks($("#booklist"), visible);
  $("#bookempty").hidden = completed.length > 0;
  $("#bookempty").textContent = "No books recorded for this month.";
  const more = $("#showmore");
  more.hidden = !hasMore;
  more.textContent = showAllBooks ? "Show fewer" : `Show all ${fmt(completed.length)} books`;
}

function drawMonth() {
  const y = years.find(x => x.year === activeYear);
  const m = y.months.find(x => x.month === activeMonth);
  document.querySelectorAll(".month").forEach((el, i) => {
    el.classList.toggle("active", i + 1 === activeMonth);
    el.setAttribute("aria-pressed", String(i + 1 === activeMonth));
  });
  const detail = $("#monthdetail");
  const heading = document.createElement("strong"); heading.textContent = `${MONTHS[activeMonth - 1]} ${activeYear}`;
  const line = document.createElement("div");
  const value = document.createElement("span");
  value.textContent = `${fmt(m.books)} ${bookUnit(m.books)} · ${fmt(m.pages)} pages recorded`;
  line.append(value);
  detail.replaceChildren(heading, line);
  drawBookList();
}

$("#showmore").onclick = () => { showAllBooks = !showAllBooks; drawBookList(); };
for (const metric of ["books","pages"]) { const button = $(metric === "books" ? "#metricBooks" : "#metricPages"); button.onclick=()=> {chartMetric=metric; $("#metricBooks").classList.toggle("active",metric==="books");$("#metricPages").classList.toggle("active",metric==="pages");$("#metricBooks").setAttribute("aria-pressed",String(metric==="books"));$("#metricPages").setAttribute("aria-pressed",String(metric==="pages"));drawBars();}; }

async function initialize() {
  try {
    const [bookRes, pageRes] = await Promise.all([
      fetch("./data/books.json", { cache: "no-cache" }),
      fetch("./data/monthly-pages.json", { cache: "no-cache" })
    ]);
    if (!bookRes.ok || !pageRes.ok) throw new Error(`Data unavailable (books: ${bookRes.status}, pages: ${pageRes.status}).`);
    const [bookData, pageData] = await Promise.all([bookRes.json(), pageRes.json()]);
    years = groupArchive(bookData.books, pageData.months);
    if (!years.length) throw new Error("No reading years found.");
    const totalBooks = years.reduce((n, y) => n + y.books, 0);
    const totalPages = years.reduce((n, y) => n + y.pages, 0);
    $("#totBooks").textContent = fmt(totalBooks);
    $("#totPages").textContent = fmt(totalPages);
    activeYear = years[years.length - 1].year;
    const recentMonths = years[years.length - 1].months.filter(m => m.books > 0);
    activeMonth = recentMonths.length ? recentMonths[recentMonths.length - 1].month : 1;
    $("#archiveStatus").hidden = true;
    draw();
  } catch (error) {
    console.error("Reading Archive could not load:", error);
    $("#archiveStatus").textContent = "Reading records are temporarily unavailable. Please refresh the page or try again later.";
    $("#archiveStatus").hidden = false;
  }
}
initialize();


// ReadingNotes are independent of the completed-book/page ledger.
async function initializeNotes(){
  const host=document.querySelector("#notesGroups");
  const search=document.querySelector("#noteSearch");
  const empty=document.querySelector("#notesEmpty");
  const total=document.querySelector("#notesCount");
  if(!host||!search||!empty||!total)return;
  const el=(tag,cls,value)=>{
    const node=document.createElement(tag);
    if(cls)node.className=cls;
    if(value!==undefined)node.textContent=value;
    return node;
  };
  try{
    const response=await fetch("./data/notes.json",{cache:"no-cache"});
    if(!response.ok)throw new Error("Notes data HTTP "+response.status);
    const data=await response.json();
    if(!Array.isArray(data.notes))throw new Error("Invalid notes schema");
    const notes=data.notes.filter(n=>n&&n.title&&n.author&&n.date);
    total.textContent=fmt(notes.length);
    function render(){
      const term=search.value.trim().toLocaleLowerCase();
      const chosen=notes.filter(n=>[n.title,n.author,n.reflection,n.quote].join(" ").toLocaleLowerCase().includes(term));
      const groups=new Map();
      chosen.forEach(n=>{
        const key=String(n.date).slice(0,7);
        if(!groups.has(key))groups.set(key,[]);
        groups.get(key).push(n);
      });
      host.replaceChildren();
      [...groups].sort((a,b)=>b[0].localeCompare(a[0])).forEach(([month,items],i)=>{
        const section=el("details","notes-month");section.open=!!term||i===0;
        const date=new Date(month+"-01T12:00:00");
        const label=isNaN(date.getTime())?month:date.toLocaleDateString("en-US",{year:"numeric",month:"long"});
        const heading=el("summary","notes-month-heading");
        heading.append(el("span","notes-month-title",label),el("span","notes-month-count",items.length+" "+bookUnit(items.length)));
        section.append(heading);
        const container=el("div","notes-cards");
        items.sort((a,b)=>b.date.localeCompare(a.date));
        items.forEach(note=>{
          const card=el("details","reading-note-card");card.open=!!term;
          const top=el("summary","note-card-heading");
          const info=el("span","note-card-left");
          info.append(el("strong","note-book-title",note.title),el("small","note-book-author",note.author||""));
          top.append(info,el("time","note-date",note.date));
          const content=el("div","note-body");
          if(note.quote){
            content.append(el("blockquote","note-quote",note.quote));
            content.append(el("div","note-provenance",note.verification==="Notion exact match"?"NOTION HIGHLIGHT · AUTO-MATCHED":"SELECTED PASSAGE"));
          }
          if(note.reflection){
            content.append(el("p","note-reflection",note.reflection));
          }else{
            content.append(el("p","note-transcription-pending","Written reflection not yet transcribed. Read the original Brunch post."));
          }
          if(note.brunch_url&&String(note.brunch_url).startsWith("https://brunch.co.kr/")){
            const link=el("a","note-brunch-link","Read original reflection ↗");
            link.href=note.brunch_url;link.target="_blank";link.rel="noopener noreferrer";content.append(link);
          }
          card.append(top,content);container.append(card);
        });
        section.append(container);host.append(section);
      });
      empty.hidden=chosen.length!==0;
    }
    search.addEventListener("input",render);render();
  }catch(error){
    console.error("Reading Notes unavailable",error);
    host.replaceChildren(el("p","notes-unavailable","Reading notes are temporarily unavailable."));
    total.textContent="—";
  }
}
initializeNotes();
