#!/usr/bin/env python3
"""Generate the black-only one-page public resume on GitHub Pages."""
import argparse
from pathlib import Path
import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

fonts=Path(reportlab.__file__).parent/'fonts'
pdfmetrics.registerFont(TTFont('ResumeVera',str(fonts/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('ResumeVeraBold',str(fonts/'VeraBd.ttf')))
pdfmetrics.registerFontFamily('ResumeVera',normal='ResumeVera',bold='ResumeVeraBold')
R='ResumeVera';B='ResumeVeraBold';K=colors.black
style={
 'name':ParagraphStyle('name',fontName=B,fontSize=19.2,leading=23,textColor=K,alignment=TA_CENTER,spaceAfter=4),
 'contact':ParagraphStyle('contact',fontName=R,fontSize=8.0,leading=11.4,textColor=K,alignment=TA_CENTER,spaceAfter=7),
 'tag':ParagraphStyle('tag',fontName=B,fontSize=8.3,leading=11.4,textColor=K,alignment=TA_CENTER,spaceAfter=6),
 'section':ParagraphStyle('section',fontName=B,fontSize=10.2,leading=12,textColor=K,spaceBefore=7.2,spaceAfter=3.5),
 'role':ParagraphStyle('role',fontName=B,fontSize=9.0,leading=11.9,textColor=K),
 'date':ParagraphStyle('date',fontName=R,fontSize=8.4,leading=11.9,alignment=TA_RIGHT,textColor=K),
 'bullet':ParagraphStyle('bullet',fontName=R,fontSize=8.9,leading=12.4,textColor=K,leftIndent=10.5,firstLineIndent=-8,spaceAfter=1.5),
 'skills':ParagraphStyle('skills',fontName=R,fontSize=8.8,leading=12,textColor=K,spaceAfter=1.2)
}
def t(s,kind):return Paragraph(s,style[kind])
def section(name):return [t(name,'section'),HRFlowable(width='100%',thickness=.65,color=K,spaceAfter=2.2)]
def entry(title,date,bullets):
 row=Table([[t(title,'role'),t(date,'date')]],colWidths=[435,105],hAlign='LEFT')
 row.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('VALIGN',(0,0),(-1,-1),'TOP')]))
 return KeepTogether([row]+[t('&#8226; '+b,'bullet') for b in bullets]+[Spacer(1,4.0)])
def build(out):
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 doc=BaseDocTemplate(str(out),pagesize=(612,792),leftMargin=36,rightMargin=36,topMargin=27,bottomMargin=25,title='Chaehyun Lim | Resume',author='Chaehyun Lim')
 doc.addPageTemplates(PageTemplate(id='resume',frames=[Frame(36,25,540,740,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)]))
 a=[
 t('CHAEHYUN LIM','name'),
 t('Atlanta, GA  |  clim70@gatech.edu  |  linkedin.com/in/lim-chaehyun  |  limdaniel10.github.io/Portfolio/','contact'),
 t('AEROSPACE SYSTEMS  |  HARDWARE INTEGRATION, TEST &amp; ELECTRIFICATION','tag'),
 *section('EDUCATION'),
 entry('Georgia Institute of Technology | M.S. Aerospace Engineering | Atlanta, GA','Expected May 2027',[]),
 entry('Georgia Institute of Technology | B.S. Aerospace Engineering | GPA 3.65/4.00, <b>Highest Honor</b>','May 2026',[]),
 t('<b>Coursework:</b> Aerospace Systems Engineering; Control Systems; Circuits &amp; Electronics; Instrumentation; Design &amp; Analysis of Experiments','skills'),
 *section('ENGINEERING EXPERIENCE &amp; PROJECTS'),
 entry('Moore Dynamics &amp; Analytics Lab | Undergraduate Researcher | Atlanta, GA','Oct 2024 - May 2026',[
  'Developed MATLAB and Arduino automation for a stepper-driven impact rig, integrating NI cDAQ acquisition, sensor calibration, visualization, and data logging.',
  'Resolved driver and MATLAB state faults; implemented camera-based pattern recognition and target-coordinate calculations, and positioned the UR30 robot during testing.',
  'Designed SolidWorks fixtures and optimized SLA printing; documented approximate impact test ranges of 250-1,500 N (coupled) and 3,000 N (released).']),
 entry('43rd VFS Student Design Competition | Propulsion Lead | Atlanta, GA','Aug 2025 - Jun 2026',[
  'Developed a conceptual hybrid-electric tiltrotor power architecture and MATLAB mission-energy models across hover, conversion, and cruise; assessed turbogenerator and battery power allocation.',
  'Compared propulsion alternatives and coordinated power/mass interfaces with other teams; team placed <b>2nd globally</b> in the undergraduate division.']),
 entry('Reaction-Wheel Heading Control | Senior Capstone | Atlanta, GA','Jan - May 2026',[
  'Integrated Arduino, IMU, ESC, and BLDC hardware for a single-axis PI-II reaction-wheel prototype; performed integration, troubleshooting, and control-response testing.',
  'Team results: 2.7 s rise, 5.9 s settling, &lt;8.24% overshoot, &plusmn;2.8 deg heading error. Ranked #1 in class; <b>Top 5</b> capstone project.']),
 entry('Vertical Lift Research Center of Excellence | Battery Test Operator','Jan - May 2025',[
  'Performed 6S Li-polymer battery-pack cycle-life tests using a published protocol (up to 1C charge, 750 W discharge); kept test records and analyzed resistance trends in Excel.']),
 entry('UAV System Design &amp; Flight Operations | Pilot &amp; System Designer','Aug 2024 - Dec 2025',[
  'Integrated a UAV airframe, 3D-printed battery enclosure, and thermal/optical payloads; executed preflight checks and programmed waypoint missions.']),
 *section('LEADERSHIP &amp; DOCUMENTATION'),
 entry('ROK Defense Intelligence Command | Squad Leader &amp; Intelligence Editor','Oct 2020 - Apr 2022',[
  'Led an 11-person squad, authored a 100-page operating guide, and oversaw 33 defense/aerospace reports; interpreted during a U.S.-ROK combined exercise. <b>Recognized by the Chairman of the ROK Joint Chiefs of Staff.</b>']),
 *section('SKILLS &amp; CERTIFICATIONS'),
 t('<b>Testing:</b> NI cDAQ, multimeter, power supply; data acquisition, calibration, and system integration.','skills'),
 t('<b>Tools:</b> MATLAB, Arduino C++, Excel, SolidWorks, Autodesk Inventor, SLA printing, Python.','skills'),
 t('<b>Certifications:</b> FAA Part 107; EASA A1/A3; ROK UAV Pilot Qualification (20+ logged flight hours).','skills'),
 t('<b>Languages:</b> Korean (native); English (fluent); Mandarin Chinese (HSK 5).','skills')
 ]
 doc.build(a)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='_site/assets/resume.pdf');args=ap.parse_args()
 build(args.out)
 print('Built monochrome resume:',args.out)
