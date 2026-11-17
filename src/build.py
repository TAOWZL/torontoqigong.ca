#!/usr/bin/env python3
"""Builds the torontoqigong.ca static site into ../tq. Edit SITE and PAGES, rerun."""
import json, os, datetime

OUT = os.path.join(os.path.dirname(__file__), "..", "docs")
TODAY = datetime.date.today().isoformat()

SITE = {
    "name": "Toronto Qigong",
    "domain": "https://torontoqigong.ca",
    "operator": "Wuji Xuan Life Wellness Ltd",
    "street": "255 Broadview Ave, Ground Floor",
    "city": "Toronto", "region": "ON", "country": "CA",
    "postal": "M4M 2G6",
    "phone": "416-595-5525", "phone_e164": "+14165955525",
    "email": "admin@wujixuan.org",
    "trial_url": "https://buy.stripe.com/8x228qePkgwX3b0cWZ3Nm0E", "monthly_url": "https://buy.stripe.com/7sY7sK0YueoP9zo1eh3Nm0F",  # OPEN ITEM: swap for an @torontoqigong.ca address if one is set up
    "noindex": False,         # flip to False at launch
    "sameAs": [],            # OPEN ITEM: Google listing URL, Instagram, Facebook, Eventbrite organiser page
}

NAV = [("neigong-class.html","Saturday class"),("private-qigong-lessons.html","Private lessons"),("online-qigong-class.html","Online"),
       ("qigong-forms.html","Forms"),("qigong-class-cost.html","Cost"),("what-is-neigong.html","What is neigong")]

def addr_line():
    p = f" {SITE['postal']}" if SITE["postal"] else ""
    return f"{SITE['street']}, {SITE['city']}, {SITE['region']}{p}"

def business_schema():
    a = {"@type":"PostalAddress","streetAddress":SITE["street"],"addressLocality":SITE["city"],
         "addressRegion":SITE["region"],"addressCountry":SITE["country"]}
    if SITE["postal"]: a["postalCode"] = SITE["postal"]
    s = {"@type":["LocalBusiness","EducationalOrganization"],"@id":SITE["domain"]+"/#school",
         "name":SITE["name"],"url":SITE["domain"]+"/","telephone":SITE["phone_e164"],"email":SITE["email"],
         "address":a,"areaServed":["Toronto","Riverdale","Leslieville","East York","Canada"],"availableChannel":{"@type":"ServiceChannel","name":"Live online classes","serviceUrl":"https://torontoqigong.ca/online-qigong-class.html"},
         "parentOrganization":{"@type":"Organization","name":SITE["operator"]},
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"10:00","closes":"11:00"}],
         "description":"Neigong and qigong classes in Toronto at 255 Broadview Ave and live online. Saturday group class in person and online, private lessons in person or online through the week.",
         "makesOffer":[
           {"@type":"Offer","name":"Trial class","price":"20.00","priceCurrency":"CAD","description":"One Saturday neigong class. Plus HST."},
           {"@type":"Offer","name":"Monthly neigong subscription","price":"150.00","priceCurrency":"CAD",
            "priceSpecification":{"@type":"UnitPriceSpecification","price":"150.00","priceCurrency":"CAD","unitText":"MONTH"},
            "description":"Saturday class every week, the other group classes on the schedule, plus one 1-hour Reiki session or one 30-minute divination coaching session each month. Plus HST."}]}
    if SITE["sameAs"]: s["sameAs"] = SITE["sameAs"]
    return s


def course_schema():
    sched={"@type":"Schedule","repeatFrequency":"P1W","byDay":"https://schema.org/Saturday","startTime":"10:00","endTime":"11:00","duration":"PT1H","scheduleTimezone":"America/Toronto"}
    return {"@type":"Course","@id":SITE["domain"]+"/#saturday-class","name":"Saturday Neigong Class","description":"A one-hour neigong class taught through qigong forms. Three to five movements per class, with coaching on the energetics of each.","provider":{"@id":SITE["domain"]+"/#school"},
            "offers":[{"@type":"Offer","category":"Trial","price":"20.00","priceCurrency":"CAD"},{"@type":"Offer","category":"Subscription","price":"150.00","priceCurrency":"CAD"}],
            "hasCourseInstance":[
              {"@type":"CourseInstance","courseMode":"onsite","courseSchedule":sched,"location":{"@type":"Place","name":"Toronto Qigong","address":{"@type":"PostalAddress","streetAddress":SITE["street"],"addressLocality":SITE["city"],"addressRegion":SITE["region"],"addressCountry":SITE["country"]}}},
              {"@type":"CourseInstance","courseMode":"online","courseSchedule":sched,"location":{"@type":"VirtualLocation","url":SITE["domain"]+"/online-qigong-class.html"}}]}

def faq_schema(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def faq_html(faqs):
    return "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faqs)

def page(slug, title, desc, h1, lede, body, faqs=None, crumbs=True, extra_schema=None, cta_h='Book a trial class', cta_p=None):
    cta_p = cta_p or "Pay online by card and you are booked. Questions first? Text " + SITE['phone'] + "."
    url = SITE["domain"] + "/" + ("" if slug=="index.html" else slug)
    graph = [business_schema()]
    if slug not in ("index.html","404.html"):
        graph.append({"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Toronto Qigong","item":SITE["domain"]+"/"},
            {"@type":"ListItem","position":2,"name":h1,"item":url}]})
    if slug in ('index.html','neigong-class.html','online-qigong-class.html'): graph.append(course_schema())
    if faqs: graph.append(faq_schema(faqs))
    if extra_schema: graph.extend(extra_schema)
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, separators=(",",":"))
    cur = ' aria-current="page"'
    navhtml = "".join('<a href="/' + h + '"' + (cur if h==slug else "") + '>' + t + '</a>' for h,t in NAV)
    robots = '<meta name="robots" content="noindex">' if (SITE["noindex"] or slug=="404.html") else ''
    canon = '' if slug=='404.html' else f'<link rel="canonical" href="{url}">'
    crumb = f'<p class="crumbs"><a href="/">Toronto Qigong</a> / {h1}</p>' if (crumbs and slug not in ("index.html","404.html")) else ""
    faqblock = f'<h2>Questions people ask</h2>\n{faq_html(faqs)}' if faqs else ""
    tel = SITE['phone_e164']; ph = SITE['phone']
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{canon}
{robots}
<meta name="theme-color" content="#BD1D21">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/newsreader-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/tokens.css">
<link rel="stylesheet" href="/assets/site.css">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE['domain']}/assets/og.png">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="in">
<a class="wordmark" href="/">Toronto Qigong<span class="zh" lang="zh-Hant">內功</span></a>
<nav aria-label="Main">{navhtml}</nav>
</div></header>
<main id="main" class="page">
<div class="lead">
{crumb}
<h1>{h1}</h1>
<p class="lede">{lede}</p>
</div>
<article>
{body}
{faqblock}
</article>
<aside class="card" aria-label="Class details">
<h2>Saturday neigong class</h2>
<dl>
<dt>When</dt><dd>Saturdays, 10 to 11 am</dd>
<dt>Where</dt><dd>255 Broadview Ave, ground floor</dd>
<dt>Online</dt><dd>Live, from anywhere</dd>
<dt>Trial</dt><dd>$20 + HST</dd>
<dt>Monthly</dt><dd>$150 + HST</dd>
</dl>
<a class="btn" href="{SITE['trial_url']}">Book the $20 trial</a>
<a class="alt" href="sms:{tel}">or text {ph}</a>
<p class="note">Private lessons Tuesday to Sunday by appointment. Closed Mondays.</p>
<p class="note" id="localtime" hidden></p>
<script src="/assets/localtime.js" defer></script>
</aside>
</main>
<section class="close" aria-label="Book"><div class="in">
<div><h2>{cta_h}</h2><p>{cta_p}</p></div>
<a class="btn" href="{SITE['trial_url']}">Book the $20 trial</a>
</div></section>
<footer>
<p><b>{SITE['name']}</b><br>{addr_line()}<br>Use the commercial door.</p>
<p><a href="tel:{tel}">{ph}</a><br><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
<p>The qigong and neigong school of {SITE['operator']}.</p>
</footer>
</body>
</html>
"""

from pages import PAGES  # content lives in pages.py

def main():
    os.makedirs(OUT, exist_ok=True)
    urls = []
    for p in PAGES:
        html = page(**p)
        with open(os.path.join(OUT, p["slug"]), "w", encoding="utf-8") as f: f.write(html)
        urls.append(SITE["domain"] + "/" + ("" if p["slug"]=="index.html" else p["slug"]))
    # 404 (real 404; host must serve it with status 404)
    nf = page(slug="404.html", title="Page not found | Toronto Qigong", desc="This page does not exist.",
              h1="That page is not here", lede="The link may be old. The class schedule, prices and booking are one click away.",
              body='<p>Try the <a href="/">home page</a>, the <a href="/neigong-class.html">Saturday class</a> or <a href="/qigong-class-cost.html">prices</a>.</p>', crumbs=False)
    open(os.path.join(OUT,"404.html"),"w",encoding="utf-8").write(nf)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls] + ["</urlset>"]
    open(os.path.join(OUT,"sitemap.xml"),"w").write("\n".join(sm)+"\n")
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
    print("built", len(urls), "pages")

if __name__ == "__main__":
    main()
