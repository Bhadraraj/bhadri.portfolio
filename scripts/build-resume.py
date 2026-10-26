from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader
import json

root=Path(__file__).resolve().parents[1]
out=root/'assets/resume/Bhadra Raj_Resume.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='NameX',fontName='Helvetica-Bold',fontSize=26,leading=30,textColor=colors.HexColor('#123b42'),spaceAfter=5))
styles.add(ParagraphStyle(name='RoleX',fontSize=12,leading=16,textColor=colors.HexColor('#38716a'),spaceAfter=8))
styles.add(ParagraphStyle(name='BodyX',fontName='Helvetica',fontSize=9.3,leading=13,spaceAfter=5,textColor=colors.HexColor('#27353a')))
styles.add(ParagraphStyle(name='SmallX',parent=styles['BodyX'],fontSize=8.4,leading=11,spaceAfter=4))
styles.add(ParagraphStyle(name='HeadingX',fontName='Helvetica-Bold',fontSize=11,leading=15,spaceBefore=12,spaceAfter=7,textColor=colors.HexColor('#123b42')))
styles.add(ParagraphStyle(name='JobX',parent=styles['BodyX'],fontName='Helvetica-Bold',spaceAfter=2))
story=[]
def p(text,style='BodyX'): return Paragraph(text,styles[style])
def add(text,style='BodyX'): story.append(p(text,style))
def heading(text): add(text,'HeadingX')
def job(title,date,bullets):
    story.append(KeepTogether([p(title,'JobX'),p(date,'SmallX')]+[p('• '+b) for b in bullets]))
add('BHADRA RAJ R','NameX')
add('Full Stack Developer | 4 years of experience','RoleX')
add('<link href="mailto:20bhadri2001@gmail.com">20bhadri2001@gmail.com</link> | +91 7449143583 | Kanyakumari, Tamil Nadu, India','SmallX')
add('<link href="https://github.com/Bhadraraj" color="#23685e">GitHub: github.com/Bhadraraj</link> | <link href="https://www.linkedin.com/in/bhadra-raj-r" color="#23685e">LinkedIn: bhadra-raj-r</link>','SmallX')
add('<link href="https://bhadraraj.github.io/bhadri.portfolio/" color="#23685e">Portfolio: bhadraraj.github.io/bhadri.portfolio</link>','SmallX')
heading('PROFILE')
add('Full Stack Developer with 4 years of experience delivering responsive websites, e-commerce platforms, and management applications. Hands-on experience with React, Next.js, Angular, TypeScript, Node.js, NestJS, and relational databases. Builds reusable interfaces, REST APIs, and role-based workflows, with additional experience in Flutter applications and AWS deployment. Working independently as a freelance developer since June 2026.')
heading('TECHNICAL SKILLS')
for text in [
'<b>Frontend:</b> React.js, Next.js, Angular, JavaScript, TypeScript, Redux, HTML5, CSS3, Tailwind CSS, Bootstrap, Material UI',
'<b>Backend &amp; APIs:</b> Node.js, NestJS, Express.js, PHP, REST APIs; Java-based application integration',
'<b>Databases:</b> PostgreSQL, MySQL, MongoDB',
'<b>Mobile &amp; Cloud:</b> Flutter, AWS (EC2, S3, RDS), Vercel, Netlify',
'<b>Tools:</b> Git, GitHub, GitLab, Postman, Figma, VS Code; Docker basics, CI/CD workflows']:
    add(text)
heading('PROFESSIONAL EXPERIENCE')
job('Freelance Full Stack Developer','June 2026 - Present',[
'Develop responsive client websites and management applications using React, TypeScript, Tailwind CSS, Node.js, NestJS, PostgreSQL, and MySQL.',
'Translate client requirements into interfaces, integrate REST APIs, and maintain deployed applications across business domains.'])
job('Full Stack Developer | Planext4u','October 2025 - May 2026',[
'Developed an e-commerce ecosystem with vendor, customer, and admin platforms, including Flutter mobile apps and Next.js web applications.',
'Built Node.js REST APIs and PostgreSQL data models for products, users, vendors, orders, and business workflows; integrated AWS deployment and storage.',
'Implemented authentication, role-based access, and reusable components using TypeScript and Tailwind CSS.'])
job('Full Stack Web Developer | Gift Web Solution Pvt. Ltd.','April 2024 - September 2025',[
'Built responsive web applications using React.js, Next.js, and TypeScript, with Node.js, Express.js, MongoDB, MySQL, and PHP backends.',
'Integrated REST APIs, translated Figma designs into responsive pages, improved application performance, and mentored junior frontend developers.'])
job('Front End Web Developer | Igeet Online, Nagercoil','January 2023 - March 2024',[
'Developed e-commerce admin and seller panels using Angular, TypeScript, Material UI, and Bootstrap; implemented role-based access and collaborated through GitLab.'])
job('Freelancer and Trainer','July 2022 - December 2022',[
'Delivered websites for clients across business domains and trained 20+ students in HTML, CSS, JavaScript, React, and Git/GitHub.'])
story.append(PageBreak())
add('SELECTED PROJECTS','HeadingX')
add('Live websites and applications | Full portfolio linked on page 1','SmallX')
projects=json.loads((root/'assets/project/projects.json').read_text())
for name,slug,url,tech,desc in projects:
    lines=[p(f'<b>{name}</b> | <link href="{url}" color="#23685e">{url.replace("https://", "").rstrip("/")}</link>','BodyX'),p(desc,'SmallX')]
    if tech: lines.append(p('<b>Stack:</b> '+tech,'SmallX'))
    lines.append(Spacer(1,2))
    story.append(KeepTogether(lines))
heading('ADDITIONAL APPLICATION EXPERIENCE')
add('E-commerce dashboards with OTP/JWT authentication and payment integration; restaurant POS with QR ordering and kitchen displays; hospital dashboards; billing and inventory applications.','SmallX')
heading('EDUCATION')
add('<b>B.E. in Electronics and Communication Engineering</b>','BodyX')
add("Stella Mary's College of Engineering, Nagercoil | 2018 - 2022 | 78%",'SmallX')
heading('CERTIFICATIONS &amp; TRAINING')
add('Python Full Stack Development - Network Systems. Angular, React.js, AWS Cloud Practitioner, Linux, and Git &amp; GitHub courses - Maanavan Learn Code.','SmallX')
def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#cbd9d8'));c.line(40,33,A4[0]-40,33)
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#54706c'));c.drawString(40,21,'BHADRA RAJ R | FULL STACK DEVELOPER');c.drawRightString(A4[0]-40,21,str(doc.page))
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=30,bottomMargin=43,title='Bhadra Raj R - Full Stack Developer',author='Bhadra Raj R')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(out)
assert len(reader.pages)==2, f'Expected two pages, got {len(reader.pages)}'
assert 'June 2026 - Present' in '\n'.join(p.extract_text() for p in reader.pages)
print(f'Created {out}: {len(reader.pages)} pages')
